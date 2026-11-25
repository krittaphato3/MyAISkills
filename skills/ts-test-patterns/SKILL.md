---
name: ts-test-patterns
description: "Provides pragmatic Vitest, Supertest/Fastify API contract, and deterministic Playwright E2E patterns without brittle mocks. Use when writing or fixing TypeScript unit and integration tests."
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: test-engineer
---

# TypeScript Test Patterns

Fast, non-flaky test patterns for modern TypeScript full-stack apps so Fast Lane verification (`vitest run <file> && tsc --noEmit`) proves real behavior without brittle mock theater.

## WHEN TO USE

- Writing new Vitest unit/component tests, backend route integration tests, or Playwright E2E specs.
- Fixing a flaky timer, async state, or ESM mock failure in TypeScript tests.

## WHEN NOT TO USE

- High-level test pyramid / mutation testing strategy — `testing-strategy` / `mutation-testing`.
- Exploratory manual browser QA — `webapp-qa`.

## DECISION TREE

```text
1. CHOOSE THE CHEAPEST REAL BOUNDARY
   - Pure domain logic / state reducer -> Vitest in-memory (0 mocks).
   - Express/Fastify/Nest route -> `.inject()` or Supertest with in-memory DB/test fixture (mock only external HTTP/LLM providers).
   - React UI state -> Testing Library (`userEvent` + accessible `getByRole` / `getByLabelText`, never CSS classes).

2. MOCKING & TIMER HYGIENE
   - Always `vi.restoreAllMocks()` / `vi.useRealTimers()` in `afterEach` so state never leaks across files.
   - Prefer `await vi.advanceTimersByTimeAsync(ms)` when testing debounces/timeouts under fake timers.
   - Never mock the module under test or replace assertions with `expect(fn).toHaveBeenCalled()` alone when output state matters.

3. PLAYWRIGHT DETERMINISM
   - Ban `waitForTimeout(N)`. Wait on auto-retrying assertions (`expect(locator).toBeVisible()`) or explicit network responses (`waitForResponse`).
```

## FAILURE MODES & MITIGATIONS

1. **Mock Leaks Across Test Files** — DETECT: test passes alone, fails in full suite. FIX: enforce `afterEach(() => { vi.restoreAllMocks(); vi.useRealTimers(); })`.
2. **Async Deadlock with Fake Timers** — DETECT: `vi.runAllTimers()` hangs on Promise+setTimeout loops. FIX: use `vi.advanceTimersByTimeAsync(...)`.
3. **Brittle Selector Rot** — DETECT: `locator('.css-1a2b3c > div:nth-child(2)')`. FIX: query by semantic `getByRole` / `getByTestId`.

## VERIFICATION GATE

- [ ] Target test file passes twice in isolation and alongside caller tests (`vitest run <file> && tsc --noEmit`).
- [ ] Zero `waitForTimeout`, zero `.skip`, zero weakened assertions.

## REFERENCES

- `test-driven-development` — RED-GREEN-REFACTOR discipline
- `testing-strategy` — test pyramid and flake triage
- `typescript-best-practices` — strict typed test fixtures without `as any`
