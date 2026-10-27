---
name: roblox-scripting
description: >-
  Builds Roblox game systems in Luau: module architecture, server-authoritative remotes, validated
  payloads, DataStore persistence with session locking, economy receipts, state machines, and
  measured performance. Use when implementing or fixing gameplay logic, networking, saving, or
  purchases. Language/platform fundamentals route to roblox-lua-developer; exploit defense to
  roblox-security; in-Studio tool operations to roblox-studio-mcp.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-scripter
---

# Roblox Scripting

Roblox is a server-authoritative engine with an untrusted client attached. Every system you write
must assume the client can send any payload, at any rate, at any time — and that two servers can
hold the same player's data at once. Get those two assumptions right and most of the platform's
hard bugs disappear.

## WHEN TO USE

- Implementing gameplay: movement, combat, abilities, progression, match state, NPC behavior.
- Networking: RemoteEvents/Functions, request/response flows, rate limits.
- Persistence: player profiles, session locks, migrations, autosave, save-on-leave.
- Economy: currency, shops, DevProducts, GamePasses, receipts.
- Debugging a runtime bug that only appears in a playtest.
- Performance work on server or client scripts.

## WHEN NOT TO USE

- DataModel/containers, Luau typing and module patterns — `roblox-lua-developer` (the platform skill).
- UI layout and input — `roblox-ui-ux`; animation — `roblox-animation`; particles — `roblox-vfx`.
- Adversarial exploit audit — `roblox-security` (call it before shipping any remote or currency path).
- Running Studio tools/playtests — `roblox-studio-mcp`.

## DECISION TREE

```text
1. WHERE DOES THE TRUTH LIVE?
   Gameplay, currency, inventory, damage, progression → server only.
   Client owns: input, camera, local prediction, visual state.
   If a value affects another player or persists, it is server-owned. No exceptions.

2. WHAT IS THE COMMUNICATION SHAPE?
   Client asks, server decides  → RemoteEvent (fire-and-forget)
   Client needs a value now     → RemoteFunction, bounded and fast; wrap/pcall, never InvokeClient
   Frequent disposable updates  → UnreliableRemoteEvent (effects only, never state that matters)
   Server → client notification → RemoteEvent:FireClient / FireAllClients

3. WHAT MUST BE VALIDATED?
   type, structure, size, enum membership, ID existence, ownership, distance, cooldown, balance,
   rate. Reject NaN/inf and unexpected Instance classes/ancestry. Validate against SERVER state,
   never against values the client supplied.

4. WHERE DOES STATE PERSIST?
   In-memory profile per player (loaded once) → session lock → save on leave/shutdown → autosave.
   Writes that depend on current data: UpdateAsync. Simple independent writes: SetAsync.
   Version the schema; migrate on load; never overwrite a failed load with defaults.

5. WHAT IS THE PERFORMANCE SHAPE?
   Per-frame work → Heartbeat, delta-time driven, no allocations in the loop.
   Expensive batch work → chunked, yielding, or Parallel Luau only if profiling proves CPU-bound.
   Clean up every connection, thread, and per-player table entry on removal.

6. HOW WILL IT BE PROVEN?
   Write the behavior test first (roblox-testing), then verify in a real playtest with server and
   client assertions; console clean; rejoin test for anything persisted.
```

## PATTERNS

### 1. Project layout (server / client / shared)
```text
ReplicatedStorage/
  Shared/        Modules used by both sides: types, config, remotes, pure utilities
  Remotes/       RemoteEvent/RemoteFunction instances (created by server at boot)
ServerScriptService/
  Services/      PlayerData, Economy, Combat, Match, RateLimiter, ReceiptProcessor
  Main.server.lua bootstraps services in dependency order
StarterPlayer/StarterPlayerScripts/
  Controllers/   Input, Camera, HUD binding, Prediction
StarterGui/
  HUD/           ScreenGui built as a template, cloned per player
```
Rule: server modules never require client modules; shared modules must be side-effect free.

### 2. Remote contract
```lua
-- ReplicatedStorage/Shared/Remotes.lua
return {
    RequestAttack = "RequestAttack",   -- client → server, no return
    StateChanged  = "StateChanged",    -- server → client
}
```
```lua
-- server handler: validate, rate-limit, apply, replicate
local function onRequestAttack(player: Player, targetId: unknown)
    if typeof(targetId) ~= "Instance" or not targetId:IsA("Model") then return end
    if not RateLimiter:allow(player, "attack", 8) then return end
    local target = targetId
    if target.Parent ~= workspace.Enemies then return end
    if not Combat:canAttack(player, target) then return end   -- distance, cooldown, alive
    Combat:applyDamage(player, target)
end
```
Never `player.leaderstats.Coins.Value += amount`. The server computes the amount.

### 3. Rate limiter (server-side, per player, per action)
Token bucket keyed by `player.UserId .. ":" .. action`; refill at a fixed rate; drop the entry on
`PlayerRemoving`. Return false rather than erroring; log repeated violations for security review.

### 4. Data profile shape
```lua
type Profile = {
    schema = 3,
    coins = 0,
    inventory = { [string] = number },
    stats = { kills = 0, deaths = 0 },
    receipts = { [string] = true },   -- PurchaseId markers, bounded
}
```
Load once into a server table, keep the session lock for the session, save on leave and on
`game:BindToClose`. Autosave on a staggered interval (avoid synchronized spikes), and always
`pcall` + retry with capped backoff and jitter while preserving per-key order.

### 5. Receipt idempotency (DevProducts)
```lua
MarketplaceService.ProcessReceipt = function(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end
    if profile.receipts[receiptInfo.PurchaseId] then
        return Enum.ProductPurchaseDecision.PurchaseGranted
    end
    profile.receipts[receiptInfo.PurchaseId] = true
    profile.coins += productRewards[receiptInfo.ProductId] or 0
    if not saveProfile(player, profile) then
        profile.receipts[receiptInfo.PurchaseId] = nil
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end
    return Enum.ProductPurchaseDecision.PurchaseGranted
end
```
Grant and receipt marker must persist together. Never acknowledge before the save succeeds.

### 6. Loop hygiene
- `RunService.Heartbeat:Connect(function(dt) ... end)` — use `dt`, no `wait()`, no table allocation.
- Store connections and disconnect on removal; use a per-player cleanup table.
- `task.spawn` for fire-and-forget with pcall; `task.defer` when ordering matters.
- Chunk bulk work and `task.wait()` between chunks; never a bare `while true do`.

### 7. Debugging a playtest-only bug
1. Reproduce with `start_stop_play`, then `get_console_output` first — read the exact error.
2. `execute_luau` in Server to inspect authoritative state; in Client for replicated state.
3. Compare what each side believes; the first divergence is the bug (`roblox-studio-mcp` step 5).
4. Fix the mechanism, add a regression test (`roblox-testing`), re-run the same playtest.

## FAILURE MODES & MITIGATIONS

1. **Client-trusted state** — currency, damage, or position accepted from the client. *DETECT:* a
   remote payload used directly in a write. *FIX:* recompute on the server; validate against server state.
2. **Unvalidated payload** — wrong type/shape crashes the handler. *DETECT:* console error on
   malformed input. *FIX:* type/shape/size guards at the top of every handler; reject quietly.
3. **Remote spam** — an exploiter fires 1000×/s. *DETECT:* server frame time spikes; queue growth.
   *FIX:* per-player token bucket + cooldowns; log violations.
4. **RemoteFunction hang** — no handler or a yielding handler. *DETECT:* client freezes. *FIX:* prefer
   events; bound the work; pcall; never `InvokeClient` for logic.
5. **Load-failure overwrite** — DataStore error treated as "new player". *DETECT:* data resets after an
   outage. *FIX:* retry, then refuse to save defaults; session lock.
6. **Double grant** — receipt processed twice. *DETECT:* duplicated currency. *FIX:* PurchaseId marker
   persisted with the grant (pattern 5).
7. **Connection leak** — per-player connections/tables never cleared. *DETECT:* memory grows with
   join/leave cycles. *FIX:* cleanup on `PlayerRemoving`; test 20 join/leave cycles.
8. **Synchronized save spike** — every player saves on the same tick. *DETECT:* throttling errors at
   interval boundaries. *FIX:* stagger autosaves per player.

## QUANTITATIVE RULES

- Every remote: server validation + rate limit + explicit failure behavior. 100% of them.
- Gameplay state: server-authoritative. Client may predict, never decide.
- DataStore: one profile key per player (`User_<UserId>`), ≤4 MiB, schema version present.
- Retries: capped exponential backoff + jitter, max ~5 attempts, per-key order preserved.
- Heartbeat work: no allocations, no waits; budget ≤2 ms typical server frame for gameplay systems.
- Save on leave + `BindToClose`; rejoin test mandatory for any persisted feature.
- Pooling/Parallel Luau only after a measurement shows the need.

## VERIFICATION GATE

- [ ] Every new remote has validation, rate limiting, and a defined rejection path.
- [ ] Currency/inventory/damage computed server-side; client cannot set values.
- [ ] Data loads once, locks the session, saves on leave, and survives a rejoin test.
- [ ] Receipt path is idempotent; a repeated PurchaseId grants once.
- [ ] Console clean during a real playtest in Server and Client contexts.
- [ ] No leaked connections: join/leave cycles do not grow memory.
- [ ] Behavior test exists and fails without the change.

## REFERENCES

- `roblox-lua-developer` — DataModel, replication model, Luau module patterns
- `roblox-security` — exploit audit for remotes, currency, and data
- `roblox-testing` — TestEZ/Jest-Lua and playtest automation
- `roblox-studio-mcp` — how to run and verify any of this in Studio
- Roblox docs: security tactics, remote events, data store best practices
