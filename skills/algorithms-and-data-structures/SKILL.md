---
name: algorithms-and-data-structures
description: >-
  Reasons about algorithmic cost and structure choice in production code: complexity analysis,
  the working set of patterns (two pointers, sliding window, binary search, heaps, hashing,
  prefix sums, graph traversal, dynamic programming), invariants, and when NOT to optimize.
  Use when code will run on large or adversarial inputs, when a hot path looks quadratic, or
  when choosing between a list, map, set, heap, or tree. Measured profiling of a named
  slowdown routes to performance-profiler; database-query tuning to query-performance-engineer;
  interview-style puzzle solving is out of scope.
metadata:
  version: 1.0.0
  domain: fundamentals
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: code-implementer
---

# Algorithms and Data Structures

Algorithmic reasoning is a design-time tool, not an interview ritual. The failure this skill
prevents is shipping the first structure that works on 20 rows and dies on 200,000 — or spending
a day micro-optimizing a loop while the real cost is one extra database round trip per item.

## WHEN TO USE

- Writing an algorithm or hot path whose input can grow beyond today's data.
- Input can be adversarial (user-supplied size, crafted ordering, duplicates).
- A function does repeated lookups, nested scans over the same collection, or list membership
  checks inside loops.
- Choosing a container type: array, hash map, set, heap, tree, queue, adjacency list.
- A review comment says "this is O(n²)" and you need to decide whether that matters here.

## WHEN NOT TO USE

- n is small and bounded with no growth path — the simplest correct code wins; complexity
  theater is its own defect.
- A slowdown is measured in production — `performance-profiler` (numbers before theory).
- A specific SQL query or endpoint is slow — `query-performance-engineer`.
- The question is really about modeling state — `principle-model-the-domain`.

## DECISION TREE

```text
1. BOUND THE INPUT
   State n and its growth: static fixture, per request, per user, unbounded growth over time.
   Small and bounded → stop optimizing, keep the readable version. Unbounded → continue.

2. MEASURE COMPLEXITY IN THE UNITS THAT COST
   Time and space, in the units the system actually pays: comparisons, allocations, DB round
   trips, network calls, memory held across requests. A nested loop over in-memory rows may be
   cheaper than one N+1 query — count both.

3. PICK THE STRUCTURE BY ACCESS PATTERN
   lookup by key → hash map          ordered range / top-k → heap or sorted tree
   membership / dedupe → set         FIFO/LIFO scheduling → queue or stack
   contiguous-range queries → prefix sums   dependencies / cycles → graph + DFS/topo
   "best k of a stream" → bounded heap

4. WRITE THE INVARIANT BEFORE THE LOOP
   One sentence: what stays true each iteration (window holds a valid range, heap holds the k
   largest seen, visited set contains exactly the reachable set). Off-by-one and wrong-assumption
   bugs die here, not in review.

5. PROVE THE WORST CASE WITH A TEST
   Empty, single, sorted, reverse-sorted, all-duplicates, and one large input. For ordering
   invariants, a property test beats five examples.

6. OPTIMIZE CONSTANTS LAST
   Cache the cheap thing (allocation, parse, round trip) before tuning the loop. Re-measure
   after each change; keep only changes that survive the measurement (AGENTS.md §9).
```

## PATTERN CHEAT SHEET

| Pattern | Fits | Trigger phrase |
|---|---|---|
| Two pointers | Sorted pair/partition, in-place dedupe | "find two that sum to", "partition around" |
| Sliding window | Contiguous subarray/substring with a constraint | "longest run of", "at most k distinct" |
| Binary search | Monotonic predicate over a sorted or derivable range | "smallest value such that", "first element ≥" |
| Prefix sums | Repeated range queries over immutable data | "sum of a range, asked many times" |
| Heap | Streaming top-k, running median, merge k sorted | "keep the largest k", "merge N streams" |
| BFS | Shortest path, unweighted layers | "minimum number of steps" |
| DFS / topo sort | Reachability, dependency order, cycle detection | "build order", "is this circular" |
| Union-find | Incremental connectivity | "are these connected", "merge groups" |
| DP | Overlapping subproblems with optimal substructure | "minimum cost path with choices", memoize by state |
| Hashing | Membership, counting, grouping | "have we seen", "how many times" |

## FAILURE MODES & MITIGATIONS

1. **Accidental quadratic** — nested scans over the same collection, string concatenation in
   loops, list membership in a loop. *DETECT:* a loop inside a loop over the same unbounded data.
   *FIX:* hoist to a set/map; accumulate, then join.
2. **ORM N+1** — a query per item behind an innocent loop. *DETECT:* query count scales with rows.
   *FIX:* batch/join; this is a `query-performance-engineer` problem, not a loop trick.
3. **Wrong structure** — `list.index()` for key lookup, hash map where order is required at
   read time. *DETECT:* a comment explaining why iteration order "should be fine".
   *FIX:* choose the structure by read pattern. Never rely on incidental hash order.
4. **Recursion depth** — recursive traversal on deep input overflows the stack. *DETECT:*
   depth grows with user input. *FIX:* iterative form with an explicit stack.
5. **DP for a greedy problem** — overengineering a solver. *DETECT:* memo table for a problem with
   a provable local choice. *FIX:* simplest correct approach that meets measured needs.
6. **Optimization without measurement** — rewriting for speed with no before/after. *DETECT:* "this
   should be faster". *FIX:* benchmark or profile first; report the number or don't claim it.

## QUANTITATIVE RULES

- Any user-visible collection above ~10k elements needs an indexed structure for lookups.
- Nested loops over the same unbounded collection require a written justification (invariant or
  complexity note) in the PR body.
- State time and space complexity in the design or PR summary, not in code comments
  (`no-comments` still applies).
- Prefer cutting a round trip, allocation, or parse over micro-tuning a loop.
- A performance claim needs a before/after measurement; a complexity claim needs the derivation.

## VERIFICATION GATE

- [ ] Complexity stated for the added/changed algorithm, with n defined.
- [ ] Worst-case inputs covered by tests (empty, single, duplicates, large, adversarial order).
- [ ] The invariant is written down and asserted where it is subtle.
- [ ] Structure choice matches the dominant access pattern, named in the summary.
- [ ] Any speedup claim carries a measurement, or remains an estimate with assumptions.

## REFERENCES

- `performance-profiler` — measured, non-database slowdowns
- `query-performance-engineer` — query-level costs (N+1, missing indexes)
- `principle-foundational-thinking` — data structures before logic
- `principle-model-the-domain` — when the shape, not the cost, is wrong
- `testing-strategy` — property tests for invariants
