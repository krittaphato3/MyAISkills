---
description: Turn a goal into an executable plan before any code is written
---
Load the `requirements-elicitation` skill and run it on: $ARGUMENTS

If the ask is already unambiguous, state a 5-8 line intent restate (Outcome / User / Why now / Success / Constraint / Out of scope) and get an explicit yes before continuing. Do not accept "whatever you think" as a yes.

Then load `deep-planner` and produce the plan: task table (id | description | deps | size+range | acceptance criterion), dependency graph, critical path, risk register, milestones.

Constraints:
- Do not write code in this command.
- Every acceptance criterion must be checkable.
- Route per AGENTS.md §3. If the work is large enough to need a PRD first, load `spec-driven-development` instead.
