#!/usr/bin/env python3
"""Generate docs/ROUTING.md: the exhaustive index of every skill, agent, and command.

Skill descriptions do the routing. This index exists so nothing in the catalog is
unreachable: if no routing row in AGENTS.md matches, the model reads this file
before improvising.

Usage:
    python tools/gen_routing.py
    python tools/gen_routing.py --check   # exit 1 if the file is stale
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
COMMANDS = ROOT / "commands"
OUT = ROOT / "docs" / "ROUTING.md"

DOMAINS = ["doctrine", "architecture", "delivery", "production", "security",
           "languages", "roblox", "meta", "fundamentals"]
DOMAIN_BLURB = {
    "doctrine": "Operating rules, orchestration, verification gates, and named principles.",
    "architecture": "Shape decisions: systems, APIs, data, distributed behavior.",
    "delivery": "Building and shipping: frontend, mobile, desktop, integrations, tests.",
    "production": "Running systems: performance, incidents, observability, scale.",
    "security": "Trust boundaries, defensive hardening, authorized offensive work.",
    "languages": "Language and runtime specifics.",
    "roblox": "Roblox platform work, from world building to publishing.",
    "meta": "Maintaining this configuration and the agent harness itself.",
    "fundamentals": "Cross-cutting computer science and data-structure reasoning.",
}
AGENT_GROUPS = [
    ("Routing and orchestration", ["planner", "product-strategist", "solution-architect",
                                    "debate-chair", "general-purpose", "ozone-agent", "poteto-agent"]),
    ("Implementation", ["code-implementer", "refactoring-specialist", "migration-engineer",
                         "test-engineer", "test-oracle", "independent-solver", "comment-sicko"]),
    ("Review and audit", ["red-team-qa", "requirement-auditor", "design-critic",
                           "security-auditor", "compliance-engineer", "dependency-guardian",
                           "cybersecurity-specialist", "accessibility-specialist"]),
    ("Domain engineering", ["db-architect", "data-engineer", "api-architect", "performance-engineer",
                             "algorithm-specialist", "llm-engineer", "ml-engineer", "ui-ux-architect",
                             "frontend-web-engineer", "mobile-developer", "desktop-developer",
                             "game-developer", "integration-engineer"]),
    ("Operations", ["devops-engineer", "observability-sre", "incident-response-engineer"]),
    ("Research and docs", ["deep-researcher", "codebase-cartographer", "documentation-engineer",
                            "browser-automation", "mcp-agent", "git-master", "meta-architect"]),
    ("Roblox", ["roblox-game-director", "roblox-scripter", "roblox-builder", "roblox-ui-designer",
                 "roblox-animator", "roblox-vfx-artist", "roblox-asset-artist",
                 "roblox-qa-engineer", "roblox-security-engineer"]),
]


def read(path: Path) -> str:
    return io.open(path, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")


def frontmatter(path: Path) -> dict:
    raw = read(path)
    if not raw.startswith("---\n"):
        return {}
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        # Command files may carry non-YAML hints (e.g. `argument-hint: [path]`).
        meta = {}
        for line in parts[1].splitlines():
            if ":" in line and not line.startswith((" ", "\t", "#")):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("'\"")
    return meta if isinstance(meta, dict) else {}


def trigger(desc: str, limit: int = 170) -> str:
    m = re.search(r"\b(?:Use|Apply)(?:\s+(?:only|strictly|primarily|whenever))?\s+"
                  r"(?:when|for|as|on|before|after|at|in|to)\b", desc, re.IGNORECASE)
    text = desc[m.start():] if m else desc
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "..."
    return text.replace("|", "\\|")


def one_liner(desc: str, limit: int = 150) -> str:
    text = " ".join(desc.split())
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    if len(first) > limit:
        first = first[:limit].rsplit(" ", 1)[0] + "..."
    return first.replace("|", "\\|")


def row(cells: list[str]) -> str:
    return "| " + " | ".join(str(c) for c in cells) + " |"


def build() -> str:
    skills = {}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        meta = frontmatter(path)
        md = meta.get("metadata") or {}
        if not isinstance(md, dict):
            md = {}
        skills[path.parent.name] = {
            "desc": (meta.get("description") or "").strip(),
            "domain": md.get("domain") or "?", "grade": md.get("grade") or "?",
            "status": md.get("status") or "active", "owner": md.get("authored-by") or "?",
        }
    agents = {p.stem: (frontmatter(p).get("description") or "").strip()
              for p in sorted(AGENTS.glob("*.md"))}
    commands = {p.stem: {**frontmatter(p), "desc": (frontmatter(p).get("description") or "").strip()}
                for p in sorted(COMMANDS.glob("*.md"))}

    L = ["<!-- Generated by tools/gen_routing.py. Do not edit by hand. -->",
         "# Routing index", "",
         f"Generated {date.today().isoformat()}. "
         f"**{len(skills)} skills, {len(agents)} agents, {len(commands)} commands.**", "",
         "Descriptions do the routing. This file is the coverage backstop: every skill and every "
         "agent in the catalog appears below, so a prompt with no matching row in `AGENTS.md` still "
         "has a discoverable owner. Read this before inventing a workflow.", "",
         "Retired entries stay listed with their status so old muscle memory still resolves.", ""]

    for domain in DOMAINS:
        names = sorted(n for n, s in skills.items() if s["domain"] == domain)
        if not names:
            continue
        L += [f"## {domain}", "", DOMAIN_BLURB.get(domain, ""), "",
              row(["Skill", "Grade", "Owner", "Use when"]),
              "|---|---|---|---|"]
        for n in names:
            s = skills[n]
            mark = "" if s["status"] == "active" else f" *({s['status']})*"
            L.append(row([f"`{n}`{mark}", s["grade"], f"`{s['owner']}`", trigger(s["desc"])]))
        L.append("")

    L += ["## Agents", "",
          "Dispatch with the `task` tool. Each agent runs in its own context.", ""]
    grouped = set()
    for title, names in AGENT_GROUPS:
        present = [n for n in names if n in agents]
        if not present:
            continue
        grouped.update(present)
        L += [f"### {title}", "", row(["Agent", "Use when"]), "|---|---|"]
        for n in present:
            L.append(row([f"`{n}`", trigger(agents[n], 160)]))
        L.append("")
    rest = sorted(set(agents) - grouped)
    if rest:
        L += ["### Other", "", row(["Agent", "Use when"]), "|---|---|"]
        for n in rest:
            L.append(row([f"`{n}`", trigger(agents[n], 160)]))
        L.append("")

    if commands:
        L += ["## Commands", "", row(["Command", "Description"]), "|---|---|"]
        for n, c in sorted(commands.items()):
            L.append(row([f"`/{n}`", one_liner(c["desc"])]))
        L.append("")

    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    content = build()
    if args.check:
        current = read(OUT) if OUT.is_file() else ""
        if current != content:
            print(f"{OUT.relative_to(ROOT)} is stale; rerun tools/gen_routing.py", file=sys.stderr)
            return 1
        print(f"{OUT.relative_to(ROOT)} is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
