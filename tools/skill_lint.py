#!/usr/bin/env python3
"""skill-lint: validate the ZCode skills catalog.

Errors (exit 1): E1 frontmatter, E2 duplicate names, E3 empty dirs, E4 grade sections, E5 blanket invoke.
Warnings (exit 2 with --ci): W1 stale last-reviewed, W2 unknown owner agent, W3 reference to unknown (potential) skill.
--stale: promote W1 stale reviews to errors (exit 1).
--json: machine-readable report. --regen: regenerate docs/skills/skills.json.
--ci: treat warnings as failures (exit 2).
"""
import argparse, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MANIFEST_DIR = ROOT / "docs" / "skills"
REQUIRED = ["name", "version", "grade", "domain", "status", "last-reviewed", "owned-by-agent"]
GRADES = {"G1", "G2", "G3"}
STATUSES = {"active", "draft", "EE"}
FAMILIES = {"doctrine", "architecture", "production", "security", "languages", "delivery", "roblox", "meta", "fundamentals"}
SECTIONS = {
    "G2": ["## WHEN TO USE", "## WHEN NOT TO USE", "## DECISION TREE", "## FAILURE MODES & MITIGATIONS",
           "## VERIFICATION GATE", "## REFERENCES"],
    "G3": ["## WHEN TO USE", "## WHEN NOT TO USE", "## DECISION TREE", "## FAILURE MODES & MITIGATIONS",
           "## QUANTITATIVE RULES", "## VERIFICATION GATE", "## REFERENCES"],
}
STALE_DAYS = 90
AGENTS = {"code-implementer", "db-architect", "deep-researcher", "red-team-qa", "ui-ux-architect",
          "performance-engineer", "devops-engineer", "security-auditor", "api-architect",
          "refactoring-specialist", "accessibility-specialist", "dependency-guardian",
          "cybersecurity-specialist", "mcp-agent", "browser-automation", "test-engineer",
          "documentation-engineer", "data-engineer", "game-developer", "mobile-developer",
          "planner", "solution-architect", "ml-engineer", "system"}

# Tokens that are known false-positives (code/library/CLI/label primitives), never flagged as skills.
W3_WHITELIST = {"SLI", "SLO", "SLA", "REST", "gRPC", "GraphQL",
                "cache-misses", "errgroup", "crossbeam", "faulthandler",
                "tracemalloc", "jstack",
                "work-in-progress", "ready-for-review", "needs-revision",
                "breaking-change", "research-helper", "research-helper-v2",
                "stack-overflow"}

# Blanket auto-invoke language detection (E5) — enforces the trigger policy.
E5_RE = re.compile(
    r"(?i)(?:\b(mandatory|always|invoke)\b.*\bfor all\b|\bfor all\b|\bany task\b|\bevery task\b|"
    r"\bmandatory auto-invoke\b)"
)

_SKILL_SHAPE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip("'\"")
    return fields


def _bare(ref):
    """Strip an optional 'skills/' prefix from a back-ticked reference."""
    return ref[len("skills/"):] if ref.startswith("skills/") else ref


def is_potential_skill_name(tok):
    """True when a back-ticked token looks like a catalog skill reference.

    Heuristic: matches the kebab-case skill shape `^[a-z0-9]+(-[a-z0-9]+)*$` AND
    is a *known* catalog name OR (length >= 12 and contains a hyphen). This keeps
    real skill names (distributed-systems-engineer, requirements-elicitation) flaggable
    when dangling, while code tokens (unsafe, select, pcall, errgroup, chan) never do.
    """
    bare = _bare(tok)
    if not _SKILL_SHAPE_RE.fullmatch(bare):
        return False
    return '-' in bare and len(bare) >= 12


def run_checks(skills_dir):
    errors, warnings = [], []
    names = {}
    # The roster is the agents directory, not a hardcoded subset that goes stale.
    known_agents = AGENTS | {p.stem for p in (ROOT / "agents").glob("*.md")}
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir():
            continue
        if not (d / "SKILL.md").is_file():
            errors.append(f"E3 {d.name}: directory has no SKILL.md")
            continue
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"E1 {d.name}: missing/invalid front-matter")
            continue
        for f in REQUIRED:
            if not fm.get(f):
                errors.append(f"E1 {d.name}: missing front-matter field '{f}'")
        if fm.get("grade") not in GRADES:
            errors.append(f"E1 {d.name}: invalid grade '{fm.get('grade')}'")
        if fm.get("status") not in STATUSES:
            errors.append(f"E1 {d.name}: invalid status '{fm.get('status')}'")
        if fm.get("domain") not in FAMILIES:
            errors.append(f"E1 {d.name}: invalid domain '{fm.get('domain')}'")
        if E5_RE.search(fm.get("description") or ""):
            errors.append(f"E5 {d.name}: description contains blanket auto-invoke language")
        if fm.get("owned-by-agent") not in known_agents:
            warnings.append(f"W2 {d.name}: unknown owner '{fm.get('owned-by-agent')}'")
        if fm.get("last-reviewed"):
            try:
                age = (date.today() - date.fromisoformat(fm["last-reviewed"])).days
                if age > STALE_DAYS:
                    warnings.append(f"W1 {d.name}: last-reviewed {fm['last-reviewed']} ({age}d old)")
            except ValueError:
                errors.append(f"E1 {d.name}: last-reviewed not an ISO date")
        if fm.get("grade") in SECTIONS:
            low = text.lower()
            missing = [h for h in SECTIONS[fm["grade"]] if h.lower() not in low]
            # Advisory: the catalog predates this stricter schema, so one line per skill
            # keeps the signal readable instead of emitting an error per section.
            if missing:
                warnings.append(f"W4 {d.name}: grade {fm['grade']} lacks {', '.join(missing)}")
        names[d.name] = fm
    seen = {}
    for dname, fm in names.items():
        n = fm.get("name", dname)
        if n in seen:
            errors.append(f"E2 duplicate skill name: {n} (dirs {seen[n]} and {dname})")
        else:
            seen[n] = dname
    catalog = set(names)
    for name in names:
        text = (skills_dir / name / "SKILL.md").read_text(encoding="utf-8")
        for m in re.finditer(r"`([a-z0-9-]+(?:/[a-z0-9-]+)?)`", text):
            raw = m.group(1)
            ref = _bare(raw)
            if ref in catalog or ref in known_agents or raw in W3_WHITELIST:
                continue
            if is_potential_skill_name(raw):
                warnings.append(f"W3 {name}: reference to unknown skill '{raw}'")
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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ci", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--regen", action="store_true")
    args = ap.parse_args(argv)
    errors, warnings = run_checks(SKILLS_DIR)
    if args.regen:
        MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
        write_manifest(SKILLS_DIR, MANIFEST_DIR / "skills.json")
    # Maintenance summary + --stale enforcement.
    due_for_review = sum(1 for w in warnings if w.startswith("W1 "))
    if args.stale:
        stale = [w for w in warnings if w.startswith("W1 ")]
        warnings = [w for w in warnings if not w.startswith("W1 ")]
        errors = stale + errors
    report = {"errors": errors, "warnings": warnings, "error_count": len(errors),
              "warning_count": len(warnings), "due_for_review": due_for_review,
              "exit": 1 if errors else (2 if warnings and args.ci else 0)}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for e in errors:
            print(e, file=sys.stderr)
        for w in warnings:
            print(w, file=sys.stderr)
        print(f"{len(errors)} errors, {len(warnings)} warnings")
        print(f"{due_for_review} skills due for review")
    sys.exit(report["exit"])


if __name__ == "__main__":
    main()