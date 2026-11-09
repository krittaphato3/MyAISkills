---
name: cloud-cost-optimization
description: >-
  Reduces cloud spend with evidence: unit economics and showback, idle and orphaned resource
  hunts, rightsizing, storage lifecycle and egress, commitment discounts, and architectural
  changes that cut cost per request without breaching an SLO. Use when a bill spikes, a cost
  review is due, or someone asks what a feature costs to run. Pricing negotiation, vendor
  selection, and database query tuning route elsewhere.
metadata:
  version: 1.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: devops-engineer
---

# Cloud Cost Optimization

A bill is a symptom. The unit is **cost per unit of value** — per request, per tenant, per
thousand events, per GB stored. A total that doubles while volume doubles is not a problem. A
total that doubles at flat volume is.

## WHEN TO USE

- The bill jumped and nobody knows which change caused it.
- Before a launch, to state what the feature costs to run at expected volume.
- A cost review, a budget cut, or a FinOps ask.
- Choosing between instance types, storage classes, or managed vs self-hosted.
- Designing showback or chargeback per team or tenant.

## WHEN NOT TO USE

- The workload is genuinely growing and cost tracks volume. Optimize unit economics, not the total.
- The problem is a slow query that also happens to cost money. `query-performance-engineer` first.
- The problem is an oversized container image or slow build. `container-optimizer`.
- The decision is a vendor contract. That is procurement, not engineering.

## DECISION TREE

```text
Why is the bill high?
├─ unknown attribution ............................. tag every resource first; without it you are guessing
├─ idle or orphaned resources ...................... find before you optimize:
│  ├─ unattached volumes, old snapshots, idle LBs .. delete (largest, cheapest win)
│  ├─ non-prod running 24/7 ....................... schedule down; often 30-40% of non-prod spend
│  └─ forgotten instances in other regions ......... inventory by region, not just the default
├─ compute overprovisioned ......................... rightsize on p95 CPU + memory, not peak
│  ├─ steady, predictable ......................... committed use / savings plan after 30 days of data
│  └─ bursty or fault-tolerant .................... spot / preemptible with graceful drain
├─ storage growing ................................. lifecycle policy: hot → warm → cold → delete
├─ egress high ..................................... cache at the edge, co-locate, compress, avoid cross-AZ chatter
├─ cost per request rising ......................... look for N+1 calls, chatty services, retries, idle polling
└─ architecture ................................... batch, queue, cache, or move work off the request path
```

### Levers, in order of effort-to-savings

| Lever | Typical saving | Risk |
|---|---|---|
| Delete idle and orphaned resources | 10-30% | none if truly unused — verify with metrics first |
| Schedule non-production down | 5-15% of total | developer friction; announce the window |
| Storage lifecycle and snapshot retention | 5-20% of storage | restore latency, compliance minimums |
| Rightsizing | 10-25% of compute | p95 regression; change one dimension at a time |
| Commitment discounts | 20-40% of covered compute | lock-in; only after usage is stable for 30 days |
| Architecture (cache, batch, spot, edge) | unbounded | correctness and reliability risk |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Savings without baseline | "We cut 40%" with no before number | Record the baseline and the load it was measured at |
| Reliability sold for cost | Rightsized on peak, p95 doubles | Size on p95 of production traffic, canary the change |
| Optimizing the small lines | Weeks spent on 2% of spend | Sort cost by service first; fix the top three |
| Untagged spend | No owner, no allocation | Tag policy enforced at creation, not in review |
| Zombie autoscaling | Min replicas set high "for safety" | Set min to the observed floor; alert on sustained max |
| Commitment before stability | Reserved instances for a workload being rewritten | 30 days of stable usage before committing |
| Egress blindness | Cross-AZ and NAT traffic unbilled in the model | Include data transfer in every architecture estimate |

## QUANTITATIVE RULES

- **Attribute before optimizing.** No action on a resource without a tag or an owner.
- **Top three services first.** Spend is almost always Pareto; the tail is not worth a sprint.
- **p95, not peak, for rightsizing.** Peak is a burst; size the baseline and let autoscaling absorb bursts.
- **One variable per change**, then measure for a full business cycle (7 days minimum).
- **State cost per request** in the design doc for any new service.
- **30 days of stable usage** before any commitment purchase.

## VERIFICATION GATE

- [ ] Baseline cost, period, and load captured before the change.
- [ ] Delta measured over a comparable period, with the load held constant or normalized.
- [ ] No SLO regression: p95 latency and error rate unchanged or better.
- [ ] Every changed resource is tagged and has an owner.
- [ ] Savings are stated as a monthly figure and a unit-economics figure.
- [ ] Rollback path exists for anything architectural.

## REFERENCES

- `system-design-architect` for capacity math and the cost pillar in trade-off analysis.
- `observability-sre` for the metrics that prove no SLO regression.
- `performance-profiler` when the cost is CPU or memory you can measure away.
- `query-performance-engineer` when the cost is database work.
- `container-optimizer` for image size and build cost.
