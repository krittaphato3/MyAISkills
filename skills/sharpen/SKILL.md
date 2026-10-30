---
name: sharpen
description: >-
  Rewrites a vague request into an executable brief without doing the work: goal, constraints,
  acceptance criterion, non-goals, and the unknowns that would change the approach. Use when a task
  is underspecified, before starting /ozone-mode, or when an agent keeps solving the wrong problem.
  Executing the task routes to ozone-mode.
metadata:
  version: 1.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: meta-architect
---

# Sharpen

"Make the dashboard better" is not a task. It is a direction. Sharpening turns it into something
that can be finished and checked, without spending implementation tokens on the wrong thing.

This skill produces the brief. It does not build the feature, and it does not interview the user
for an hour.

## WHEN TO USE

- A request is one sentence with no acceptance criterion.
- Two people could read the request two ways, and the work differs materially.
- The last attempt solved something adjacent and got corrected.
- Before a T2 or T3 task where a wrong shape is expensive to undo.

## WHEN NOT TO USE

- The request already names the behavior, the surface, and what done looks like.
- A one-line fix with an obvious check.
- The missing information can be observed by running something. Go run it instead of asking.
- The real problem is a product decision; frame it with `product-engineering` first.

## DECISION TREE

```text
1. EXTRACT THE INTENT
   One sentence: who wants what outcome, and why now. If you cannot write it, say which part is
   missing rather than inventing it.

2. WRITE THE ACCEPTANCE CRITERION
   Externally observable, falsifiable, one sentence. "Saving with a duplicate email shows an
   inline error and does not create a row."

3. NAME THE SMALLEST CHANGE
   The least work that satisfies the criterion. This is the anti-overbuild clause.

4. LIST NON-GOALS
   What is explicitly out: refactors, new dependencies, adjacent screens, redesigns.

5. SEPARATE FACTS FROM ASSUMPTIONS
   Facts you can check by reading or running. Assumptions you will proceed on, stated plainly.

6. ASK ONLY WHAT BLOCKS
   At most three questions, each with the default you will use if unanswered. The ask is the slow
   path; a stated assumption is usually faster and correctable.

7. HAND OFF
   The sharpened brief goes to ozone-mode, which picks the playbook and the tier.
```

## PATTERNS

### Before and after

```text
Before:  make the dashboard better

After:   Goal: a returning user can see yesterday's revenue without scrolling.
         Criterion: at 1280px and 375px, yesterday's total is visible above the fold and
         matches the figure on the reports page.
         Smallest change: move the total into the header summary; no chart changes.
         Non-goals: restyling, new charts, mobile navigation.
         Assumptions: "yesterday" means the user's local day; revenue excludes refunds.
         Blocking question: none. Proceeding on the assumptions above.
```

### Question budget

Three questions maximum, each phrased so silence has a default:

```text
Q: Should refunds count toward revenue? Default: no, matching the reports page.
```

## FAILURE MODES & MITIGATIONS

1. **Interrogation** — ten questions before any work. *DETECT:* the user is doing the design. *FIX:* three questions, defaults stated, proceed.
2. **Invented requirement** — a criterion the user never asked for. *DETECT:* the brief contains features absent from the request. *FIX:* mark it as a proposal, not a requirement.
3. **Scope inflation** — the "smallest change" grows into a redesign. *DETECT:* non-goals list is empty. *FIX:* write the exclusions explicitly.
4. **Paraphrase only** — the request restated with nicer words and no new precision. *DETECT:* no acceptance criterion. *FIX:* add the checkable sentence.
5. **Sharpening instead of doing** — endless brief polishing. *DETECT:* second revision with no code. *FIX:* one pass, then route.

## VERIFICATION GATE

- [ ] Goal is one sentence naming the outcome.
- [ ] Acceptance criterion is observable and falsifiable.
- [ ] Smallest change is named and is smaller than the obvious implementation.
- [ ] Non-goals are listed.
- [ ] Assumptions are stated with the default chosen.
- [ ] No question was asked that a command could answer.

## REFERENCES

- `ozone-mode` — consumes the brief and picks the playbook
- `requirements-elicitation` — when the ambiguity is genuinely in the user's head
- `product-engineering` — when the request is a solution without a problem
- `in-your-own-words` — the same restatement discipline at task start
