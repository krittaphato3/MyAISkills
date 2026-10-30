---
name: benchmark-checklist
description: >-
  Runs the pre-report checklist on a measurement: the exact command, environment, run count, noise
  band, denominator, and the alternative explanation that could produce the same number. Use when
  a benchmark, latency, coverage, or cost figure is about to be quoted in a report or PR. The
  reasoning behind it routes to principle-explain-the-number.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: performance-engineer
---

# Benchmark Checklist

A number becomes evidence only after someone can reproduce it and rule out the boring explanation.
This is the gate between "I measured something" and "I am reporting this as a result".

## WHEN TO USE

- About to put a speed, latency, size, coverage, or cost figure in a reply, PR, or doc.
- A benchmark moved in a surprising direction, fast or slow.
- Comparing two implementations, two branches, or two environments.
- A tool or subagent handed you a metric you intend to repeat.

## WHEN NOT TO USE

- Deterministic counts with no measurement involved: rows returned, files matched, tests passed.
- The number is an internal intermediate that no decision or claim depends on.
- The reasoning is the question rather than the procedure; use the principle instead.

## DECISION TREE

```text
1. NAME THE COMMAND
   Copy the exact invocation. If it took flags, seeds, or env vars, they are part of the number.

2. NAME THE ENVIRONMENT
   Machine, CPU class, memory, build mode, dataset size, cache state, network. Before and after
   must share all of it, or the comparison is void.

3. COUNT THE RUNS
   One run is an anecdote. Five minimum. Report median and p95, not the best run.

4. FIND THE NOISE BAND
   Run the unchanged baseline twice. The spread between those runs is your resolution. A delta
   smaller than the band is not a delta.

5. CHECK THE DENOMINATOR
   Per request, per row, per user, per token. A ratio that improved because the base shrank is
   not an improvement.

6. RULE OUT THE ALTERNATIVE
   Wrong function measured, cache serving the result, path not exercised, input too small to
   matter, warm-up excluded. Name each and say why it is not the explanation.

7. LABEL THE RESULT
   measured with its command, inferred with its reasoning, or guess. Never upgrade the label.
```

## FAILURE MODES & MITIGATIONS

1. **Best-of-n reporting** — the fastest run quoted as the result. *DETECT:* no run count. *FIX:* median plus p95 across at least five runs.
2. **Environment drift** — before and after on different builds or datasets. *DETECT:* the two commands differ. *FIX:* re-measure both on one setup.
3. **Wrong target** — the harness times a helper, not the hot path. *DETECT:* the profiler disagrees with the benchmark. *FIX:* confirm with a profile.
4. **Warm-up included** — first-run compilation folded into the average. *DETECT:* high variance between runs. *FIX:* discard warm-up explicitly and say so.
5. **Denominator games** — a ratio improved while the absolute value got worse. *DETECT:* numerator and denominator both moved. *FIX:* report the absolute number too.
6. **Precision theatre** — three decimals from a noisy harness. *DETECT:* precision exceeds the noise band. *FIX:* round to what the measurement supports.

## VERIFICATION GATE

- [ ] Command and environment named, identical before and after.
- [ ] At least five runs; median and p95 reported.
- [ ] Noise band measured and the delta exceeds it.
- [ ] Denominator and base population stated.
- [ ] Alternative explanations ruled out in writing.
- [ ] Every figure labeled measured, inferred, or guess.

## REFERENCES

- `principle-explain-the-number` — why an unexplained number is a rumor
- `performance-profiler` — building the harness
- `web-performance` — browser-side measurement
- `ship-gate` — where the claim is audited
