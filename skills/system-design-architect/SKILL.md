---
name: system-design-architect
description: >-
  Shapes systems and does the capacity math: component selection, boundaries, data flow,
  caching, load balancing, and back-of-envelope sizing that justifies the design. Use when
  choosing an architecture or defending one at scale. Consistency and replication behavior
  routes to distributed-systems-engineer; database topology to database-at-scale; the
  decision record to adr-engineering.
metadata:
  version: 3.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: solution-architect
---

# SYSTEM DESIGN ARCHITECT

Design systems that survive real traffic: capacity math before component choice, trade-offs written down as ADRs, and failure modes engineered in from the first draft. Architecture is the discipline of making irreversible decisions reversible.

## WHEN TO USE

- You are choosing between components, protocols, or topologies that will be expensive or costly to change later (storage engine, cache tier, sharding key, message broker vs direct DB).
- The design must hold under specific, quantified load — you can state a target in requests-per-second (RPS), users, writes/day, or payload size and need to prove the shape can absorb it.
- A capacity, latency, cost, or consistency trade-off exists that a developer cannot resolve by themselves and that should be recorded for the whole team.
- You must communicate a design to peers, reviewers, or an operations team; a structured Architecture Decision Record (ADR) is the deliverable, not prose opinions.
- Requirements mix functional flow with non-functional constraints (availability, cost ceiling, compliance retention) and need a single coherent blueprint that balances them.

## WHEN NOT TO USE

- **Single-file or low-volume app** — a local process, single instance, or an internal module with tens of QPS needs no shard key, no cache tier, and no ADR; an over-architected design costs more than it saves.
- **Component already selected and locked** — if the storage engine, language, and deployment are fixed and not changeable, do not re-derive a full architecture; solve only the remaining narrow decision.
- **Exploratory prototype** — during throwaway validation the goal is speed of learning; formal ADRs, capacity plans, and redundancy layers slow that down.
- **The decision is purely local** — a method-local algorithm or an in-process structure with no cross-team, cross-host, or lifetime impact needs no architecture artifact.
- **One-off batch or script** — a single run that does not repeat at scale and produces a fixed report needs capacity math only if it exceeds the machine budget.
- **A clearly better, already-standard default exists** — avoid introducing distributed complexity when a single host with a cache already meets the stated numbers.

## DECISION TREE

```text
START
 1. REQUIREMENTS — write them down with numbers.
    a. Functional: what read and write operations, entities, and data flow?
    b. Non-functional: target RPS, latency SLO, availability (nines), write/read ratio,
       data growth, retention period, budget ceiling, compliance constraints.
    If any number is unknown, derive it from a volume assumption and state it as such.
    If no number can be justified at all, revisit WHEN NOT TO USE (you may not need this).
 2. CAPACITY ESTIMATION — quantify the load in units you can multiply.
       peak_RPS, avg_bytes_per_read/write, total_write_bytes/day, storage (GB/TB),
       required throughput (bandwidth), and expected growth over a 3-year horizon.
       Run every estimate twice linearly per QUANTITATIVE RULES and cross-check.
 3. COMPONENT SELECTION —
       storage engine: relational vs columnar vs document vs blob vs search?
       serving tier: request-response vs queue vs stream vs cache-first?
       data access: read-model vs write-model, and what cache tiers in front.
       Pick the smallest component set that is proven to handle the estimated
       numbers, no more (YAGNI) and no less (no missed SPOF).
 4. TRADE-OFF DOCUMENTATION (ADR) — for each irreversible decision write
       context, decision, consequences, alternatives (see PATTERNS).
 5. REVIEW — walk the design through the VERIFICATION GATE: re-derive the
       capacity math, confirm no SPOF or scale cliff, and get the ADR
       reviewed by an adversarial reviewer before approval.
```
Never skip from Step 1 directly to a diagram: every architectural choice must be traceable to a stated requirement number.

## PATTERNS

### ADR format (context, decision, consequences, alternatives)
Record every irreversible choice. Structure:
- Context: the forcing pressures (numbers, deadlines, budget, constraints) that make a decision necessary.
- Decision: the concrete option chosen, precisely and decisively (one sentence, no "it depends").
- Consequences: the positive and negative effects that follow, including what you accept giving up.
- Alternatives: options considered and why each was rejected, with the evidence that ruled them out.

Before writing a new ADR, check that the choice is actually required and there is a requirement to justify rearchitecting.

### Trade-off framework (CAP, consistency vs latency vs cost)
Fundamental tension triangles:
- CAP: partition tolerance is mandatory; between consistency and availability you choose a point; you cannot get both staleness and partition-free behavior.
- Consistency vs latency: stronger consistency costs cross-node coordination latency; eventual consistency gives liveness at the cost of read staleness.
- Consistency vs cost: replicas, quorums, and write-ahead logs each carry licensing plus storage cost; cap the cost ceiling before you commit to a consistency level.
- State the target explicitly for each triangle: a latency SLO number, an availability target, and a hard cost ceiling — then pick the smallest configuration satisfying all three.

Method: for each pair, write the target value explicitly (e.g. "reads tolerate up to 10s staleness" or "p95 write latency must exceed X"), and reject a choice without one.

### Caching tiers
- Cache the hot set, not everything. Rule of thumb: roughly 80% of read traffic targets a small hot subset — size the cache to that subset.
- Cache hierarchy: L1 in-memory (per-instance, smallest and fastest), L2 distributed shared (Redis/memcached), then the source of truth. Integrity requires a consistent invalidation path, not only TTL.
- Never cache mutable state where staleness is visible to users without a defined TTL and a defined SLO on that staleness. Choose the tier from the read:write ratio — a write-heavy dataset may not be cacheable at all.

### Queue-based load leveling
- Buffer bursty writes and calls with a queue and a decoupling that lets producers run faster than consumers tolerate the burst.
- Decouples producer rate from consumer throughput: consumers process at a sustainable pace, the queue absorbs spikes instead of the database.
- Back the queue with a durable store for at-least-once semantics; process idempotently on the consumer side so replay is safe.
- Set an alert on queue depth and a dead-letter queue for poison messages; a never-drained queue is a zombie path with a hidden cost.

### Sharding (data partitioning)
- Choose a genuinely high-cardinality, evenly distributed key (a user_id usually beats a country for split) so no one shard becomes hot.
- Partition on a key that collocates the queries you emit; a query touching many shards is expensive and should be routed or re-modeled.
- Decide the number of shards for the 10-year growth you estimated in Step 2 — adding shards later is a painful live resharding.
- Allocate a shard_count and a shard_selector (hash mod a fixed number) explicitly, and document the rebalance cost in the ADR.

## FAILURE MODES & MITIGATIONS

- **Over-design (YAGNI)** — a bespoke microservice topology, sharded store, and cache grid for a system that would run fine on one host.
  DETECT: the components exceed what the capacity math in Step 2 can justify; no number in any non-functional row requires the extra layer.
  FIX: shrink to the minimal set that satisfies the stated numbers; keep the extra design recorded as an ADR alternative for when growth arrives.
- **Capacity estimates without traffic math** — a raw number (e.g. "10k users", "1M posts") used with no QPS, byte size, or per-day write calculation.
  DETECT: a requirement row that has no derived peak_RPS or storage bytes; the number does not come from a stated formula.
  FIX: express each requirement as an arithmetic expression and run the 3-quantity check (see VERIFICATION GATE) before settling on instances or storage.
- **Single points of failure missed** — one DB, one cache node, or one message in front of all writes; a crash takes the whole system down.
  DETECT: any component in the flow diagram with no replicated or redundant peer; the availability number (4 nines) is not backed by any second copy of it crossing paths.
  FIX: enumerate every component, mark reachable failure to availability, and add at least a standby/partition availability match to the requirement.
- **Ignoring non-functional constraints (cost, compliance)** — a design meets RPS and latency but blows the budget or stores data it must not keep.
  DETECT: cost grows unbounded with no ceiling number, or data-location/retention terms are not reflected in where and how data is stored and accessed.
  FIX: derive a cost model from the capacity math (instances × per-node price), enforce a hard ceiling, and map retention and location requirements to concrete transformers (encrypt, archive, shrink) in the ADR.
- **Design without failure modes** — the happy path is fully drawn; the outage, latency spike, and poison message are not considered.
  DETECT: every box has a single inbound arrow and no error branch; no partial-failure or degraded-operation paths exist in the diagram.
  FIX: for each component list the plausible degradations (timeout, crash, overflow, invalid input) and a mitigation for each in the ADR.
- **Wrong estimate for the actually-read direction** — storage sized by total writes but reads hit the same rows constantly, turning storage math into no read capacity.
  DETECT: read QPS exceed write QPS yet sizing only counted writes; cache hit assumptions are unstated.
  FIX: model read:write ratio and cache tier capacity from the hot subset before sizing persistent storage.
- **Cache without invalidation** — a fast cache tier is added but never evicts or invalidates, so it serves stale data forever.
  DETECT: no TTL, no version key, no mutation path that updates or invalidates the cache on write; a read and a write on the same entity disagree.
  FIX: a key eviction policy and a defined staleness bound per data type; treat hard-guarantee needs in the ADR.
- **Unbounded or poison backlog** — a queue with no depth guard or dead-letter grows until memory and store exhaust.
  DETECT: queue length has no alert, no cap, and no poison movement; a bad item blocks the whole consumer pipeline.
  FIX: bounded queue, dead-letter topic, alert on depth and aging, idempotent consumers.

## QUANTITATIVE RULES

### Numbers every engineer should know (rough order of magnitude)
| Operation | Latency (approximate) |
|---|---|
| L1/L2 cache reference | ~1 ns |
| Main memory reference | ~100 ns |
| Read 1 MB sequentially from memory | ~0.25 ms |
| Fast network round trip within a data center | ~0.5 ms |
| SSD random read | ~0.1-0.3 ms |
| Read 1 MB sequentially from SSD | ~0.3 ms |
| HDD seek | a few ms |
| Read 1 MB sequentially from HDD | ~5-10 ms |
| Network send/recv of a small metric | ~0.1-1 ms |
| DNS lookup | ~10-100 ms |

### Sustained throughput (requests/second) per server type
| Server type | Approx sustained RPS |
|---|---|
| Single-core CPU-bound numeric loop | 100k-1M ops |
| Typical stateless web/API instance | 1k-10k RPS small payloads |
| App + relational DB single write path | hundreds to a few thousand |
| Cached reads (Redis/memcached) | 10k-100k reads/s |
| Kafka / message broker (durable) | 100k+ messages/s (write-ahead) |

### Storage math (derive, do not guess)
- 1,000,000 users x 1 KB per user row = 1 GB logical rows
- Each user writing 10 records/day of 1 KB = 10 MB/day ingest
- 1M users × 10 writes/day × 1 KB = 10 GB / day added to the store
- Yearly growth = 10 GB/day × 365 ≈ 3.65 TB/year for that entity alone
- Always add a multiplier for indexes, metadata, write-ahead logs, and replication copies (rule of thumb: plan for 1.5-2x the logical bytes); state the multiplier you used.

### QPS -> instances formula
```
required_instances = ceil( peak_RPS × (1 + headroom) / single_instance_RPS )
```
Always round a fractional instance count up, and add one standby instance per tier to keep the availability target during a node loss.
Example: single mid-tier instance handles 5,000 RPS. Peak is 20,000 RPS with 20% headroom:
20k × 1.2 / 5k = 4.8 → 5 instances, plus 1 standby for failover = 6.

### Worked example (end-to-end)
Goal: 2M users, each reads their home feed ~10x/day and writes comments ~5/day; 1 KB per object; SLO p95 < 250 ms.
Traffic: reads = 2M × 10/day / 86,400 s ≈ 231 read RPS; writes = 2M × 5/day ≈ 116 write RPS; peak burst factor 5x ≈ 1.2k reads/s.
Storage: 2M × 5 writes × 1 KB = 10 GB/day ≈ 3.65 TB/year before indexes/replication.
Instances: reads at ~1.2k RPS peak → ceil(1200 × 1.2 / 5000) = 1 stateless instance + 1 standby; writes go to a single primary with read replicas; a Redis cache tier absorbs the hot subset and keeps p95 under the SLO.
Result: a two-instance stateless tier, one primary DB with replicas, one cache — and every one of these numbers is stated and re-derivable in the ADR.

### Availability (nines -> downtime)
| Availability | Downtime per year | Downtime per month |
|---|---|---|
| 99% | ~3.65 days | ~7.30 h |
| 99.9% | ~8.76 h | ~43.8 min |
| 99.95% | ~4.38 h | ~21.9 min |
| 99.99% | ~52.6 min | ~4.4 min |
| 99.999% | ~5.26 min | ~26 s |

Cost scales with each extra nine: every redundant replica and automated failover must be budgeted, and the price of each nine is rarely worth it below a real SLO-backed customer need.
### Growth modeling
Always size for the volume at the 3-year mark, not today. If traffic doubles yearly, a current load of X becomes roughly X, X×2, X×4 at years 1-3; components picked for today's number will fail before the design matures.
### Bandwidth math
```
bytes_per_second = peak_RPS × avg_response_bytes
Gb/s = bytes_per_second × 8 / 1e9
```
Example: 5,000 RPS × 4 KB = 20 MB/s → 160 Mb/s. A single Gbps NIC budget is 1,000 Mb/s, so that fits comfortably; but aggregation across N backend hosts multiples the requirement — total bandwidth = per-host flow. Sum over all backends and compare that sum to the switch fabric's aggregate capacity, not just one NIC.

## VERIFICATION GATE

- **Capacity-math cross-check**: re-run every estimate from the QUANTITATIVE RULES table in a different order and reconfirm equals the original; confirm instances, storage, and bandwidth all derive from the same traffic numbers (peak_RPS, writes/day, avg_bytes).
- **Design review checklist** — confirm all four, or the review fails:
  - SPOF: every component has redundancy (or documented single-point decision) that matches the stated availability target.
  - Scaling: the design scales to the 10-year number without a re-architecture step; adding a shard or cache does not become the blocker.
  - Failure modes: every box has a degraded path and a mitigation written in the ADR.
  - Cost: the computed instance/store/bandwidth arithmetic is within the stated ceiling; retention and replication growth are priced.
- **ADR review by an adversarial reviewer**: a red-team reviewer hammers the ADRs for evidence, capacity numbers, missed SPOF, and unstated revocation/trade-offs either in consequence or a removed alternative. If any consequence is asserted without a number, revert to Step 1.
- Record: the decision tree steps, the arithmetic, the chosen components, the ADR, and the review disposition (pass/fail) as the deliverable.

## REFERENCES

- Martin Kleppmann — *Designing Data-Intensive Applications* (DDIA): data models, replication, partitions, consistency, and vault of failure mode detail.
- System Design Interview and its popular "Numbers every system design should know" companion posts and frameworks for capacity.
- Jeff Dean — "Numbers every programmer should know", 2010 — latency figure; translate to HDD-rounded where needed.
- AWS Well-Architected Framework (pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) — trade-off guidance and cost review.