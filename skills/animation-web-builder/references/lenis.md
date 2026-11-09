# Lenis — smooth scrolling

Smooth scroll is a global input transform. It touches every scroll listener on the page, so it is
either integrated once at the app shell or not at all. Half-installing it produces double-eased,
laggy scrolling.

Package: `lenis` (v1+). React binding: `lenis/react` exports `ReactLenis` and `useLenis`.

## Setup

```js
import Lenis from 'lenis'

const lenis = new Lenis({
  duration: 1.2,        // seconds of easing; lower is tighter
  smoothWheel: true,
  syncTouch: false,     // true = smooth on touch too; usually worse on mobile
  wheelMultiplier: 1,
  touchMultiplier: 1.5,
})

function raf(time) {
  lenis.raf(time)
  requestAnimationFrame(raf)
}
requestAnimationFrame(raf)
```

React, at the shell:

```jsx
import { ReactLenis } from 'lenis/react'

export default function App({ children }) {
  return (
    <ReactLenis root options={{ duration: 1.2, smoothWheel: true }}>
      {children}
    </ReactLenis>
  )
}
```

## Integrating with GSAP ScrollTrigger

GSAP's ticker must drive Lenis, and ScrollTrigger must re-read Lenis' scroll position. Otherwise
ScrollTrigger samples the native scroll and the animation desynchronises by the easing duration.

```js
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)

lenis.on('scroll', ScrollTrigger.update)

gsap.ticker.add((time) => {
  lenis.raf(time * 1000)      // gsap ticker is seconds, lenis wants ms
})
gsap.ticker.lagSmoothing(0)   // required: otherwise GSAP hides the lag and scroll stutters
```

Do **not** keep a separate `requestAnimationFrame` loop once the ticker drives Lenis. Two loops
double-step the easing.

## Required behaviours

| Need | API | Note |
|---|---|---|
| Stop scrolling behind a modal | `lenis.stop()` / `lenis.start()` | Restore on unmount, and on route change |
| Nested scroll area inside a smooth page | `data-lenis-prevent` on the inner element | Without it the inner container does not scroll |
| Anchor links | `lenis.scrollTo('#section', { offset: -80 })` | Native anchors jump and bypass the easing |
| Scroll to top on route change | `lenis.scrollTo(0, { immediate: true })` | Otherwise the new route opens mid-page |
| Cleanup | `lenis.destroy()` | React: `useLenis` handles it; raw usage must not leak |
| Responsive disable | `lenis.destroy()` under a breakpoint or reduced-motion | Mobile touch smoothing is usually a regression |

## Failure modes

| Failure | Mechanism | Symptom |
|---|---|---|
| Two RAF loops | Custom `requestAnimationFrame` plus `gsap.ticker` | Scroll overshoots or stutters |
| ScrollTrigger not synced | No `lenis.on('scroll', ScrollTrigger.update)` | Pinned sections drift, markers mismatch |
| `lagSmoothing` left on | GSAP clamps large deltas | Visible jump after a tab regains focus |
| Fixed element inside a transformed wrapper | Ancestor `transform` breaks `position: fixed` | Header scrolls away, pin behaves oddly |
| `overflow: hidden` on `html`/`body` | Kills Lenis' scroll source | Page does not scroll at all |
| Reduced motion ignored | Smoothing always on | Vestibular discomfort; WCAG 2.3.3 concern |
| Inner scroll containers unmarked | Wheel events captured by Lenis | Dropdowns and code blocks cannot scroll |

## Budget

Smooth scroll is cheap on the main thread but it makes **every** scroll-linked computation run
through the same easing. Measure with the CPU profiler while scrolling a section that has a
ScrollTrigger, not on an empty page.

- Target 60 fps during scroll; 50 fps floor on mid-tier mobile.
- Disable `syncTouch` below tablet width unless the design explicitly needs it.
- Respect `prefers-reduced-motion: reduce` by destroying Lenis and falling back to native scroll.
