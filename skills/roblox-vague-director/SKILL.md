---
name: roblox-vague-director
description: "Expands 1-sentence vague Roblox game ideas into playable non-slop vertical slices with genre formulas and ProfileService/spr patterns. Use when prompting vaguely for a Roblox game."
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: roblox-game-director
---

# Roblox Vague Director

Turns a short or vague idea (*"cozy fishing with pets"*, *"samurai parry arena"*) into a front-page quality vertical slice without interrogating the user or letting a fast model collapse into monolithic slop.

## WHEN TO USE

- User gives a 1-sentence or underspecified Roblox game prompt.
- Fast-model execution needs concrete genre defaults, module boundaries, and sharded briefs.

## WHEN NOT TO USE

- User already provides a complete GDD or narrow single-script bugfix — route to `roblox-scripting` or `roblox-game-production`.
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. MATCH GENRE FORMULA (auto-select defaults, do not ask >1 blocking question)
   - Simulator / Pet  -> Action -> Capacity/Currency -> Egg Hatch (luck boost) -> Zone Gate
   - Combat / Arena   -> Light/Heavy + Parry/Dash -> Hitpause + Screen Shake -> KOs -> Weapon Unlock
   - Obby / Climb     -> Checkpoint Stream -> Gravity/Speed Mutators -> Stage Timer -> Trails/Cosmetics
   - Tycoon / Base    -> Dropper -> Collector -> Upgrader -> Button Purchase -> Rebirth Multiplier
   - Dungeon / Loot   -> Room Wave -> Chest/Drop Rarity -> Loadout Extraction -> Upgrade Forge

2. EMIT 1-PAGE SLICE SPEC (1 paragraph vision + 5 constraints)
   - Core Loop sentence + Lighting (`Future` + `Atmosphere` + 60-30-10 palette).
   - Folder skeleton: `ReplicatedStorage/Shared` (strict `--!strict` types + remotes),
     `ServerScriptService/Services` (authoritative), `StarterPlayerScripts/Controllers` (UI/FX).
   - Persistence baseline: ProfileService/ProfileStore session-locked profile (`UpdateAsync` + `BindToClose`).
   - UI baseline: `UICorner`, gradient `UIStroke`, 9-slice drop shadow, `spr`/TweenService spring bounce.

3. SHARD SPECIALISTS (1 role per turn/subagent, <=150 LOC per Luau module)
   World (`roblox-builder`) -> Data+Remotes (`roblox-scripter`) -> UI (`roblox-ui-designer`)
   -> Feel/Audio (`roblox-animator` + `roblox-vfx-artist`) -> QA Playtest (`roblox-qa-engineer`).
```

## FAILURE MODES & MITIGATIONS

1. **Monolithic God Script** — DETECT: `GameManager.server.lua` >250 lines doing UI+Data+Combat. FIX: split into Services/Controllers with typed module boundaries.
2. **Endless Clarification Loop** — DETECT: asking 5+ design questions on a casual prompt. FIX: pick the strongest genre formula defaults and let the user steer after playable M0.
3. **Grey Plastic / Flat UI Slop** — DETECT: unstyled Parts or sharp flat TextButtons. FIX: enforce `roblox-world-building` PBR + `roblox-ui-ux` embossed strokes before M0.

## VERIFICATION GATE

- [ ] Genre formula, core loop, and folder layout declared before code generation.
- [ ] Every generated Luau module starts with `--!strict` and passes `selene` / Studio console clean.
- [ ] Playtest confirms core verb -> reward -> persistence survives rejoin.

## REFERENCES

- `roblox-game-production` — milestone gate definitions (M0–M4)
- `roblox-scripting` & `roblox-lua-developer` — server authority and strict patterns
- `roblox-ui-ux`, `roblox-world-building`, `roblox-vfx` — anti-slop visual & kinetic baselines
