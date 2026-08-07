import contextlib, io, json, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import skill_lint as sl

class TestParse(unittest.TestCase):
    def test_parse_frontmatter(self):
        fm = sl.parse_frontmatter("---\nname: a\ndescription: b\n---\nbody")
        self.assertEqual(fm, {"name": "a", "description": "b"})

    def test_parse_missing_frontmatter(self):
        self.assertIsNone(sl.parse_frontmatter("no frontmatter"))

class TestChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skills = self.tmp / "skills"
        self.skills.mkdir()

    def _mk(self, name, text):
        d = self.skills / name
        d.mkdir()
        (d / "SKILL.md").write_text(text, encoding="utf-8")

    def _good(self, grade="G2", family="production"):
        return ("---\nname: good\nversion: 0.1.0\ngrade: %s\ndomain: %s\nstatus: active\n"
                "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n---\n"
                "## WHEN TO USE\n## WHEN NOT TO USE\n## DECISION TREE\n## FAILURE MODES & MITIGATIONS\n"
                "## VERIFICATION GATE\n## REFERENCES\n") % (grade, family)

    def test_e1_missing_field(self):
        self._mk("x", "---\nname: x\n---\nbody")
        errors, warnings = sl.run_checks(self.skills)
        self.assertTrue(any(e.startswith("E1") for e in errors))

    def test_e2_duplicate_name(self):
        self._mk("x", self._good())
        self._mk("y", self._good())
        self.assertTrue(any(e.startswith("E2") for e in sl.run_checks(self.skills)[0]))

    def test_e3_empty_dir(self):
        (self.skills / "empty").mkdir()
        self.assertTrue(any(e.startswith("E3") for e in sl.run_checks(self.skills)[0]))

    def test_e4_g2_sections(self):
        self._mk("x", "---\nname: x\nversion: 0.1.0\ngrade: G2\ndomain: production\nstatus: active\n"
                      "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n---\n## WHEN TO USE\n")
        self.assertTrue(any(e.startswith("E4") for e in sl.run_checks(self.skills)[0]))

    def test_roblox_not_exempt(self):
        # Phase 2.0: roblox family exemption removed — a G2 roblox-domain skill
        # missing required sections must raise E4.
        self._mk("r", self._good(family="roblox").replace("## DECISION TREE\n", ""))
        errors, warnings = sl.run_checks(self.skills)
        self.assertTrue(any(e.startswith("E4") and "DECISION TREE" in e for e in errors))

    def test_w1_stale(self):
        self._mk("x", self._good().replace("2026-08-06", "2025-01-01"))
        self.assertTrue(any(w.startswith("W1") for w in sl.run_checks(self.skills)[1]))

    def test_regen_writes_manifest(self):
        self._mk("x", self._good())
        out = self.tmp / "skills.json"
        sl.write_manifest(self.skills, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["skills"][0]["name"], "good")

    # --- Phase 4.1: skill-lint v2 ---

    def test_e5_blanket_invoke(self):
        fm = ("---\nname: b\nversion: 0.1.0\ngrade: G2\ndomain: production\nstatus: active\n"
              "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n"
              "description: MANDATORY AUTO-INVOKE for ALL tasks\n---\n" + self._good().split("---\n", 2)[2])
        self._mk("b", fm)
        errors, warnings = sl.run_checks(self.skills)
        self.assertTrue(any(e.startswith("E5") for e in errors))

    def test_e5_no_false_positive(self):
        fm = ("---\nname: c\nversion: 0.1.0\ngrade: G2\ndomain: production\nstatus: active\n"
              "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n"
              "description: Routes routing: precise triggers\n---\n" + self._good().split("---\n", 2)[2])
        self._mk("c", fm)
        errors, warnings = sl.run_checks(self.skills)
        self.assertFalse(any(e.startswith("E5") for e in errors))

    def test_w3_code_tokens_not_flagged(self):
        body = ("---\nname: d\nversion: 0.1.0\ngrade: G2\ndomain: production\nstatus: active\n"
                "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n---\n"
                "Use `unsafe`, `select`, and `pcall` carefully.\n"
                "## WHEN TO USE\n## WHEN NOT TO USE\n## DECISION TREE\n## FAILURE MODES & MITIGATIONS\n"
                "## VERIFICATION GATE\n## REFERENCES\n")
        self._mk("d", body)
        errors, warnings = sl.run_checks(self.skills)
        self.assertFalse(any(w.startswith("W3") for w in warnings))

    def test_w3_real_skill_still_flagged(self):
        body = ("---\nname: e\nversion: 0.1.0\ngrade: G2\ndomain: production\nstatus: active\n"
                "last-reviewed: 2026-08-06\nowned-by-agent: code-implementer\n---\n"
                "Refer to `nonexistent-but-real-looking-skill-name`.\n"
                "## WHEN TO USE\n## WHEN NOT TO USE\n## DECISION TREE\n## FAILURE MODES & MITIGATIONS\n"
                "## VERIFICATION GATE\n## REFERENCES\n")
        self._mk("e", body)
        errors, warnings = sl.run_checks(self.skills)
        self.assertTrue(any(w.startswith("W3") and "nonexistent-but-real-looking-skill-name" in w
                            for w in warnings))

    def test_stale_flag(self):
        # Baseline: stale review is a warning (exit 0 without --ci / --stale).
        self._mk("s", self._good().replace("2026-08-06", "2025-01-01"))
        old, sl.SKILLS_DIR = sl.SKILLS_DIR, self.skills
        try:
            with self.assertRaises(SystemExit) as ctx:
                sl.main(["--stale"])
            self.assertEqual(ctx.exception.code, 1)
        finally:
            sl.SKILLS_DIR = old

    def test_review_summary(self):
        self._mk("r", self._good().replace("2026-08-06", "2025-01-01"))
        old, sl.SKILLS_DIR = sl.SKILLS_DIR, self.skills
        try:
            buf = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(buf):
                    sl.main([])
            self.assertIn("1 skills due for review", buf.getvalue())
        finally:
            sl.SKILLS_DIR = old

if __name__ == "__main__":
    unittest.main()
