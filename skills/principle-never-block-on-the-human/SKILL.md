---
name: principle-never-block-on-the-human
description: Apply when tempted to ask 'should I do X?' on reversible work. Proceed, present the result,
  let the human course-correct after the fact; reserve confirmation for irreversible actions.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: meta-architect
---


# Never Block on the Human

The human supervises asynchronously. Agents must stay unblocked: make reasonable decisions, proceed, and let the human course-correct after the fact. Code is cheap. Waiting is expensive.

**Why:** Every permission pause stalls the pipeline and makes the human the bottleneck. Since code changes are reversible and reviewable, a wrong decision usually costs less than blocking.

**Pattern:**
- **Proceed, then present.** Do the work, show the result. Don't ask "should I do X?" Do X, explain why.
- **Reserve questions for genuine ambiguity.** Ask only when you truly cannot infer intent from context.
- **Make the system self-healing.** When you notice a problem, log it and fix it in the next round.
- **Supervision is async.** The human reviews plans, diffs, and changes on their own schedule. Design workflows for review-after-the-fact.
- **Code is cheap, attention is scarce.** A wrong implementation costs minutes to fix. A blocked agent costs the human's attention to unblock.

**Boundaries:**
- **Irreversible actions** (force-push, delete production data, send external messages) still require confirmation.
- **Reversible actions** (write code, edit notes, split tasks) should proceed without blocking.
- **Product direction** comes from the human; *execution* should not block.

## WHEN TO USE

Reversible work where asking "should I do X?" would stall progress.

## WHEN NOT TO USE

Irreversible or outward-facing actions — ask per AGENTS.md §3.
Genuine product preference calls no experiment can settle.

## VERIFICATION GATE

Proceeded and presented a result; the question was replaced by an experiment where possible.
