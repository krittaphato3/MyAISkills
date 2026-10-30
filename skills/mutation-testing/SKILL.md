---
name: mutation-testing
description: >-
  Tests whether the tests can fail. Introduces small semantic mutations, runs the suite, and
  reports survivors as untested behavior. Use when a suite is green but defects escape, when
  judging test quality without reading every test, or after adding coverage for a risky module.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: test-engineer
---

# Mutation Testing

Coverage says the line ran. Mutation testing says whether anything would notice if the line were
wrong. It is the cheapest answer to "are these tests real", and it does not depend on trusting
the agent that wrote them.

## WHEN TO USE

- A green suite keeps letting defects through.
- A module is risky (money, auth, data integrity) and you want evidence its tests bite.
- An agent wrote both the code and the tests; you need a check that does not trust either.
- Deciding whether a refactor's test suite is strong enough to permit the change.

## WHEN NOT TO USE

- A tiny change already covered by a failing-before/passing-after test.
- Slow integration suites where a mutation run would take longer than the feature.
- Code with no observable behavior (pure config, generated files).

## DECISION TREE

```text
1. PICK THE SCOPE
   One module or the changed files. Never the whole repo on the first run.

2. CHOOSE OPERATORS
   Negate conditions, flip comparison boundaries (< to <=), swap boolean operators,
   remove a return value, change a constant. Semantic, not formatting.

3. RUN EACH MUTANT AGAINST THE SUITE
   Killed = a test failed. Survived = the suite still passed. Timeout = inconclusive.

4. TRIAGE SURVIVORS
   Missing assertion -> assert the outcome.
   Missing case       -> add the boundary or error path.
   Equivalent mutant  -> document why it cannot be killed.

5. FIX THE WEAK TESTS, NOT THE MUTANT LIST
   The goal is behavior coverage, not a score.

6. RECORD THE BASELINE
   Mutation score for the module, and the survivors you accepted with reasons.
```

## FAILURE MODES & MITIGATIONS

1. **Score chasing** — assertions added only to kill mutants. *DETECT:* tests assert internals. *FIX:* assert observable outcomes.
2. **Equivalent mutants** — behavior-preserving mutations counted as failures. *DETECT:* the mutant cannot be observed. *FIX:* mark equivalent with a reason.
3. **Whole-repo run** — hours of compute for a number nobody acts on. *DETECT:* run time exceeds the change. *FIX:* scope to changed files.
4. **Tautological tests** — expected values computed by the code under test; mutants survive silently. *DETECT:* hardcoded vs computed expectations. *FIX:* literal expected values.
5. **Flaky suite** — mutants survive because tests are nondeterministic. *DETECT:* unrelated failures. *FIX:* fix determinism first, then measure.

## VERIFICATION GATE

- [ ] Scope named and limited to the changed or risky module.
- [ ] Mutations are semantic, not cosmetic.
- [ ] Survivors triaged into missing assertion, missing case, or equivalent.
- [ ] At least one survivor produced a real test improvement.
- [ ] Baseline score recorded with the accepted survivors and their reasons.

## REFERENCES

- `testing-strategy` — which layer a test belongs in
- `test-driven-development` — the RED-first discipline this complements
- `ship-gate` — where this evidence is consumed
- `verification-before-completion` — artifact requirements
