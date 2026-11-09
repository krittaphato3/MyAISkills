---
name: react-bits
description: >-
  Adds React Bits animated components to a React app: text effects (split, blur, gradient, shiny),
  animated backgrounds (aurora, particles, threads, grid), magnetic and spark buttons, and card
  micro-interactions, installed through the shadcn registry in JS or TS with CSS or Tailwind. Use
  when a marketing or landing surface needs a designed animation and you want a vetted component
  rather than a blank GSAP timeline. Scroll storytelling routes to animation-web-builder.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: ui-ux-architect
---

# React Bits

React Bits is not an npm dependency you import. It is a registry of components you **copy into your
repository** and then own — source, styles, and all. That changes the cost model: installation is
free, maintenance is yours.

`npx shadcn@latest add @react-bits/SplitText-TS-TW`

The suffix is the flavour: `JS-CSS`, `JS-TW`, `TS-CSS`, `TS-TW`. Pick the one matching the project
before installing; converting afterwards is a manual rewrite.

## WHEN TO USE

- A landing, pricing, or marketing page needs one expressive element (a headline treatment, an
  ambient background) and no design system component exists for it.
- Building a hero section, product launch page, or waitlist page where motion is the point.
- A text effect is wanted for a specific phrase and the alternative is hand-rolling per-character
  spans and a stagger.
- The team wants a starting point for a micro-interaction (magnetic button, click spark, tilt card)
  that will be adapted, not used verbatim.

## WHEN NOT TO USE

- Application UI: forms, tables, settings, dashboards, modals. Use the design system; animated
  primitives here are a liability and an inconsistency.
- The requirement is scroll-driven sequencing across sections, pinned panels, or an image-sequence
  canvas. That is `animation-web-builder`, which owns the scroll narrative.
- The animation must be accessible-by-construction and the library has no reduced-motion path.
- You need to redistribute the components themselves (see the license caveat below).

## DECISION TREE

```text
What are you adding?
├─ a headline or short phrase needs character-level motion ..... Text Animation (SplitText, BlurText, GradientText, ShinyText)
├─ the page needs ambient depth behind content ................. Background (Aurora, Particles, Threads, Grid, Beams)
├─ a primary CTA needs tactility ............................... Micro interaction (Magnet, ClickSpark, StarBorder)
├─ a card or panel needs presence .............................. Component (tilt, glare, spotlight)
└─ punctuation on a scroll narrative ........................... animation-web-builder, then embed the result

Can you afford it?
├─ bundle budget has headroom (< 50 KB gzip for the effect) .... proceed, mark the import lazy
├─ effect draws on a canvas or WebGL ........................... measure fps on a mid-tier phone first
└─ no headroom ................................................. CSS-only alternative or drop it
```

### Install flavours

| Flavour | Use when |
|---|---|
| `TS-TW` | TypeScript + Tailwind — the common case |
| `TS-CSS` | TypeScript + CSS modules or global CSS |
| `JS-TW` | JavaScript codebase with Tailwind |
| `JS-CSS` | JavaScript with plain CSS |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Vendored code rots | Copied component diverges from upstream with no update path | Vendor deliberately: rename, add a header comment with source and version, treat as your code |
| Bundle bloat | Several backgrounds imported at module scope | `React.lazy` + `Suspense`, one effect per route |
| GPU meltdown on mobile | Canvas/WebGL background plus full-screen filter | Cap particle count, `dpr` clamp, disable under a width/`matchMedia` threshold |
| Motion sickness | Animation runs regardless of user preference | Honour `prefers-reduced-motion`: freeze to the final frame, never remove content |
| Hydration mismatch | Random seeds generated during render, SSR HTML differs | Seed deterministically or render client-only |
| Illegible text | Animated background behind body copy | Put copy on a solid or heavily scrimmed surface; never on raw particles |
| Contrast regression | Gradient text loses contrast at one end of the ramp | Both gradient stops must pass 4.5:1 on the actual background |
| License surprise | Components resold or redistributed in a template | MIT + Commons Clause: use freely in products, do not sell or redistribute the components |
| Design system collision | Three animation idioms across two pages | Pick one effect vocabulary; document it |

## QUANTITATIVE RULES

- **≤ 1 ambient background per page**, ≤ 3 animated elements per viewport.
- **≤ 50 KB gzip** added initial JS per effect; lazy-load anything above.
- **60 fps on a mid-tier mobile device**, 30 fps absolute floor; measure, do not assume.
- **Every animated component ships a reduced-motion path.** No exceptions.
- **Text contrast ≥ 4.5:1 at every point of the animation**, not just the resting state.
- **Vendored files carry source URL + version** in a header comment.

## VERIFICATION GATE

- [ ] Installed in the matching flavour; the build has no unused JS/CSS flavour twins.
- [ ] `prefers-reduced-motion: reduce` renders the final state with no animation.
- [ ] SSR/hydration produces no mismatch warning in the console.
- [ ] Bundle delta measured and under budget; effect is lazy-loaded if it is not above the fold.
- [ ] Frame rate measured on a throttled mobile profile, recorded in the PR.
- [ ] Text over the effect passes contrast at both ends of any gradient.
- [ ] License respected: components used inside the product, not redistributed as components.

## REFERENCES

- `animation-web-builder` for scroll-driven sequences, pinned sections, and GSAP/ScrollTrigger work.
- `ui-layout-spacing` for the spacing and composition the motion sits inside.
- `accessibility-audit` for reduced-motion, contrast, and focus behaviour under animation.
- `web-performance` for bundle and Core Web Vitals impact.
- Upstream: <https://reactbits.dev> and <https://github.com/DavidHDev/react-bits>
