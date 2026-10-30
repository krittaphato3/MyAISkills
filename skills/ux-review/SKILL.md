---
name: ux-review
description: >-
  Reviews a live interface for usability and interaction quality: Nielsen heuristics, full state
  coverage (loading, empty, error, permission, offline, long content), affordances and microcopy,
  motion intent and reduced motion, keyboard and focus sanity, and responsive behavior at real
  viewports. Use when a screen is "done" and needs a quality pass, when users report confusion, or
  when a flow crosses several screens. Formal conformance audits route to accessibility-audit;
  visual craft (color, type, hierarchy) to refactoring-ui; spacing math to ui-layout-spacing.
metadata:
  version: 1.1.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: design-critic
---

# UX Review

Screens pass tests and still fail people: the empty state says "no data", the error says "an error
occurred", the primary action is a gray label, the spinner never resolves. This skill is the
review pass that catches those — on the running interface, with evidence, before users do.

## WHEN TO USE

- A view or flow is implemented and about to ship.
- Users report confusion, dead ends, or "I can't find it" for an existing screen.
- A flow crosses screens (create → confirm → result) and the seams have not been walked.
- Motion or microcopy was added and needs an intent check.

## WHEN NOT TO USE

- Pure visual craft: color, type scale, hierarchy — `refactoring-ui` and `impeccable`.
- Formal WCAG conformance evidence — `accessibility-audit`.
- Spacing rhythm, gaps, concentric radii — `ui-layout-spacing`.
- Backend-only changes with no user surface.

## METHOD (drive the real interface)

```text
1. RUN IT
   Open the app and walk the flow as a user at 375 / 768 / 1280 CSS pixels.
   Record steps + screenshots for every BLOCKER/MAJOR finding. A finding without a
   reproduction is an opinion.

2. HEURISTIC PASS (review prompts, not a rubric to score)
   Visibility of system state · match the user's language · user control and escape routes ·
   consistency and conventions · error prevention · recognition over recall · flexibility and
   efficiency · aesthetic and minimalist design · recognize and recover from errors · help.

3. STATE INVENTORY (per view)
   default · loading · empty · sparse · dense/long content · error (network, validation,
   permission) · offline · read-only/permission denied.
   Any missing applicable state is a finding with the same status as a visual bug.

4. INTERACTION DETAILS
   Keyboard: every control reachable and operable; focus visible and never trapped; Escape
   closes overlays; destructive actions confirm or offer undo. Targets ≥24px (WCAG 2.2 AA
   minimum). Motion honors prefers-reduced-motion; transitions are interruptible and under
   ~300ms for frequent actions.

5. MICROCOPY
   Labels read as the user's language. Errors say what happened, why, and the next step.
   Destructive confirmations name the object being destroyed.

6. SEVERITY-RANK AND HAND OFF
   BLOCKER: task impossible or data at risk (crash, dead end, silent failure).
   MAJOR: confusion, wrong default, unreachable control, missing state.
   MINOR: polish and consistency.
   ≤12 findings, each with steps, severity, and suggested resolution. No edits from the
   reviewer: findings go to the implementer (ui-ux-architect / frontend-web-engineer).
```

## PATTERNS

- **Empty state formula** — what belongs here + why it is empty (when non-obvious) + one next
  action. Never "no results" while data is still loading.
- **Loading** — skeleton for structure, spinner only for short waits; no fake progress bars.
- **Error recovery** — inline, specific, recoverable; preserve the user's input.
- **Destructive action** — confirm with the object named, or act and offer undo for a window.
- **Permission state** — say who can grant access, with the path.
- **Motion** — animate state changes that could be missed; never animate on a path the user
  hits every minute. Transform/opacity only; no layout thrash.
- **Interruptibility** — a fast user can click through during the animation; the UI must land
  in a consistent state either way.

## FAILURE MODES & MITIGATIONS

1. **Happy-path review** — only the seeded demo state was walked. *DETECT:* no empty/error
   findings. *FIX:* state inventory per view; walk each state.
2. **Side-effect review** — reviewing code, not the running UI. *DETECT:* findings cite JSX, not
   behavior. *FIX:* drive the real surface; screenshots per finding.
3. **Decorative motion** — animation on frequent actions slowing the user. *DETECT:* wait times
   added to repetition. *FIX:* motion only where state change could be missed.
4. **Hover-only affordances** — actions discoverable only with a mouse. *DETECT:* keyboard pass
   misses them. *FIX:* visible affordance; hover is enhancement, not the mechanism.
5. **Cliché polish** — fashionable treatments that erase product character (the "AI look").
   *DETECT:* the redesign could belong to any product. *FIX:* preserve the existing visual
   direction; add craft within it (`impeccable`).
6. **Finding flood** — 40 untriaged nits. *DETECT:* no severity column. *FIX:* cap at 12,
   severity-ranked, reproducibility required for BLOCKER/MAJOR.

## QUANTITATIVE RULES

- ≥3 viewport widths walked; keyboard pass on every changed control.
- Every new or changed view has its applicable states enumerated; ≥1 non-default state exercised.
- Findings capped at 12, severity-ranked, each with reproduction steps.
- Motion: ≤300ms for frequent interactions; reduced-motion honored everywhere it appears.
- Review is read-only: no fixes inside the review pass.

## VERIFICATION GATE

- [ ] The interface was driven live; BLOCKER/MAJOR findings carry screenshots and steps.
- [ ] State inventory filled per view; missing states are named findings.
- [ ] Keyboard and focus pass done; reduced-motion spot-check done.
- [ ] Microcopy issues listed with suggested replacement text.
- [ ] Findings severity-ranked and handed to an implementer; nothing silently fixed.

## REFERENCES

- `references/ui-conformance-checklist.md` — the itemized pass to run alongside the heuristics
- `accessibility-audit` — formal WCAG 2.2 AA conformance
- `refactoring-ui`, `impeccable`, `ui-layout-spacing` — visual craft and layout
- `frontend-web-engineer` — implementation of accepted findings
- `design-critic` (agent) — runs this review; `ui-ux-architect` — builds the fix
