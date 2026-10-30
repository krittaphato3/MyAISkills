---
name: blast-radius
description: >-
  Find what a change could break somewhere else before it ships, beyond the diff, and prove the one
  fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X',
  'what could this break', or reviewing a small diff you don't trust.
metadata:
  version: 2.0.0
  domain: architecture
  grade: G2
  status: active
  last-reviewed: '2026-10-31'
  owned-by-agent: refactoring-specialist
---

# Blast Radius

Find what a change breaks somewhere else before it ships. Listing callers is necessary but insufficient;
the core job is identifying and eliminating breakage where text search stops: serialized state, wire formats,
lifecycle timings, and unstated caller assumptions.

## WHEN TO USE

- Before modifying a shared utility, public interface, database schema, or exported contract.
- Assessing regression risk for a complex refactoring or behavior change.
- Reviewing a seemingly small diff touching core abstractions.

## WHEN NOT TO USE

- Pure private logic with strictly verified local callers.
- Active incident containment (route to `incident-response-engineer`).

## DECISION TREE

```text
1. ENUMERATE DIRECT CALLERS
   Search all direct usages: `rg -w "<symbol>"`. Never rely on memory.
   Examine every call site for assumptions about nullability, throw behavior, or parameter defaults.

2. TRACE BEYOND GREP
   Follow boundaries text search cannot see:
   - Serialized payloads: JSON schemas, wire formats, Redis keys, DB rows.
   - Execution timing: microtasks, race conditions, mount/unmount lifecycles.
   - Cross-language / multi-package consumers.

3. FORMULATE THE SAFETY INVARIANT
   Define the single concrete condition that guarantees callers won't break:
   "This change preserves the return shape for all non-empty inputs and defaults empty inputs to []."

4. EXECUTE LEVEL 4 PROOF
   Words are not evidence. Prove the safety invariant with running code:
   - Level 1: "I think it is safe." (Unacceptable)
   - Level 2: Pointed at line numbers in code.
   - Level 3: Logical proof of non-reachability.
   - Level 4: Executable test or probe script calling the real code and asserting safety. (Mandatory)
   If a safety invariant cannot reach Level 4 cheaply, mark it explicitly as UNPROVEN in the ledger.

5. VERIFY DOWNSTREAM SUITES
   Run the full test suites of all consumer packages or modules identified in step 1.
```

## FAILURE MODES & MITIGATIONS

| Failure Mode | Mitigation |
|---|---|
| Believing a plausible writeup | Words are not proof. Require an executable probe script or passing test. |
| Missing dynamic callers | Check string-based lookups, event emitters, and reflection hooks. |
| Incomplete regression runs | Run the test suites of every identified consumer module. |

## VERIFICATION GATE

- [ ] All direct consumers identified via `rg -w` search.
- [ ] Safety invariant stated explicitly and validated with Level 4 executable proof.
- [ ] Downstream consumer test suites run and green.

## REFERENCES

- `skills/how/SKILL.md` — What the code currently does
- `skills/why/SKILL.md` — Why it was shaped that way
- `skills/ship-gate/SKILL.md` — Pre-ship verification gate and blast-radius audit
