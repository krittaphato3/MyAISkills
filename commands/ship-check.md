---
description: Run the pre-ship gate on the current change
argument-hint: [optional scope hint]
---

# Ship Check

Gate the current change before it is reported done or offered for commit: `$ARGUMENTS`

Load `ship-gate` and run it in order. Do not skip a step because the change looks small; say
`skip: <reason>` if you genuinely are.

## Sequence

1. **Freeze the head.** Name the commit or working-tree state under test. Any later edit voids
   this verdict.
2. **Deterministic checks.** Typecheck, lint, full test suite, build if the build is the artifact.
   Capture raw output and exit status, after the last edit.
3. **Claim audit.** List every claim you intend to make. For each, name the hunk that proves it.
   No hunk means delete the claim or finish the work.
4. **Diff scan.** Unrelated files, dead code, debug prints, new `skip`/`only`/`ignore`/`noqa`,
   secrets, single-caller abstractions, undocumented config changes.
5. **Independent verdict.** Dispatch a fresh-context, edit-denied reviewer with intent,
   acceptance criterion, diff, and evidence. It re-runs the check on this head. Findings need a
   reproduction to block.
6. **Blast radius.** Who else calls the changed path, what breaks if this is wrong, and the
   rollback step.
7. **Report.** DONE / CHANGED / VERIFIED / GAPS, then ask separately for commit, push, or deploy.

## Refuse to pass when

- Evidence predates the last edit.
- A claim has no corresponding hunk.
- A test was skipped, weakened, or written tautologically to get green.
- The reviewer is the author, or the reviewer edited the artifact.
- An unrun check is presented as passing.

## Output

```text
HEAD       <commit or working tree state>
CHECKS     <command> -> <result>
CLAIMS     <claim> -> <file:line hunk>   (or DELETED)
REVIEW     PASS | CONDITIONAL (owned follow-ups) | FAIL
BLAST      <callers, failure mode, rollback>
NOT RUN    <check> because <reason>
VERDICT    SHIP | HOLD
```
