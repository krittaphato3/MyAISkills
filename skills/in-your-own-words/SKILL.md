---
name: in-your-own-words
description: >-
  Restates the task in the agent's own words before acting: goal, acceptance criterion, smallest
  expected change, non-goals, and the assumptions that could be wrong. Use at the start of a
  non-trivial task or when a request could be read two ways. Ambiguity that genuinely needs the
  user routes to requirements-elicitation.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: planner
---

# In Your Own Words

Parroting the request proves nothing. Restating it in different words, with the criterion and the
assumptions made explicit, is the cheapest test of whether you understood it. Most wrong work is
a confident misread, not a coding failure.

## WHEN TO USE

- Start of any task where the diff will be larger than a few lines.
- The request contains a pronoun, a comparison, or a word with two meanings ("faster", "cleaner",
  "like the other page").
- You notice yourself filling a gap with an assumption.
- A previous attempt was corrected for solving the wrong problem.

## WHEN NOT TO USE

- A one-line fix with an unambiguous target.
- The user explicitly wants speed and the request is already precise.
- As a substitute for asking when the ambiguity is genuinely unresolvable by reading or running.

## DECISION TREE

```text
1. WRITE THE GOAL
   Who gets what outcome. One sentence, no solution words.

2. WRITE THE CRITERION
   The observable check that will decide pass or fail. If you cannot name one, the task is not
   understood yet.

3. WRITE THE SMALLEST CHANGE
   The least work that satisfies it. This is what stops scope drift before it starts.

4. WRITE THE NON-GOALS
   What you are deliberately not touching. Name at least one thing a reasonable person might
   expect and you are excluding.

5. LIST ASSUMPTIONS WITH THEIR FAILURE COST
   Each assumption plus what breaks if it is false. Proceed on the cheap ones; test the expensive
   ones before writing code.

6. PROCEED OR ASK
   Proceed when the assumption is reversible. Ask only when the wrong branch is expensive and
   unobservable. Never ask what a command can answer.

7. CHECK BEFORE REPORTING
   At the end, re-read the restatement. Did the diff serve that goal, or a different one?
```

## PATTERNS

### Restatement shape

```text
GOAL        a returning user sees yesterday's revenue without scrolling
CRITERION   total visible above the fold at 1280 and 375, matches the reports page
SMALLEST    move the existing total into the header summary
NON-GOALS   restyling, new charts, mobile navigation
ASSUMPTION  "yesterday" is the user's local day. If false: the number is wrong by hours.
ASSUMPTION  refunds excluded. If false: total is higher than the reports page.
PLAN        one component change plus a DOM assertion at two widths
```

### Two readings

When a request supports two readings, write both and pick the cheaper to reverse:

```text
Reading A: hide the section on mobile.  Cost if wrong: users lose access (cheap to revert).
Reading B: collapse it behind a disclosure.  Cost if wrong: extra tap for everyone.
Proceeding with B because it preserves access; say so in the report.
```

## FAILURE MODES & MITIGATIONS

1. **Parroting** — the request repeated with synonyms. *DETECT:* no criterion, no non-goals. *FIX:* add the checkable sentence and one exclusion.
2. **Solution smuggling** — the restatement names the implementation before the goal is settled. *DETECT:* the goal contains a component or library name. *FIX:* rewrite the goal as a user outcome.
3. **Assumption hiding** — an unstated guess drives the design. *DETECT:* a decision with no corresponding assumption line. *FIX:* state it, with its failure cost.
4. **Question reflex** — asking instead of reading or running. *DETECT:* a question a command could answer. *FIX:* run the command, state the result.
5. **Restatement drift** — the final diff serves a goal nobody wrote down. *DETECT:* the report does not quote the restatement. *FIX:* quote it and check the diff against it.

## VERIFICATION GATE

- [ ] Goal written as an outcome, with no implementation named.
- [ ] Criterion is observable and falsifiable.
- [ ] Smallest change named; non-goals listed.
- [ ] Assumptions carry their failure cost.
- [ ] No question asked that reading or running could answer.
- [ ] Final report quotes the goal and shows the diff served it.

## REFERENCES

- `sharpen` — the same discipline applied to a written brief
- `requirements-elicitation` — when the answer really is in the user's head
- `principle-laziness-protocol` — smallest change, deletion first
- `ozone-mode` — routes the playbook after the restatement
