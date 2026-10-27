---
name: roblox-assets
description: >-
  Sources and optimizes Roblox assets: generated meshes, materials and procedural models, Creator
  Store search and licensing, texture and triangle budgets, audio import rules, avatar and
  HumanoidDescription setup, and reuse/instancing strategy. Use when a build needs a model, mesh,
  texture, material, sound, or avatar asset, or when assets are bloating load time. Character
  animation routes to roblox-animation; environment layout to roblox-world-building.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-asset-artist
---

# Roblox Assets

Assets are where a Roblox game quietly becomes slow. One 20k-triangle mesh is fine; forty of them in
one view, each with a unique 2k texture, is a different game on a phone. The discipline is: search
before generating, generate before importing, reuse before varying, and never ship an asset you did
not look at.

## WHEN TO USE

- A build needs a prop, vehicle, character, weapon, environmental kit, or decoration.
- Searching the Creator Store or the creator's inventory for an existing asset.
- Generating meshes, materials, or procedural models.
- Textures, decals, images, sounds, or avatar appearance.
- Import/upload rules: formats, sizes, licensing, permissions.
- Load time, memory, or draw-call problems traced to assets.

## WHEN NOT TO USE

- Placing assets into a level and lighting the scene — `roblox-world-building`.
- Rigging and animating a character — `roblox-animation`.
- Particle textures and effect tuning — `roblox-vfx`.
- Non-Roblox asset pipelines with no Studio integration — handle outside, return here to import.

## DECISION TREE

```text
1. DOES IT ALREADY EXIST?
   search_asset (Creator Store + inventory) → inspect → insert_asset.
   Check licensing/permissions before using: Open Use vs Restricted, and group/experience ownership.
   Never assume a marketplace asset is free to reuse.

2. CAN IT BE GENERATED?
   Procedural model (primitives, tunable attributes) → best for blocky props, vehicles, creatures.
   generate_mesh → organic or detailed single objects; textured.
   generate_material → tileable PBR surface for a MaterialVariant.
   Generate with a specific prompt (scale, style, parts) and verify the result visually and by
   property before accepting.

3. WHAT IS THE BUDGET?
   Individual mesh ≤20,000 triangles (import ceiling, not a target).
   Avatar bodies: 4,000 head / 1,750 torso / 1,248 per limb; ≤4 bone influences; no root weighting.
   Textures ≤4096×4096; start at 256 for 5×5 studs, 512 for 10×10, 1024 for 20×20.
   Audio: MP3/OGG/WAV/FLAC, <20 MB, <7 min, ≤48 kHz.
   Aim well below ceilings; the scene budget is the real constraint.

4. IMPORT OR BUILD?
   Studio-native primitives → cheaper, instanced, editable.
   Imported mesh → unique geometry, breaks instancing; use for hero assets only.
   MaterialVariant for reusable surfaces; SurfaceAppearance for a specific mesh's UVs.

5. WHERE DOES IT LIVE?
   ReplicatedStorage.Assets for shared props (streaming-safe).
   ServerStorage for server-only templates.
   Workspace only for placed instances; do not store the source kit in Workspace.

6. VERIFY
   Insert → inspect properties/scale → screen_capture from a fixed camera → check triangle/texture
   cost → confirm it reads at low graphics quality → confirm licensing.
```

## PATTERNS

### 1. Search-first asset workflow
```text
search_asset(query, scope=creator_store|inventory|group)
→ review name/creator/license → insert_asset(assetId, assetType, parentPath, assetName)
→ inspect_instance (size, orientation, Anchored, collision) → normalize scale → capture
```
Normalize everything to game scale on insert (1 stud ≈ 0.28 m; Humanoid ≈ 5 studs). Imported assets
rarely arrive at the right size.

### 2. Generation prompts that produce usable assets
```text
Good: "a low-poly wooden market stall, 3 meters wide, sloped striped awning, two crates,
       chunky stylized shapes, no text"
Weak: "a shop"
Include: style, scale, key parts, what to omit. Expose tunables as attributes when the model should
be editable later (procedural model).
```

### 3. Budget table
| Asset | Ceiling | Practical target |
|---|---|---|
| Single mesh | 20,000 tris | 500–5,000 for props |
| Avatar head | 4,000 tris | near the cap only for hero bodies |
| Avatar torso | 1,750 tris | — |
| Avatar limb (each) | 1,248 tris | — |
| Texture | 4096×4096 | 256 / 512 / 1024 by stud size |
| Audio file | <20 MB, <7 min | short, loopable, mono where possible |
| Unique materials per prop set | — | reuse a small palette |

### 4. Materials and textures
- `MaterialVariant` for repeated surfaces (brick, metal, fabric): one asset, many parts.
- `SurfaceAppearance` for a specific mesh's authored look (color/normal/roughness/metalness maps).
- One texture atlas per kit beats one texture per prop.
- Check tiling/scale on large surfaces; stretched textures are the most visible cheap mistake.

### 5. Audio import
- Rights: only audio you are legally allowed to use; platform rules apply.
- Formats MP3/OGG/WAV/FLAC; <20 MB; <7 min; ≤48 kHz; mono or stereo 2.0/3.0/5.1.
- Upload quotas vary by verification status — check the current limit before a bulk import.
- After import: set `SoundId`, `Looped`, `Volume`, roll-off for 3D use (`roblox-vfx`).

### 6. Avatar appearance
```lua
local description = Players:GetHumanoidDescriptionFromUserId(userId)
description.Shirt = shirtId
description.Pants = pantsId
description.BodyTypeScale = 0.1
humanoid:ApplyDescription(description)
```
Apply after the character exists; clear/override old accessories deliberately; test R15 and R6 if both
are supported. Custom bodies must follow Roblox's rig/geometry/texture requirements.

### 7. Reuse and optimization
- Kit-bash: a small set of modular pieces reused with different materials/colors.
- Identical mesh + material can instance; unique combinations cannot.
- Turn off `CastShadow` on decorative assets; `RenderFidelity` Automatic unless measured.
- Strip invisible faces/parts from imported models; collapse tiny parts.
- Keep source kits out of Workspace so streaming does not carry them.

## FAILURE MODES & MITIGATIONS

1. **Licensing violation** — Restricted asset used without permission. *DETECT:* asset privacy state is
   Restricted or ownership is another group. *FIX:* replace or obtain permission; record the license.
2. **Import at wrong scale** — giant/tiny props. *DETECT:* Humanoid/door reference mismatch. *FIX:*
   normalize on insert; keep a 1-stud reference block in the kit.
3. **Triangle/texture sprawl** — unique high-poly assets everywhere. *DETECT:* memory and draw calls
   climb. *FIX:* reuse kits, atlas textures, lower poly for background props.
4. **Unverified generation** — mesh looks wrong, floats, or has no collision. *DETECT:* no capture or
   property check. *FIX:* inspect + capture + playtest before accepting.
5. **Audio rejection** — wrong format/size/rights. *DETECT:* upload fails or is moderated. *FIX:*
   convert, trim, confirm rights before upload.
6. **Avatar apply failure** — description applied before the Humanoid exists. *DETECT:* default avatar
   or partial outfit. *FIX:* wait for character/Humanoid, then apply; verify accessories.
7. **Source kit in Workspace** — every player streams the entire asset library. *DETECT:* long join
   times. *FIX:* move to ReplicatedStorage/ServerStorage.

## QUANTITATIVE RULES

- 1 mesh ≤20,000 triangles; props target 500–5,000; avatars per the platform split.
- Textures: 256 (≈5×5 studs), 512 (≈10×10), 1024 (≈20×20); max 4096.
- Audio: <20 MB, <7 min, ≤48 kHz, rights confirmed.
- One texture atlas per kit; ≤3 unique materials per prop family where possible.
- Every imported/generated asset: inspect + capture + scale check before acceptance.
- No Restricted asset without documented permission.

## VERIFICATION GATE

- [ ] Existing assets searched before generating or importing.
- [ ] Licensing/permissions confirmed and recorded.
- [ ] Scale normalized against a Humanoid/door reference.
- [ ] Triangle/texture/audio budgets checked, not just under the ceiling.
- [ ] Generated assets inspected, captured, and accepted or regenerated.
- [ ] Asset placed in the correct container; source kit not in Workspace.
- [ ] Visual check at low graphics quality; no stretched textures or floating geometry.

## REFERENCES

- `roblox-world-building` — placement, lighting, streaming-friendly kits
- `roblox-animation` — rigging and clips for custom characters
- `roblox-vfx` — audio playback and particle textures
- `roblox-security` — asset permissions and secret handling
- `roblox-studio-mcp` — generation tools, insertion, capture
- Roblox docs: modeling specifications, texture specifications, Creator Store, audio assets
