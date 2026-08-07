# system-design-architect — Flagship Eval

## 1. Trigger test

FIRE (5):
1. "Design the full architecture for a social feed at 200k reads/s and 10k writes/s, cost-constrained."
2. "Estimate capacity and sharding for a storage service that must hold 20TB in 3 years."
3. "Choose a storage engine + cache tier + message broker for a new product with a stated RPS load."
4. "We are picking the SLOs and ADR-driven architecture decisions for a new service — draft the trade-offs."
5. "Size the compute and storage for an ingestion pipeline at a bounded 3-year growth projection."

NOT FIRE (3):
6. "Add shard key / cache-tier and ADRs to a single-file script that runs at 10 QPS locally."
7. "Refactor one method's local algorithm in-process with no cross-host impact."
8. "Write a query-performance-tune one index on a small table."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5 — requirements, capacity, component selection, ADR, redundant SPOF/review all walkable in order.
(b) failure modes have detection + mitigation: 5 — over-design, capacity-without-math, missed SPOF, cost/compliance, cache/no-invalidation, poison backlog all DETECT→FIX.
(c) quantitative rules are numbers: 5 — numbers-you-should-know tables, QPS→instances formula with worked 6-instance example, bandwidth math.
(d) verification gate executable: 5 — capacity re-derive, SPOF/scale/cost checklist, ADR adversarial review.
(e) references authoritative: 4 — DDIA + Jeff Dean + AWS WAF all authoritative; "System Design Interview" is less authoritative than the others.
(f) no contradictions: 4 — consistent with adr-engineering and systems-core; scale/sharing rules align with database-at-scale though overlap is real.

## 3. Reference task
Design a system for 2M users reading feeds 10x/day and writing 5 comments/day, P95 < 250ms, under a hard cost ceiling and must be resilient answerable across node loss. The skill should return: requirement numbers, capacity math, smallest surviving component set (web tier + primary DB + replicas + cache), a sharding plan sizing for 10-year growth, and an ADR record.
