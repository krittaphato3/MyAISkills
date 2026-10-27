---
name: concurrency-engineer
description: >-
  Designs and debugs concurrency and parallelism: threads, goroutines, async/await,
  actors, channels and CSP, locks, lock-free structures, cancellation, and data-race or
  deadlock safety. Use when correctness depends on interleaving, shared state, or
  backpressure. Multi-node consistency routes to distributed-systems-engineer; queued work
  to background-jobs-engineer.
metadata:
  version: 3.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: code-implementer
---

# concurrency-engineer

World-class guidance for writing correct, scalable concurrent and parallel code: choosing the right primitive (threads vs async vs actors vs CSP), guarding shared state with locks or message passing, using lock-free structures only when justified, and proving safety with race/deadlock detectors, stress tests, and model checking. Per-language memory models and atomic orderings (C++ `std::atomic`, Go happens-before, Rust atomics, JMM/JSR-133) are owned by systems-core-architect, cited by name — this skill covers the language-agnostic coordination design, failure modes, and numeric budgets that sit on top of those models.

## WHEN TO USE

Use this skill when two or more activities can overlap in time or run in parallel on separate cores, especially when you must answer "how do these threads/goroutines/tasks coordinate safely?":

- Designing the threading, goroutine, async, actor, or CSP model for a subsystem before writing it.
- Adding or refactoring a mutex, atomic, channel, future, sync pool, or concurrent collection.
- Parallelizing a CPU-bound loop across cores, or overlapping I/O waits in a service.
- Debugging or fixing a data race, deadlock, livelock, starvation, priority inversion, or thread/goroutine leak.
- Deciding whether state should be shared (locked), sharded, or passed as a message.
- Verifying a change with race detectors, stress tests, deadlock monitors, or model checking.
- Reviewing any code that spawns background work whose lifetime nobody joins.

## WHEN NOT TO USE

- **Purely sequential work** — one logical task, no overlapping wait or compute. Adding concurrency buys complexity with no payoff.
- **Serial-fraction-dominated work** — if Amdahl's serial fraction s > 0.1 (speedup ceiling 1/s ≤ 10x), fix the serial path instead of adding cores.
- **Work smaller than the overhead** — parallelizing a task that is not ≥ 5-10x its spawn cost makes it slower, not faster.
- **No measured need** — no profile, no stated latency/throughput requirement. Do not add threading or locking on intuition.
- **Platform forbids threads** — single-threaded runtimes (browser main thread, some WASM) where only async or workers apply; use those rules, not raw threads.
- **Per-language memory models** — that is systems-core-architect's job. Delegate atomic-ordering decisions to it; return here for structure and failure modes.

## DECISION TREE

Branch top-down; the first match decides. Always establish the goal first.

### 1. Parallelism vs concurrency

- **Speedup for a CPU-bound task** (turn N cores into less wall-clock) → parallelism. Pays off only when the serial fraction s stays small (Amdahl ceiling 1/s) and the work is embarrassingly parallel or a measured hot loop.
- **Responsiveness / overlap under I/O** (handle 10k concurrent waits) → concurrency without demanding many cores; one event loop or one thread-per-wait, not busy threads iterating over a lock.
- **Both** → pipeline: compute stages run on cores, I/O boundaries are async; connect stages with bounded queues.

### 2. Threads vs async vs actors vs CSP (Go channels) — by workload

- **Threads**: long-lived, CPU-bound or blocking-syscall-bound tasks with straightforward stack-based control flow. Simplest mental model; costs are per-thread stack (typically 1-8 MiB) and context switches under contention.
- **Async / event-driven**: 10k+ mostly-waiting tasks (network servers, timers). Cheap per-task footprint (state machine, no stack), one scheduler. Costs: non-blocking code shape and the trap of blocking inside it (sync-over-async deadlock).
- **Actors**: each entity (session, user, worker) owns a mailbox and processes one message at a time — no shared fields, so races are impossible by construction (Erlang, Akka, Orleans, Python `thespian`). Best when the domain decomposes into isolated, message-driven entities. Never share state across actors; pass only owned messages.
- **CSP (Go channels)**: goroutines own their goroutine; coordination happens by handing values over `chan`, not by sharing memory. Use channels when a value's ownership moves (a job, a packet, a result); use a mutex when a shared invariant must be read/updated in place.
- Tie-break: **"hand me a value / who owns it" → channel or future. "read and keep a live invariant" → mutex or atomic.** When in doubt, protect state with a mutex and communicate ownership with channels.

### 3. Shared state vs message passing

Ask "who writes, and how often?":

- Single writer, many readers → make the value effectively immutable and publish it once (atomic publish), or use an RwLock if it changes.
- Multiple writers to one invariant → one mutex, or shard the key space into several smaller locks.
- The value moves (ownership transfer) → pass it over a channel/message/future; shared ownership is a race vector, ownership transfer removes the race by construction.
- Actor-internal fields: the actor alone mutates them; never expose references to other threads.

## PATTERNS

### 1. Lock-ordering discipline
Impose a global total order on every lock (rank by module/id/address). Acquire only in ascending rank, release in reverse, and never hold a lock while acquiring a lower-rank one. Encode the order in a checked helper so a distant edit cannot break it. Two locks overlapping in either order is a deadlock waiting to happen.

### 2. Lock-free structures (only when justified)
- Justification: the profile names the mutex (see QUANTITATIVE RULES threshold) AND the structure fits a proven off-the-shelf pattern (SPSC/MPMC queue, Treiber stack, hazard-pointer map, refcount) AND you can argue liveness. Lock-free is not "fewer worries" — it trades a mutex deadlock for harder memory-ordering bugs that race detectors may miss (see FAILURE MODES). Never hand-roll an arbitrary concurrent object "lock-free" without a formal model.
- Prefer the library implementation first: Go `sync.Pool`/`sync.Map`, Java `java.util.concurrent` (ConcurrentHashMap, LongAdder), Rust `crossbeam`/`flume`, C++ folly/libcds.
- Validate with model checking or herd on the memory order, plus stress and soak (VERIFICATION GATE).

### 3. Thread pools with bounded queues
- Always bound the task queue; an unbounded queue is a memory bomb under burst. Set capacity so in-flight + queued is a stated bound; when full, apply backpressure (block producers) or shed load.
- Size the pool by workload (see QUANTITATIVE RULES): CPU-bound = physical cores; I/O-bound = cores × (wait + compute)/compute, measured.
- Never mix blocking-io tasks and CPU tasks in one shared pool — one blocking task in a full worker starves everyone. Use separate pools per work class.
- Deterministic shutdown: stop, drain/cancel, signal exit, join all workers. A scope that returns without joining its workers is a leak.

### 4. Cancellation propagation
- Every blocking wait takes a cancel token (context / CancellationToken / AbortSignal). Cancel = wake all waiters (close the channel, cancel the context), not a flag they must poll — a wait never wakes from a bare bool.
- Propagate failure outward: when a child fails, cancel its siblings (Go `errgroup.WithContext`) so nobody waits on a graph that already aborted.
- Cancel-in-defer on every scope so no goroutine, thread, or future leaks.

### 5. Structured concurrency
- Bind every task's lifetime to an enclosing scope: enter, spawn children, await all before returning; the scope cannot exit while a child still runs (Go `errgroup`, Rust `scoped_threads`, Kotlin `coroutineScope`, Python `asyncio.TaskGroup`).
- One root, one join-point per task graph. "Fire-and-forget `go func` that nobody joins and takes no context" is a leak, not a pattern.
- Propagate errors and cancellation downward; the group returns the first failing error and cancels the rest.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX. All that apply must be checked during a concurrency review.

1. **Data race** — read and write to the same memory on different threads with no happens-before edge. *DETECT:* `go test -race`, TSan (`-fsanitize=thread`), Rust Miri, JVM race-detector tooling, Python audit of shared globals; happens-before reasoning. *FIX:* mutex/atomic, or move the datum into a channel/actor; apply the ordering rules from systems-core-architect.

2. **Deadlock** — locks taken out of order, or a join blocked by a task that itself blocks on the join. *DETECT:* lock-order audit, `go vet`, thread dump on hang (`jstack`, `faulthandler.dump_traceback_later`), TSan/GCD deadlock reports. *FIX:* global lock order (PATTERNS section), hold at most one lock, `try_lock` + bounded backoff, or remove the locks by ownership transfer.

3. **Livelock** — threads actively retry but none progress (lock-release-then-retry collision). *DETECT:* cores burn while throughput stays flat; no task completes; monitors show no deadlock. *FIX:* exponential backoff with jitter, bounded retries, or park waiters on a queue instead of active retry.

4. **Starvation** — a thread/goroutine never gets a turn. *DETECT:* a task's completion time grows unboundedly despite load; scheduler/priority metrics show some waiters never served. *FIX:* FIFO/fair queues, fewer high-priority users, per-stream quotas, park instead of spin.

5. **Priority inversion** — low priority holds a resource a high-priority task needs, and a medium-priority task preempts the low one forever. *DETECT:* high-priority tasks take far too long; wait-time histograms; classic obscure systems bug (Mars Pathfinder). *FIX:* priority-inheritance or priority-ceiling mutex, or do not mix priority classes on one lock; use a real-time scheduler for hard-real-time expectations.

6. **False sharing** — two cores write independent fields that share one cache line, thrashing the coherence protocol. *DETECT:* perf `cache-misses`, throughput stops scaling with core count; TSan does NOT catch it (no race, just slowness). *FIX:* pad per-thread hot fields onto aligned 64/128-byte boundaries (alignas in C++, Rust, Java `@Contended`), shard counters, and place distinct hot indices on distinct lines.

7. **Sync-over-async deadlock** — a synchronous `.Wait()`/`.Result` blocks the only thread that must run the async task (single-thread executors, thread-local schedulers). *DETECT:* the app hangs only on a load that touches that path; the thread dump shows a sync wait blocked by the very scheduler that queues the task. *FIX:* async-await end-to-end, or `ConfigureAwait(false)`/detached execution so the coroutine runs on another thread; never sync-block across an async boundary.

8. **Goroutine/thread leak** — a worker waits forever on a channel/context/mutex that never fires and is never reclaimed. *DETECT:* `runtime.NumGoroutine`/thread count rises under soak; `go.uber.org/goleak`; OS thread count grows over time; a scoped-thread scope never returns. *FIX:* every task takes a context and selects on `ctx.Done()`; cancel-in-defer; the producer alone closes the channel; structured concurrency plus a bounded pool instead of per-event spawn.

## QUANTITATIVE RULES

Approximate numbers for current x86-64/ARM64 hardware — measure on the target machine; these are budgets, not absolutes.

- **Oversubscription, CPU-bound**: threads ≈ physical cores (not hyperthreads) for FP/SIMD-heavy work; beyond ~2× physical cores you get cache thrash and context-switch overhead, not speedup.
- **Oversubscription, I/O-bound**: threads ≈ physical cores × factor, where factor ≈ (avg_block + avg_compute)/avg_compute, measured (commonly 2-8x for network/DB waits), capped by scheduler overhead. When compute is tiny relative to waits, overlap yields many concurrent operations on few threads.
- **Spawn/coordination overhead**: goroutine ~1µs, `std::thread` ~10-50µs, Java `ForkJoinTask` ~10ns, async task ~few to tens of ns. Only parallelize work ≥ 5-10x that overhead.
- **Lock cost and contention threshold**: an uncontended mutex is ~20-40ns; a contended lock forces a context switch ~1-3µs (50-100x). If the same lock is acquired > ~1M/sec or shows > ~5% contention in a profile, redesign — shard, RwLock, atomic, or channel.
- **Atomic cost**: a cache-local atomic RMW is ~10-50ns; the dominant cost on a contended shared line is the cache-line bounce itself (µs+). Shard hot counters per-thread instead of one global atomic.
- **Channel/buffer sizing**: keep buffers bounded (a small power of two, or ~0-4 per worker). Prefer freshness → size 1; size up to smooth a downstream stage's processing batch; an unbuffered channel is strict per-message synchronization (correct but slow for pipelines). Never use an unbounded queue for production input — block producers (backpressure) instead.
- **False-sharing budget**: every hot per-thread write should own a clean cache line, not share a line with counters other threads update.

## VERIFICATION GATE

Concurrency correctness is a behavior claim, not a style claim. Nothing below is optional for code that touches this skill.

- **Race detector**: `go test -race` (Go), TSan `-fsanitize=thread,address,undefined` (C/C++), `cargo miri` for Rust unsafe, JVM race tooling where available. Zero findings on the changed path. Know the limit: TSan does not always catch lock-free memory-ordering errors — run the model check below for those.
- **Stress + soak**: run the concurrent path at sustained P90 and at 2x P0 for ≥ 30-60s with varied interleavings; soak ≥ 1h when verifying a leak-free design. Watch thread count and heap across the soak.
- **Deadlock detector**: collect thread dumps on a hang sweep (`faulthandler.dump_traceback_later`, `jstack`), and add a leak check (goleak, futures-leak assertion) to CI on every scoped/errgroup graph.
- **Before/after benchmark**: pin the environment (cores, input, frequency), warm ≥ 3 rounds, run ≥ 5, report median and p90. A concurrency change fails if median regresses > 5% or p90 grows beyond ~4x the median (queueing signature).
- **Model checking (where available)**: herd7 for C11 atomics when relaxing below `seq_cst`; TLC/LTL or a JMM/Rust memory-model tool for new lock-free structures. Any relaxation below `seq_cst`, or any new hand-rolled lock-free structure, requires this pass — "I think it is safe by construction" is not evidence. Map the rules through systems-core-architect's ordering guidance.

## REFERENCES

- The Go Memory Model — go.dev/ref/mem.
- JSR-133 / JLS section 17, "The Java Memory Model" — ordering and visibility rules for the JVM.
- C++ memory model — cppreference.com, `std::memory_order`; the C++ memory-model papers.
- Herlihy & Shavit, "The Art of Multiprocessor Programming" — canonical text on locks, lock-free structures, and transactional memory.
- Effective Go, concurrency chapter — go.dev/doc/effective_go — idiomatic goroutines and channels.
- Rust: the `Send`/`Sync` model, The Rust Book chapter 16; the `crossbeam` and `flume` crate docs.
- "Priority Inheritance Protocols: An Approach to Real-Time Synchronization" (Sha, Rajkumar, Lehoczky) — the priority-inversion fix.
- systems-core-architect — per-language memory models and atomic ordering rules.
