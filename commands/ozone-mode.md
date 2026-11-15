---
description: Activate Ozone Mode
argument-hint: [task description]
---

# Ozone Mode

Activate the engineering router for this task: `$ARGUMENTS`

## What to do

1. **Classify.** T0 (trivial, in-thread), T1 (one implementer), T2 (dual track plus critic),
   T3 (debate). State the tier and why.
2. **Route.** Read `skills/ozone-mode/SKILL.md`, match one playbook under
   `skills/ozone-mode/playbooks/`, and copy its steps into the todo list verbatim.
   A step you skip stays visible as `skip: <reason>`.
3. **Ground.** Name the data shape before any logic. Quote the acceptance criterion. Find the
   callers of what you are about to change.
4. **Act.** Smallest diff that meets the criterion. No unrequested refactors.
5. **Prove.** Run typecheck, lint, and the relevant tests locally first. They cost no model
   tokens. Then verify on the real surface the user will use.
6. **Gate.** Run `ship-gate` before reporting complete: every claim traces to a hunk, an
   independent verdict covers T2/T3 work, blast radius and unverified items are stated.
7. **Report.** DONE, CHANGED, VERIFIED, GAPS. No emojis. Label every claim measured, inferred,
   or guess.

## Non-negotiables

- Never report done without an artifact produced after the final edit.
- Never weaken a test, lint rule, or type check to make something pass.
- Never self-certify T2/T3 work. Independent verification, on the exact head.
- Never commit, push, or deploy without explicit approval.

## Task

$ARGUMENTS
