---
description: Resume work from the last handoff without re-deriving anything
---
Load the `session-continuity` skill and follow its resume protocol:

1. Read the handoff file first — before any file exploration or grep.
2. Restate GOAL + STATUS + NEXT in one line.
3. Confirm the recorded CONSTRAINTS still hold (the repo may have moved since).
4. Spot-check that DONE items still pass; a stale "done" is a task, not a fact.
5. Execute the recorded NEXT action.

Do not re-open recorded DECISIONS; ask only if a constraint now conflicts. If no handoff exists, say so and offer `/onboard` instead of guessing.

Files present:
!`ls -1 .agent 2>/dev/null || echo "(no .agent directory)"`
