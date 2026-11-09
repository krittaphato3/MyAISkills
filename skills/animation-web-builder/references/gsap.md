# GSAP — timelines, ScrollTrigger, and cleanup

GSAP is the sequencing layer. Its value is not individual tweens; it is the timeline, which lets a
scroll position or a label drive a dozen properties with one source of time.

```js
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)
```

Registration is per page load. Forgetting it is the most common cause of "ScrollTrigger is not
defined" in a bundled app.

## The three shapes worth knowing

**1. Timeline driven by scroll (the workhorse).**

```js
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: section,
    start: 'top top',
    end: '+=1500',
    scrub: 0.5,          // seconds of catch-up; true = hard-locked to scroll
    pin: true,
    anticipatePin: 1,
    invalidateOnRefresh: true,
  },
})
tl.to(headline, { y: 0, opacity: 1, duration: 1 })
  .to(cards, { y: 0, opacity: 1, stagger: 0.08 }, '<0.2')
```

**2. Batched reveal for lists.** `ScrollTrigger.batch()` groups elements entering in the same frame,
so a 200-row list does not create 200 triggers.

```js
ScrollTrigger.batch('.card', {
  start: 'top 85%',
  onEnter: (batch) => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.06, overwrite: true }),
})
```

**3. Scoped setup with cleanup.** In React, `useGSAP()` from `@gsap/react` reverts every animation
and trigger created inside it on unmount. Without it, route changes leak triggers and the next page
animates against stale elements.

```jsx
import { useGSAP } from '@gsap/react'
useGSAP(() => { /* tweens + ScrollTrigger here */ }, { scope: containerRef })
```

## ScrollTrigger options that change behaviour

| Option | Effect | When it matters |
|---|---|---|
| `scrub: true` | Progress maps 1:1 to scroll | Frame-by-frame sequences |
| `scrub: 0.5` | 0.5 s of easing catch-up | Text and cards; feels less rigid |
| `pin: true` | Fixes the element for the duration | Full-screen sections |
| `anticipatePin: 1` | Pins slightly early on fast scroll | Removes the one-frame jump on entry |
| `invalidateOnRefresh` | Recomputes start/end values on resize | Any responsive layout |
| `markers: true` | Debug start/end lines | Development only — never ship |
| `toggleActions` | `onEnter onLeave onEnterBack onLeaveBack` | Non-scrubbed reveals |
| `snap` | Snaps to labelled progress points | Section-per-screen designs |
| `fastScrollEnd` | Skips intermediate states on a flick | Long pages with many triggers |

After any layout change (images loading, accordion opening, fonts swapping) call
`ScrollTrigger.refresh()`. Most "animations are misaligned" bugs are a missing refresh.

## Performance rules

- Animate **`transform` and `opacity`** only. `top`, `left`, `width`, `height`, `margin` trigger layout.
- Use `x`/`y` and `scale` rather than `left`/`top` and `width`.
- Add `will-change: transform` sparingly — one per animated layer, removed when the animation ends.
- Prefer `stagger` over N separate timelines.
- A `scrub` timeline with 200 tweens is a scroll-jank machine; collapse to a handful of properties.
- Kill what you created: `ctx.revert()` or `useGSAP`, plus `ScrollTrigger.getAll().forEach(t => t.kill())`
  in a hand-rolled cleanup.

## Failure modes

| Failure | Mechanism | Symptom |
|---|---|---|
| Plugin not registered | Bundler split, registration in another chunk | `ScrollTrigger is not defined` |
| No refresh after async layout | Start/end computed on stale heights | Sections overlap or trigger late |
| Pinned element inside `overflow: hidden` | Pin needs the scroll container | Pin does not stick, page jumps |
| Transforming an ancestor of a pinned element | Breaks `position: fixed` math | Pin offset drifts |
| Timelines recreated on every render | No scope/cleanup | Animations stack, double speed after navigation |
| `markers: true` shipped | Debug left in | Orange lines in production |
| Animating layout properties | Layout thrash per frame | 20-30 fps on a simple fade |

## Verification

- [ ] Scroll the full page at speed and at 25% CPU throttle: no jump at pin boundaries.
- [ ] Resize from mobile to desktop width: triggers recompute, nothing overlaps.
- [ ] Navigate away and back: no duplicate animations, no leaked triggers
      (`ScrollTrigger.getAll().length` returns to its prior value).
- [ ] `prefers-reduced-motion: reduce` shows final states with no scrub.
- [ ] No `markers: true` in the built bundle.
