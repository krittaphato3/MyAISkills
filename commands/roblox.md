---
description: Turn a prompt into a complete, non-slop AAA Roblox game via autonomous multi-agent orchestration
argument-hint: [game concept or prompt]
skills: roblox-game-production, roblox-studio-mcp
---

# Autonomous Roblox Game Production

Turn a simple prompt into a complete, production-grade Roblox game without amateur slop.

## Target
$ARGUMENTS

## Operating Principles: The Anti-Slop Doctrine
1. **Zero Raw Grey Plastic**: Every part must have defined PBR MaterialVariants, color palette discipline (60-30-10 rule), and cohesive environmental atmosphere.
2. **AAA UI/UX Standard**: No flat default rectangles or garish primary buttons. All interfaces require rounded corners (`UICorner`), subtle strokes (`UIStroke`), gradient highlights (`UIGradient`), spring micro-interactions (`TweenService`), safe-area scaling, and tactile sound effects.
3. **Strict Server Authority**: Zero client trust. The server validates all inputs, cooldowns, distances, and state transitions. Client performs local prediction with server reconciliation.
4. **Kinetic Feel & Animation**: Combat and movement must include animation blending, procedural lean, camera sway, hitpause (freeze frames), and screen shake.
5. **Dynamic Soundscape**: Every action has audio feedback. Impact sounds must use randomized pitch variation (plus/minus 5 percent) to prevent ear fatigue, paired with 3D spatial roll-off.
6. **Hard Evidence Verification**: No milestone completes without live verification: clean console logs (`get_console_output`) and visual proof (`screen_capture`).

## Autonomous Execution Pipeline

### Phase 1: Concept & Core Loop (roblox-game-director)
- Connect to the active Roblox Studio instance via `list_roblox_studios`.
- Formulate the Core Loop: `Player does {verb} to get {reward}, which lets them {next verb}`.
- Scope the Milestone 0 to Milestone 4 vertical slice and establish the cut list.

### Phase 2: World Atmosphere & Spatial Greybox (roblox-builder)
- Set lighting technology to `Future`.
- Configure `Atmosphere`, `ColorCorrection`, `Bloom`, and skybox.
- Block out the arena or play area with proportional gameplay scales and player spawns.

### Phase 3: 3D Assets & PBR Textures (roblox-asset-artist)
- Source or generate 3D models via Studio MCP (`generate_mesh`, `generate_procedural_model`).
- Create and assign PBR `generate_material` variants.
- Enforce strict draw-call and polygon budgets for mobile compatibility.

### Phase 4: Systems, Networking & Security (roblox-scripter & roblox-security-engineer)
- Scaffold modular architecture in `ReplicatedStorage` and `ServerScriptService`.
- Implement server-authoritative state management and token-bucket remote event rate limiting.
- Bind client controllers with snappy local prediction.

### Phase 5: AAA Tactile UI/UX (roblox-ui-designer)
- Construct responsive ScreenGui with `UIAspectRatioConstraint` and safe-area insets.
- Build interactive 3D hero showcases using telephoto `ViewportFrame` instances.
- Implement tactile spring button tweens and micro-interaction sound bindings.

### Phase 6: Kinetic Animation & Camera Feel (roblox-animator)
- Author rig-aware animation tracks (`Action`, `Movement`, `Idle`).
- Implement procedural spring tilt, camera bobbing, and hit reactions.

### Phase 7: VFX & Dynamic Audio (roblox-vfx-artist)
- Build burst particle emitters, weapon trails, and impact effects with low-overdraw curves.
- Implement spatial sound effects with pitch jitter and ambient sound beds.

### Phase 8: Autonomous QA & Visual Gate (roblox-qa-engineer)
- Run playtests via `start_stop_play`.
- Verify zero runtime errors via `get_console_output`.
- Capture viewport screenshots via `screen_capture` to confirm visual presentation before final delivery.
