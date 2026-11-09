---
name: database-at-scale
description: >-
  Chooses and operates database topology beyond one node: replication, sharding,
  partitioning, zero-downtime migrations, pool sizing, and rebalance or DR cadence. Use
  when scale-out, failover, or a risky migration is the question. A single slow query
  routes to query-performance-engineer first; schema shape routes to db-architect.
metadata:
  version: 3.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  authored-by: db-architect
---

# database-at-scale

World-class reference for taking a database from one node to many without losing correctness or availability. Covers the scale ladder (scale-up vs replicas vs shard vs managed), shard-key selection, replication topology and isolation by workload, zero-downtime migration (expand/contract, dual-write, backfill), connection math, quantitative shard and batch-size limits, and a verification gate that must pass before production cutover. All rules are concrete budgets and formulas, not adjectives.

The decision was made to write each rule as a number you can measure. Treat a value such as "47 rows per second per worker" as a starting budget to calibrate on the real cluster, never as a guarantee before you run the VERIFICATION GATE.

## WHEN TO USE

- The data, query, or write rates exceed what one node can serve within the latency or availability SLO, and a fresh subagent must inherit and safely extend the scaling plan.
- You must choose between scale-up, read replicas, a sharded cluster, and moving to a managed database, and want the trade-offs and triggering thresholds stated, not guessed.
- You are adding replication and must decide topology (sync vs async, quorum) and how a client sees its own write immediately after the write returns.
- You must run a large schema or data migration without a maintenance window, and need the expand/contract, dual-write, and backfill-with-verify sequence.
- You are sizing a connection pool, choosing a shard key, or setting a replica-lag budget, and need the math spelled out with a worked number.
- A partition is hot or a node is failing to vacuum or compact, and you must confirm a targeted fix against measured numbers.
- You must prove failover, backup restore, or migration behavior before trusting them in production.

Self-assign this skill before choosing a shard key, adding a replica, opening a live migration, or changing replication topology.

## WHEN NOT TO USE

- A single node with comfortable headroom and no scale, failover, or growth requirement; the machinery adds risk without adding value.
- Per-query tuning, index design, or bad-plan fixes: those live in query-performance-engineer and must be exhausted before adding machines. Do not replicate or shard around a fixable slow query.
- Correctness or business-logic bugs that a new topology will not cure — fix the code, not the cluster.
- A heavy batch or data-warehouse scan where a full scan is optimal and no replicas or shards change the answer.
- A managed store whose topology you do not own. If the vendor fixes replicas and sharding, do not re-implement them.
- Prototypes with no growth or failover requirement; adding replicas or shards prematurely is itself a scaling failure.
- Migrations that can afford real downtime (small table, short window). The zero-downtime machinery would then be waste and added risk.
- Decision making about a consistency guarantee the code does not actually provide; pick a topology that matches what the code can promise.

## DECISION TREE

Walk each branch in order; each later fork uses the earlier answers. Record the choice and what it sacrifices in a one-line trade-off.

### Scale-up vs read replicas vs shard vs managed

1. **Scale-up first.** If the working set fits in memory, CPU or I/O is not saturated for sustained periods, and the budget allows, add CPU/RAM. Simplest path: no application change, no consistency cost. Stop when you pay for large nodes you do not use, or a vertical limit (memory ceiling, license, single-node throughput) binds.
2. **Read replicas** when write throughput is fine but read load or analytical queries exceed the primary. Replicas offload reads; they do not raise the write ceiling. Choosing replicas means accepting read-staleness or routing current reads to the primary, and adds an extra DR/copy story.
3. **Shard when writes outpace one node or the working set outgrows one node's memory and read replicas cannot help.** Sharding is the last resort and the costliest to own: routing, rebalancing, and cross-shard consistency become your problem. Split only what must split; keep as one physical dataset everything that must be cross-shard atomic.
4. **Move to managed when operational overhead or HA is the binding constraint and you accept vendor control of topology and tooling.** Choose it when you would otherwise maintain replicas, failover, and backups yourself without the people to do it.

### Shard key selection

1. Draw candidate keys from the hottest, most selective access path (point lookups, tenant id, user id). The key must name the entity that most reads and writes in a per-request WHERE clause.
2. Confirm even spread: high cardinality and uniform distribution, with no dominant single value and no small top-N skew. A key that produces a hot value creates a hot shard, not a fix.
3. Confirm the key is immutable or nearly so. A key that users change turns one write into a rebalancing and a data-move exercise.
4. Confirm most queries can encode the key in the WHERE, so the load balances without cross-shard fan-out. A query that cannot name the key does a scatter (all-shard) scan and multiplies cost by the shard count.
5. Prefer hash-based logical sharding over range-only when there is no natural partition by time or region. Hash is the default because range skews onto hot ranges; use range only when the hot region is deliberate.
6. Prefer tenant-keyed sharding when multi-tenancy exists: per-tenant isolation beats a global hash when a tenant must not flood the others and ownership is clean.

### Replication topology

- **Sync vs async apply.** Synchronous commit (sync replica on Postgres; semi-sync on MySQL) guarantees the replica has a write before the client sees ack, at the cost of commit latency equal to one replica round-trip and a hard availability dependence on the replica. Async applies fast and stays available, but a replica can lag or lose the tail of a crash and read stale.
- **Quorum.** Write to W nodes and read from R with W+R > N and W > N/2 so the quorums intersect; standard when availability outranks a global order. Add a monotonic epoch/fencing token so only the majority-granted leader may write.
- **Failover and DR.** Designate a failover replica promoted intentionally, never by accident; fence the old primary so a stale node can never accept writes again. Give every replica the same, observed, WAL/binlog-backed stream and monitor per-replica lag. Decide which region wins on a regional partition in advance (CAP class).

### Isolation level by workload

- **Read-only reporting / OLAP on replicas:** READ COMMITTED (Postgres) or REPEATABLE READ with a statement snapshot, no write locks, highest concurrency.
- **OLTP primary writes:** READ COMMITTED default in both engines is enough for most single-row workloads; raise to SERIALIZABLE only where phantom or write-skew must be absolutely impossible, and accept the lock and deadlock cost.
- **Fence the assumption:** never let a fast index or a cached plan cover for what an isolation level must guarantee. If two readers must see consistent snapshots, code it at the isolation level; a query hint will not protect it.

### Record every decision

For each branch, write into the design record the choice, the rejected alternative, and the concrete failure mode conceded (e.g., "chose async replica; accepts 2 s read staleness on the reporting path"). The VERIFICATION GATE and any postmortem then check against this record.

### Worked example — a two-tenant order store

A service bursts to 40 k read/s and 800 write/s on a single 8-core Postgres (max_connections 300, 32 GB RAM, working set 180 GB). Two large tenants each ~90 GB, plus a long tail of small tenants.

1. Reads outpace the primary and are tiered and lease-only; writes 800/s are within a single leader's ceiling (~3-5k/s on this hardware). Scale-up is wasted on reads, so choose **read replicas**: add 2-3 PG replicas serving reporting and the high-volume read path; steering reads back to writes only for the read-your-writes window.
2. Writes still rarely join across tenants, but the total working set (180 GB) is already past the 32 GB RAM; steady, but a working set of shard % triggers. Because the two tenants are naturally isolated and their reads dominate, split by **tenant key** into 2 data shards (each `tenant_id` charted), plus a separate meta/keyspace shard.
3. Connection math: max_connections 300. App = 24 instances. A current pool of 40 per instance is 960 total — impossible; the correct ceiling is 0.8×(300/24) ≈ 10 per instance. Shrink to 12, add timeouts, retarget acquire config. These numbers go to the load gate.
4. Migration: add the cross-tenant index in expand, dual-write each tenant write, backfill each shard's history at ~500 rows/s × −20% margin = 400 rows/s. Verify per-shard row count equals the audit source and run sample checksums before switching reads.
5. A per-tenant value that turns hot is a **hot key**; keep `tenant_id` high-cardinality-hashed per tenant sub-key, never a single value.
6. Confirm the VERIFICATION GATE's failover drill, 2× peak load, and restore all pass on the 2-shard layout before cutover.

Record: scale-up rejected because write ceiling and cost; replicas chosen for reads; tenants sharded; async lag target 5 s on reporting path, read-your-writes ≤ 100 ms on the write path.

## PATTERNS

- **Zero-downtime migration — expand/contract + dual-write + backfill-and-verify.** Add the new column or table (expand); for every write, in the same transaction write both the old and the new schema (dual-write); then backfill the historical rows in bounded batches with a verify that row counts and checksums equal the source. When dual-write has run for at least one full business cycle (≥ 1 working day) without divergence, switch reads to the new schema, then drop the old column or table (contract).
  - Guard: do not drop the old schema until both (a) no new write uses it and (b) the verify count and checksum match. If the new-side write fails during dual-write, the old-side transaction must still commit; otherwise the migration eats live traffic.
- **Sharding with rebalancing.** Add shards by splitting existing ones; never the whole dataset. Migrate data in a consistent-hash-friendly split threshold with a double-write path during the move; a shard becomes a candidate when a load threshold is crossed while concurrent migration is capped so the cluster can't saturate while moving.
- **Connection pooling at scale.** Each application process holds a bounded pool; the sum of all pools must stay well under the database total `max_connections`. A connection is a backend process (Postgres) or a thread (MySQL) plus buffers, so every one costs memory and scheduling. A pool sized to the DB ceiling guarantees a connection storm; under-sizing queues every request.
- **Read-your-writes routing.** After a client writes, its subsequent reads route to the node holding the write (the leader or the shard that served the write) for a defined staleness budget; otherwise the client reads a lagging replica silently. If the app is fine with staleness, say so in the SLO — do not silently accept it.

## FAILURE MODES & MITIGATIONS

Each entry: detection, then fix. Validate at least 8 before claiming a scaled database is safe.

Full detail: `references/failure-modes-mitigations.md`.

## COMMON ANTI-PATTERNS

- **Sharding to fix a bad index or a plan.** Exhaust query-performance-engineer first; a shard cannot outrun a bombed query plan. - **Async replication promising read-your-writes.** Async reorders the reads; the promise breaks.
Route to the writer or monotonic read routing, or eat the stale read. - **A failover of only preference.** Without epoch/fencing, the old primary writes again (split brain).

Full detail: `references/common-anti-patterns.md`.

## REBALANCE AND DR CADENCE

- Trigger a rebalance on a load threshold, not a fixed calendar date. Migrate a bounded number of moves at once (cap concurrent moves at 1-2) so the cluster does not saturate while moving data.
- Every rebalance runs through the same dual-write + verify path as a migration: double-write during the move, verify counts and checksums after, and never route traffic to a half-moved shard.
- A hot table with replication and growth must record lag and bloat daily; a cold table can be checked on demand. Codify the cadence so silencing a check is an explicit, reviewed decision.

## SAFER BY DESIGN

Scaling is about making a system fail in a bounded way. Every choice above should leave clear headroom and an explicit ownership boundary. If a rule cannot be converted to a number and a measured gate, it stays an opinion until it is measured.

A scale-out decision is only complete when it carries a rollback path: the rebalance can halt, the migration can pause, and the failover can be reversed within the same window. Any plan without an exit route is a plan that has already chosen to stay.

## QUANTITATIVE RULES

Numbers are budgets for a scaling plan; each must be measured on the real cluster before you commit.

Full detail: `references/quantitative-rules.md`.

## VERIFICATION GATE

Nothing below is optional. Scaled-DB is "done" only when relevant checks are green against the numbers. The five checks map directly to the failures they retire: rehearsal retires migration corruption; checksum retires silent drift; failover drill retires split brain; 2× load test retires pool exhaustion, hot shard, and deadlock storms; restore retires backup restore failure.

**Migration rehearsal on a copy** — duplicate schema+data at production size and run the full expand/dual-write/contract without live traffic; fail if the copy's backfill veers off row-count/checksum or exceeds the time budget.

**Checksum verification** — before the final read switch, aggregate checksums and row counts per shard must match; re-run after any mismatch.

**Failover drill** — kill the primary; assert the replica becomes primary within the election budget, the old primary cannot write (fencing), and no acked write is lost.

**Load test at 2× peak** — at 1× then 2× for a sustained window; assert P95 within budget, no pool saturation, no lag breach where the SLO holds, and no hot shard or deadlocks forming.

**Backup-restore drill** — back up, restore clean, replay to a point; measure the span against RTO/RPO. Fail if the restore drifts or exceeds RPO.

**Drill format** — each drill is a scripted run with a start time, a stop condition, and a recorded result. Do not hand-drill production: rehearse on a copy, promote, and only then schedule the production drill. Record the output of every run in the design record so a regression is visible on the next cycle.

**Load test 2× peak numbers** — at 2× peak, run at least 30 minutes sustained. Assert: P95 latency ≤ 2× its target; connection pool never reaches refusal; replica lag stays inside the read-your-writes window; no deadlock or lock timeout appears in the sample. Any assertion that fails means the design is not done.

Record for each: the rehearsal, the verify, the failover, the 2× load test, and the restore within RTO. A scaling claim without this evidence is unverified.

## Go back to query-performance-engineer first

Exhaust query-performance-engineer before scaling. Slow-query, index, and cache fixes off single-node pressure cheaper and faster than any topology change. Its DECISION TREE also names when to shard versus index.

## REFERENCES

- **Kleppmann, M.** Designing Data-Intensive Applications (O'Reilly). Chapters on replication and partitioning: the authoritative basis for topology and shard-key choices.
- **PostgreSQL documentation** — streaming/synchronous replication, VACUUM and autovacuum, `pg_stat_replication`, logical replication.
- **MySQL 8.0 Reference Manual** — single/multi replication, InnoDB reorg and `OPTIMIZE TABLE`, transaction isolation.
- **query-performance-engineer** — the G2 index/plan skill to exhaust before this one; check its DECISION TREE and failure modes first.

## CHANGELOG

- 2026-08-06 | Phase 3.5: database-at-scale created (G3: replication, sharding, zero-downtime migration, quantitative rules) | database-at-scale