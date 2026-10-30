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
2. **Pre-fix RED proof.** Verify raw pre-fix failure output is logged for any bugfix or new feature.
3. **Deterministic checks.** Typecheck, lint, and full workspace/package regression suite. Single-file
   test runs are rejected as final proof. Capture raw output and exit status after the last edit.
4. **Claim audit.** List every claim you intend to make. For each, name the hunk that proves it.
   No hunk means delete the claim or finish the work.
5. **Diff scan.** Line-by-line: unrelated files, dead code, debug prints, modified pre-existing tests,
   new `skip`/`only`/`ignore`/`noqa`, secrets, single-caller abstractions, or sprawl.
6. **Independent verdict.** Dispatch a fresh-context, edit-denied reviewer with intent,
   acceptance criterion, diff, and evidence. It re-runs the check on this head. Findings need a
   reproduction to block.
7. **Blast radius & rollback.** Search all direct callers (`rg -w`), formulate safety invariant,
   and specify the exact rollback command (`git restore <files>`).
8. **Report.** DONE / CHANGED / VERIFIED / GAPS, then ask separately for commit, push, or deploy.

## Refuse to pass when

- Evidence predates the last edit.
- The test run was restricted to an isolated single file rather than the workspace/package suite.
- A bugfix or new feature lacks pre-fix RED failure evidence.
- A pre-existing test was modified, weakened, or skipped without an explicit documented contract change.
- A claim has no corresponding hunk.
- Cascading breakages or file sprawl occurred without triggering the git revert circuit breaker.
- The reviewer is the author, or the reviewer edited the artifact.
- An unrun check is presented as passing.

## Output

```text
HEAD       <commit or working tree state>
RED PROOF  <command + pre-fix failure output summary>
CHECKS     <full regression suite command> -> <result>
CLAIMS     <claim> -> <file:line hunk>   (or DELETED)
DIFF AUDIT CLEAN | SPRAWL DETECTED
REVIEW     PASS | CONDITIONAL (owned follow-ups) | FAIL
BLAST      <callers via rg -w, failure mode, rollback command>
NOT RUN    <check> because <reason>
VERDICT    SHIP | HOLD
```
