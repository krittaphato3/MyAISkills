---
description: Adversarial review of the current diff against code-health criteria, severity-ranked
argument-hint: [diff, branch, PR, or file paths]
---

Run the review protocol (`requesting-code-review` + `red-team-qa`):

1. Scope the change: $ARGUMENTS (default: the working diff against the default branch).
2. Dispatch `red-team-qa` read-only with: the diff, the acceptance criteria, and test evidence.
3. Checklist: design fit · correctness · edge cases · error handling · over-engineering and
   complexity · test meaning (behavior not implementation) · naming and docs · security
   (auth boundaries, injection, secrets) · rollout and rollback risk.
4. Severity-rank findings (BLOCKER / MAJOR / MINOR) with location and a reproduction; a clean
   change gets a PASS that names what was checked instead of manufactured findings.
5. No auto-fixes: findings go to `code-implementer`; contested findings route to `debate-chair`.

Target: $ARGUMENTS
