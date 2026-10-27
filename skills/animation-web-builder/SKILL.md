---
name: animation-web-builder
description: >-
  Builds scroll-driven, motion-rich web experiences: image-sequence canvas animation, GSAP
  ScrollTrigger, parallax, section transitions, and performance-budgeted motion. Use when
  a landing or marketing page needs immersive scroll storytelling or a 60fps animation
  budget. Routine UI transitions, layout, and component work route to
  frontend-web-engineer.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: ui-ux-architect
---

# Animation Web Builder

Build Awwwards-level animated websites with scroll-driven frame animations and immersive motion design.

## Core Technique: Apple-Style Image Sequence Animation

See `references/image-sequence.md` (FFmpeg frame extraction + preload + canvas + GSAP ScrollTrigger component) — the 4-step pipeline: video→frames→preload→scroll-draw.

## Performance Budget

- **Target**: 60fps scroll animation
- **Frame count**: 100-200 frames per section (5-7 seconds at 30fps)
- **Image size**: 800-1200px wide, JPG quality 60-80%
- **Preloading**: ALL frames must be loaded before animation starts
- **Canvas size**: Match display size, not source size
- **Memory**: ~50MB for 150 frames at 1200px wide JPG

## GSAP ScrollTrigger Integration

```javascript
// Link canvas frame playback to scroll
ScrollTrigger.create({
  trigger: sectionElement,
  start: 'top top',
  end: '+=2000', // 2000px of scroll distance
  scrub: 0.5, // smooth lag
  pin: true, // pin the section
  onUpdate: (self) => {
    const frame = Math.floor(self.progress * totalFrames)
    drawFrame(frame)
  },
})
```

## Section Transition Patterns

### Cross-fade between sections
```javascript
// Fade out section A, fade in section B
gsap.to(sectionA, {
  opacity: 0,
  scrollTrigger: {
    trigger: sectionB,
    start: 'top bottom',
    end: 'top center',
    scrub: true,
  },
})
```

### Parallax layers
```javascript
gsap.to(foregroundLayer, {
  y: -100,
  scrollTrigger: {
    trigger: section,
    start: 'top bottom',
    end: 'bottom top',
    scrub: true,
  },
})
```

## Asset Pipeline

1. Source video (mp4, 1080p, 30fps)
2. FFmpeg → frame sequence (JPG, quality 3)
3. Organize in `/public/frames/<section>/` directories
4. Component loads frames, canvas renders on scroll
5. Fallback: static image for slow connections

## Key Principles (from Awwwards winners)

- **Pre-render beats real-time**: Bake expensive visuals into frames
- **Separate concerns**: Lenis (scroll) + GSAP (choreography) + Canvas (rendering)
- **Narrative-driven**: Every animation serves the story
- **Performance-first**: Lazy load, device-adaptive quality, RAF budgeting

## WHEN TO USE
- A landing/hero page needs scroll-driven, immersive motion (image-sequence canvas, parallax, pinned sections) at a known performance budget.
- You must orchestrate sections with GSAP ScrollTrigger (pin, scrub, cross-fades) for an Awwwards-level feel.
- You're implementing a video→frame-sequence canvas animation (Apple/Stripe/Linear-style) with scroll scrubbing.
- The asset pipeline (FFmpeg frames → preload → canvas draw) must be set up with caching and a static fallback.

## WHEN NOT TO USE
- **A simple static page** — basic interaction or a single fade does not need scroll-driven frame animation; use the platform defaults or a minimal library.
- **A functional dashboard / app UI** — heavy scroll-cinematography on a dense utilitarian UI harms usability; keep it to marketing/story surfaces.
- **Accessibility-sensitive content-oriented pages where motion is a UX risk** — users with vestibular disorders need the prefers-reduced-motion media query respected; if the page is non-entertainment, preserve a static fallback.
- **One-off DOM animation** (a hover pop) — a lightweight lib or CSS transition suffices; this skill is for the scroll-frameworks.

## DECISION TREE
```text
1. MOTION GOAL → scroll-scrubbed video/image-sequence? → canvas technique. Product story + transitions? →
   GSAP ScrollTrigger orchestration. Simple parallax/layers? → GSAP + y/motion, skip frames.
2. ASSET → heavy video? convert to frames/sprite sheet (FFmpeg). Verify frame budget (100-200/section).
3. PRELOAD → all frames loaded before animation starts; handle slow networks with the static fallback image.
4. ORCHESTRATE → GSAP + ScrollTrigger with scrub; bind canvas draw to scroll progress; pin the section.
5. PERFORMANCE → measure 60fps; lazy-load, device-adaptive quality, RAF budgeting; drop frames if needed.
6. REDUCED-MOTION → provide a static fallback honoring the prefers-reduced-motion media query; never force motion.
```
Never start with a heavy canvas until you've confirmed the asset and performance budget allow an animated experience at all.

## FAILURE MODES & MITIGATIONS
- **Frames not fully preloaded → blank/stutter on scroll.**
  DETECT: canvas is empty or flashes until enough frames load; scroll jumps gaps.
  FIX: preload ALL frames into Image objects before first draw, show a static poster, and only start ScrollTrigger once `loaded == frameCount` (see the React component).
- **Oversized assets / memory blowup.**
  DETECT: frame JPGs too large or too many (hundreds of full-res), memory spikes (~50MB+ per section), slow LCP.
  FIX: cap frame size (1200px-ish), use JPG q3, lower fps/frame count (15fps), sprite-sheet to amortize requests, and lazy-load non-hero sections.
- **Frame skipping / wrong frame for scroll position.**
  DETECT: the displayed frame lags or jumps — `Math.floor(progress*frameCount)` misbounds or the sequence index is off-by-one.
  FIX: clamp index to `[0, frameCount-1]`, use `frameCount-1` as the max, and scrub with `scrub: 0.5` to smooth.
- **Scroll stutter from main-thread work.**
  DETECT: scrubbing causes jank because heavy drawing runs on scroll on the UI thread or `requestAnimationFrame` fires for off-screen canvas.
  FIX: keep frame drawing in `rAF` budget, pause when off-screen, and consider `ImageDecoder`/Web Worker for decode if supported.
- **prefers-reduced-motion media query ignored.**
  DETECT: motion-critical users or reviewers fail WCAG because the animation does not provide a reduced-motion fallback.
  FIX: feature-detect the prefers-reduced-motion media query (reduce) and show the static post-frame image; document the fallback in the component.
- **Unmeasured "performance".**
  DETECT: the page claims 60fps but there is no measurement; heap/frame time or LCP is not recorded.
  FIX: record a before/after (frame-rate, LCP, total bytes) and capture a profile as evidence when any optimization is claimed.

## VERIFICATION GATE
- **60fps budget honest**: measure and record the frame rate under target scroll speed and device; no >frame budget dips without a documented tradeoff.
- **No blank first paint**: static fallback shows and the animated canvas becomes visible only once preloaded.
- **Preload complete before animation**: the ScrollTrigger fires only after `loaded == frameCount`; no jank gap.
- **Reduced-motion fallback honors the prefers-reduced-motion media query**: the static image is shown without JS-driven motion.
- **Bytes + LCP within budget**: recorded frames/bytes/decode time match the planned budget; heap spikes bounded.
- **red-team-qa review**: check for memory blowup, skipped frames, and missing reduced-motion support.

## REFERENCES
- GSAP documentation — ScrollTrigger, scrub, pinning.
- MDN — Canvas API, `requestAnimationFrame`, and performance patterns.
- web.dev page lifecycle / animation performance guidance.
- Prefers reduced-motion — MDN accessibility for motion.
- GSAP community scroll-triggered frame/sequence examples.
