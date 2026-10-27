---
description: Analyze complexity and data-structure choice for a hot path before implementing
argument-hint: <module, function, or design to analyze>
---

Run `algorithms-and-data-structures` via `algorithm-specialist` (read-only):

1. Bound n and its growth; state the current time and space cost with `file:line` evidence.
2. Identify the dominant access pattern and the structure that matches it.
3. Name the invariant the algorithm maintains; give the trade-offs (readability, memory).
4. Attach the proof plan: worst-case test shapes, property tests for invariants, and a benchmark
   only when speed is the goal.
5. State explicitly when NOT to optimize (bounded inputs, clarity wins).
6. Implementation routes to `code-implementer`; measured production slowdowns to
   `performance-engineer`; query-level costs to `query-performance-engineer`.

Target: $ARGUMENTS
