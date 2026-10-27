---
description: Pause safely — write a durable handoff so the next session resumes with full context
argument-hint: [output path, default the repo's existing handoff file]
---

Apply `session-continuity` with `token-economy` (compact deliberately, not automatically):

1. Write or refresh the handoff in this order: goal (user's words) · constraints and permissions ·
   decisions made (with the why) · artifacts and their paths · current gate and status ·
   open questions with owners · the single next action · do-not-redo list (dead ends, rejected
   approaches and why).
2. Keep it ≤60 lines, rewritten rather than appended; the next action appears in the first
   10 lines.
3. Save it where the project already keeps such state; otherwise default to `.agent/CONTEXT.md`
   under the project root.
4. Nothing required to resume may live only in chat. Credentials and personal data do not go in
   the file.

Target: $ARGUMENTS
