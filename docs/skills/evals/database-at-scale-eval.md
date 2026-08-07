# database-at-scale — Flagship Eval

## 1. Trigger test

FIRE (5):
- "A Postgres node saturates, choose scale-up vs read replicas vs shard vs managed for a 40k read/s path."
- "Split a 1.6TB tenancy that now runs on 4 nodes into 8-16 nodes with rebalancing."
- "Run a zero-downtime migration (expand/contract, dual-write, backfill-with-verify) on this order table."
- "Size the connection pool for 24 app instances so we never exceed a 300-conn max."
- "A partition is hot and node autovacuum lags — verify against real numbers and confirm a fix."

NOT FIRE (3):
6. "Design a single-node local DB with comfortable headroom."
7. "Tune one index / slow query on a small table"
8. "Fix a business-logic bug in a CLI that stores to a local sqlite file."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — scale-up→replicas→shard→managed, shard-key, sync/async/quorum, isolation, worked example.
(b) failure modes have detection+mitigation: 5/5 — replication-lag, split-brain, migration-drift with checksum, hot-shard, deadlock-storm, pool-exhaustion, atleast 10.
(c) quantitative rules are numbers: 5/5 — lag ≤50ms/≤30s, connection math formula, shard ≤100-300GB, batch rate = budget-20%, pool 60-80% ceiling.
(d) verification gate executable: 5/5 — rehearsal, checksum, failover drill, 2×peak load test, restore-within-RTO.
(e) references authoritative: 4/5 — DDIA, PostgreSQL, MySQL docs; query-performance-engineer referenced for boundary.
(f) no contradictions: 5/5 — explicitly forwards to query-performance-engineer first; aligned with distributed-systems on quorum/RYW.

## 3. Reference task
A tenant store bursts to 40k reads/s and 800 writes/s on a single 8-core PG (300 conns, 32GB RAM, 180GB working set). The skill must pick replicas vs shard, compute pool ceiling per instance, give a zero-downtime migration sequence, and a verification gate that includes failover + 2× peak.
