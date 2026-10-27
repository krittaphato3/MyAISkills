---
name: roblox-security
description: >-
  Defends a Roblox game against exploiters: trust boundaries, remote and ProximityPrompt validation,
  rate limits, server-authoritative economy, DataStore integrity, secret handling, and a pre-ship
  audit with reproducible attack tests. Use when adding any remote, reward, purchase, teleport,
  admin surface, or player-data path, or before publishing. General web/app security routes to
  security-hardening-specialist; broader threat modeling method to threat-modeling.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-security-engineer
---

# Roblox Security

In Roblox, every client is fully controlled by the player. They can read every replicated instance,
call any remote with any arguments, fire at any rate, and execute their own Luau. There is no
"trusted client" mode. Security here is not hardening an app — it is designing as if the attacker is
already inside the client, because they are.

## WHEN TO USE

- Any new RemoteEvent/RemoteFunction, ProximityPrompt, ClickDetector, or tool interaction.
- Currency, rewards, inventory, progression, trading, purchases.
- Player data writes and migrations.
- Admin/debug commands, teleport flows, matchmaking, leaderboards.
- Before publishing: a full exploit-surface audit.
- After a duplication or cheat report.

## WHEN NOT TO USE

- Server-side web/API security outside Roblox — `security-hardening-specialist`.
- GDPR/privacy obligations — `privacy-compliance`.
- General threat-modeling method for a non-Roblox design — `threat-modeling`.
- Performance-only reviews — `roblox-scripting` / `roblox-testing`.

## DECISION TREE

```text
1. MAP THE TRUST BOUNDARY
   Client-owned: input, camera, local UI, prediction.
   Server-owned: character state that matters, currency, inventory, damage, rewards, ownership.
   Everything crossing the boundary is hostile input until validated.

2. ENUMERATE THE SURFACE
   Remotes · ProximityPrompts/ClickDetectors · Tools · Humanoid state · Value objects ·
   Client modules · Teleports · DataStore writes · HTTP endpoints · Admin commands ·
   Marketplace receipts · Shared attributes/tags.

3. FOR EACH SURFACE, ASK THE FOUR QUESTIONS
   Can the client choose the target? Can it choose the amount? Can it call this repeatedly?
   What does the server verify against its own state before acting?

4. APPLY THE CONTROLS
   Type/shape/size validation · allowlists for IDs · ownership + distance + line-of-sight checks ·
   cooldown + token-bucket rate limit · server-computed rewards · idempotent receipts ·
   audit logging of rejections.

5. PROVE IT WITH AN ATTACK TEST
   For each surface, write the exploit attempt (spoofed payload, wrong target, replay, spam) and
   show the server rejecting it. A control without a test is a comment.

6. AUDIT BEFORE SHIP
   Grep every remote, every currency write, every `FireServer` sink; verify server-side checks;
   verify no secret or admin path is replicated. Re-run after any feature change.
```

## PATTERNS

### 1. The four-question gate (per remote)
```lua
-- Bad: client decides what and how much
Remotes.GrantItem.OnServerEvent:Connect(function(player, itemId, amount)
    Inventory:add(player, itemId, amount)
end)

-- Good: client asks, server decides
Remotes.RequestCraft.OnServerEvent:Connect(function(player, recipeId)
    if typeof(recipeId) ~= "string" then return end
    local recipe = Recipes[recipeId]           -- allowlist, server-owned table
    if not recipe then return end
    if not RateLimiter:allow(player, "craft", 4) then return end
    if not Inventory:hasAll(player, recipe.cost) then return end
    Inventory:consume(player, recipe.cost)     -- server computes the cost
    Inventory:add(player, recipe.result, 1)
end)
```

### 2. Validation checklist (put at the top of every handler)
- `typeof` / type check each argument; reject tables with unexpected keys.
- Reject `NaN`/`inf` numbers (`value ~= value` catches NaN; check `math.abs(value) < math.huge`).
- Enumerate allowed string IDs from a server table, never construct from client input.
- If an `Instance` is passed: `IsA` the expected class, verify `:IsDescendantOf(expectedContainer)`,
  and verify the player is close enough/allowed.
- Verify cooldown and resource cost from server state, not from the payload.
- Return/abort silently on failure; log a counter for repeated rejections.

### 3. Rate limiting that survives spam
Token bucket per `(userId, action)`; refill `rate` per second, capacity `burst`. On rejection, do not
error; increment a violation counter. Escalate after a threshold (kick is a last resort, and it must
not be triggerable by an innocent client bug).

### 4. Economy integrity
- Currency lives in the server profile only; the client never sends deltas.
- Purchases: `ProcessReceipt` with `PurchaseId` dedupe persisted with the grant; never acknowledge
  before the save (`roblox-scripting` pattern 5).
- GamePasses: `UserOwnsGamePassAsync` checked on the server, cached per session with an expiry.
- Trading: both sides confirmed server-side; validate ownership at commit time, not at offer time.

### 5. Data integrity
- Load failures must never be treated as a new profile (`roblox-scripting`).
- Session lock prevents two servers writing the same profile.
- Schema migrations are versioned and tested on copies of old data.
- Never trust a `Player` argument's claimed identity — derive identity from the event's player.

### 6. Secrets and admin surfaces
- API keys/tokens live in ServerScriptService/ServerStorage or server env; never in ReplicatedStorage,
  never in a LocalScript, never in a `StringValue` the client can read.
- Admin commands require a server-side allowlist by `UserId`; never a client-sent flag.
- Debug tools must be gated and removed/disabled before publish.
- `HttpService` keys are server-only; never echo them in errors or remote responses.

### 7. Pre-ship audit commands
```text
script_grep "FireServer"        → every client → server sink
script_grep "OnServerEvent"     → every handler; check validation
script_grep "OnServerInvoke"    → every RemoteFunction; check return shape
script_grep "leaderstats"       → any client write path
script_grep "IntValue"          → value-object tampering surface
script_grep "Kick"              → is it reachable from client input?
script_grep "HttpService"       → key handling
```
Then run one playtest per surface attempting the exploit.

## FAILURE MODES & MITIGATIONS

1. **Client-trusted amount** — `amount` from the payload. *DETECT:* grep shows arithmetic on a remote
   argument. *FIX:* server computes from an allowlisted ID.
2. **Missing target validation** — acting on any instance the client names. *DETECT:* remote accepts a
   Model without ancestry/distance checks. *FIX:* IsA + IsDescendantOf + distance + ownership.
3. **Remote spam** — no rate limit. *DETECT:* server frame spikes under load. *FIX:* token bucket +
   cooldown; log violations.
4. **NaN / inf injection** — numbers poison positions or balances. *DETECT:* NaN propagates into
   CFrame/currency. *FIX:* finiteness checks at the boundary.
5. **Duplication** — receipt/trade/item granted twice. *DETECT:* duplicate IDs in inventory. *FIX:*
   idempotency key + single durable grant.
6. **Admin surface exposed** — a client flag or a reachable remote. *DETECT:* grep for permission
   checks that read client data. *FIX:* server-side UserId allowlist; remove debug paths.
7. **Secret replicated** — key in ReplicatedStorage. *DETECT:* search replicated containers. *FIX:*
   move to server storage; rotate the key.
8. **Prompt exploit** — ProximityPrompt triggered from a distance or after the state changed.
   *DETECT:* no distance/state re-check in `Triggered`. *FIX:* re-validate everything server-side.

## QUANTITATIVE RULES

- 100% of remotes validated + rate limited; zero exceptions, including "internal" ones.
- Zero client-writable fields that affect currency, inventory, damage, or ownership.
- Every purchase path idempotent by `PurchaseId`; every trade validated at commit.
- Pre-ship audit re-run for any feature that adds a remote, reward, or write path.
- Attack tests: ≥1 per surface, with the rejection output recorded.
- Admin/debug surfaces: 0 reachable from the client at publish time.

## VERIFICATION GATE

- [ ] Trust boundary enumerated; every client → server sink listed.
- [ ] Each sink validates type/shape/range/ownership/rate against server state.
- [ ] Currency, inventory, damage, and rewards computed server-side only.
- [ ] Purchases deduped by PurchaseId; save-before-acknowledge verified.
- [ ] Data load failure cannot overwrite a real profile; session lock in place.
- [ ] No secret in replicated containers; admin paths server-gated.
- [ ] One reproducible attack test per surface, showing rejection, attached.
- [ ] Audit re-run after the final feature change.

## REFERENCES

- `roblox-scripting` — remote contracts, profiles, receipt handling
- `roblox-testing` — automated rejection tests and playtest harness
- `threat-modeling` — the general method this applies to Roblox
- `security-hardening-specialist` — non-Roblox application security
- `roblox-studio-mcp` — running the audit and playtests in Studio
