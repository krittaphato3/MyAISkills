---
name: correct
description: >-
  Turns repeated corrections into enforcement. Mines the session for mistake classes, fixes each
  at the highest level that works (architecture, types, lint, CI, tests, docs), and keeps a table
  pairing every rule with what enforces it. Use when the user corrects the same thing twice or
  asks why a mistake keeps recurring.
metadata:
  version: 1.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: meta-architect
---

# Correct

A correction that lives only in the chat is a correction you will receive again.

The user should not have to point out the same class of mistake twice. When they do, the output
is not an apology and a fix. It is a change to the system that made the mistake possible.

## WHEN TO USE

- The user corrects the same behavior a second time, in this session or a previous one.
- A review finding repeats a class already fixed elsewhere in the repo.
- A defect escaped that a check could have caught.
- The user asks to make a rule stick.

## WHEN NOT TO USE

- A one-off preference with no recurrence. Just comply.
- A disagreement about goals rather than execution. That is `requirements-elicitation`.
- The correction would require weakening a check or suppressing a real failure. Refuse and explain.

## DECISION TREE

```text
1. NAME THE CLASS
   Not "the button was wrong" but "state derived in two places drifts". A class is a sentence
   that predicts a future mistake.

2. FIND THE HIGHEST ENFORCEMENT LEVEL THAT WORKS
   architecture  make the wrong shape impossible (types, single owner, state machine)
   types         make the illegal state unrepresentable
   lint          a rule with a corrective message
   CI            a check that fails the build
   tests         a regression test that names the class
   docs          a written rule, last resort, because it decays

3. IMPLEMENT IT
   Change the mechanism, not the prose. A rule without an enforcement point is a wish.

4. RECORD THE PAIR
   rule -> what enforces it -> where. Keep this table in the repo, not in chat.

5. VERIFY THE ENFORCEMENT
   Break the rule deliberately and confirm something fails. An unverified rule is untested.
```

## FAILURE MODES & MITIGATIONS

1. **Documentation-only fix** — a new paragraph in a rules file. *DETECT:* no code, test, or lint change. *FIX:* move one level up the ladder.
2. **Over-enforcement** — a lint rule that blocks legitimate patterns. *DETECT:* suppressions appear immediately. *FIX:* narrow the rule or use a type instead.
3. **Single-case test** — one regression test for one instance of a class. *DETECT:* the next instance escapes. *FIX:* test the class, or enforce structurally.
4. **Silent rule** — enforcement exists with no message explaining the fix. *DETECT:* the failure says what, not what to do. *FIX:* write the corrective message.
5. **Rule sprawl** — twenty rules nobody can rank. *DETECT:* the rules file grows faster than defects fall. *FIX:* consolidate; keep the ones that caught something.

## VERIFICATION GATE

- [ ] The mistake class is named in one sentence that predicts recurrence.
- [ ] Enforcement lives at the highest level that works, not in prose.
- [ ] Deliberately violating the rule produces a failure.
- [ ] The rule-to-enforcement table is updated.
- [ ] No check was weakened to make the rule pass.

## REFERENCES

- `principle-encode-lessons-in-structure` — the underlying doctrine
- `agent-config-maintenance` — where rules and skills live in this config
- `skill-creator` — turning a lesson into a reusable skill
- `verification-before-completion` — proving the enforcement works
