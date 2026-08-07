import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from apply_metadata import merge_frontmatter

SAMPLE = "---\nname: demo-skill\ndescription: Does X.\n---\n# DEMO\nBody text.\n"

class TestMerge(unittest.TestCase):
    def test_preserves_name_and_description(self):
        out = merge_frontmatter(SAMPLE, {"version": "0.1.0", "domain": "production", "grade": "G2",
                                         "status": "active", "last-reviewed": "2026-08-06",
                                         "owned-by-agent": "code-implementer"})
        self.assertIn("name: demo-skill", out)
        self.assertIn("description: Does X.", out)

    def test_inserts_all_standard_fields(self):
        out = merge_frontmatter(SAMPLE, {"version": "0.1.0", "domain": "production", "grade": "G2",
                                         "status": "active", "last-reviewed": "2026-08-06",
                                         "owned-by-agent": "code-implementer"})
        for f in ["version:", "grade:", "domain:", "status:", "last-reviewed:", "owned-by-agent:"]:
            self.assertIn(f, out.split("---")[1])

    def test_is_idempotent(self):
        meta = {"version": "0.1.0", "domain": "production", "grade": "G2",
                "status": "active", "last-reviewed": "2026-08-06", "owned-by-agent": "code-implementer"}
        once = merge_frontmatter(SAMPLE, meta)
        self.assertEqual(merge_frontmatter(once, meta), once)

    def test_keeps_existing_version_if_present(self):
        src = "---\nname: x\nversion: 0.2.0\n---\nbody\n"
        out = merge_frontmatter(src, {"version": "0.1.0", "domain": "d", "grade": "G2",
                                      "status": "active", "last-reviewed": "2026-08-06",
                                      "owned-by-agent": "code-implementer"})
        self.assertIn("version: 0.2.0", out)

if __name__ == "__main__":
    unittest.main()
