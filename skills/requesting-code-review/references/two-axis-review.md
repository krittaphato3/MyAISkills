# Two-axis review

A single reviewer blends two different questions and then reports one verdict. That blend is why
a change can pass review while implementing the wrong thing: it followed every convention, so
the standards axis was happy, and nobody asked whether it satisfied the request.

Split the review into two independent passes.

## Axis 1: Standards

Does the change follow the repo's own rules and general engineering standards?

- Named conventions from `AGENTS.md`, lint config, and neighbouring code.
- Duplication, dead code, an abstraction with one caller.
- Error handling at boundaries; no swallowed errors.
- Test quality: would these tests fail if the behavior broke.
- Naming that matches the domain vocabulary already in use.

## Axis 2: Spec

Does the change implement the thing that was asked for?

- The acceptance criterion, quoted, satisfied literally.
- Every requested behavior present; nothing extra added.
- Edge cases named in the request handled.
- The user-visible outcome, not just the internal mechanism.

## Rules

1. Two reviewers, or two sequential passes with fresh context. Never one blended verdict.
2. Report the axes separately: `STANDARDS pass|fail`, `SPEC pass|fail`.
3. A change that passes one and fails the other does not ship. Say which axis failed.
4. Findings are hypotheses until reproduced. A finding with no evidence is a note.
5. Neither reviewer edits the artifact. The author fixes; the reviewer verifies the fix.
6. Any edit after the verdict invalidates it. Re-review the delta.

## Why the split matters

The common escape is a clean diff that solves the wrong problem. Standards review cannot see it,
because the code is good. Spec review cannot see the duplication or the missing error path,
because the behavior is right. You need both, and you need them separated so one does not
launder the other.
