---
description: Prove work with deterministic local evidence (tests, linters, types, benchmarks)
argument-hint: [scope or tests to run]
---

Apply Ozone Mode verification doctrine:
No claim of "done", "fixed", or "improved" without attached executable evidence:
1. Run local test suites (`npm test`, `pytest`, `cargo test`).
2. Run type check (`tsc --noEmit` or equivalent).
3. Run linter and format check (`eslint`, `biome`).
4. Output exact pass/fail logs and diff summaries.

Target: $ARGUMENTS
