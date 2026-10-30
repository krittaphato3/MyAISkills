---
name: test-driven-development
description: >-
  Drives behavior changes with a failing test first: RED for the right reason, GREEN with the
  minimum code, REFACTOR while green, plus coverage and test-pyramid discipline. Use for features,
  bug fixes, and pinned refactors. Exploration spikes and doc-only changes are exempt; reviewing
  the result routes to requesting-code-review.
metadata:
  version: 3.1.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: test-engineer
---

# Test-Driven Development

The point of TDD is not the order of the keystrokes; it is that a test you have seen fail is the
only proof the test can detect the bug you are about to fix. A test written after the code passes
on the first run and proves nothing.

## WHEN TO USE

- Any feature, bug fix, or behavior change in production code.
- A refactor: pin current behavior with characterization tests *before* moving code.
- A bug report: reproduce it as a failing test before touching the implementation.
- A regression after an incident: the escaped bug becomes a permanent test.

## WHEN NOT TO USE

- Throwaway exploration ("will this API even work?") — delete the spike, then TDD the kept part.
- Doc-only, comment-only, or config-only changes — run the existing suite instead.
- Generated code — test the generator or the contract, not the output.
- A user explicitly waives it for a ≤5-line trivial fix — record why in the report.

## DECISION TREE

```text
1. WRITE ONE FAILING TEST
   Assert observable behavior, not internals. Name it: should {expected} when {condition}.
   Run it. Confirm it fails for the reason you expect — not a typo, not a missing import.

2. RED EVIDENCE
   Save the failure output (assertion, expected vs actual). This is the artifact that proves
   the test has teeth. No RED = you do not know the test works.

3. GREEN — MINIMUM CODE
   Implement only enough to pass. No speculative abstraction, no extra options, no drive-by
   cleanup. If you cannot make it pass in a small step, the test is too big: split it.

4. REFACTOR WHILE GREEN
   Remove duplication, name things, extract seams. Run the suite after each move. Behavior
   never changes in this phase.

5. BROADEN THE NET
   Add the cases the first test missed: empty/null, boundary values, error paths, large input,
   concurrency, and one integration case if a real boundary is involved.

6. RUN THE FULL SUITE + LINT
   Green only counts if the whole suite and the typechecker agree. Fix regressions you caused;
   do not "fix" them by relaxing assertions.
```

## PATTERNS

### 1. Red-first proof (the artifact)
```text
RUN: npx vitest run tests/invoice.test.ts
FAIL  should reject a zero-amount invoice
  expected 400, received 201        ← the behavior is missing
PASS  (3 other cases)
```
Then after the fix: same command, all green. Report both.

### 2. Good test anatomy
- **Arrange** the smallest world that exposes the behavior.
- **Act** once — one action per test.
- **Assert** the outcome the requirement names, not the implementation's side effects.
- Independent: no order dependency, no shared mutable fixtures.
- Deterministic: fake the clock, seed randomness, pin timezone/locale.
- Fast: unit <100ms, integration <1s; slow tests are integration/e2e by definition.

### 3. Test pyramid and where to spend
```text
Unit          many    pure logic, validation, state machines, edge cases
Integration   some    DB queries, HTTP handlers, queue consumers, transactions
E2E           few     one per critical user journey; never the main safety net
```
Push assertions down: a rule that can be a unit test should not be an E2E test.

### 4. Assertions that actually test behavior
| Weak | Strong |
|---|---|
| `expect(fn).toHaveBeenCalled()` | `expect(result).toEqual({...})` |
| 200 status only | status + body shape + persisted row |
| snapshot of everything | targeted fields + one invariant |
| no exception thrown | the specific error type/code for the bad input |
| coverage says 100% | each branch asserted with a distinct expectation |

### 5. Bug-fix protocol
1. Reproduce with the user's input (or the smallest input that still fails).
2. Assert the *correct* behavior — the test fails now.
3. Fix the mechanism, not the symptom (`systematic-debugging`).
4. Keep the repro as the regression test, named after the bug.
5. Confirm the test fails if the fix is reverted (mutation sanity check, at least mentally).

### 6. Independence for high-stakes work
For T3 changes, tests come from `test-oracle`, written against the spec before the implementation
exists. Tests written by the implementer are smoke checks, not an independent oracle — they encode
the same misunderstanding as the code.

### 7. Where red-first pays, and where it does not

Red-first has real signal when the failure predates the fix: you watch the same command flip.
That is the bug-fix case, and it is the case worth defending.

For greenfield features, design before tests. Name the data shape, edge cases, and contracts
first; tests derived from a design are stronger than a design derived from the first test. When
the agent writes both the test and the implementation, a red step only proves the agent ran
something. The evidence that survives that critique is a test that fails when the behavior is
deliberately broken, which is what `mutation-testing` measures.

Practical split:

| Situation | Approach |
|---|---|
| Bug fix with a cheap local repro | Red-first. Required. |
| Greenfield feature | Design first, then tests per slice, then verify behavior |
| Legacy behavior nobody documented | Characterization tests before any change |
| Agent wrote code and tests together | Mutation pass, or an independent oracle on T2/T3 |
| Refactor | Pin behavior first, change structure, stay green |

Do not turn this into a reason to skip tests. The rule that survives every case is: a test you
have never seen fail is a test you cannot trust.

## FAILURE MODES & MITIGATIONS

1. **Test-after theater** — test written after the code, passes immediately. *DETECT:* no RED run
   recorded. *FIX:* stash the implementation, watch it fail, restore.
2. **Wrong-reason RED** — fails on a syntax/import error rather than the behavior. *DETECT:* failure
   message unrelated to the assertion. *FIX:* fix the harness, re-run until the assertion fails.
3. **Assertion-free coverage** — lines executed, outcomes unasserted. *DETECT:* coverage high, bugs
   escape. *FIX:* assert values, not calls; add edge cases.
4. **Over-mocking** — the test verifies the mocks. *DETECT:* changing an internal call breaks tests
   while behavior is unchanged. *FIX:* mock only at real boundaries (network, clock, DB).
5. **Flaky green** — passes sometimes. *DETECT:* rerun fails. *FIX:* quarantine, fix determinism,
   never ship a retrying test as proof.
6. **Giant first test** — 40 assertions, unclear failure. *DETECT:* one test, many reasons to fail.
   *FIX:* split into one behavior per test.
7. **Suite erosion** — tests skipped/deleted to get green. *DETECT:* new `skip`/`only`/`xfail`.
   *FIX:* revert; fix or report the real failure.

## QUANTITATIVE RULES

- ≥80% line coverage on new code; 100% on money/auth/data-integrity paths.
- One RED→GREEN cycle per behavior; batching >3 behaviors per cycle is a violation.
- Unit <100ms, integration <1s, E2E <30s; suites that exceed this are misclassified.
- Full suite + typecheck green before any "done" claim; flaky retries ≤2 then quarantine.
- Every fixed bug gets exactly one regression test that fails on revert.

## VERIFICATION GATE

- [ ] RED output attached, failing for the expected reason.
- [ ] GREEN output attached: full suite + typecheck, not only the new test.
- [ ] Refactor happened with the suite green throughout (if refactoring occurred).
- [ ] Edge/error cases covered, not just the happy path.
- [ ] No assertion weakened, skipped, or deleted to pass.
- [ ] Regression test exists for each bug fixed and is proven to catch it.

## REFERENCES

- `verification-before-completion` — what counts as a passing artifact
- `systematic-debugging` — finding the mechanism before writing the fix
- `test-oracle` (agent) — independent tests for T3 reviews
- `requesting-code-review` — what happens after green
