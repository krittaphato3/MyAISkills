---
name: data-pipeline-engineer
description: >-
  Builds bulk data movement and transformation: ETL/ELT jobs, batch versus streaming, DAG
  orchestration, incremental loads and CDC, schema evolution, backfills, and data-quality
  checks. Use when data must land somewhere reliably at volume. Database topology routes
  to database-at-scale; per-query tuning to query-performance-engineer; app-side workers
  to background-jobs-engineer.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: data-engineer
---

# Data Pipeline Engineer

A pipeline is judged on three things and nothing else: is the data **complete**, is it **correct**, and is it **reproducible** — including when it has to be re-run. Streaming is a transport choice; idempotent, re-runnable steps are the actual requirement.

## WHEN TO USE

- **Bulk movement/transformation** — ETL/ELT between systems, warehouses, lakes.
- **Incremental loads** — watermarks, change data capture, upserts, deletes.
- **Orchestration** — DAGs, dependencies between steps, scheduling, retries.
- **Schema evolution** — adding/renaming/typing columns without breaking consumers.
- **Correctness incidents** — missing rows, duplicates, drift between source and target.
- **Backfills** — reprocessing history after a bug or a logic change.

## WHEN NOT TO USE

- **Database topology, replication, sharding, zero-downtime migrations** — `database-at-scale`.
- **A single slow query** — `query-performance-engineer`.
- **Queue/worker mechanics for application jobs** — `background-jobs-engineer`.
- **Dashboard/SLO design** — `observability-sre`.

## DECISION TREE

1. **Batch or stream?** Batch unless the requirement is a bounded latency the business actually needs. Streaming costs correctness complexity; do not pay it by default.
2. **Is it idempotent?** Every step must be safe to re-run for a window: upsert by key, or delete-then-insert for the partition. Design this before writing transform logic.
3. **Full or incremental?** Incremental needs a watermark (and a late-arrival policy). If late data is possible, define how it is absorbed.
4. **What is the grain?** Name the primary key and the timestamp of every table. Most pipeline bugs are grain bugs.
5. **How does schema change?** Additive-only by default; breaking changes get a migration + consumer plan.
6. **How is it orchestrated?** Dependencies explicit; retries bounded; each step emits a run record.
7. **How is it checked?** Data-quality assertions on row counts, null rates, referential integrity, and freshness — failing the run, not just warning.

## PATTERNS

### 1. Idempotent steps
```text
extract(source, window) → stage → transform → MERGE/UPSERT on natural key → publish
      ↑ watermark persisted only after the target commit
```
- The watermark advances only after a successful commit; otherwise a crash loses data silently.
- Prefer partition overwrite (delete window → insert) for recomputable transforms; MERGE for cumulative tables.
- Never append-only a source that can redeliver rows without a dedupe key.

### 2. Incremental & CDC
- Watermark on an immutable, monotonic column (updated_at with tie-breakers, or a sequence).
- Handle late arrivals with a lookback window wider than the expected delay, or an explicit late-arrival path.
- CDC deletes are as important as inserts; a pipeline that cannot see deletes drifts.
- Backfills reuse the exact same code path with an explicit window — never a one-off script.

### 3. Schema evolution
- Additive changes (new nullable columns) are safe; renames and type changes are breaking.
- Version the contract with consumers; publish a deprecation window for anything removed.
- Cast explicitly at the boundary; do not let an inferred type silently change a column.

### 4. Data quality gates
```text
row_count vs expected range · null/dup rate on key columns · referential integrity
· freshness (max timestamp age) · distribution shift on critical metrics
```
- Quality checks fail the run and block downstream, or they are decoration.
- Store the check results as evidence per run (counts, rates, thresholds).

### 5. Orchestration
- DAG with explicit dependencies; a step starts only when its inputs are complete.
- Bounded retries with backoff; a failed step alerts and stops dependents (no partial propagation).
- Every run writes a record: inputs, window, counts in/out, duration, status — the audit trail that makes backfills safe.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Non-idempotent step** — DETECT: a re-run duplicates rows. FIX: MERGE on a natural key or partition overwrite.
2. **Watermark advanced too early** — DETECT: gaps after a crash. FIX: advance only after the target commit.
3. **Grain bug** — DETECT: fan-out duplication from a bad join. FIX: assert key uniqueness after every join.
4. **Silent schema break** — DETECT: downstream job fails or a column turns null. FIX: explicit casts + contract tests.
5. **Late data ignored** — DETECT: totals drift from source. FIX: lookback window or late-arrival handling.
6. **Deletes invisible** — DETECT: target has rows the source deleted. FIX: CDC delete handling or periodic reconciliation.
7. **Quality checks that warn only** — DETECT: bad data flows downstream. FIX: fail the run and block dependents.
8. **One-off backfill script** — DETECT: backfill logic differs from production. FIX: reuse the same code path with an explicit window.
9. **No run record** — DETECT: nobody can answer "what ran, on what window". FIX: persist per-run metadata.

## QUANTITATIVE RULES

- Every step idempotent for an explicit window; a re-run must not change the result.
- Uniqueness asserted on the natural key after every join (zero duplicate tolerance on grain columns).
- Freshness SLA per table with an alert when the max timestamp age exceeds it.
- Bounded retries with backoff; failed quality checks block downstream.
- Every run persists inputs, window, row counts in/out, duration, and status.
- Backfills use production code paths; one-off scripts are a review reject.

## VERIFICATION GATE

- **Idempotent?** Re-running the same window produces identical output, demonstrated.
- **Watermark safe?** Advances only after commit, with the failure window reasoned about.
- **Grain correct?** Uniqueness assertion passes on the output keys.
- **Quality gated?** Checks run per load, fail the run, and produce evidence.
- **Reconciled?** Source↔target row counts reconcile, with the query attached.
- **Auditable?** Per-run metadata is stored and queryable.

```text
[DATA PIPELINE]
Mode: {batch | streaming} · Orchestrator: {tool} · Schedule: {..}
Tables: {name} grain {key} · watermark {column} · late-arrival {policy}
Idempotency: {MERGE key | partition overwrite}
Quality checks: counts {..} · null rate {..} · referential {..} · freshness {..}
Reconciliation: source {n} = target {n} — {query/path}
Run record: {table/log path}
Backfill: {same-code-path command}
```

## REFERENCES

- `database-at-scale` — topology, replication, zero-downtime migrations.
- `query-performance-engineer` — per-query tuning, carved out above.
- `background-jobs-engineer` — scheduling/queue mechanics for app jobs.
- `observability-sre` — freshness and failure alerting.
- `data-engineer` agent — the implementing role.

Ownership: maintained by data-engineer; data-pipeline-engineer is the production-domain skill for bulk data movement.
