---
name: roblox-world-building
description: >-
  Builds Roblox worlds and levels: greybox layouts, parts versus terrain, modular kits, lighting and
  Atmosphere, StreamingEnabled level design, collision and render fidelity, and measured budgets.
  Use when creating or reworking a map, environment, prop set, or lighting mood. Character rigs and
  motion route to roblox-animation; gooey particle work to roblox-vfx; imported meshes and textures
  to roblox-assets.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-builder
---

# Roblox World Building

A Roblox map is a performance contract disguised as art. Every unanchored assembly, every unique
mesh, every shadow-casting part and every oversized model costs frame time on a phone you will never
see. Build the level twice: once as a greybox that proves the space plays well, once as art that
respects the budget.

## WHEN TO USE

- New map, zone, lobby, arena, or obstacle course.
- Reworking traversal, sightlines, cover, or spawn flow.
- Lighting/mood pass (time of day, Atmosphere, post effects).
- World performance problems: long join times, streaming pop-in, frame drops in dense areas.
- Preparing a build for mobile or low-end devices.

## WHEN NOT TO USE

- Character models and animation — `roblox-animation`.
- Particle/beam/trail effects and audio — `roblox-vfx`.
- Mesh/material/texture authoring or Creator Store licensing — `roblox-assets`.
- Terrain-heavy procedural generation code with gameplay logic — pair with `roblox-scripting`.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. WHAT MUST THE SPACE DO?
   List the gameplay verbs it must support (traverse, hide, fight, parkour, shop, spawn).
   Level design starts from verbs, not from a mood board.

2. GREYBOX FIRST
   Block out with anchored Parts on a grid; no textures, no props, no lighting pass.
   Walk it in a playtest. Fix scale, sightlines, and flow before any art time is spent.
   Standard scale: 1 stud ≈ 0.28 m; a Humanoid is ~5 studs tall; door ≈ 7×3 studs.

3. CHOOSE THE MEDIUM PER AREA
   Broad landforms → Terrain (4×4×4-stud voxels).
   Precise structures, modular kits, props → Parts/MeshParts (anchored, welded).
   Never mix both for the same surface; seams and z-fighting are the usual result.

4. MODULARIZE FOR STREAMING
   Group logically/spatially related objects. Keep a static model's extent under ~64 cubic studs so
   it streams as a unit. Static models only for LOD; runtime-mutated or animated models are not.
   One anchor per assembly; weld decorative parts to it.

5. SET THE STREAMING BASELINE
   Workspace.StreamingEnabled = true for large worlds.
   Starting points: StreamingMinRadius 64, StreamingTargetRadius 1024; verify on target devices.
   Scripts must tolerate missing descendants (WaitForChild with timeout).

6. LIGHT AND ATMOSPHERE LAST
   Lighting: ClockTime, Brightness, Ambient/OutdoorAmbient, shadow softness.
   Atmosphere: Density/Haze/Glare/Offset tuned together so distance stays readable.
   Post effects sparingly (`roblox-vfx` for the budget); test at low graphics quality.

7. MEASURE AND CUT
   Playtest from the player's spawn, at density, on the lowest target device or emulator.
   Cut or merge unique assets, shadow casters, and transparent layers until the budget holds.
```

## PATTERNS

### 1. Greybox kit
```text
Workspace.Level/
  Zones/{ZoneName}/          -- one folder per streamable zone
    Geometry/                -- anchored Parts, CanCollide true, CastShadow false by default
    Props/                   -- decorative, welded to an anchor
    Spawns/                  -- SpawnLocation(s)
    Markers/                 -- named parts for scripts (no collision, no render)
```
Markers as invisible anchored parts are how code finds places without hardcoded coordinates.

### 2. Collision and render fidelity
| Object | CollisionFidelity | RenderFidelity | Notes |
|---|---|---|---|
| Walls/floors | Default/Box | Automatic | Cheap, predictable |
| Decorative props | Box or Hull | Automatic | Never Precise unless required |
| Imported mesh hero asset | Hull/Precise only if needed | Automatic/Precise | Precise is expensive |
| Distant set dressing | Box | Automatic | CastShadow false |

Anchored, `CanCollide=false` decoration with `CastShadow=false` is the cheapest visible object.

### 3. Terrain rules
- Sculpt large forms with terrain; do not carve fine detail into voxels (it reads badly and costs).
- Fill in regions, not thousands of tiny operations; chunk large fills with `task.wait()`.
- Prefer terrain materials over decals for ground variation.
- Terrain water is cheap visually; verify swimming/flow assumptions with gameplay code.

### 4. Streaming-safe level design
- Keep critical gameplay containers (remotes, configs, UI) in ReplicatedStorage/StarterGui, never in
  Workspace.
- Teleports and long traversal must handle parts that are not streamed in yet.
- Don't mark large swaths Persistent to dodge streaming bugs; that defeats the point.
- Test: spawn → sprint to the far edge → teleport back → verify no missing ground or script errors.

### 5. Lighting presets that survive quality settings
```text
ClockTime 14-16 (day) / 18-19 (dusk) / 0-5 (night)
Brightness 2-3 day, 0.5-1 night; Atmosphere Density 0.3-0.4 (avoid fog walls)
Bloom 0.3-0.6, ColorCorrection subtle; never rely on post FX for readability
```
Check the scene at graphics quality 1 and 10: if gameplay readability depends on bloom or shadows,
it will fail on low-end phones.

### 6. Budget checks (targets, not engine caps)
- Draw calls and triangles: profile the densest view; a low-end device reference is ~1k draw calls /
  ~1M triangles — treat as a ceiling to stay well under.
- Unique mesh/texture IDs break instancing: reuse kits instead of one-off meshes.
- Shadow casters: only objects that need grounding shadows.
- Transparent/overdraw layers: minimize stacked glass, fog planes, and large particles.

## FAILURE MODES & MITIGATIONS

1. **Art before layout** — beautiful map that plays badly. *DETECT:* traversal/flow problems found
   after the art pass. *FIX:* greybox and playtest first; art is a second pass.
2. **Scale drift** — doors, stairs, and gaps that don't fit a Humanoid. *DETECT:* players get stuck;
   jump heights feel wrong. *FIX:* build on a grid with reference props at Humanoid scale.
3. **Streaming pop-in** — critical geometry missing on spawn. *DETECT:* falling through the world,
   nil descendants. *FIX:* streaming-safe containers, WaitForChild timeouts, chunk models ≤64 studs.
4. **Precise everything** — collision/render fidelity maxed for props. *DETECT:* frame time collapses
   in dense areas. *FIX:* Box/Hull + Automatic unless measured otherwise.
5. **Unique-asset sprawl** — every prop a different mesh/texture. *DETECT:* draw calls high, memory
   high. *FIX:* modular kits, MaterialVariants, reuse.
6. **Lighting-dependent readability** — dark scene that only works with bloom. *DETECT:* low quality
   setting makes the level unplayable. *FIX:* contrast from materials and layout, post FX as garnish.
7. **Unanchored assemblies** — physics simulates the scenery. *DETECT:* props drift, server CPU high.
   *FIX:* anchor static geometry; weld decorations to one anchor.

## QUANTITATIVE RULES

- 1 stud ≈ 0.28 m; Humanoid ≈ 5 studs; door ≈ 7×3; grid-snap structural geometry.
- Terrain voxel = 4×4×4 studs; don't sculpt detail below that.
- Streaming baseline: MinRadius 64 / TargetRadius 1024; static model extent ≤64 cubic studs.
- Collision: Box/Hull by default; Precise only with a measured reason.
- Shadow casters and transparent layers: minimize in the densest view; verify at quality 1.
- Measure at spawn and at the densest viewpoint, on the lowest target device, before calling it done.

## VERIFICATION GATE

- [ ] Greybox was playtested before the art pass.
- [ ] Terrain vs parts chosen per area with no mixed seams.
- [ ] Static geometry anchored; decorations welded; no stray unanchored assemblies.
- [ ] Streaming enabled (large worlds) and traversal tested across stream-in/out boundaries.
- [ ] Lighting/Atmosphere readable at low graphics quality.
- [ ] Densest-view measurement recorded; unique assets and shadow casters justified.
- [ ] Before/after screenshots from a fixed camera for visual claims.

## REFERENCES

- `roblox-studio-mcp` — building and verifying in Studio
- `roblox-assets` — meshes, materials, textures, licensing
- `roblox-vfx` — particles, beams, post-processing budgets
- `roblox-scripting` — markers, spawn logic, streaming-aware code
- Roblox docs: terrain, instance streaming, lighting, performance optimization
