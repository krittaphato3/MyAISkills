---
name: roblox-economy-retention
description: "Designs safe Roblox monetization, idempotent ProcessReceipt purchases, PolicyService checks, and FTUE retention loops. Use when adding GamePasses, DevProducts, shops, or currency."
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: roblox-scripter
---

# Roblox Economy & Retention

Protects players from lost Robux purchases and protects your economy from inflation, duplication bugs, or regional compliance bans.

## WHEN TO USE

- Implementing `MarketplaceService.ProcessReceipt` for Developer Products.
- Adding GamePass checks, pet/crate RNG systems, daily rewards, or shops.
- Designing the first 60 seconds (FTUE) and currency sinks/faucets.

## WHEN NOT TO USE

- Low-level DataStore locking or remote rate limits alone — `roblox-scripting` / `roblox-security`.

## DECISION TREE

```text
1. DEVELOPER PRODUCTS (idempotent ProcessReceipt — ONE handler in workspace)
   - Never grant reward until profile is loaded AND PurchaseId is NOT in `profile.ReceiptHistory`.
   - Grant reward + record PurchaseId in RAM + save (`UpdateAsync`) -> return `PurchaseGranted` ONLY after commit;
     otherwise return `NotProcessedYet` so Roblox safely retries.

2. REGIONAL & PLATFORM COMPLIANCE (`PolicyService:GetPolicyInfoForPlayerAsync`)
   - Check `ArePaidRandomItemsRestricted` before showing Robux lootboxes/eggs; swap to direct-buy or disable if true.
   - Check `AllowedExternalLinkReferences` before displaying social/Discord codes.

3. GAMEPASS CACHING & BALANCING
   - Cache `UserOwnsGamePassAsync` per session in server memory; update live on `PromptGamePassPurchaseFinished`.
   - Every currency faucet (farming/rewards) must pair with a sink (upgrades, consumables, rebirths) to prevent inflation.
```

## FAILURE MODES & MITIGATIONS

1. **Duplicate `ProcessReceipt` Callbacks** — DETECT: two scripts set `MarketplaceService.ProcessReceipt`, overwriting one another. FIX: single central `MonetizationService.server.luau` registry.
2. **Uncommitted Robux Grant** — DETECT: returning `PurchaseGranted` before DataStore save confirms. FIX: save or persist `PurchaseId` ledger before returning `PurchaseGranted`.
3. **Inflation Spiral** — DETECT: players hit max currency in 10 minutes with nothing left to buy. FIX: exponential sinks + prestige/rebirth resets + time-gated mastery.

## VERIFICATION GATE

- [ ] Single `ProcessReceipt` callback verified across entire codebase via `script_grep`.
- [ ] Duplicate `PurchaseId` replay test proves reward is granted exactly once.
- [ ] `PolicyService` guard wraps every paid randomized reward path.

## REFERENCES

- `roblox-scripting` & `roblox-security` — server authority and audit gates
- `roblox-testing` — TestEZ receipt replay and economy invariant tests
