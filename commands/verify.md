---
description: Prove work with deterministic local evidence (tests, linters, types, benchmarks)
argument-hint: [scope or tests to run]
---

Apply the verification doctrine (`verification-before-completion`):
No claim of "done", "fixed", or "improved" without attached executable evidence:
1. Run the smallest relevant check set first (targeted test file/module), then the full suite.
2. Run type check (`tsc --noEmit` or equivalent).
3. Run linter and format check (`eslint`, `biome`).
4. Output exact pass/fail logs and diff summaries; a new test must pass on two consecutive runs.
5. Failures are reported as limitations — never skipped, weakened, or suppressed to green; a
   claimed speedup needs before/after numbers.

Target: $ARGUMENTS
