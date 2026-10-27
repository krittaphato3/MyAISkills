---
name: roblox-project-indexer
description: 'Builds and maintains an offline project architecture index (roblox_project_index.json/.md)
  in the active game workspace: scripts, remotes (RemoteEvents/Functions/Bindables), GUI surfaces, value
  configs, and CollectionService tags, refreshed via Studio MCP. Replaces slow, token-heavy game-tree
  sweeps with an instant local map. Use when opening or switching Roblox projects, mapping architecture,
  or looking up remotes and scripts.'
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-26'
  owned-by-agent: roblox-scripter
---


# Roblox Project Indexer

Large Roblox experiences contain hundreds of scripts, dozens of networking remotes, complex GUI hierarchies, and tagged entities scattered across `ServerScriptService`, `ReplicatedStorage`, `StarterPlayer`, `StarterGui`, `Workspace`, and `ServerStorage`. Inquiring about instances using Studio MCP tools (`search_game_tree`, `script_search`, or `script_grep`) over and over consumes massive model token budgets, incurs repeated network roundtrips, risks freezing the Studio main thread, and is constrained by tool query caps (such as 10 or 50 matches).

The **Roblox Project Indexer** solves this by extracting a comprehensive snapshot of the entire place architecture once via an optimized, chunked Luau script executed through Studio MCP `execute_luau`. It writes a local machine-readable JSON index (`roblox_project_index.json`) and a structured Markdown index (`roblox_project_index.md`) directly into the active game's workspace folder.

---

## PER-PROJECT STORAGE RULE (CRITICAL)

The index **MUST** always be saved directly in the active project directory:
- `<project_root>/roblox_project_index.json`
- `<project_root>/roblox_project_index.md`

**NEVER** write game indexes to the global configuration directory `C:\Users\Oz\.zcode`.

### Why Per-Project Storage is Mandatory
1. **Multi-Game Organization**: Developers and teams manage multiple Roblox places (e.g., lobby, main gameplay place, dungeon sub-places, seasonal events). Storing indexes per-project keeps architecture metadata cleanly separated with zero cross-game contamination.
2. **Version Control Integration**: Storing the index within the project repo allows teams to track structural changes, remote additions, and script growth across Git commits.
3. **Instant Tool Access**: Subagents working in the game's root directory can immediately read or grep the local files (`roblox_project_index.md` or `.json`) without performing global file hops or Studio queries.

---

## WHAT IT INDEXES

1. **Scripts**:
   - `Script`, `LocalScript`, `ModuleScript`
   - Full DataModel path (`game.ServerScriptService.GameManager`)
   - Parent path and architectural category (`Server`, `Shared`, `Client`, `ClientUI`, `Workspace`)
   - Line counts and `RunContext` (`LegacyServer`, `Server`, `Client`, `Plugin`, `Module`)
2. **Networking & Remotes**:
   - `RemoteEvent`, `RemoteFunction`, `BindableEvent`, `BindableFunction`, `UnreliableRemoteEvent`
   - Full DataModel path, parent container, and communication classification
3. **GUI Surfaces**:
   - `ScreenGui`, `BillboardGui`, `SurfaceGui`
   - `Enabled` state, `ResetOnSpawn` flag, and nested `ViewportFrame` counts
4. **CollectionService Tags**:
   - All active tags registered via `CollectionService:GetAllTags()`
   - Instance counts per tag and sample instance paths
5. **Place Summary**:
   - Place name, PlaceId, GameId, total instances scanned, and timestamp

---

## WHEN TO USE

- Opening or switching between Roblox game projects to establish situational awareness.
- Mapping an existing or unfamiliar place architecture before writing new features.
- Looking up script locations, remote event names, GUI surfaces, or tags without Studio MCP calls.
- Verifying whether a remote or module already exists before creating duplicates.
- Auditing place complexity: total script count, line counts, remote inventories, and GUI surfaces.
- Refreshing the local project map after major structural additions, file moves, or Rojo syncs.

---

## WHEN NOT TO USE

- Reading full script source code or applying code edits — use `roblox-studio-mcp` (`script_read`, `multi_edit`).
- Implementing runtime server logic, remote handling, or DataStores — use `roblox-scripting`.
- Configuring filesystem-to-Studio project sync or Rojo manifests — use `roblox-toolchain`.
- Designing GUI styling, 3D ViewportFrame hero showcases, or HUD aesthetics — use `roblox-ui-ux`.
- Security exploit audits and remote parameter vulnerability reviews — use `roblox-security`.

---

## DECISION TREE

```text
1. NEED TO LOCATE OR AUDIT A SCRIPT, REMOTE, GUI, OR TAG?
   ├─ Does <project_root>/roblox_project_index.md or .json exist locally?
   │  ├─ Yes → Grep / Read local index directly. Zero Studio MCP calls needed.
   │  └─ No / Stale → Proceed to Step 2.
   │
2. GENERATE OR REFRESH PROJECT INDEX
   ├─ Verify Studio connection via list_roblox_studios and get_studio_state (datamodel_type: "Edit").
   ├─ Run index generator: execute_luau with references/index_generator.luau.
   ├─ Parse returned JSON payload.
   └─ Save roblox_project_index.json and roblox_project_index.md into the active project directory.
   │
3. EXECUTE TARGETED ACTIONS
   └─ Use exact full paths from the local index for targeted script_read, multi_edit, or asset inspection.
```

---

## EXECUTION WORKFLOW

### Step 1: Execute the Generator via Studio MCP

Execute `references/index_generator.luau` in Roblox Studio using `execute_luau` in Edit mode:

```json
{
  "studio_id": "<studio_id>",
  "datamodel_type": "Edit",
  "code": "<content of references/index_generator.luau>"
}
```

The generator yields via `task.wait()` every 200 items, guaranteeing that Studio never hangs and MCP connections remain stable regardless of place size.

### Step 2: Parse and Save JSON Index

Write the raw JSON response directly to `<project_root>/roblox_project_index.json`.

Schema overview:
```json
{
  "placeInfo": {
    "name": "My Experience",
    "placeId": 0,
    "gameId": 0,
    "totalInstancesScanned": 1420,
    "scannedAt": "2026-10-26T12:00:00Z"
  },
  "summary": {
    "totalScripts": 45,
    "scriptsByClass": { "Script": 12, "ModuleScript": 25, "LocalScript": 8 },
    "totalRemotes": 18,
    "remotesByClass": { "RemoteEvent": 14, "RemoteFunction": 4 },
    "totalGuis": 6,
    "guisByClass": { "ScreenGui": 6 },
    "totalTags": 5
  },
  "scripts": [ ... ],
  "networking": [ ... ],
  "guis": [ ... ],
  "tags": [ ... ]
}
```

### Step 3: Write Markdown Index

Generate `<project_root>/roblox_project_index.md` formatted for rapid agent retrieval:

```markdown
# Roblox Project Architecture Index

**Place**: My Experience (PlaceId: 0)  
**Scanned**: 2026-10-26T12:00:00Z | 1,420 total instances  
**Summary**: 45 Scripts | 18 Remotes | 6 GUIs | 5 Tags  

## 1. Networking & Remotes
| Remote Name | Class | Full Path |
|---|---|---|
| RequestAttack | RemoteEvent | game.ReplicatedStorage.Remotes.RequestAttack |
| FetchInventory | RemoteFunction | game.ReplicatedStorage.Remotes.FetchInventory |

## 2. Scripts Inventory
### Server (`ServerScriptService`)
- `game.ServerScriptService.Main` (Script, 120 lines)
- `game.ServerScriptService.Services.CombatService` (ModuleScript, 340 lines)

### Shared (`ReplicatedStorage`)
- `game.ReplicatedStorage.Common.Config` (ModuleScript, 65 lines)

### Client (`StarterPlayer` / `StarterGui`)
- `game.StarterPlayer.StarterPlayerScripts.CombatController` (LocalScript, 210 lines)

## 3. GUI Surfaces
| GUI Name | Class | Enabled | ResetOnSpawn | ViewportFrames | Path |
|---|---|---|---|---|---|
| HUD | ScreenGui | true | false | 2 | game.StarterGui.HUD |
| ShopMenu | ScreenGui | false | false | 5 | game.StarterGui.ShopMenu |

## 4. CollectionService Tags
- `DamageZone` (12 instances)
- `Interactable` (8 instances)
- `MobSpawn` (4 instances)
```

---

## MULTI-PROJECT WORKFLOW BEST PRACTICES

1. **Independent Game Workspaces**: When switching between a lobby place and a gameplay place, keep separate workspace directories. Each contains its own `roblox_project_index.json` and `roblox_project_index.md`.
2. **Never Query Studio Blindly**: Before running `search_game_tree` or `script_grep`, check if `roblox_project_index.md` already contains the target instance path.
3. **Incremental Refresh**: Re-run the index generator whenever you create new network remotes or refactor folder hierarchies.

---

## VERIFICATION GATE

Before relying on or declaring index generation complete:
- [ ] Generator executed with `datamodel_type: "Edit"` and finished cleanly without errors.
- [ ] Both `<project_root>/roblox_project_index.json` and `<project_root>/roblox_project_index.md` exist directly in the active project root directory.
- [ ] Neither index file was written to global `C:\Users\Oz\.zcode` or home directory.
- [ ] Scripts, networking remotes, GUI surfaces, and `CollectionService` tags are comprehensively cataloged.
- [ ] Full DataModel paths begin with `game.` and accurately represent instance hierarchy.
- [ ] Subsequent code exploration tools consult the local index instead of executing heavy Studio sweeps.
