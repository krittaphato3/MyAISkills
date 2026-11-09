---
name: principles
description: >-
  One indexed set of 24 engineering principles in five groups (core, architecture, verification,
  delegation, meta), each with a one-line rule and a reference file. Use when a task needs a
  judgment call rather than a technique: over-engineering, a diff that keeps growing, two failed
  fixes that share one premise, unverified work, scope creep, context bloat, stalling on a human,
  a guard instead of a root cause, or deciding what to delete before adding. Replaces 23 separate
  principle skills with one trigger.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: meta-architect
  supersedes: >-
    principles, principles, principles,
    principles, principles,
    principles, principles, principles,
    principles, principles,
    principles, principles,
    principles, principles,
    principles, principles,
    principles, principles,
    principles,
    principles, principles,
    principles, principles
---

# Principles

Twenty-four rules that shape how work is done, independent of the work's subject. Each is a
judgment call, not a technique: the technique skills say *how* to build a thing, these say *what
a good answer looks like* and what to throw away.

Load the reference for a principle only when its rule is the one in contention. The table is the
whole index; reading it costs less than loading any single skill it replaces.

## WHEN TO USE

- A diff is growing and you cannot say why each line is needed.
- A second fix failed the same way as the first.
- You are about to declare done and have only a claim, not an artifact.
- A design choice is being repeated in five places, or a signal is being threaded through five layers.
- You are waiting on a human for something reversible, or dumping raw output into the main thread.
- You are about to add a guard, an abstraction, a compatibility layer, or a config flag.

## WHEN NOT TO USE

- The task matches a technique skill (`systematic-debugging`, `test-driven-development`,
  `verification-before-completion`). Load that skill; it carries its own working rules.
- You need a decision *between designs*. That is `architect`, `debate-protocol`, or
  `exhaust-the-design-space`, not a single principle.
- You are maintaining this catalog. That is `agent-config-maintenance`.

## DECISION TREE

```text
What is the symptom?
├─ too much code / too many layers / diff keeps growing ...... laziness-protocol
│  ├─ dead weight, stubs, redundant validators first ....... subtract-before-you-add
│  ├─ hard to trace, one-caller wrappers, hidden state ..... minimize-reader-load
│  └─ wrong core types, so downstream code branches ........ foundational-thinking
├─ the same fix keeps failing ............................... attack-the-premise
│  └─ symptom patched, cause untouched ..................... fix-root-causes
├─ bolting a new requirement onto an old design ............. redesign-from-first-principles
├─ branchy code encoding one domain shape ................... model-the-domain
├─ illegal states still representable ....................... type-system-discipline
│  └─ validation drifting inward from a boundary ........... boundary-discipline
├─ repeated choice needs one source of truth ................ minimize-reader-load
├─ work amid crashes, retries, partial runs ................. make-operations-idempotent
├─ two concurrent writers to one resource ................... separate-before-serializing-shared-state
├─ old API still alive next to the new one .................. migrate-callers-then-delete-legacy-apis
├─ mid-rewrite, deciding what to preserve ................... outcome-oriented-execution
├─ "done" without evidence .................................. prove-it-works
├─ multi-step work with no checkpoint ....................... sequence-verifiable-units
├─ deciding what to build at all ............................ experience-first
│  └─ novel design with no precedent ....................... exhaust-the-design-space
├─ tests pass but behavior broke / tests break on refactor .. test-behavior-not-implementation
├─ a number is about to be reported ......................... explain-the-number
├─ context filling with raw payloads ........................ guard-the-context-window
├─ blocked on a human for something reversible .............. never-block-on-the-human
├─ bulk or repeated work done by hand ....................... build-the-lever
└─ the same correction happened twice ....................... encode-lessons-in-structure
```

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Principle shopping | Loading five principles to justify a design already chosen | Pick the one the symptom names; if none names it, it is not a principle problem |
| Guard as fix | `if x is None` silences the crash, leaves the state wrong | `fix-root-causes`: ask what produced `None` |
| Premature abstraction | Two callers look similar today, diverge tomorrow | `laziness-protocol`: second real caller before the abstraction |
| Verification theater | Tests assert mocks; the artifact was never run | `prove-it-works`: run the feature, read the real value |
| Context poisoning | A 4k-line log pasted into the main thread | `guard-the-context-window`: subagent reads, returns the finding |
| Premise blindness | Every fix assumes the same unstated condition | `attack-the-premise`: write the premise down, test it directly |

## QUANTITATIVE RULES

- **Second caller, not second use.** An abstraction is earned by a second *independent* caller.
- **Three layers.** If answering "what does this do" needs more than three files, flatten it.
- **One number, one artifact.** Any performance claim carries a before/after measurement from a
  pinned environment, or it is not reported.
- **Two attempts.** Two fixes sharing one premise means the premise is wrong, not the fix.

## VERIFICATION GATE

Before declaring a principle applied:

- [ ] The symptom named in the table is the one that actually occurred.
- [ ] The change is smaller than or equal to what the principle demands, not larger.
- [ ] A reviewer can point at the line that satisfies the rule.
- [ ] No principle was cited to justify work that was already decided.

## REFERENCES

- `references/laziness-protocol.md`
- `references/foundational-thinking.md`
- `references/redesign-from-first-principles.md`
- `references/attack-the-premise.md`
- `references/subtract-before-you-add.md`
- `references/minimize-reader-load.md`
- `references/outcome-oriented-execution.md`
- `references/experience-first.md`
- `references/exhaust-the-design-space.md`
- `references/build-the-lever.md`
- `references/model-the-domain.md`
- `references/boundary-discipline.md`
- `references/type-system-discipline.md`
- `references/make-operations-idempotent.md`
- `references/migrate-callers-then-delete-legacy-apis.md`
- `references/separate-before-serializing-shared-state.md`
- `references/prove-it-works.md`
- `references/fix-root-causes.md`
- `references/sequence-verifiable-units.md`
- `references/test-behavior-not-implementation.md`
- `references/explain-the-number.md`
- `references/guard-the-context-window.md`
- `references/never-block-on-the-human.md`
- `references/encode-lessons-in-structure.md`
