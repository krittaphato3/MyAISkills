#!/usr/bin/env python3
"""Validate routing_cases.json schema, referential integrity, and description collisions.

Usage:
    python tools/test_routing.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES_FILE = ROOT / "tools" / "routing_cases.json"
SKILLS_DIR = ROOT / "skills"
AGENTS_DIR = ROOT / "agents"

STOPWORDS = {
    "the", "and", "for", "with", "when", "use", "from", "into", "this", "that",
    "your", "are", "not", "all", "any", "how", "what", "why", "who", "you",
    "can", "only", "make", "work", "code", "file", "files", "before", "after",
}


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) >= 3 and w not in STOPWORDS}


def load_frontmatter(path: pathlib.Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    parts = raw.split("---", 2)
    return (yaml.safe_load(parts[1]) or {}) if len(parts) >= 3 else {}


def main() -> int:
    skills = {}
    for p in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm = load_frontmatter(p)
        skills[p.parent.name] = fm

    agents = {}
    for p in sorted(AGENTS_DIR.glob("*.md")):
        agents[p.stem] = load_frontmatter(p)

    data = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    errors: list[str] = []
    tested_skills: set[str] = set()
    tested_agents: set[str] = set()

    for idx, case in enumerate(cases, 1):
        q = case.get("query", "")
        sk = case.get("skill")
        co = case.get("skills") or []
        ag = case.get("agent")

        if not q.strip():
            errors.append(f"case {idx}: empty query")
        if sk is not None:
            if sk not in skills:
                errors.append(f"case {idx}: unknown primary skill '{sk}'")
            else:
                tested_skills.add(sk)
        for csk in co:
            if csk not in skills:
                errors.append(f"case {idx}: unknown co-skill '{csk}'")
            else:
                tested_skills.add(csk)
        if ag is not None:
            if ag not in agents:
                errors.append(f"case {idx}: unknown agent '{ag}'")
            else:
                tested_agents.add(ag)

    # Check high-Jaccard description collisions across active skills
    active_toks = {
        name: tokens(f"{name} {fm.get('description', '')}")
        for name, fm in skills.items()
        if not fm.get("disable-model-invocation")
    }
    names = sorted(active_toks)
    collisions: list[tuple[float, str, str]] = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ta, tb = active_toks[a], active_toks[b]
            if not ta or not tb:
                continue
            jacc = len(ta & tb) / len(ta | tb)
            if jacc >= 0.50:
                collisions.append((jacc, a, b))

    for jacc, a, b in collisions:
        errors.append(f"description collision (Jaccard={jacc:.2f}): {a} <-> {b}")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    print(
        f"ROUTING OK: {len(cases)} cases passed | "
        f"skills covered={len(tested_skills)}/{len(skills)} | "
        f"agents covered={len(tested_agents)}/{len(agents)} | "
        f"collisions=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
