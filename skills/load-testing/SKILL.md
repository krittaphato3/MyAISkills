---
name: load-testing
description: >-
  Designs and runs load, stress, soak, and spike tests that answer a capacity question: open vs
  closed workload model, arrival rate and think time, production-shaped data, percentile and
  saturation metrics, and a pass/fail decided before the run. Use when someone asks how much
  traffic a system handles, before a launch, or when capacity, autoscaling, or a latency SLO
  must be proven. Profiling a single slow request routes to performance-profiler.
metadata:
  version: 1.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: performance-engineer
---

# Load Testing

A load test is an experiment. It needs a question, a hypothesis, a controlled input, and a
decision rule written before the run. Without those it produces a graph that nobody can act on.

## WHEN TO USE

- Someone claims a capacity number ("we handle 5k rps") and no one has measured it.
- Before a launch, migration, or pricing change that increases traffic.
- Validating autoscaling, connection pooling, or a new cache under real concurrency.
- Deciding the minimum instance count, pool size, or rate limit.
- A soak test is needed to find a leak that only appears after hours.

## WHEN NOT TO USE

- One endpoint is slow for one request. That is profiling: `performance-profiler`.
- The bottleneck is already known to be a SQL query: `query-performance-engineer`.
- The system has no SLO and no target. Define the target first; otherwise there is nothing to fail against.
- You need to prove correctness under concurrency, not throughput: `concurrency-engineer`.

## DECISION TREE

```text
What question are you answering?
├─ "does it work at all under traffic?" ........... smoke: 1-2 users, every critical path, 1-5 min
├─ "does it meet the SLO at expected load?" ....... load: expected peak arrival rate, 30-60 min
├─ "where does it break?" ......................... stress: ramp until error rate or latency SLO breaks
├─ "what is the maximum?" ......................... breakpoint: fine-grained ramp, record the knee
├─ "does it leak or degrade over time?" ........... soak: 70% load for 4-24 h, watch RSS and pools
└─ "does it survive a spike?" ..................... spike: 0 → 5x in under a minute, watch recovery

Then choose the workload model:
├─ requests originate outside the system (users) .. OPEN model: fixed arrival rate, VUs grow
└─ concurrent users each wait for a response ....... CLOSED model: fixed VUs, rate falls as latency rises
```

### The mistake that invalidates most load tests

A closed model applied to an open-model question. If you hold VUs constant and latency rises, the
offered rate **falls** — the system looks stable while it is actually shedding load. For "can we
handle 5k rps", the arrival rate must be fixed, not the user count.

| Question | Model | Tool setting |
|---|---|---|
| Can we absorb a traffic spike? | open | constant arrival rate / rps target |
| Do 500 concurrent users feel fast? | closed | fixed VUs with think time |
| Where is the throughput knee? | open, ramped | arrival rate staircase |
| Does the connection pool exhaust? | either, with realistic concurrency | VUs above pool size |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Closed model for an open question | Rate collapses as latency rises; failure hidden | Fix arrival rate; assert achieved rps |
| Empty or tiny dataset | Every query hits cache or an index of 100 rows | Production-shaped volume and cardinality |
| Single generator | The load generator saturates first | ≥2 generators, or confirm generator headroom |
| Mean latency reported | A 4s p99 hides behind a 40ms mean | Report p50/p95/p99 and error rate together |
| No saturation data | Know it broke, not why | Collect CPU, queue depth, pool in-use, GC, IO wait |
| Cached run | Second run looks 10x faster | Flush caches or report warm vs cold explicitly |
| Ignoring downstream | API holds up, database or third party melts | Load every tier; watch dependency error rates |
| No stop condition | Test hammers production for an hour after failure | Hard abort on error rate > 1% or p99 > 3x SLO |
| Testing against prod | Real user impact, unclean data | Staging with production-shaped data, or a canary slice |

## QUANTITATIVE RULES

- **Write the pass criterion first.** "p95 < 300 ms and error rate < 0.1% at 2,000 rps for 30 minutes."
- **Warm up for 10% of the run** and exclude it from the report.
- **Report p50, p95, p99, error rate, achieved rps, and saturation** — never a single number.
- **Ramp, do not step.** Unless the test *is* the spike, ramp over 2-5 minutes.
- **Soak ≥ 4 hours** (24 for leak hunting) at 70% of the target rate.
- **At least 3 runs** per configuration; a single run is an anecdote.
- **Generator headroom ≥ 2x** the target rate, verified by a no-op endpoint run.

## VERIFICATION GATE

- [ ] The question is one sentence, and the pass criterion is numeric and written down.
- [ ] Workload model matches the question (open for rate, closed for concurrency).
- [ ] Dataset volume and cardinality match production within an order of magnitude.
- [ ] Achieved arrival rate is asserted, not assumed, and within 5% of target.
- [ ] Percentiles, error rate, and saturation series are captured and attached.
- [ ] Stop conditions are configured and one was tested.
- [ ] The report states the environment, the data shape, and what was not measured.

## REFERENCES

- `performance-profiler` for finding the bottleneck once the test shows one.
- `query-performance-engineer` for database-level saturation.
- `resilience-pattern-engineer` for what should happen at the limit: timeouts, shedding, backoff.
- `observability-sre` for the SLO the test is decided against.
- `system-design-architect` for translating a measured knee into capacity and instance counts.
