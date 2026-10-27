---
name: roblox-studio-mcp
description: >-
  Operates Roblox Studio through its built-in MCP server: pick the connected Studio instance, choose
  the Edit/Server/Client datamodel, read the tree and scripts before writing, apply batched edits,
  run Luau safely, playtest, and verify with console output and screenshots. Use for any Roblox task
  that touches a live Studio session — building, scripting, asset insertion, animation setup, or
  testing. Pure design questions route to the relevant roblox-* skill; non-Roblox engines to
  game-developer.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-game-director
---

# Roblox Studio MCP

Studio's MCP server is not a code sandbox with a nice API — it is a remote control for a place the
user has open. Every write is immediately real in their project, there is no atomic multi-edit
transaction across scripts, and version history is not an undo button for an agent's batch. The
protocol below exists so that speed never costs the user their work.

## WHEN TO USE

- Any task whose output must exist inside Roblox Studio: scripts, instances, terrain, UI, effects,
  assets, animation setup, playtests.
- Before any `execute_luau`, `multi_edit`, asset insertion, or playtest cycle.
- When a Studio session looks desynced, multiple instances are open, or a tool call fails.
- When another Roblox specialist needs to know how to verify its work.

## WHEN NOT TO USE

- Pure Luau reasoning with no Studio session (reviewing a snippet, explaining an API) — answer
  directly or use `roblox-scripting`.
- Asset creation outside Studio (Blender, image generation) — do that first, then return here.
- Deciding *what* to build — `roblox-game-production`.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
0. CONNECT & TARGET
   list_roblox_studios → exactly one? use it. More than one? pick by name and CONFIRM with the
   user before modifying anything. Never guess a studio_id.
   get_studio_state → know whether you are in Edit or a running playtest.

1. CHECKPOINT BEFORE BULK WORK
   Any change that touches more than a couple of scripts or deletes/reparents instances:
   ask the user to save the place / export a .rbxl checkpoint, or confirm version history exists.
   Say what you are about to change and how much. This is a permission event for destructive work.

2. READ BEFORE WRITE
   search_game_tree (path/type/keywords, max_depth 3-6) → script_search → script_grep →
   script_read / inspect_instance on the exact nodes. Never create a duplicate system because you
   did not look for the existing one.

3. WRITE IN THE RIGHT CONTEXT
   multi_edit + datamodel_type=Edit  → scripts (create or patch)
   execute_luau + Edit               → instances, GUI, terrain, effects, bulk property changes
   execute_luau + Server/Client      → only during a playtest, to exercise runtime logic
   Edit is rejected while playing. Stop the playtest first; do not loop on the error.

4. BOUND THE WORK
   execute_luau runs on Studio's main thread. It freezes the editor until it yields.
   - Build in chunks; call task.wait() once per chunk (not per item).
   - Parent each small subtree once; a single .Parent write costs the whole subtree size.
   - Never ship a loop without a yield. Never `while true do` without task.wait().
   - Bulk generation: use async jobs (generate_procedural_model async=true) and continue with
     independent work; wait only when the next step depends on it.

5. PLAYTEST LIKE A PLAYER
   start_stop_play(is_start=true) → get_console_output → exercise via user_keyboard_input /
   user_mouse_input (real input path) or character_navigation (movement shortcut, bypasses input) →
   execute_luau in Server and Client to assert state → screen_capture for visual checks.
   Always start_stop_play(false) when done; confirm the state returned to Edit.

6. VERIFY, THEN REPORT
   Console clean (no errors, no new warnings) + the behavior observed + the artifact (output,
   screenshot path, instance path). A screenshot proves pixels, not logic. Report what was changed
   by path, and what was not verified.
```

## TOOL MAP

| Need | Tool | Context |
|---|---|---|
| Find Studio instances | `list_roblox_studios` | — |
| Current mode / available datamodels | `get_studio_state` | — |
| Explore hierarchy | `search_game_tree` (path, instance_type, keywords, max_depth ≤10) | Edit/Server/Client |
| Read properties/attributes | `inspect_instance` | Edit/Server/Client |
| Find scripts by name | `script_search` (≤10 results) | Edit |
| Search code | `script_grep` (≤50 matches) | Edit/Server |
| Read a script / range | `script_read` | Edit |
| Create or patch scripts | `multi_edit` (atomic per script) | Edit only |
| Run Luau | `execute_luau` | Edit/Server/Client |
| Playtest | `start_stop_play` | — |
| Output/warnings | `get_console_output` | — |
| Visual check | `screen_capture` (optional camera position/look-at) | — |
| Simulate input | `user_keyboard_input`, `user_mouse_input` | during play |
| Move test character | `character_navigation` | during play |
| Creator Store / inventory | `search_asset`, `insert_asset` | Edit |
| Generate art | `generate_mesh`, `generate_material`, `generate_procedural_model` (+ `wait_job_finished`) | Edit |
| Images | `store_image`, `upload_image` | Edit |
| Docs | `http_get` | — |

Tool names and availability vary by Studio version; if something is missing, use what
`get_studio_state` and the client expose rather than inventing a call.

## PATTERNS

### 1. Session preamble (every Roblox task)
```text
[STUDIO]
instance: {name} (studio_id={id})
state: {Edit | playing}
target: {place name} — confirmed with user: {yes/no}
checkpoint: {saved by user | version history | not needed (read-only)}
scope: {what will change; what will not}
```

### 2. Script patch loop
```text
script_read path → plan the diff → multi_edit with exact old_string anchors →
script_read back → get_console_output → run the behavior (playtest or execute_luau) →
report the new content hash/path
```
`multi_edit` is atomic **per script**, not across scripts. Two scripts that must change together can
end up inconsistent if the second fails; keep a paired change small and verify both.

### 3. Bulk instance creation
```lua
-- chunked, yields once per chunk, parents once per chunk
for chunkIndex = 1, #chunks do
    local container = Instance.new("Folder")
    for _, spec in ipairs(chunks[chunkIndex]) do
        local part = Instance.new("Part")
        part.Name = spec.name
        part.Size = spec.size
        part.CFrame = spec.cframe
        part.Anchored = true
        part.Parent = container
    end
    container.Parent = workspace.Level
    task.wait()
end
```
Never build 10k instances then parent them in one write, and never omit the yield.

### 4. Server/client assertion during play
```lua
-- execute_luau, datamodel_type = "Server"
local Players = game:GetService("Players")
local player = Players:GetPlayers()[1]
return { players = #Players:GetPlayers(), hasProfile = player:FindFirstChild("Profile") ~= nil }
```
Return small, structured values. Do not dump whole instances into the response.

### 5. Visual verification that means something
Capture before and after from the **same camera position**. State what the screenshot is supposed
to show and what it cannot show (logic, timing, network). Pair it with a console/state assertion.

### 6. Recovery from a desynced session
1. `get_studio_state`. 2. If the mode is wrong, `start_stop_play(false)` **once**. 3. If the tool
still fails, stop calling tools, tell the user to check the MCP connection in Studio, and wait.
Repeating a failed state transition is how an agent wedges the session.

## FAILURE MODES & MITIGATIONS

1. **Wrong Studio instance** — edits land in another place. *DETECT:* instance name differs from the
   user's project. *FIX:* always `list_roblox_studios` + confirm; never infer.
2. **Edit during playtest** — `multi_edit`/Edit calls rejected. *DETECT:* "datamodel_type not
   available". *FIX:* stop play, re-check state, retry once.
3. **Frozen Studio** — one huge unyielding `execute_luau`. *DETECT:* call times out, connection drops.
   *FIX:* chunk + `task.wait()`; reduce subtree parent writes.
4. **Silent data loss** — `:ClearAllChildren()` or a broad delete on a container. *DETECT:* missing
   instances the user did not ask to remove. *FIX:* checkpoint first, scope deletes to named paths,
   ask before destructive operations.
5. **Phantom success** — "done" while the console has errors. *DETECT:* `get_console_output` shows
   red. *FIX:* never report done with console errors; fix or report blocked.
6. **State loop** — repeated start/stop or mode calls. *DETECT:* tool error repeats. *FIX:* stop after
   one retry; hand control back with the exact error.
7. **Duplicate systems** — a second RemoteEvent/DataStore wrapper because nobody searched. *DETECT:*
   two modules with the same responsibility. *FIX:* grep first; extend, don't duplicate.
8. **Unreviewed generated code** — mesh/procedural output accepted blindly. *DETECT:* no screenshot or
   property check. *FIX:* inspect + capture; generation is a draft, not a deliverable.

## QUANTITATIVE RULES

- One Studio target per task; confirm it once, reuse the `studio_id`.
- `execute_luau` chunks: ~1000 instances or one region per call, one `task.wait()` per chunk.
- `search_game_tree` depth ≤6 by default; raise only with a reason.
- Playtest cycle: one behavior per cycle; stop play before the next edit.
- No task is done with console errors. Visual claims need a same-camera before/after.
- Generated assets: verify ≥1 property and ≥1 screenshot before accepting.

## VERIFICATION GATE

- [ ] Instance confirmed and stated (`studio_id`, place name).
- [ ] Checkpoint/permission obtained for bulk or destructive changes.
- [ ] Tree/scripts read before writing; no duplicated system.
- [ ] Edits applied in the correct datamodel; playtest state restored to Edit at the end.
- [ ] `get_console_output` clean; behavior exercised (not just compiled).
- [ ] Visual change captured from a fixed camera; logic asserted separately.
- [ ] Report lists changed paths, evidence, and anything unverified.

## REFERENCES

- `roblox-game-production` — what to build and in what order
- `roblox-scripting` — Luau systems, remotes, data, economy
- `roblox-world-building` / `roblox-ui-ux` / `roblox-animation` / `roblox-vfx` / `roblox-assets`
- `roblox-testing` — playtest automation and test suites
- `roblox-security` — what to check before shipping
- Roblox docs: <https://create.roblox.com/docs/studio/mcp>
