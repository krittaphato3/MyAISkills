---
name: meshy-3d-generation
description: "Generates and edits 3D assets via Meshy CLI: text/image-to-3D, texturing, remeshing, LODs, UV unwrapping, format conversion, and rigging. Use when creating or converting 3D game assets."
license: MIT
compatibility: "Needs Node.js 22.12+ and the Meshy CLI 0.8.x (npm install -g meshy-cli@0.8); network access to Meshy API."
metadata:
  version: 1.1.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: roblox-asset-artist
---

# Meshy 3D Generation

Use Meshy CLI **0.8** (`0.8.6` or later) to turn requests into delivered `.glb` / `.fbx` / `.obj` 3D assets with preview verification. Login or task submission alone is not completion.

## WHEN TO USE

- User asks to generate, texture, remesh, UV-unwrap, rig, animate, or convert a 3D model via Meshy CLI.
- Creating custom hero game props, characters, or weapons for `roblox-3d-pipeline` or Blender workflows.

## WHEN NOT TO USE

- Procedural parametric Blender edits without Meshy API credits — use `blender` MCP directly.
- Simple Roblox blockout geometry — `roblox-world-building`.

## DECISION TREE

```text
1. PREFLIGHT AUTH & SCOPE
   - Check CLI (`meshy --version >= 0.8.6`) and `auth status --format json --no-update-check`.
   - If login is required, run `auth login --device`, present URL/code to user, and verify `auth status` before submitting jobs.
   - Confirm asset purpose & topology budget BEFORE paid generation (e.g. game asset low-poly smart topology <=6k tris vs high-poly render).

2. SUBMIT & AWAIT SINGLE JOB
   - Prefer reference-image -> image-to-3D when exact silhouette matters; use text-to-3D for fast ideation.
   - Submit once with `create --async`, capture task ID, and wait on that task (never re-submit duplicate paid tasks on timeout).

3. CONVERT & VERIFY DELIVERY
   - Export target format (`fbx` / `glb` / `obj`), inspect preview output, and hand off to `roblox-3d-pipeline` for pivot/scale checks.
```

## Read what this request needs

| Need | Reference |
|---|---|
| CLI runner, credentials, or output location | [Setup](references/setup.md) |
| Generation, texturing, remeshing, conversion, or 2D images | [Pipelines](references/pipelines.md) |
| Rigging, animation, or generated motion | [Animation](references/animation.md) |
| Cost, waiting, preview, delivery, or lookup | [Delivery](references/delivery.md) |
| Showing previews in visual chat | [Visual hosts](references/visual-hosts.md) |
| Failed or uncertain operation | [Troubleshooting](references/troubleshooting.md) |

## FAILURE MODES & MITIGATIONS

1. **Duplicate Paid Charges** — DETECT: re-running `create --async` after a CLI timeout. FIX: poll existing task ID via `Troubleshooting` lookup before any new submit.
2. **High-Poly Game Bloat** — DETECT: exporting standard 100k+ poly model for mobile/Roblox. FIX: specify game smart-topology options up front or remesh/decimate to <=6k tris.
3. **Auth Leakage** — DETECT: echoing API keys/tokens in chat or project files. FIX: device-code auth only, keep credentials strictly inside Meshy CLI config.

## VERIFICATION GATE

- [ ] Requested 3D file saved at target path in requested format with non-zero size.
- [ ] Topology/face budget verified for game assets; available preview inspected.
- [ ] Actual job status and output paths reported accurately.

## REFERENCES

- `roblox-3d-pipeline` — Blender normalization and Roblox Studio import gate
- `roblox-assets` — triangle and texture memory budgets
- `references/setup.md`, `references/pipelines.md`, `references/delivery.md`
