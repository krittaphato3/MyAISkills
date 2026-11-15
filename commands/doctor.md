---
description: Audit the skill/agent catalog for collisions, dangling refs, and gaps
agent: meta-architect
subtask: true
---
Load the `skill-creator` skill and run the catalog audit defined in the `meta-architect` agent.

For every `skills/*/SKILL.md`: `name` matches its directory; `description` is present, 1-1024 chars, a specific trigger with no blanket claim; no duplicate or near-duplicate trigger against another skill; `authored-by` resolves to a real `agents/*.md`.
For every `agents/*.md`: description states what it owns and when to dispatch; it appears in `AGENTS.md` §3; permissions are least-privilege.
Cross-checks: every skill and agent reachable from `AGENTS.md` §3; no route points at a missing file; no skill cites an MCP server that is not configured; every command in `commands/` points at a skill/agent that exists.

Fix what is safe to fix and record it in `ANALYSIS.md` with version bumps. Report the rest with severity.

Inventory:
!`ls -1 skills`
!`ls -1 agents`
!`ls -1 commands 2>/dev/null || echo "(no commands directory)"`
