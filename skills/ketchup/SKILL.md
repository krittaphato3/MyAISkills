---
name: ketchup
description: >-
  Reports the delta since the user's last message: what moved, what is verified, what is waiting on
  them, and what is still open, each line decidable without a follow-up question. Use when the user
  returns after a gap, asks what happened, or before a long run continues. Session handoff routes
  to handoff; rebuilding old context routes to recall.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: meta-architect
---

# Ketchup

The user was away. They should not have to read the transcript, and they should not have to ask
"so what happened". One reply, every open item decidable from it.

Ketchup is a delta report, not a summary of the codebase and not a session handoff.

## WHEN TO USE

- The user returns after a gap and asks what changed.
- A long run finished and needs a status report.
- Several workstreams advanced and the next step depends on which one they pick.
- Before continuing work that was paused mid-flight.

## WHEN NOT TO USE

- The user is present and following along. Answer the actual question.
- A fresh agent needs to take over. That is `handoff`.
- The user wants to reconstruct old context. That is `recall`.

## DECISION TREE

```text
1. ANCHOR TO THE LAST MESSAGE
   What did they last see or ask? Everything before that is context, not news.

2. LIST WHAT MOVED
   One line per item: what changed and where. Files, branches, artifacts. No adjectives.

3. MARK VERIFICATION PER ITEM
   verified (command + result), unverified (code exists, check not run), blocked (why).

4. NAME WHAT WAITS ON THEM
   Decisions, approvals, credentials, a choice between named options. Each with a default.

5. NAME WHAT IS OPEN
   Known gaps, failing checks, deferred work. Not hidden, not buried.

6. POINT AT THE NEXT STEP
   One sentence. If it is theirs, say the default you will take if they say nothing.
```

## PATTERNS

### Reply shape

```text
Since your last message:

CHANGED     router rewritten; poteto now forwards (skills/ozone-mode, skills/poteto-mode)
VERIFIED    lint_config 0 errors; skill_lint 0 errors / 108 advisory
UNVERIFIED  playbooks not executed against a real repo task
WAITING     commit approval; default is to leave the tree uncommitted
OPEN        50 older skills lack decision-tree sections
NEXT        commit locally, then backfill sections if you want the warnings gone
```

### Rules

- Newest change first.
- No restating of things the user already saw.
- No "everything is on track". Either a check passed or it did not.
- Every waiting item has a default, so silence is actionable.
- Numbers keep their label: measured, inferred, guess.

## FAILURE MODES & MITIGATIONS

1. **Transcript replay** — retelling the whole session. *DETECT:* more than a screen for three items. *FIX:* anchor to their last message and cut everything before it.
2. **Status without evidence** — "tests pass" with no command. *DETECT:* no artifact path. *FIX:* attach the command and result, or mark unverified.
3. **Buried blocker** — the one thing they must decide sits in paragraph four. *DETECT:* the ask is not in its own section. *FIX:* WAITING section, one line per decision.
4. **False green** — stale results presented as current. *DETECT:* the artifact predates the last edit. *FIX:* re-run or label stale.
5. **Option dump** — five choices with no recommendation. *DETECT:* no default given. *FIX:* recommend one and state the default.

## VERIFICATION GATE

- [ ] Anchored to the user's last message; no older material replayed.
- [ ] Every changed item names its artifact or path.
- [ ] Each item marked verified, unverified, or blocked.
- [ ] Waiting items have a default so silence moves work forward.
- [ ] Open gaps are listed, not omitted.
- [ ] Next step is one sentence.

## REFERENCES

- `handoff` — compressing state for a fresh session
- `recall` — rebuilding context from transcripts and git
- `session-continuity` — durable state across sessions
- `verification-before-completion` — what counts as verified
