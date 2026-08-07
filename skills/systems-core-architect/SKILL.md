---
name: systems-core-architect
description: Use when writing non-fullstack systems languages like C++, Rust, Go, or backend Python.
version: 1.0.0
grade: G3
domain: languages
status: active
last-reviewed: 2026-08-06
owned-by-agent: code-implementer
supersedes: ""
---
# systems-core-architect

World-class guidance for performance-critical, memory-critical systems code in C++, Rust, Go, and backend Python. Covers language selection, per-language patterns, concurrency and memory models, quantitative performance budgets, and a verification gate that must pass before "done" is claimed.

## WHEN TO USE

Use this skill when the work is systems code in C++, Rust, Go, or backend Python, and at least one of these holds:

- The code sits on a hot path: parsing, serialization, networking I/O, compute kernels, compression, hashing, allocators, caches, or indexing.
- Latency or throughput is a stated requirement (P99 budgets, requests/sec, memory footprint limits).
- Memory management is manual or explicit and mistakes are expensive: native pointers, owned buffers, manual lifetimes, unsafe blocks.
- The task is concurrency or parallelism: threading, goroutines, async runtimes, lock-free or lock-based coordination.
- You are reviewing or fixing performance/UB/race bugs (see FAILURE MODES & MITIGATIONS).
- A fresh subagent inherits an existing C++/Rust/Go/Python codebase and must stay idiomatic and safe in it.

## WHEN NOT TO USE

- CRUD applications, CRUD web backends, dashboards, or glue layers where the bottleneck is a database or external service, not compute.
- Managed-runtime work that this skill does not own: JVM/Java/Kotlin (use java-jvm-expert), .NET/CLR, Node.js/V8, Ruby, PHP, frontend TypeScript.
- Business-logic-heavy Python/Django/FastAPI CRUD that is not I/O-bound-engineered for latency (the GIL and interpreter overhead dominate).
- Prototypes or throwaway scripts where developer velocity beats 2-3x throughput.
- Any task where the ecosystem decides the language for you (e.g., ML research in Python, browser code in JS) — then apply only the performance rules, not the language choice.
- Premature optimization: no measured hot path, no profile, no requirement. If profiling does not implicate the code, do not hand-tune it.

## DECISION TREE

### 1. Language selection

Ask three questions in order. Answer is a weighted score, not a taste preference.

- **Memory safety risk of the failure mode** — is a memory bug (use-after-free, buffer overflow, data race) catastrophic for this product? Yes → prefer Rust; then Go; then C++ with strict review. No → any language works.
- **Required control** — do you need explicit layout, no GC pauses, custom allocators, ABI interop with existing C/C++ libs, or deterministic destruction? Yes → C++ or Rust. GC pauses unacceptable → not Go for the hot path.
- **Ecosystem/team reality** — existing codebase language, available libraries, hiring pool, build times, deployment target.

Rules of thumb:

- **Rust** when safety + speed + concurrency are all required, and the team can absorb the borrow checker. Default for new native projects.
- **C++** when you must interop with existing C/C++ code, need battle-tested ecosystem (SIMD, GPU, game engines, HPC), or GC/borrower-free style with manual control is already established. You inherit all UB risks.
- **Go** when you want safe-by-default, fast builds, trivial deployment, and goroutine-based concurrency, and can tolerate GC + ~2-5x slower raw CPU loops than C++/Rust.
- **Backend Python** when the Python ecosystem wins (ML, data science, web frameworks) and the hot path can be pushed into C (numpy, asyncio I/O, C extensions). Never for latency-critical inner loops in pure Python.

### 2. When to drop to unsafe/raw

- **Rust `unsafe`**: only after a safe alternative is proven insufficient by profile, not by intuition. Preconditions before writing any `unsafe` block: (a) invariant documented inline, (b) checked in a SAFETY comment, (c) validated by miri + tests, (d) isolated to the smallest function possible. Never spread `unsafe` across a module.
- **C++ raw pointers/`new`**: treat raw `new`/`delete` as a code smell. Prefer `std::unique_ptr`, `std::shared_ptr`, `std::span`, references. Raw pointers are acceptable only for non-owning observation and must be lifetime-reviewed.
- **Go `unsafe`/`cgo`**: only for FFI or layout-critical interop; `unsafe.Pointer` casts must be reviewed line-by-line; keep cgo calls off the hot path (cgo transition is ~50-100ns and triggers a GC stack-copy handshake))
- **Python C extensions**: only when profile shows the interpreter loop is the cost. Prefer numpy/Cython over hand-written CPython C API.

### 3. When to parallelize vs keep sequential

Run this check before spawning anything:

- Compute the serial fraction s from profiling. Amdahl ceiling = 1/s. If s > 0.2, parallel speedup caps at 5x regardless of cores — fix the serial part first.
- Per-task parallel overhead must be < 10% of the work. If a task takes < 2-5x the spawn cost (goroutine ~1µs, std::thread ~50µs, Python ProcessPool ~ms), keep it sequential.
- Only parallelize when there is (a) embarrassingly parallel work, or (b) a measured contention-free hot loop.
- Prefer structured concurrency: `errgroup` (Go), `std::jthread`/scoped threads (C++), scoped `std::thread::scope` (C++20), Python `asyncio.gather` — so no goroutine/thread can outlive its scope without explicit handling.

## PATTERNS

### C++

- **RAII**: acquire resources in constructors, release in destructors (mutexes, file handles, GPU buffers, sockets). Trade-off: hidden destructor costs and non-obvious lifetime ends; keep destructors cheap and noexcept.
- **Move semantics**: `std::move` transfers owned buffers, avoids copies on return and container growth. Trade-off: move-only types become non-copyable; moved-from objects must be valid-but-unspecified. Never `return std::move(x)` on a local — NRVO already elides.
- **Value vs reference**: pass small types (`<= 2-3 words`) by value, larger by `const&`; return by value (guaranteed elision). Trade-off: by-value copies cost memory traffic; by-reference risks aliasing/lifetime bugs. Use `std::span` for non-owning contiguous ranges.
- **noexcept**: mark move ctors, swap, and destructors noexcept — else `std::vector` reallocation will copy instead of move (3-10x slower on large elements). Trade-off: throwing from a noexcept function terminates; only mark functions that provably don't throw.
- **pimpl (pointer-to-implementation)**: hide private members behind a unique_ptr to an impl struct. Trade-off: ABI stability and compile-time isolation vs one heap allocation + one indirection per object. Never for small hot-path value types.

### Rust

- **Ownership/borrowing**: one owner per value; borrows are `&` (shared) or `&mut` (exclusive). Trade-off: the compiler enforces correctness at compile time, but fights you on graph/self-referential data — use indices/arenas instead of self-referential structs.
- **Interior mutability**: `Cell`/`RefCell` (single-thread), `Mutex`/`RwLock`/atomics (multi-thread). Trade-off: `RefCell` panics on double-borrow (panic = bug); prefer `Cell` for `Copy` types; prefer atomics over `Mutex` when the critical section is one word.
- **Send/Sync**: `Send` = may move across threads; `Sync` = may be shared by reference. Trade-off: auto-derived, but wrapper types like `Rc` are not `Send` — use `Arc`; if you hand-implement `unsafe impl Send`, you are declaring the type is thread-safe: prove it in a SAFETY comment.
- **`unsafe` review checklist** (run every item before merging any unsafe code):
  1. **Null deref**: is the pointer guaranteed non-null? Check all `unwrap_unchecked`, raw derefs.
  2. **Aliasing**: does an exclusive (`*mut`) pointer alias a shared (`*const`) pointer or an existing `&mut`? Violations = UB, even if tests pass.
  3. **Lifetime escapes**: can the produced reference outlive the backing allocation? Verify with `cargo miri`.
  4. **FFI**: is the C ABI signature correct (`extern "C"`, correct repr/C layout)? Does the callee retain the pointer? Who frees?

### Go

- **Goroutine lifecycle**: every goroutine must have a known exit path — a channel that closes, a context that cancels, or a bounded worker loop. Orphan goroutines leak stacks + block GC. Prefer worker pools with `errgroup` over fire-and-forget `go func`.
- **Channels vs mutex**: channels for ownership transfer, coordination, and pipelines (idiomatic Go); mutexes for protecting shared state invariants. Trade-off: channels are slower per-op and opaque; mutexes are faster but easy to misuse. When in doubt, protect state with a mutex and communicate ownership with channels.
- **Context cancellation**: every blocking op that can wait (network, DB, `select`) must take a `context.Context` and honor `ctx.Done()`. Never store contexts in structs; pass as first parameter. Cancel in `defer` to stop goroutine leaks.
- **errgroup**: `errgroup.Group` or `errgroup.WithContext(ctx)` for structured fan-out; cancels the context on first error and waits for all goroutines. Trade-off: it waits for all before returning — use `SetLimit(n)` to bound concurrency.

### Backend Python

- **GIL reality**: only one thread executes bytecode at a time. The GIL is released during blocking I/O and by many C extensions (numpy releases it on big ops). Pure-Python CPU loops are serialized by the GIL — threads do not speed those up.
- **asyncio vs threads vs multiprocessing**: asyncio for many concurrent I/O ops with low per-connection overhead; threads for I/O with blocking third-party libs that don't support async; multiprocessing for CPU-bound work that must use all cores (each process gets its own GIL). Trade-off: asyncio is fastest for I/O-bound but rewrites code as coroutines; multiprocessing needs picklable payloads and has IPC cost.
- **uvloop**: drop-in `asyncio` event-loop replacement, ~2x+ throughput on I/O-bound loops. Use in production web workers when CPU-bound work is small.
- **Zero-copy buffers**: use `memoryview`/the buffer protocol (`struct.pack_into`, `os.readv`, `socket.sendmsg`, `io.BytesIO`) to avoid `bytes` copies; prefer `bytearray` reuse over repeated `b"".join`. Watch out: slicing a `memoryview` avoids copies but retains the parent — release it to free memory.

## FAILURE MODES & MITIGATIONS

Each entry lists detection first, then fix. ≥10 required; all must be checked during review of systems code.

1. **Undefined behavior (C/C++)** — signed overflow, OOB, strict-aliasing, shift-count errors. *Detection:* UBSan (`-fsanitize=undefined`), MSan for uninitialized reads; static analyzers (clang-tidy). *Fix:* compile with `-Wall -Wextra -Wconversion -Wstrict-aliasing`; prefer `std::span` bounds checks; enable sanitizers in CI.
2. **Data race** — concurrent read/write to the same memory without synchronization. *Detection:* TSan (`-fsanitize=thread`), `go test -race`, Rust compiler (compile error), Python via `faulthandler` + audit of shared globals. *Fix:* atomics with correct ordering, mutex, or move the data into a channel/message.
3. **Deadlock** — two or more locks acquired in inconsistent order. *Detection:* lock-order audit; TSan reports deadlocks; Go runtime detects all-goroutines-blocked; Python `faulthandler.dump_traceback_later` on hang. *Fix:* impose a global lock order; hold at most one lock at a time; use `try_lock`/timeout and retry; prefer `errgroup`/single-owner patterns.
4. **Memory leak** — allocated memory never freed; unbounded growth. *Detection:* ASan leak sanitizer (`-fsanitize=address`), `valgrind --leak-check=full`, `go test` with `runtime.MemStats` deltas, Python `tracemalloc`. *Fix:* RAII, `unique_ptr`, `defer close`/`defer cancel`, worker-pool cleanup, arena allocation.
5. **Stack overflow** — unbounded recursion or oversized stack frames. *Detection:* ASan (`stack-overflow`), crash with SIGSEGV on native; Python `RecursionError`. *Fix:* convert to iteration, raise the stack size only as a last resort, bound recursion depth explicitly.
6. **False sharing** — independent fields on the same cache line written by different cores, thrashing the coherence protocol. *Detection:* perf with `cache-misses`/`cacheline` events; throughput scales worse than cores; TSan does NOT catch this. *Fix:* pad hot per-thread structs to a cache line (64 bytes typical, alignas(64)); ensure distinct indices have distinct lines; shard counters.
7. **Allocator fragmentation** — many allocations of varied sizes leave unusable free holes; RSS grows beyond live data. *Detection:* jemalloc stats (`mallctl`), `mallinfo`, RSS vs live-size diff over time, ASan's allocator report. *Fix:* pool/arena allocators for fixed-size hot objects; slab re-use; batch `std::vector` reserve; avoid interleaving many size classes on one thread.
8. **Slice/iterator invalidation (C++)** — vector reallocation or element insertion invalidates references/iterators; use-after-realloc. *Detection:* ASan, valgrind, iterator debugging (`_GLIBCXX_DEBUG`, `_LIBCPP_DEBUG`). *Fix:* `reserve()` before growth, use indices into stable storage, or store by value in `deque`/linked containers only when profiling demands.
9. **Go slice aliasing** — two slices share a backing array; append on one overwrites the other's view. *Detection:* race detector won't catch it (no race, wrong data); unit tests on aliasing; vet. *Fix:* `slices.Clone` before storing a sub-slice, cap copies (`dst := make([]T, n); copy(dst, src)`).
10. **Use-after-free / use-after-return (C/C++)** — pointer to freed or returned-from stack memory. *Detection:* ASan (both), `-fsanitize-address-use-after-scope`. *Fix:* ownership discipline (unique_ptr), never return references to locals, `std::shared_ptr` only when shared ownership is real.
11. **Integer overflow/truncation** — sizes, indices, counters wrapping or narrowing. *Detection:* UBSan `-fsanitize=integer`/`-fsanitize=unsigned-integer-overflow`, `-Wconversion`, Python is immune (arbitrary precision). *Fix:* use size_t/ptrdiff_t consistently, check `n > max`, saturating arithmetic, static_cast only after range check.
12. **Goroutine leak** — goroutines blocked forever on a channel/context that never fires. *Detection:* `runtime.NumGoroutine()` over time, `go.uber.org/goleak` in tests. *Fix:* every goroutine takes a context and selects on `ctx.Done()`; use `errgroup.WithContext`; close channels in the producer only; use buffered channels for one-shot handoffs.
13. **Lock contention** — threads queue on one mutex, serializing a hot path. *Detection:* Go `pprof mutex` profile, `perf sched`, thread-stall sampling; throughput flat after N cores. *Fix:* shard locks per key, use RWLock for read-mostly, atomics for single-word state, or move work out of the critical section.
14. **Memory-ordering bugs (relaxed atomics)** — wrong orderings that pass TSan but misbehave on real hardware (loads reordered). *Detection:* TSan + formal validation (herd7/C11 memory model), stress tests on ARM. *Fix:* use acquire/release or seq_cst until profiling justifies weaker orderings; document ordering invariants.

## QUANTITATIVE RULES

Approximate numbers for current mainstream x86-64/ARM64 hardware — measure on the target machine; these are budgets, not absolutes.

- **Cache-latency ladder**: L1 ~1ns (~4 cycles), L2 ~5ns (~12 cycles), L3 ~15ns (~40 cycles), RAM ~100ns (~300 cycles), random SSD ~50-150µs, disk (spinning) ~10ms. Each jump is ~3-7x. A RAM miss costs ~300 cycles — hide it with prefetch/batching or eliminate it with locality.
- **Branch mispredict** ~20 cycles; a mispredicting branch in a 1ns loop triples its cost. Replace hot branches with branchless arithmetic, lookup tables, or sorting data by predictability.
- **P99 > 4x P50 ⇒ queueing** — tail latency ballooning beyond 4x the median is a queueing signature (single worker, lock convoy, GC pause, OS run-queue), not slow code. Fix by removing contention or adding concurrency; do not micro-optimize the median.
- **Allocation in a hot loop**: malloc/free is ~20-100ns (plus page-fault spikes), often 10-50x a cache hit. Budget: if a loop iterates < ~100ns/iteration, allocations dominate — hoist them, use an arena/pool, or reuse a buffer. Never allocate inside an inner loop without proof.
- **Lock-contention threshold**: an uncontended mutex lock is ~20ns; a contended lock costs a context switch ~1-2µs (50-100x). If the same lock is acquired > ~1M times/sec or shows > 5% contention in profiles, redesign (shard, RWLock, atomics, or lock-free).
- **Syscall** ~0.5-1µs; a blocking syscall in a hot loop is a design error unless amortized by batching (io_uring, readv).
- **Oversubscription**: for CPU-bound work use N threads = physical cores (not hyperthreads) for heavy SIMD/FP; 1.5-2x physical cores for mixed I/O+CPU. Beyond 2x physical cores on CPU-bound work you get thrashes, not speedup. For Python, one process per physical core for CPU-bound multiprocessing.
- **Go specific**: goroutine spawn ~1µs (vs std::thread ~50µs); channel op ~30-100ns; runtime scales fine to 100k goroutines but scheduler sees diminishing returns past ~10k runnable.
- **Rust/C++ overhead rules of thumb**: `std::function`/`Box<dyn>` virtual call ~2-5ns; a `noexcept` move vs copy is the difference between 1 and 3+ copies on growth. Hot structs: keep them ≤ 64 bytes to fit one cache line; access arrays forward for prefetch.

## VERIFICATION GATE

Nothing below is optional. A task is "done" only when the relevant items pass.

**Sanitizers / correctness (must all pass before perf work):**

- C/C++: `-fsanitize=address,undefined` on all tests; TSan on concurrent tests; run with `-O1 -g`. `valgrind --leak-check=full --error-exitcode=1` for leaks and uninitialized reads.
- Rust: `cargo test` + `cargo miri test` for any unsafe code; `cargo clippy -D warnings`.
- Go: `go test -race ./...` on every package touching concurrency; `go vet`; `go.uber.org/goleak.VerifyTestMain` for goroutine leaks.
- Python: `python -X dev` (debug checks), `faulthandler` enabled, `tracemalloc` for leak checks in long-running services.

**Before/after benchmark protocol (required for any optimization claim):**

1. Pin the environment: same machine, CPU governor pinned (disable turbo/frequency scaling), no other load, fixed input data, process pinned to fixed cores.
2. Warm up: run the benchmark until steady state (typically ≥ 3 warmup rounds) before recording.
3. Run ≥ 5 measured rounds; report median and p90 (mean hides tail; single runs are not evidence).
4. Compare apples-to-apples: same compiler flags, same input distribution, same metric.
5. Record the exact command and environment in the change note (compiler version, flags, CPU model).
6. A regression is real only if it reproduces across ≥ 3 rounds and the p90 moves; otherwise it is noise.

**Done criteria:**

- All sanitizers/race checks above pass with zero findings on the affected code path.
- Before/after benchmark recorded: median + p90, ≥ 5 runs, pinned env. If the task is a bug fix, the fix must not regress throughput on the hot path (> 5% median regression fails the gate).
- Leak checks pass for the new allocation/ownership code (ASan leak run or tracemalloc baseline-vs-after).
- `unsafe` code (Rust) and raw-pointer code (C++) has line-by-line review against the checklist in PATTERNS → Rust.

## REFERENCES

- cppreference.com — C++ standard library and language reference.
- The Rust Book (doc.rust-lang.org/book) — ownership, borrowing, lifetimes; The Rustonomicon — the `unsafe` contract and UB rules.
- Effective Go (go.dev/doc/effective_go) — idiomatic concurrency; The Go Memory Model (go.dev/ref/mem) — ordering guarantees; go.dev/blog/race-detector.
- perf(1) man page — profiling, cache-miss events, sched analysis.
- "Latency Numbers Every Programmer Should Know" (Jeff Dean / colin-scott.github.io) — the cache/syscall latency ladder.
- Valgrind docs; LLVM SanitizerCoverage/AddressSanitizer docs; `cargo miri` docs (rust-lang.github.io/miri).
- errgroup docs (pkg.go.dev/golang.org/x/sync/errgroup); goleak docs (pkg.go.dev/go.uber.org/goleak).
- uvloop docs (uvloop.readthedocs.io); CPython buffer protocol docs for zero-copy I/O.
