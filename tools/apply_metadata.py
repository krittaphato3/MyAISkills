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
