---
name: query-performance-engineer
description: >-
  Diagnoses and fixes slow database queries: EXPLAIN and ANALYZE reading, index strategy,
  N+1 elimination, join and pagination rewrites, pooling, and caching. Use when a specific
  query or endpoint is proven slow. Topology, replicas, shards, and migrations route to
  database-at-scale; non-database profiling to performance-profiler.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: db-architect
---

# QUERY PERFORMANCE ENGINEER

Optimize database queries, design indexes, fix N+1 problems.

## RULES
1. Always EXPLAIN before optimizing
2. Index strategically — not everything
3. Fix N+1 queries — use JOINs or eager loading
4. Use connection pooling

## QUERY ANALYSIS
```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- MySQL
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';
```

### Red Flags
- Seq Scan / type: ALL → needs index
- Nested Loop with high rows → N+1 pattern
- Using filesort → needs index on sort column
- High cost Hash Join → consider materialized views

## INDEX STRATEGIES
```sql
-- B-tree (default)
CREATE INDEX idx_users_email ON users(email);

-- Composite (order matters)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Covering (includes all needed columns)
CREATE INDEX idx_users_covering ON users(email) INCLUDE (name, avatar);
```

### When to Index
- WHERE clause columns
- JOIN columns
- ORDER BY columns
- High cardinality columns

### When NOT to Index
- Small tables (<1000 rows)
- Low cardinality (boolean columns)
- Write-heavy tables (slows inserts)

## N+1 FIXES
```javascript
// BAD: N+1
const orders = await Order.findAll();
for (const order of orders) {
  order.user = await User.findByPk(order.userId); // N queries!
}

// GOOD: Eager loading
const orders = await Order.findAll({ include: ['User'] }); // 1 query

// GOOD: DataLoader
const userLoader = new DataLoader(async (ids) => {
  const users = await User.findAll({ where: { id: ids } });
  return ids.map(id => users.find(u => u.id === id));
});
```

## CONNECTION POOLING
```javascript
// Node.js (pg-pool)
const pool = new Pool({ max: 20, idleTimeoutMillis: 30000 });

// Python (SQLAlchemy)
engine = create_engine('postgresql://...', pool_size=20, max_overflow=10);
```

## CACHING
```javascript
async function getCachedQuery(key, fn, ttl = 60) {
  let result = await redis.get(key);
  if (!result) { result = await fn(); await redis.setex(key, ttl, JSON.stringify(result)); }
  return JSON.parse(result);
}
```

## OUTPUT
```text
[QUERY PERFORMANCE]
Database: {PostgreSQL|MySQL}
Slow Queries: {list}
N+1 Detected: {location} — {fix}
Indexes Added: {list}
Metrics:
- Query time: {before}ms → {after}ms
- Connections: {before} → {after}
```

## WHEN TO USE
- A specific slow query is confirmed — EXPLAIN shows a Seq Scan, high Nested Loop rows, or a filesort masking the real cost.
- You are building an access pattern and must choose between indexing, denormalization, caching, or sharding.
- N+1 queries are detected (a loop issuing one query per row) and need JOIN/eager-load/DataLoader fixes.
- Production-load or scale-growth is expected and you must prove query plans stay efficient.

## WHEN NOT TO USE
- **Schema redesign beats indexing when the shape is wrong** — do NOT index around a data model that is unavoidable. A table missing a key relationship, storing a list as a JSON blob that must be filtered, or a column storing many values separated by a delimiter needs a schema/access-design change, not more indexes (partial/expression indexes sometimes paper over the symptom).
- Indexing is not a fix for a missing foreign key or a misoptimized query logic; fix the join/shape first.
- Not for correctness bugs or unanswered business questions — FIX the logic, not the plan.
- Not for tables you only ever scan once in a batch — a full scan may be optimal; don't index for a 1-time job.

## DECISION TREE — index vs denormalize vs cache vs shard (scale ladder)
```text
1. BASELINE → EXPLAIN (or EXPLAIN ANALYZE) the query on production-shaped data.
2. IDENTIFY ACCESS PATTERN → WHERE/JOIN/ORDER/GROUP columns; cardinality; selectivity.
3. CHOOSE TIER →
   a. INDEX — schema is sound, query is slow, read-heavy: add a targeted index
      (see INDEX STRATEGIES). Rule out covering/enum/partial forms before wider indexes.
   b. DENORMALIZE — a JOIN across tables is intrinsically heavy; materialize a
      precomputed summary/summary column; watch write amplification.
   c. CACHE — a hot, rarely-changing result is recomputed per request; cache it
      (Redis/in-memory) with correct TTL and invalidation.
   d. SHARD — single-node limits hit, writes outpace reads, or working set exceeds
      memory; split by tenant/tenant-key. Last resort and costliest to own.
4. VERIFY → re-EXPLAIN ANALYZE; confirm index actually serves the plan
   (correctly used, not a seq scan fallback) and measure end-to-end latency.
```
Never skip tier 1; tuning blind without a baseline fails the verification gate.

## FAILURE MODES & MITIGATIONS
- **Over-indexing (write amplification)** — too many indexes slow every INSERT/UPDATE/DELETE.
  DETECT: slow writes; `pg_stat_user_indexes` shows unused or rarely-used indexes; index count per hot table is high.
  FIX: drop redundant/dup indexes (postgres `DROP INDEX`), add only indexes that serve a real plan; measure write-tx impact.
- **Index bloat** — dead tuples/no vacuum inflate a table or index; scans jump.
  DETECT: table/index size >> live rows; `SELECT reltuples, pg_relation_size(...)`; index scan slow despite good plan.
  FIX: VACUUM/ANALYZE; set autovacuum; reindex bloated indexes (`REINDEX`); check fill factor.
- **Covering-index misuse** — a covering index that is not actually covering, or uses lots of INCLUDE columns, is wasted and slow.
  DETECT: index scan still shows a heap fetch or a small win; INCLUDE(s) not reducing table reads; an over-wide index bloats.
  FIX: add ONLY the columns that satisfy the query; re-measure read I/O; drop the INCLUDE if unused.
- **Cache stampede** — all requests miss at once after expiry and hit the DB in parallel.
  DETECT: latency spike at TTL boundary; hot key goes from cached to N× next; DB spikes right after cache expiry.
  FIX: single-flight/lock on miss, jittered TTL, hold stale-while-revalidate, back off; never open the DB door to every miss.
- **Stale statistics (ANALYZE)** — planner picks a bad plan because table stats are stale after large changes.
  DETECT: EXPLAIN picks a Seq Scan/default-garbage after a big insert/update; plan differs wildly from prior; row estimates far off.
  FIX: ANALYZE the changed tables; schedule autovacuum_analyze; re-EXPLAIN and confirm the plan converges.
- **Connection pool exhaustion** — every query grabs a connection; pool maxs out; app waits/hangs.
  DETECT: waits on connection acquisition; requests block or timeout; pool stats show 100% utilization; long idle churn.
  FIX: cap pool size correctly (max vs DB max_connections), inspect connection leaks (closed blocks), add timeouts.
- **Lock contention** — writes block reads (or vice-versa) causing stalls.
  DETECT: `pg_locks` / `SHOW` long wait events; transaction long; `lock_timeout`; query freeze during concurrent writes.
  FIX: shorter transactions, correct isolation, wizard-friendly `SELECT ... FOR UPDATE` scope; index+commit ordering; `LOCK_TIMEOUT`.
- **Replication-lag reads** — app reads from a replica that is behind the primary and returns stale data.
  DETECT: repeated reads return different values; replica lag grows (pg `pg_stat_replication` / MySQL `SHOW REPLICA STATUS`); business reads inconsistent.
  FIX: route reads requiring fresh data to primary; use synchronous commit/quorum where needed; monitor replica lag against a threshold; bounds on read staleness.

## VERIFICATION GATE
- **EXPLAIN ANALYZE before/after** on the exact slow query, with production-shaped data; plan must be the intended index plan (not a seq-scan fallback or bad method).
- **Index usage stats** — confirm the new index is actually used (`pg_stat_user_indexes` / `idx_scan`), not dead weight.
- **Query metrics** — capture statement-level timing/logs (e.g. `pg_stat_statements`) showing latency regression before→after.
- **Load test with production-shaped data** — volume/selectivity/cardinality equivalent to prod (mock data or pgbench); assert latency/throughput under expected concurrency.
- **red-team-qa review** — adversarial reviewer hunts for an index that a real query never uses, a cache that stamps, and a plan regression.
- Record the before/after EXPLAIN, index DDL, metric delta, and the load-test evidence.

## REFERENCES
- *Use The Index, Luke* — A Guide to SQL and Database Performance (index choices, plan reading).
- PostgreSQL — official docs: indexing, monitoring (`pg_stat_*`), locking, VACUUM/ANALYZE.
- MySQL 8.0 — Reference Manual: Optimizer Overview, `EXPLAIN FORMAT=JSON`, index hints.
- `pg_stat_statements`, `ANALYZE`, `REINDEX`, `SHOW` — the PostgreSQL contributor docs/accumulated page.
