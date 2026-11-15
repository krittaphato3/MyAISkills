# Autonomous Anti-Slop Roblox Production Pipeline

This reference document synthesizes cutting-edge multi-agent game generation frameworks (GameGPT, Nixera roblox-ai-studio, RoAutomation) into a deterministic, high-fidelity pipeline for Roblox Studio via MCP.

---

## 1. THE ROOT CAUSES OF AI GAME DEV SLOP

Single-model game generation fails because one LLM attempting every discipline simultaneously produces:
- **Visual Homogeneity**: Default grey plastic blocks, flat terrain, and stock ShadowMap lighting with no post-effects.
- **Unusable UI**: Flat rectangles with default fonts, hardcoded pixel offsets that break on mobile notches, and no audio or tween feedback.
- **Vulnerable Architecture**: Client-authoritative remotes (`DamageRemote:FireServer(target, 100)`), race conditions, and lack of token-bucket rate limiting.
- **Floaty Mechanics**: Character locomotion with no animation priority blending, no procedural lean, no camera kick, and zero impact frames.
- **Silent Worlds**: Silent interactions, lack of pitch jitter on repeated SFX (causing ear fatigue), and missing spatial 3D audio roll-off.

---

## 2. THE MULTI-AGENT HIERARCHICAL TASK NETWORK (HTN)

The anti-slop engine resolves this through an 8-stage assembly line with strict handoff boundaries:

```text
[Prompt Intake]
      │
      ▼
[Stage 1: roblox-game-director] ──── GDD & Core Loop Spec (Verb -> Reward -> Unlock)
      │
      ├───────────────────────────────┬───────────────────────────────┐
      ▼                               ▼                               ▼
[Stage 2: roblox-builder]   [Stage 3: roblox-asset-artist]  [Stage 4: roblox-scripter]
World Atmosphere, Future    3D Meshes (generate_mesh)       Modular Luau, Netcode,
Lighting & Arena Greybox    & PBR MaterialVariants          Server Authority & State
      │                               │                               │
      └───────────────────────────────┼───────────────────────────────┘
                                      │
      ┌───────────────────────────────┴───────────────────────────────┐
      ▼                               ▼                               ▼
[Stage 5: roblox-ui-designer] [Stage 6: roblox-animator]    [Stage 7: roblox-vfx-artist]
AAA Tactile HUD, Spring       Kinetic Animation Tracks,     Burst Particles, Weapon
Tweens & 3D ViewportFrames    Procedural Lean & Hitpause    Trails & Spatial Sound
      │                               │                               │
      └───────────────────────────────┼───────────────────────────────┘
                                      │
                                      ▼
                       [Stage 8: roblox-qa-engineer]
                       In-Engine Playtest, Console Audit,
                       Screen Capture Visual Gate
```

---

## 3. ANTI-SLOP SPECIFICATIONS PER DISCIPLINE

### A. World Building and Atmosphere
- **Lighting Technology**: Always set `Lighting.Technology = Enum.Technology.Future`.
- **Atmosphere Stack**: Configure `Atmosphere` (Density 0.3-0.45, Haze 0-2, Color tuned to theme). Add single subtle instances of `BloomEffect`, `ColorCorrectionEffect`, and `SunRaysEffect`.
- **Color Palette Rule**: Follow the 60-30-10 distribution:
  - 60% Dominant environmental tone (e.g., dark slate stone or deep metal).
  - 30% Secondary structure tone (e.g., weathered cedar planks or burnished bronze).
  - 10% Accent/energy tone (e.g., emissive neon cyan or glowing amber).

### B. AAA UX/UI Design
- **Safe-Area Layout**: Anchor parent frames to scale `(1, 0, 1, 0)` with `GuiService:GetGuiInset()` margins to protect camera notches and home bars.
- **Tactile Sizing**: Wrap interactive elements in `UIAspectRatioConstraint`. Use `UICorner` (radius 6-12 px) and `UIStroke` (ApplyStrokeMode = Border, subtle contrast).
- **Interactive 3D ViewportFrames**: Show weapons, pets, and key items inside `ViewportFrame` instances using telephoto isometric cameras (FOV 25-30 degrees) with continuous subtle idle rotation.
- **Tween Feedback**: All buttons must have hover (brightness tint or 1.03 scale) and down (0.95 scale via `Enum.EasingStyle.Back` or `Quad`) transitions with sound triggers.

### C. Luau Architecture & Security
- **Data Model Separation**:
  - `ReplicatedStorage.Common`: Shared types, constants, and network RemoteEvent definitions.
  - `ReplicatedStorage.Controllers`: Client UI, prediction, and visual state controllers.
  - `ServerScriptService.Services`: Authoritative state machines, inventory, combat validation, and persistence.
- **Server Authority**: The server validates all actions: distance checks (`(p1 - p2).Magnitude <= MAX_REACH`), cooldown debounces, and stamina/mana reservations.
- **Rate Limiting**: RemoteEvents must employ token-bucket rate limiting per player to reject spam.

### D. Kinetic Animation & Combat Feel
- **Priority Hierarchy**:
  - `Enum.AnimationPriority.Action`: Melee attacks, casts, dodges.
  - `Enum.AnimationPriority.Movement`: Custom walks, sprints, falls.
  - `Enum.AnimationPriority.Idle`: Stance breathing, weapon idle.
- **Kinetic Juice**:
  - **Hitpause**: 0.05-0.10s micro-pause on attack land.
  - **Procedural Lean**: Spring-based HumanoidRootPart roll during strafes.
  - **Camera Kick**: Quick impulse FOV punch (+3 FOV then damped spring return).

### E. VFX & Sound Design
- **Particle Budgeting**: Use burst emitters (`emitter:Emit(n)`) with lifetime under 0.6 seconds instead of continuously running emitters.
- **Audio Fatigue Protection**:
  - Impact sounds must apply pitch jitter: `sound.PlaybackSpeed = Random.new():NextNumber(0.95, 1.05)`.
  - 3D spatial audio must use `RollOffMode.InverseTapered` with clamped Min/Max distances.
  - UI audio must be parented to `SoundService` with subtle volumes (0.2-0.4).

---

## 4. MULTI-MODAL VERIFICATION GATE

Before any vertical slice or game feature is marked done:
1. **Console Check**: Query `get_console_output` to verify zero Lua syntax, runtime, or nil-indexing errors.
2. **Visual Inspection**: Execute `screen_capture` at key camera viewpoints to visually evaluate lighting balance, model placement, and UI legibility.
3. **Hierarchy Audit**: Use `inspect_instance` or `search_game_tree` to confirm correct parenting and anchored states.
