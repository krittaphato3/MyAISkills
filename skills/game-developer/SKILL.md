---
name: game-developer
description: >-
  Writes gameplay and engine code for Unity (C#), Unreal (C++/Blueprint), and Godot
  (GDScript): loops, state machines, input, physics, save systems, and frame budgets. Use
  when the deliverable runs in one of these engines. Roblox and Luau route to the
  roblox-* suite (roblox-game-director for coordination, roblox-scripting for systems);
  browser games to frontend-web-engineer.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: game-developer
---

# GAME DEVELOPER

Expert game development across multiple engines and platforms.

## ROBLOX / LUAU

> Non-Roblox skill. Any Roblox, Luau, Studio, DataModel, RemoteEvent, ScreenGui task → the `roblox-*` suite: `roblox-game-director` to coordinate, or the matching discipline skill (`roblox-scripting`, `roblox-world-building`, `roblox-ui-ux`, `roblox-animation`, `roblox-vfx`, `roblox-assets`, `roblox-security`, `roblox-testing`). Platform/language fundamentals live in `roblox-lua-developer`. No Roblox code lives here by design.

## UNITY / GODOT / PATTERNS

See `references/engines.md` (MonoBehaviour controller, Godot character controller, object pooling) — load only the engine needed. Module and state-machine patterns in a Roblox context live in `roblox-lua-developer/references/code-patterns.md`; the engine-agnostic forms are in Game Programming Patterns (below).

## OUTPUT
```text
[GAME DEV]
Engine: {Roblox|Unity|Godot|Unreal}
Platform: {PC|Mobile|Console}

DELIVERABLES:
- {script/component 1}
- {script/component 2}

PATTERNS USED:
- {pattern 1}
- {pattern 2}
```

## WHEN TO USE
- Writing gameplay code, engine-specific logic (Unity/C#, Unreal/C++/Blueprint, Godot/GDScript), or a game system that must run in an engine.
- You need a canonical script/pattern (state machine, object pooling, movement, input, animation tweening) in a game context.
- Debugging or extending an existing gameplay feature in one of these engines.
- Designing a game mechanism (spawning, scoring, physics response) that must be implemented in-engine. (Roblox/Luau work routes to the `roblox-*` suite.)

## WHEN NOT TO USE
- **Roblox (Luau) development** — that is the `roblox-*` suite, coordinated by `roblox-game-director`.
- **Game-design-adjacent but not code**: balancing spreadsheets, narrative/level design prose without an implementation target.
- **Non-engine game backend** (matchmaking API, auth, telemetry) — platform/service code is devops/api, not in-engine.
- **One-off native UI outside the engine** — leave to mobile/UI skills unless it's an in-engine HUD.

## DECISION TREE
```text
1. ENGINE → Unity/C#? Unreal (C++ / Blueprint)? Godot/GDScript? Roblox/Luau?
   Roblox → roblox-game-director (or the matching roblox-* skill). Else continue.
2. WHAT  → gameplay logic (movement/combat)? A reusable system (state machine / pool)?
   A mechanism (physics/animation/audio)? → select the matching pattern section.
3. PATTERN → for a recurring need pick the canonical pattern from GAME DESIGN PATTERNS
   (state machine, object pooling, factory, event bus) and adapt to the engine.
4. INTEGRATE → wire it to the engine's update/input/collision hooks; respect tick/authority model.
5. VERIFY → test the edge cases in-engine (empty/high concurrency, framerate). Record the result.
```
Never pick a pattern before you know the engine and whether it's gameplay vs a reusable system.

## FAILURE MODES & MITIGATIONS
- **Wrong engine idioms.** DETECT: code uses the wrong API or foreign conventions (e.g., a C# MonoBehaviour used as a static utility), and build/runtime issues surface in-engine.
  FIX: follow the engine's official script model (Component/MonoBehaviour in Unity, Node in Godot, Actor in Unreal), and choose the section matching the engine.
- **Missing tick/framerate discipline.** DETECT: heavy work in `Update`/`_physics_process` causes frame drops or desync under spawn storms.
  FIX: use delta-time (`delta`/`Time.deltaTime`) everywhere, move non-per-frame work to fixed timestep or a coroutine/async, and keep hot paths allocation-light.
- **State-machine spaghetti.** DETECT: `if`/`switch` on state littered across the class; states become hard to add and test.
  FIX: use the canonical state-machine pattern with explicit `Enter/Exit/Update` states; keep transitions data-driven.
- **Object-pool misuse / GC hitches.** DETECT: instantiation/deletion churns in hot paths produces GC stalls (Unity/Godot) or object churn.
  FIX: pool frequently-reused objects, warm the pool, disable rather than destroy, and re-enable on get with zeroed state. (see Object Pooling)
- **Network/authority desync.** DETECT: clients disagree on a shared game state; writes happen on the wrong authority.
  FIX: put authoritative logic on the server/authoritative host, replicate only the smallest data, and validate client input.
- **Cross-engine confusion in one codebase.** DETECT: Godot, Unity, and Roblox snippets mixed into the same file/function.
  FIX: keep one engine per script and per subsystem; isolate engine adapters behind a thin interface when code must be portable.

## VERIFICATION GATE
- **In-engine run**: the feature builds and runs in the target engine with no console errors or warnings introduced.
- **Behavioral edge cases pass**: high-concurrency/empty/boundary inputs handled without crash (spawn storm, zero entities, max capacity).
- **Framerate discipline honored**: no fixed-cost-per-frame work in the active loop; hot path is measured to hold the target frame rate.
- **State machine test**: transitions are exercised (empty→running→paused→exit); no illegal transition reachable.
- **red-team-qa review**: adversarial check for framerate-sinking code, network desync, or a state machine that can be wrong-commanded.

## REFERENCES
- Unity Learn / scripting docs — MonoBehaviour, physics, pooling.
- Unreal Engine docs — Actors, Blueprints, Gameplay Framework.
- Godot documentation — Nodes, GDScript, physics and signal flow.
- Game Programming Patterns (Nystrom) — state machine, object pool, command, observer.
