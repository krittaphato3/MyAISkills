---
description: Deploy dual-track parallel subagents for simultaneous implementation and independent acceptance testing
argument-hint: <feature or bug specification>
---

Deploy Ozone Mode parallel test-and-develop framework for:
$ARGUMENTS

1. Define the specification and data contract (TypeScript types / FSM) first.
2. Fan out only for independent units — shared files or state serialize first. Fan-out multiplies
   token cost, so spend it on real parallelism (≤5 concurrent; `token-economy`).
3. In a single turn, emit concurrent Agent calls:
   - Worker A: `code-implementer` to write the business logic.
   - Worker B: `test-oracle` to write the independent test suite based on the spec.
4. Integrate both artifacts, run the local test runner (`npm test`, `pytest`, `cargo test`), and confirm green assertions.
5. Run `comment-sicko` to strip slop and verify boundary hygiene.
