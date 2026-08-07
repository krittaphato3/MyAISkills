# concurrency-engineer — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Design the threading/async model for a subsystem that holds 10k concurrent network waits with shared mutable state."
2. "Debug a deadlock between two Go goroutines and a livelock in retry logic."
3. "Should this state be a mutex, an atomic, sharded, or passed as a message?"
4. "Add a bounded thread pool with backpressure to a bursty producer path."
5. "Verify a lock-free queue change with race detectors, stress, and model checking."

Not fire (3):
6. "Do basic sequential arithmetic on one core (no threads)."
7. "Choose C++ atomics ordering for one hot loop — that's systems-core-architect's rule."
8. "One-off script with no concurrency, single-threaded."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — parallelism vs concurrency, primitives (thread/async/actor/CSP), shared-vs-message, all first-match.
(b) failure modes have detection + mitigation: 5/5 — all 8 (race, deadlock, livelock, starvation, priority inversion, false sharing, sync-over-async, leak) DETECT→FIX.
(c) quantitative rules are numbers: 5/5 — µs spawn costs, mutex/atomic ns, contention % threshold, channel buffer guidance.
(d) verification gate executable: 5/5 — go test -race, TSan, miri, stress+soak, backoff model-checking for lock-free relaxations.
(e) references authoritative: 5/5 — Go Mem Model, JSR-133, cppreference, Herlihy & Shavit, priority-inheritance paper.
(f) no contradictions: 4/5 — correctly delegates memory-model/ordering to systems-core-architect to avoid duplication; consistent.

## 3. Reference task
A microservice handles 10k concurrent I/O waits but also a small CPU-bound render stage. The skill must choose the coordination model, shard or message-pass the shared state, size a bounded pool, and design race/deadlock/stress verification commands that actually run.
