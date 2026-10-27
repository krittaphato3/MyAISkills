---
name: roblox-vfx
description: >-
  Creates Roblox effects and sound: ParticleEmitters, Beams, Trails and attachments, lighting
  post-effects, impact/ambient/spatial audio, pooling and cleanup, and low-quality fallbacks. Use
  when a hit, cast, explosion, aura, weather, trail, or sound needs to exist or be fixed. UI motion
  routes to roblox-ui-ux; character clips to roblox-animation; map lighting mood to
  roblox-world-building.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-vfx-artist
---

# Roblox VFX & Audio

Effects are cheap to make and expensive to run. The platform gives you per-emitter ceilings, but the
real budget is screen coverage: large transparent particles stacked on top of each other cost far
more than a hundred small ones. Good game feel comes from timing and contrast, not from particle
count — and every effect needs a cheap version for phones.

## WHEN TO USE

- Hit/cast/explosion/aura/weather/ambient effects, trails, beams, lightning, portals.
- Sound design: impacts, UI clicks, ambience, music, 3D positional audio.
- Effects that must fire on animation markers or gameplay events.
- Frame drops in combat, or effects that look different on mobile.
- Cleaning up leaked effects/sounds after repeated actions.

## WHEN NOT TO USE

- Character or prop animation — `roblox-animation`.
- UI transitions and screen layout — `roblox-ui-ux`.
- Global lighting/mood and map atmosphere — `roblox-world-building` (this skill covers effect budgets
  and post-processing tuning that ship with effects).
- Image/texture/audio asset creation or licensing — `roblox-assets`.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. WHAT IS THE BEAT?
   Every effect answers a gameplay moment: impact, cast, warning, reward, ambience.
   If it does not communicate state, it is decoration — make it cheap.

2. DOES IT NEED A 3D ANCHOR?
   World-space effect → Attachment on the part/bone, particle/beam parented there.
   Screen-space feedback → UI layer (roblox-ui-ux), not a particle in the camera.
   Character-bound → attachment on the rig; detach/destroy on death.

3. ONE-SHOT OR LOOP?
   One-shot → Emit(n) burst + Debris cleanup (or pool).
   Loop → low Rate, enabled only while the state is active; disable when it ends.
   Never leave a looping emitter running invisibly.

4. HOW EXPENSIVE IS THE OVERDRAW?
   Large particles, stacked transparency, and many emitters in one frame are the cost drivers.
   Reduce size/count/lifetime before reducing quality of the effect's shape.
   Plan the mobile fallback: fewer particles, smaller size, no secondary layers.

5. WHERE DOES THE SOUND LIVE?
   3D → Sound parented to a part/attachment with RollOffMin/MaxDistance and RollOffMode.
   UI/global → SoundService or a non-positional Sound parented to a persistent container.
   Loop music separately from SFX; fade between tracks; pool impact sounds.

6. HOW IS IT VERIFIED?
   Playtest the worst case (many effects at once), capture before/after, check frame time and
   console, and confirm the mobile/low-quality variant.
```

## PATTERNS

### 1. Burst effect (one-shot, pooled)
```lua
local function playHit(position: Vector3, color: Color3)
    local attachment = Instance.new("Attachment")
    attachment.WorldPosition = position
    attachment.Parent = workspace.Effects

    local emitter = Instance.new("ParticleEmitter")
    emitter.Texture = HIT_TEXTURE
    emitter.Color = ColorSequence.new(color)
    emitter.Lifetime = NumberRange.new(0.25, 0.4)
    emitter.Speed = NumberRange.new(8, 14)
    emitter.Rate = 0                       -- bursts only
    emitter.Parent = attachment

    emitter:Emit(12)                       -- count, not a continuous rate
    Debris:AddItem(attachment, 1)
end
```
`Emit(n)` avoids a permanently running emitter. Pool the attachment/emitter pair if the effect fires
many times per second.

### 2. Loop effect lifecycle
```lua
local function setAura(character: Model, enabled: boolean)
    local existing = character:FindFirstChild("AuraAttachment")
    if enabled and not existing then
        local attachment = Instance.new("Attachment")
        attachment.Name = "AuraAttachment"
        attachment.Parent = character:FindFirstChild("HumanoidRootPart")
        -- emitter with low Rate (e.g. 8–15) and short lifetime
    elseif not enabled and existing then
        existing:Destroy()                 -- destroys the emitter with it
    end
end
```
State-driven creation/destruction beats toggling `Enabled` on effects you forgot about.

### 3. Beam / trail setup
- Both need two `Attachment`s; parent them to the moving parts/bones.
- Beam: reduce `Segments` (e.g. 10–20) unless the curve needs more; `FaceCamera` for billboards.
- Trail: shorter `Lifetime` = shorter visible trail; disable when the weapon is sheathed.
- Never create a Beam per frame; create once, move the attachments.

### 4. Post-processing placement
| Effect | Where | Notes |
|---|---|---|
| Bloom, ColorCorrection, DepthOfField (global) | `Lighting` | One instance each; tune subtly |
| Menu blur / player-specific | `player.Camera` (client) | Remove when the menu closes |
| Hit flash | UI frame or camera effect | Cheapest, most readable |
Post effects multiply overdraw; verify at low graphics quality and on mobile.

### 5. Audio design rules
```text
Impact SFX: 0.15–0.5 s, pooled, pitch variance ±5%
UI click:    <0.15 s, non-positional, SoundService parent
Ambience:    looped, low volume, fade in/out over 1–2 s
Music:       one track at a time, crossfade 1–2 s, duck under dialogue
3D sounds:   RollOffMode Linear or Inverse, Min 5-10, Max 60-120 studs
```
Sounds inherit volume from `SoundService`/`SoundGroup`; use groups for SFX/Music/Voice so players can
mix, and never stack more than a handful of the same impact in one frame.

### 6. Mobile / low-quality fallback
Detect quality tier once (`UserGameSettings.SavedQualityLevel` on the client) and swap:
- fewer particles (`Emit(6)` vs `Emit(20)`), smaller size, no secondary emitter
- disable depth of field and heavy bloom
- shorter trail lifetime, fewer segments
- keep the *timing and color* identical so gameplay reads the same

## FAILURE MODES & MITIGATIONS

1. **Emitter never stops** — looping effect left enabled. *DETECT:* particle count grows; frame time
   drops over time. *FIX:* state-driven destroy/disable; cap concurrent loops.
2. **Overdraw collapse** — huge transparent particles stacked. *DETECT:* mobile frame drops in combat.
   *FIX:* reduce size/coverage first; fewer layers; fallback variant.
3. **Effect spam** — one emitter created per hit, thousands live. *DETECT:* instance count climbs.
   *FIX:* `Emit(n)` on a pooled emitter; Debris cleanup with short lifetimes.
4. **Beam/trail invisible** — missing attachments or wrong parent. *DETECT:* nothing renders.
   *FIX:* two attachments, correct ancestry, re-test in play mode.
5. **Sound plays globally** — music parented to a part. *DETECT:* volume fades with distance.
   *FIX:* non-positional Sound in SoundService for music/UI.
6. **Audio stacking** — 20 identical impacts in one frame. *DETECT:* clipping/distortion. *FIX:* pool
   and throttle per sound key; pitch variance.
7. **Post FX dependency** — scene only reads at max quality. *DETECT:* low quality is unreadable.
   *FIX:* contrast from color and shape; post as garnish.
8. **Leaked attachments** — effects parented to destroyed characters. *DETECT:* orphan instances in
   workspace. *FIX:* parent to a cleanable container; destroy on death/despawn.

## QUANTITATIVE RULES

- Per-emitter ceilings: 400 particles/s desktop, 100/s mobile — stay far below; these are caps, not
  targets.
- Particle lifetime ≤20 s (engine cap); gameplay effects typically 0.2–1.5 s.
- Flipbook animation ≤30 fps; reuse textures, avoid many unique high-res flipbooks.
- Beams: ≤20 segments unless a curve requires more. Trails: short lifetimes.
- ≤1 global Bloom/ColorCorrection/DOF each; remove player-specific effects when their UI closes.
- 3D audio roll-off: Min 5–10, Max 60–120 studs; pool and throttle repeated impacts.
- Verify the worst-case scene on the lowest target device, not an empty baseplate.

## VERIFICATION GATE

- [ ] Every effect maps to a gameplay beat and has a stated purpose.
- [ ] One-shot effects use bursts + cleanup; loops are state-driven and destroyed.
- [ ] No emitter/attachment leak after 20 repeated activations.
- [ ] Mobile/low-quality fallback exists and preserves timing and readability.
- [ ] Post effects verified at low graphics quality; no readability dependency.
- [ ] Audio: correct spatialization, pooled, grouped, no clipping in the worst case.
- [ ] Before/after capture and frame-time or console evidence attached.

## REFERENCES

- `roblox-animation` — markers that trigger effects
- `roblox-world-building` — lighting and global atmosphere
- `roblox-assets` — textures, audio files, and licensing
- `roblox-ui-ux` — screen-space feedback and UI motion
- `roblox-testing` — worst-case effect and perf verification
- Roblox docs: particle emitters, beams, trails, post-processing, audio assets
