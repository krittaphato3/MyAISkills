---
description: Activate Ozone Mode
argument-hint: [task description]
---

Activate Ozone Mode with Staff-level engineering rigor:
- Domain modeling and strict type invariants first
- Parallel multi-subagent dispatch: implementer (`code-implementer`) + independent test oracle (`test-oracle`) running simultaneously in one turn
- Zero-token local defense: compiler (`tsc --noEmit`), linters, and local test runners
- Anti-slop: delete speculative abstractions, keep functions under 40 lines
- Guard the context window: isolate large scans inside subagents

Task: $ARGUMENTS