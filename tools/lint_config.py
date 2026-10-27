#!/usr/bin/env python3
"""Validate the skill/agent configuration and generate skills/INDEX.md.

Usage:
    python tools/lint_config.py                # validate, print report
    python tools/lint_config.py --write-index  # validate + regenerate INDEX.md
    python tools/lint_config.py --strict       # warnings fail the run too

Exit codes: 0 clean, 1 errors, 2 warnings under --strict.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
INDEX = SKILLS / "INDEX.md"

DOMAINS = ["doctrine", "architecture", "delivery", "production", "security",
           "languages", "roblox", "meta"]
REQUIRED_META = ["version", "domain", "grade", "status", "last-reviewed", "owned-by-agent"]
DESC_LIMIT = 1024
DESC_MIN = 120
# A routing description must say what it does, when to use it, and what routes elsewhere;
# anything this short or this placeholder-y is a stub that will never route.
PLACEHOLDER_PATTERNS = [
    "description here", "description goes here", "lorem ipsum", "write description",
    "your description", "placeholder description", "to be written",
]
AGENT_ALLOWED_KEYS = {"description", "mode", "color", "temperature", "steps", "permission", "name"}
STALE_PATTERNS = ["opencode", ".config/opencode"]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
AGENT_REF_RE = re.compile(r"`?(agents/([a-z0-9-]+)\.md)`?")
SKILL_PATH_RE = re.compile(r"`?(skills/([a-z0-9-]+)(?:/[^`\s)]*)?)`?")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def check_desc_quality(label: str, desc: str) -> None:
    """A description can be present and still be unusable for routing; check it is real."""
    text = desc.strip()
    low = text.lower()
    for pat in PLACEHOLDER_PATTERNS:
        if pat in low:
            err(f"{label}: description is a placeholder ('{pat}')")
            break
    if len(text) < DESC_MIN:
        err(f"{label}: description too short to route ({len(text)} < {DESC_MIN} chars)")
    if "  " in text or "\n" in text:
        warn(f"{label}: description has stray whitespace (breaks trigger matching)")


def frontmatter(path: Path) -> tuple[dict, str]:
    raw = io.open(path, encoding="utf-8").read().replace("\r\n", "\n")
    if not raw.startswith("---\n"):
        raise ValueError("file does not start with '---'")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated frontmatter")
    meta = yaml.safe_load(parts[1]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter is not a mapping")
    return meta, parts[2]


TRIGGER_RE = re.compile(r"\bUse (?:whenever|when|for|as|on|before|after|at|in)\b")


def short_trigger(desc: str, limit: int = 150) -> str:
    m = re.search(r"\bUse (?:when|for|as|on|before|after|it|the)\b", desc)
    if m:
        text = desc[m.start():]
    else:
        text = desc
    text = " ".join(text.split())
    if len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0]
        return cut + "…"
    return text


def check_links(path: Path, body: str, skill_dir: Path | None) -> None:
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if target.strip().lower() in {"url", "path", "link", "your-url", "..."}:
            continue  # template placeholder
        clean = target.split("#", 1)[0].strip()
        if not clean:
            continue
        if skill_dir is not None:
            resolved = (skill_dir / clean).resolve()
            if not resolved.exists():
                # allow references to other skills by bare name
                if (SKILLS / clean).exists() or (SKILLS / clean / "SKILL.md").exists():
                    continue
                warn(f"{path.name}: link target not found: {clean}")
        for name in re.findall(r"agents/([a-z0-9-]+)\.md", clean):
            if not (AGENTS / f"{name}.md").exists():
                err(f"{path.name}: dangling agent reference: {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    agent_names = {p.stem for p in AGENTS.glob("*.md")}
    skills: list[dict] = []

    # ---- agents ----
    for path in sorted(AGENTS.glob("*.md")):
        try:
            meta, body = frontmatter(path)
        except ValueError as exc:
            err(f"agents/{path.name}: {exc}")
            continue
        name = meta.get("name")
        if name != path.stem:
            err(f"agents/{path.name}: name '{name}' != filename")
        desc = meta.get("description") or ""
        if not desc.strip():
            err(f"agents/{path.name}: empty description")
        elif len(desc) > DESC_LIMIT:
            err(f"agents/{path.name}: description {len(desc)} > {DESC_LIMIT}")
        else:
            check_desc_quality(f"agents/{path.name}", desc)
        legacy = set(meta) - AGENT_ALLOWED_KEYS
        if legacy:
            err(f"agents/{path.name}: legacy/unknown frontmatter key(s): {', '.join(sorted(legacy))}")
        if not TRIGGER_RE.search(desc):
            warn(f"agents/{path.name}: description has no 'Use when/for/at/before' trigger clause")
        if meta.get("mode") != "subagent":
            err(f"agents/{path.name}: mode must be 'subagent'")
        perm = meta.get("permission")
        if not isinstance(perm, dict):
            err(f"agents/{path.name}: missing permission block")
        steps = meta.get("steps")
        if not isinstance(steps, int) or not 5 <= steps <= 200:
            warn(f"agents/{path.name}: steps should be an int 5..200 (got {steps!r})")
        if not body.strip():
            err(f"agents/{path.name}: empty body")

    # ---- skills ----
    seen_desc: dict[str, str] = {}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        skill_dir = path.parent
        name = skill_dir.name
        try:
            meta, body = frontmatter(path)
        except ValueError as exc:
            err(f"skills/{name}/SKILL.md: {exc}")
            continue
        if meta.get("name") != name:
            err(f"skills/{name}: frontmatter name '{meta.get('name')}' != directory")
        desc = meta.get("description") or ""
        if not desc.strip():
            err(f"skills/{name}: empty description")
        elif len(desc) > DESC_LIMIT:
            err(f"skills/{name}: description {len(desc)} > {DESC_LIMIT}")
        else:
            check_desc_quality(f"skills/{name}", desc)
        if not TRIGGER_RE.search(desc):
            warn(f"skills/{name}: description lacks a 'Use when/for/at/before' trigger clause")
        if desc in seen_desc:
            err(f"skills/{name}: duplicate description of '{seen_desc[desc]}'")
        seen_desc[desc] = name

        md = meta.get("metadata") or {}
        if not isinstance(md, dict):
            err(f"skills/{name}: metadata must be a mapping")
            md = {}
        for key in REQUIRED_META:
            if not md.get(key):
                err(f"skills/{name}: metadata.{key} missing")
        if md.get("domain") and md["domain"] not in DOMAINS:
            err(f"skills/{name}: domain '{md['domain']}' not in {DOMAINS}")
        owner = md.get("owned-by-agent")
        if owner and owner not in agent_names:
            err(f"skills/{name}: owned-by-agent '{owner}' has no agent file")
        if md.get("status") not in ("active", "deprecated", "experimental"):
            warn(f"skills/{name}: status '{md.get('status')}' unexpected")
        for pat in STALE_PATTERNS:
            if pat in body or pat in str(meta):
                err(f"skills/{name}: stale reference to '{pat}'")
        for ref_file in skill_dir.rglob("*.md"):
            if ref_file == path:
                continue
            ref_text = io.open(ref_file, encoding="utf-8", errors="replace").read()
            for pat in STALE_PATTERNS:
                if pat in ref_text:
                    err(f"{ref_file.relative_to(ROOT)}: stale reference to '{pat}'")

        # required structural sections (agent-browser is an intentional CLI stub)
        if name != "agent-browser":
            for section in ("## WHEN TO USE", "## WHEN NOT TO USE", "## VERIFICATION GATE"):
                if section not in body:
                    warn(f"skills/{name}: missing '{section}'")
        lines = body.count("\n")
        if lines > 500:
            warn(f"skills/{name}: body {lines} lines (>500) — consider references/")
        check_links(path, body, skill_dir)

        skills.append({
            "name": name,
            "domain": md.get("domain", "?"),
            "grade": md.get("grade", "?"),
            "status": md.get("status", "?"),
            "owner": owner or "?",
            "trigger": short_trigger(desc),
            "lines": lines,
        })

    # cross-file: agent referenced in AGENTS.md must exist
    agents_md = ROOT / "AGENTS.md"
    if not agents_md.exists():
        err("AGENTS.md missing")
    else:
        text = agents_md.read_text(encoding="utf-8")
        for ref in sorted(set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text))):
            if ref in {s["name"] for s in skills}:
                continue
            if ref in agent_names:
                continue
            if ref in {"debate-protocol", "context-engineering"}:
                continue
        for ref in sorted(set(AGENT_REF_RE.findall(text))):
            if ref[1] not in agent_names:
                err(f"AGENTS.md: dangling agent reference '{ref[1]}'")
        if "ASK EVERY TIME" not in text:
            err("AGENTS.md: permission matrix for commit/push missing")

    # ---- routing fixture ----
    cases_path = ROOT / "tools" / "routing_cases.json"
    if cases_path.exists():
        import json
        data = json.loads(cases_path.read_text(encoding="utf-8"))
        cases = data.get("cases", [])
        skill_names = {s["name"] for s in skills}
        sizes = {"small", "big"}
        works = {"development", "security", "roblox", "other"}
        security_skills = {"threat-modeling", "security-hardening-specialist", "roblox-security", "roblox-asset-security"}
        dev_skills = {"test-driven-development", "verification-before-completion"}
        seen_work: set[str] = set()
        for i, case in enumerate(cases, 1):
            if case.get("skill") and case["skill"] not in skill_names:
                err(f"routing_cases[{i}]: unknown skill '{case['skill']}'")
            if case.get("agent") and case["agent"] not in agent_names:
                err(f"routing_cases[{i}]: unknown agent '{case['agent']}'")
            if not case.get("query"):
                err(f"routing_cases[{i}]: empty query")
            size = case.get("size")
            if size is not None and size not in sizes:
                err(f"routing_cases[{i}]: size must be one of {sorted(sizes)} (got {size!r})")
            if size == "big" and not case.get("agent"):
                err(f"routing_cases[{i}]: 'big' tasks must dispatch an agent (sizing gate)")
            if size == "small" and case.get("agent"):
                warn(f"routing_cases[{i}]: 'small' task names an agent — sizing gate says no subagent")
            # ---- relevance gate: mandatory co-skills per AGENTS.md §7.1 ----
            loaded = {case.get("skill")} | set(case.get("skills") or [])
            loaded.discard(None)
            for s in case.get("skills") or []:
                if s not in skill_names:
                    err(f"routing_cases[{i}]: unknown co-skill '{s}'")
            work_list = case.get("work") or []
            if isinstance(work_list, str):
                work_list = [work_list]
            if not isinstance(work_list, list):
                err(f"routing_cases[{i}]: 'work' must be a list or string")
                work_list = []
            for w in work_list:
                if w not in works:
                    err(f"routing_cases[{i}]: unknown work type '{w}' (allowed: {sorted(works)})")
                    continue
                seen_work.add(w)
                if w == "development" and not (loaded & dev_skills) == dev_skills:
                    missing = sorted(dev_skills - loaded)
                    err(f"routing_cases[{i}]: development work must load {missing} (relevance gate)")
                if w == "security" and not (loaded & security_skills):
                    err(f"routing_cases[{i}]: security work must load one of {sorted(security_skills)} (relevance gate)")
                if w == "roblox" and not any(s.startswith("roblox-") for s in loaded):
                    err(f"routing_cases[{i}]: roblox work must load a roblox-* skill (relevance gate)")
        if len(cases) < 8:
            warn("routing_cases.json: fewer than 8 cases — coverage is thin")
        for w in sorted(works - {"other"}):
            if w not in seen_work:
                warn(f"routing_cases.json: no case with work='{w}' — relevance gate untested for it")
        if not any(c.get("size") == "small" for c in cases):
            warn("routing_cases.json: no 'small' case — the sizing gate's no-subagent path is untested")
        if not any(c.get("size") == "big" for c in cases):
            warn("routing_cases.json: no 'big' case — the sizing gate's mandatory-subagent path is untested")
    else:
        warn("tools/routing_cases.json missing — routing is untested")

    # ---- index ----
    if args.write_index:
        INDEX.write_text(render_index(skills, len(agent_names)), encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)} ({len(skills)} skills, {len(agent_names)} agents)")

    # ---- report ----
    print(f"skills: {len(skills)}   agents: {len(agent_names)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if warnings and args.strict:
        print(f"\n0 errors, {len(warnings)} warning(s) (strict)")
        return 2
    print(f"\nclean ({len(warnings)} warning(s))")
    return 0


def render_index(skills: list[dict], agent_count: int) -> str:
    out = [
        "<!-- Generated by tools/lint_config.py --write-index. Do not edit by hand. -->",
        "# Skill Index",
        "",
        f"{len(skills)} skills across {len(DOMAINS)} domains · {agent_count} agents · v3.0.0 · "
        "reviewed 2026-10-22",
        "",
        "Discovery uses each skill's `description`; this file is for humans and maintenance.",
        "Routing rules live in [AGENTS.md](../AGENTS.md) §7.",
        "",
    ]
    for domain in DOMAINS:
        rows = [s for s in skills if s["domain"] == domain]
        if not rows:
            continue
        out += [f"## {domain}", "",
                "| Skill | Grade | Owner agent | Use when |",
                "|---|---|---|---|"]
        for s in sorted(rows, key=lambda x: x["name"]):
            trigger = s["trigger"].replace("|", "\\|")
            status = "" if s["status"] == "active" else f" *({s['status']})*"
            out.append(f"| `{s['name']}`{status} | {s['grade']} | `{s['owner']}` | {trigger} |")
        out.append("")
    out += [
        "## Maintenance",
        "",
        "```bash",
        "python tools/lint_config.py               # validate",
        "python tools/lint_config.py --write-index # regenerate this file",
        "```",
        "",
        "Add a skill: create `skills/<name>/SKILL.md` with the standard frontmatter, add it to a",
        "domain table in AGENTS.md §7, then lint. Retire a skill: set `status: deprecated` and point",
        "its description at the replacement; delete only after references are gone.",
        "",
    ]
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
