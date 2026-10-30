---
name: principle-attack-the-premise
description: >-
  Breaks the shared assumption behind repeated failed fixes. Use when a second fix fails the same
  way, when two attempts share one premise, or when the evidence keeps contradicting the theory.
  Routes premise-free debugging to systematic-debugging and design forks to architect.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: red-team-qa
---

# Attack the Premise

Two fixes that fail the same way are not two bugs. They are one wrong assumption, tested twice.

The instinct after a failed fix is to look harder at the symptom. The cheaper move is to write
down the premise the fix assumed and test that instead. A premise is testable in minutes; a
symptom hunt can burn a session.

## WHEN TO USE

- A second fix produces the same failure, or a different failure from the same cause.
- The evidence contradicts the theory and the response is to add another guard.
- A plan depends on "the library does X" or "that path cannot be reached".
- A design review keeps returning to the same objection from different reviewers.

## WHEN NOT TO USE

- The first attempt failed for an obvious, named reason. Fix that reason.
- No fix has been attempted yet. Use `systematic-debugging` to find the mechanism first.
- The disagreement is a product preference, not a factual premise.

## DECISION TREE

```text
1. LIST THE PREMISES
   Every fix assumed something: state shape, call order, data freshness, who owns the value,
   what the framework guarantees. Write them as sentences that can be false.

2. FIND THE SHARED ONE
   What do both failed attempts believe? That belief is the suspect, not the code.

3. TEST IT DIRECTLY
   One command, one probe, one assertion. Cheapest observation that splits true from false.
   Do not test the symptom again; test the belief.

4. ACT ON THE ANSWER
   Premise false  -> delete both fixes, redesign from the real behavior.
   Premise true   -> the mechanism is elsewhere; bisect the call path with instrumentation.

5. RECORD IT
   Add the premise to the change description or a comment only where the code cannot show it.
```

## FAILURE MODES & MITIGATIONS

1. **Guard stacking** — a third null check instead of asking why the value is null. *DETECT:* the diff adds branches without removing a cause. *FIX:* test the premise about where null originates.
2. **Theory preservation** — evidence is explained away to keep the model. *DETECT:* "probably", "should still". *FIX:* name the observation that would falsify the model and go get it.
3. **Symptom bisect** — hours spent narrowing the symptom with no premise written. *DETECT:* no sentence starting "I assume". *FIX:* write three premises, test the riskiest.
4. **Authority premise** — "the docs say" treated as behavior. *DETECT:* no run of the actual call. *FIX:* observe it.
5. **Premise creep** — the fix grows to accommodate a premise nobody checked. *DETECT:* the design now has an option that exists only for the theory. *FIX:* test the premise before keeping the option.

## VERIFICATION GATE

- [ ] The shared premise is written as a falsifiable sentence.
- [ ] One command or probe tested it, with output.
- [ ] The fix follows from the result, not from the original theory.
- [ ] Both earlier fixes are removed if the premise was false.
- [ ] The remaining uncertainty is named.

## REFERENCES

- `systematic-debugging` — finding the mechanism before theorizing
- `principle-fix-root-causes` — why symptom fixes return
- `doubt-driven-development` — adversarial review of a conclusion
