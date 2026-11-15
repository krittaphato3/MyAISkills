---
description: Reproduce, root-cause, and fix a bug, flake, or red gate
---
Load the `systematic-debugging` skill and apply it to: $ARGUMENTS

Sequence — do not skip steps:
1. REPRODUCE — get a deterministic failing case; attach the raw output as evidence.
2. ISOLATE — narrow to the smallest failing unit; bisect if needed.
3. ROOT CAUSE — state the cause explicitly; a symptom patch is a failure.
4. FIX — load `test-driven-development`; dispatch a subagent per AGENTS.md §3 to make the change.
5. REGRESSION TEST — add the exact repro as a test; attach the green run.

Route per AGENTS.md §3 (a DB query problem routes to `query-performance-engineer`, a concurrency issue to `concurrency-engineer`). Report with the evidence attached per `verification-before-completion`.

Current state:
!`git status --short`
