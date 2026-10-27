---
description: Review the running interface for usability, state coverage, keyboard, motion, and microcopy
argument-hint: <screen, flow, or URL>
---

Run `ux-review` via `design-critic` (read-only):

1. Drive the real surface at 375 / 768 / 1280 CSS pixels; screenshot every BLOCKER/MAJOR finding.
2. Heuristic pass (visibility of state, user language, escape routes, consistency, error
   prevention, recognition over recall) and a state inventory per view: default · loading ·
   empty · error · permission · offline · long content.
3. Keyboard and focus pass on every changed control; reduced-motion spot-check; target sizes ≥24px.
4. Microcopy review with suggested replacement text; destructive actions name their object.
5. Severity-rank ≤12 findings with reproductions. Fixes route to `ui-ux-architect` /
   `frontend-web-engineer`; formal WCAG conformance to `accessibility-audit`.

Target: $ARGUMENTS
