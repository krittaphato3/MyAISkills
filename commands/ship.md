---
description: Run the full pre-merge gate, then commit through git-master
---
Run the pre-merge gate end-to-end per AGENTS.md §4 and §7.

1. Load `verification-before-completion`. Every applicable Definition-of-Done box must have an attached artifact (tests, lint/typecheck, review verdict, benchmarks where performance was touched).
2. Dispatch `red-team-qa` with `requesting-code-review`. The verdict must be PASS or CONDITIONAL with every finding addressed. A FAIL stops here.
3. If and only if the gate is green, dispatch `git-master` to commit using a Conventional Commit message that explains **why**, staging only the named paths for this change.

Hard limits: do NOT push, do NOT open a PR, do NOT merge, do NOT force any operation. If the gate is red, report what failed and stop.

State before:
!`git status --short`
!`git diff --stat`
