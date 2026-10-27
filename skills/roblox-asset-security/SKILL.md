---
name: roblox-asset-security
description: 'Audits third-party Roblox marketplace and Creator Store assets (models, packages, meshes,
  plugins) inserted via Studio MCP for supply-chain risks: hidden backdoors, obfuscated bytecode, malicious
  require(assetId) calls, and fake core scripts. Use when searching, inserting, or reviewing external
  assets before parenting them into the DataModel. Runtime exploit defense routes to roblox-security;
  general dependency auditing to dependency-supply-chain-guardian; visual tuning to roblox-assets.'
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-24'
  owned-by-agent: roblox-security-engineer
---


# Roblox Asset Security

Free and marketplace assets in Roblox are a major vector for supply chain attacks. Malicious creators
hide backdoors inside models, meshes, animations, and plugins that execute obfuscated bytecode, require
external asset IDs, abuse HttpService for credential harvesting, or infect the place with persistent
telemetry. This skill governs the inspection, quarantine, and sanitization of any external asset before
it becomes part of the game.

## WHEN TO USE

- After searching or inserting any asset via Studio MCP (`search_asset`, `insert_asset`).
- Reviewing third-party toolbox models, meshes, audio, or packages before parenting into the active DataModel.
- Auditing existing workspace models for hidden scripts, fake infection modules, or backdoor loaders.
- Evaluating plugins or developer tools installed from the Creator Store.
- Cross-owner inventory checks when importing assets from external groups or users.

## WHEN NOT TO USE

- In-game exploit defense, remote validation, and player data security — `roblox-security`.
- Traditional software dependency and npm/crate/wally security — `dependency-supply-chain-guardian`.
- Visual styling, material assignment, and mesh optimization — `roblox-assets`.
- General threat modeling for system architecture — `threat-modeling`.

## DECISION TREE

```text
1. QUARANTINE ON INSERT
   Never parent an unvetted asset directly to game.Workspace or ServerScriptService.
   Parent initially to a quarantine container (e.g. ServerStorage.Quarantine or an unparented tree).

2. SCRIPT RECONNAISSANCE
   Scan all descendants for BaseScript (Script, LocalScript, ModuleScript).
   If the asset is advertised as a static model, prop, or mesh:
   - Any script inside it is suspicious by default.
   - Remove or review all scripts before approval.

3. PATTERN SCANNING FOR BACKDOORS
   Inspect script sources for high-risk signatures:
   - `require(number)` — external asset require (loads unreviewed code from assetId).
   - `getfenv()`, `setfenv()`, `loadstring()` — environment tampering and runtime execution.
   - `string.reverse`, `string.gsub` obfuscation, `\x..` hex-escapes, or byte-array unpackers.
   - `HttpService:PostAsync` or `GetAsync` to untrusted external endpoints (telemetry/exfiltration).
   - Fake "Vaccine", "Anti-Lag", or "Fixer" script names (common trojan disguise).
   - Deeply nested or hidden children in welds, parts, or camera instances.

4. MESH & VISUAL VALIDATION
   Verify MeshPart textures, collision properties, and bounding boxes.
   Ensure asset does not carry malicious ProximityPrompts, ClickDetectors, or TouchTransmitters.

5. PROMOTION OR PURGE
   If clean: remove unnecessary metadata, strip unneeded scripts, and parent to the destination container.
   If malicious or suspect: discard the instance immediately and log the asset ID and creator.
```

## AUDIT PROTOCOL & DETECTION PATTERNS

### High-Risk Signatures in Luau
```text
Signature 1: require(assetId)
Pattern: require\s*\(\s*\d{6,}\s*\)
Risk: Critical. Loads external module at runtime that can be swapped to malicious code at any time.

Signature 2: Obfuscated Bytecode
Pattern: \\(\d{1,3}|x[0-9a-fA-F]{2})
Risk: Critical. String encryption hiding backdoors or webhooks.

Signature 3: Environment Manipulation
Pattern: getfenv\s*\(|setfenv\s*\(|_G\[|shared\[
Risk: High. Circumvents static analysis and Luau sandboxing.

Signature 4: Untrusted HTTP Exfiltration
Pattern: HttpService\s*:\s*(GetAsync|PostAsync|RequestAsync)
Risk: High. Leaks server game IDs, place keys, or player information.
```

### Studio MCP Quarantine Flow
When using `insert_asset`:
1. Insert under `game.ServerStorage.AssetQuarantine`.
2. Inspect with `inspect_instance` or run `script_grep` across the quarantine container.
3. If scripts exist, read with `script_read` or analyze via `execute_luau`.
4. Sanitize by deleting unauthorized scripts.
5. Move verified model to `game.Workspace` or intended target.

## QUANTITATIVE RULES

- 0 unvetted assets placed directly into replicated or active gameplay containers.
- 0 `require(assetId)` calls tolerated in marketplace models (all code must be local modules).
- 0 obfuscated or hex-encoded strings allowed in accepted scripts.
- 100% of inserted models scanned for unexpected descendant scripts before release.
- Cross-owner inserts require explicit verification against the current place universe owner.

## VERIFICATION GATE

- [ ] Asset inserted into isolated quarantine location prior to inspection.
- [ ] Descendant inventory completed; all scripts, animations, and configurations identified.
- [ ] No `require(assetId)` or external module loading present.
- [ ] No `getfenv`, `setfenv`, or obfuscated string packing found.
- [ ] HttpService access verified and confirmed strictly necessary or absent.
- [ ] Extraneous or disguised scripts (e.g. fake infection fixes) deleted.
- [ ] Cleaned asset verified functional in edit mode before committing to place tree.

## REFERENCES

- `roblox-security` — runtime trust boundaries and exploit defense
- `roblox-assets` — asset production, meshes, textures, and Creator Store sourcing
- `roblox-studio-mcp` — insert_asset and DataModel inspection workflows
- `dependency-supply-chain-guardian` — general package supply-chain security
