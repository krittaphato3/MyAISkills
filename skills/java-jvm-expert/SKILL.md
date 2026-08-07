---
name: java-jvm-expert
description: Use when writing or refactoring Java code, JVM applications, or backend services.
version: 1.0.0
grade: G2
domain: languages
status: active
last-reviewed: 2026-08-06
owned-by-agent: code-implementer
---

# Java / JVM Expert (G2)

## WHEN TO USE
Use when the target is a modern JVM backend service — Spring Boot, Micronaut, Quarkus, Vert.x, or
any long-running server process where **latency, throughput, or GC behavior** materially affects the
outcome.

Apply this skill whenever you are:
- Building or diagnosing **high-concurrency** code: many threads / virtual threads, request
  fan-out, reactive pipelines, shared thread pools, event loops.
- Writing **GC- / performance-sensitive** paths: hot request handlers, per-request object graphs,
  large-stream transformation, batch writers operating under a hard memory ceiling.
- Making a design input out of heap sizing, collector selection, or allocation-sites rather than
  blindly accepting JVM defaults.
- Reading **GC logs, JFR recordings, flame graphs, or heap dumps** to explain a production incident.

Use when the question is how the **JVM reaches correctness under load** — not just whether the code
compiles.

## WHEN NOT TO USE
- **Non-JVM scripts / languages**: Python, Ruby, Node, Go, Scala-Native. Different runtime, wrong
  flags, wrong profilers; this skill's guidance is inapplicable.
- **GraalVM native-image** work: the goal is AOT, closed-world, tiny-footprint startup. GC there is
  SubstrateVM/serial, and the JFR/async-profiler workflow below does not transfer. Route to the AOT
  specialist.
- **CRUD-only services on a managed platform** (Spring Boot + JPA or a cloud data plane) where the
  platform's JVM tuning already covers the case. This skill only adds false rigor there.
- Rapid prototypes / one-off scripts where profiling is premature optimization.
- Pure library API questions with no JVM-semantics reasoning involved.

## DECISION TREE
1. **Is the JVM misbehaving, or the code?** Profile before reaming the GC. If the flame graph shows
   a CPU hotspot that is algorithmic or allocation work, the bottleneck is the code, not the collector.
2. **Heap sizing** — start here; everything downstream depends on it:
   - Set `-Xms=-Xmx` (start equal to max) to suppress resizing pauses and bound the awarded heap.
   - Begin at `-Xmx ≈ 4×` the warmed live-set. Measure live-set from `jmap -histo:live` after a soak.
   - Too-small `-Xmx` → OOM thrash and Fatal Error GC loops.
   - Too-large `-Xmx` → long pauses because the old-gen cache is rarely reclaimed.
3. **Choose a collector** by heap scale:
   - **G1GC** (default): best for mid heaps (~1–16 GB) and throughput-dominated servers. Tune
     `-XX:MaxGCPauseMillis`, `-XX:G1NewSizePercent`, `-XX:InitiatingHeapOccupancyPercent`.
   - **ZGC / Shenandoah**: for heaps ≥16 GB or sub-millisecond / low-latency tails. ZGC never
     stops-the-world but pays CPU for remapping. Do not use ZGC below ~4 GB.
   - **SerialGC**: single-CPU tiny JVMs, serverless warm starts, CDS/bootstrap runs. Not for
     concurrent production servers.
4. **Reduce allocation at source**, once the collector is fixed:
   - Locate hot sites with async-profiler `alloc` mode or `jmap -histo:live`.
   - Apply primitive streams, buffer reuse, avoid autoboxing (an `Integer` _per loop iteration_).
   - Replace reflection / instanceof chains with pattern matching + sealed types.
   - Only when the profiler proves GC/malloc dominating, consider object pooling — always weigh pool
     cache-misses and pool-lock pressure against the saving.
5. **Platform limits**: honor cgroup/container caps (`-XX:+UseContainerSupport`); bound
   `-XX:MaxDirectMemorySize`, `-XX:MaxMetaspaceSize`, `-XX:ReservedCodeCacheSize`. The JVM can commit
   more than your container limit if you size flags to the host instead of the cgroup.

### Profile vs reason
- **Profile** when the GC log shows a trend (young-gen churn, promotion spikes) or when a flame graph
  exposes a dominant hotspot.
- **Reason** when the symptom maps to a known class: OOM from `-Xmx` too small, starvation from an
  under-provisioned pool, leak from an unclosed classloader. Never profile an overcapacity / sizing
  problem; fix the flag first, then profile what remains.

## PATTERNS
### Modern Java (17 / 21)
- **Records**: immutable value carriers — `record Point(int x, int y) {}` — compact
  `equals`/`hashCode`/`toString` and constructor validation. Records are still heap-allocated; they
  reduce ceremony, not allocation.
- **Pattern matching for switch** (17 final) over records/sealed types, plus record deconstruction,
  replaces the instanceof tower. Pair with `sealed` types for compiler-checked exhaustiveness instead
  of runtime `ClassCastException` / default fallthrough.
- **Sealed types**: `sealed interface Shape permits Circle, Square`. A missing case becomes a compile
  error instead of a runtime miss.
- **Virtual threads** (JDK 21, `Thread.ofVirtual().start(...)`): scale I/O-bound concurrency to
  ~1e6 threads; pair with structured concurrency (`StructuredTaskScope`) for guaranteed cleanup. Do
  not use them for CPU-bound work — they still serialize on carrier threads; use a bounded thread
  pool for compute.

### Executor discipline
- Always bound your pool — never `newFixedThreadPool(cap)` with unbounded work. Use
  `ThreadPoolExecutor(core, max, ...workQueue, handler)`.
- Choose a backing queue explicitly (`ArrayBlockingQueue(cap)`) and a rejection policy:
  - `CallerRuns` — natural backpressure; preferred by default.
  - `Abort` — throws `RejectedExecutionException`; can drop work if unhandled.
  - `Discard` / `DiscardOldest` — silent loss; last resort.
- Lifecycle: `awaitTermination(timeout, unit)` then `shutdownNow()`; attach error callbacks to
  `CompletableFuture`s before they're exposed, never swallow failures.

### Avoiding allocation in hot loops
- **Escape analysis (EA)**: keep hot-loop locals non-escaping (no return/store, no capture) so the
  JIT can on-stack-allocate them. A manual pool that keeps objects escaping defeats EA.
- **Primitive streams**: prefer `int[]` / `IntStream` over boxing; a boxed `Integer` per element can
  cost 2–5× allocation in practice.
- **Object-pooling trade-off**: a pool only wins when allocation volume is huge **and** entries are
  long-lived/reused **and** the pool's own lock is not the bottleneck. For immutable values prefer
  ephemeral creation on the EA-inlinable path unless a microbenchmark proves pooling wins.

## FAILURE MODES & MITIGATIONS
Each entry is DETECT + FIX.

1. **GC pauses (STW)** — DETECT: `-Xlog:gc*` Pause(Duration) lines, JFR GC-pause events, tail-latency
   cliffs. FIX: cap young-gen to bound per-pause (`-XX:G1NewSizePercent`), pick ZGC for sub-ms, lower
   `-Xmx`, or fix the actual allocation root that drives each pause.

2. **OutOfMemoryError** — DETECT: `-XX:+HeapDumpOnOutOfMemoryError` yields a dump; `jmap -dump:live`
   on demand; MAT Leak-Suspects report. FIX: kill the leak (ever-growing `ArrayList`, unclosed
   `ScheduledExecutor`, over-retained `ThreadLocal`); resize the heap or pool the class.

3. **Thread starvation** — DETECT: all pool threads `WAITING`/`BLOCKED` on one lock, `jcmd
   Thread.print` blocked monitors, request timeouts. FIX: right-size the bounded pool, root-cause the
   blocking path (lock or blocking I/O), or virtual-thread / async the I/O.

4. **Classloader leaks** — DETECT: hot-reloads grow Metaspace; MAT shows a classloader pinned by a
   `static` field or a static `Map`. FIX: don't store the loader globally, `close()` `URLClassLoader`s,
   use `-XX:+TraceClassLoading` to see what keeps it alive.

5. **CPU spin / busy-wait** — DETECT: 100% CPU with a hot `Thread.sleep(0)` or polling loop in the
   flame graph; GC idle but CPU pegged. FIX: replace busy-poll with a `Condition`/`notify` or a
   `Semaphore`; cap any residual poll loop.

6. **Metaspace growth** — DETECT: `-Xlog:gc+metaspace=debug`, `jcmd VM.metaspace`; metaspace trending
   up on a long-running app. FIX: remove the dynamic class genesis (proxies, bytecode gen,
   `String.intern` at load), set `-XX:MaxMetaspaceSize`, prune generators and executors.

7. **`-Xlog:gc` as the diagnostic backbone** — always enable `-Xlog:gc*=debug:file=gc.log` for prod
   incident spills. Read pause:young vs promotion vs to-space-exhausted phases; the highest STW
   segment is the one to fix first.

8. **Allocation pressure** — DETECT: promotion stats, `jmap -histo:live` big blocks, retained-vs-
   shallow divergence. FIX: collapse the top allocation site (see PATTERNS), retune tenuring if
   premature promotion showers tenured gen.

9. **Synchronization overhead / lock convoy** — DETECT: a `synchronized`/lock hotspot in the flame
   graph, `jcmd Thread.print` monitor contention. FIX: narrow the lock scope, a `ReadWriteLock`/
   `LongAdder`/striping, or drop the lock with immutable data.

## VERIFICATION GATE
Run before claiming "optimized".

1. **JFR recording**
   - `jfr start --name app --duration 90s --filename app.jfr` on the running JVM.
   - Inspect: `jfr view gc` and `jfr print --events jdk.GC*,jdk.JavaMonitorEnter` for pauses and
     contention.
2. **async-profiler flame graphs**
   - `./profiler.sh -d 30 -e cpu -o flamegraph <pid>` for CPU; `-e alloc` for allocation stacks.
   - Identify the dominant leaf and its caller stack; link each flame to a GC event if GC-heavy.
3. **JMH microbenchmark** — template:
   ```java
   @Benchmark
   @Warmup(iterations = 5, time = 1)
   @Measurement(iterations = 10, time = 1)
   @Fork(3)
   public void hotLoop() { ... }
   ```
   - Report ops/s as a median across forks, never a single best run.
   - Use `-prof gc` to separate allocation from time; state the benchmark's input/state explicitly.
4. **Heap dump analysis**
   - `-XX:+HeapDumpOnOutOfMemoryError` writes on crash; MAT "Leak Suspects" finds the retainer.
   - On-demand: `jcmd <pid> GC.heap_dump /tmp/app.hprof` then MAT or `jhat`.
   - Take `jmap -histo:live` before and after for a deltas view.
5. **Before/after metrics** — record p50/p95/p99 latency, GC pause percentile, promotion, alloc MB/s,
   and `-Xmx` used, under the same load, cgroup, and pinning.
   - **Done gate**: accept a change only when p99 and GC pause both improve measurably _with no
     alloc/s regression_; otherwise revert or re-baseline.

## REFERENCES
- OpenJDK GC Tuning Guide (G1/Parallel/CMS), `https://docs.oracle.com/en/java/javase/.../garbage-collection`.
- JEP 395 (records, 16) — `https://openjdk.org/jeps/395`.
- JEP 409 (sealed classes, 17) — `https://docs.oracle.com/en/java/javase/.../jep-409`.
- JEP 406 (pattern matching for switch) — `https://openjdk.org/jeps/406`.
- JEP 444 (virtual threads, 21) — `https://openjdk.org/jeps/444`.
- JEP 453 (structured concurrency) — `https://openjdk.org/jeps/453`.
- OpenJDK JMH docs — `https://github.com/openjdk/jmh` and the JMH samples suite.
- async-profiler README — `https://github.com/async-profiler`.
- `jmap`/`jfr`/`jcmd` man pages in the official JDK tool docs.