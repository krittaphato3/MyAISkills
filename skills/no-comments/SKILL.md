---
name: no-comments
description: Removes narrating comments and encodes the constraints worth keeping as code or checks. Use
  before review or merge when a diff gained explanatory comments, or when comments restate code. Non-obvious
  why-comments forced by external systems stay.
metadata:
  version: 1.1.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-11-09'
  authored-by: comment-sicko
---


# No comments

Spawn Comment Sicko. Act on accepted findings.

Authoring agents defend comments. Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Spawn a subagent with agent: "comment-sicko"`. Pass the scope. Do not restate its rules.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run `/how` or `/why` on their symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principles** and **principles** skills guide intent only: fix real causes, redesign as if requirements always existed, never bolt on symptom guards. Neither authorizes widening the fence nor fixing instances outside it.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.

## DECISION TREE

- The comment restates the next line -> delete it.
- The comment explains a non-obvious *why* forced by an external system -> keep it, with a link or task
  reference.
- The constraint can be enforced by a type, assertion, or lint -> encode it and delete the comment.
- A licence header or tooling directive -> keep.
- The comment narrates the diff ("changed X to Y") -> delete; that belongs in the commit message.
- A public API docstring -> keep; that is documentation, not narration.

## FAILURE MODES & MITIGATIONS

- **Deleting the why-comment.** Mitigation: if a reader would ask "why on earth", the comment stays.
- **Moving comments into variable names.** Mitigation: rename only when the name carries the meaning
  without prose.
- **Comment-dense code.** Mitigation: extract a named function instead of explaining a block.
- **Stale comments surviving an edit.** Mitigation: grep for every symbol the comment names after a
  rename.
- **Docstrings stripped as noise.** Mitigation: public API documentation is not a narrating comment.

## WHEN TO USE

Before review or merge, when a diff gained narrating comments.

## WHEN NOT TO USE

Comments documenting a non-obvious why forced by an external system — keep them.
Generated files.

## VERIFICATION GATE

Accepted findings applied; rejected findings carry reasons.
No behavior changed by comment removal.

## REFERENCES

- `principles/minimize-reader-load` - what a reader must hold in their head.
- `technical-writing` - prose when prose is warranted.
- `refactoring-intelligence` - structural fixes that remove the need to explain.
