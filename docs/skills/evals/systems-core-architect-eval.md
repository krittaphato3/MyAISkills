# systems-core-architect — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Write a high-throughput C++17 packet parser for a hot networking path with a 2ms P99 budget."
2. "Fix a use-after-free and an out-of-bounds write found in this Rust crate's unsafe decoder."
3. "Refactor this goroutine pool in Go; it leaks threads and the race detector flags a data race on the work counter."
4. "Review whether this Go service is CPU-bound or memory-bound and whether adding 16 cores actually scales compute."
5. "Pick a language (C++/Rust/Go/Python) for a performance-critical indexing engine with sub-millisecond indexing on 24 cores."

Not fire (3):
6. "Add a CRUD REST endpoint to this Django backend that mostly does DB lookups."
7. "Design a data model and ORM schema for a small user-management app."
8. "Write a JavaScript frontend component for a settings panel."

## 2. Quality rubric (1-5)
(a) decision tree covers stated branches: 5 — language selection, unsafe drop, parallelize-vs-sequential each with explicit guard conditions.
(b) every failure mode has detection + mitigation: 5 — all 14 failure modes carry a concrete detector (sanitizer/vet/miri) and a fix.
(c) quantitative rules are numbers not adjectives: 5 — ns/µs latencies, cycles, thread budgets, contention %.
(d) verification gate is executable: 5 — named commands (`-fsanitize`, `go test -race`, `cargo miri`), ≥5-run benchmark protocol.
(e) references authoritative: 4 — cppreference, Rust Book, Effective Go, perf(1) all authoritative; Latency Numbers is a classic but aged.
(f) no contradictions: 5 — explicit boundary to java-jvm-expert, query-performance-engineer implied; consistent with Phase-1 doctrine.

## 3. Reference task
A team must index 20M documents, 60% writes on a hot path, with a 5ms P99 index-latency SLO on 8 physical cores. Recommend a language, identify the parallelization strategy with Amdahl-bound, and give a verification gate that includes a pinned before/after benchmark. The skill must respond with a weighted language choice, a serial-fraction check, thread oversubscription guidance, and concrete sanitizer/race/leak commands.
