---
description: Map an unfamiliar codebase and emit a project-level AGENTS.md
agent: codebase-cartographer
subtask: true
---
Dispatch the `codebase-cartographer` subagent per AGENTS.md §3 to map this repository: stack, entry points, one vertical slice, conventions, verified commands, risk zones, and a ranked "start here".

Focus (optional): $ARGUMENTS

Then:
1. Load the `session-continuity` skill and write the handoff so the next session resumes without re-deriving.
2. Emit a **proposed project-level `AGENTS.md`** for this repository containing only project-specific facts a fresh agent needs: build / lint / typecheck / test / dev commands (verified, with observed exit status), repo layout and non-obvious architecture, conventions and gotchas. Keep it under ~60 lines. Do not invent conventions — cite `file:line` for every claim, and mark anything unverified as UNKNOWN.
3. Tell the user to review and commit it. Do not commit it yourself.
