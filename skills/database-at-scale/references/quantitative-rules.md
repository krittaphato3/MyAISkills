# database-at-scale — QUANTITATIVE RULES

### Replica lag budgets
- read-your-writes means P95 replica lag ≤ 50 ms by routing to the writer or a quorum.
- Cross-region async lag is commonly seconds: expect 0.5-2 s, alert if lag exceeds target for > 10 s continuously, fail the test at 2× the target.
- The read-your-writes window is (P95 write) + (max acceptable staleness). Keep it explicit.
- Worked: app write path P95 25 ms, accept 100 ms staleness → a read-your-writes reader after a write routes to the writer for 125 ms, then may read a replica. Anything that must be fresh routes to the writer for the full window or uses monotonic reads.

### Replication wavelength in DR
When you add a replica for DR, state its target lag in seconds (e.g., ≤ 30 s cross-region) and its RPO (e.g. ≤ 1 min) as separate numbers. A replica that meets lag but not RPO, or vice versa, is a different network contract. Alert on both at once.

### Connection math
max_connections on PG/MySQL is typically 100-300. The sum of all app pools must stay at 60-80% or under so admin, vacuum/compaction, and maintenance workers have ceiling.

Worked: Postgres `max_connections = 300`; 24 app instances each hold 40 pooled connections = 960 needed, which exceeds the ceiling by 3.2× and forces refusal + latency. A safe basis: each instance pool_size ≈ 80% × max_connections ÷ instances. With 200 max and 10 instances: pool_size ≈ (0.8×200)/10 = 16 per instance is the upper bound. Start lower (10-12) and raise only under a load gate that proves no connection refusal.

If avg query time is q ms and you need requests/sec r per instance, then active connections ≈ r×q/1000; a pool must be ≥ that plus headroom, and ≤ the ceiling, or sockets churn. Never size a pool by max_connections alone — size by concurrency × per-query latency.

### Shard size limits
- Keep the working set for a hot shard below available RAM and keep each shard under ~100-300 GB for OLTP (range-heavy less); trigger a split when a shard exceeds the mean by ~20% or the absolute cap for the node.

### Worked shard sizing
Given 4 nodes of 64 GB RAM each and a 1.6 TB dataset. To keep each hot working set under one node's RAM you can hold at most ~50 GB hot per node, so sharding by a flat split of 4 (400 GB each) leaves hot data over memory. Prefer more, smaller shards: split to 8-16 so the hot shard's working set fits ~48-60 GB of RAM. Choose the number N where N × working_set_per_shard ≤ 0.8 × node RAM; a rebalance is then a split, not a global reshard.

### Migration batch sizing
- Size a batch so it does not starve the cluster and P99 production latency stays in budget. A starting formula: target rows_per_second = (production write budget, e.g., 500 rows/s) − 20% margin. For a 10 M row table that is 500 − 100 = 400 rows/s ≈ 10 h of backfill plus verify.
- Set per-batch rows at what fits a comfortable fraction of shared working memory and reduce if the latency budget regresses.
- Each batch must be restartable and idempotent; if a batch fails, re-run only that batch, then continue. The verify runs per-batch and an aggregate rowcount+checksum at the end.

### Worked migration budget
Given: 10 M rows, ~500 B/row → ~5 GB new column, batch of 50,000 rows. Sample P99 write-latency during dual-write is 120 ms; load gate 2×peak demand is unresolved. Start at 200 rows/s; on a copy ramp to 400 rows/s in 100 rows/s steps, watching replication lag and write P99. If P99 stays ≤ 200 ms and lag stays ≤ 5 s, accept 400 rows/s → the backfill completes in about 7 h. Otherwise keep the migration pace lower, or extend the window, and record the achieved number.
