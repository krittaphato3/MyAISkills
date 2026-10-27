---
name: testing-strategy
description: >-
  Chooses what to test and how, layer by layer: behavior lists, test sizes, builders, property-based
  tests, mutation checks, fuzzing parsers, contract tests at service boundaries, snapshot review
  rules, and flake triage. Use when deciding which tests a change needs, when a suite feels slow,
  brittle, or falsely green, or before adding a new testing layer or tool. The red-green implementation
  loop routes to test-driven-development; proving a task complete routes to verification-before-completion;
  coverage tooling questions route to test-engineer.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: test-engineer
---

# Testing Strategy

Test suites fail in two directions: too little (bugs ship) and too much of the wrong kind (slow,
brittle, and ignored). This skill picks the smallest set of tests that would actually fail if the
behavior broke — and keeps the suite trustworthy enough that a red result means something.

## WHEN TO USE

- Deciding which tests a change needs (new feature, bug fix, refactor).
- A suite is slow, flaky, or passes when it should not.
- Choosing a testing tool or layer: unit, integration, E2E, property, contract, snapshot.
- Reviewing a PR whose tests assert nothing meaningful.

## WHEN NOT TO USE

- Writing the first failing test and iterating red→green — `test-driven-development`.
- Attaching evidence to a completion claim — `verification-before-completion`.
- Debugging a failing test as a bug — `systematic-debugging`.
- Coverage tooling and CI wiring questions — `test-engineer`.

## DECISION TREE

```text
1. LIST BEHAVIORS THAT CAN BREAK
   Scenarios in user/API language, not function names. Each behavior gets one test that would
   fail for its regression — or a written reason it is exempt (covered elsewhere, untestable
   now, deferred).

2. PICK THE SIZE
   Small: single process, no network/disk I/O — pure logic, parsing, reducers.
   Medium: one machine, real DB/queue with local instances, stubbed externals — seams and
   integrations.
   Large/E2E: whole system, few of them, critical user journeys only.
   ~80/15/5 (unit/integration/E2E) is a heuristic for healthy suites, not a target to game.
   Integration-heavy stacks (typical component web apps) may correctly invert it — the trophy
   shape is context, not law.

3. CHOOSE THE ORACLE
   Assert observable behavior (returns, state, rendered output, HTTP response), not interactions
   with internals. A behavior-preserving refactor should leave tests untouched.
   Name tests for behavior: "rejects expired tokens", not "calls validateToken".

4. CONTROL THE DATA
   Builders/factories with sensible defaults; each test overrides only the fields it depends on.
   Explicit local data beats shared fixtures with hidden state.

5. REACH FOR SPECIALIZED TOOLS ONLY WHERE THEY PAY
   Property-based: ordering, round-trip, and invariant claims over generated inputs
   (shrink reports minimize the counterexample — keep it as a regression).
   Mutation testing: changed, critical modules; survivors mean missing assertions, not a score
   to maximize.
   Fuzzing: parsers, decoders, boundary input — any code that consumes bytes from outside.
   Contract tests: service boundaries you do not own (consumer expectations verified against
   provider), so integration breaks are caught without full E2E.
   Snapshots/approvals: only small, deterministic, meaningfully reviewed outputs; an unreviewed
   `--update` is how a bug becomes the baseline.

6. TREAT FLAKES AS DEFECTS
   Reproduce, isolate the nondeterminism (time, ordering, network, randomness), fix or quarantine
   with an owner and a date. A rerun may diagnose; it must never silently convert red to green.
```

## FAILURE MODES & MITIGATIONS

1. **Coverage as goal.** *DETECT:* percentage celebrated; assertions shallow. *FIX:* behavior list;
   mutation runs on critical modules instead.
2. **Implementation-detail tests.** *DETECT:* refactor breaks tests that assert behavior unchanged.
   *FIX:* assert through the public surface.
3. **Shared-fixture soup.** *DETECT:* tests pass alone, fail together. *FIX:* builders; explicit
   per-test state.
4. **Snapshot blindness.** *DETECT:* large snapshot diffs merged without review. *FIX:* small
   snapshots; review every update; prefer explicit assertions for intent.
5. **Rerun-to-green.** *DETECT:* CI retries masking flakes; zero flake tickets. *FIX:* flake
   triage with owner; quarantine visibly.
6. **E2E as the default.** *DETECT:* hour-long suites; everyone bypasses them. *FIX:* push coverage
   down to medium tests; keep E2E for journeys.
7. **Test doubles that lie.** *DETECT:* prod breaks where the mock "verified" success. *FIX:*
   contract tests against real schemas; fewer, more realistic stubs.

## QUANTITATIVE RULES

- Every new behavior: one failing-first test, or a named exemption.
- Two consecutive runs must both pass before a suite is called deterministic.
- At most one rerun to diagnose a suspected flake; then triage.
- Mutation runs on changed critical files only; treat survivors as missing assertions.
- E2E additions need a named critical journey; otherwise push down a layer.
- Never leave `.only`, skips, or retries in place of a fix (AGENTS.md §2.4).

## VERIFICATION GATE

- [ ] Behavior list covered or exemptions named with reasons.
- [ ] New tests fail without the change (or were written failing-first).
- [ ] Tests assert observable behavior, not internal calls.
- [ ] Deterministic across two consecutive runs; no new flake introduced.
- [ ] No skipped/only/disabled tests left behind; failures reported as limitations, never
      suppressed.

## REFERENCES

- `test-driven-development` — the red-green loop this strategy feeds
- `verification-before-completion` — evidence for a done claim
- `systematic-debugging` — when a red test is the symptom, not the problem
- `test-engineer`, `test-oracle` (agents) — suite ownership and independent acceptance tests
