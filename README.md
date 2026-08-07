# MyAISkills

Production-grade AI coding-agent system: a curated skill catalog, subagent definitions, and MCP configuration, built to a **Staff → World-class engineering standard**.

Transformed from a "vibe-coding" cheat-sheet collection into a **verify-first, gate-driven engineering system** — the anti-vibe-coding layer.

## Catalog (37 skills)

| Grade | Meaning | Count |
|---|---|---|
| **G3** | World-class: decision trees, quantitative rules, failure modes, executable verification gates | 14 |
| **G2** | Staff minimum: decision tree, failure modes, verification gate, references | 23 |

Domains: architecture (8), production (9), delivery (7), doctrine (4), meta (3), languages (3), security (2), roblox (1).

### G3 flagships
- **Systems**: systems-core-architect, distributed-systems-engineer, concurrency-engineer, database-at-scale, observability-sre, incident-response-engineer
- **Workflow** (adapted from `addyosmani/agent-skills`): requirements-elicitation, spec-driven-development, source-driven-development, doubt-driven-development
- **Architecture/planning/orchestration**: system-design-architect, adr-engineering, deep-planner, general-orchestrator

## Repo layout
```
skills/           37 graded skills (each SKILL.md = frontmatter + grade-ladder content)
agents/           23 subagent definitions (planner, solution-architect, ml-engineer, ...)
tools/            skill_lint.py (quality gate), apply_metadata.py + tests
docs/skills/      SKILLS.md index, skills.json manifest, evals/, WORKFLOW.md, CONTRIBUTING.md
docs/superpowers/ spec + implementation plan for this transformation
mcp/              MCP server config (redacted example)
AGENTS.md         operating principles
```

## Quality gate
```bash
python tools/skill_lint.py --json   # validates frontmatter, grades, sections, blanket-invoke (E5)
python tools/skill_lint.py --regen  # regenerate skills.json manifest
```
Target: **0 errors, 0 warnings on the transform catalog** (achieved at last verification).

## Operating doctrine
The system is a **verify-first engineering agentic system**, not a code generator:
- TDD-first · verification-before-completion (proof, not assertion)
- Definition of Done before work starts
- Gate-driven execution (general-orchestrator) — stop on failed gate, fix, re-verify
- Smart routing: precise triggers + domain + owner — no blanket "auto-invoke"
- Full discipline in `docs/skills/WORKFLOW.md` and `skills/system-instructions/SKILL.md`

## MCP
Copy `mcp/mcp-config.example.json` into your client's MCP config and set your GitHub token. See `mcp/`.