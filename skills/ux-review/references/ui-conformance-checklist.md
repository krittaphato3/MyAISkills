# UI conformance checklist

Run this alongside the heuristic pass. Each line is a defect if it fails, not a style preference.
Findings still need a reproduction and a severity; the checklist decides what to look for, not
what matters most.

## Semantics and assistive technology

- [ ] Every interactive element is a real `button`, `a`, or input, not a clickable `div`.
- [ ] One `h1` per view; heading levels descend without gaps.
- [ ] Landmarks present: `header`, `nav`, `main`, `footer`; `main` appears once.
- [ ] Icon-only controls have an accessible name (`aria-label` or visually hidden text).
- [ ] Decorative images and icons are hidden from assistive tech (`alt=""`, `aria-hidden`).
- [ ] Live regions announce async results (`aria-live`), not the whole page.
- [ ] Invalid fields expose `aria-invalid` and point at their error with `aria-describedby`.
- [ ] Toggles expose state (`aria-pressed` or `aria-checked`), not just color.
- [ ] Tables use `th` with `scope`; layout tables do not exist.
- [ ] Page has a `lang` attribute matching the content.

## Forms

- [ ] Every input has a visible `label`, associated by `for`/`id`.
- [ ] `autocomplete` is set for name, email, tel, address, and password fields.
- [ ] `type` is correct: `email`, `tel`, `url`, `number`, `search`.
- [ ] `inputmode` set where the mobile keyboard matters.
- [ ] Validation runs on submit or blur, not on every keystroke.
- [ ] Errors are inline, specific, and preserve what the user typed.
- [ ] Required fields are marked in text, not only with an asterisk.
- [ ] Submit is disabled only while actually submitting, and says why it is disabled.
- [ ] Password fields offer reveal, and paste is not blocked.
- [ ] Enter submits; a multi-line field does not submit on Enter.
- [ ] Double submit cannot create two records.

## Keyboard and focus

- [ ] Every action works without a mouse, in a sensible tab order.
- [ ] `:focus-visible` is styled and clearly visible on every control.
- [ ] Focus is never trapped outside a modal; Escape closes overlays.
- [ ] Opening a modal moves focus into it; closing returns focus to the trigger.
- [ ] Route changes move focus to the new heading or main region.
- [ ] Skip-to-content link exists on long pages.
- [ ] Custom widgets implement the expected arrow-key behavior, or use the native element.
- [ ] No positive `tabindex`.

## Typography and copy

- [ ] Body text is at least 16px; line length is 45–75 characters.
- [ ] Line height 1.4–1.6 for body copy; tighter only for headings.
- [ ] Numeric columns use tabular figures (`font-variant-numeric: tabular-nums`).
- [ ] Curly quotes and proper dashes in prose; no straight quotes in rendered copy.
- [ ] Ellipsis is a single character where it is a character.
- [ ] No all-caps body text; letter-spacing only on short labels.
- [ ] Truncation has a way to see the full value (tooltip, expand, detail view).
- [ ] Error and empty-state copy says what happened and the next step.

## Images and media

- [ ] `width` and `height` set (or aspect-ratio) so the layout does not shift.
- [ ] Below-the-fold images lazy-load; the hero does not.
- [ ] `srcset`/`sizes` used where the image renders at different widths.
- [ ] Video has captions; autoplay is muted and pausable.
- [ ] Alt text describes purpose, not the file name.

## Layout, motion, and theme

- [ ] No horizontal scroll at 320px.
- [ ] Touch targets at least 24px, ideally 44px on primary actions.
- [ ] Content does not overlap or clip at 200% zoom.
- [ ] Spacing comes from a scale, not arbitrary one-off values.
- [ ] `prefers-reduced-motion` disables non-essential motion.
- [ ] Animations use transform and opacity; no layout thrash.
- [ ] Dark mode sets `color-scheme` so form controls and scrollbars match.
- [ ] Contrast meets 4.5:1 for body text, 3:1 for large text and UI boundaries.

## State, URL, and data

- [ ] Loading, empty, error, offline, and permission-denied states exist where applicable.
- [ ] Filters, tabs, and pagination are reflected in the URL and survive reload.
- [ ] Back and forward restore the previous view, not a reset.
- [ ] Deep links work in a fresh session.
- [ ] Long lists paginate or virtualize; no unbounded render.
- [ ] Destructive actions name the object and confirm or offer undo.

## Locale and formatting

- [ ] Dates, numbers, currency, and relative times use `Intl`, not string concatenation.
- [ ] Layout survives a 30% longer translated string.
- [ ] No text baked into images.
- [ ] Time zones are explicit where a time is shown to another person.

## Console and network

- [ ] No console errors or warnings on a normal path.
- [ ] No failed requests in the network panel.
- [ ] No hydration mismatch warnings.
- [ ] No request waterfalls that block first render.
- [ ] No `console.log` left in shipped code.

## How to report

```text
{BLOCKER|MAJOR|MINOR} {view} @{viewport}
Check:      {the line from this list}
Observed:   {what happened}
Expected:   {what should happen}
Repro:      {steps or screenshot}
```

Cap at 12 findings. Rank by user impact. Hand them to the implementer; the review does not edit.
