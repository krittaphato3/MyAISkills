# database-at-scale — COMMON ANTI-PATTERNS

- **A failover of only preference.** Without epoch/fencing, the old primary writes again (split brain).
- **Over-indexing during a migration:** adding many indexes to speed the backfill, then never dropping them, raising write amplification for the migration's dual-write.
- **A testing gap on the migration copy:** a migration never rehearsed on a copy is an un-met VERIFICATION GATE.
- **A pool sized to max_connections rather than concurrency × latency** — this guarantees a storm at high load, not a stable ceiling.
- **A migration that backfills while the source still writes but misses the concurrent-write tail** — the last rows are never dual-written and drift forever.
- **Sharding by a mutable key** (user email changes) that forces a rebalance on every key change.
