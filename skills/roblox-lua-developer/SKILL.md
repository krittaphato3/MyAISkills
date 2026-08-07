---
name: roblox-lua-developer
description: Luau and Roblox platform development: coding, UI, networking, persistence, economy, security, performance, VFX, animation, audio, terrain, assets, plugins, testing. Routes to the right domain workflow autonomously.
version: 2.0.0
grade: G2
domain: roblox
status: active
last-reviewed: 2026-08-06
supersedes: "roblox suite 1.x (21 skills): roblox-3d-assets, roblox-animation, roblox-architecture, roblox-asset-import, roblox-audio, roblox-avatar, roblox-cinematics, roblox-coding, roblox-data-persistence, roblox-economy, roblox-game-dev, roblox-networking, roblox-orchestrator, roblox-performance, roblox-plugins, roblox-security, roblox-terrain, roblox-testing, roblox-tools-workflow, roblox-ui-ux, roblox-vfx"
owned-by-agent: game-developer
---

# ROBLOX LUA DEVELOPER

Single entry point for all Luau and Roblox platform work. This skill consolidates the 21-skill Roblox 1.x suite into one capability-focused skill: shared MCP instrumentation, the shared verification protocol, and 15 domain workflows are unified here. Route any Roblox/Luau task to the correct domain workflow via the DECISION TREE.

## WHEN TO USE

Use this skill for ANY task that touches the Roblox platform or the Luau language, including but not limited to:

- **Luau coding** — scripts, ModuleScripts, class factories, event systems, state machines, typed tables, DataStore wrappers, utility modules. Any code that runs in Studio or at runtime.
- **UI/UX** — ScreenGui, HUDs, menus, UIListLayout/UIGridLayout, themes, responsive layout, UI tweening, accessibility (WCAG 2.1 AA where representable).
- **Networking** — RemoteEvent/RemoteFunction design, client-server replication, server-authoritative protocols, rate limiting, request/response flows.
- **Data persistence** — DataStore save/load, session locking, auto-save, migration, versioned stores, player data caching.
- **Economy** — DevProducts, GamePasses, private servers, leaderstats, currency managers, ProcessReceipt handling, anti-exploit for currency.
- **Security** — server authority, input validation, anti-exploit monitors, exploit-vector audit (remote spoofing, value-object tampering, module injection).
- **Performance** — profiling, memory management, object pooling, streaming, connection hygiene, frame-budget discipline.
- **VFX** — ParticleEmitter, Beam, Trail, Lighting/Atmosphere, post-processing, materials, glow/emission effects.
- **Animation** — TweenService, AnimationTrack/Animator, Motor6D rigs, procedural motion, easing, keyframes, sequence playback.
- **3D assets** — MeshPart generation, MaterialVariant, procedural models, Creator Store search/insert, local image/material pipelines.
- **Audio** — Sound/SoundService, 3D spatial audio, roll-off, music managers, audio zones, SFX pooling.
- **Terrain** — Terrain service, Region3 fills, biomes, foliage placement, skyboxes, streaming-friendly world building.
- **Plugins** — Studio plugin toolbars, DockWidgetPluginGui, Selection service, plugin settings, Studio API extension.
- **Testing** — TestEZ-style suites, in-Studio runners, playtest automation, input simulation, visual regression, TDD.
- **Cinematics** — camera paths, letterboxing, fades, dialogue UI, cutscene sequencing, input lockdown during cutscenes.
- **Avatar** — HumanoidDescription, R15/R6 rigs, clothing, accessories, body colors, scale, outfit systems.
- **Multi-domain builds** — full features that span several of the above (e.g. an inventory system = UI + persistence + networking + security); drive them with the orchestration path in the DECISION TREE.

Activate automatically on keywords: Roblox, Luau, Studio, DataStore, RemoteEvent, ScreenGui, GamePass, DevProduct, leaderstats, TweenService, HumanoidDescription, Terrain, ParticleEmitter, ProcessReceipt, `create.roblox.com`, and any reference to the Roblox API/DataModel.

## WHEN NOT TO USE

- **Non-Roblox game engines** (Unity, Unreal, Godot, custom engines) — delegate to the game-developer agent; this skill only covers Roblox.
- **MCP server authoring** — building or extending MCP servers/skills infrastructure — delegate to the mcp-builder skill.
- **General-purpose Lua outside Luau** — if the target runtime is PUC-Lua/LuaJIT without the Roblox DataModel, this skill's platform sections do not apply.
- **Web frontend/backend development, databases, or other non-Roblox domains** — delegate to the relevant stack.
- **Pure asset authoring outside Roblox** (standalone Blender/Photoshop deliverable with no Studio integration) — hand off to the appropriate asset workflow; return here when the asset must be imported, scripted, or verified in Studio.
- **Task 2.0 caveat**: the 21 specialized skills of the old suite (roblox-3d-assets … roblox-vfx) no longer exist and must not be invoked. Use this skill's DOMAIN WORKFLOWS instead.

## MCP INSTRUMENTATION

All Roblox work is executed and verified through the Roblox Studio MCP bridge. Every domain workflow in this skill uses the same core tool set; domain-specific tools are noted per workflow.

### Core tools (shared)

| Tool | Purpose | Context |
|---|---|---|
| `search_game_tree` | Explore the DataModel hierarchy by path, instance type, or keyword | Edit / Server / Client |
| `inspect_instance` | Read a single instance's properties and children | Edit / Server / Client |
| `script_search` | Find scripts by name pattern | Edit |
| `script_grep` | Find code patterns across all scripts | Edit / Server |
| `script_read` | Read a full script body by path | Edit |
| `multi_edit` | Batch apply edits (or create scripts with a className) | Edit |
| `get_studio_state` | Check current Studio/play state and available datamodel types | n/a |
| `get_console_output` | Read console output; errors and warnings from the last run | n/a |
| `execute_luau` | Run arbitrary Luau in Edit, Server, or Client context | Edit / Server / Client |
| `screen_capture` | Capture the viewport; optionally from a custom camera | n/a |
| `start_stop_play` | Enter/exit play mode for runtime testing | n/a |

### Asset and interaction tools (used by specific workflows)

| Tool | Purpose | Used by |
|---|---|---|
| `generate_mesh` | AI mesh generation from a text prompt | 3D assets, asset import |
| `generate_material` | AI MaterialVariant generation | 3D assets, VFX, terrain |
| `generate_procedural_model` | Parametric model with editable attributes | 3D assets, terrain |
| `search_asset` | Search Creator Store (scope: auto/creator_store/user/group) | 3D assets, audio, avatar, terrain |
| `insert_asset` | Insert an asset by ID (Model/Image/Audio/Package) | 3D assets, audio, avatar |
| `store_image` | Load a local image file and return an image URI | asset import, UI |
| `upload_image` | Upload images from a URL to Roblox | asset import, UI |
| `character_navigation` | Move the test character to coordinates or an instance | testing, tools |
| `user_keyboard_input` | Simulate keyboard presses (with waits) | testing |
| `user_mouse_input` | Simulate mouse clicks at coordinates | testing |
| `list_roblox_studios` | List connected Studio instances | tools |
| `http_get` | Fetch Roblox API reference docs | all |

### Standard interaction loop

1. **Audit first**: `search_game_tree` (target container, depth 2–6) → `script_grep` (relevant APIs) → `inspect_instance` on the specific nodes before writing any code.
2. **Write**: prefer `multi_edit` for modifications of existing scripts; use `execute_luau` with `datamodel_type: "Edit"` to create instances (GUI, particles, terrain, plugins).
3. **Test**: `start_stop_play(is_start: true)` for runtime behavior → `execute_luau` in Server context for server logic and Client context for client logic → `get_console_output`.
4. **Verify visually**: `screen_capture` before/after; when a reference image exists, iterate until pixel match.
5. **Close out**: `start_stop_play(is_start: false)`; re-run `get_console_output`; never report done while the console shows errors.

## ROBLOX PLATFORM

### DataModel tree

Everything is an Instance in a single root object, `game`. Core containers and their roles:

| Container | Role |
|---|---|
| `Workspace` | Run-time world: parts, models, terrain, camera, characters. Client has read access; physics and most writes replicate to clients. |
| `ReplicatedStorage` | Replicates to all clients; shared assets, ModuleScripts, and the RemoteEvent/RemoteFunction definitions live here. Never put run-time scripts that must execute on the client here. |
| `ServerScriptService` | Server-only scripts and modules. Never referenced by client code. |
| `ServerStorage` | Server-only storage; not replicated, never accessible by clients. Place templates here. |
| `StarterPlayer` / `StarterPlayerScripts` / `StarterGui` | Templates cloned into each player on spawn. Client code, HUD, and player scripts live here. |
| `Players` | Player instances, their leaderstats, characters, and PlayerGui. |
| `Lighting` | Global lighting, atmosphere, post-processing effects; replicated to clients. |
| `SoundService` | Global sound management; settings replicate. |
| `LocalizationService`, `TextService` | Text/UI localization and measurement. |
| `DataStoreService` | Persistent player/global data (server-only). |

### Core services (short reference)

| Service | Key APIs | When to use |
|---|---|---|
| `RunService` | `Heartbeat`, `RenderStepped`, `Stepped` | Frame loops, physics-synced updates |
| `TweenService` | `TweenService:Create`, `TweenInfo` | Property animations |
| `Debris` | `Debris:AddItem(item, lifetime)` | Timed cleanup of temporary instances |
| `Players` | `Players.PlayerAdded`, `PlayerRemoving`, `GetPlayerFromCharacter` | Player lifecycle, character lookup |
| `DataStoreService` | `GetDataStore`, `GetAsync`, `SetAsync`, `UpdateAsync`, `GetSortedAsync`, `IncrementAsync` | Persistence |
| `MarketplaceService` | `ProcessReceipt`, `UserOwnsGamePassAsync`, `GetProductInfo` | Monetization |
| `InsertService` | `InsertService:LoadAsset(assetId)` | Runtime asset loading |
| `Lighting` | `ClockTime`, `Ambient`, `FogEnd`, `Brightness`, post-effects | Environment |
| `SoundService` | `AmbientReverb`, sound pooling | Audio |
| `Selection` | `Selection:Get()`, `Selection:Set()` | Plugin object selection |
| `TextService` | `GetTextSize` | UI text fitting |

### Client/server replication model

- Roblox is **server-authoritative**: the server owns the simulation; clients see a lag-compensated, property-replicated view.
- Only **server writes** to the DataModel replicate to clients. Client-side edits to non-owned parts are reverted by the server.
- Characters and physics state replicate; smooth rendering is handled by the engine's interpolation.
- **RemoteEvents fire and forget**; **RemoteFunctions yield** the caller and return a value. Prefer RemoteEvents for frequent/one-way traffic; use RemoteFunctions sparingly (yielding + timeout risk).
- Every remote invocation must be **validated server-side** — the client never provides a trusted value (position, currency delta, damage, inventory item).
- The server does NOT have a direct reference to `Players.LocalPlayer`. Always derive the caller from the `player` argument of `OnServerEvent` / `OnServerInvoke`, never from a captured reference.

### RemoteEvents vs RemoteFunctions

| Aspect | RemoteEvent | RemoteFunction |
|---|---|---|
| Handshake | Fire-and-forget | Request/response |
| Server side | `OnServerEvent:Connect(handler)` | `OnServerInvoke = function(player, ...)` |
| Client side | `OnClientEvent:Connect(handler)`; `FireServer(...)` | `InvokeServer(...)` (yields) |
| Failure mode | Dropped if handler errors | Yields forever if no handler or timeout — always wrap with pcall or use a timeout |
| Best for | Movement input, actions, state updates, frequent small messages | Transactions needing a result (get inventory, validate purchase) |
| Security | Validate every payload | Validate every payload; never return server-internal data |

### Streaming

- `Workspace.StreamingEnabled = true` loads chunks of the world on demand based on player position and `StreamOutBehavior` (default `Destroy`).
- Instances inside a streamed-in region fire `ChildAdded`/`AncestryChanged` on clients — use `WaitForChild` with a timeout or `Instance.DescendantAdded` to avoid nil access on streamed-in parents.
- Never assume a workspace part exists at client load; gate logic on the region being loaded (`workspace:WaitForChild("Map", 10)` style waits with timeouts).
- Streaming is the biggest cause of "UI race" and "missing part" bugs; keep critical scripts in `ReplicatedStorage` (always available) rather than `Workspace`.

### Physics determinism limits

- Physics is **not deterministic across clients or runs**: `Touched` order, collision resolution, and `BodyVelocity`/`BodyPosition` drift vary with frame rate and network jitter.
- Never compute gameplay-critical results from `Touched` alone — re-validate server-side (position checks, ownership checks).
- `RunService.Heartbeat` runs at physics rate (60 Hz nominal but can drop); never assume constant `dt` — pass the delta-time argument.
- Constraint-based mechanisms (Hinges, Springs, WeldConstraints) are robust; raw CFrame writes from client scripts desync and get corrected.
- For ranked/competitive mechanics, compute authoritative results on the server from server state, not from client-reported motion.

## LUAU

### Language model

- **Type inference**: Luau infers types from literals and usage; annotate public module boundaries with `type` aliases. Example: `type PlayerData = { Coins: number, Level: number, Inventory: {[string]: number} }`. Use `typeof(...)` for structural types. This is documentation and lint-verified — catch errors before runtime.
- **Tables**: the single data structure; arrays (integer keys, use `ipairs`/`#`) vs dictionaries (`pairs`). Never mix sparse integer keys with `#`. `table.create(n, v)` pre-fills a table; `table.freeze` makes read-only tables (use for configs/constants).
- **Metatables**: OO and operator overloading via `__index`, `__newindex`, `__call`, `__tostring`, `__eq`. Pattern: `local C = {}; C.__index = C; function C.new(...) return setmetatable({...}, C) end`. Overriding `__index` on hot paths adds a lookup cost.
- **Closures**: first-class functions with upvalues; use them for callbacks and encapsulating private state (module-local "private" variables). Beware closure capture in loops — capture the loop variable by copy when needed.
- **Task library**: `task.spawn`, `task.delay`, `task.wait`, `task.cancel`, `task.defer` replace the legacy `spawn`/`delay`/`wait` and do not yield on the main thread incorrectly. Prefer them everywhere.
- **Safety**: `pcall`/`xpcall` for expected failures (DataStore, MarketplaceService, remote calls). `math.clamp` for numeric ranges. No global mutable state; every module returns a single table or function.

### Performance idioms (O(n) and frame-budget discipline)

- **Cache property access** — hoist `local pos = part.Position`; do not re-read properties inside per-frame loops when stable; property reads are reflection + occasional allocation.
- **Avoid per-frame allocations** — hoist table/vector construction out of `Heartbeat`/`RenderStepped`. Prefer pooling (`ParticleEmitter:Emit(n)`, object pools for projectiles/VFX) over `Instance.new` in hot loops.
- **Batch iteration** — process large collections in chunks (e.g. 100/frame) and `task.wait()` between batches to keep frame time flat.
- **Connection hygiene** — every `:Connect` returns a `RBXScriptConnection`; disconnect when done or route through a connection manager. Leaked connections accumulate listeners and memory.
- **Minimize `WaitForChild` in hot paths** — cache resolved instances at startup; `WaitForChild` yields and can stall scripts.
- **Profile before optimizing** — measure with `collectgarbage("count")`, `os.clock()`, and the Studio Performance Console before changing anything. Do not guess.
- **Streaming-friendly design** — keep always-needed scripts/assets in `ReplicatedStorage`; treat `Workspace` content as load-on-demand.

### Code patterns (shared)

**Module class factory** — the canonical reusable-module shape; use for DataStore wrappers, managers, and systems:

```lua
-- ReplicatedStorage.Modules.MyModule (or ServerScriptService for server-only)
local MyModule = {}
MyModule.__index = MyModule

function MyModule.new(config)
    return setmetatable({ config = config or {} }, MyModule)
end

function MyModule:DoSomething()
    -- implementation
end

return MyModule
```

**Private state via closure** — module-local variables are invisible to callers:

```lua
local State = {}
do
    local secret = {}
    function State.Get(key) return secret[key] end
    function State.Set(key, value) secret[key] = value end
end
return State
```

**Typed table at module boundary**:

```lua
-- Document shape, validated by the Luau type checker.
type PlayerData = { Coins: number, Level: number, Inventory: {[string]: number} }
local DEFAULT_DATA: PlayerData = table.freeze({ Coins = 0, Level = 1, Inventory = {} })
```

**Event-dispatch helper** (avoid anonymous listener sprawl):

```lua
local E = {}
local listeners = {}
function E:On(name, fn)
    local bucket = listeners[name]
    if not bucket then
        bucket = {}
        listeners[name] = bucket
    end
    table.insert(bucket, fn)
end
return E
```

**Loop-capture guard** — closures capture loop variables by reference; bind a copy when needed:

```lua
local buttons = { ... }
for i, button in ipairs(buttons) do
    local index = i
    button.Activated:Connect(function() print("clicked", index) end)
end
```

## DOMAIN WORKFLOWS

One compressed workflow per domain. Each row: key APIs, common pitfalls, and the MCP verification that gates completion.

### UI/UX

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| ScreenGui, Frame, TextLabel, TextButton, ScrollingFrame, UIGridLayout, UIListLayout, UIPadding, UIScale, UICorner, UIStroke, UIAspectRatioConstraint, TweenService, `GroupTransparency`, `ZIndexBehavior.Sibling` | Missing `ResetOnSpawn = false` (HUD destroyed on respawn); nested frames deeper than 3 levels; absolute positions instead of UIPadding/scales; no mobile/tablet viewport testing | `screen_capture` before/after; compare to reference; `get_console_output` for UI errors; `execute_luau` Client context to build/verify GUI |

### Networking

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| RemoteEvent, RemoteFunction, `FireServer`, `FireClient`, `FireAllClients`, `OnServerEvent`, `OnClientEvent`, `OnServerInvoke`, `InvokeServer`, wrapper modules, rate limiters | Trusting client payloads; no validation on the server; unbounded remote frequency (spam); using RemoteFunction where an event suffices (yields); no timeout handling | `execute_luau` Server context for handlers, Client context for fire calls; `get_console_output` for replication errors; red-team-qa review of every new remote |

### Data persistence

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| DataStoreService, `GetDataStore(name, scope)`, `GetAsync`, `SetAsync`, `UpdateAsync`, `IncrementAsync`, `GetSortedAsync`, `RemoveAsync`, session locking, versioned store names | No pcall around DataStore calls (error 500s); ignoring rate limits (per-key/second); losing data on server crash without session lock; unversioned keys breaking migrations; exposing keys to clients | `execute_luau` Server context save/load cycle; `get_console_output` for DataStore errors; verify persistence across two play sessions and with multiple simulated players |

### Economy

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| MarketplaceService, `ProcessReceipt`, `UserOwnsGamePassAsync`, `GetProductInfo`, DevProducts, GamePasses, private servers, leaderstats Folder/IntValue | Client-editable currency (must be server-authoritative); ProcessReceipt returning `NotProcessedYet` after granting (double-grant risk); no receipt dedup; leaderstats created too late | `execute_luau` Server context: mock a receipt, assert single grant; `get_console_output`; red-team-qa review of purchase flow |

### Security

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| Server authority, input validation (`type` checks, `math.clamp`, string sanitizers, allowlist tables), rate limiters, anti-exploit monitors, `player:Kick`, unique remote names per feature | Remote spoofing (client calls server APIs directly); value-object tampering (IntValue/leaderstats edited by client); module injection via `require` of untrusted content; no logging of violations; admin commands reachable from client | `script_grep` audit of all attack surfaces; `execute_luau` Client context to attempt spoofed calls; `red-team-qa` adversarial review; verify server rejects invalid input |

### Performance

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| RunService, `Heartbeat`, `RenderStepped`, object pools, connection managers, batched processing, `collectgarbage`, `os.clock`, `StreamingEnabled`, Debris | Per-frame allocations; unbounded particle/instance counts; `while true do` loops without yield; leaked connections; `WaitForChild` in hot paths; premature optimization without profiling | `execute_luau` memory before/after; `get_console_output` for warnings; `screen_capture` to confirm visual quality maintained; frame-time comparison where possible |

### VFX

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| ParticleEmitter, Beam, Trail, Attachment, Lighting, Atmosphere, BloomEffect, ColorCorrectionEffect, DepthOfFieldEffect, Debris | Over-emitting (thousands of live particles); no `Debris:AddItem` cleanup; beams without FaceCamera on billboards; continuous emission instead of `Emit(n)` bursts; destroying/recreating effects instead of pooling | `screen_capture` before/after; compare to reference; `get_console_output`; `execute_luau` Edit context to create effects |

### Animation

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| TweenService, TweenInfo, Animator, AnimationTrack, AnimationController, Motor6D, RunService.Heartbeat, easing enums | Tweens never cleaned up on state change (drift); `AnimationId` changes not re-`LoadAnimation`; connecting Heartbeat without disconnecting; assuming constant framerate | `start_stop_play(true)`; `screen_capture` motion state; `get_console_output`; adjust easing/timing and re-capture |

### 3D assets

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| MeshPart, SpecialMesh, MaterialVariant, `generate_mesh`, `generate_material`, `generate_procedural_model`, `search_asset`, `insert_asset`, `store_image`, `upload_image`, maxTriangles | Vague generation prompts (underspecified meshes); wrong scale for game units; searching/generating when a Creator Store asset already fits; skipping visual verification | `search_asset` first; `screen_capture` of the inserted/generated asset; `inspect_instance` property check; compare to reference |

### Audio

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| Sound, SoundService, `RollOffMode`, `RollOffMaxDistance`, `RollOffMinDistance`, Looped, `Play`, `Stop`, TweenService for fades, audio zones via Touched | Global music parented to a part (only plays in range); no roll-off on 3D sounds; stacking sounds without pooling; no fade transitions | `execute_luau` Client context playback test; `get_console_output`; `screen_capture` not applicable — verify via console and `execute_luau` (e.g. print Playing state) |

### Terrain

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| workspace.Terrain, `FillRegion`, `FillWedge`, Region3, Material enum, Sky, `setSkybox`, foliage placement, biome tables | Filling huge regions at high resolution (performance blow-up); inconsistent resolution; skybox not applied to all faces; foliage models not anchored | `screen_capture` before/after terrain changes; compare to reference; `get_console_output`; `inspect_instance` on Terrain |

### Plugins

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| plugin, `CreateToolbar`, `CreateButton`, `CreateDockWidgetPluginGui`, DockWidgetPluginGuiInfo, Selection, `GetSetting`/`SetSetting`, `InitialDockState` | No cleanup of toolbar/button connections on plugin disable; widget enabled state not persisted; untested in a fresh Studio session; no settings persistence | `execute_luau` Edit context to run plugin code; `search_game_tree` to verify structure; `get_console_output`; manual Studio test |

### Testing

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| TestEZ-style suites, simple pcall runners, `start_stop_play`, `character_navigation`, `user_keyboard_input`, `user_mouse_input`, `screen_capture` visual regression | Tests only on client or only on server; no cleanup of test data; visual checks skipped; no edge/error-case coverage; asserting with tolerance on frame-dependent state | `start_stop_play(true)`; `execute_luau` test suite in both contexts; `get_console_output` results; `screen_capture`; `start_stop_play(false)` |

### Cinematics

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| workspace.CurrentCamera, TweenService camera paths, letterbox frames, fade overlays, dialogue GUI, input lockdown (ContextActionService) | Player input during cutscene; camera tween blocking the main thread (`tween.Completed:Wait()` chains); UI not cleaned after cutscene; frame-rate-dependent pacing | `start_stop_play(true)`; `screen_capture` key frames; `get_console_output`; verify input disabled via `user_keyboard_input` |

### Avatar

| Key APIs | Common pitfalls | MCP verification |
|---|---|---|
| HumanoidDescription, `ApplyDescription`, body colors, scale properties, Shirt, Pants, ShirtGraphic, Accessory, InsertService:LoadAsset, R15/R6 | Applying descriptions before character load; accessory welds broken on respawn; not removing old clothing/accessories before applying new; only testing one rig type | `execute_luau` Client context to apply customization; `screen_capture` of the character; test both R15 and R6; `get_console_output` |

## DECISION TREE

```
Any Roblox/Luau task
├─ Task touches 2+ domains (e.g. inventory = UI + persistence + networking)?
│   └─ Yes → Orchestration path (below); assign subagents, integrate, QA.
├─ Pure Luau coding / scripts / modules / event systems?        → coding workflow
├─ GUI / HUD / menus / responsive layout / themes?              → UI/UX workflow
├─ RemoteEvent / RemoteFunction / client-server traffic?        → networking workflow
├─ DataStore / save / load / migration / session lock?          → data persistence workflow
├─ DevProducts / GamePasses / currency / receipts?              → economy workflow
├─ Anti-exploit / validation / server authority audit?          → security workflow
├─ Profiling / memory / pooling / streaming optimization?       → performance workflow
├─ Particles / beams / lighting / post-processing?              → VFX workflow
├─ Tweens / character animation / rigs / procedural motion?     → animation workflow
├─ Meshes / materials / models / textures / Creator Store?      → 3D assets workflow
├─ Music / SFX / 3D audio / audio zones?                        → audio workflow
├─ Terrain / biomes / foliage / skybox / world building?        → terrain workflow
├─ Studio plugins / toolbars / DockWidget?                      → plugins workflow
├─ Tests / playtest automation / input simulation / QA?         → testing workflow
├─ Cutscenes / camera paths / dialogue / letterboxing?          → cinematics workflow
└─ Avatar / customization / outfits / HumanoidDescription?      → avatar workflow
```

**Client vs server placement:**

- Client only: UI construction/updates, camera control, input handling, character-local cosmetics, animation playback triggers.
- Server only: DataStore I/O, economy mutations, authority decisions (damage, movement validation, purchases), anti-exploit enforcement, physics-authoritative logic.
- Both (replicate): RemoteEvent/RemoteFunction definitions in ReplicatedStorage, shared ModuleScripts, shared type definitions.

**Orchestration path (multi-domain tasks):** 1) decompose into the domain workflows above; 2) identify dependencies (architecture → data layer → networking → server logic → client UI → VFX → testing); 3) run independent work in parallel, dependent work in sequence; 4) integrate and run the VERIFICATION GATE end-to-end; 5) never declare done until all checks pass.

## FAILURE MODES & MITIGATIONS

1. **Replication race on client-authoritative state.** Detection: server reads a value the client just wrote and gets a stale/rolled-back value; `console` shows property revert warnings. Fix: keep authoritative state server-side; treat client data as untrusted input and write it back through validated remotes; never rely on client-side `Value` objects for gameplay logic.
2. **DataStore rate limiting / 403 errors.** Detection: `get_console_output` shows "Requests exceed the rate limit" from GetAsync/SetAsync. Fix: `pcall` every DataStore call, exponential backoff retry, batch writes, cache reads in memory, version the store name (`_v1`) and respect the per-key per-second budget.
3. **Session locking / lost writes.** Detection: two servers both modify the same player data; a player's save is lost on crash. Fix: acquire a session lock key on join and release on leave (with a stale-lock timeout), single-writer per player, auto-save every 120 s with last-write-wins guarded by lock ownership.
4. **Remote spoofing exploit.** Detection: a client invokes a server remote with fabricated payloads (speed, currency, item id); `red-team-qa` finds an unvalidated `OnServerEvent`. Fix: server-authoritative validation on every payload (type, range via `math.clamp`, allowlist), per-player rate limiting per action, unique remote names per feature, log violations and kick after threshold.
5. **Value-object tampering.** Detection: `leaderstats` or an IntValue backing currency changes without a server write; clients modify a replicated Value directly. Fix: never read gameplay-critical values from replicated Value objects; keep the authoritative copy server-side and replicate display-only values; validate on server before any state change.
6. **Streaming pop-in / missing parts.** Detection: `nil` index errors on Workspace children at load; parts referenced in scripts are gone after a region unloads. Fix: enable streaming-aware access (`WaitForChild` with timeout or DescendantAdded), keep critical scripts/assets in ReplicatedStorage, set `StreamOutBehavior` deliberately, gate logic on the region being loaded.
7. **Memory leaks from event connections.** Detection: memory climbs across respawns (`collectgarbage("count")`); console shows connection warnings on PlayerRemoving. Fix: disconnect or route through a connection manager tied to the player lifecycle; use `task.cancel` for cancellable work; never capture `player` in long-lived closures after removal.
8. **TweenService drift.** Detection: UI/parts end at wrong positions after a tween; repeat tweens overshoot; `tween.Completed` fires late or never after parent destruction. Fix: capture original properties, cancel prior tweens on the same instance before starting a new one, guard `tween.Completed` callbacks against destroyed instances, prefer one tween per property group.
9. **UI layout race with streaming.** Detection: GUI referencing streamed-in parts positions at 0,0 or errors; UI built before the world loads. Fix: wait for both the world region and the PlayerGui before measuring; use `UIScale`/`UIPadding` instead of absolute offsets; rebuild UI on respawn with `ResetOnSpawn = false` for persistent HUDs.
10. **Client-authoritative physics/mechanics.** Detection: `Touched` fires inconsistently across clients; movement hacks (speed/clip) work because client reports its own position. Fix: validate movement/damage server-side against server-owned state; use BodyMovers/constraints from server; never trust client-reported positions for rewards or collisions.
11. **RemoteFunction yield hang.** Detection: a client `InvokeServer` never returns; the character freezes; console shows no error. Fix: wrap invokes in `pcall` with a timeout (`task.delay` + flag), prefer RemoteEvents for non-essential flows, always ensure a server handler is connected before invoking.
12. **Unbounded particle/VFX emission.** Detection: frame rate drops when effects run; memory spikes. Fix: `ParticleEmitter:Emit(n)` bursts instead of continuous high rate, `Debris:AddItem` cleanup, cap live particles (< 1000), pool reusable effects instead of destroy/recreate.
13. **ProcessReceipt double-grant.** Detection: a DevProduct purchase grants currency twice after a retry. Fix: track processed receipt IDs in DataStore, return `PurchaseGranted` only after the grant is persisted, return `NotProcessedYet` for unprocessable receipts so Roblox retries safely.
14. **Global state / module cycle requires.** Detection: scripts reference globals that error "attempt to index a nil value"; `require` cycles. Fix: module pattern only (`local M = {}; return M`), no global assignment, dependency injection via requires, keep scripts under ~500 lines.

## VERIFICATION GATE

Every Roblox change must pass this gate before being reported as done:

1. **Console clean**: `get_console_output()` shows zero errors and no new warnings attributable to the change. Fix any error, then re-run.
2. **Integration tests**: `execute_luau` runs in the context where the code executes — Server context for server logic, Client context for client logic, Edit for instance/plugin creation. Assert the expected behavior (state change, returned value, instance existence).
3. **Visual check**: `screen_capture()` for any UI, VFX, terrain, animation, cinematic, avatar, or 3D-asset change. When a reference image exists, iterate until pixel match. Re-verify at a second viewport/camera angle for responsive/3D work.
4. **Playtest**: `start_stop_play(true)` → `character_navigation` + `user_keyboard_input`/`user_mouse_input` where the feature is interactive → `get_console_output` → `start_stop_play(false)`.
5. **Security review**: any networking or economy change requires a red-team-qa review (adversarial payloads, rate-limit audit, server-authority check) before sign-off.
6. **Persistence check** (when data is involved): verify data survives across two play sessions and multiple players.
7. **Performance sanity** (when relevant): `collectgarbage("count")` before/after and frame-time comparison confirm no regression.
8. **QA sign-off**: never report "done" while the console shows errors, tests fail, or visual comparison does not match. Report status as complete only when ALL checks pass.

## REFERENCES

- Roblox DataModel: https://create.roblox.com/docs/reference/engine/classes/DataModel
- Roblox services overview: https://create.roblox.com/docs/exploration (engine services list)
- RemoteEvent: https://create.roblox.com/docs/reference/engine/classes/RemoteEvent
- RemoteFunction: https://create.roblox.com/docs/reference/engine/classes/RemoteFunction
- DataStoreService: https://create.roblox.com/docs/reference/engine/classes/DataStoreService
- DataStore best practices: https://create.roblox.com/docs/cloud-services/datastores
- MarketplaceService: https://create.roblox.com/docs/reference/engine/classes/MarketplaceService
- StreamingEnabled: https://create.roblox.com/docs/workspace/streaming
- TweenService: https://create.roblox.com/docs/reference/engine/classes/TweenService
- RunService: https://create.roblox.com/docs/reference/engine/classes/RunService
- Luau language: https://luau.org
- Luau type checking: https://luau.org/typecheck
- Luau performance: https://luau.org/performance
- Roblox API reference (classes index): https://create.roblox.com/docs/reference/engine
- Roblox Luau article: https://create.roblox.com/docs/luau
- Roblox performance guide: https://create.roblox.com/docs/performance-optimization
- Roblox plugins: https://create.roblox.com/docs/plugins
- Roblox avatar/HumanoidDescription: https://create.roblox.com/docs/reference/engine/classes/HumanoidDescription
- Roblox test automation: https://create.roblox.com/docs/studio/ui-actions

## SUBAGENT PROTOCOL

Map the task to the right implementation/QA agent. The developer (this skill) writes code; specialized agents QA and review.

| Responsibility | Agent |
|---|---|
| Writing new scripts / systems | code-implementer |
| Architecture / module structure / refactor | refactoring-specialist |
| Code review (correctness, security) | red-team-qa |
| Performance profiling / optimization review | performance-engineer |
| Penetration / adversarial security testing | cybersecurity-specialist |
| Accessibility review of touch/UI flows | accessibility-specialist |
| Data migration / JSON/data correctness | data-engineer |
| Visual verification / reference comparison | screen_capture + comparison |
| Browser automation for web asset acquisition | browser-automation |

For multi-domain features, the Orchestration path in the DECISION TREE coordinates these agents; never merge QA and implementation responsibilities in the same pass.

## CODE PATTERNS

Consolidated, production-grade patterns extracted from the source suite. Each is annotated with the pitfall it avoids.

### State machine (game/UI state transitions)

```lua
local SM = {}
SM.__index = SM

function SM.new()
    return setmetatable({ states = {}, currentState = nil }, SM)
end

function SM:AddState(name, state) self.states[name] = state end

function SM:Transition(newName)
    if self.currentState then self.currentState:Exit() end
    self.currentState = self.states[newName]
    if self.currentState then self.currentState:Enter() end
end

function SM:Update(dt)
    if self.currentState then self.currentState:Update(dt) end
end

return SM  -- Avoids opaque if/else if/else chains; states are first-class tables.
```

### DataStore wrapper (pcall + cache + UpdateAsync)

```lua
local DataStoreService = game:GetService("DataStoreService")

local Store = {}
Store.__index = Store

function Store.new(name, version)
    return setmetatable({
        store = DataStoreService:GetDataStore(name .. "_v" .. (version or 1)),
        cache = {},
    }, Store)
end

function Store:GetAsync(key)
    if self.cache[key] ~= nil then return self.cache[key] end     -- read cache, O(1)
    local ok, data = pcall(function() return self.store:GetAsync(key) end)  -- never uncaught
    if ok then self.cache[key] = data end
    return ok and data or nil
end

function Store:SetAsync(key, value)
    local ok, err = pcall(function() return self.store:SetAsync(key, value) end)
    if ok then self.cache[key] = value end
    return ok, err
end

function Store:UpdateAsync(key, fn)
    -- UpdateAsync guarantees atomic read-modify-write; use for economy/numeric state.
    local ok, result = pcall(function() return self.store:UpdateAsync(key, fn) end)
    if ok then self.cache[key] = result end
    return ok, result
end

return Store
```

### Object pool (avoid per-frame Instance.new churn)

```lua
local Pool = {}
Pool.__index = Pool

function Pool.new(template, size)
    local self = setmetatable({ template = template, available = {}, active = {} }, Pool)
    for _ = 1, (size or 10) do
        local obj = template:Clone()
        obj.Parent = nil
        table.insert(self.available, obj)
    end
    return self
end

function Pool:Get()
    local obj = table.remove(self.available) or self.template:Clone()
    table.insert(self.active, obj)
    return obj
end

function Pool:Return(obj)
    obj.Parent = nil
    self.active[table.find(self.active, obj)] = nil   -- O(1) index removal
    table.insert(self.available, obj)
end

return Pool
```

### Connection manager (leak prevention)

```lua
local Connections = { list = {} }

function Connections:Add(conn)
    table.insert(self.list, conn)
    return conn
end

function Connections:Clean()
    for _, conn in ipairs(self.list) do
        if conn.Connected then conn:Disconnect() end
    end
    self.list = {}
end

return Connections
```

### Server-authoritative remote (validate BEFORE acting)

```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Event = ReplicatedStorage:WaitForChild("Events"):WaitForChild("MoveRequest")

Event.OnServerEvent:Connect(function(player, target)
    -- 1) type-check, 2) range-check via clamp, 3) allowlist, 4) rate limit
    if typeof(target) ~= "Vector3" then return end
    local root = player.Character and player.Character.PrimaryPart
    if not root then return end                     -- no character, no action
    local MAX = 64
    if (target - root.Position).Magnitude > MAX then
        return                                      -- reject out-of-range teleport
    end
    -- 5) apply ONLY after validation
    root.CFrame = CFrame.new(target)
end)
```

### Rate limiter (per-actor, sliding window)

```lua
local Limits = {}
function Limits.accept(player, action, maxPerWindow, windowSec)
    local key = player.UserId .. ":" .. action
    local now = tick()
    local buf = Limits[key] or {}
    local valid = {}
    -- keep only fresh entries to bound memory
    for _, t in ipairs(buf) do if now - t < windowSec then table.insert(valid, t) end end
    if #valid >= maxPerWindow then Limits[key] = valid; return false end
    table.insert(valid, now); Limits[key] = valid; return true
end
```

### UI responsive pattern (viewport-aware)

```lua
local camera = workspace.CurrentCamera
local frame = script.Parent.Frame  -- inside a ScreenGui in StarterGui

local function relayout()
    local vp = camera.ViewportSize
    local mobile = vp.X < 768
    frame.Size = mobile and UDim2.new(0.9, 0, 0.4, 0) or UDim2.new(0.3, 0, 0.5, 0)
end

camera:GetPropertyChangedSignal("ViewportSize"):Connect(relayout)
relayout()
```
Keep GUI scripts in StarterPlayerScripts / under PlayerGui; set ResetOnSpawn = false for persistent HUDs.

## OUTPUT FORMAT

```text
[ROBLOX LUA DEVELOPER]
Task: {description}
Domain workflow(s): {coding | ui-ux | networking | persistence | economy | security | performance | vfx | animation | 3d-assets | audio | terrain | plugins | testing | cinematics | avatar | orchestration}
Files Modified: {list}
MCP Verification: {get_console_output | execute_luau | screen_capture | playtest | security-review | persistence-check | perf-sanity}
Status: {complete | needs-review}
```
