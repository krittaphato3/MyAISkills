---
name: principle-explain-the-number
description: >-
  Vets a measurement before it is trusted, reported, or acted on: what produced it, what limits
  it, and whether it measured the thing you think. Use before quoting any benchmark, latency,
  coverage, or cost figure. Routes benchmark design to performance-profiler.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: performance-engineer
---

# Explain the Number

A number you cannot explain is a rumor with decimals.

Before a measurement changes a decision, answer three questions: what produced it, what limits
it, and what else could have produced the same value. If you cannot answer the third, the number
is not evidence yet.

## WHEN TO USE

- About to report a speedup, a regression, a coverage figure, a cost, or a failure rate.
- A benchmark result is surprising in either direction.
- Comparing two implementations, two runs, or two environments.
- A subagent or tool reports a metric you are about to repeat.

## WHEN NOT TO USE

- The number is an input to a calculation whose sensitivity you already know.
- Exact counts from a deterministic operation (rows returned, files matched).
- The measurement is only a smoke signal and no decision rests on it. Say so.

## DECISION TREE

```text
1. WHAT PRODUCED IT
   Command, harness, input size, environment, cache state, run count. If you cannot name the
   command, you cannot cite the number.

2. WHAT LIMITS IT
   Noise floor, sample size, cold start, network, thermal state, dataset skew, measurement
   overhead. Name the dominant limiter.

3. WHAT ELSE COULD PRODUCE IT
   The wrong function measured, the cache serving the result, the test not exercising the path,
   the input too small to matter. Rule each out explicitly.

4. IS THE DIFFERENCE REAL
   Compare distributions, not single runs. Median plus tail, same conditions, enough runs.
   A 5% delta inside a 20% noise band is not a delta.

5. LABEL AND REPORT
   measured (with command), inferred (with reasoning), or guess. Never upgrade a label silently.
```

## FAILURE MODES & MITIGATIONS

1. **Single-run theater** — one fast run reported as the result. *DETECT:* no run count. *FIX:* at least 5 runs, median and p95.
2. **Environment drift** — before and after measured under different conditions. *DETECT:* different machine, build, dataset, or cache state. *FIX:* re-measure both on one setup.
3. **Wrong target** — the benchmark measures a helper, not the hot path. *DETECT:* the profile does not name the changed function. *FIX:* confirm with a profiler.
4. **Denominator games** — coverage or cost improved because the base changed. *DETECT:* totals moved without the numerator moving. *FIX:* compare like populations.
5. **Precision without accuracy** — three significant figures from a noisy harness. *DETECT:* decimals beyond the noise floor. *FIX:* round to what the measurement supports.
6. **Survivorship timing** — only successful runs counted. *DETECT:* timeouts and errors excluded. *FIX:* include failures in the distribution.

## VERIFICATION GATE

- [ ] Command and environment named.
- [ ] Run count and spread reported, not one value.
- [ ] Dominant limiter stated.
- [ ] Alternative explanations ruled out in writing.
- [ ] Every figure labeled measured, inferred, or guess.

## REFERENCES

- `performance-profiler` — building the harness
- Benchmark review standard: before/after table, pinned environment, stated run count
- `verification-before-completion` — claim to artifact mapping
- `token-economy` — cost figures and their limits
