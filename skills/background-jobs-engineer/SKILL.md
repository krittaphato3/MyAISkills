---
name: background-jobs-engineer
description: >-
  Designs work that runs outside a request: queues, workers, cron and delayed jobs,
  retries with backoff, dead-letter queues, idempotent handlers, and visibility timeouts.
  Use when work must survive the request, be retried, or be scheduled. In-process threads,
  async primitives, and locks route to concurrency-engineer; bulk data movement to
  data-pipeline-engineer.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: code-implementer
---

# Background Jobs Engineer

Anything slow, flaky, or scheduled belongs outside the request path. This skill is the discipline of durable async work: jobs that survive a deploy, run exactly once as far as the user can tell, and fail into a place a human can find them.

## WHEN TO USE

- **Slow work off the request path** — emails, PDFs, exports, thumbnails, third-party calls.
- **Scheduled work** — cron, nightly reports, recurring syncs, cleanup/purge.
- **Delayed work** — reminders, trial-expiry, retry-after-cooldown.
- **Fan-out / batch** — process 10k rows, backfill, reindex.
- **Fixing job reliability** — duplicates, lost jobs, stuck queues, retry storms.

## WHEN NOT TO USE

- **In-process parallelism** — threads, goroutines, async/await, mutexes, data races: `concurrency-engineer`.
- **Retry/backoff/circuit-breaker policy for a specific service call** — `resilience-pattern-engineer` supplies the policy; this skill supplies the job that applies it.
- **Data pipelines with transformation semantics** — `data-pipeline-engineer`.
- **One fast step that belongs inline** — do not queue a 2 ms operation.

## DECISION TREE

1. **Does it belong off-path?** Queue it if it is slow, unreliable, retryable, scheduled, or not needed for the response. Otherwise keep it inline.
2. **What is the trigger?** Event-driven (on user action), scheduled (cron), or delayed (time offset). Different mechanisms, different failure modes.
3. **Is the handler idempotent?** Assume at-least-once delivery. If the handler is not idempotent, make it so before enqueueing anything.
4. **What is the payload?** Pass an **id**, not the full object — state is read fresh at execution and the queue is not a database.
5. **What is the retry policy?** Bounded attempts, exponential backoff + jitter, and a dead-letter destination. No infinite retries.
6. **What does failure look like?** A dead-letter queue with alerting, plus an operator path to re-drive.
7. **Is it observable?** Queue depth, oldest-job age, failure rate, and duration per job type — alert on age and depth.

## PATTERNS

### 1. Job handler contract
```text
load state by id → check if already done (idempotency key) → do work
→ record completion → ack
```
- Idempotency key stored durably (DB row, unique constraint) — not in worker memory.
- No shared mutable global state between jobs; each job is a pure function of the DB.
- Never hold a transaction open for the whole job.

### 2. Enqueueing
- Enqueue in the **same transaction** as the state change when possible (transactional outbox), so a crash cannot lose the job or emit it for a rolled-back change.
- If no outbox, accept and document the failure window, and add a reconciler.
- Keep payloads small; version them so old queued jobs survive a deploy.

### 3. Schedules
- Cron jobs run in **one** place: a leader election, a lock, or a scheduler that guarantees single execution.
- Recurring jobs must be safe to run late, early, or twice (a missed run is normal).
- Bound the window: a nightly job processes a specific date range, so a re-run is deterministic.

### 4. Retries & dead letters
- Retry only on transient errors (timeouts, 5xx, throttling); never on validation/4xx.
- `delay = min(cap, base * 2^attempt) + jitter`. Cap attempts (commonly 5–8).
- After the cap: dead-letter with the payload, error, and attempt history; alert; provide re-drive.

### 5. Long jobs & fan-out
- Break a long job into chunks that checkpoint progress, so a crash resumes rather than restarts.
- Fan out with a concurrency limit; a queue of 50k jobs should not spawn 50k parallel workers.
- Backpressure: stop pulling when downstream is saturated.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Non-idempotent handler** — DETECT: a retry charges twice / sends twice. FIX: idempotency key + durable completion record.
2. **Lost job** — DETECT: state changed but the job never ran. FIX: transactional outbox or a reconciler that finds missed work.
3. **Duplicate scheduled run** — DETECT: the nightly job ran on multiple nodes. FIX: single-flight lock / leader election.
4. **Infinite retry** — DETECT: a poison message cycling forever. FIX: capped attempts + dead-letter + alert.
5. **Fat payload** — DETECT: full objects serialized into the queue; stale data executed later. FIX: pass ids; read at execution.
6. **Unbounded fan-out** — DETECT: worker count scales with queue depth. FIX: fixed concurrency + backpressure.
7. **Silent backlog** — DETECT: queue grows with no alert. FIX: alert on oldest-job age and depth.
8. **Deploy breaks in-flight jobs** — DETECT: old payloads fail after a schema change. FIX: version payloads and handlers; drain before breaking changes.
9. **Job holds a DB transaction** — DETECT: lock contention and timeouts during batches. FIX: short transactions per unit of work.

## QUANTITATIVE RULES

- Payload size small and id-based; large blobs go to object storage with a reference.
- Retry attempts capped (5–8) with exponential backoff + jitter; zero unbounded retries.
- Every queue has a dead-letter destination and an alert on depth / oldest-job age.
- Scheduled jobs run single-flight; recurring jobs tolerate missed/duplicate runs.
- Chunk long jobs (bounded units) so a crash resumes; worker concurrency is capped.
- Alert thresholds: queue depth and oldest-job age — not just failure count.

## VERIFICATION GATE

- **Idempotent?** Handler safe to run twice, with a durable completion record.
- **Durable enqueue?** Job cannot be lost or emitted for a rolled-back change (outbox or documented window).
- **Bounded retries?** Policy present, dead-letter configured, alerting on.
- **Single-flight schedules?** Recurring work cannot double-run across nodes.
- **Observable?** Depth, age, failure rate, duration instrumented.
- **Crash-safe?** A killed worker mid-job leaves a recoverable state, demonstrated or reasoned with evidence.

```text
[BACKGROUND WORK]
Trigger: {event | scheduled | delayed}   Mechanism: {queue | cron | scheduler}
Job: {name} · payload {id-based} · idempotency {key}
Retries: {attempts} · backoff {base, jitter} · dead-letter {destination} · alert {rule}
Concurrency: {cap} · backpressure {yes}
Observability: depth {..} · oldest-age {..} · failure-rate {..} · duration {..}
Crash test: {evidence path}
```

## REFERENCES

- `concurrency-engineer` — in-process parallelism, carved out above.
- `resilience-pattern-engineer` — the retry/backoff/circuit-breaker policy applied inside a job.
- `data-pipeline-engineer` — transformation-heavy batch work.
- `observability-sre` — alerting on queue health.
- `integration-engineer` — webhook processing that feeds these queues.

Ownership: maintained by code-implementer; background-jobs-engineer is the production-domain skill for durable async work.
