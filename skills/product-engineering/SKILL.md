---
name: product-engineering
description: >-
  Frames work by user value before code: the problem and its evidence, a working-backwards PR/FAQ,
  appetite with scope hammering, the smallest valuable slice, success metrics with baselines,
  cost-of-delay ordering, and build-vs-buy calls. Use when a request is a solution without a
  stated problem, when scope needs cutting, when choosing between two things to build, or when a
  refactor or infrastructure project needs an outcome-based case. Delivery sequencing routes to
  deep-planner; UX behavior review to ux-review; pricing, legal, and roadmap politics are product
  decisions this skill does not make.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G3
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: product-strategist
---

# Product Engineering

The most expensive engineering failure is building the wrong thing correctly. Product engineering
is the discipline of deciding what deserves to exist, how small it can be, and how you will know
it worked — before writing code. Engineers are well placed for this: they see the implementation
cost the roadmap cannot.

## WHEN TO USE

- The request arrives as a solution ("add a settings page") with no stated problem.
- Two or more efforts compete for the same week; ordering is the question.
- A feature, refactor, or infrastructure project needs a case made in outcomes, not components.
- Scope must be cut to fit a fixed window.
- A build-vs-buy fork (auth, payments, search, queue) is on the table.

## WHEN NOT TO USE

- The work is already shaped and sequenced — `deep-planner` turns it into tasks.
- The request is genuinely ambiguous about intent — `requirements-elicitation` first.
- The deliverable is UX quality on an existing screen — `ux-review`.
- The decision is a personal or team preference beyond evidence; say so and pick.

## DECISION TREE

```text
1. PROBLEM, WITH EVIDENCE
   Who is failing at what, and how do we know? Ticket volume, support quotes, funnel data,
   direct observation. No evidence → the first deliverable is evidence, not a feature.

2. OUTCOME AND METRIC BEFORE SCOPE
   One primary metric, two guardrails, a baseline, and a measurement window. "Increase activation
   from 31% to 40% within 6 weeks" — not "improve onboarding."

3. WORKING BACKWARDS
   Draft the release announcement and the FAQ (what, who cares, how we know, what could go
   wrong) as if it already shipped. If the paragraph is boring, the scope is wrong. This is a
   one-page artifact, not a ceremony.

4. APPETITE, THEN SCOPE HAMMERING
   Fix the time, vary the scope. List rabbit holes (the unknown that can eat weeks) and no-gos
   (what this version explicitly will not do). Cutting scope is the tool; moving the date is not.

5. SMALLEST VALUABLE SLICE
   The thinnest version that delivers the outcome to some real users, with its exclusions named.
   Ship it, observe, then earn the next slice. "Platform for one use case" is a failure shape.

6. ORDER BY COST OF DELAY
   Value, time-criticality, risk reduction, and unlock-capacity versus job size. Existential
   risks first; then high-leverage work with room to contribute; snacks and vanity work last.

7. BUILD VS BUY, EXPLICITLY
   Commodity capability (auth, email, payments, search) → buy or configure; differentiation or
   deep integration → build. Price the exit (migration/rollback), not just the invoice. When
   buying, the future decision is "keep it boring", so integrate at an arm's length.
```

## PATTERNS

### 1. PR/FAQ one-pager
```text
PRESS RELEASE  Who it is for · what it does · why it matters (user words, no jargon)
FAQ            How we know it worked · what could go wrong · what it costs · what we will NOT do
```

### 2. Shape Up pitch
```text
Problem · Appetite (time box) · Solution sketch (fat marker, no pixel polish)
Rabbit holes (unknowns that can eat the appetite) · No-gos (explicit exclusions)
```

### 3. Outcome case for a refactor or infra project
```text
Baseline:   recurring toil hours/week · incident count · delivery friction (lead time, flake rate)
Change:     what moves, by how much, measured how
Cost:       implementation + maintenance + migration risk
Verdict:    do / defer / don't, with the trigger that would change the answer
```
Frame debt as outcomes. "It is technical debt" is not evidence — a baseline is.

### 4. Metric tree
Goal → 2-4 observable signals → one primary metric + guardrails (latency, error rate, support
volume). Pick the HEART lens that fits (happiness, engagement, adoption, retention, task
success) or the funnel stage (acquisition, activation, retention, referral, revenue) — a lens,
not a scoreboard of every number.

## FAILURE MODES & MITIGATIONS

1. **Solution-shaped work** — shipping a requested screen that solves nothing. *DETECT:* no problem
   statement. *FIX:* write one paragraph of problem and evidence before any code.
2. **Metric without baseline** — "make it faster/better" with no current value. *DETECT:* no number
   in the plan. *FIX:* measure first; if measuring is impossible, say so and pick a proxy.
3. **Appetite creep** — scope grows, date slides, nobody decides. *DETECT:* the no-go list grows as
   the date moves. *FIX:* hammer the scope; the appetite is the constraint.
4. **Platform for one use case** — building the general solution first. *DETECT:* one consumer, many
   abstractions. *FIX:* ship the slice; generalize at the third call site.
5. **Vanity metrics** — impressive numbers that do not change a decision. *DETECT:* the metric's
   movement would not change any behavior. *FIX:* metric tree with guardrails; fewer numbers.
6. **Scoring theater** — fake precision on WSJF-style rankings. *DETECT:* decimals, no uncertainty
   labels. *FIX:* order of magnitude and assumptions; scoring is decision support.

## QUANTITATIVE RULES

- One primary metric, at most two guardrails, one baseline, one window.
- PR/FAQ and pitch artifacts: one page each. If longer, the thinking is missing.
- The smallest slice should be reviewable and shippable within days, not weeks.
- No new service, platform, or abstraction without three concrete consumers or one strategic
  reason written down.
- Every shipped slice schedules the outcome check (data review or explicit "not measuring").

## VERIFICATION GATE

- [ ] Problem statement names who fails at what, with evidence attached.
- [ ] Success metric has a baseline, a target, and a measurement window.
- [ ] The smallest valuable slice is named, with its exclusions.
- [ ] Rabbit holes and no-gos are written down.
- [ ] Build-vs-buy forks name the exit cost, not just the entry cost.
- [ ] A post-ship check exists (scheduled, or explicitly declined with a reason).

## REFERENCES

- `requirements-elicitation` — extracting intent from an ambiguous ask
- `deep-planner` — sequencing the chosen scope into verifiable tasks
- `ux-review` — evidence from the live interface
- `staff-engineering` sources: Shape Up, Working Backwards, product-engineer role writing
- `documentation-engineer` — writing the PR/FAQ and pitch artifacts
