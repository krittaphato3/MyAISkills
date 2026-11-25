---
name: roblox-3d-pipeline
description: "Orchestrates 3D game asset creation from Meshy CLI or Blender MCP into Studio with polygon budgets, PBR maps, and security audits. Use when generating or importing 3D Roblox assets."
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: roblox-asset-artist
---

# Roblox 3D Asset Pipeline

Connects text/image 3D generation (`meshy-3d-generation`, `blender` MCP, Studio `generate_mesh`) cleanly to Roblox Studio without importing high-poly lag bombs, broken pivots, or un-textured meshes.

## WHEN TO USE

- Creating custom weapons, pets, props, buildings, or rigged characters for Roblox via Meshy, Blender, or Studio MCP.
- Preparing external `.glb` / `.fbx` / `.obj` assets for Studio import.

## WHEN NOT TO USE

- Pure blockout / greyboxing using native Parts or Terrain — `roblox-world-building`.
- Only auditing a Creator Store asset ID — `roblox-asset-security`.

## DECISION TREE

```text
1. PICK GENERATOR
   - Hero organic prop / pet / weapon from text or image -> `meshy-3d-generation` (GLB/FBX + PBR)
   - Parametric modular architecture / hard-surface -> `blender` MCP (`execute_blender_code`)
   - Quick Studio-native primitive/mesh -> `roblox-studio-mcp` (`generate_mesh` / `generate_procedural_model`)

2. NORMALIZE IN BLENDER BEFORE STUDIO IMPORT
   - Target triangle budget: Props <= 2,500 tris; Hero weapons/pets <= 6,000 tris; Max single MeshPart <= 10,000 tris.
   - Apply transforms (`Ctrl+A` scale=1, rotation=0), set origin/pivot to base or grip handle, +Y/+Z forward aligned.
   - Verify UV map exists; pack/resize PBR textures <= 1024x1024 (`SurfaceAppearance`: ColorMap, NormalMap, RoughnessMap, MetalnessMap).

3. IMPORT, AUDIT & COLLISION SETUP
   - Import FBX/GLB into Studio or upload via Asset Manager.
   - Run `roblox-asset-security` scan if third-party model; set `CollisionFidelity = Box` (props) or `Hull`, `RenderFidelity = Automatic`.
   - Test rendering under `Future` lighting via `screen_capture`.
```

## FAILURE MODES & MITIGATIONS

1. **50k-Tri Frame Drop** — DETECT: raw AI mesh imported without decimate. FIX: Blender Decimate modifier to <=6k tris + LODs before export.
2. **Broken Pivot / Giant Scale** — DETECT: weapon floats 10 studs from hand grip. FIX: normalize origin to grip attachment and 1 Blender unit = 1 meter (~3.57 studs) before export.
3. **Hull Collision Trap** — DETECT: `PreciseConvexDecomposition` on 50 foliage props. FIX: set `CanCollide = false` + invisible simple hitbox Part or `Box` fidelity.

## VERIFICATION GATE

- [ ] Mesh triangle count verified <= 10,000 tris and texture maps <= 1024px.
- [ ] Transforms applied, origin aligned, `CollisionFidelity` set appropriately.
- [ ] Studio `screen_capture` confirms PBR lighting and clean console output.

## REFERENCES

- `meshy-3d-generation` — Meshy CLI text/image-to-3D generation and rigging
- `roblox-assets` & `roblox-asset-security` — budgets and backdoor screening
- `roblox-studio-mcp` — Studio instance verification and visual capture
