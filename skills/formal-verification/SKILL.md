---
name: formal-verification
description: >-
  Proves a property that tests cannot reach: model a protocol, state machine, scheduler, retry loop,
  parser, or concurrent data structure, check it with the tool that fits (TLA+, Alloy, Dafny, Kani,
  loom, proptest, Jepsen), and hand back a project-local check that re-runs on every change. Use when
  a race, deadlock, lost update, or invariant violation is plausible and stochastic tests keep
  missing it. Ordinary test suites route to test-engineer.
metadata:
  version: 1.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-11-08'
  authored-by: test-engineer
---

# Formal Verification

Testing samples the inputs you thought of. Verification quantifies over the ones you did not. The
question is never "should we prove it" but "which property is worth a model, and how small can the
model be".

## WHEN TO USE

- A concurrency bug is plausible: locks, queues, actor mailboxes, connection pools, lock-free code.
- A protocol spans nodes: leader election, replication, membership change, distributed transactions.
- A state machine has states you cannot easily reach from the outside: payment, order, onboarding,
  retry with backoff, session lifecycle.
- A parser or decoder must never crash or loop on adversarial input.
- A safety property is claimed in a design doc ("we never double-charge", "no two leaders").
- A stochastic test suite is green but the bug class is real and rare.

## WHEN NOT TO USE

- The behavior is deterministic and cheaply testable. Write the test; `test-engineer`.
- The property is about performance, not correctness. That is measurement, not verification.
- The model would need the whole system to be faithful. Shrink the question until it fits.
- The team cannot maintain the model. An unmaintained proof is worse than a test — it lies.

## DECISION TREE

```text
What kind of property?
├─ "no bad state is reachable" (safety) ........... TLA+ / TLC, Alloy
│  ├─ distributed protocol (messages, crashes) ... TLA+ with a small message model
│  └─ structural invariant over a data model ..... Alloy, bounded scope
├─ "something good eventually happens" (liveness) . TLA+ with fairness; expect it to be hard
├─ "this function does what its signature says" ... Dafny, F*, or refined types
├─ "this Rust/unsafe code has no UB" .............. Kani, Miri; Prusti for contracts
├─ "this concurrent structure is linearizable" .... loom (Rust), jepsen/porcupine (systems)
├─ "these inputs never panic/loop" ................ proptest / fast-check / libFuzzer + a shrinker
└─ "this state machine can reach an invalid state"  explicit model + exhaustive BFS, or TLA+
```

### Tool fit

| Shape | Tool | Cost |
|---|---|---|
| Distributed protocol, message passing | TLA+ / TLC | Days; highest payoff |
| Structural invariant, bounded scope | Alloy | Hours |
| Sequential algorithm with contracts | Dafny | Days |
| Rust `unsafe`, panics, overflow | Kani, Miri | Hours |
| Concurrent data structure | loom | Hours |
| Whole-system partition behavior | Jepsen | Weeks |
| Adversarial input robustness | proptest, libFuzzer | Hours |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Model drift | Code changes, the model does not, proof is stale | Check the model in CI, and tie it to the code path by name |
| Proving the model, not the system | Model is simpler than the implementation in the way that matters | List every abstraction and justify why it preserves the property |
| Unbounded state space | TLC never terminates | Small constants (2-3 nodes, 2 values); prove the small case |
| Liveness by hand-wave | "Eventually" assumed without fairness | State fairness explicitly; expect to weaken the claim |
| Green with no coverage | Property holds trivially | Add a deliberately broken variant; the check must fail |
| Nobody can read it | Model is a second codebase | Keep it under ~200 lines; pair it with a diagram |
| Verification parked in a branch | Runs once, never again | Ship as a project-local skill + CI job |

## QUANTITATIVE RULES

- **2-3 nodes, 2-3 values.** Small models find the real bugs; scale hides them.
- **One property per model.** A model claiming four properties proves none clearly.
- **Every abstraction is listed** with the reason it preserves the property.
- **Mutate the model once** to confirm the checker fails. A checker that never fails is unproven.
- **Model ≤ 200 lines**, or split the property.
- **CI re-runs the model** at a bounded depth on every change to the covered module.

## VERIFICATION GATE

- [ ] The property is written in one sentence a non-author can read.
- [ ] The tool choice is justified by the property's shape, not by familiarity.
- [ ] A broken variant of the model fails the check — recorded.
- [ ] Every abstraction from the real code is listed with its justification.
- [ ] The model runs in CI in bounded time, or its exclusion is written down.
- [ ] A project-local skill or script reproduces the check from a clean checkout.
- [ ] The finding, if any, is reproduced against the real code and links to the trace.

## REFERENCES

- `test-engineer` for the surrounding test suite and where verification fits in the pyramid.
- `concurrency-engineer` for the concurrency semantics being modelled.
- `distributed-systems-engineer` for consistency models and failure assumptions.
- `mutation-testing` for the cheap version of "does this check bite".
- `systematic-debugging` when a reported bug is suspected to be a race.
