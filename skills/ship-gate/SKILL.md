---
name: ship-gate
description: >-
  The last gate before "done": audits every claim against the diff, re-runs the checks after the
  final edit, dispatches an independent verdict on the exact head, and states blast radius,
  rollback, and what was not verified. Use before reporting a non-trivial change complete or
  asking for commit, push, or deploy approval.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G3
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: red-team-qa
---

# Ship Gate

Green is not safe. A green suite says the checks you have agree with the code you wrote. It says
nothing about the requirement you misread, the path nobody tested, or the claim you are about to
make in the summary.

This gate is the difference between "it works on my machine" and "I can defend this in review".

## WHEN TO USE

- Before reporting a non-trivial change complete.
- Before asking for commit, push, merge, or deploy approval.
- After a subagent reports success and before that work is integrated.
- When a change touches auth, money, migrations, PII, or a public contract.

## WHEN NOT TO USE

- T0 work: a typo, a docs sentence, a one-line fix with an obvious check.
- An unmerged spike that will be deleted.
- Active incident rollback. Restore first, gate afterwards.

## DECISION TREE

```text
1. FREEZE THE HEAD
   Note the exact commit or working-tree state being gated. Any later edit voids the verdict.

2. RUN THE DETERMINISTIC CHECKS
   Typecheck, lint, full test suite, build if the build is the artifact.
   Preserve exit status. Capture raw output. Run after the last edit.

3. AUDIT CLAIMS AGAINST THE DIFF
   For every sentence you intend to report: which hunk proves it?
   No hunk -> delete the claim or do the work. This catches "adds tenant isolation" when the
   diff filters by user id.

4. CHECK THE DIFF ITSELF
   Unrelated files, dead code, debug prints, weakened tests, new suppressions, secrets,
   an abstraction with one caller, a config change nobody mentioned.

5. DISPATCH THE INDEPENDENT VERDICT
   Fresh-context reviewer, edit denied, briefed with intent + criterion + diff + evidence.
   It re-runs the check on this head. Findings need a reproduction to be blockers.

6. STATE THE BLAST RADIUS
   Who else calls the changed path. What breaks if this is wrong. The rollback step.

7. REPORT AND ASK
   DONE / CHANGED / VERIFIED / GAPS, then a separate request for commit, push, or deploy.
```

## FAILURE MODES & MITIGATIONS

1. **Self-certification** — the author's own green run accepted as the verdict. *DETECT:* no independent reviewer. *FIX:* fresh context, edit denied.
2. **Claim drift** — summary promises more than the diff delivers. *DETECT:* a claim with no hunk. *FIX:* delete the claim or finish the work.
3. **Stale green** — evidence from before the final edit. *DETECT:* timestamps, changed files after the run. *FIX:* re-run.
4. **Weakened proof** — a skipped test, loosened assertion, or suppression in the diff. *DETECT:* diff scan for skip, only, ignore, disable, noqa, xfail. *FIX:* revert and fix the cause.
5. **Happy-path only** — one flow exercised, states untested. *DETECT:* no error or empty-state evidence. *FIX:* add the adjacent cases.
6. **Silent limitation** — an unrun check reported as passing. *DETECT:* no NOT RUN line. *FIX:* name it.
7. **Gate as ritual** — the checklist ticked with no artifact. *DETECT:* no command output. *FIX:* the gate is the output, not the checkbox.

## QUANTITATIVE RULES

- 1 artifact per gate. Zero artifacts means not green.
- Checks run after the final edit, never before.
- ≤2 review rounds; a third needs new evidence.
- Every claim maps to a hunk, or it is deleted.
- Blast radius names at least one caller or states "no external callers, verified by search".
- Commit, push, and deploy are three separate approvals.

## VERIFICATION GATE

- [ ] Head frozen and named.
- [ ] Typecheck, lint, and full suite green, output captured after the last edit.
- [ ] Every reported claim traces to a hunk.
- [ ] Diff scanned for unrelated changes, suppressions, secrets, debug artifacts.
- [ ] Independent reviewer verdict on this exact head.
- [ ] Blast radius and rollback stated.
- [ ] NOT RUN items listed with reasons.
- [ ] Approval requested separately for commit, push, and deploy.

## REFERENCES

- `verification-before-completion` — evidence ladder and claim table
- `requesting-code-review` — packaging and reviewer discipline
- `blast-radius` — finding the callers a diff can break
- `mutation-testing` — whether the tests can actually fail
- `AGENTS.md` §3 and §8 — permission matrix and definition of done
