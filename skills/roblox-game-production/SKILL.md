---
name: roblox-game-production
description: >-
  Runs a Roblox game from concept to publishable build: scope a vertical slice, sequence systems and
  content, hand off between code/art/UI/audio specialties, gate each milestone, and decide what to
  cut. Use when starting a Roblox project, planning a feature set, or coordinating several Roblox
  specialists. Single-discipline work routes to that discipline's skill; Studio execution to
  roblox-studio-mcp.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-game-director
---

# Roblox Game Production

Roblox projects die from scope, not from missing features. The platform makes the first hour feel
productive — parts, terrain, a HUD, a RemoteEvent — and then the game has no loop, no reason to
return, and forty half-finished systems. This skill is the production discipline that keeps a build
shippable: one loop, one vertical slice, then depth.

## WHEN TO USE

- Starting a new Roblox experience or a major mode.
- Turning a one-line idea ("a parkour obby with pets") into a scoped feature set.
- Coordinating several specialists on one place (code, world, UI, animation, VFX, assets, QA).
- Deciding whether to add a feature, cut it, or ship what exists.
- A project that has grown but cannot be published.

## WHEN NOT TO USE

- A single well-scoped feature in an existing game — route to the discipline skill.
- Pure Studio mechanics (tool calls, playtests) — `roblox-studio-mcp`.
- Monetization policy or legal questions — research current Roblox requirements; this skill covers
  product shape, not platform policy.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. NAME THE LOOP
   One sentence: "Player does {verb} to get {reward}, which lets them {next verb}."
   If you cannot name it, there is no game yet — do not build systems.
   Define the session: first 60 seconds, one session (5-15 min), and why they return.

2. SCOPE THE VERTICAL SLICE
   The smallest build that proves the loop end to end: one map area, one core mechanic, one reward,
   one save, one HUD, one sound/VFX pass. Everything else is post-slice.
   Write the cut list at the same time as the build list.

3. ORDER THE WORK
   Foundation → loop → feedback → persistence → content → polish.
   Foundation: folder layout, remotes convention, data schema, UI shell, build/test loop.
   Never build content before the loop earns it.

4. ASSIGN OWNERS (one per deliverable)
   code → roblox-scripter · world → roblox-builder · UI → roblox-ui-designer ·
   animation → roblox-animator · VFX/audio → roblox-vfx-artist · assets → roblox-asset-artist ·
   security review → roblox-security-engineer · test/playtest → roblox-qa-engineer.
   The director integrates and gates; it does not do every discipline's work.

5. GATE EACH MILESTONE
   M0 playable: loop works in a playtest, console clean.
   M1 fun-check: the loop is understandable without explanation and has a reason to repeat.
   M2 durable: saves survive rejoin/crash; economy cannot be duplicated.
   M3 polished: UI scales on phone/tablet/desktop/console; VFX within budget; audio mixed.
   M4 shippable: security review passed, perf measured on low-end, failure paths handled.

6. INTEGRATE IN STUDIO, IN ORDER
   Pull each specialist's change into the place, verify it in the same session, then move on.
   One integration at a time; a broken merge is cheaper to find alone.

7. CUT OR SHIP
   At each gate ask: does this serve the loop? If not, cut it and record why.
   Shipping a small complete game beats an ambitious unplayable one.
```

## PATTERNS

### 1. One-page game brief (write this before code)
```text
TITLE: {working name}
LOOP: {verb → reward → next verb}
SESSION: {first 60s | typical 10 min | return reason}
PLAYERS: {solo | co-op | competitive}   DEVICES: {phone, tablet, desktop, console}
CORE SYSTEMS: {movement, combat, economy, progression, social}
SLICE: {map area, mechanic, reward, save, HUD, one audio/VFX pass}
CUT LIST: {features explicitly not in v1, and why}
SUCCESS TEST: {what a playtester must be able to do unaided}
RISKS: {top 3 + mitigation}
```

### 2. Build order that avoids rework
1. **Project skeleton** — folder layout, shared config/types, remote naming, data schema version.
2. **Loop prototype** — the core verb, server-authoritative, no polish.
3. **Feedback** — UI state, sound, VFX, animation cues for the verb.
4. **Persistence** — save/load with session locking; verify rejoin.
5. **Content** — maps, items, progression curves.
6. **Polish** — camera, lighting, transitions, mobile/console passes.
7. **Hardening** — security review, perf, failure paths, analytics hooks.

### 3. Specialist handoff contract
Every handoff states: deliverable path(s) in the DataModel, acceptance test, performance budget,
dependencies, and what is explicitly out of scope. Example:
```text
HANDOFF UI ← code
Paths: StarterGui.HUD (ScreenGui), ReplicatedStorage.Shared.Remotes
Contract: HUD.UpdateHealth(number), HUD.SetCoins(number); no client trust
Acceptance: values update within 1 frame of server change; scales at 320×480 and 1920×1080
Budget: ≤80 GUI objects visible; no per-frame layout recalculation
Out of scope: inventory screen (v2)
```

### 4. Scope math
Estimate in "sessions of work", not hours. If the slice needs more than ~5 sessions, cut until it
does not. A Roblox game can ship with one polished loop and three maps; it cannot ship with ten
systems at 60%.

### 5. Fun-check protocol
Silent playtest: a person who has not seen the design plays for 3 minutes.
Record: what they did first, where they stopped, what they asked. If they ask "what do I do?", the
UI or the loop failed — not the player. Fix the loop before adding content.

### 6. Definition of done for a Roblox milestone
Playable from a fresh Studio playtest · console clean · saves survive rejoin · mobile layout verified ·
no known economy exploit · VFX/particles within budget · every remote validated server-side.

## FAILURE MODES & MITIGATIONS

1. **System-first building** — inventory, pets, shops before the core verb. *DETECT:* no playable loop
   after days of work. *FIX:* stop, build the slice, return to systems only if the loop needs them.
2. **Feature creep at the gate** — "while we're here" additions. *DETECT:* slice scope grows every
   review. *FIX:* cut list is binding; new ideas go to v2 with a date.
3. **Unverified integration** — specialists' work merged without a playtest. *DETECT:* first full
   playtest happens at the end. *FIX:* integrate + verify per change.
4. **Client-trust economy** — currency or rewards computed on the client. *DETECT:* server accepts
   deltas. *FIX:* `roblox-security` review before M2.
5. **Content before feel** — ten maps, movement feels bad. *DETECT:* playtesters quit in the first
   minute. *FIX:* polish the core verb; content multiplies feel, it cannot create it.
6. **No persistence test** — saves lost on rejoin. *DETECT:* only tested in one session. *FIX:* rejoin
   test at M2, including crash/shutdown.
7. **Device blindness** — desktop-only UI and effects. *DETECT:* no phone/tablet/console pass.
   *FIX:* responsive UI + low-quality VFX fallback before M3.

## QUANTITATIVE RULES

- One loop per game; ≤5 core systems in v1.
- Vertical slice ≤5 work sessions; if larger, cut.
- Content after the loop passes the fun-check, never before.
- Each milestone gate has a playtest artifact (console output + screenshot + notes).
- Every remote and currency path gets a security review before M2.
- Performance measured on the lowest target device before M4, not after launch.

## VERIFICATION GATE

- [ ] Loop sentence and session shape written.
- [ ] Slice scope + cut list exist and are honored.
- [ ] Every deliverable has one owner and an acceptance test.
- [ ] Milestone gate evidence attached (playtest, console, screenshot, notes).
- [ ] Persistence verified across rejoin; economy reviewed server-side.
- [ ] UI verified on phone, tablet, desktop (console if targeted).
- [ ] Report states what shipped, what was cut, and what remains unverified.

## REFERENCES

- `roblox-studio-mcp` — how work is executed and verified in Studio
- `roblox-scripting` · `roblox-world-building` · `roblox-ui-ux` · `roblox-animation` ·
  `roblox-vfx` · `roblox-assets` · `roblox-security` · `roblox-testing`
- `deep-planner` — task graph and risk register for larger builds
- `debate-protocol` — when a design or architecture choice is genuinely contested
