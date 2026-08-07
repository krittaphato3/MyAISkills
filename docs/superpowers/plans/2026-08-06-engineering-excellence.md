# Engineering Excellence Transformation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the ZCode skills catalog from cheat-sheet quality to Staff/World-class engineering grade — every skill G2+ (no exemptions), 9 G3 skills, the 21-skill Roblox suite consolidated into one capability-focused skill, 3 new subagents (planner, solution-architect, ml-engineer), conflicts eliminated, and the catalog versioned, linted, and eval-backed for the future.

**Architecture:** (1) Consolidate to a single canonical store (`C:/Users/Oz/.zcode/skills/`), (2) enforce a grade ladder (G1→G2→G3) via a uniform skill skeleton checked by a lint tool, (3) rewrite doctrine to eliminate contradictions, (4) consolidate the Roblox suite into `roblox-lua-developer` + rebuild 3 stub skills + deepen 6 cheat-sheets to G2, (5) create 8 G3 skills (7 domain flagships + deep-planner) and 3 new subagents, (6) close with evals, lint gates, and a measured success-criteria report. Taxonomy lives in the manifest, not in directory renames.

**Tech Stack:** Markdown skills (frontmatter YAML), Python 3 stdlib only for tooling (`unittest` for tests), JSON manifest.

## Global Constraints

- Root directory: `C:/Users/Oz/.zcode`. Canonical skills store: `C:/Users/Oz/.zcode/skills/` — single source of truth after Phase 0.
- **No git repository exists** in `.zcode` or `.agents` (verified 2026-08-06). Every "commit" step in this plan is replaced by: run skill-lint → regenerate manifest → append to `docs/skills/CHANGELOG.md`. If the user approves git init in Phase 4 Task 4.4, later tasks may commit normally.
- Frontmatter standard (all skills): `name`, `description` (precise trigger, never "MANDATORY for ALL"), `version` (semver), `grade` (G1/G2/G3), `domain` (one of: doctrine, architecture, production, security, languages, delivery, roblox, meta), `status` (active/draft/superseded), `last-reviewed` (ISO date), `supersedes` (optional), `owned-by-agent` (one of the 23 agents or `system`).
- Grade ladder: **G2 = the floor for every skill — no exemptions.** G3 adds a `## QUANTITATIVE RULES` section. The Roblox suite is consolidated into a single G2 skill `roblox-lua-developer` (Task 2.0).
- Skill skeleton headings (lint-enforced): `## WHEN TO USE`, `## WHEN NOT TO USE`, `## DECISION TREE`, `## PATTERNS`, `## FAILURE MODES & MITIGATIONS`, `## QUANTITATIVE RULES` (G3 only), `## VERIFICATION GATE`, `## REFERENCES`.
- Precedence rules (documented in doctrine, Phase 1): task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults. Duplicate triggers are a lint error.
- Better-than guarantee: no capability is lost during consolidation; every touched skill gains content, none shrinks; existing triggers smoke-tested after every phase.
- Workflow discipline (anti-vibe-coding): all code work is TDD-first; verification-before-completion (proof, not assertion); Definition of Done before starting; red-team-qa at every gate; performance claims need before/after benchmarks; non-trivial work gets a plan first. Full standard: Task 1.1 (`## WORKFLOW STANDARDS`) + `docs/skills/WORKFLOW.md` (Task 1.4).
- Token efficiency: the orchestrator applies trivial edits inline (≤5 lines, doc-only corrections to plan-authored text) instead of dispatching a subagent; substantive code/content changes always go through subagents. Briefs are files, never pasted; one report per task; ledger writes batched.
- Smart routing: no skill may carry blanket-invoke language ("MANDATORY for ALL" / "invoke for ALL <domain> tasks"). lint v2 (Task 4.1) adds a W/E rule flagging blanket-invoke descriptions; every skill routes by precise trigger + domain + owner (system-instructions TRIGGER POLICY).
- Execution per AGENTS.md: all file work through subagents; red-team-qa before phase gates; main thread orchestrates only.

---

## Phase 0 — Hygiene & Baseline

Goal: single canonical store, zero duplicates, zero empty dirs, complete frontmatter everywhere, lint tool + manifest exist and pass.

### Task 0.1: Final inventory & diff-verification

**Files:**
- Create: `docs/skills/inventory-2026-08-06.json`

**Interfaces:**
- Consumes: nothing (raw filesystem).
- Produces: `inventory-2026-08-06.json` — the authoritative pre-change snapshot; Phase 0.2 and 0.3 consume its contents.

- [ ] **Step 1: Enumerate the catalog**

Run:
```bash
ls C:/Users/Oz/.zcode/skills/ > /tmp/zcode-skills.txt
ls C:/Users/Oz/.agents/skills/ > /tmp/agents-skills.txt
```
Expected: 40 dirs in `.zcode` (7 of which — banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max — are empty), 44 dirs in `.agents` (35 real duplicates, 3 unique: find-skills, skill-creator, mcp-builder; 4 empty: systems-core-architect, java-jvm-expert, ml-python-scientist, readme-architect).

- [ ] **Step 2: Diff-verify every duplicated pair**

Run:
```bash
for d in $(comm -12 /tmp/zcode-skills.txt /tmp/agents-skills.txt); do
  if [ -f "C:/Users/Oz/.zcode/skills/$d/SKILL.md" ] && [ -f "C:/Users/Oz/.agents/skills/$d/SKILL.md" ]; then
    diff -q "C:/Users/Oz/.zcode/skills/$d/SKILL.md" "C:/Users/Oz/.agents/skills/$d/SKILL.md" || echo "DRIFT: $d"
  fi
done
```
Expected: `DRIFT:` lines for any pair that has diverged. For each drifted pair: keep the copy with the newer mtime and the larger byte count; record the decision in the inventory file.

- [ ] **Step 3: Write the inventory snapshot**

Write `docs/skills/inventory-2026-08-06.json`:
```json
{
  "generated": "2026-08-06",
  "canonical": "C:/Users/Oz/.zcode/skills/",
  "zcode_skill_dirs": 40,
  "agents_skill_dirs": 44,
  "empty_dirs": ["banner-design","brand","design","design-system","slides","ui-styling","ui-ux-pro-max","systems-core-architect","java-jvm-expert","ml-python-scientist","readme-architect"],
  "unique_to_agents": ["find-skills","skill-creator","mcp-builder"],
  "duplicated_pairs": 35,
  "drifted_pairs": {"<name>": "<kept copy path>"},
  "skills": [
    {"name": "<name>", "path": "<absolute path>", "bytes": <size>, "source": "zcode|agents"}
  ]
}
```
The `skills` array must list every SKILL.md found in both trees (43 entries). No placeholders — fill real values from the enumeration.

- [ ] **Step 4: Record in changelog**

Append to `docs/skills/CHANGELOG.md` (create the file with this header first):
```markdown
# Skills Catalog Changelog
All catalog changes are recorded here. Format: `YYYY-MM-DD | <change> | <skills affected>`
```
Then add: `2026-08-06 | Phase 0.1: baseline inventory captured (43 skills, 35 dup pairs, 11 empty dirs) | all`.

### Task 0.2: Consolidate to canonical store

**Files:**
- Move: `C:/Users/Oz/.agents/skills/{find-skills,skill-creator,mcp-builder}/` → `C:/Users/Oz/.zcode/skills/`
- Delete: the 37 duplicated `.agents/skills/<name>/` directories, the 4 genuinely empty `.agents/skills/` dirs (java-jvm-expert, ml-python-scientist, readme-architect, systems-core-architect), then `.agents/skills/` itself
- Materialize: replace the 4 resolving symlinks in `.zcode/skills` (java-jvm-expert, ml-python-scientist, readme-architect, systems-core-architect — content physically lives in `C:/Users/Oz/.claude/skills/`) with real directories
- Unlink: the 7 broken symlinks in `.zcode/skills` (banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max — doubly-broken chains `.zcode → .claude → .agents`)
- Note: `C:/Users/Oz/.claude/skills/` is the user's primary store — NOT touched (out of scope). Its 7 dangling links remain as-is.

**Interfaces:**
- Consumes: `inventory-2026-08-06.json` (typed `empty_dirs` — broken_symlink vs empty_dir; `skills` array with byte counts).
- Produces: a single canonical catalog at `C:/Users/Oz/.zcode/skills/` with exactly 44 real populated skill directories; `.agents/skills/` gone.

- [ ] **Step 1: Move the three unique skills**

```bash
mkdir -p "C:/Users/Oz/.zcode/skills"
for d in find-skills skill-creator mcp-builder; do
  mv "C:/Users/Oz/.agents/skills/$d" "C:/Users/Oz/.zcode/skills/$d"
done
```
Verify: `ls C:/Users/Oz/.zcode/skills/ | wc -l` → 51 (37 real + 4 symlinks + 7 broken links + 3 moved; the 11 links are handled in Steps 3–4).

- [ ] **Step 2: Delete the 37 duplicated + 4 empty dirs in `.agents/skills`, then the root**

```bash
cd C:/Users/Oz/.agents/skills
for d in */; do
  d="${d%/}"
  if [ -d "C:/Users/Oz/.zcode/skills/$d" ]; then rm -rf "$d"; fi
done
cd C:/Users/Oz && rmdir .agents/skills 2>/dev/null || rm -rf .agents/skills
```
Verify: `ls C:/Users/Oz/.agents/skills 2>&1` → `No such file or directory`. (All `.agents` entries are real dirs, never symlinks — `rm -rf` is safe here. `.zcode` symlinks are NEVER touched with `rm -rf`.)

- [ ] **Step 3: Materialize the 4 resolving symlinks in `.zcode/skills`**

The dirs java-jvm-expert, ml-python-scientist, readme-architect, systems-core-architect are symlinks resolving to real dirs under `C:/Users/Oz/.claude/skills/`. Copy the dereferenced content into real dirs, then remove the links (plain `rm` on a symlink removes only the link):
```bash
cd C:/Users/Oz/.zcode/skills
for d in java-jvm-expert ml-python-scientist readme-architect systems-core-architect; do
  tmp="$d.new"
  mkdir -p "$tmp"
  cp -L "$d/SKILL.md" "$tmp/SKILL.md"
  rm "$d"
  mv "$tmp" "$d"
done
```
Verify: each of the 4 is now a real dir (`[ -d "$d" ] && [ ! -L "$d" ]`), and SKILL.md byte counts match the inventory (514/500/5097/505).

- [ ] **Step 4: Unlink the 7 broken symlinks**

```bash
cd C:/Users/Oz/.zcode/skills
for d in banner-design brand design design-system slides ui-styling ui-ux-pro-max; do
  rm "$d"
done
```
Verify: `ls C:/Users/Oz/.zcode/skills/ | wc -l` → 44; `ls C:/Users/Oz/.zcode/skills/*/SKILL.md | wc -l` → 44.

- [ ] **Step 5: Smoke test — catalog still loads**

```bash
for d in C:/Users/Oz/.zcode/skills/*/; do
  [ -s "$d/SKILL.md" ] || echo "EMPTY: $d"
done
```
Expected: no `EMPTY:` lines. (The 21 roblox skills stay in place until Task 2.0 consolidates them.)

- [ ] **Step 6: Changelog**

Add: `2026-08-06 | Phase 0.2: consolidated to canonical store — moved find-skills/skill-creator/mcp-builder from .agents; deleted 37 dup copies + 4 empty dirs + .agents/skills root; materialized 4 .claude symlinks (java-jvm-expert, ml-python-scientist, readme-architect, systems-core-architect); unlinked 7 broken symlinks (banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max). .claude/skills untouched | all`.

### Task 0.3: Frontmatter metadata (apply_metadata.py)

**Files:**
- Create: `tools/apply_metadata.py`
- Test: `tools/tests/test_apply_metadata.py`
- Modify: every `skills/<name>/SKILL.md` (43 files — mechanical frontmatter insertion, content untouched)

**Interfaces:**
- Consumes: canonical store from 0.2; the META mapping table below.
- Produces: `apply_metadata.py` (idempotent merger) + standard frontmatter on all 43 skills. Later content tasks (Phase 1–3) rewrite individual skills and carry the same fields forward.

- [ ] **Step 1: Write the failing tests**

`tools/tests/test_apply_metadata.py`:
```python
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
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `python -m unittest tools/tests/test_apply_metadata.py -v`
Expected: FAIL — `ModuleNotFoundError: apply_metadata`.

- [ ] **Step 3: Write the implementation**

`tools/apply_metadata.py`:
```python
#!/usr/bin/env python3
"""One-off: insert the standard frontmatter fields into every skill. Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
FIELD_ORDER = ["name", "description", "version", "grade", "domain", "status",
               "last-reviewed", "supersedes", "owned-by-agent"]
DEFAULTS = {"version": "0.1.0", "grade": "G2", "status": "active", "last-reviewed": "2026-08-06"}

META = {
  # delivery
  "animation-web-builder": {"domain": "delivery", "owned-by-agent": "ui-ux-architect"},
  "game-developer": {"domain": "delivery", "owned-by-agent": "game-developer"},
  "mobile-developer": {"domain": "delivery", "owned-by-agent": "mobile-developer"},
  "readme-architect": {"domain": "delivery", "owned-by-agent": "documentation-engineer"},
  # architecture
  "api-design-architect": {"domain": "architecture", "owned-by-agent": "api-architect"},
  "resilience-pattern-engineer": {"domain": "architecture", "owned-by-agent": "code-implementer"},
  "refactoring-intelligence": {"domain": "architecture", "owned-by-agent": "refactoring-specialist"},
  # production
  "performance-profiler": {"domain": "production", "owned-by-agent": "performance-engineer"},
  "query-performance-engineer": {"domain": "production", "owned-by-agent": "db-architect"},
  "devops-pipeline-engineer": {"domain": "production", "owned-by-agent": "devops-engineer"},
  "container-optimizer": {"domain": "production", "owned-by-agent": "devops-engineer"},
  "monorepo-workspace-architect": {"domain": "production", "owned-by-agent": "devops-engineer"},
  "github-flow-master": {"domain": "production", "owned-by-agent": "code-implementer"},
  "dependency-supply-chain-guardian": {"domain": "production", "owned-by-agent": "dependency-guardian"},
  # security
  "cybersecurity-specialist": {"domain": "security", "owned-by-agent": "cybersecurity-specialist"},
  "security-hardening-specialist": {"domain": "security", "owned-by-agent": "security-auditor"},
  # languages
  "systems-core-architect": {"domain": "languages", "owned-by-agent": "code-implementer", "grade": "G1"},
  "java-jvm-expert": {"domain": "languages", "owned-by-agent": "code-implementer", "grade": "G1"},
  "ml-python-scientist": {"domain": "languages", "owned-by-agent": "ml-engineer", "grade": "G1"},  # ml-engineer agent created in Phase 3 (lint W2 tolerated until then)
  # doctrine
  "system-instructions": {"domain": "doctrine", "owned-by-agent": "system"},
  # meta
  "skill-creator": {"domain": "meta", "owned-by-agent": "system"},
  "find-skills": {"domain": "meta", "owned-by-agent": "system"},
  "mcp-builder": {"domain": "meta", "owned-by-agent": "mcp-agent"},
}

def merge_frontmatter(text: str, meta: dict) -> str:
    m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)$", text, re.S)
    if not m:
        return "---\n" + "\n".join(f"{k}: {v}" for k, v in meta.items() if v) + "\n---\n" + text
    fields = {}
    for line in m.group(2).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    # Preserve existing fields; fill only missing ones from meta (idempotent).
    for k in FIELD_ORDER:
        if k not in fields:
            fields[k] = meta.get(k)
    body = "\n".join(f"{k}: {v}" for k, v in fields.items() if v is not None)
    return m.group(1) + body + m.group(3) + m.group(4)


if __name__ == "__main__":
    for d in SKILLS_DIR.iterdir():
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        meta = dict(DEFAULTS)
        meta.update(META.get(d.name, {"domain": "roblox", "owned-by-agent": "game-developer"}))
        out = merge_frontmatter(text, meta)
        if out != text:
            f.write_text(out, encoding="utf-8")
```
Note: the `roblox` default branch covers all 21 roblox skills (domain roblox, owner game-developer) — no per-skill entries needed.

- [ ] **Step 4: Run tests, verify they pass**

Run: `python -m unittest tools/tests/test_apply_metadata.py -v`
Expected: PASS (4/4).

- [ ] **Step 5: Apply to the catalog**

Run: `python tools/apply_metadata.py`
Verify spot checks:
```bash
head -12 C:/Users/Oz/.zcode/skills/performance-profiler/SKILL.md
head -12 C:/Users/Oz/.zcode/skills/roblox-coding/SKILL.md
head -12 C:/Users/Oz/.zcode/skills/systems-core-architect/SKILL.md
```
Expected: each has complete frontmatter with the mapped values (systems-core-architect shows `grade: G1`).

- [ ] **Step 6: Re-run to prove idempotency**

Run: `python tools/apply_metadata.py && git diff 2>/dev/null || echo "no git — compare checksums"`
Verify no changes on second run (compare `md5sum skills/*/SKILL.md` before/after — identical).

- [ ] **Step 7: Changelog**

Add: `2026-08-06 | Phase 0.3: standard frontmatter applied to 43 skills (apply_metadata.py) | all`.

### Task 0.4: skill-lint v1 (TDD)

**Files:**
- Create: `tools/skill_lint.py`
- Test: `tools/tests/test_skill_lint.py`

**Interfaces:**
- Consumes: canonical store (0.2), frontmatter standard (0.3).
- Produces: `skill_lint.py` — the quality gate every later task and phase runs. Exit codes: 0 = pass, 1 = errors, 2 = warnings-only (with `--ci`). Flags: `--json` (machine output), `--regen` (regenerate `docs/skills/skills.json`).

- [ ] **Step 1: Write the failing tests**

`tools/tests/test_skill_lint.py` — cover: frontmatter parse; E1 missing field; E2 duplicate name; E3 empty dir; E4 G2 sections missing; roblox exemption (no E4 for roblox family); W1 stale last-reviewed; `--regen` writes skills.json; exit codes.
```python
import json, subprocess, sys, tempfile, unittest
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

    def test_roblox_exempt(self):
        self._mk("r", self._good(family="roblox"))
        errors, warnings = sl.run_checks(self.skills)
        self.assertFalse(any(e.startswith("E4") for e in errors))

    def test_w1_stale(self):
        self._mk("x", self._good().replace("2026-08-06", "2025-01-01"))
        self.assertTrue(any(w.startswith("W1") for w in sl.run_checks(self.skills)[1]))

    def test_regen_writes_manifest(self):
        self._mk("x", self._good())
        out = self.tmp / "skills.json"
        sl.write_manifest(self.skills, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["skills"][0]["name"], "good")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `python -m unittest tools/tests/test_skill_lint.py -v`
Expected: FAIL — `ModuleNotFoundError: skill_lint`.

- [ ] **Step 3: Write the implementation**

`tools/skill_lint.py`:
```python
#!/usr/bin/env python3
"""skill-lint: validate the ZCode skills catalog.

Errors (exit 1): E1 frontmatter, E2 duplicate names, E3 empty dirs, E4 grade sections.
Warnings (exit 2 with --ci): W1 stale last-reviewed, W2 unknown owner agent, W3 reference to unknown skill.
--json: machine-readable report. --regen: regenerate docs/skills/skills.json.
"""
import argparse, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MANIFEST_DIR = ROOT / "docs" / "skills"
REQUIRED = ["name", "version", "grade", "domain", "status", "last-reviewed", "owned-by-agent"]
GRADES = {"G1", "G2", "G3"}
STATUSES = {"active", "draft", "superseded"}
FAMILIES = {"doctrine", "architecture", "production", "security", "languages", "delivery", "roblox", "meta"}
EXEMPT_FAMILIES = {"roblox"}
SECTIONS = {
    "G2": ["## WHEN TO USE", "## WHEN NOT TO USE", "## DECISION TREE", "## FAILURE MODES & MITIGATIONS", "## VERIFICATION GATE", "## REFERENCES"],
    "G3": ["## WHEN TO USE", "## WHEN NOT TO USE", "## DECISION TREE", "## FAILURE MODES & MITIGATIONS",
           "## QUANTITATIVE RULES", "## VERIFICATION GATE", "## REFERENCES"],
}
STALE_DAYS = 90
AGENTS = {"code-implementer","db-architect","deep-researcher","red-team-qa","ui-ux-architect",
          "performance-engineer","devops-engineer","security-auditor","api-architect",
          "refactoring-specialist","accessibility-specialist","dependency-guardian",
          "cybersecurity-specialist","mcp-agent","browser-automation","test-engineer",
          "documentation-engineer","data-engineer","game-developer","mobile-developer",
          "planner","solution-architect","ml-engineer","system"}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def run_checks(skills_dir):
    errors, warnings = [], []
    names = {}
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir():
            continue
        if not (d / "SKILL.md").is_file():
            errors.append(f"E3 {d.name}: directory has no SKILL.md")
            continue
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"E1 {d.name}: missing/invalid frontmatter")
            continue
        for f in REQUIRED:
            if not fm.get(f):
                errors.append(f"E1 {d.name}: missing frontmatter field '{f}'")
        if fm.get("grade") not in GRADES:
            errors.append(f"E1 {d.name}: invalid grade '{fm.get('grade')}'")
        if fm.get("status") not in STATUSES:
            errors.append(f"E1 {d.name}: invalid status '{fm.get('status')}'")
        if fm.get("domain") not in FAMILIES:
            errors.append(f"E1 {d.name}: invalid domain '{fm.get('domain')}'")
        if fm.get("owned-by-agent") not in AGENTS:
            warnings.append(f"W2 {d.name}: unknown owner '{fm.get('owned-by-agent')}'")
        if fm.get("last-reviewed"):
            try:
                age = (date.today() - date.fromisoformat(fm["last-reviewed"])).days
                if age > STALE_DAYS:
                    warnings.append(f"W1 {d.name}: last-reviewed {fm['last-reviewed']} ({age}d old)")
            except ValueError:
                errors.append(f"E1 {d.name}: last-reviewed not an ISO date")
        if fm.get("domain") not in EXEMPT_FAMILIES and fm.get("grade") in SECTIONS:
            low = text.lower()
            for h in SECTIONS[fm["grade"]]:
                if h.lower() not in low:
                    errors.append(f"E4 {d.name}: grade {fm['grade']} missing '{h}'")
        names[d.name] = fm
    seen = {}
    for dname, fm in names.items():
        n = fm.get("name", dname)
        if n in seen:
            errors.append(f"E2 duplicate skill name: {n} (dirs {seen[n]} and {dname})")
        else:
            seen[n] = dname
    for name, fm in names.items():
        for m in re.finditer(r"`([a-z0-9-]+)`", (skills_dir / name / "SKILL.md").read_text(encoding="utf-8")):
            if m.group(1) not in names and m.group(1) not in {"SLI", "SLO", "SLA", "REST", "gRPC", "GraphQL"}:
                warnings.append(f"W3 {name}: reference to unknown skill '{m.group(1)}'")
    return errors, warnings


def write_manifest(skills_dir, out_path):
    entries = []
    for d in sorted(skills_dir.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        fm = parse_frontmatter(f.read_text(encoding="utf-8")) or {}
        entries.append({"name": fm.get("name", d.name), "path": str(f).replace(str(ROOT) + "\\", "").replace("/", "/"),
                        "version": fm.get("version"), "grade": fm.get("grade"), "domain": fm.get("domain"),
                        "status": fm.get("status"), "last-reviewed": fm.get("last-reviewed"),
                        "owned-by-agent": fm.get("owned-by-agent")})
    out_path.write_text(json.dumps({"generated": date.today().isoformat(), "count": len(entries), "skills": entries},
                                   indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ci", action="store_true")
    ap.add_argument("--regen", action="store_true")
    args = ap.parse_args()
    errors, warnings = run_checks(SKILLS_DIR)
    if args.regen:
        MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
        write_manifest(SKILLS_DIR, MANIFEST_DIR / "skills.json")
    report = {"errors": errors, "warnings": warnings, "error_count": len(errors),
              "warning_count": len(warnings), "exit": 1 if errors else (2 if warnings and args.ci else 0)}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for e in errors:
            print(e, file=sys.stderr)
        for w in warnings:
            print(w, file=sys.stderr)
        print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(report["exit"])


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `python -m unittest tools/tests/test_skill_lint.py -v`
Expected: PASS (9/9).

- [ ] **Step 5: Run lint on the real catalog**

Run: `python tools/skill_lint.py --json`
Expected: G1 stubs produce no E4 (SECTIONS defines requirements only for G2/G3); every G2-marked skill missing sections produces `E4` errors — this is the expected Phase-0 baseline; Phase 2/3 tasks resolve them. Record the error list in the phase-gate report.

### Task 0.5: Manifest & changelog skeleton

**Files:**
- Create: `docs/skills/SKILLS.md`, `docs/skills/CHANGELOG.md` (started in 0.1), regenerate `docs/skills/skills.json`

**Interfaces:**
- Consumes: skill-lint `--regen` (0.4).
- Produces: the human-readable index consumed by Phase 1.3 (agent↔skill matrix) and every subsequent task's changelog entry.

- [ ] **Step 1: Generate skills.json**

Run: `python tools/skill_lint.py --regen`
Verify: `docs/skills/skills.json` contains 43 entries with all fields.

- [ ] **Step 2: Write SKILLS.md index**

`docs/skills/SKILLS.md` — a table generated from skills.json with columns: Skill | Version | Grade | Domain | Status | Owner | Last reviewed. Group by domain family. Add a legend: grade ladder (G1/G2/G3) and the precedence rules (from Global Constraints).

- [ ] **Step 3: Verify with lint**

Run: `python tools/skill_lint.py --regen; python tools/skill_lint.py`
(Note: use `;` not `&&` — `--regen` exits 1 on the baseline errors, which would short-circuit the chain.)
Expected: exit 1 with only the known Phase-0 baseline (119 E4 / 114 W3 / 0 E1–E3) — no new error categories.

- [ ] **Step 4: Changelog**

Add: `2026-08-06 | Phase 0.5: manifest skeleton (SKILLS.md, skills.json) created | all`.

**Phase 0 gate:** [ ] inventory file complete; [ ] 43 canonical skills, 0 duplicates, 0 empty dirs; [ ] apply_metadata tests pass and second run is a no-op; [ ] skill-lint tests pass; [ ] lint baseline recorded; [ ] manifest exists; [ ] changelog complete. → subagent: red-team-qa re-verifies the 0-duplicate/0-empty claim against the filesystem.

---

## Phase 1 — Governance & Doctrine

Goal: one consistent doctrine; no contradictory instructions anywhere; trigger discipline replaces "MANDATORY for ALL".

### Task 1.1: system-instructions v2

**Files:**
- Rewrite: `skills/system-instructions/SKILL.md`

**Interfaces:**
- Consumes: frontmatter standard (0.3), precedence rules (Global Constraints).
- Produces: the operational doctrine every other skill and the main thread follow; referenced by Task 1.2 (AGENTS.md alignment) and by `general-orchestrator` (Phase 3.7).

- [ ] **Step 1: Write the new frontmatter + intro**

Frontmatter: `name: system-instructions`, `version: 2.0.0`, `grade: G2`, `domain: doctrine`, `status: active`, `last-reviewed: 2026-08-06`, `owned-by-agent: system`. Description: "Operational doctrine: delegation protocol, confidence gates, waiting protocol, verification gates, trigger policy, and workflow standards. Invoke when orchestrating multi-step work or resolving instruction conflicts."

- [ ] **Step 2: Write the doctrine sections**

Must include, in order:
1. `## WHEN TO USE` — multi-step work, subagent dispatch, conflict resolution.
2. `## WHEN NOT TO USE` — single-step tasks that need no orchestration.
3. `## DECISION TREE` — multi-step vs single-step? conflict → precedence rules; needs research → deep-researcher; needs a plan → deep-planner; execution → orchestrate with verification gates.
4. `## PRECEDENCE RULES` — verbatim from Global Constraints: task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults; duplicate triggers = lint error.
5. `## DELEGATION PROTOCOL` — golden rule (main thread orchestrates, all file work through subagents); what the main thread may do directly (orchestration decisions, GitHub PR MCP, memory MCP, doc fetches) vs. what must go through subagents (file edits, builds, tests, browser, DB MCP); confidence thresholds table (≥80 proceed, 70–79 research, <50 stop).
6. `## WAITING PROTOCOL` — while agents run: no file exploration; memory MCP only; wait silently.
7. `## TRIGGER POLICY` — how skills declare triggers (frontmatter description, no "MANDATORY for ALL"); when to invoke one skill vs. several; when to use `general-orchestrator`.
8. `## VERIFICATION GATES` — before implementation (confidence ≥80), before commit (tests/lint/QA), phase gates (lint + red-team-qa).
9. `## WORKFLOW STANDARDS` — TDD-first (failing test → minimal impl → refactor → green); verification-before-completion (proof-based evidence, never "looks right"); Definition of Done before starting; measurement discipline (before/after benchmarks, pinned env); systematic debugging (root cause, not symptom patches); review gates (red-team-qa + requesting-code-review); plan-before-code for non-trivial tasks (deep-planner / writing-plans). Reference the superpowers workflow skills (test-driven-development, verification-before-completion, systematic-debugging, requesting-code-review).
10. `## FAILURE MODES & MITIGATIONS` — context overflow while orchestrating; duplicate subagent dispatch; agent drift (result doesn't match the brief); contradictory instructions (→ precedence rules); verification theater (asserting without evidence); silent partial failures.
11. `## VERIFICATION GATE` — the doctrine is verified when: red-team-qa contradiction review passes; lint passes on system-instructions (all G2 sections present); no "MANDATORY for ALL" descriptions anywhere; WORKFLOW.md exists and matches.
12. `## REFERENCES` — AGENTS.md, docs/skills/WORKFLOW.md, superpowers workflow skills (test-driven-development, verification-before-completion, systematic-debugging, requesting-code-review), docs/superpowers/plans/2026-08-06-engineering-excellence.md.
13. `## SAFETY` — destructive actions pause and ask.

- [ ] **Step 3: Lint + changelog**

Run: `python tools/skill_lint.py --regen`
Expected: no errors for system-instructions (G2 sections all present).
Add: `2026-08-06 | Phase 1.1: system-instructions v2 (doctrine, precedence, trigger policy) | system-instructions`.

### Task 1.2: AGENTS.md alignment

**Files:**
- Modify: `C:/Users/Oz/.zcode/AGENTS.md`

**Interfaces:**
- Consumes: system-instructions v2 (1.1).
- Produces: AGENTS.md consistent with v2 — no contradictions.

- [ ] **Step 1: Apply the alignment edits**

Keep AGENTS.md as the short principles file. Changes:
- Replace the "GOLDEN RULE" line with: `GOLDEN RULE: The main thread orchestrates; ALL file work and coding goes through subagents. Full delegation protocol: skills/system-instructions.`
- Add a `PRECEDENCE` line: `Task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults.`
- Add `GRADE STANDARD: every skill is G2+ (3 transitional G1 language skills upgrade in Phase 2; see docs/skills/SKILLS.md); quality gates enforced by tools/skill_lint.py.`
- Update the pipeline section to reference the phase gates (lint + red-team-qa).
- Leave the AGENTS (17) registry and coding ethics unchanged.

- [ ] **Step 2: Contradiction check**

Read the full AGENTS.md and full system-instructions v2; list every pair of statements that could contradict. Verify: nothing in AGENTS.md claims the main thread may not make orchestration decisions, and nothing in v2 claims AGENTS.md's ethics are overridden. Record the check result in the changelog entry.

- [ ] **Step 3: Changelog**

Add: `2026-08-06 | Phase 1.2: AGENTS.md aligned with system-instructions v2 (precedence + grade standard) | doctrine`.

### Task 1.3: Agent↔skill matrix

**Files:**
- Create: `docs/skills/AGENT-SKILL-MATRIX.md`

**Interfaces:**
- Consumes: skills.json (0.5), the 17 agent definitions in `C:/Users/Oz/.zcode/agents/*.md`.
- Produces: the matrix consumed by `general-orchestrator` (3.7) for routing.

- [ ] **Step 1: Build the matrix**

From skills.json group skills by `owned-by-agent`; for each agent list its skills. Include a routing rule per agent: which family/trigger routes to it. Flag any agent with zero skills (deep-researcher, red-team-qa, accessibility-specialist, data-engineer, test-engineer) with a note: "no owned skills — QA/research roles consume other skills' verification gates". Add 'planned' rows for the Phase-3 agents: planner, solution-architect, ml-engineer.

- [ ] **Step 2: Cross-check agent definitions**

Read each `C:/Users/Oz/.zcode/agents/*.md`; verify its description matches the domains of its owned skills. Record mismatches in the matrix as "needs alignment" notes (content fix in Phase 2/3 tasks).

- [ ] **Step 3: Create the 3 missing agent definitions**

`cybersecurity-specialist`, `game-developer`, `mobile-developer` are declared in AGENTS.md's registry and own 24 of the 44 skills (game-developer owns the 21 roblox skills + game-developer; cybersecurity-specialist owns cybersecurity-specialist; mobile-developer owns mobile-developer) but have NO `C:/Users/Oz/.zcode/agents/*.md` file. Create them following the existing file format (frontmatter: name, description, color, tools — same tool list as peers: Read, Grep, Glob, Bash, WebFetch, WebSearch; then a role prompt aligned with the AGENTS.md registry description and the owned skills' domains). Verify: 20 agent definition files exist; every `owned-by-agent` value in skills.json resolves to a real agent file or `system`.

- [ ] **Step 4: Changelog**

Add: `2026-08-06 | Phase 1.3: agent↔skill matrix created; 3 missing agent definitions restored (cybersecurity-specialist, game-developer, mobile-developer) | docs/skills/AGENT-SKILL-MATRIX.md, agents/*`.

### Task 1.4: Delivery-discipline doc (WORKFLOW.md)

**Files:**
- Create: `docs/skills/WORKFLOW.md`

**Interfaces:**
- Consumes: system-instructions v2 `## WORKFLOW STANDARDS` (1.1).
- Produces: the delivery-discipline reference that every content task and `general-orchestrator` (3.7) cite for DoD/verification rules.

- [ ] **Step 1: Write the doc**

`docs/skills/WORKFLOW.md` MUST include:
1. **Definition of Done checklist** — tests pass (or proof-based verification for non-code work), lint clean, review done, changelog recorded, evidence attached.
2. **TDD protocol** — failing test → minimal implementation → refactor → green; exceptions require justification.
3. **Verification-before-completion rules** — "done" requires evidence: test output, benchmark tables; screenshots only as supporting material, never the only proof; no "looks right" sign-offs.
4. **Measurement discipline** — performance claims: before/after benchmark, pinned environment, ≥5 runs, median + p90.
5. **Systematic debugging protocol** — reproduce → isolate → root cause → fix → regression test.
6. **Review gates** — red-team-qa at every phase gate; requesting-code-review for non-trivial changes.
7. **Anti-vibe-coding anti-patterns** — assert without evidence; merge untested code; screenshots as sole verification; "no-stop" execution without gates; symptom patches; unmeasured optimizations; skipping the plan for non-trivial work.
8. **Plan-before-code rule** — non-trivial tasks require a plan (deep-planner or writing-plans) before implementation.

- [ ] **Step 2: Changelog**

Add: `2026-08-06 | Phase 1.4: delivery-discipline doc (WORKFLOW.md) created | docs/skills/WORKFLOW.md`.

**Phase 1 gate:** [ ] red-team-qa review of system-instructions v2 + AGENTS.md finds zero contradictions; [ ] no skill description contains "MANDATORY for ALL" (grep `grep -ri "mandatory for all" skills/` → empty); [ ] WORKFLOW STANDARDS present in system-instructions v2 and WORKFLOW.md exists; [ ] vibe-coding phrases appear in doctrine only as prohibitions (grep `grep -inE "no-stop|looks done|looks right" skills/system-instructions/SKILL.md docs/skills/WORKFLOW.md` returns only prohibition lines); [ ] matrix complete; [ ] lint passes with no new errors beyond Phase-0 baseline.

---

## Phase 2 — Staff-Grade Content (G2/G3)

Goal: Roblox suite consolidated into one skill (21 → 1); every general skill meets the G2 floor; systems-core-architect reaches G3. Each task follows the same pattern: rewrite sections per the content contract, run lint, update manifest + changelog.

### Task 2.0: Roblox suite consolidation (21 → 1)

**Files:**
- Create: `skills/roblox-lua-developer/SKILL.md`
- Delete: the 21 `skills/roblox-*/` directories
- Modify: `tools/skill_lint.py` + `tools/tests/test_skill_lint.py` (remove the roblox family exemption)

**Interfaces:**
- Consumes: all 21 roblox skills (content sources), frontmatter standard (0.3), lint v1 (0.4).
- Produces: `roblox-lua-developer` (G2, domain roblox, owner game-developer) — the single entry point for all Roblox work; supersession recorded in manifest + changelog. `general-orchestrator` (3.7) and `game-developer` route Roblox tasks here.

- [ ] **Step 1: Read all 21 source skills**

Read every `skills/roblox-*/SKILL.md`. Extract and dedupe: shared MCP workflow boilerplate (search_game_tree, get_studio_state, get_console_output, execute_luau, screen_capture), shared verification protocol, and the per-domain unique content. Also read `C:/Users/Oz/.claude/skills/lua-architect/SKILL.md` (if present) as an additional Lua guidance source — reuse its content where it beats the roblox sources.

- [ ] **Step 2: Write the consolidated skill**

`skills/roblox-lua-developer/SKILL.md`, frontmatter: `name: roblox-lua-developer`, `version: 2.0.0`, `grade: G2`, `domain: roblox`, `status: active`, `last-reviewed: 2026-08-06`, `supersedes: "roblox suite 1.x (21 skills)"`, `owned-by-agent: game-developer`. Sections, in order:
1. `## WHEN TO USE` — any Roblox/Luau task: coding, UI, networking, persistence, economy, security, performance, VFX, animation, audio, terrain, assets, plugins, testing.
2. `## WHEN NOT TO USE` — non-Roblox game engines (→ game-developer); MCP server authoring (→ mcp-builder).
3. `## ROBLOX PLATFORM` — DataModel tree, core services (ReplicatedStorage, DataStoreService, TweenService, etc.), client/server replication model, RemoteEvents vs RemoteFunctions, streaming, physics determinism limits.
4. `## LUAU` — language features (type inference, tables, metatables, closures), performance idioms (avoid per-frame allocations, cache property access).
5. `## DOMAIN WORKFLOWS` — one compressed table per domain: UI/UX, networking, data persistence, economy, security, performance, VFX, animation, 3D assets, audio, terrain, plugins, testing, cinematics, avatar. Each row: key APIs, common pitfalls, MCP verification (execute_luau / console / screen_capture).
6. `## DECISION TREE` — route a task to the right domain workflow; client vs server placement; when to use orchestration (multi-domain tasks).
7. `## FAILURE MODES & MITIGATIONS` (≥10): replication race on client-authoritative state, DataStore rate limits/session locking, exploit vectors (remote spoofing — server authority), streaming pop-in, memory leaks from event connections, TweenService drift, UI layout race with streaming.
8. `## VERIFICATION GATE` — MCP protocol: get_console_output (zero errors), execute_luau integration tests, screen_capture visual check, red-team-qa security review for networking/economy changes.
9. `## REFERENCES` — Roblox docs (DataModel, services, Luau), Luau language docs, Roblox API reference.

- [ ] **Step 3: Delete the 21 old skill directories**

```bash
cd C:/Users/Oz/.zcode/skills
rm -rf roblox-3d-assets roblox-animation roblox-architecture roblox-asset-import roblox-audio roblox-avatar roblox-cinematics roblox-coding roblox-data-persistence roblox-economy roblox-game-dev roblox-networking roblox-orchestrator roblox-performance roblox-plugins roblox-security roblox-terrain roblox-testing roblox-tools-workflow roblox-ui-ux roblox-vfx
```
Verify: `ls C:/Users/Oz/.zcode/skills/ | grep -c roblox` → 1 (only roblox-lua-developer).

- [ ] **Step 4: Remove the lint roblox exemption**

In `tools/skill_lint.py`: delete `EXEMPT_FAMILIES = {"roblox"}` and the `fm.get("domain") not in EXEMPT_FAMILIES` condition (all skills now get section checks). In `tools/tests/test_skill_lint.py`: replace `test_roblox_exempt` with `test_roblox_not_exempt` asserting a G2 roblox-domain skill missing sections DOES raise E4. Run: `python -m unittest tools/tests/test_skill_lint.py -v` — expect PASS.

- [ ] **Step 5: Lint + manifest + changelog**

Run: `python tools/skill_lint.py --regen && python tools/skill_lint.py`
Expected: no E2/E3; roblox-lua-developer passes E4 (all G2 sections present).
Changelog: `2026-08-06 | Phase 2.0: Roblox suite consolidated 21→1 (roblox-lua-developer); 21 skills superseded and deleted | roblox-*`.

### Task 2.1: systems-core-architect rebuild (G3)

**Files:**
- Rewrite: `skills/systems-core-architect/SKILL.md`

**Interfaces:**
- Consumes: G3 section list (Global Constraints), skill-lint.
- Produces: the G3 language/performance skill; `concurrency-engineer` (3.4) references its per-language models.

Content contract — MUST include:
- `## WHEN TO USE`: C++, Rust, Go, backend Python systems code; memory/performance-critical paths. `## WHEN NOT TO USE`: CRUD/app code, managed runtimes.
- `## DECISION TREE`: language selection (memory safety vs control vs ecosystem); when to drop to unsafe/raw; when to parallelize vs keep sequential.
- `## PATTERNS` with trade-offs, per language: C++ (RAII, move semantics, value vs reference, noexcept, pimpl); Rust (ownership/borrowing, interior mutability, Send/Sync, `unsafe` review checklist: deref null, aliasing, lifetime escapes, FFI); Go (goroutine lifecycle, channels vs mutex, context cancellation, errgroup); backend Python (GIL realities, asyncio vs threads vs multiprocessing, uvloop, zero-copy buffers).
- `## FAILURE MODES & MITIGATIONS`: undefined behavior, data races, deadlocks, memory leaks, stack overflow, false sharing, allocator fragmentation, slice/iterator invalidation — each with detection method and fix.
- `## QUANTITATIVE RULES` (G3): cache-miss latency table (L1 ~1ns, L2 ~5ns, L3 ~15ns, RAM ~100ns, disk ~10ms); branch mispredict ~20 cycles; P99 > 4× P50 ⇒ queueing; allocation in hot loop cost; lock contention threshold.
- `## VERIFICATION GATE`: sanitizers (ASan/UBSan/TSan), valgrind, `go test -race`, `cargo miri`, leak checks; before/after benchmarks with pinned environment; criteria for "done".
- `## REFERENCES`: cppreference, Rust Book + Rustonomicon, Effective Go, Go memory model, perf(1) docs, cache-latency numbers (latency numbers every programmer should know).

- [ ] **Step 1:** Write frontmatter (`version: 1.0.0`, `grade: G3`, `domain: languages`, `owned-by-agent: code-implementer`, `supersedes: ""` if none) + WHEN TO USE / WHEN NOT TO USE.
- [ ] **Step 2:** Write DECISION TREE + PATTERNS per the contract.
- [ ] **Step 3:** Write FAILURE MODES & MITIGATIONS (≥10 entries, each with detection + fix).
- [ ] **Step 4:** Write QUANTITATIVE RULES (numbers, not vibes).
- [ ] **Step 5:** Write VERIFICATION GATE + REFERENCES.
- [ ] **Step 6:** Run `python tools/skill_lint.py --regen` — expect E4 clearance for this skill; run full lint, record remaining baseline errors.
- [ ] **Step 7:** Changelog: `2026-08-06 | Phase 2.1: systems-core-architect rebuilt to G3 | systems-core-architect`.

### Task 2.2: java-jvm-expert rebuild (G2)

**Files:**
- Rewrite: `skills/java-jvm-expert/SKILL.md`

Content contract — MUST include:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (not for non-JVM scripting; not when GraalVM native-image is the answer).
- `## DECISION TREE`: heap sizing → collector choice (G1 vs ZGC vs Serial) → allocation-site reduction → platform limits; when to profile vs reason.
- `## PATTERNS`: modern Java (records, pattern matching, sealed types, virtual threads); executor discipline (bounded pools, rejection policy); avoiding allocation in hot loops (escape analysis assumptions, primitive streams, object pooling trade-off).
- `## FAILURE MODES & MITIGATIONS`: GC pauses (collector swap, heap tuning), OOM (heap dump analysis, leak suspect), thread starvation, classloader leaks, CPU spin, Metaspace growth, `-Xlog:gc` diagnostics.
- `## VERIFICATION GATE`: JFR recordings + async-profiler workflow (flame graphs), JMH microbenchmark template with warmup/iterations, heap dump analysis (`jmap`/Eclipse MAT), before/after metrics.
- `## REFERENCES`: OpenJDK GC tuning guide, JEPs (virtual threads, records), JMH docs, async-profiler README.

- [ ] **Steps 1–6:** Same pattern as 2.1 (write sections per contract, lint, changelog). Version `1.0.0`, grade `G2`, domain `languages`, owner `code-implementer`.

### Task 2.3: ml-python-scientist rebuild (G2)

**Files:**
- Rewrite: `skills/ml-python-scientist/SKILL.md`

Content contract — MUST include:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (not for plain scripting; not when the answer is a managed service).
- `## DECISION TREE`: vectorize vs loop (size thresholds, memory budget); pandas vs numpy vs polars vs SQL; framework choice (PyTorch vs TF vs JAX) by deployment target.
- `## PATTERNS`: vectorized idioms (no per-row loops); tensor shape discipline (`[B, T, H]` comments); GPU memory hygiene (`.detach()`, `no_grad`, `pin_memory`, gradient accumulation); distributed training basics (DDP, gradient clipping); reproducibility (seeds, determinism flags, pinned deps).
- `## FAILURE MODES & MITIGATIONS`: GPU OOM (gradient checkpointing, batch size tuning), data leakage (time-series splits), nondeterminism (seed failures, non-deterministic kernels), dtype/precision bugs (float16 accumulation), NaN propagation, stale tensor references.
- `## VERIFICATION GATE`: shape assertions, gradient checks, holdout eval discipline, `torch.cuda.memory_summary`, run-to-run variance report.
- `## REFERENCES`: PyTorch docs, NumPy guidelines, CUDA memory docs, reproducibility guides.

- [ ] **Steps 1–6:** Same pattern. Version `1.0.0`, grade `G2`, domain `languages`, owner `ml-python-scientist`.

### Task 2.4: performance-profiler deepen (G2)

**Files:**
- Modify: `skills/performance-profiler/SKILL.md` (keep existing tool tables; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (not before measuring; not for one-off scripts).
- `## DECISION TREE`: symptoms → hypothesis → profile → optimize → re-verify loop; CPU vs memory vs I/O vs lock first.
- `## FAILURE MODES & MITIGATIONS`: optimizing unmeasured paths; microbenchmark lies (JIT warmup, inlining); sampling bias; profiling in production vs staging; benchmark noise (env pinning, iterations, statistical significance).
- `## VERIFICATION GATE`: before/after benchmark protocol (same env, ≥5 runs, report median + p90), profiler evidence attached, Pareto rule (top 3 bottlenecks).
- `## REFERENCES`: Brendan Gregg methodology, perf/async-profiler docs, Google "Making latency measurement useful" style guidance.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `performance-engineer`.

### Task 2.5: resilience-pattern-engineer deepen (G2)

**Files:**
- Modify: `skills/resilience-pattern-engineer/SKILL.md` (keep pattern snippets; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (retry is wrong for non-idempotent or latency-critical paths).
- `## DECISION TREE`: fail-fast vs retry vs degrade; retryable error classification (5xx/network vs 4xx); jitter choice; circuit breaker vs bulkhead vs rate limit.
- `## FAILURE MODES & MITIGATIONS`: retry storms, thundering herd (jitter: full jitter formula), breaker flapping (failure-rate-based not count-based), timeouts too short/long, cascade failures, idempotency-key misuse.
- `## VERIFICATION GATE`: fault injection (chaos: kill dependency, pause network), load test under degraded backend, breaker state transition assertions, retry budget math check.
- `## REFERENCES`: AWS fault-tolerance whitepaper, Google SRE workbook (managing load, cascading failures), resilience engineering classics.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `code-implementer`.

### Task 2.6: security-hardening-specialist deepen (G2 + threat modeling)

**Files:**
- Modify: `skills/security-hardening-specialist/SKILL.md` (keep OWASP tables; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (hardening ≠ pentesting; authorize first).
- `## DECISION TREE`: threat model first (STRIDE per component) → attack surface review → controls per finding → verify.
- `## FAILURE MODES & MITIGATIONS`: CORS misconfig, IDOR, mass assignment, rate-limit bypass, timing attacks, JWT algorithm confusion, session fixation, secrets in images/logs.
- `## VERIFICATION GATE`: SAST + dependency audit + manual auth/authz test matrix; headers verified via curl; secrets scan (gitleaks/trufflehog) clean.
- `## REFERENCES`: OWASP ASVS, OWASP Top 10, NIST SP 800-63 (auth), CORS spec.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `security-auditor`.

### Task 2.7: refactoring-intelligence deepen (G2)

**Files:**
- Modify: `skills/refactoring-intelligence/SKILL.md` (keep smell table; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (rewrite vs refactor decision; don't refactor without tests).
- `## DECISION TREE`: characterize (tests) → smell inventory → risk ranking → incremental (branch-by-abstraction / strangler fig) → verify.
- `## FAILURE MODES & MITIGATIONS`: refactor without characterization tests; behavior drift; over-refactoring; large-bang merges; lost history.
- `## VERIFICATION GATE`: characterization tests green before/after, diff review (behavior-preserving), metric comparison (complexity, duplication), red-team-qa review.
- `## REFERENCES`: Fowler Refactoring, Feathers Working Effectively with Legacy Code, branch-by-abstraction guidance.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `refactoring-specialist`.

### Task 2.8: api-design-architect deepen (G2)

**Files:**
- Modify: `skills/api-design-architect/SKILL.md` (keep REST/status-code tables; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (not for internal function calls; not when streaming/batch fits better).
- `## DECISION TREE`: REST vs GraphQL vs gRPC vs async events (consistency, client diversity, streaming needs).
- `## FAILURE MODES & MITIGATIONS`: breaking changes without versioning, inconsistent error shapes, unbounded page sizes, missing idempotency on retryable writes, N+1 in GraphQL resolvers, deadlock on sync-over-async.
- `## VERIFICATION GATE`: OpenAPI contract validation, contract tests per endpoint, idempotency replay test, load test on pagination.
- `## REFERENCES`: Google API design guide, RFC 7807, OpenAPI 3.x spec, gRPC best practices.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `api-architect`.

### Task 2.9: query-performance-engineer deepen (G2)

**Files:**
- Modify: `skills/query-performance-engineer/SKILL.md` (keep EXPLAIN/index tables; add G2 sections)

Content contract — MUST add:
- `## WHEN TO USE` / `## WHEN NOT TO USE` (schema redesign > index when shape is wrong).
- `## DECISION TREE`: EXPLAIN → identify access pattern → index vs denormalize vs cache vs shard (scale ladder).
- `## FAILURE MODES & MITIGATIONS`: over-indexing (write amplification), index bloat, covering-index misuse, cache stampede, stale stats (ANALYZE), connection pool exhaustion, lock contention, replication lag reads.
- `## VERIFICATION GATE`: EXPLAIN ANALYZE before/after, index usage stats, query metrics (pg_stat_statements), load test with production-shaped data.
- `## REFERENCES`: Use The Index, Luke; PostgreSQL docs (indexing, locking); MySQL 8 optimizer docs.

- [ ] **Steps 1–6:** Same pattern. Version `0.2.0`, grade `G2`, owner `db-architect`.

**Phase 2 gate:** [ ] Task 2.0 complete: 21 roblox dirs gone, roblox-lua-developer present and G2-clean; [ ] all 9 content skills updated (versions bumped); [ ] lint: zero E4 errors for these skills; [ ] every touched skill's frontmatter description is a precise trigger — no "MANDATORY" phrasing remains in rewritten skills; [ ] red-team-qa reviewed each skill (incl. the consolidation) for placeholder content and internal contradictions; [ ] nothing shrank (byte counts ≥ prior for modified files; consolidated skill ≥ 500 lines); [ ] changelog entries complete.

---

## Phase 3 — World-Class Flagships (G3)

Goal: 8 new G3 skills (7 flagships + deep-planner), 3 new subagents (planner, solution-architect, ml-engineer), and evals on all 9 G3 skills. All follow the G3 section list from Global Constraints. Each skill task creates `skills/<name>/SKILL.md` and ends with lint + changelog (same Steps 1–7 pattern as 2.1; contracts below).

### Task 3.1: distributed-systems-engineer

**Files:** Create: `skills/distributed-systems-engineer/SKILL.md`
Version `1.0.0`, grade `G3`, domain `architecture`, owner `solution-architect` (agent created in Task 3.9; lint W2 warning tolerated until then).

Contract — MUST include:
- `## DECISION TREE`: consistency model selection (linearizable vs serializable vs causal vs eventual) by requirement; replication topology (single-leader vs multi-leader vs quorum); partitioning (hash vs range, rebalance strategy); transactions (2PC vs Saga vs outbox).
- `## PATTERNS`: idempotency keys, outbox pattern, distributed locking with leases + fencing tokens, quorum read/write, gossip for membership.
- `## FAILURE MODES & MITIGATIONS`: split brain (fencing, quorum), clock skew (NTP, hybrid logical clocks), thundering herd, cascade failure, replication lag (read-your-writes), lost update, partial failure of 2PC.
- `## QUANTITATIVE RULES`: quorum math (W+R > N), latency budget decomposition (network RTT table), replication lag SLO targets, retry budget formula (request rate × failure rate × retry count).
- `## VERIFICATION GATE`: fault-injection matrix (kill leader, partition, pause clock), Jepsen-style linearizability checks where feasible, chaos tests, load under degraded conditions.
- `## REFERENCES`: DDIA (Kleppmann), Raft paper, Jepsen analyses, Google Spanner/TrueTime papers.

### Task 3.2: incident-response-engineer

**Files:** Create: `skills/incident-response-engineer/SKILL.md`
Version `1.0.0`, grade `G3`, domain `production`, owner `devops-engineer`.

Contract — MUST include:
- `## DECISION TREE`: severity classification (SEV1–3 with time-to-mitigate targets) → contain (rollback vs forward-fix vs feature-flag off) → mitigate → remediate → postmortem.
- `## PATTERNS`: rollback-first discipline, feature-flag kill switch, status communication cadence, war-room roles (incident commander, comms, ops), runbook-first alerting.
- `## FAILURE MODES & MITIGATIONS`: fixing instead of containing, investigation tunnel vision (timebox), missing telemetry, postmortem blame (blameless format), alert silence, bad rollback (schema mismatch).
- `## QUANTITATIVE RULES`: MTTR/MTTD targets, error-budget burn rates, rollback decision latency budget, communication intervals (5-15-30).
- `## VERIFICATION GATE`: game-day drills, checklist dry-runs, postmortem action-item follow-through tracking, timeline reconstruction accuracy check.
- `## REFERENCES`: Google SRE workbook (incident response), blameless postmortem guides, PagerDuty/incident.io practices.

### Task 3.3: system-design-architect

**Files:** Create: `skills/system-design-architect/SKILL.md`
Version `1.0.0`, grade `G3`, domain `architecture`, owner `solution-architect` (agent created in Task 3.9; lint W2 warning tolerated until then).

Contract — MUST include:
- `## DECISION TREE`: requirements (functional + non-functional with numbers) → capacity estimation → component selection → trade-off documentation (ADR) → review.
- `## PATTERNS`: ADR format (context, decision, consequences, alternatives); trade-off framework (CAP, consistency vs latency vs cost); caching tiers; queue-based load leveling; sharding.
- `## FAILURE MODES & MITIGATIONS`: over-design (YAGNI), capacity estimates without traffic math, single points of failure missed, ignoring non-functional constraints (cost, compliance), design without failure modes.
- `## QUANTITATIVE RULES`: "numbers every engineer should know" table (latency, QPS per server type, storage math: 1M users × 1KB × 10 writes/day), QPS→instances formula, bandwidth math.
- `## VERIFICATION GATE`: capacity math cross-check, design review checklist (SPOF, scaling, failure modes, cost), ADR review by red-team-qa.
- `## REFERENCES`: DDIA, system design interview sources, "numbers every programmer should know", AWS well-architected framework.

### Task 3.4: concurrency-engineer

**Files:** Create: `skills/concurrency-engineer/SKILL.md`
Version `1.0.0`, grade `G3`, domain `architecture`, owner `code-implementer`. References `systems-core-architect` (2.1) per-language models.

Contract — MUST include:
- `## DECISION TREE`: parallelism vs concurrency; threads vs async vs actors vs CSP (Go channels) by workload; shared state vs message passing.
- `## PATTERNS`: lock ordering discipline, lock-free structures (when justified), thread pools with bounded queues, cancellation propagation, structured concurrency.
- `## FAILURE MODES & MITIGATIONS`: data races (tooling per language), deadlock (lock ordering, timeout), livelock, starvation, priority inversion, false sharing, async deadlock (sync-over-async), goroutine leaks.
- `## QUANTITATIVE RULES`: oversubscription (CPU-bound ≈ cores, I/O-bound ≈ cores × factor), contention cost thresholds, channel buffer sizing.
- `## VERIFICATION GATE`: TSan/race detectors, stress tests with soak duration, deadlock detectors, benchmark before/after, model-checking where available.
- `## REFERENCES`: Go memory model, JSR-133 (Java memory model), C++ memory model, Herlihy "Art of Multiprocessor Programming".

### Task 3.5: database-at-scale

**Files:** Create: `skills/database-at-scale/SKILL.md`
Version `1.0.0`, grade `G3`, domain `architecture`, owner `db-architect`. References `query-performance-engineer` (2.9).

Contract — MUST include:
- `## DECISION TREE`: scale-up vs read replicas vs shard vs move-to-managed; shard key selection; replication topology (sync vs async, quorum); isolation level by workload.
- `## PATTERNS`: zero-downtime migration (expand/contract, dual-write, backfill + verify), sharding with rebalancing, connection pooling at scale, read-your-writes routing.
- `## FAILURE MODES & MITIGATIONS`: replication lag (staleness), split brain in failover, migration corruption (checksum verify), hot shard, deadlock storms, vacuum/compaction stalls, backup restore failure.
- `## QUANTITATIVE RULES`: replica lag budgets, connection math (max_connections per instance vs pool), shard size limits, migration batch-size formulas.
- `## VERIFICATION GATE`: migration rehearsal on copy, checksum verification, failover drill, load test at 2× peak, backup-restore drill.
- `## REFERENCES`: DDIA (replication/partitioning), PostgreSQL docs (replication, vacuum), MySQL 8 docs (InnoDB), use-the-index-luke.

### Task 3.6: observability-sre

**Files:** Create: `skills/observability-sre/SKILL.md`
Version `1.0.0`, grade `G3`, domain `production`, owner `devops-engineer`.

Contract — MUST include:
- `## DECISION TREE`: SLI selection (golden signals) → SLO with target + window → error budget → alerting on burn rate → dashboards → runbooks.
- `## PATTERNS`: three pillars (metrics/logs/traces), RED vs USE method, distributed tracing with sampling, structured logging standards, alert-on-symptoms.
- `## FAILURE MODES & MITIGATIONS`: alert fatigue (dedupe, thresholds), alerting on causes not symptoms, dashboards without actions, log spam, missing golden signals, sampling bias.
- `## QUANTITATIVE RULES`: burn-rate alert thresholds (e.g., 14.4× for 1h), SLO math (error budget = 1 − SLO; budget burn per incident), cardinality limits.
- `## VERIFICATION GATE`: SLO error-budget reporting, alert drill (fire test alert, verify runbook), trace coverage check, dashboard review.
- `## REFERENCES`: Google SRE book (chapters 4–5, monitoring), SRE workbook, OpenTelemetry docs, Prometheus best practices.

### Task 3.7: general-orchestrator

**Files:** Create: `skills/general-orchestrator/SKILL.md`
Version `1.0.0`, grade `G3`, domain `delivery`, owner `code-implementer`. Reference implementation: `skills/roblox-orchestrator/SKILL.md` (already read — generalize its protocol).

Contract — MUST include:
- `## WHEN TO USE`: multi-skill backend/distributed tasks (parallelizable, multi-domain); `## WHEN NOT TO USE`: single-skill tasks (use the specific skill directly).
- `## DECISION TREE`: decompose (skill inventory per subtask) → dependency graph → parallel vs sequential → dispatch per AGENTS.md → verify per subtask → integrate.
- `## PATTERNS`: subagent routing via AGENT-SKILL-MATRIX (1.3), **gate-driven execution** (every subtask has a proof-based gate per WORKFLOW.md — stop on failed gate, fix, re-verify; replaces the Roblox "no-stop" pattern), checkpoint cadence, verification per subtask (tests/logs/evidence, never "looks done"), rollback on failed gate.
- `## FAILURE MODES & MITIGATIONS`: agent drift, context overflow, orphaned subtasks, verification theater (checking the wrong thing), parallel dependency violations, silent partial failures.
- `## QUANTITATIVE RULES`: fan-out limits (≤5 parallel agents recommended), checkpoint interval guidance, retry budget for flaky verification.
- `## VERIFICATION GATE`: every subtask has an explicit pass criterion; integration smoke test; final report format (from roblox-orchestrator, generalized).
- `## REFERENCES`: AGENTS.md, system-instructions v2 (1.1), AGENT-SKILL-MATRIX (1.3), roblox-orchestrator as reference implementation, `C:/Users/Oz/.claude/skills/subagent-orchestrator/` (if present — compare its protocol before finalizing).

### Task 3.8: deep-planner skill + planner agent

**Files:**
- Create: `skills/deep-planner/SKILL.md`
- Create: `C:/Users/Oz/.zcode/agents/planner.md`

**Interfaces:**
- Consumes: system-instructions v2 (1.1), AGENT-SKILL-MATRIX (1.3), deep-researcher output.
- Produces: the planning workflow used by `general-orchestrator` (3.7); the `planner` subagent type (registry 17 → 18).

- [ ] **Step 1: Create the planner agent definition**

`C:/Users/Oz/.zcode/agents/planner.md` (same frontmatter format as the existing agent files — see `agents/red-team-qa.md`):
```markdown
---
name: "planner"
description: "Deep Planning Engineer. Decomposes goals/specs into executable plans: task graphs, dependency analysis, estimation, risk registers. Consumes research; produces plans consumed by general-orchestrator."
color: blue
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---
You are a Deep Planning Engineer. Given a goal or spec you produce a plan, not code.
METHODOLOGY
1. Decompose: split the goal into independently testable tasks; each task has one owner and one acceptance criterion.
2. Dependency graph: map task dependencies; identify the critical path and parallelizable work.
3. Estimate: T-shirt size (S/M/L/XL) then time range; state assumptions; flag unknowns (research tasks).
4. Risk register: for each risk — likelihood, impact, mitigation, trigger to escalate.
5. Plan review: verify every task has a testable outcome, no circular dependencies, no orphan tasks.
6. Research integration: when knowledge is missing, emit explicit research questions for deep-researcher before finalizing.
OUTPUT FORMAT: task table (id, description, deps, estimate, acceptance criterion), critical path, risk register.
```

- [ ] **Step 2: Write the deep-planner skill**

`skills/deep-planner/SKILL.md`, frontmatter: name deep-planner, version 1.0.0, grade G3, domain doctrine, status active, last-reviewed 2026-08-06, owned-by-agent planner. Sections:
1. `## WHEN TO USE` — multi-task goals, specs → plan, research-informed planning. `## WHEN NOT TO USE` — single-step tasks; not a substitute for the brainstorming/spec phase.
2. `## DECISION TREE` — goal clear? → decompose → dependencies → estimate → risk → review; unknown domain → emit research questions to deep-researcher first.
3. `## PATTERNS` — task decomposition rules (independently testable, one acceptance criterion each), dependency graphs & critical path, T-shirt estimation with ranges, risk registers, plan review checklist, milestone checkpoints.
4. `## FAILURE MODES & MITIGATIONS` — over-decomposition (task explosion), under-specification (untestable tasks), hidden dependencies, estimation optimism (reference-class forecasting), orphan tasks, plan drift (re-plan triggers).
5. `## QUANTITATIVE RULES` — estimation ranges (S: 0.5–1d, M: 1–3d, L: 3–5d, XL: 5–10d, split above); planning overhead ≈ 10–15% of project time; re-plan if > 20% of tasks slip.
6. `## VERIFICATION GATE` — plan audit: every task testable? dependencies acyclic? critical path computed? risks have mitigations? acceptance criteria measurable?
7. `## REFERENCES` — superpowers writing-plans (plan format), reference-class forecasting, Cone of Uncertainty, dependency-graph practice.

- [ ] **Step 3: Lint + changelog**

Run: `python tools/skill_lint.py --regen` — deep-planner must pass E4 (all G3 sections present).
Changelog: `2026-08-06 | Phase 3.8: deep-planner skill + planner agent | deep-planner, agents/planner.md`.

### Task 3.9: solution-architect + ml-engineer agents

**Files:**
- Create: `C:/Users/Oz/.zcode/agents/solution-architect.md`, `C:/Users/Oz/.zcode/agents/ml-engineer.md`
- Modify: `skills/system-design-architect/SKILL.md` (frontmatter owner), `skills/ml-python-scientist/SKILL.md` (frontmatter owner)

**Interfaces:**
- Consumes: agent file format (see `agents/red-team-qa.md`), skills from 3.3 and 2.3.
- Produces: two subagent types (registry 18 → 20); valid owners for `system-design-architect` and `ml-python-scientist` (fixes the pre-existing invalid owner `ml-python-scientist`).

- [ ] **Step 1: Create the solution-architect agent**

`C:/Users/Oz/.zcode/agents/solution-architect.md`:
```markdown
---
name: "solution-architect"
description: "Staff Solution Architect. System design, capacity estimation, ADR ownership, architecture reviews, trade-off analysis. Owns system-design-architect and distributed-systems-engineer skills."
color: purple
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---
You are a Staff Solution Architect. You produce architecture, not code.
METHODOLOGY
1. Requirements: quantify non-functional requirements (traffic, latency, cost) before design.
2. Capacity estimation: compute storage, QPS, bandwidth from traffic math before choosing components.
3. Trade-off documentation: every design decision is an ADR (context, decision, consequences, alternatives).
4. Review: check SPOFs, scaling limits, failure modes, cost — before sign-off.
OUTPUT FORMAT: system sketch, capacity math, ADR list, review findings.
```

- [ ] **Step 2: Create the ml-engineer agent**

`C:/Users/Oz/.zcode/agents/ml-engineer.md`:
```markdown
---
name: "ml-engineer"
description: "Machine Learning Engineer. Model training, evaluation, reproducibility, GPU memory management, serving. Owns ml-python-scientist skill."
color: green
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---
You are a Machine Learning Engineer. You build and validate models, not notebooks.
METHODOLOGY
1. Pipeline discipline: data validation and leakage checks before training.
2. Eval hygiene: fixed holdout, multiple seeds, report variance.
3. Reproducibility: seed everything, pin dependencies, record configs.
4. GPU memory: profile, batch-size tune, gradient checkpointing, cleanup.
5. Serving constraints: latency, throughput, cost targets documented before handoff.
```

- [ ] **Step 3: Update owners**

In `skills/system-design-architect/SKILL.md` frontmatter: `owned-by-agent: solution-architect`. In `skills/ml-python-scientist/SKILL.md` frontmatter: `owned-by-agent: ml-engineer`.

- [ ] **Step 4: Registry + matrix + changelog**

Update AGENTS.md registry (20 → 23: add planner, solution-architect, ml-engineer rows — if Phase 1 already ran, apply as a follow-up edit). Extend `docs/skills/AGENT-SKILL-MATRIX.md` with the 3 new agents.
Changelog: `2026-08-06 | Phase 3.9: solution-architect + ml-engineer agents; owner updates | agents/*, system-design-architect, ml-python-scientist`.

### Task 3.10: Flagship evals (14 G3 skills — 9 original system/family flagships + 5 addyosmani workflow adaptations)

**Files:**
- Create: `docs/skills/evals/<name>-eval.md` for each of: systems-core-architect, distributed-systems-engineer, incident-response-engineer, system-design-architect, concurrency-engineer, database-at-scale, observability-sre, general-orchestrator, deep-planner, requirements-elicitation, spec-driven-development, source-driven-development, doubt-driven-development, adr-engineering (14 files)

**Interfaces:**
- Consumes: the 14 G3 skills (2.1, 3.1–3.9e).
- Produces: per-skill eval files; a results summary at `docs/skills/evals/results-2026-08-06.md`.

- [ ] **Step 1: Write each eval file**

Each `docs/skills/evals/<name>-eval.md` contains:
1. **Trigger test — 8 concrete scenarios.** Task descriptions the skill should and should not fire on (e.g., for distributed-systems-engineer: fire on "design leader election for a 50-node cluster", "our writes race under partition — fix"; must NOT fire on "write a CRUD endpoint"). List 8: 5 fire + 3 no-fire, each one line, concrete.
2. **Quality rubric — 6 criteria, scored 1–5:** (a) decision tree covers the stated branches; (b) every failure mode has detection + mitigation; (c) quantitative rules are numbers, not adjectives; (d) verification gate is executable (commands/checks); (e) references are authoritative and current; (f) no contradictions with other skills (checked against Phase 1 doctrine).
3. **Reference task** — one realistic scenario the skill must produce a credible response for (2–3 sentences).

- [ ] **Step 2: Run the evals via subagent**

Dispatch a subagent to run the 14 eval files as one batched pass (token-smart — not 14 separate dispatches): for each, feed the 8 trigger scenarios → record invoke/no-invoke verdict against the skill's WHEN TO USE; score the 6 rubric criteria; run the reference task and judge credibility. Record scores in `docs/skills/evals/results-2026-08-06.md` (table: skill, trigger accuracy, rubric avg, notes).

- [ ] **Step 3: Fix failures inline**

Any rubric score < 3 or trigger miss → fix the skill in the same task, re-run that eval, record the delta.

- [ ] **Step 4: Changelog**

Add: `2026-08-07 | Phase 3.10: flagship evals (14 skills) — results at docs/skills/evals/results-2026-08-07.md | 14 G3 skills`.

**Phase 3 gate:** [ ] 14 new skills created + systems-core-architect at G3 (14 total G3); [ ] 3 new agents defined (planner, solution-architect, ml-engineer) + 3 restored, 23 agent files total; [ ] lint passes on all G3 (all G3 sections present); [ ] evals run on all 14, avg rubric ≥ 4, trigger accuracy ≥ 7/8; [ ] red-team-qa reviewed each flagship + each agent definition for cross-skill contradictions; [ ] changelog complete.

---

## Phase 4 — Future-Proofing & Final Verification

### Task 4.1: skill-lint v2

**Files:**
- Modify: `tools/skill_lint.py`, `tools/tests/test_skill_lint.py`

**Interfaces:**
- Consumes: skill-lint v1 (0.4), G3 section list.
- Produces: lint with `--ci` (warnings → exit 2) and stale-review enforcement used by the quarterly maintenance cycle.

- [ ] **Step 1: Add the failing tests**

Add to `test_skill_lint.py`:
```python
    def test_ci_flag_warnings_exit_2(self):
        code = subprocess.run([sys.executable, str(Path(__file__).resolve().parent.parent / "skill_lint.py"),
                               "--ci"], capture_output=True, cwd=str(self.tmp), env={"PATH": os.environ["PATH"]})
        self.assertEqual(code.returncode, 2)
```
(plus a test that without `--ci`, warnings exit 0; and that `--regen` + `--json` compose.)

- [ ] **Step 2: Implement v2 changes**

In `tools/skill_lint.py`: `--ci` already implemented in v1 — extend: add `--stale` flag to fail on stale reviews (W1 → error when `--stale`), and print a maintenance summary line: `N skills due for review` (last-reviewed > 90 days). Also narrow W3: only flag backtick references that match a known skill name or the `skills/<name>` pattern (the Phase-0 baseline produced 114 noisy warnings from agent names, CLI flags, and packages — reduce to signal; adjust the whitelist if needed and update `test_` coverage accordingly).

- [ ] **Step 3: Run tests, verify pass**

Run: `python -m unittest tools/tests/test_skill_lint.py -v`
Expected: PASS (all v1 tests + new v2 tests).

- [ ] **Step 4: Changelog**

Add: `2026-08-06 | Phase 4.1: skill-lint v2 (--ci, --stale, review summary) | tools/skill_lint.py`.

### Task 4.2: Upgrade-process doc

**Files:**
- Create: `docs/skills/CONTRIBUTING.md`

Content — MUST include: the skill lifecycle (propose → spec → plan → implement → red-team-qa → lint → eval → review); the frontmatter standard and grade ladder (verbatim from Global Constraints); how to bump versions (`version` bump on content change, `supersedes` on replacement); the quarterly re-review cycle (run `skill_lint.py --stale`, update `last-reviewed`); changelog rules.

- [ ] **Step 1:** Write the doc.
- [ ] **Step 2:** Changelog: `2026-08-06 | Phase 4.2: upgrade-process doc (CONTRIBUTING.md) | docs/skills/CONTRIBUTING.md`.

### Task 4.3: G2 sweep (remaining skills)

**Files:**
- Modify: every general skill still at grade G1 or missing G2 sections after Phase 2 (expected: none of the 10 Phase-2 skills — 9 content + roblox-lua-developer; likely: devops-pipeline-engineer, container-optimizer, monorepo-workspace-architect, github-flow-master, dependency-supply-chain-guardian, cybersecurity-specialist, game-developer, mobile-developer, animation-web-builder, readme-architect, skill-creator, find-skills, mcp-builder — verify with lint first)

- [ ] **Step 1: Identify the sweep set**

Run: `python tools/skill_lint.py --json | python -c "import json,sys; d=json.load(sys.stdin); [print(e) for e in d['errors'] if e.startswith('E4')]"`
The E4 list is the sweep set.

- [ ] **Step 2: Add G2 sections per skill**

For each skill in the set: add `## WHEN TO USE` / `## WHEN NOT TO USE` (rewrite the description's trigger claim into the sections), `## FAILURE MODES & MITIGATIONS` (≥5 entries specific to that skill's domain), `## VERIFICATION GATE`, `## REFERENCES` (≥3). Rewrite the frontmatter description as a precise trigger (drop "MANDATORY" phrasing — the trigger policy forbids blanket auto-invoke claims). Keep existing content intact; bump `version` to `0.2.0`; set `grade: G2`.

- [ ] **Step 3: Lint + changelog**

Run: `python tools/skill_lint.py --regen && python tools/skill_lint.py`
Expected: zero E4 errors. Changelog: `2026-08-06 | Phase 4.3: G2 sweep — <list> | <skills>`.

### Task 4.4: Optional git init (user decision)

**Files:** `C:/Users/Oz/.zcode/.gitignore`, git init in `.zcode`

- [ ] **Step 1: Confirm with the user**

Ask: "Init a git repo in `C:/Users/Oz/.zcode` for skill version history?" If no → skip this task, note in changelog: `2026-08-06 | Phase 4.4: git init declined | none`.
- [ ] **Step 2: If approved:** create `.gitignore` (exclude `v2/`, `tmp/`, `workspace/`, `.zcode/plans`, `cli/`), `git init`, initial commit `chore: baseline after engineering-excellence Phase 4`. Record in changelog.

### Task 4.5: Final verification & success-criteria report

**Files:**
- Create: `docs/skills/final-verification-2026-08-06.md`

- [ ] **Step 1: Run the full verification battery**

```bash
python tools/skill_lint.py --regen
python tools/skill_lint.py --json
python tools/apply_metadata.py && echo "apply_metadata: no-op expected"
```
Check against the spec's success criteria:
1. 0 empty dirs, 0 duplicated skills, 0 blanket-invoke descriptions (grep `grep -riE "mandatory for all|for ALL .*tasks" skills/` → empty).
2. 100% skills with complete frontmatter (lint E1 = 0).
3. 100% skills G2+ with the G2 sections, no exemptions (lint E4 = 0).
4. 9 G3 skills with evals (skills.json query + ls docs/skills/evals/).
5. lint exits 0; manifest regenerated and current.
6. Precedence rules documented in doctrine; red-team-qa contradiction check recorded.
7. Roblox consolidation smoke test: 21 roblox-* dirs absent, roblox-lua-developer present with all G2 sections, supersession recorded in skills.json + changelog.
8. Nothing shrank: every touched skill's byte count ≥ pre-change (compare vs inventory snapshot).
9. **Universal coverage map**: every project type (cyber/security, generic coding, advanced systems, world-class problem solving, delivery, roblox, ML) maps to ≥1 skill + ≥1 owning agent — produce the map as a section in the report using skills.json + AGENT-SKILL-MATRIX.md.

- [ ] **Step 2: Write the report**

`docs/skills/final-verification-2026-08-06.md`: table of the 8 criteria + the universal-coverage map with pass/fail + evidence (command output snippets). Any fail → fix in a follow-up task, re-run.

- [ ] **Step 3: Changelog**

Add: `2026-08-06 | Phase 4.5: final verification — <PASS/FAIL summary> | all`.

**Phase 4 gate:** [ ] all 8 success criteria PASS (report on file); [ ] lint exit 0; [ ] full catalog red-team-qa pass complete; [ ] changelog documents every change.

---

## Success-Criteria Mapping (spec §6 → plan tasks)

| Spec criterion | Plan coverage |
|---|---|
| 0 empty dirs / 0 duplicates / 0 "MANDATORY for ALL" | Task 0.2, 1.1, gate greps (4.5 Step 1) |
| 100% complete frontmatter | Task 0.3, enforced by lint E1 |
| 100% skills G2+ (no exemptions) | Tasks 2.0–2.9, 3.1–3.9, 4.3, enforced by lint E4 |
| 9 G3 skills with evals | Tasks 2.1, 3.1–3.9, 3.10 |
| lint exit 0 + manifest current | Tasks 0.4, 0.5, 4.1, 4.5 |
| Precedence documented, no contradictions | Tasks 1.1, 1.2, gate |
| Roblox consolidated (21→1) + triggers smoke-tested | Task 2.0, 4.5 Step 1.7 |
| Nothing shrank | Task 4.5 Step 1.8 (byte-count check) |
