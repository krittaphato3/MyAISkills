---
name: roblox-lua-developer
description: >-
  Roblox platform and Luau fundamentals: the DataModel tree and containers, core services, the
  client/server replication model, streaming and physics limits, Luau typing and module patterns, and
  where code belongs. Use when you need platform knowledge, a module layout, or a Luau language
  question. Implementing systems routes to roblox-scripting; Studio tool operation to
  roblox-studio-mcp; UI/world/animation/VFX/assets to their Roblox skills.
metadata:
  version: 4.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-scripter
---

# Roblox Platform & Luau

The shared foundation under every Roblox discipline: what the DataModel is, what replicates, where
code belongs, and how Luau differs from Lua. Read this before the first script in a project; come back
when a bug turns out to be a replication or container mistake rather than a logic error.

## WHEN TO USE

- Starting work in a Roblox place and deciding where scripts and modules belong.
- A question about the DataModel, services, replication, streaming, or physics behavior.
- Luau language questions: types, metatables, task library, module patterns, performance idioms.
- Reviewing a project layout or a new module structure.
- A bug that smells like replication (works on the server, not the client — or vice versa).

## WHEN NOT TO USE

- Implementing gameplay, remotes, persistence, economy — `roblox-scripting`.
- UI, world building, animation, VFX, assets, security, testing — their Roblox skills.
- Driving Studio tools or playtests — `roblox-studio-mcp`.
- Planning a game or a milestone — `roblox-game-production`.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. DOES THE CODE RUN ON SERVER, CLIENT, OR BOTH?
   Server-only state and authority → ServerScriptService / ServerStorage
   Shared pure logic, types, config → ReplicatedStorage.Shared
   Client presentation and input     → StarterPlayerScripts / StarterGui
   Misplaced code is the most common Roblox architecture bug: fix the container first.

2. DOES IT NEED TO REPLICATE?
   Yes, to all clients → ReplicatedStorage (assets, remotes, shared modules)
   No, server only     → ServerStorage / ServerScriptService
   Per-player template → StarterGui / StarterPlayerScripts (cloned on spawn)

3. IS IT A LANGUAGE QUESTION?
   Types, tables, metatables, task.*, perf idioms → references/luau.md
   Common module/class patterns          → references/code-patterns.md

4. IS IT A REPLICATION-SHAPED BUG?
   Server value correct, client stale → check the property replicates and the client waits for it
   Client change reverts               → expected: the server owns non-owned instances
   Missing instance after spawn        → streaming; use WaitForChild with a timeout

5. IS IT A PERFORMANCE QUESTION?
   → roblox-scripting for loops/allocations; roblox-world-building for scene cost;
     roblox-vfx for particles; roblox-testing for measurement.
```

## THE DATAMODEL

Everything is an `Instance` under `game`. The containers that matter:

| Container | Role | Replicates |
|---|---|---|
| `Workspace` | Runtime world: parts, terrain, camera, characters | Yes (physics + most writes) |
| `ReplicatedStorage` | Shared modules, remotes, reusable assets | Yes |
| `ServerScriptService` | Server scripts and services | No |
| `ServerStorage` | Server-only templates and secrets | No |
| `StarterPlayer` / `StarterPlayerScripts` | Client scripts cloned per player | Templates |
| `StarterGui` | ScreenGui templates cloned into PlayerGui | Templates |
| `Players` | Player instances, characters, PlayerGui | Yes |
| `Lighting` | Global lighting, Atmosphere, post effects | Yes |
| `SoundService` | Global audio settings | Yes |
| `DataStoreService` | Persistence (server only) | No (service) |

Rule of thumb: if a client must see it, it lives in a replicated container; if it must not, it lives in
ServerStorage/ServerScriptService. Secrets never go in ReplicatedStorage.

## REPLICATION MODEL

- Roblox is **server-authoritative**. The server simulates; clients receive a replicated, interpolated
  view and can predict locally.
- **Only server writes replicate.** A client edit to a non-owned instance is reverted by the server.
- **Characters and physics replicate**; smoothness comes from client interpolation, not from trusting
  client transforms.
- **RemoteEvents** fire and forget; **RemoteFunctions** yield for a response (use sparingly, bound the
  work, never `InvokeClient` for logic); **UnreliableRemoteEvents** are for disposable updates only.
- Every remote payload is hostile input: validate type, shape, size, ownership, distance, and rate on
  the server (`roblox-scripting`, `roblox-security`).

### Streaming
`Workspace.StreamingEnabled` loads Workspace content on demand. Consequences:
- Workspace instances can appear and disappear; client code must use `WaitForChild` with a timeout.
- Critical scripts/configs belong in ReplicatedStorage, not Workspace.
- Keep static model extents modest (≈64 cubic studs) so they stream as a unit.

### Physics determinism
Physics is **not deterministic** across clients or runs: `Touched` order, collisions, and constraint
drift vary with frame rate and latency. Never compute gameplay-critical outcomes from `Touched` or
client-reported positions — re-validate on the server. `Heartbeat` provides a delta time; never assume
a constant step.

## PROJECT LAYOUT

```text
ReplicatedStorage/
  Shared/        types, config, pure utilities, remotes definitions
  Assets/        reusable props, UI templates, effects
ServerScriptService/
  Services/      PlayerData, Economy, Combat, Match, RateLimiter, Receipts
  Main.server.lua
StarterPlayer/StarterPlayerScripts/
  Controllers/   Input, Camera, HUD binding, Prediction
StarterGui/
  HUD/           ScreenGui template
```
- Server modules must never require client modules.
- Shared modules must be side-effect free (no yielding at require time, no service calls at load).
- Bootstrap services in dependency order from one `Main.server.lua`.
- Type public module APIs and remote payloads; enable `--!strict` incrementally.

## LUAU ESSENTIALS

See `references/luau.md` for the full treatment. The high-leverage differences from Lua:
- Gradual typing (`--!strict`, `type`, `export type`) — catches interface mistakes, does **not**
  validate network input.
- `task.wait` / `task.spawn` / `task.defer` / `task.delay` instead of `wait`/`spawn`.
- Generalized iteration, string interpolation, `continue`, compound assignment.
- `typeof` distinguishes Roblox types (`Vector3`, `CFrame`, `Instance`) where `type` returns "userdata".
- Performance: avoid per-frame table allocation, cache `game:GetService` results, prefer
  `table.create`, avoid `Instance.new` in hot loops.

See `references/code-patterns.md` for module/class/state-machine patterns used across the suite.

## FAILURE MODES & MITIGATIONS

1. **Wrong container** — server logic in ReplicatedStorage, or a secret in a replicated folder.
   *DETECT:* clients can read what they should not; duplicated execution. *FIX:* move to
   ServerScriptService/ServerStorage; audit replicated contents.
2. **Client writes trusted state** — expecting a client change to persist. *DETECT:* value snaps back.
   *FIX:* server owns it; client sends intent (`roblox-scripting`).
3. **Streaming nil** — assuming a Workspace descendant exists on the client. *DETECT:* nil index
   errors at spawn. *FIX:* WaitForChild with timeout; keep critical data out of Workspace.
4. **Physics as truth** — using `Touched` for damage or pickups. *DETECT:* missed/duplicate hits.
   *FIX:* server-side distance/state validation; use Touched as a hint only.
5. **Service lookup churn** — `game:GetService` in hot loops. *DETECT:* frame-time cost. *FIX:* cache at
   module top.
6. **Require cycles / side effects** — modules that yield or run logic on require. *DETECT:* load-order
   bugs. *FIX:* side-effect-free shared modules, explicit init functions.

## QUANTITATIVE RULES

- Critical configs/remotes in ReplicatedStorage; server-only data in ServerStorage.
- Every client `WaitForChild` on a streamed path has a timeout.
- No `game:GetService` inside a per-frame loop; cache it.
- `--!strict` on new shared modules and data schemas where feasible.
- Streaming baseline for large worlds: MinRadius 64 / TargetRadius 1024 (verify on device).
- Physics-derived gameplay decisions are always re-validated on the server.

## VERIFICATION GATE

- [ ] Each new module lives in the correct container for its replication needs.
- [ ] Shared modules are side-effect free and require-safe.
- [ ] Client code tolerates streamed-in/out instances.
- [ ] No secret or server-only logic is replicated.
- [ ] Physics-driven gameplay has a server-side validation path.
- [ ] Hot-path service lookups and allocations checked.

## REFERENCES

- `references/luau.md` — type system, tables, metatables, task library, performance idioms
- `references/code-patterns.md` — module, class, and state-machine patterns
- `roblox-scripting` — systems: remotes, data, economy, performance
- `roblox-studio-mcp` — reading and editing the DataModel in Studio
- `roblox-security` — the trust boundary in practice
- Roblox docs: instances, replication, instance streaming, Luau
