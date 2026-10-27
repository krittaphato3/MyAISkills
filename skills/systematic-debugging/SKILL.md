---
name: systematic-debugging
description: >-
  Finds and fixes root causes: reproduce minimally, isolate by bisection, name the mechanism with
  proof, apply the smallest fix, and lock it with a regression test. Use for any bug, flake, red
  gate, or unexpected behavior. Greenfield design routes to deep-planner; an intentional behavior
  change to test-driven-development.
metadata:
  version: 3.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: code-implementer
---

# Systematic Debugging

Debugging is a search problem, and the search is over hypotheses, not edits. The failure mode this
skill prevents is the shotgun: five speculative changes, one of which accidentally works, leaving a
codebase with four unexplained mutations and no idea which one mattered.

## WHEN TO USE

- Failing test, red gate, CI failure, or a bug report with a symptom.
- Intermittent/flaky behavior, performance regression, memory growth.
- A production incident's root-cause phase (containment is `incident-response-engineer`).
- "It works locally but not in CI/deploy".

## WHEN NOT TO USE

- The behavior was never specified and is being designed — that is planning, not debugging.
- The change is intentional and the test is simply outdated — update the test deliberately.
- You are asked to make a failure go away without understanding it. Say what that would cost.

## DECISION TREE

```text
1. REPRODUCE
   Smallest known input + exact command + observed vs expected. Re-run it twice: a bug you
   cannot reproduce is not yet a bug you can fix. If it is intermittent, capture the frequency
   and the conditions (timing, concurrency, order, environment).

2. MINIMIZE
   Remove inputs, config, and steps until it barely fails. The minimal repro usually names the
   cause. A 5-line repro is worth more than 5 log statements.

3. OBSERVE (cheap signals first)
   Error text verbatim → stack trace → logs around the failure → the values at the boundary.
   Read the actual message; most "mystery" bugs are a misread error.

4. BISECT
   Time: git bisect over commits.
   Space: disable half the config/flags/features.
   Input: halve the data; find the smallest failing value.
   Code: comment out or short-circuit halves of the path.
   Each step must be a real test, not a guess.

5. HYPOTHESIZE, THEN FALSIFY
   Write the mechanism as a sentence: "X reads Y before Z commits it, so it sees the old value."
   Predict what else must be true. Check that prediction. A hypothesis that explains only the
   symptom is not yet the cause.

6. NAME THE MECHANISM
   Root cause = the specific line/order/assumption that produces the failure, quoted with
   file:line. "Race condition" is a category, not a cause; "the retry reuses the same idempotency
   key after the first write commits" is a cause.

7. FIX THE CAUSE, MINIMALLY
   Smallest change that removes the mechanism. No drive-by refactors, no unrelated hardening.
   If the correct fix is large, land the minimal correct fix first and schedule the rest.

8. LOCK IT
   The repro becomes a regression test that fails on revert. Full suite + lint green.
   Then ask: where else does this mechanism exist? (Escape analysis.)

9. REPORT
   Repro → mechanism → fix → evidence → residual risk. If it was an incident, feed the postmortem.
```

## PATTERNS

### 1. Hypothesis ledger
```text
H1 {mechanism}              predict: {what must be true}   test: {command}   result: {confirm|refute}
H2 ...
Current best: H2 (confidence 0.7) because {evidence}
```
One live hypothesis at a time. Two simultaneous changes make the result uninterpretable.

### 2. Boundary tracing
Log the value on both sides of each boundary the data crosses: request → handler → service →
query → response. The first place the value is wrong is the component to investigate. This beats
reading code hoping to spot it.

### 3. Flake protocol
- Reproduce with the seed, or with `--repeat 50`, or by forcing the suspected interleaving.
- Common causes in order: shared state between tests, real clock/timezone, unawaited async,
  ordering assumptions, network, random data, port/DB collisions.
- Record the root cause even when a retry passes. "Flaky, rerun fixed it" is how flakes become
  permanent.

### 4. Environment divergence
When it works locally but not in CI: compare runtime version, env vars, OS/path casing, installed
lockfile state, timezone/locale, network egress, and concurrency. Diff the *environment*, not the
code, until you find the first difference that matters.

### 5. Five whys, stopping at code
Keep asking why until the answer is a mechanism in the code or configuration. Stopping at "human
error" means the guardrail is missing; stopping at "the library does it" means you have not read
the library.

### 6. Escape analysis
After the fix: search for the same pattern elsewhere (same helper, same query shape, same missing
await). A bug that exists once in a codebase usually exists twice. Add a lint rule or type if the
class is mechanically detectable.

## FAILURE MODES & MITIGATIONS

1. **Shotgun fixing** — several changes at once. *DETECT:* >1 edit between test runs. *FIX:* revert
   to the last known state, one change per hypothesis.
2. **Symptom patch** — catch/ignore, retry, sleep, bump timeout. *DETECT:* the mechanism is unnamed.
   *FIX:* go back to step 5; the symptom will return under load.
3. **Unreproduced fix** — "seems better now". *DETECT:* no before/after repro. *FIX:* reproduce,
   then prove it is gone.
4. **Wrong layer** — debugging the UI for a data bug. *DETECT:* repeated fixes with no effect.
   *FIX:* boundary tracing from the source of truth outward.
5. **Log-and-pray** — adding prints without a hypothesis. *DETECT:* many logs, no prediction.
   *FIX:* state what value would confirm/refute, then log exactly that.
6. **Missing regression test** — fix without a test. *DETECT:* no new test in the diff. *FIX:* add
   the repro as a test, verify it fails on revert.
7. **Flake dismissal** — retry until green. *DETECT:* rerun-as-fix. *FIX:* quarantine + root cause.
8. **Fix-induced regression** — the fix breaks a neighbor. *DETECT:* suite red elsewhere. *FIX:*
   full suite, not just the failing test.

## QUANTITATIVE RULES

- One hypothesis and one change at a time; re-run the repro after each.
- Minimal repro: ≤20 lines or ≤3 steps; if larger, keep minimizing.
- A fix without a regression test is not complete.
- Flaky retries: ≤2 to classify, then quarantine; never >2 as a strategy.
- If 3 hypotheses fail, stop guessing and gather new data (logs, trace, `git log`, docs).

## VERIFICATION GATE

- [ ] Before: repro command + failing output captured.
- [ ] Mechanism named at file:line, in one sentence.
- [ ] After: same command passes; full suite + lint green.
- [ ] Regression test added and proven to fail on revert.
- [ ] Escape analysis done: other occurrences found or ruled out.
- [ ] Residual risk / follow-ups stated.

## REFERENCES

- `test-driven-development` — turning the repro into the regression test
- `verification-before-completion` — evidence requirements
- `incident-response-engineer` — containment before root cause
- `codebase-navigation` — locating the owning code
- `performance-profiler` — when the "bug" is a measurement
