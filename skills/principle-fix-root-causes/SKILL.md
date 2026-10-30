---
name: principle-fix-root-causes
description: Apply when debugging. Trace each symptom to its root cause and fix it there; reproduce first,
  ask why until you reach it, resist nil-check guards that silence crashes.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: meta-architect
---


# Fix Root Causes

When debugging, do not paper over symptoms. Trace every problem to its root cause and fix it there.

**Why:** Symptom fixes accumulate. Each workaround makes the system harder to reason about, and the real bug remains. Root-cause fixes are slower upfront but reduce total debugging time.

**Pattern:**
- Reproduce first (if you can't reproduce it, you can't verify your fix)
- Ask "why" until you hit the root cause
- Resist the urge to add guards (adding a nil check to silence a crash is a symptom fix)
- If a workaround needs a paragraph-long comment to justify it, the code is wrong (fix the code, not the comment)
- Check for the pattern, not just the instance (grep for the same pattern, fix all instances)
- When stuck, instrument. Don't guess (add logging, read the actual error)

**Restart bugs: suspect state before code**

Code doesn't change between runs. State does. When something "fails after restart," suspect stale persistent state first: config files, caches, lock files, serialized state. If clearing a state file restores behavior, prioritize state validation as the fix.

## WHEN TO USE

Debugging, or when a symptom keeps returning.

## WHEN NOT TO USE

A live incident where mitigation first is correct — `incident-response-engineer`.

## VERIFICATION GATE

The first point of divergence was identified with a reproduction; no defensive band-aid added.
