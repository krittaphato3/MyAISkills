---
name: web-performance
description: >-
  Diagnoses and fixes browser performance: Core Web Vitals (LCP, INP, CLS), bundle and hydration
  cost, image/font loading, render blocking, caching, and third-party scripts, measured lab and
  field. Use when a page is slow, scores poorly, or a performance budget must be met or defended.
  Server-side CPU/memory profiling routes to performance-profiler; SQL slowness to
  query-performance-engineer; scroll animation budgets to animation-web-builder.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: ui-ux-architect
---

# Web Performance

Users experience latency as a single number; browsers measure it as several. Optimize the metric
that is actually failing, at the percentile that matters (p75), with a before/after measurement —
not the one that is easiest to improve.

## WHEN TO USE

- A page feels slow, Lighthouse/PSI is red, or a Core Web Vitals alert fired.
- Bundle size, hydration, or client JS cost is the suspected cause.
- Setting performance budgets for a new page or feature.
- A performance claim must be proven ("this made it faster").

## WHEN NOT TO USE

- Server/DB latency — `performance-profiler` or `query-performance-engineer`.
- Perceived-speed polish with no measurable target yet — define the metric first.
- Animation smoothness budgets — `animation-web-builder` (this skill covers the page around it).
- You cannot measure: fix observability first (`observability-sre`), then come back.

## DECISION TREE

```text
1. WHICH METRIC FAILS?
   LCP  → loading: server response, render-blocking assets, hero image/font, client render.
   INP  → interaction: long tasks, heavy hydration, large event handlers, layout thrash.
   CLS  → stability: unsized media, injected banners, font swap, late layout shifts.
   TTFB → server/infra: caching, origin latency, redirects, CDN miss.
   Field vs lab disagree → trust field for users, lab for reproduction.

2. REPRODUCE WITH A TRACE
   Same device class, throttling, cache state, and build as the complaint. Save the trace.
   A number without a trace is an anecdote.

3. FIND THE LONGEST POLE
   Attribute time: network waterfall → main-thread tasks → render/layout → paint.
   Fix the dominant contributor first; micro-optimizing the second is waste.

4. APPLY THE SMALLEST STRUCTURAL FIX
   Load less, load later, load from closer, or render less. Prefer removing work over
   speeding it up. See PATTERNS.

5. VERIFY AT p75, SAME CONDITIONS
   ≥5 runs, median + p75, pinned build and throttle. Report delta and absolute value.
   A win in one lab run is noise until repeated.

6. GUARD THE WIN
   Add a budget check (bundle size, LCP assertion in CI, or a perf test) so it does not regress.
```

## PATTERNS

### 1. Targets (p75, mobile)
| Metric | Good | Needs work | Poor |
|---|---|---|---|
| LCP | ≤2.5s | 2.5–4.0s | >4.0s |
| INP | ≤200ms | 200–500ms | >500ms |
| CLS | ≤0.1 | 0.1–0.25 | >0.25 |
| TTFB | ≤800ms | 0.8–1.8s | >1.8s |

Treat these as gates, not aspirations: a regression past "good" blocks release unless explicitly
accepted with a reason.

### 2. LCP playbook
- Identify the LCP element first (it is often not the hero image you assume).
- Server: cache HTML/CDN, cut redirects, stream or prerender where it helps.
- Image: correct dimensions, modern format (AVIF/WebP), `srcset`/`sizes`, `fetchpriority="high"`,
  never lazy-load the LCP image.
- Fonts: `font-display: swap`, preload the one critical face, subset, self-host when possible.
- CSS/JS: remove render-blocking imports from the critical path; inline only truly critical CSS.
- Client-rendered hero: SSR/SSG it, or render a static shell first.

### 3. INP playbook
- Find long tasks (>50ms) in the trace; break them up or defer them.
- Reduce hydration: server components/islands, `client:visible`, lazy boundaries.
- Event handlers: do less synchronously; yield before expensive work; debounce input.
- Avoid layout thrash (read/write batching) and giant lists without virtualization.

### 4. CLS playbook
- Width/height or `aspect-ratio` on every image/video/iframe.
- Reserve space for ads, banners, and async content.
- Avoid inserting DOM above existing content; use transforms for animation.
- Font metrics: `size-adjust`/fallback matching to reduce swap shift.

### 5. Budgets
```text
JS shipped (initial):      ≤170KB gzip  (target; justify above)
CSS:                       ≤50KB gzip
Hero image:                ≤200KB, dimensions known
Third-party scripts:       ≤1 blocking; each needs an owner and a reason
LCP p75:                   ≤2.5s on mid-tier mobile
```
Budgets belong in CI (bundle-size check, Lighthouse budget file), not in a wiki.

### 6. Third parties
Every third-party script is someone else's performance problem shipped to your users. Load async,
self-host what can be, remove what nobody uses, and measure the delta when adding one.

## FAILURE MODES & MITIGATIONS

1. **Metric whack-a-mole** — LCP improved, INP regressed. *DETECT:* only one metric reported.
   *FIX:* report all three plus TTFB; gate on the full set.
2. **Lab-only win** — local Lighthouse green, field red. *DETECT:* no field data or no throttling.
   *FIX:* reproduce with mobile throttle + cold cache; check field p75.
3. **Unverified claim** — "should be faster now". *DETECT:* no before/after numbers. *FIX:* ≥5 runs,
   median + p75, same build conditions.
4. **Lazy-loading the LCP** — `loading="lazy"` on the hero. *DETECT:* LCP image has lazy attr.
   *FIX:* eager + high priority.
5. **Bundle blindness** — adding a library for one function. *DETECT:* bundle delta unmeasured.
   *FIX:* check the size before merging; prefer native/platform APIs.
6. **Regression by default** — no budget, so every release adds weight. *DETECT:* size trend up.
   *FIX:* CI budget with a hard threshold.

## QUANTITATIVE RULES

- Report p75 (and median) over ≥5 runs, pinned build, mobile throttling.
- One dominant fix per iteration; measure after each, stop when the gate passes.
- Initial JS ≤170KB gzip, CSS ≤50KB; any increase >10KB needs justification in the PR.
- No more than one blocking third-party script on the critical path.
- LCP/INP/CLS must all be in "good" at p75 before a performance task is called done.

## VERIFICATION GATE

- [ ] The failing metric was identified from field or reproduced lab data, with a trace saved.
- [ ] Before/after numbers exist at p75 with identical conditions.
- [ ] The fix addresses the dominant contributor, evidenced by the trace.
- [ ] All three Core Web Vitals + TTFB are reported, not just the improved one.
- [ ] A budget or assertion guards the improvement against regression.

## REFERENCES

- `frontend-web-engineer` — implementation of the page
- `animation-web-builder` — frame budget for scroll/motion work
- `performance-profiler` — CPU/memory/IO on the server
- `observability-sre` — field RUM instrumentation and alerting
