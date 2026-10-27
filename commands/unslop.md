---
description: Ruthlessly audit diffs or files for AI fluff, redundant comments, dead code, and speculative bloat
argument-hint: [file path or target]
---

Apply pstack's unslop and comment-sicko standards:
1. Strip all trivial comments explaining obvious code.
2. Delete speculative abstractions, premature helpers, and unused parameters.
3. Replace scattered boolean flags with strict discriminated unions.
4. Keep functions under 40 lines and minimize reader load.

Target: $ARGUMENTS
