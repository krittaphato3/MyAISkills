---
name: verification-before-completion
description: >-
  Blocks false 'done' claims by requiring a checkable criterion and an attached artifact: test
  output, lint or typecheck log, benchmark table, reproduction, or diff evidence. Use before
  reporting any task complete, and whenever words like fixed, passes, faster, or secure appear. A
  screenshot alone never suffices.
metadata:
  version: 3.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: test-engineer
---

# Verification Before Completion

Done = a checkable criterion plus an artifact that proves it. Everything else is a hypothesis.
This is the cheapest quality mechanism in the system: one command often prevents a whole class of
wrong claims.

## WHEN TO USE

- Before saying "done", "fixed", "works", "passes", "faster", "safer", or "ready to merge".
- At every gate in multi-step work, and before any integration smoke test.
- When a subagent reports success — verify its claim before accepting it.
- When a check cannot be run: say so, with the reason, and mark the work unverified.

## WHEN NOT TO USE

- Mid-planning, before any artifact could exist — record confidence and assumptions instead.
- Pure factual answers backed by a cited source — that citation *is* the artifact.
- Review work (a verdict is the artifact) — but the verdict still needs evidence behind it.

## DECISION TREE

```text
1. NAME THE CRITERION
   One sentence, written before the work: "X returns 404 for another tenant's id".
   If the user wrote it, quote it verbatim. If it is vague, make it measurable first.

2. CHOOSE THE CHEAPEST REAL CHECK
   Behavior change   → the test that would fail without the change
   Type contract     → typecheck / compiler
   Style/regression  → lint (whole project, not just touched files)
   Performance       → benchmark: before/after, pinned env, ≥5 runs, median + p75
   Security          → traversal/IDOR/forged-signature cases + scanner output
   UI                → DOM/HTTP assertion or test; screenshot is supporting only
   Data              → query with counts + checksum before/after
   Docs/config       → render/link check or a dry run
   None available    → state the gap; propose the check that should exist

3. RUN IT, CAPTURE RAW OUTPUT
   The exact command + its actual output. Not a paraphrase. Not a memory of an earlier run.
   Exit status counts: preserve it (pipefail / explicit capture).

4. COMPARE AGAINST THE CRITERION, NOT A PROXY
   Green suite ≠ feature implemented if no test covers the feature. Build success ≠ runtime
   behavior. A screenshot ≠ correct state after interaction.

5. ATTACH AND REPORT
   Criterion · command · result · artifact path. Red = not done: fix or report blocked.
   Partial evidence for a partial change is fine *if labeled*.
```

## PATTERNS

### 1. Evidence ladder (strongest first)
1. Failing-before / passing-after test on the exact behavior.
2. Reproduction script that no longer reproduces the bug.
3. Existing suite + lint + typecheck, all green, with output.
4. Benchmark with pinned conditions and before/after numbers.
5. Type-level proof (compiler rejects the bad state).
6. Live request/response or DOM assertion against the running artifact.
7. Diff review against the spec (a human/agent verdict).
8. Reasoned argument with file:line references — weakest; never sufficient alone.

### 2. Claim → required artifact
| Claim | Minimum artifact |
|---|---|
| "Fixed the bug" | Repro that failed before, passes now; regression test path |
| "Tests pass" | Full suite output + count; not "the relevant ones" |
| "Types are fine" | `tsc --noEmit` / `cargo check` / `mypy` output |
| "Faster" | Before/after table, ≥5 runs, p50+p95, same machine/build |
| "Secure" | The attack case run and rejected + the control that rejects it |
| "Works end to end" | One real request/DOM flow exercised, with output |
| "No regressions" | Full suite + the specific adjacent behavior exercised |
| "Clean" | Lint/format output, zero findings |

### 3. Gate vocabulary
```text
GREEN    criterion met, artifact attached (path + summary)
RED      criterion not met → fix or roll back; blocks the next step
FLAKY    passed on retry (≤2) — root cause recorded, never silently accepted
UNGATED  dispatched but never verified — treated as RED
BLOCKED  check cannot run — say why; work is unverified, not done
```

### 4. Verification of someone else's claim
Read the artifact, not the summary. Re-run the command when cheap. Look for the gap between "the
test passes" and "the requirement is met" — that gap is where most false green lives.

### 5. Honest limitation reporting
```text
VERIFIED   tests/api.test.ts::tenant_isolation — pass (12/12 suite green)
NOT RUN    e2e — no browser available in this environment
LIMITATION visual layout unverified; logic covered by DOM assertions
```

## FAILURE MODES & MITIGATIONS

1. **Verification theater** — the gate checks something adjacent because it is easy. *DETECT:* the
   artifact does not mention the criterion. *FIX:* re-run the exact criterion; if impossible, say so.
2. **Looks-done** — "should work now". *DETECT:* no command, no output. *FIX:* run it.
3. **Stale evidence** — an earlier run is presented as proof of the current code. *DETECT:* artifact
   predates the last edit. *FIX:* re-run after the final change; earlier results do not carry.
4. **Proxy green** — build passes, behavior untested. *DETECT:* no test path for the changed branch.
   *FIX:* write the behavioral check.
5. **Partial scope** — one case proves "the feature". *DETECT:* only the happy path was exercised.
   *FIX:* checklist from the spec; at least one edge and one error path.
6. **Suppressed failure** — skip/ignore added to make it green. *DETECT:* new `skip`, `only`,
   `@ts-ignore`, `eslint-disable`, `# noqa`, `xfail` in the diff. *FIX:* remove; fix the cause or
   report it as a real limitation.
7. **Exit-status loss** — piping through `tail`/`grep` hides the failure. *DETECT:* command chains
   without `pipefail` or status capture. *FIX:* preserve status and inspect the output.

## QUANTITATIVE RULES

- ≥1 artifact per GREEN gate; 0 artifacts = not green, no exceptions.
- Flaky retries ≤2, then FAIL; record the root cause even if it passes.
- Performance: ≥5 runs, median + p75/p95, identical environment, before *and* after.
- Re-run affected checks after the final edit — results from before the last change do not count.
- Coverage alone never satisfies a gate; the assertion must test behavior, not lines.

## VERIFICATION GATE

- [ ] Criterion stated in one measurable sentence.
- [ ] Command run and raw output captured (exit status preserved).
- [ ] Artifact matches the criterion, not a proxy.
- [ ] Any unrun check is named with a reason and marked unverified.
- [ ] No check was weakened, skipped, or silenced to pass.
- [ ] Report contains VERIFIED / NOT RUN / LIMITATION lines.

## REFERENCES

- `AGENTS.md` §4 (reporting) and §8 (definition of done)
- `test-driven-development` — producing the RED/GREEN evidence
- `requesting-code-review` / `debate-protocol` — verdicts as evidence
- `systematic-debugging` — before/after repro evidence
