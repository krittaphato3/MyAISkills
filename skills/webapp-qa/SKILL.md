---
name: webapp-qa
description: >-
  Drives the running web app like a user and proves the flow works: real navigation, form input,
  keyboard paths, console and network errors, and the empty, loading, and error states. Use when a
  UI change is called done, or before shipping a screen. Heuristic design critique routes to
  ux-review.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: ui-ux-architect
---

# Web App QA

"It compiles" and "the component renders" are not evidence that a user can complete the task.
The browser is the artifact. Drive it, watch the console, and capture what happened.

## WHEN TO USE

- A UI change is about to be called done.
- A flow spans more than one screen: signup, checkout, onboarding, settings.
- A form, modal, menu, or keyboard interaction changed.
- Before shipping a screen a user will depend on.

## WHEN NOT TO USE

- Pure logic or API changes with no UI surface.
- A heuristic design critique of a static mock. That is `ux-review`.
- Load or soak testing. That is `web-performance` or a dedicated harness.

## DECISION TREE

```text
1. NAME THE USER JOURNEY
   One sentence: "a new user signs up, verifies, and reaches the dashboard".

2. LAUNCH THE REAL APP
   The dev server or a built preview, not a component test harness. Record the URL and port.

3. DRIVE IT WITH REAL INPUT
   Clicks, typing, keyboard only (Tab, Enter, Escape), back button. No internal setters,
   no test-only endpoints, no direct state injection.

4. WATCH THE SIGNALS
   Console errors and warnings, failed network requests, 4xx/5xx, hydration warnings.
   A silent console error is a defect even when the screen looks right.

5. CHECK THE STATES NOBODY SCREENSHOTS
   Empty, loading, error, offline, slow network, duplicate submit, very long text, narrow width.

6. CAPTURE EVIDENCE
   Screenshot or DOM assertion per step, plus the console and network summary.
   The action and the resulting state, not just the final screen.

7. VERIFY SIDE EFFECTS
   The row written, the email queued, the file stored. Visible state alone is not proof.

8. CLEAN UP
   Stop the server, remove test data, reset the account you created.
```

## FAILURE MODES & MITIGATIONS

1. **Screenshot as proof** — a picture of the final screen with no interaction. *DETECT:* no console or network evidence. *FIX:* drive the flow and capture signals.
2. **Happy path only** — the success case passes, error states untested. *DETECT:* no evidence for empty, error, or slow states. *FIX:* exercise them deliberately.
3. **Harness shortcut** — state set directly, bypassing the UI. *DETECT:* no click or keystroke in the steps. *FIX:* use real input.
4. **Ignored console** — errors logged but not read. *DETECT:* no console summary. *FIX:* treat console errors as failures.
5. **Journey weakened to pass** — the flow edited until green. *DETECT:* the acceptance path changed. *FIX:* restore the real journey and report the defect.
6. **Test data leak** — accounts, rows, uploads left behind. *DETECT:* no cleanup step. *FIX:* clean up and record what was created.

## VERIFICATION GATE

- [ ] User journey named and driven end to end.
- [ ] Real input used; no direct state injection.
- [ ] Console and network checked, with a summary of errors.
- [ ] Empty, loading, and error states exercised.
- [ ] Keyboard-only path works, including focus after navigation.
- [ ] Side effects verified beyond the visible screen.
- [ ] Evidence captured per step and cleanup completed.

## REFERENCES

- `ux-review` — heuristic critique of the interface itself
- `accessibility-audit` — WCAG conformance and screen-reader semantics
- `agent-browser` — browser automation entry point
- `create-verification-skill` — turning this into a repeatable project script
- `ship-gate` — where UI evidence is required
