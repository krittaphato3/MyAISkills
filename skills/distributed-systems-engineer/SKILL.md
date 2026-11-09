---
name: distributed-systems-engineer
description: >-
  Decides distributed-systems behavior: consistency models, consensus, replication,
  partitioning, distributed transactions, idempotency, and their failure modes. Use when
  correctness across nodes, partitions, or regions is the question. Component and capacity
  shape routes to system-design-architect; database topology to database-at-scale.
metadata:
  version: 3.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  authored-by: solution-architect
---

# distributed-systems-engineer

World-class reference for designing and operating distributed systems. Covers consistency-model selection, replication topologies, partitioning, distributed transactions, distributed-locking and outbox patterns, quantitative design rules, and a fault-injection verification gate that must pass before "done" is claimed. Numbers, not adjectives; every rule is actionable and measurable.

## WHEN TO USE

Use this skill when the work spans more than one machine coordinating shared state, and at least one of these holds:

- You must choose a consistency model, replication topology, or partitioning strategy for a service or database, and a fresh subagent must inherit and safely extend the choice.
- You must decide how writes replicate across nodes (single-leader vs multi-leader vs quorum) and what a client may observe immediately after a write returns.
- You are selecting a distributed-transaction mechanism (2PC vs Saga vs outbox) and need the availability, atomicity, and throughput trade-offs spelled out.
- You are defending against partial failure: leader loss, network partition, clock skew, message replay, or out-of-order arrival.
- The product needs an availability or latency SLO that a single node cannot meet, or an existing cluster is being resized or re-partitioned.
- You are designing or reviewing idempotency, outbox, distributed-locking with leases and fencing, quorum, or gossip-membership behavior.
- You must reason about why a distributed system passed the test environment but misbehaved under a real partition, clock skew, or slow follower.

Self-assign this skill before choosing W+R values, adding quorum reads, introducing consensus, adopting an outbox, or sizing a replication factor.

## WHEN NOT TO USE

- Single-node systems with no replication, partition, or crash-recovery story.
- Web/API routing where the underlying store (database, broker, managed service) already provides the needed consistency; do not re-implement replication you do not own.
- Purely batched or embarrassingly parallel workloads that tolerate eventual consistency and hold no cross-partition invariants.
- Deciding a guarantee that lives elsewhere and is not yours to configure, for example a vendor-managed store with a fixed topology.
- Thin CRUD over a maintained database where there is no genuinely distributed decision to make.
- Prototypes with no real scale, failover, or partition requirement; adding consensus machinery prematurely is itself a failure mode.
- Anything where a single abstraction can give you the guarantee with less machinery, for example ordering through one message queue instead of a replicated log.

## DECISION TREE

Walk each branch in order; every later fork uses the earlier answers. Record the decision and what it sacrifices in the design record.

### Consistency model — by requirement

1. A single total order of all operations that matches real-time occurrence — **linearizable**. Pick this when reading stale data, or accepting that two clients observe different orders of the same writes, is unacceptable. Applies to financial ledgers, seat inventory, distributed locks, and unique-constraint tokens.
2. A total order exists but only across operations that are causally related — **causal consistency**. Suits chat, feeds, and per-key read-your-writes where no cross-object ordering is asserted.
3. You need atomic multi-record transactions but not full linearizable visibility for every read — **serializable** at the transaction granularity.
4. Read-your-writes and/or monotonic reads within a session, no global order — **session consistency**. Good default for a user's own timeline where "my write shows up" is the contract.
5. No cross-object invariant and merges allowed — **eventual consistency** with an explicit conflict-resolution strategy (last-writer-wins, versioned, or application merge) chosen before deployment.

Choose the **weakest** model your invariants require. Every model above eventual costs availability and latency; confirm against real traffic, not estimates.

Quick summary of the four required models — what it guarantees, what it costs, and a default yes/no:

| Model | Guarantees | Costs | Use it when |
|---|---|---|---|
| Linearizable | single real-time total order | availability on partition; latency of quorum | money, seats, locks, unique tokens |
| Serializable | total order of transactions | isolation machinery; no cross-txn real-time order | multi-record atomic txns |
| Causal | order among causally related ops | per-session state; no global order | chat, feeds, per-key RYW |
| Eventual | converges; no order | explicit conflict resolution | any high-avail, mergeable data |

If in doubt between two adjacent models, pick the weaker one and validate with the VERIFICATION GATE before hardening.

### Replication topology

- **Single-leader:** one node accepts all writes; replicas serve reads. Default choice: strongest ordering and read-your-writes (route the session to the leader). Write throughput is bounded by the leader; add a failover replica, not a write shard.
- **Multi-leader:** any of several nodes accepts writes; conflicts merge at read or application time. Use only for cross-region or cross-vendor writes where a single global leader is geographically untenable. Requires a conflict-resolution rule and accepts per-key divergence.
- **Quorum / leaderless:** writes go to W nodes, reads to R, with W+R > N; any node can serve; versions resolve at read time. Default for read-heavy, write-always-available systems that accept per-key conflicts. Highest concurrent-read throughput, weakest ordering.

### Partitioning

- **Hash by key:** spreads data across nodes with low skew; good for point lookups. **Range:** supports range scans but risks hot keys and skew. Choose by the real query workload, not by preference.
- **Rebalancing:** never copy whole slots live. Use consistent hashing or dynamic partition split and merge driven by a coordinator that double-writes during the transition. Trigger rebalance on a load threshold and cap concurrent migration so the cluster does not saturate while rebalancing.

### Distributed transactions

- **Take 2PC** where atomicity across nodes is a hard requirement, the participant count is small, and participants are reachable; it holds locks and is availability-weak when the coordinator fails mid-protocol. Keep the window and the participant count small.
- **Take a Saga** for long business flows that span services where a rollback cannot be atomic but can be compensated; each step is a local transaction and failure triggers the compensating step.
- **Take an outbox** to publish an event exactly-once from a local transaction without a coordinator; external consumers then deduplicate. Use it where 2PC is overkill or brittle.

### Worked example — a three-region inventory service

Service: item stock, written by regional stock teams, read by a checkout frontend, cross-region replication, 250 ms P95 budget per checkout.

1. Consistency: stock must not oversell, and a checkout must see the current count in its own region. A checkout that accepts a read-your-writes contract is enough; a global linearizable read of every key is not required. Choose session/serializable for the per-key write, not global linearizability.
2. Replication: a multi-leader model with one leader per region. Writes land in the local region, quorum-gated there; cross-region apply is async. A write acknowledged locally is durable in that region before it returns to the client.
3. Partitioning: hash by SKU so the hot-purchase keys spread; range is not needed (no scans). Rebalance by consistent hashing, triggered when a region node crosses the load threshold.
4. Transaction: reservation is a single-key compare-and-set or an outbox-plus-read path rather than a 2PC; the cross-region case uses an outbox followed by async apply and consumer idempotency. No 2PC across regions.

Check the result against the budget: local quorum RTT plus a reservation write must fit inside the 3 ms region budget, leaving 250+ ms of headroom for the checkout funnel. The latency budget in QUANTITATIVE RULES decides whether this is feasible.

### Record every decision

For each branch, write down in the design record: the choice, the rejected alternatives, and the concrete failure mode you are trading away (e.g., "chose quorum read over leader read; accepts a stale read of one key during a partition"). This record is what the VERIFICATION GATE and an incident postmortem later check against. A decision you cannot state as a trade-off is not yet a decision.

## PATTERNS

Each pattern states the guard you must not omit.

Full detail: `references/patterns.md`.

## FAILURE MODES & MITIGATIONS

Each entry lists *detection* first, then *fix*. Validate at least the following 8 before claiming a distributed system is correct.

Full detail: `references/failure-modes-mitigations.md`.

## QUANTITATIVE RULES

Numbers are budgets, not absolutes; take them into a measurement harness on the real cluster before committing.

Full detail: `references/quantitative-rules.md`.

## VERIFICATION GATE

Nothing below is optional. A distributed design is "done" only when the relevant checks are green against the numbers above.

**Fault-injection matrix (run once per release; each row is simulated then asserted):**

- **Kill leader:** kill the primary process mid-write. Assert: a new leader is selected within the election budget, writes resume, there is no split brain, and fencing rejects a stale old-leader writer.
- **Partition:** isolate one side of the cluster. Assert: the minority side does not serve writes, the majority continues, and on heal no acknowledged write is lost and no duplicate is applied.
- **Pause a node's clock:** free the node's clock for the fence. Assert: fencing still rejects writes from a node whose lease has expired, and HLC ordering still orders events correctly.
- **Drop a replica's sync:** force long per-replica lag. Assert: missing writes do not metastasize, read-your-writes holds within the SLO, and a lagging replica cannot become leader and clobber the log.

**Jepsen-style linearizability checks where feasible.** Run a linearizability checker, such as the Knossos or Jepsen checker, against a recorded history of the write path. If the system claims linearizability only in a model, do not claim it in production; state and verify the true strength with causal, serializable, or read-your-writes tests as appropriate.

**Chaos tests.** Automate the matrix (kill, partition, pause) in a loop while a load generator writes. After each iteration, assert: no lost acknowledged write, idempotent replay (at-least-once delivery never applies an action twice), fencing consistent across failures, no split brain, and eventual convergence.

**Degraded-load test.** Run at partial capacity, for example 50%, sustained for 30 minutes or more with a few nodes down. Verify backpressure, circuit breaker, and quorum thresholds hold; fail if P90 latency exceeds about 2x its budget or if an out-of-order or duplicate side effect appears.

**Concrete tooling to run the matrix:**

- kill a leader: `kill -9 <leader-pid>` or the orchestrator's force-fail; watch election time.
- partition a node: `iptables -A OUTPUT -p tcp -d <peer> -j DROP` (note: rules with a target like tc use the tc netem command for packet loss/latency emulation, and ntpdate tooling to freeze a clock).
- pause a clock: disable NTP or use a debug pause-clock hook on the node; verify HLC ordering holds.
- inject DB lag: `ALTER <replica> ...` to stall a replica or add a sleep in the apply path.
- drive load: a write/read generator asserting the invariants (no lost ack, no duplicate, fencing check) while each fault runs.

**Operational runbook — on a real incident, answer in this order:**

1. Is there a partition or leader loss? Check heartbeats, epochs, and quorum membership first.
2. Is that a fencing breach or a stale primary? Compare fencing tokens on the storage before trusting any write from a candidate leader.
3. Is it read-your-writes lag or a lost update? Reproduce with a write-then-read in the same session; check compare-and-set.
4. Is there a thundering herd or cascade in flight? Look at retry rate and backoff; drop backoff/jitter in before any code change.

**Done criteria:**

- Fault-injection matrix rows pass with assertions tied to a specific quantitative rule (quorum, lag SLO, fencing, retry).
- If the design claims linearizable or serializable, a linearizability or causal-checker history passes; otherwise document the degraded model actually verified.
- Retry budget and quorum constants are explicit in config and match the tested node count and latency budget.
- No placeholder or TODO markers remain.

## REFERENCES

- **Kleppmann, M.** *Designing Data-Intensive Applications* (O'Reilly). Chapters on replication, partitioning, transactions, consistency, and consensus: the authoritative practical reference for model and topology selection.
- **Ongaro, D.; Ousterhout, J.** *In Search of an Understandable Consensus Algorithm (Raft)*, 2014. Leader election, log replication, fencing, and the epoch idea that this skill builds on.
- **Jepsen analyses by Kyle Kingsbury (aphyr)** and the **Knossos** checker: the tools to prove or refute a linearizability claim and to calibrate what fault-injection testing teaches.
- **Google Spanner and TrueTime papers:** Spanner, Google's Globally-Distributed Database (2012/2017), and TrueTime, showing how a real system reconciles strict atomic commitment with loosely synchronized clocks.

Primary external references for this skill in training corpus: the referenced DDIA chapters and the Raft paper are the load-bearing sources; the Jepsen analyses and Spanner papers are the validation-and-trade-off sources referenced throughout the QUANTITATIVE RULES and VERIFICATION GATE sections.

## CHANGELOG

- 2026-08-06 | Phase 3.1: distributed-systems-engineer created (G3: consistency, replication, partitions, consensus, failure modes, quantitative rules) | distributed-systems-engineer