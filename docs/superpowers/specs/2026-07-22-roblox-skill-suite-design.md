# Roblox All-in-One Game Dev Skill Suite — Design Doc

**Date:** 2026-07-22
**Status:** Approved
**Author:** ZCode AI

## 1. Overview

A comprehensive suite of 21 AI skills that turn ZCode into a full-stack Roblox game development assistant. Every skill uses the Roblox Studio MCP for direct Studio integration, spawns subagents for execution, and includes pixel-perfect verification loops.

## 2. Core Principles

### 2.1 Subagent-Driven Execution
- Every skill spawns specialized agents (code-implementer, ui-ux-architect, red-team-qa, etc.)
- Main thread orchestrates only — never writes code directly
- Parallel execution where tasks are independent

### 2.2 Pixel-Perfect Accuracy
- Reference images = identical output, not "close enough"
- `screen_capture` verification loop: Before → Execute → After → Compare → Iterate
- Never report "done" until visual match is confirmed

### 2.3 No-Stop Execution
- Once ordered, skills execute end-to-end
- Verify, iterate, confirm — never abandon mid-task
- If blocked, research the solution and continue

### 2.4 MCP-Native
- Every skill uses Roblox MCP tools as primary execution mechanism
- Falls back to code patterns when MCP is unavailable

## 3. Architecture

### 3.1 Skill Layers

```
Layer 1: Orchestrator
  └── roblox-game-dev (routes to specialized skills)

Layer 2: Core Skills (one per topic)
  ├── roblox-coding
  ├── roblox-ui-ux
  ├── roblox-vfx
  ├── roblox-animation
  ├── roblox-3d-assets
  ├── roblox-audio
  ├── roblox-terrain
  ├── roblox-networking
  ├── roblox-security
  ├── roblox-performance
  ├── roblox-testing
  ├── roblox-plugins
  ├── roblox-architecture
  ├── roblox-economy
  ├── roblox-tools-workflow
  ├── roblox-avatar
  ├── roblox-cinematics
  ├── roblox-data-persistence
  └── roblox-asset-import

Layer 3: Orchestrator (master coordination)
  └── roblox-orchestrator
```

### 3.2 Trigger Design
Each skill's frontmatter `description` includes "Roblox" as a required keyword:
```yaml
---
name: roblox-coding
description: MANDATORY AUTO-INVOKE for all Roblox Luau coding, scripts, modules, DataStores, and event system tasks.
---
```

### 3.3 MCP Tool Mapping

| Skill | Primary MCP Tools |
|---|---|
| roblox-coding | `script_read`, `multi_edit`, `script_search`, `script_grep`, `execute_luau` |
| roblox-ui-ux | `search_game_tree`, `inspect_instance`, `execute_luau`, `screen_capture` |
| roblox-vfx | `generate_material`, `execute_luau`, `inspect_instance`, `screen_capture` |
| roblox-animation | `script_read`, `multi_edit`, `execute_luau`, `screen_capture` |
| roblox-3d-assets | `generate_mesh`, `generate_material`, `generate_procedural_model`, `search_asset`, `insert_asset`, `upload_image`, `store_image` |
| roblox-audio | `search_asset`, `insert_asset`, `execute_luau`, `inspect_instance` |
| roblox-terrain | `generate_procedural_model`, `execute_luau`, `search_asset`, `screen_capture` |
| roblox-networking | `script_read`, `multi_edit`, `script_grep`, `execute_luau` |
| roblox-security | `script_read`, `script_grep`, `multi_edit`, `execute_luau` |
| roblox-performance | `execute_luau`, `get_console_output`, `screen_capture` |
| roblox-testing | `start_stop_play`, `execute_luau`, `get_console_output`, `user_keyboard_input`, `user_mouse_input` |
| roblox-plugins | `execute_luau`, `multi_edit`, `search_game_tree` |
| roblox-architecture | `search_game_tree`, `inspect_instance`, `script_grep` |
| roblox-economy | `multi_edit`, `script_read`, `execute_luau`, `script_grep` |
| roblox-tools-workflow | `get_console_output`, `start_stop_play`, `character_navigation`, `user_keyboard_input`, `user_mouse_input`, `screen_capture` |
| roblox-avatar | `search_game_tree`, `inspect_instance`, `execute_luau`, `search_asset`, `insert_asset`, `screen_capture` |
| roblox-cinematics | `execute_luau`, `screen_capture`, `start_stop_play`, `user_keyboard_input` |
| roblox-data-persistence | `script_read`, `multi_edit`, `script_grep`, `execute_luau` |
| roblox-asset-import | `upload_image`, `store_image`, `search_asset`, `insert_asset`, `generate_mesh`, `generate_material` |
| roblox-orchestrator | All tools — coordinates across all skills |

## 4. Skill Structure Template

Every SKILL.md follows this structure:

```markdown
---
name: roblox-{topic}
description: MANDATORY AUTO-INVOKE for all Roblox {topic} tasks including {keywords}.
---

# ROBLOX {TOPIC}

## PURPOSE
What this skill does and when it triggers.

## MCP WORKFLOW
Step-by-step guide for using MCP tools for this topic.

## SUBAGENT PROTOCOL
Which agents to spawn and when.

## CODE PATTERNS
Production-ready Luau templates.

## VERIFICATION PROTOCOL
screen_capture + iteration loop for visual accuracy.

## BEST PRACTICES
Do's and don'ts for this topic.

## CROSS-REFERENCES
Links to related skills.

## OUTPUT FORMAT
Standard output format for this skill.
```

## 5. Detailed Skill Specifications

### 5.1 roblox-game-dev (Orchestrator)
- **Trigger:** Any Roblox game development request
- **Action:** Analyzes request → routes to appropriate specialized skill(s)
- **MCP:** All tools available
- **Subagents:** Dispatches to specialized skills

### 5.2 roblox-coding
- **Trigger:** Luau code, scripts, modules, events, API usage
- **MCP Workflow:**
  1. `script_search` / `script_grep` to find existing code
  2. `script_read` to understand context
  3. `multi_edit` to write/modify scripts
  4. `execute_luau` to test in Edit/Client/Server context
  5. `get_console_output` to verify no errors
- **Patterns:** Module patterns, event systems, OOP, state machines, DataStore wrappers

### 5.3 roblox-ui-ux
- **Trigger:** GUI, HUD, menus, ScreenGui, UIListLayout, themes, responsive design
- **MCP Workflow:**
  1. `search_game_tree` to find existing GUIs
  2. `inspect_instance` to understand UI hierarchy
  3. `execute_luau` to create/modify UI elements
  4. `screen_capture` to verify visual output
  5. Iterate until pixel-perfect match with reference
- **Patterns:** UI scale patterns, theme systems, animation transitions, accessibility

### 5.4 roblox-vfx
- **Trigger:** Particles, beams, trails, lighting, post-processing, shaders
- **MCP Workflow:**
  1. `inspect_instance` to check existing effects
  2. `generate_material` for custom materials
  3. `execute_luau` to create particle emitters, beams, etc.
  4. `screen_capture` to verify visual output
  5. Iterate until effect matches reference
- **Patterns:** ParticleEmitter configs, Beam setups, Lighting presets, ColorSequence/NumberSequence

### 5.5 roblox-animation
- **Trigger:** Animators, tweens, keyframes, Motor6D, rigging, easing
- **MCP Workflow:**
  1. `script_read` to understand existing animation code
  2. `multi_edit` to create/modify animation scripts
  3. `execute_luau` to test animations
  4. `screen_capture` to verify motion
- **Patterns:** TweenService configs, AnimationTrack patterns, procedural animation, easing functions

### 5.6 roblox-3d-assets
- **Trigger:** Mesh generation, materials, models, textures, 3D objects
- **MCP Workflow:**
  1. `generate_mesh` for custom meshes from text prompts
  2. `generate_material` for custom materials
  3. `generate_procedural_model` for parametric objects
  4. `search_asset` / `insert_asset` for marketplace assets
  5. `upload_image` / `store_image` for custom textures
  6. `screen_capture` to verify visual output
- **Patterns:** MeshPart setup, MaterialVariant creation, ProceduralModel attributes

### 5.7 roblox-audio
- **Trigger:** Sound, music, 3D audio, SFX, audio zones, ambient
- **MCP Workflow:**
  1. `search_asset` to find audio in Creator Store
  2. `insert_asset` to add audio to workspace
  3. `execute_luau` to set up SoundGroups, spatial audio
  4. `inspect_instance` to verify audio properties
- **Patterns:** SoundGroup setup, 3D spatial audio, crossfading, music managers

### 5.8 roblox-terrain
- **Trigger:** Terrain, world-building, biomes, foliage, skybox, decorations
- **MCP Workflow:**
  1. `generate_procedural_model` for terrain features
  2. `search_asset` for terrain assets
  3. `execute_luau` for Terrain API calls
  4. `screen_capture` to verify world appearance
- **Patterns:** Terrain:FillRegion, biome generation, foliage placement, skybox setup

### 5.9 roblox-networking
- **Trigger:** RemoteEvents, RemoteFunctions, replication, client-server communication
- **MCP Workflow:**
  1. `script_grep` to find existing RemoteEvents
  2. `script_read` to understand current networking patterns
  3. `multi_edit` to create/modify networking code
  4. `execute_luau` to test in Client/Server context
- **Patterns:** RemoteEvent wrappers, request-response patterns, replication optimization, signal libraries

### 5.10 roblox-security
- **Trigger:** Anti-exploit, server authority, input validation, security hardening
- **MCP Workflow:**
  1. `script_grep` to audit existing code for vulnerabilities
  2. `script_read` to understand attack surfaces
  3. `multi_edit` to add security measures
  4. `execute_luau` to test exploits and defenses
- **Patterns:** Server authority validation, rate limiting, anti-cheat, input sanitization

### 5.11 roblox-performance
- **Trigger:** Profiling, optimization, memory, streaming, frame rate
- **MCP Workflow:**
  1. `execute_luau` to run microprofiler queries
  2. `get_console_output` to check for performance warnings
  3. `screen_capture` to verify visual quality after optimization
- **Patterns:** Object pooling, streaming optimization, memory management, batch processing

### 5.12 roblox-testing
- **Trigger:** Unit tests, playtest automation, QA, test-driven development
- **MCP Workflow:**
  1. `start_stop_play` to control playtesting
  2. `execute_luau` to run test suites
  3. `user_keyboard_input` / `user_mouse_input` for UI testing
  4. `get_console_output` to check test results
  5. `screen_capture` for visual regression
- **Patterns:** TestEZ patterns, automated playtesting, visual regression tests

### 5.13 roblox-plugins
- **Trigger:** Plugin development, toolbar, DockWidget, Studio API
- **MCP Workflow:**
  1. `search_game_tree` to explore plugin structure
  2. `multi_edit` to create/modify plugin code
  3. `execute_luau` in Edit context to test
- **Patterns:** DockWidgetPluginGui, toolbar buttons, plugin settings, menu integration

### 5.14 roblox-architecture
- **Trigger:** Game structure, module patterns, ECS, event systems, code organization
- **MCP Workflow:**
  1. `search_game_tree` to understand current structure
  2. `inspect_instance` to examine instance hierarchy
  3. `script_grep` to find patterns across codebase
  4. `multi_edit` to restructure
- **Patterns:** Module architecture, event-driven design, component systems, folder organization

### 5.15 roblox-economy
- **Trigger:** DevProducts, GamePasses, leaderboards, currency, monetization
- **MCP Workflow:**
  1. `script_grep` to find existing economy code
  2. `script_read` to understand current patterns
  3. `multi_edit` to add/modify economy systems
  4. `execute_luau` to test transactions
- **Patterns:** MarketplaceService integration, currency systems, purchase validation, data persistence

### 5.16 roblox-tools-workflow
- **Trigger:** Debugging, playtesting, screenshots, input simulation, Studio workflows
- **MCP Workflow:**
  1. `get_studio_state` to check current state
  2. `start_stop_play` to control playtesting
  3. `character_navigation` to move character
  4. `user_keyboard_input` / `user_mouse_input` for input simulation
  5. `screen_capture` for screenshots
  6. `get_console_output` for debugging
- **Patterns:** Debug workflows, automated testing, screenshot comparison, input recording

### 5.17 roblox-avatar
- **Trigger:** Avatar/character customization, body parts, clothing, accessories, R15/R6
- **MCP Workflow:**
  1. `search_game_tree` to find existing avatar setup
  2. `inspect_instance` to examine character hierarchy
  3. `search_asset` / `insert_asset` for avatar items
  4. `execute_luau` to apply customization
  5. `screen_capture` to verify appearance
- **Patterns:** HumanoidDescription, body scaling, accessory fitting, clothing layers

### 5.18 roblox-cinematics
- **Trigger:** Cutscenes, camera paths, dialogue, cinematic sequences, letterboxing
- **MCP Workflow:**
  1. `script_read` to find existing camera/cinematic code
  2. `multi_edit` to create cutscene scripts
  3. `execute_luau` to test camera movements
  4. `start_stop_play` + `user_keyboard_input` to playtest
  5. `screen_capture` to verify cinematic output
- **Patterns:** Camera tweening, CFrame interpolation, dialogue UI, letterbox bars, fade transitions

### 5.19 roblox-data-persistence
- **Trigger:** DataStore, saving/loading, data migration, leaderboards, session locking
- **MCP Workflow:**
  1. `script_grep` to find existing DataStore usage
  2. `script_read` to understand current data patterns
  3. `multi_edit` to implement/modify persistence
  4. `execute_luau` to test save/load cycles
- **Patterns:** DataStore wrapper, session locking, retry logic, data migration, backup systems

### 5.20 roblox-asset-import
- **Trigger:** Importing external images, audio, models into Roblox
- **MCP Workflow:**
  1. `store_image` to load local images
  2. `upload_image` to upload to Roblox
  3. `search_asset` to find marketplace alternatives
  4. `insert_asset` to place in workspace
  5. `generate_mesh` / `generate_material` for AI-generated assets
  6. `screen_capture` to verify imported assets
- **Patterns:** Image upload pipeline, audio import, mesh conversion, texture application

### 5.21 roblox-orchestrator (Master)
- **Trigger:** Complex multi-skill tasks, full game builds, large features
- **Action:** Coordinates all subagents across skills, ensures no-stop execution
- **MCP:** All tools
- **Subagents:** Spawns multiple specialized agents in parallel

## 6. Verification Protocol

Every skill that modifies visuals or behavior:

1. **Before** — `screen_capture` current state
2. **Execute** — Make changes via MCP tools
3. **After** — `screen_capture` the result
4. **Compare** — If user provided reference image, compare and iterate until identical
5. **Confirm** — Only report "done" when visual match is verified

## 7. Subagent Protocol

| Task Type | Agent | When |
|---|---|---|
| Code implementation | `code-implementer` | Writing/modifying Luau scripts |
| UI/UX design | `ui-ux-architect` | Building GUIs, layouts, themes |
| QA/security review | `red-team-qa` | Before marking any task complete |
| Performance check | `performance-engineer` | After implementing features |
| Documentation | `documentation-engineer` | Final output formatting |
| Asset creation | `browser-automation` | Importing assets via web |

## 8. Implementation Order

1. `roblox-game-dev` (orchestrator) — routes all requests
2. `roblox-coding` — foundation for all other skills
3. `roblox-ui-ux` — most common visual task
4. `roblox-3d-assets` — asset generation
5. `roblox-vfx` — visual effects
6. `roblox-animation` — motion and transitions
7. `roblox-audio` — sound and music
8. `roblox-terrain` — world building
9. `roblox-networking` — client-server communication
10. `roblox-security` — protection and validation
11. `roblox-performance` — optimization
12. `roblox-testing` — quality assurance
13. `roblox-plugins` — Studio extensions
14. `roblox-architecture` — code organization
15. `roblox-economy` — monetization
16. `roblox-tools-workflow` — debugging and testing
17. `roblox-avatar` — character customization
18. `roblox-cinematics` — cutscenes and camera
19. `roblox-data-persistence` — save/load systems
20. `roblox-asset-import` — external asset pipeline
21. `roblox-orchestrator` — master coordination

## 9. File Locations

All skills will be created at:
```
C:\Users\Oz\.zcode\skills\roblox-{topic}\SKILL.md
```

The existing `game-developer` skill will be updated to reference the new Roblox-specific skills.
