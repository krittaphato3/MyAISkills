# Roblox Skill Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 21 Roblox game development skills that turn ZCode into a full-stack Roblox assistant with MCP integration, subagent execution, and pixel-perfect verification.

**Architecture:** Each skill is a standalone SKILL.md file in `C:\Users\Oz\.zcode\skills\roblox-{topic}\`. All skills follow the same template structure. Skills are independent and can be created in parallel via subagents. The existing `game-developer` skill will be updated to reference the new Roblox skills.

**Tech Stack:** Markdown (SKILL.md), Roblox Studio MCP tools, ZCode subagent system

## Global Constraints

- All skills go in `C:\Users\Oz\.zcode\skills\roblox-{topic}\SKILL.md`
- Each skill's frontmatter `description` MUST include "Roblox" as a trigger keyword
- Each skill MUST include: MCP Workflow, Subagent Protocol, Code Patterns, Verification Protocol, Best Practices
- Skills must reference the Roblox MCP tools by exact name (e.g., `script_read`, `multi_edit`)
- No skill should trigger for non-Roblox game dev requests
- All code examples must be production-ready Luau
- Each skill targets a specific topic — no overlap in primary responsibility

---

## Batch 1: Foundation Skills (create first — other skills reference these)

### Task 1: roblox-game-dev (Orchestrator)

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-game-dev\SKILL.md`

**Interfaces:**
- Consumes: User request mentioning "Roblox"
- Produces: Routes to specialized skill(s)

- [ ] **Step 1: Create the directory**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-game-dev"
```

- [ ] **Step 2: Create SKILL.md**

Write `C:\Users\Oz\.zcode\skills\roblox-game-dev\SKILL.md` with this content:

```markdown
---
name: roblox-game-dev
description: MANDATORY AUTO-INVOKE for ALL Roblox game development tasks. Entry point that routes to specialized Roblox skills for coding, UI/UX, VFX, animation, assets, audio, terrain, networking, security, performance, testing, plugins, architecture, economy, avatar, cinematics, data persistence, and asset import.
---

# ROBLOX GAME DEVELOPMENT

Expert Roblox game development across all disciplines. This is the entry point — route to specialized skills for execution.

## PURPOSE

When a user mentions "Roblox" or "Luau" in a game development context, this skill activates and determines which specialized skill(s) to invoke.

## ROUTING TABLE

| User Intent | Route To Skill |
|---|---|
| Writing/modifying Luau code, scripts, modules | `roblox-coding` |
| GUI, HUD, menus, ScreenGui, UI layout | `roblox-ui-ux` |
| Particles, beams, trails, lighting effects | `roblox-vfx` |
| Animations, tweens, keyframes, rigging | `roblox-animation` |
| 3D meshes, materials, models, textures | `roblox-3d-assets` |
| Sound, music, 3D audio, SFX | `roblox-audio` |
| Terrain, world-building, biomes, foliage | `roblox-terrain` |
| RemoteEvents, replication, client-server | `roblox-networking` |
| Anti-exploit, server authority, security | `roblox-security` |
| Profiling, optimization, memory | `roblox-performance` |
| Unit tests, playtest automation | `roblox-testing` |
| Plugin development, toolbar, DockWidget | `roblox-plugins` |
| Game structure, patterns, ECS, organization | `roblox-architecture` |
| DevProducts, GamePasses, currency, monetization | `roblox-economy` |
| Debugging, screenshots, input simulation | `roblox-tools-workflow` |
| Avatar customization, body parts, clothing | `roblox-avatar` |
| Cutscenes, camera paths, dialogue, cinematics | `roblox-cinematics` |
| DataStore, saving/loading, leaderboards | `roblox-data-persistence` |
| Importing external images, audio, models | `roblox-asset-import` |
| Complex multi-skill tasks, full game builds | `roblox-orchestrator` |

## MCP TOOLS AVAILABLE

All Roblox MCP tools are available for routing decisions:
- `search_game_tree` — explore instance hierarchy
- `inspect_instance` — examine specific instances
- `script_search` / `script_grep` — find scripts
- `get_studio_state` — check current Studio state

## WORKFLOW

1. **Analyze** the user's request
2. **Identify** which specialized skill(s) apply
3. **Invoke** the appropriate skill via the Skill tool
4. **Coordinate** if multiple skills are needed

## CROSS-REFERENCES

All Roblox skills: `roblox-coding`, `roblox-ui-ux`, `roblox-vfx`, `roblox-animation`, `roblox-3d-assets`, `roblox-audio`, `roblox-terrain`, `roblox-networking`, `roblox-security`, `roblox-performance`, `roblox-testing`, `roblox-plugins`, `roblox-architecture`, `roblox-economy`, `roblox-tools-workflow`, `roblox-avatar`, `roblox-cinematics`, `roblox-data-persistence`, `roblox-asset-import`, `roblox-orchestrator`
```

- [ ] **Step 3: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-game-dev\SKILL.md"
git commit -m "feat: add roblox-game-dev orchestrator skill"
```

---

### Task 2: roblox-coding

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-coding\SKILL.md`

**Interfaces:**
- Consumes: User request for Luau code, scripts, modules, events, API usage
- Produces: Production-ready Luau scripts written via MCP `multi_edit`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-coding"
```

- [ ] **Step 2: Create SKILL.md**

Write `C:\Users\Oz\.zcode\skills\roblox-coding\SKILL.md` with this content:

```markdown
---
name: roblox-coding
description: MANDATORY AUTO-INVOKE for all Roblox Luau coding, scripts, modules, DataStores, event systems, and API usage tasks. Uses MCP tools to read, write, and test Luau code directly in Roblox Studio.
---

# ROBLOX CODING

Production-quality Luau development with direct Studio integration via MCP.

## MCP WORKFLOW

### Step 1: Understand Current State
```
1. script_search("keyword") — find existing scripts by name
2. script_grep("pattern") — find code patterns across all scripts
3. script_read("game.ServerScriptService.MyScript") — read full script content
4. search_game_tree(path: "ServerScriptService") — explore script locations
```

### Step 2: Write/Modify Code
```
1. multi_edit(
     file_path: "game.ServerScriptService.MyScript",
     edits: [{ old_string: "...", new_string: "..." }],
     datamodel_type: "Edit"
   ) — apply multiple edits in one batch
2. For new scripts: multi_edit with className: "LocalScript" or "Script"
```

### Step 3: Test
```
1. execute_luau(code: "print('test')", datamodel_type: "Edit") — quick test
2. get_studio_state() — check if play is running
3. start_stop_play(is_start: true) — start play test
4. execute_luau(code: "...", datamodel_type: "Client") — test client-side
5. execute_luau(code: "...", datamodel_type: "Server") — test server-side
6. get_console_output() — check for errors
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Writing new scripts | `code-implementer` |
| Refactoring existing code | `refactoring-specialist` |
| Code review | `red-team-qa` |
| Performance optimization | `performance-engineer` |

## CODE PATTERNS

### Module Pattern
```lua
-- ReplicatedStorage.Modules.MyModule
local MyModule = {}
MyModule.__index = MyModule

function MyModule.new(config)
    local self = setmetatable({}, MyModule)
    self.config = config or {}
    return self
end

function MyModule:DoSomething()
    -- implementation
end

return MyModule
```

### Event System
```lua
-- Server-side event handler
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local Events = ReplicatedStorage:WaitForChild("Events")
local MyEvent = Events:WaitForChild("MyEvent")

MyEvent.OnServerEvent:Connect(function(player, action, data)
    -- Validate input
    if type(action) ~= "string" then return end
    if type(data) ~= "table" then return end

    -- Process action
    -- ...
end)
```

### DataStore Wrapper
```lua
local DataStoreService = game:GetService("DataStoreService")
local MyDataStore = DataStoreService:GetDataStore("PlayerData_v1")

local DataStoreManager = {}

function DataStoreManager:LoadData(player)
    local success, data = pcall(function()
        return MyDataStore:GetAsync("player_" .. player.UserId)
    end)

    if success and data then
        return data
    end

    -- Default data structure
    return {
        Coins = 0,
        Level = 1,
        Inventory = {},
    }
end

function DataStoreManager:SaveData(player, data)
    local success, err = pcall(function()
        MyDataStore:SetAsync("player_" .. player.UserId, data)
    end)

    if not success then
        warn("Failed to save data for " .. player.Name .. ": " .. tostring(err))
    end

    return success
end

return DataStoreManager
```

### State Machine
```lua
local StateMachine = {}
StateMachine.__index = StateMachine

function StateMachine.new()
    return setmetatable({
        states = {},
        currentState = nil,
    }, StateMachine)
end

function StateMachine:AddState(name, state)
    self.states[name] = state
end

function StateMachine:Transition(newState)
    if self.currentState then
        self.currentState:Exit()
    end
    self.currentState = self.states[newState]
    if self.currentState then
        self.currentState:Enter()
    end
end

function StateMachine:Update(dt)
    if self.currentState then
        self.currentState:Update(dt)
    end
end

return StateMachine
```

## BEST PRACTICES

- Always use `pcall` for DataStore calls
- Never trust client input — validate everything on server
- Use `:WaitForChild()` with timeout for critical instances
- Prefer `task.spawn` / `task.delay` over `spawn` / `delay`
- Use typed tables for documentation: `type PlayerData = { Coins: number, Level: number }`
- Avoid global variables — use module patterns
- Use `task.cancel()` for cancellable async work

## VERIFICATION PROTOCOL

1. `get_console_output()` — check for errors after code changes
2. `execute_luau(code: "print('verification')")` — quick sanity check
3. `screen_capture()` — verify visual output if UI-related
4. Never report "done" until console shows no errors

## OUTPUT FORMAT

```text
[ROBLOX CODING]
Task: {description}
Files Modified: {list}
Patterns Used: {list}
Status: {complete|needs-review}
```
```

- [ ] **Step 3: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-coding\SKILL.md"
git commit -m "feat: add roblox-coding skill"
```

---

### Task 3: roblox-architecture

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-architecture\SKILL.md`

**Interfaces:**
- Consumes: User request for game structure, patterns, code organization
- Produces: Architectural decisions applied via MCP

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-architecture"
```

Write `C:\Users\Oz\.zcode\skills\roblox-architecture\SKILL.md` with:

```markdown
---
name: roblox-architecture
description: MANDATORY AUTO-INVOKE for all Roblox game architecture, module patterns, ECS, event systems, folder structure, and code organization tasks. Uses MCP to explore and restructure the DataModel.
---

# ROBLOX ARCHITECTURE

Game structure, module patterns, and code organization for Roblox projects.

## MCP WORKFLOW

### Step 1: Analyze Current Structure
```
1. search_game_tree(max_depth: 4) — full project overview
2. search_game_tree(path: "ServerScriptService", instance_type: "BaseScript") — find all server scripts
3. search_game_tree(path: "ReplicatedStorage", instance_type: "ModuleScript") — find all modules
4. inspect_instance(path: "Workspace.MyFolder") — examine specific hierarchy
5. script_grep("require(") — find module dependencies
```

### Step 2: Restructure
```
1. multi_edit() — create new module scripts
2. execute_luau(code: "Instance.new('Folder').Name = 'Systems'", datamodel_type: "Edit") — create folders
3. search_game_tree() — verify new structure
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Structure analysis | `Explore` subagent |
| Refactoring | `refactoring-specialist` |
| Code review | `red-team-qa` |

## ARCHITECTURE PATTERNS

### Folder Structure
```
game/
├── ServerScriptService/
│   ├── Server/
│   │   ├── Systems/          -- Game systems (DataStore, Matchmaking, etc.)
│   │   ├── Events/           -- Server event handlers
│   │   └── Commands/         -- Admin commands
├── ReplicatedStorage/
│   ├── Modules/              -- Shared modules
│   │   ├── Utils/            -- Utility functions
│   │   ├── Types/            -- Type definitions
│   │   └── Events/           -- RemoteEvent definitions
│   ├── Events/               -- RemoteEvents/RemoteFunctions
│   └── Assets/               -- Shared assets
├── StarterPlayerScripts/     -- Client scripts
│   ├── Client/
│   │   ├── UI/               -- UI controllers
│   │   ├── Systems/          -- Client systems
│   │   └── Events/           -- Client event handlers
├── StarterGui/               -- UI elements
│   ├── HUD/
│   ├── Menus/
│   └── Themes/
└── Workspace/
    ├── Map/                  -- World geometry
    ├── Spawns/               -- Spawn points
    └── Interactive/          -- Interactive objects
```

### Event-Driven Architecture
```lua
-- ReplicatedStorage.Modules.EventBus (shared)
local EventBus = {}
EventBus.__index = EventBus

function EventBus.new()
    return setmetatable({ listeners = {} }, EventBus)
end

function EventBus:On(event, callback)
    if not self.listeners[event] then
        self.listeners[event] = {}
    end
    table.insert(self.listeners[event], callback)
end

function EventBus:Emit(event, ...)
    if self.listeners[event] then
        for _, callback in ipairs(self.listeners[event]) do
            task.spawn(callback, ...)
        end
    end
end

return EventBus
```

### Component System
```lua
-- Simple ECS-like component system
local ComponentRegistry = {}

function ComponentRegistry:Register(componentName, defaults)
    ComponentRegistry[componentName] = {
        defaults = defaults or {},
    }
end

function ComponentRegistry:Create(componentName, overrides)
    local def = ComponentRegistry[componentName]
    if not def then return nil end

    local component = {}
    for k, v in pairs(def.defaults) do
        component[k] = v
    end
    if overrides then
        for k, v in pairs(overrides) do
            component[k] = v
        end
    end
    return component
end

return ComponentRegistry
```

## BEST PRACTICES

- Group related scripts into Folders, not flat lists
- Use ModuleScripts for reusable logic — never duplicate code
- Separate client and server concerns strictly
- Use type annotations for documentation
- Keep scripts under 500 lines — split if larger
- Use dependency injection via module requires
- Name folders with PascalCase, scripts with descriptive names

## VERIFICATION PROTOCOL

1. `search_game_tree(max_depth: 4)` — verify structure after changes
2. `script_grep("require(")` — verify no broken dependencies
3. `get_console_output()` — check for require errors

## CROSS-REFERENCES

- `roblox-coding` — for code patterns and Luau expertise
- `roblox-networking` — for client-server architecture
- `roblox-plugins` — for plugin architecture
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-architecture\SKILL.md"
git commit -m "feat: add roblox-architecture skill"
```

---

## Batch 2: Visual Skills (can be created in parallel)

### Task 4: roblox-ui-ux

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-ui-ux\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-ui-ux"
```

Write `C:\Users\Oz\.zcode\skills\roblox-ui-ux\SKILL.md` with:

```markdown
---
name: roblox-ui-ux
description: MANDATORY AUTO-INVOKE for all Roblox GUI, HUD, menus, ScreenGui, UIListLayout, themes, responsive design, and UI animation tasks. Uses MCP to build, inspect, and verify UI elements with pixel-perfect accuracy.
---

# ROBLOX UI/UX

Production-quality GUI development with pixel-perfect verification.

## MCP WORKFLOW

### Step 1: Analyze Existing UI
```
1. search_game_tree(path: "StarterGui", max_depth: 6) — explore UI hierarchy
2. inspect_instance(path: "StarterGui.MyScreenGui") — examine UI properties
3. script_grep("ScreenGui") — find UI-related code
```

### Step 2: Build/Modify UI
```
1. execute_luau(code: [UI creation code], datamodel_type: "Edit") — create UI elements
2. multi_edit() — modify UI scripts
3. screen_capture() — verify visual output
4. Compare with reference image — iterate until identical
```

### Step 3: Verify
```
1. screen_capture() — capture final state
2. If user provided reference: compare and iterate
3. get_console_output() — check for UI errors
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| UI design/layout | `ui-ux-architect` |
| UI scripts | `code-implementer` |
| Accessibility check | `accessibility-specialist` |
| Visual verification | `screen_capture` + comparison |

## CODE PATTERNS

### ScreenGui Setup
```lua
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "GameHUD"
screenGui.ResetOnSpawn = false
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
screenGui.Parent = playerGui

-- Main frame
local mainFrame = Instance.new("Frame")
mainFrame.Name = "MainFrame"
mainFrame.Size = UDim2.new(0.3, 0, 0.5, 0)
mainFrame.Position = UDim2.new(0.02, 0, 0.25, 0)
mainFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
mainFrame.BackgroundTransparency = 0.1
mainFrame.Parent = screenGui

-- UIListLayout for auto-arrangement
local layout = Instance.new("UIListLayout")
layout.Padding = UDim.new(0, 8)
layout.FillDirection = Enum.FillDirection.Vertical
layout.HorizontalAlignment = Enum.HorizontalAlignment.Left
layout.Parent = mainFrame

-- Corner rounding
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 8)
corner.Parent = mainFrame
```

### Responsive UI
```lua
local Camera = workspace.CurrentCamera
local screenGui = script.Parent

local function updateLayout()
    local viewportSize = Camera.ViewportSize
    local isMobile = viewportSize.X < 768

    if isMobile then
        -- Mobile layout
        screenGui.MainFrame.Size = UDim2.new(0.9, 0, 0.4, 0)
        screenGui.MainFrame.Position = UDim2.new(0.05, 0, 0.3, 0)
    else
        -- Desktop layout
        screenGui.MainFrame.Size = UDim2.new(0.3, 0, 0.5, 0)
        screenGui.MainFrame.Position = UDim2.new(0.02, 0, 0.25, 0)
    end
end

Camera:GetPropertyChangedSignal("ViewportSize"):Connect(updateLayout)
updateLayout()
```

### UI Animation
```lua
local TweenService = game:GetService("TweenService")

local function fadeIn(guiObject, duration)
    guiObject.GroupTransparency = 1
    local tween = TweenService:Create(
        guiObject,
        TweenInfo.new(duration or 0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
        { GroupTransparency = 0 }
    )
    tween:Play()
    return tween
end

local function slideIn(guiObject, duration)
    local originalPos = guiObject.Position
    guiObject.Position = originalPos + UDim2.new(0, -100, 0, 0)
    guiObject.GroupTransparency = 1

    local tween = TweenService:Create(
        guiObject,
        TweenInfo.new(duration or 0.3, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        { Position = originalPos, GroupTransparency = 0 }
    )
    tween:Play()
    return tween
end
```

### Theme System
```lua
local Themes = {
    Dark = {
        Background = Color3.fromRGB(30, 30, 30),
        Surface = Color3.fromRGB(45, 45, 45),
        Primary = Color3.fromRGB(99, 102, 241),
        Text = Color3.fromRGB(255, 255, 255),
        TextSecondary = Color3.fromRGB(156, 163, 175),
    },
    Light = {
        Background = Color3.fromRGB(243, 244, 246),
        Surface = Color3.fromRGB(255, 255, 255),
        Primary = Color3.fromRGB(99, 102, 241),
        Text = Color3.fromRGB(17, 24, 39),
        TextSecondary = Color3.fromRGB(107, 114, 128),
    },
}

local ThemeManager = {}
local currentTheme = Themes.Dark

function ThemeManager:SetTheme(themeName)
    currentTheme = Themes[themeName] or Themes.Dark
end

function ThemeManager:GetColor(colorName)
    return currentTheme[colorName]
end

function ThemeManager:ApplyToFrame(frame)
    frame.BackgroundColor3 = currentTheme.Background
end

return ThemeManager
```

## VERIFICATION PROTOCOL

1. `screen_capture()` — capture before changes
2. Execute UI creation code
3. `screen_capture()` — capture after changes
4. If reference image provided: compare pixel-by-pixel
5. Iterate: adjust properties → re-capture → compare
6. Only report "done" when visual match is confirmed

## BEST PRACTICES

- Use `UIListLayout` / `UIGridLayout` for automatic arrangement
- Always set `ResetOnSpawn = false` for persistent HUDs
- Use `UIScale` for responsive elements
- Prefer `UIPadding` over manual positioning
- Use `GroupTransparency` for fading entire containers
- Test on multiple viewport sizes (mobile, tablet, desktop)
- Use `ZIndexBehavior = Enum.ZIndexBehavior.Sibling` for proper layering
- Avoid nested frames deeper than 3 levels

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-animation` — for UI animations
- `roblox-vfx` — for visual effects on UI
- `roblox-tools-workflow` — for screenshots and verification
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-ui-ux\SKILL.md"
git commit -m "feat: add roblox-ui-ux skill"
```

---

### Task 5: roblox-vfx

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-vfx\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-vfx"
```

Write `C:\Users\Oz\.zcode\skills\roblox-vfx\SKILL.md` with:

```markdown
---
name: roblox-vfx
description: MANDATORY AUTO-INVOKE for all Roblox visual effects including particles, beams, trails, lighting, post-processing, materials, and shader-like effects. Uses MCP to create, inspect, and verify VFX with pixel-perfect accuracy.
---

# ROBLOX VFX

Production-quality visual effects with MCP-driven creation and verification.

## MCP WORKFLOW

### Step 1: Analyze Existing Effects
```
1. search_game_tree(instance_type: "ParticleEmitter") — find existing particles
2. search_game_tree(instance_type: "Beam") — find existing beams
3. inspect_instance(path: "Workspace.Effects.MyEffect") — examine effect properties
4. script_grep("ParticleEmitter") — find effect-related code
```

### Step 2: Create Effects
```
1. generate_material(materialDescription: "...", baseMaterial: "Plastic", materialPattern: "Regular", materialId: "...") — custom materials
2. execute_luau(code: [VFX creation code], datamodel_type: "Edit") — create effects
3. screen_capture() — verify visual output
```

### Step 3: Verify
```
1. screen_capture() — capture effect
2. Compare with reference — iterate until match
3. get_console_output() — check for errors
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| VFX creation | `code-implementer` |
| Material generation | `generate_material` MCP tool |
| Visual verification | `screen_capture` + comparison |

## CODE PATTERNS

### Particle Explosion
```lua
local function createExplosion(position)
    local attachment = Instance.new("Attachment")
    attachment.WorldPosition = position
    attachment.Parent = workspace.Terrain

    local emitter = Instance.new("ParticleEmitter")
    emitter.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 200, 50)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 100, 0)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 0, 0)),
    })
    emitter.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(0.5, 2),
        NumberSequenceKeypoint.new(1, 0),
    })
    emitter.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.8, 0),
        NumberSequenceKeypoint.new(1, 1),
    })
    emitter.Lifetime = NumberRange.new(0.5, 1.5)
    emitter.Speed = NumberRange.new(20, 40)
    emitter.SpreadAngle = Vector2.new(360, 360)
    emitter.Rate = 0
    emitter.Parent = attachment

    -- Burst once
    emitter:Emit(50)

    -- Cleanup after effect finishes
    game:GetService("Debris"):AddItem(attachment, 2)
end
```

### Beam Effect
```lua
local function createBeam(part0, part1, color)
    local attachment0 = Instance.new("Attachment")
    attachment0.Parent = part0

    local attachment1 = Instance.new("Attachment")
    attachment1.Parent = part1

    local beam = Instance.new("Beam")
    beam.Attachment0 = attachment0
    beam.Attachment1 = attachment1
    beam.Color = ColorSequence.new(color or Color3.fromRGB(0, 150, 255))
    beam.Width0 = 0.5
    beam.Width1 = 0.5
    beam.LightEmission = 1
    beam.FaceCamera = true
    beam.Parent = part0

    return beam
end
```

### Trail Effect
```lua
local function setupTrail(part)
    local attachment0 = Instance.new("Attachment")
    attachment0.Position = Vector3.new(0, 0.5, 0)
    attachment0.Parent = part

    local attachment1 = Instance.new("Attachment")
    attachment1.Position = Vector3.new(0, -0.5, 0)
    attachment1.Parent = part

    local trail = Instance.new("Trail")
    trail.Attachment0 = attachment0
    trail.Attachment1 = attachment1
    trail.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(100, 200, 255)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 50, 150)),
    })
    trail.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(1, 1),
    })
    trail.Lifetime = 1
    trail.MinLength = 0.1
    trail.LightEmission = 0.8
    trail.Parent = part

    return trail
end
```

### Lighting Preset
```lua
local Lighting = game:GetService("Lighting")

local function applyNightLighting()
    Lighting.ClockTime = 0
    Lighting.Ambient = Color3.fromRGB(20, 20, 40)
    Lighting.Brightness = 0.5
    Lighting.FogEnd = 1000
    Lighting.FogColor = Color3.fromRGB(10, 10, 30)

    -- Remove existing effects
    for _, child in ipairs(Lighting:GetChildren()) do
        if child:IsA("PostEffect") then
            child:Destroy()
        end
    end

    -- Add bloom
    local bloom = Instance.new("BloomEffect")
    bloom.Intensity = 0.5
    bloom.Size = 24
    bloom.Threshold = 1.5
    bloom.Parent = Lighting

    -- Add color correction
    local cc = Instance.new("ColorCorrectionEffect")
    cc.Brightness = 0
    cc.Contrast = 0.1
    cc.Saturation = -0.2
    cc.TintColor = Color3.fromRGB(180, 180, 220)
    cc.Parent = Lighting
end
```

## VERIFICATION PROTOCOL

1. `screen_capture()` — capture before
2. Create VFX via `execute_luau`
3. `screen_capture()` — capture after
4. Compare with reference image
5. Iterate: adjust colors/sizes/positions → re-capture → compare
6. Only confirm when visual matches

## BEST PRACTICES

- Use `Debris:AddItem()` for cleanup of temporary effects
- Set `LightEmission = 1` for glowing effects
- Use `FaceCamera = true` for beams and billboards
- Limit particle count for performance (aim for < 1000 active particles)
- Use `Emit(n)` for one-shot bursts instead of continuous emission
- Pool frequently-created effects instead of destroying/recreating
- Test effects at different camera distances

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-3d-assets` — for materials and meshes
- `roblox-performance` — for VFX optimization
- `roblox-tools-workflow` — for screenshots
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-vfx\SKILL.md"
git commit -m "feat: add roblox-vfx skill"
```

---

### Task 6: roblox-animation

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-animation\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-animation"
```

Write `C:\Users\Oz\.zcode\skills\roblox-animation\SKILL.md` with:

```markdown
---
name: roblox-animation
description: MANDATORY AUTO-INVOKE for all Roblox animation tasks including Animators, tweens, keyframes, Motor6D rigging, easing, procedural animation, and motion design. Uses MCP to create, test, and verify animations.
---

# ROBLOX ANIMATION

Production-quality animation with MCP-driven creation and verification.

## MCP WORKFLOW

### Step 1: Analyze Existing Animations
```
1. script_grep("Animator") — find animation-related code
2. search_game_tree(instance_type: "AnimationController") — find animation setups
3. inspect_instance(path: "Workspace.Character.Humanoid") — examine humanoid
4. script_read("game.ServerScriptService.AnimationSystem") — read animation code
```

### Step 2: Create/Modify Animations
```
1. multi_edit() — write animation scripts
2. execute_luau(code: [animation code], datamodel_type: "Client") — test client-side
3. start_stop_play(is_start: true) — play test
4. screen_capture() — verify motion
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Animation scripts | `code-implementer` |
| Motion design | `ui-ux-architect` |
| Visual verification | `screen_capture` + comparison |

## CODE PATTERNS

### TweenService Animation
```lua
local TweenService = game:GetService("TweenService")

local function tweenPart(part, properties, duration, style, direction)
    local tweenInfo = TweenInfo.new(
        duration or 1,
        style or Enum.EasingStyle.Quad,
        direction or Enum.EasingDirection.Out
    )
    local tween = TweenService:Create(part, tweenInfo, properties)
    tween:Play()
    return tween
end

-- Example: bounce effect
local function bounceEffect(part)
    local originalSize = part.Size
    tweenPart(part, { Size = originalSize * 1.2 }, 0.1, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    task.delay(0.1, function()
        tweenPart(part, { Size = originalSize }, 0.3, Enum.EasingStyle.Bounce, Enum.EasingDirection.Out)
    end)
end
```

### Procedural Bob Animation
```lua
local RunService = game:GetService("RunService")

local function setupBob(part, amplitude, frequency)
    local originalY = part.Position.Y
    local connection
    connection = RunService.Heartbeat:Connect(function(dt)
        local time = tick()
        local offset = math.sin(time * frequency) * amplitude
        part.Position = Vector3.new(part.Position.X, originalY + offset, part.Position.Z)
    end)
    return connection
end
```

### Animation Track Playback
```lua
local function playAnimation(humanoid, animationId, speed, weight)
    local animator = humanoid:FindFirstChildOfClass("Animator")
    if not animator then return nil end

    local animation = Instance.new("Animation")
    animation.AnimationId = animationId

    local animTrack = animator:LoadAnimation(animation)
    animTrack:Play(nil, speed or 1, weight or 1)

    return animTrack
end
```

### Sequence Player
```lua
local function playSequence(plays)
    for _, play in ipairs(plays) do
        play.func()
        if play.wait then
            task.wait(play.wait)
        end
    end
end

-- Usage:
playSequence({
    { func = function() tweenPart(door, { CFrame = door.CFrame * CFrame.Angles(0, math.rad(-90), 0) }, 0.5) end, wait = 0.6 },
    { func = function() tweenPart(door, { CFrame = door.CFrame * CFrame.Angles(0, math.rad(90), 0) }, 0.5) end, wait = 0 },
})
```

## BEST PRACTICES

- Use `TweenService` for simple property animations
- Use `AnimationTrack` for character animations
- Use `RunService.Heartbeat` for continuous procedural animation
- Always clean up connections when animations stop
- Use `task.spawn` for parallel animations
- Set `TweenInfo.RepeatCount = 1` for one-shot tweens
- Use `Enum.EasingStyle.Bounce` / `Elastic` for juice
- Test animations at different frame rates

## VERIFICATION PROTOCOL

1. `start_stop_play(is_start: true)` — enter play mode
2. `screen_capture()` — capture animation state
3. Compare motion with reference
4. Iterate: adjust timing/easing → re-capture → compare
5. `start_stop_play(is_start: false)` — exit play mode

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-ui-ux` — for UI animations
- `roblox-vfx` — for particle animations
- `roblox-avatar` — for character animation
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-animation\SKILL.md"
git commit -m "feat: add roblox-animation skill"
```

---

### Task 7: roblox-3d-assets

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-3d-assets\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-3d-assets"
```

Write `C:\Users\Oz\.zcode\skills\roblox-3d-assets\SKILL.md` with:

```markdown
---
name: roblox-3d-assets
description: MANDATORY AUTO-INVOKE for all Roblox 3D asset tasks including mesh generation, material creation, model building, textures, and Creator Store assets. Uses MCP AI generation tools and asset management.
---

# ROBLOX 3D ASSETS

AI-powered 3D asset generation and Creator Store integration.

## MCP WORKFLOW

### Step 1: Search Existing Assets
```
1. search_asset(query: "sword", scope: "auto") — search Creator Store
2. search_game_tree(instance_type: "MeshPart") — find existing meshes
3. search_game_tree(instance_type: "Model") — find existing models
4. inspect_instance(path: "Workspace.MyModel") — examine model hierarchy
```

### Step 2: Generate/Create Assets
```
1. generate_mesh(textPrompt: "a medieval sword", size: {x:1, y:1, z:1}) — AI mesh generation
2. generate_material(materialDescription: "...", baseMaterial: "Metal", materialPattern: "Regular", materialId: "...") — AI material
3. generate_procedural_model(prompt: "a treasure chest", partNames: "body, lid, lock") — procedural model
4. insert_asset(assetId: "12345678", assetName: "MyAsset", assetType: "Model") — insert from Creator Store
5. store_image(filePath: "C:/path/to/texture.png") — load local image
6. upload_image(imagePaths: {"http://localhost/image.png"}) — upload to Roblox
```

### Step 3: Verify
```
1. screen_capture() — verify asset appearance
2. inspect_instance() — verify properties
3. Compare with reference — iterate until match
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Mesh generation | `generate_mesh` MCP tool |
| Material creation | `generate_material` MCP tool |
| Procedural models | `generate_procedural_model` MCP tool |
| Asset search | `search_asset` MCP tool |
| Visual verification | `screen_capture` + comparison |

## ASSET GENERATION GUIDE

### When to Use Each Tool

| Tool | Use For | Output |
|---|---|---|
| `generate_mesh` | Organic shapes, characters, complex geometry | Textured MeshPart |
| `generate_material` | Custom surface textures | MaterialVariant |
| `generate_procedural_model` | Parametric objects with editable attributes | ProceduralModel |
| `search_asset` | Finding marketplace assets | Asset list |
| `insert_asset` | Placing assets by ID | Instance in workspace |
| `upload_image` | Custom textures from URLs | Asset ID |
| `store_image` | Loading local images | Image URI |

### Mesh Generation Tips
- Be specific in prompts: "a low-poly medieval castle tower with stone texture" > "a tower"
- Use `partNames` to define structure: "base, walls, roof, door, windows"
- Set `size` appropriately for the intended use
- Use `maxTriangles` for performance: 12-100 for simple, 1000+ for detailed

### Material Generation Tips
- Describe the surface: "worn metal with scratches and rust patches"
- Choose appropriate `baseMaterial`: Metal, Wood, Fabric, etc.
- Use `materialPattern`: Regular for uniform, Organic for natural variation

## BEST PRACTICES

- Start with `search_asset` before generating — someone may have already made it
- Use `generate_procedural_model` for objects with tunable parameters
- Use `generate_mesh` for unique organic shapes
- Always verify generated assets with `screen_capture`
- Set appropriate `size` for game scale
- Use `maxTriangles` to control mesh complexity
- Store local images with `store_image` before passing to `generate_procedural_model`

## CROSS-REFERENCES

- `roblox-vfx` — for visual effects using assets
- `roblox-terrain` — for world-building assets
- `roblox-avatar` — for character assets
- `roblox-asset-import` — for external asset pipeline
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-3d-assets\SKILL.md"
git commit -m "feat: add roblox-3d-assets skill"
```

---

### Task 8: roblox-terrain

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-terrain\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-terrain"
```

Write `C:\Users\Oz\.zcode\skills\roblox-terrain\SKILL.md` with:

```markdown
---
name: roblox-terrain
description: MANDATORY AUTO-INVOKE for all Roblox terrain, world-building, biomes, foliage, skybox, and environment design tasks. Uses MCP to create and verify terrain and world elements.
---

# ROBLOX TERRAIN

World-building, terrain generation, and environment design.

## MCP WORKFLOW

### Step 1: Analyze Current World
```
1. search_game_tree(path: "Workspace", instance_type: "Terrain") — find terrain
2. search_game_tree(path: "Workspace.Map") — explore map structure
3. inspect_instance(path: "Workspace.Terrain") — examine terrain
4. screen_capture() — capture current world state
```

### Step 2: Build World
```
1. generate_procedural_model(prompt: "...", partNames: "...") — generate world features
2. search_asset(query: "tree, grass, rock") — find environment assets
3. insert_asset(assetId: "...", assetName: "Tree") — place assets
4. execute_luau(code: [terrain code], datamodel_type: "Edit") — terrain manipulation
5. screen_capture() — verify world appearance
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Terrain generation | `code-implementer` |
| Asset placement | `generate_procedural_model` / `search_asset` |
| World verification | `screen_capture` + comparison |

## CODE PATTERNS

### Terrain Fill
```lua
local Terrain = workspace.Terrain

-- Fill a region with grass
local region = Region3.new(
    Vector3.new(-50, 0, -50),
    Vector3.new(50, 10, 50)
)
Terrain:FillRegion(region, 4, Enum.Material.Grass)
```

### Biome Generator
```lua
local biomes = {
    Forest = { material = Enum.Material.Grass, treeChance = 0.3 },
    Desert = { material = Enum.Material.Sand, treeChance = 0.01 },
    Snow = { material = Enum.Material.Ice, treeChance = 0.1 },
}

local function generateBiome(center, radius, biomeName)
    local biome = biomes[biomeName]
    if not biome then return end

    local region = Region3.new(
        center - Vector3.new(radius, 5, radius),
        center + Vector3.new(radius, 5, radius)
    )
    Terrain:FillRegion(region, 4, biome.material)
end
```

### Foliage Placement
```lua
local function placeFoliage(position, model, count)
    for i = 1, count do
        local offset = Vector3.new(
            math.random() * 20 - 10,
            0,
            math.random() * 20 - 10
        )
        local clone = model:Clone()
        clone:SetPrimaryPartCFrame(CFrame.new(position + offset))
        clone.Parent = workspace.Map
    end
end
```

### Skybox Setup
```lua
local Lighting = game:GetService("Lighting")

local function setupSkybox(skyboxId)
    local existing = Lighting:FindFirstChildOfClass("Sky")
    if existing then existing:Destroy() end

    local sky = Instance.new("Sky")
    sky.SkyboxBk = skyboxId
    sky.SkyboxDn = skyboxId
    sky.SkyboxFt = skyboxId
    sky.SkyboxLf = skyboxId
    sky.SkyboxRt = skyboxId
    sky.SkyboxUp = skyboxId
    sky.StarCount = 3000
    sky.Parent = Lighting
end
```

## VERIFICATION PROTOCOL

1. `screen_capture()` — capture before terrain changes
2. Execute terrain generation
3. `screen_capture()` — capture after
4. Compare with reference image
5. Iterate: adjust materials/positions → re-capture → compare

## BEST PRACTICES

- Use `Region3` for bulk terrain operations
- Combine terrain materials with placed models for realism
- Use `FillWedge` for natural-looking slopes
- Keep terrain resolution consistent (4 is default)
- Use `Debris:AddItem()` for temporary terrain features
- Test world at different camera distances

## CROSS-REFERENCES

- `roblox-3d-assets` — for meshes and materials
- `roblox-vfx` — for environmental effects
- `roblox-performance` — for world streaming
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-terrain\SKILL.md"
git commit -m "feat: add roblox-terrain skill"
```

---

## Batch 3: Audio & Specialized Skills

### Task 9: roblox-audio

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-audio\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-audio"
```

Write `C:\Users\Oz\.zcode\skills\roblox-audio\SKILL.md` with:

```markdown
---
name: roblox-audio
description: MANDATORY AUTO-INVOKE for all Roblox audio, sound, music, 3D spatial audio, SFX, audio zones, and ambient sound tasks. Uses MCP to search, insert, and configure audio assets.
---

# ROBLOX AUDIO

Sound design, music, and 3D audio with MCP integration.

## MCP WORKFLOW

### Step 1: Find Audio Assets
```
1. search_asset(query: "battle music", assetType: "Audio", scope: "auto") — search Creator Store
2. search_game_tree(instance_type: "Sound") — find existing sounds
3. inspect_instance(path: "Workspace.AudioManager") — examine audio setup
```

### Step 2: Insert and Configure
```
1. insert_asset(assetId: "12345678", assetName: "BGMusic", assetType: "Audio") — insert audio
2. execute_luau(code: [audio setup code], datamodel_type: "Edit") — configure audio
3. execute_luau(code: [play code], datamodel_type: "Client") — test playback
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Audio search | `search_asset` MCP tool |
| Audio scripts | `code-implementer` |
| Audio verification | `execute_luau` + `get_console_output` |

## CODE PATTERNS

### Background Music Manager
```lua
local SoundService = game:GetService("SoundService")

local MusicManager = {}
local currentTrack = nil

function MusicManager:PlayTrack(soundId, volume, fadeTime)
    if currentTrack then
        self:FadeOut(currentTrack, fadeTime or 1)
    end

    local sound = Instance.new("Sound")
    sound.SoundId = soundId
    sound.Volume = 0
    sound.Looped = true
    sound.Parent = SoundService
    sound:Play()

    self:FadeIn(sound, volume or 0.5, fadeTime or 1)
    currentTrack = sound
    return sound
end

function MusicManager:FadeIn(sound, targetVolume, duration)
    local tweenService = game:GetService("TweenService")
    local tween = tweenService:Create(sound, TweenInfo.new(duration), { Volume = targetVolume })
    tween:Play()
end

function MusicManager:FadeOut(sound, duration)
    local tweenService = game:GetService("TweenService")
    local tween = tweenService:Create(sound, TweenInfo.new(duration), { Volume = 0 })
    tween:Play()
    tween.Completed:Connect(function()
        sound:Stop()
        sound:Destroy()
    end)
end

return MusicManager
```

### 3D Spatial Audio
```lua
local function setup3DAudio(part, soundId, maxDistance, rollOff)
    local sound = Instance.new("Sound")
    sound.SoundId = soundId
    sound.RollOffMode = Enum.RollOffMode.Linear
    sound.RollOffMaxDistance = maxDistance or 50
    sound.RollOffMinDistance = 5
    sound.Parent = part
    sound:Play()
    return sound
end
```

### Audio Zone
```lua
local function createAudioZone(parts, enterSound, exitSound, bgMusic)
    local playersInZone = {}

    for _, part in ipairs(parts) do
        part.Touched:Connect(function(hit)
            local player = game:GetService("Players"):GetPlayerFromCharacter(hit.Parent)
            if player and not playersInZone[player.UserId] then
                playersInZone[player.UserId] = true
                if enterSound then enterSound:Play() end
                if bgMusic then bgMusic:Play() end
            end
        end)

        part.TouchEnded:Connect(function(hit)
            local player = game:GetService("Players"):GetPlayerFromCharacter(hit.Parent)
            if player and playersInZone[player.UserId] then
                playersInZone[player.UserId] = nil
                if exitSound then exitSound:Play() end
                if bgMusic then bgMusic:Stop() end
            end
        end)
    end
end
```

## BEST PRACTICS

- Use `SoundService` for global sounds (music, UI sounds)
- Use `Part.Sound` for 3D spatial audio
- Always set `RollOffMaxDistance` for 3D sounds
- Use `Looped = true` for background music
- Fade in/out music for smooth transitions
- Pool frequently-played sounds
- Test audio at different listener positions

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-asset-import` — for importing custom audio
- `roblox-tools-workflow` — for testing audio
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-audio\SKILL.md"
git commit -m "feat: add roblox-audio skill"
```

---

### Task 10: roblox-avatar

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-avatar\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-avatar"
```

Write `C:\Users\Oz\.zcode\skills\roblox-avatar\SKILL.md` with:

```markdown
---
name: roblox-avatar
description: MANDATORY AUTO-INVOKE for all Roblox avatar, character customization, body parts, clothing, accessories, R15/R6 rigging, and HumanoidDescription tasks. Uses MCP to modify and verify character appearance.
---

# ROBLOX AVATAR

Character customization, body modification, and appearance systems.

## MCP WORKFLOW

### Step 1: Analyze Character
```
1. search_game_tree(path: "Workspace", keywords: "character, humanoid") — find characters
2. inspect_instance(path: "Workspace.Character.Humanoid") — examine humanoid
3. script_grep("HumanoidDescription") — find customization code
4. script_grep("ShirtGraphic, Pants") — find clothing code
```

### Step 2: Modify Avatar
```
1. execute_luau(code: [avatar code], datamodel_type: "Client") — apply customization
2. search_asset(query: "sword, hat", assetType: "Package") — find accessories
3. insert_asset(assetId: "...", assetName: "Accessory", assetType: "Package") — add items
4. screen_capture() — verify appearance
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Avatar scripts | `code-implementer` |
| Asset search | `search_asset` MCP tool |
| Visual verification | `screen_capture` + comparison |

## CODE PATTERNS

### HumanoidDescription Setup
```lua
local function applyAvatar(humanoid, description)
    humanoid:ApplyDescription(description)
end

-- Create custom description
local function createCustomDescription()
    local desc = Instance.new("HumanoidDescription")

    -- Body colors
    desc.HeadColor3 = Color3.fromRGB(245, 205, 170)
    desc.LeftArmColor3 = Color3.fromRGB(245, 205, 170)
    desc.LeftLegColor3 = Color3.fromRGB(30, 30, 30)
    desc.RightArmColor3 = Color3.fromRGB(245, 205, 170)
    desc.RightLegColor3 = Color3.fromRGB(30, 30, 30)
    desc.TorsoColor3 = Color3.fromRGB(30, 100, 200)

    -- Scale
    desc.HeightScale = 1
    desc.WidthScale = 1
    desc.HeadScale = 1

    return desc
end
```

### Accessory Management
```lua
local function addAccessory(character, accessoryId)
    local accessory = game:GetService("InsertService"):LoadAsset(accessoryId)
    if accessory then
        local handle = accessory:FindFirstChild("Handle")
        if handle then
            local att = Instance.new("Attachment")
            att.Name = "AccessoryAttachment"
            att.Parent = character:FindFirstChild("Head") or character:FindFirstChild("UpperTorso")
            handle:FindFirstChildOfClass("Weld"):Destroy()
            local weld = Instance.new("Weld")
            weld.Part0 = att.Parent
            weld.Part1 = handle
            weld.C0 = att.CFrame
            handle.Parent = character
        end
    end
end
```

### Outfit System
```lua
local Outfits = {
    Warrior = {
        Shirt = "rbxassetid://12345678",
        Pants = "rbxassetid://12345679",
        Accessories = { 12345680 },
    },
    Mage = {
        Shirt = "rbxassetid://12345681",
        Pants = "rbxassetid://12345682",
        Accessories = { 12345683 },
    },
}

local function applyOutfit(character, outfitName)
    local outfit = Outfits[outfitName]
    if not outfit then return end

    -- Remove existing clothing
    for _, item in ipairs(character:GetChildren()) do
        if item:IsA("Shirt") or item:IsA("Pants") or item:IsA("ShirtGraphic") then
            item:Destroy()
        end
    end

    -- Apply new clothing
    if outfit.Shirt then
        local shirt = Instance.new("Shirt")
        shirt.ShirtTemplate = outfit.Shirt
        shirt.Parent = character
    end
    if outfit.Pants then
        local pants = Instance.new("Pants")
        pants.PantsTemplate = outfit.Pants
        pants.Parent = character
    end
end
```

## BEST PRACTICES

- Use `HumanoidDescription` for bulk avatar changes
- Test with both R15 and R6 rigs
- Use `ApplyDescription` for safe avatar modification
- Clean up old accessories before adding new ones
- Use `InsertService:LoadAsset` for dynamic accessory loading
- Verify avatar changes with `screen_capture`

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-3d-assets` — for custom meshes
- `roblox-animation` — for character animation
- `roblox-asset-import` — for importing avatar assets
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-avatar\SKILL.md"
git commit -m "feat: add roblox-avatar skill"
```

---

### Task 11: roblox-cinematics

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-cinematics\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-cinematics"
```

Write `C:\Users\Oz\.zcode\skills\roblox-cinematics\SKILL.md` with:

```markdown
---
name: roblox-cinematics
description: MANDATORY AUTO-INVOKE for all Roblox cutscenes, camera paths, dialogue systems, cinematic sequences, letterboxing, and camera effects tasks. Uses MCP to create, test, and verify cinematic experiences.
---

# ROBLOX CINEMATICS

Cutscenes, camera work, and cinematic storytelling.

## MCP WORKFLOW

### Step 1: Plan Cinematic
```
1. search_game_tree(path: "Workspace.Cutscenes") — find existing cutscenes
2. script_grep("Camera") — find camera-related code
3. inspect_instance(path: "Workspace.Camera") — examine camera
```

### Step 2: Create Cinematic
```
1. multi_edit() — write cutscene scripts
2. execute_luau(code: [camera code], datamodel_type: "Client") — test camera
3. start_stop_play(is_start: true) — play test
4. screen_capture() — verify cinematic output
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Cutscene scripts | `code-implementer` |
| Camera design | `ui-ux-architect` |
| Visual verification | `screen_capture` + comparison |

## CODE PATTERNS

### Camera Path
```lua
local TweenService = game:GetService("TweenService")

local function moveCamera(camera, cframes, durations)
    for i, cframe in ipairs(cframes) do
        local duration = durations[i] or 1
        local tween = TweenService:Create(
            camera,
            TweenInfo.new(duration, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut),
            { CFrame = cframe }
        )
        tween:Play()
        tween.Completed:Wait()
    end
end

-- Usage:
moveCamera(workspace.CurrentCamera, {
    CFrame.new(0, 10, -20) * CFrame.Angles(0, 0, 0),  -- Wide shot
    CFrame.new(0, 5, 0) * CFrame.Angles(0, 0, 0),     -- Close up
    CFrame.new(10, 8, -10) * CFrame.Angles(0, -45, 0), -- Side angle
}, { 2, 1.5, 2 })
```

### Letterbox Effect
```lua
local function showLetterbox(playerGui, duration)
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "Letterbox"
    screenGui.Parent = playerGui

    local topBar = Instance.new("Frame")
    topBar.Size = UDim2.new(1, 0, 0.12, 0)
    topBar.Position = UDim2.new(0, 0, 0, 0)
    topBar.BackgroundColor3 = Color3.new(0, 0, 0)
    topBar.Parent = screenGui

    local bottomBar = Instance.new("Frame")
    bottomBar.Size = UDim2.new(1, 0, 0.12, 0)
    bottomBar.Position = UDim2.new(0, 0, 0.88, 0)
    bottomBar.BackgroundColor3 = Color3.new(0, 0, 0)
    bottomBar.Parent = screenGui

    if duration then
        task.delay(duration, function()
            screenGui:Destroy()
        end)
    end

    return screenGui
end
```

### Fade Transition
```lua
local function fadeToBlack(playerGui, duration)
    local screenGui = Instance.new("ScreenGui")
    screenGui.Parent = playerGui

    local overlay = Instance.new("Frame")
    overlay.Size = UDim2.new(1, 0, 1, 0)
    overlay.BackgroundColor3 = Color3.new(0, 0, 0)
    overlay.BackgroundTransparency = 1
    overlay.Parent = screenGui

    local tween = game:GetService("TweenService"):Create(
        overlay,
        TweenInfo.new(duration or 1),
        { BackgroundTransparency = 0 }
    )
    tween:Play()
    tween.Completed:Wait()

    return screenGui, overlay
end
```

### Dialogue Box
```lua
local function showDialogue(playerGui, speaker, text, duration)
    local screenGui = Instance.new("ScreenGui")
    screenGui.Parent = playerGui

    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(0.6, 0, 0.15, 0)
    frame.Position = UDim2.new(0.2, 0, 0.8, 0)
    frame.BackgroundColor3 = Color3.fromRGB(20, 20, 30)
    frame.BackgroundTransparency = 0.1
    frame.Parent = screenGui

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 8)
    corner.Parent = frame

    local speakerLabel = Instance.new("TextLabel")
    speakerLabel.Size = UDim2.new(1, -20, 0.3, 0)
    speakerLabel.Position = UDim2.new(0, 10, 0, 5)
    speakerLabel.Text = speaker
    speakerLabel.TextColor3 = Color3.fromRGB(100, 200, 255)
    speakerLabel.TextXAlignment = Enum.TextXAlignment.Left
    speakerLabel.BackgroundTransparency = 1
    speakerLabel.Parent = frame

    local textLabel = Instance.new("TextLabel")
    textLabel.Size = UDim2.new(1, -20, 0.6, 0)
    textLabel.Position = UDim2.new(0, 10, 0.35, 0)
    textLabel.Text = text
    textLabel.TextColor3 = Color3.new(1, 1, 1)
    textLabel.TextXAlignment = Enum.TextXAlignment.Left
    textLabel.TextWrapped = true
    textLabel.BackgroundTransparency = 1
    textLabel.Parent = frame

    if duration then
        task.delay(duration, function()
            screenGui:Destroy()
        end)
    end

    return screenGui
end
```

## BEST PRACTICES

- Use `TweenService` for smooth camera movements
- Disable player controls during cutscenes
- Use `workspace.CurrentCamera` for camera manipulation
- Add letterbox bars for cinematic feel
- Use `FadeToBlack` for scene transitions
- Clean up all UI elements after cutscene ends
- Test cutscenes at different frame rates

## CROSS-REFERENCES

- `roblox-animation` — for camera animation
- `roblox-ui-ux` — for dialogue UI
- `roblox-audio` — for cutscene music/SFX
- `roblox-tools-workflow` — for playtesting
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-cinematics\SKILL.md"
git commit -m "feat: add roblox-cinematics skill"
```

---

### Task 12: roblox-economy

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-economy\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-economy"
```

Write `C:\Users\Oz\.zcode\skills\roblox-economy\SKILL.md` with:

```markdown
---
name: roblox-economy
description: MANDATORY AUTO-INVOKE for all Roblox monetization, DevProducts, GamePasses, leaderboards, currency systems, and in-game economy tasks. Uses MCP to implement and verify economy systems.
---

# ROBLOX ECONOMY

Monetization, currency systems, and in-game economy.

## MCP WORKFLOW

### Step 1: Analyze Current Economy
```
1. script_grep("MarketplaceService") — find monetization code
2. script_grep("leaderstats") — find leaderboard code
3. script_grep("DataStore") — find data persistence
4. script_read("game.ServerScriptService.Economy") — read economy scripts
```

### Step 2: Implement Economy
```
1. multi_edit() — write economy scripts
2. execute_luau(code: [economy code], datamodel_type: "Server") — test server-side
3. execute_luau(code: [client code], datamodel_type: "Client") — test client UI
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Economy scripts | `code-implementer` |
| Data persistence | `roblox-data-persistence` |
| Security review | `red-team-qa` |

## CODE PATTERNS

### MarketplaceService Integration
```lua
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

-- Product IDs (replace with your actual IDs)
local PRODUCTS = {
    COINS_100 = 12345678,
    COINS_500 = 12345679,
    VIP_PASS = 12345680,
}

MarketplaceService.ProcessReceipt = function(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    local productId = receiptInfo.ProductId

    if productId == PRODUCTS.COINS_100 then
        -- Add 100 coins
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            leaderstats.Coins.Value += 100
        end
    elseif productId == PRODUCTS.COINS_500 then
        -- Add 500 coins
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            leaderstats.Coins.Value += 500
        end
    end

    return Enum.ProductPurchaseDecision.PurchaseGranted
end
```

### GamePass Check
```lua
local MarketplaceService = game:GetService("MarketplaceService")

local function hasGamePass(player, gamePassId)
    local success, hasPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, gamePassId)
    end)
    return success and hasPass
end

-- Usage:
if hasGamePass(player, 12345680) then
    -- Grant VIP benefits
end
```

### Leaderboard System
```lua
local function setupLeaderboard(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = leaderstats

    local level = Instance.new("IntValue")
    level.Name = "Level"
    level.Value = 1
    level.Parent = leaderstats
end
```

### Currency Manager
```lua
local CurrencyManager = {}

function CurrencyManager:AddCoins(player, amount)
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats and leaderstats:FindFirstChild("Coins") then
        leaderstats.Coins.Value += amount
        return true
    end
    return false
end

function CurrencyManager:RemoveCoins(player, amount)
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats and leaderstats:FindFirstChild("Coins") then
        if leaderstats.Coins.Value >= amount then
            leaderstats.Coins.Value -= amount
            return true
        end
    end
    return false
end

function CurrencyManager:GetCoins(player)
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats and leaderstats:FindFirstChild("Coins") then
        return leaderstats.Coins.Value
    end
    return 0
end

return CurrencyManager
```

## BEST PRACTICS

- Always validate purchases server-side
- Use `pcall` for MarketplaceService calls
- Store purchase receipts for debugging
- Implement anti-exploit for currency changes
- Use leaderstats for visible currency
- Save currency data with DataStore
- Test with mock products before publishing

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-data-persistence` — for saving currency
- `roblox-security` — for purchase validation
- `roblox-ui-ux` — for shop UI
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-economy\SKILL.md"
git commit -m "feat: add roblox-economy skill"
```

---

## Batch 4: Systems Skills

### Task 13: roblox-networking

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-networking\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-networking"
```

Write `C:\Users\Oz\.zcode\skills\roblox-networking\SKILL.md` with:

```markdown
---
name: roblox-networking
description: MANDATORY AUTO-INVOKE for all Roblox RemoteEvents, RemoteFunctions, replication, client-server communication, and networking tasks. Uses MCP to implement, audit, and verify networking code.
---

# ROBLOX NETWORKING

Client-server communication, replication, and networking patterns.

## MCP WORKFLOW

### Step 1: Audit Existing Networking
```
1. script_grep("RemoteEvent") — find all RemoteEvents
2. script_grep("RemoteFunction") — find all RemoteFunctions
3. script_grep("OnServerEvent") — find server event handlers
4. script_grep("FireServer") — find client fire calls
5. script_grep("OnClientEvent") — find client event handlers
6. script_grep("FireClient") — find server fire calls
```

### Step 2: Implement Networking
```
1. multi_edit() — write networking code
2. execute_luau(code: [server code], datamodel_type: "Server") — test server
3. execute_luau(code: [client code], datamodel_type: "Client") — test client
4. get_console_output() — check for replication errors
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Networking code | `code-implementer` |
| Security audit | `red-team-qa` |
| Performance check | `performance-engineer` |

## CODE PATTERNS

### RemoteEvent Wrapper (Server)
```lua
-- ReplicatedStorage.Modules.NetworkManager
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local NetworkManager = {}
local events = {}

function NetworkManager:CreateEvent(name)
    local event = Instance.new("RemoteEvent")
    event.Name = name
    event.Parent = ReplicatedStorage.Events
    events[name] = event
    return event
end

function NetworkManager:ListenToClient(name, callback)
    local event = events[name] or ReplicatedStorage.Events:WaitForChild(name)
    event.OnServerEvent:Connect(function(player, ...)
        -- Validate input here
        callback(player, ...)
    end)
end

function NetworkManager:FireClient(player, name, ...)
    local event = events[name] or ReplicatedStorage.Events:WaitForChild(name)
    event:FireClient(player, ...)
end

function NetworkManager:FireAllClients(name, ...)
    local event = events[name] or ReplicatedStorage.Events:WaitForChild(name)
    event:FireAllClients(...)
end

return NetworkManager
```

### RemoteEvent Wrapper (Client)
```lua
-- StarterPlayerScripts.Modules.NetworkManager
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local NetworkManager = {}
local events = {}

function NetworkManager:ListenToServer(name, callback)
    local event = ReplicatedStorage.Events:WaitForChild(name)
    event.OnClientEvent:Connect(callback)
end

function NetworkManager:FireServer(name, ...)
    local event = ReplicatedStorage.Events:WaitForChild(name)
    event:FireServer(...)
end

return NetworkManager
```

### Request-Response Pattern
```lua
-- Server: Handle request
local function handleRequest(player, requestData)
    -- Validate
    if type(requestData) ~= "table" then return end

    -- Process
    local result = processRequest(player, requestData)

    -- Respond
    NetworkManager:FireClient(player, "RequestResponse", result)
end

-- Client: Send request and wait for response
local function sendRequest(requestData)
    local response = nil
    local received = false

    NetworkManager:ListenToServer("RequestResponse", function(result)
        response = result
        received = true
    end)

    NetworkManager:FireServer("PlayerRequest", requestData)

    -- Wait for response with timeout
    local timeout = 5
    local elapsed = 0
    while not received and elapsed < timeout do
        task.wait(0.1)
        elapsed += 0.1
    end

    return response
end
```

### Rate Limiter
```lua
local RateLimiter = {}
RateLimiter.__index = RateLimiter

function RateLimiter.new(maxRequests, windowSeconds)
    return setmetatable({
        maxRequests = maxRequests or 10,
        windowSeconds = windowSeconds or 1,
        requests = {},
    }, RateLimiter)
end

function RateLimiter:Check(userId)
    local now = tick()
    if not self.requests[userId] then
        self.requests[userId] = {}
    end

    -- Remove old requests
    local valid = {}
    for _, t in ipairs(self.requests[userId]) do
        if now - t < self.windowSeconds then
            table.insert(valid, t)
        end
    end
    self.requests[userId] = valid

    if #valid >= self.maxRequests then
        return false -- Rate limited
    end

    table.insert(self.requests[userId], now)
    return true
end

return RateLimiter
```

## BEST PRACTICS

- Always validate client input on server
- Use wrapper modules for RemoteEvents
- Implement rate limiting for player actions
- Never trust client data — treat as untrusted
- Use RemoteFunctions sparingly (they yield)
- Group related events under a folder
- Name events clearly: "PlayerAction", "GameStateUpdate"

## VERIFICATION PROTOCOL

1. `execute_luau` in Server context — test server handlers
2. `execute_luau` in Client context — test client fire
3. `get_console_output()` — check for replication errors
4. `red-team-qa` review for security issues

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-security` — for input validation
- `roblox-performance` — for replication optimization
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-networking\SKILL.md"
git commit -m "feat: add roblox-networking skill"
```

---

### Task 14: roblox-security

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-security\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-security"
```

Write `C:\Users\Oz\.zcode\skills\roblox-security\SKILL.md` with:

```markdown
---
name: roblox-security
description: MANDATORY AUTO-INVOKE for all Roblox anti-exploit, server authority, input validation, security hardening, and vulnerability assessment tasks. Uses MCP to audit and secure game code.
---

# ROBLOX SECURITY

Anti-exploit, server authority, and security hardening.

## MCP WORKFLOW

### Step 1: Security Audit
```
1. script_grep("FireServer") — find all client-to-server calls (attack surface)
2. script_grep("Value") — find exploitable Value objects
3. script_grep("RemoteEvent") — audit all remote events
4. script_grep("require") — check for module injection
5. script_read() — read each suspicious script
```

### Step 2: Harden
```
1. multi_edit() — add validation and anti-exploit measures
2. execute_luau(code: [security code], datamodel_type: "Server") — test defenses
3. red-team-qa review — verify security
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Security audit | `red-team-qa` |
| Code hardening | `code-implementer` |
| Penetration testing | `cybersecurity-specialist` |

## CODE PATTERNS

### Server Authority Validation
```lua
-- NEVER trust client input
RemoteEvent.OnServerEvent:Connect(function(player, action, data)
    -- Validate action type
    if type(action) ~= "string" then
        warn("Invalid action from " .. player.Name)
        return
    end

    -- Validate data
    if type(data) ~= "table" then
        warn("Invalid data from " .. player.Name)
        return
    end

    -- Validate specific fields
    if data.amount and (type(data.amount) ~= "number" or data.amount < 0 or data.amount > 1000) then
        warn("Invalid amount from " .. player.Name)
        return
    end

    -- Process validated action
    processAction(player, action, data)
end)
```

### Anti-Exploit Monitor
```lua
local AntiExploit = {}
local violations = {}

function AntiExploit:LogViolation(player, violationType, details)
    if not violations[player.UserId] then
        violations[player.UserId] = {
            count = 0,
            firstViolation = tick(),
        }
    end

    violations[player.UserId].count += 1
    violations[player.UserId].lastViolation = tick()

    warn(string.format("[ANTI-EXPLOIT] %s: %s - %s", player.Name, violationType, details))

    -- Auto-kick after 5 violations
    if violations[player.UserId].count >= 5 then
        player:Kick("Suspicious activity detected")
    end
end

function AntiExploit:CheckSpeed(player, maxSpeed)
    local character = player.Character
    if not character then return end

    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    if humanoid.WalkSpeed > maxSpeed then
        self:LogViolation(player, "Speed", "WalkSpeed: " .. humanoid.WalkSpeed)
        humanoid.WalkSpeed = 16 -- Reset to default
    end
end

return AntiExploit
```

### Input Sanitization
```lua
local Sanitizer = {}

function Sanitizer:String(input, maxLength)
    if type(input) ~= "string" then return "" end
    return string.sub(input, 1, maxLength or 100):gsub("[^%w%s%-_]", "")
end

function Sanitizer:Number(input, min, max)
    if type(input) ~= "number" then return min or 0 end
    return math.clamp(input, min or -math.huge, max or math.huge)
end

function Sanitizer:Table(input, allowedKeys)
    if type(input) ~= "table" then return {} end
    local cleaned = {}
    for k, v in pairs(input) do
        if allowedKeys and allowedKeys[k] then
            cleaned[k] = v
        end
    end
    return cleaned
end

return Sanitizer
```

### Rate Limiter (Server-Side)
```lua
local ServerRateLimiter = {}
local playerRequests = {}

function ServerRateLimiter:Check(player, action, maxPerSecond)
    local key = player.UserId .. "_" .. action
    local now = tick()

    if not playerRequests[key] then
        playerRequests[key] = {}
    end

    -- Remove old entries
    local valid = {}
    for _, t in ipairs(playerRequests[key]) do
        if now - t < 1 then
            table.insert(valid, t)
        end
    end
    playerRequests[key] = valid

    if #valid >= (maxPerSecond or 10) then
        return false
    end

    table.insert(playerRequests[key], now)
    return true
end

return ServerRateLimiter
```

## BEST PRACTICES

- Always validate input on server
- Use server authority for all game logic
- Implement rate limiting on all remote events
- Log suspicious activity
- Never expose admin commands to clients
- Use unique RemoteEvent names per feature
- Clean up player data on disconnect
- Test with simulated exploits

## VERIFICATION PROTOCOL

1. `script_grep` audit — find all attack surfaces
2. `red-team-qa` review — adversarial testing
3. `execute_luau` in Client context — test exploit attempts
4. Verify server rejects invalid input

## CROSS-REFERENCES

- `roblox-networking` — for RemoteEvent patterns
- `roblox-coding` — for Luau patterns
- `roblox-data-persistence` — for data security
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-security\SKILL.md"
git commit -m "feat: add roblox-security skill"
```

---

### Task 14: roblox-performance

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-performance\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-performance"
```

Write `C:\Users\Oz\.zcode\skills\roblox-performance\SKILL.md` with:

```markdown
---
name: roblox-performance
description: MANDATORY AUTO-INVOKE for all Roblox performance optimization, profiling, memory management, streaming, frame rate, and efficiency tasks. Uses MCP to profile, optimize, and verify performance improvements.
---

# ROBLOX PERFORMANCE

Profiling, optimization, and memory management.

## MCP WORKFLOW

### Step 1: Profile
```
1. execute_luau(code: "print(collectgarbage('count'))", datamodel_type: "Client") — check memory
2. get_console_output() — check for performance warnings
3. script_grep("while true") — find potential infinite loops
4. script_grep("wait(") — find blocking waits
5. search_game_tree(instance_type: "ParticleEmitter") — count particles
```

### Step 2: Optimize
```
1. multi_edit() — optimize code
2. execute_luau(code: [optimized code], datamodel_type: "Client") — test
3. get_console_output() — verify improvements
4. screen_capture() — verify visual quality maintained
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Performance analysis | `performance-engineer` |
| Code optimization | `code-implementer` |
| Memory profiling | `execute_luau` + `get_console_output` |

## CODE PATTERNS

### Object Pool
```lua
local ObjectPool = {}
ObjectPool.__index = ObjectPool

function ObjectPool.new(template, initialSize)
    local pool = setmetatable({
        template = template,
        available = {},
        active = {},
    }, ObjectPool)

    for i = 1, initialSize or 10 do
        local obj = template:Clone()
        obj.Parent = nil
        table.insert(pool.available, obj)
    end

    return pool
end

function ObjectPool:Get()
    local obj
    if #self.available > 0 then
        obj = table.remove(self.available)
    else
        obj = self.template:Clone()
    end
    table.insert(self.active, obj)
    return obj
end

function ObjectPool:Return(obj)
    for i, v in ipairs(self.active) do
        if v == obj then
            table.remove(self.active, i)
            break
        end
    end
    obj.Parent = nil
    table.insert(self.available, obj)
end

return ObjectPool
```

### Connection Cleaner
```lua
local ConnectionManager = {}
local connections = {}

function ConnectionManager:Add(connection)
    table.insert(connections, connection)
    return connection
end

function ConnectionManager:Clean()
    for _, conn in ipairs(connections) do
        if conn.Connected then
            conn:Disconnect()
        end
    end
    connections = {}
end

return ConnectionManager
```

### Batch Processing
```lua
local function batchProcess(items, processFunc, batchSize, yieldBetweenBatches)
    batchSize = batchSize or 100
    for i = 1, #items, batchSize do
        local batch = {}
        for j = i, math.min(i + batchSize - 1, #items) do
            table.insert(batch, items[j])
        end
        processFunc(batch)
        if yieldBetweenBatches then
            task.wait()
        end
    end
end
```

### Memory Monitor
```lua
local function monitorMemory(interval)
    interval = interval or 5
    while true do
        local mem = collectgarbage("count")
        print(string.format("[MEMORY] Current: %.2f KB", mem))
        task.wait(interval)
    end
end
```

## BEST PRACTICES

- Use object pooling for frequently created/destroyed objects
- Clean up connections when no longer needed
- Use `task.spawn` / `task.delay` over `spawn` / `delay`
- Batch operations to spread across frames
- Monitor memory usage during development
- Use `StreamingEnabled` for large worlds
- Minimize use of `:WaitForChild()` in hot paths
- Profile before optimizing — measure, don't guess

## VERIFICATION PROTOCOL

1. `execute_luau` — measure memory before/after
2. `get_console_output()` — check for warnings
3. `screen_capture()` — verify visual quality maintained
4. Compare frame rates if possible

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-terrain` — for streaming optimization
- `roblox-vfx` — for particle optimization
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-performance\SKILL.md"
git commit -m "feat: add roblox-performance skill"
```

---

### Task 15: roblox-data-persistence

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-data-persistence\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-data-persistence"
```

Write `C:\Users\Oz\.zcode\skills\roblox-data-persistence\SKILL.md` with:

```markdown
---
name: roblox-data-persistence
description: MANDATORY AUTO-INVOKE for all Roblox DataStore, saving/loading, data migration, leaderboards, session locking, and persistence tasks. Uses MCP to implement and verify data systems.
---

# ROBLOX DATA PERSISTENCE

DataStore patterns, saving/loading, and data migration.

## MCP WORKFLOW

### Step 1: Audit Existing Data
```
1. script_grep("DataStoreService") — find DataStore usage
2. script_grep("GetDataStore") — find DataStore instances
3. script_grep("GetAsync") — find read operations
4. script_grep("SetAsync") — find write operations
5. script_read() — read data scripts
```

### Step 2: Implement/Modify
```
1. multi_edit() — write data persistence code
2. execute_luau(code: [data code], datamodel_type: "Server") — test save/load
3. get_console_output() — check for DataStore errors
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Data scripts | `code-implementer` |
| Security review | `red-team-qa` |
| Data migration | `data-engineer` |

## CODE PATTERNS

### DataStore Wrapper
```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local DataStoreWrapper = {}
DataStoreWrapper.__index = DataStoreWrapper

function DataStoreWrapper.new(dataStoreName, version)
    local storeName = dataStoreName .. "_v" .. (version or 1)
    return setmetatable({
        store = DataStoreService:GetDataStore(storeName),
        cache = {},
    }, DataStoreWrapper)
end

function DataStoreWrapper:GetAsync(key)
    if self.cache[key] then
        return self.cache[key]
    end

    local success, data = pcall(function()
        return self.store:GetAsync(key)
    end)

    if success then
        self.cache[key] = data
    end

    return success and data or nil
end

function DataStoreWrapper:SetAsync(key, value)
    local success, err = pcall(function()
        self.store:SetAsync(key, value)
    end)

    if success then
        self.cache[key] = value
    end

    return success, err
end

function DataStoreWrapper:UpdateAsync(key, transformFunc)
    local success, data = pcall(function()
        return self.store:UpdateAsync(key, transformFunc)
    end)

    if success then
        self.cache[key] = data
    end

    return success, data
end

return DataStoreWrapper
```

### Session Lock
```lua
local SessionLocks = {}

function SessionLocks:Acquire(player)
    local key = "session_" .. player.UserId
    local success = pcall(function()
        -- Try to set a session lock
        local store = DataStoreService:GetDataStore("SessionLocks")
        store:SetAsync(key, {
            locked = true,
            timestamp = tick(),
        })
    end)
    return success
end

function SessionLocks:Release(player)
    local key = "session_" .. player.UserId
    pcall(function()
        local store = DataStoreService:GetDataStore("SessionLocks")
        store:RemoveAsync(key)
    end)
end

function SessionLocks:IsLocked(player)
    local key = "session_" .. player.UserId
    local success, data = pcall(function()
        local store = DataStoreService:GetDataStore("SessionLocks")
        return store:GetAsync(key)
    end)

    if success and data and data.locked then
        -- Check for stale lock (older than 5 minutes)
        if tick() - (data.timestamp or 0) > 300 then
            self:Release(player)
            return false
        end
        return true
    end

    return false
end

return SessionLocks
```

### Auto-Save
```lua
local AutoSave = {}
local playerData = {}

function AutoSave:Track(player, data)
    playerData[player.UserId] = data
end

function AutoSave:Start(interval)
    interval = interval or 120 -- 2 minutes

    while true do
        task.wait(interval)
        for userId, data in pairs(playerData) do
            local player = Players:GetPlayerByUserId(userId)
            if player then
                -- Save data
                pcall(function()
                    local store = DataStoreService:GetDataStore("PlayerData")
                    store:SetAsync("player_" .. userId, data)
                end)
            end
        end
    end
end

function AutoSave:Stop(player)
    playerData[player.UserId] = nil
end

return AutoSave
```

### Data Migration
```lua
local DataMigrator = {}

function DataMigrator:Migrate(oldStoreName, newStoreName, transformFunc)
    local oldStore = DataStoreService:GetDataStore(oldStoreName)
    local newStore = DataStoreService:GetDataStore(newStoreName)

    -- Note: This is simplified. Real migration requires pagination
    local success, pages = pcall(function()
        return oldStore:GetSortedAsync(false, 100)
    end)

    if not success then return end

    for _, key in ipairs(pages:GetCurrentPage()) do
        local data = oldStore:GetAsync(key)
        if data then
            local newData = transformFunc(data)
            newStore:SetAsync(key, newData)
        end
    end
end

return DataMigrator
```

## BEST PRACTICES

- Always use `pcall` for DataStore operations
- Implement session locking for critical data
- Auto-save periodically (every 2 minutes)
- Use versioned DataStore names for migrations
- Cache data in memory for fast access
- Handle DataStore throttling with retry logic
- Never expose DataStore keys to clients
- Test with mock data before publishing

## VERIFICATION PROTOCOL

1. `execute_luau` in Server context — test save/load cycle
2. `get_console_output()` — check for DataStore errors
3. Verify data persists across play sessions
4. Test with multiple players

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-security` — for data security
- `roblox-economy` — for currency persistence
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-data-persistence\SKILL.md"
git commit -m "feat: add roblox-data-persistence skill"
```

---

## Batch 5: Tooling & Import Skills

### Task 16: roblox-testing

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-testing\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-testing"
```

Write `C:\Users\Oz\.zcode\skills\roblox-testing\SKILL.md` with:

```markdown
---
name: roblox-testing
description: MANDATORY AUTO-INVOKE for all Roblox unit tests, playtest automation, QA, test-driven development, and quality assurance tasks. Uses MCP to run tests, simulate input, and verify results.
---

# ROBLOX TESTING

Unit tests, playtest automation, and quality assurance.

## MCP WORKFLOW

### Step 1: Set Up Tests
```
1. search_game_tree(path: "ServerScriptService", keywords: "test") — find existing tests
2. script_read() — read test files
3. multi_edit() — write test scripts
```

### Step 2: Run Tests
```
1. start_stop_play(is_start: true) — start play test
2. execute_luau(code: [test code], datamodel_type: "Client") — run client tests
3. execute_luau(code: [test code], datamodel_type: "Server") — run server tests
4. get_console_output() — check test results
5. start_stop_play(is_start: false) — stop play
```

### Step 3: Automated Playtesting
```
1. start_stop_play(is_start: true) — start play
2. character_navigation(x: 0, y: 5, z: 0) — move character
3. user_keyboard_input(actions: [{action: "keyPress", key_code: "Space"}]) — simulate input
4. user_mouse_input(actions: [{action: "mouseButtonClick", mouse_button: "left"}]) — click
5. screen_capture() — capture result
6. get_console_output() — check results
7. start_stop_play(is_start: false) — stop play
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Test writing | `test-engineer` |
| Test execution | `execute_luau` + `get_console_output` |
| Visual regression | `screen_capture` + comparison |
| QA review | `red-team-qa` |

## CODE PATTERNS

### TestEZ-Style Tests
```lua
local TestEZ = require(path.to.TestEZ)

local MyModuleTests = {}

function MyModuleTests:BeforeEach()
    -- Setup before each test
end

function MyModuleTests:TestAddition()
    local result = 2 + 2
    expect(result).to.equal(4)
end

function MyModuleTests:TestStringConcat()
    local result = "hello" .. " " .. "world"
    expect(result).to.equal("hello world")
end

return MyModuleTests
```

### Simple Test Runner
```lua
local function runTests(tests)
    local passed = 0
    local failed = 0
    local errors = {}

    for name, testFunc in pairs(tests) do
        local success, err = pcall(testFunc)
        if success then
            passed += 1
            print("[PASS] " .. name)
        else
            failed += 1
            table.insert(errors, { name = name, error = err })
            print("[FAIL] " .. name .. ": " .. tostring(err))
        end
    end

    print(string.format("\nResults: %d passed, %d failed", passed, failed))
    return { passed = passed, failed = failed, errors = errors }
end

-- Usage:
runTests({
    ["Addition"] = function()
        assert(2 + 2 == 4, "Expected 4")
    end,
    ["Concatenation"] = function()
        assert("hello" .. " " .. "world" == "hello world", "Expected 'hello world'")
    end,
})
```

### Visual Regression Test
```lua
local function visualRegressionTest(part, expectedColor, tolerance)
    tolerance = tolerance or 0.1
    local actualColor = part.BrickColor.Color
    local diff = (actualColor - expectedColor).Magnitude
    return diff <= tolerance
end
```

### Playtest Script
```lua
local function automatedPlaytest()
    -- Start game
    -- Navigate to key areas
    -- Test interactions
    -- Verify outcomes
    -- Capture screenshots
    -- Report results
end
```

## BEST PRACTICS

- Write tests before implementation (TDD)
- Use TestEZ for structured testing
- Test both client and server contexts
- Automate repetitive playtests
- Use `screen_capture` for visual regression
- Test edge cases and error conditions
- Clean up test data after runs
- Run tests in CI/CD if possible

## VERIFICATION PROTOCOL

1. `start_stop_play` — enter play mode
2. `execute_luau` — run test suite
3. `get_console_output` — collect results
4. `screen_capture` — visual verification
5. `start_stop_play` — exit play mode
6. Report pass/fail with details

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-tools-workflow` — for debugging
- `roblox-performance` — for performance tests
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-testing\SKILL.md"
git commit -m "feat: add roblox-testing skill"
```

---

### Task 17: roblox-plugins

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-plugins\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-plugins"
```

Write `C:\Users\Oz\.zcode\skills\roblox-plugins\SKILL.md` with:

```markdown
---
name: roblox-plugins
description: MANDATORY AUTO-INVOKE for all Roblox plugin development, toolbar creation, DockWidget, Studio API, and Studio extension tasks. Uses MCP to create and test plugins.
---

# ROBLOX PLUGINS

Plugin development, toolbar, DockWidget, and Studio API.

## MCP WORKFLOW

### Step 1: Explore Plugin Structure
```
1. search_game_tree(path: "ServerScriptService", keywords: "plugin") — find plugins
2. search_game_tree(instance_type: "DockWidgetPluginGui") — find widgets
3. script_grep("plugin") — find plugin-related code
```

### Step 2: Create/Modify Plugins
```
1. multi_edit(className: "ModuleScript") — write plugin code
2. execute_luau(code: [plugin code], datamodel_type: "Edit") — test in edit mode
3. search_game_tree() — verify plugin structure
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Plugin code | `code-implementer` |
| UI design | `ui-ux-architect` |
| Testing | `execute_luau` in Edit context |

## CODE PATTERNS

### Basic Plugin
```lua
-- Plugin: MyTool
local toolbar = plugin:CreateToolbar("My Tools")
local button = toolbar:CreateButton(
    "My Tool",
    "Click to activate",
    "rbxassetid://12345678"
)

button.Click:Connect(function()
    print("Tool activated!")
end)
```

### DockWidget Plugin
```lua
local toolbar = plugin:CreateToolbar("My Tools")
local widget = plugin:CreateDockWidgetPluginGui(
    "MyWidget",
    DockWidgetPluginGuiInfo.new(
        Enum.InitialDockState.Float,
        false,  -- Initially disabled
        false,  -- Override previous state
        300, 200,  -- Size
        200, 150  -- Min size
    )
)
widget.Title = "My Widget"

local button = toolbar:CreateButton(
    "Toggle Widget",
    "Toggle my widget",
    "rbxassetid://12345678"
)

button.Click:Connect(function()
    widget.Enabled = not widget.Enabled
end)

-- Add UI to widget
local frame = Instance.new("Frame")
frame.Size = UDim2.new(1, 0, 1, 0)
frame.Parent = widget
```

### Selection Plugin
```lua
local Selection = game:GetService("Selection")

local toolbar = plugin:CreateToolbar("Selection Tools")
local button = toolbar:CreateButton(
    "Get Selection",
    "Get selected objects",
    "rbxassetid://12345678"
)

button.Click:Connect(function()
    local selection = Selection:Get()
    for _, obj in ipairs(selection) do
        print(obj:GetFullName())
    end
end)
```

### Plugin Settings
```lua
local settings = plugin:GetSetting("MySettings") or {
    AutoSave = true,
    Interval = 60,
}

local function saveSettings()
    plugin:SetSetting("MySettings", settings)
end
```

## BEST PRACTICS

- Use `plugin:CreateToolbar` for organizing tools
- Use `DockWidgetPluginGui` for persistent UI
- Save settings with `plugin:GetSetting` / `plugin:SetSetting`
- Handle plugin cleanup properly
- Test plugins in a fresh Studio session
- Use `Selection` service for object manipulation
- Provide clear button tooltips

## VERIFICATION PROTOCOL

1. `execute_luau` in Edit context — test plugin code
2. `search_game_tree` — verify plugin structure
3. `get_console_output` — check for errors
4. Manual testing in Studio

## CROSS-REFERENCES

- `roblox-coding` — for Luau patterns
- `roblox-ui-ux` — for plugin UI
- `roblox-tools-workflow` — for Studio workflows
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-plugins\SKILL.md"
git commit -m "feat: add roblox-plugins skill"
```

---

### Task 18: roblox-tools-workflow

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-tools-workflow\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-tools-workflow"
```

Write `C:\Users\Oz\.zcode\skills\roblox-tools-workflow\SKILL.md` with:

```markdown
---
name: roblox-tools-workflow
description: MANDATORY AUTO-INVOKE for all Roblox debugging, playtesting, screenshots, input simulation, Studio workflows, and MCP tool usage tasks. Uses the full MCP toolset for Studio interaction.
---

# ROBLOX TOOLS & WORKFLOW

Debugging, playtesting, screenshots, and Studio workflows.

## MCP WORKFLOW

### Step 1: Check Studio State
```
1. get_studio_state() — check current play state and available datamodel types
2. list_roblox_studios() — list connected Studio instances
3. get_console_output() — check for errors/warnings
```

### Step 2: Control Playtesting
```
1. start_stop_play(is_start: true) — start play
2. start_stop_play(is_start: false) — stop play
```

### Step 3: Navigate and Interact
```
1. character_navigation(datamodel_type: "Client", x: 0, y: 5, z: 0) — move character
2. character_navigation(datamodel_type: "Client", instance_path: "Workspace.MyPart") — move to instance
3. user_keyboard_input(datamodel_type: "Client", actions: [
    { action: "keyPress", key_code: "Space" },
    { action: "wait", wait_time_ms: 500 }
  ]) — simulate keyboard
4. user_mouse_input(datamodel_type: "Client", actions: [
    { action: "mouseButtonClick", x: 500, y: 300, mouse_button: "left" }
  ]) — simulate mouse
```

### Step 4: Capture and Verify
```
1. screen_capture(capture_id: "ScreenCapture_1") — capture viewport
2. screen_capture(camera_position: {0, 10, -20}, look_at_position: {0, 5, 0}, capture_id: "CustomView") — custom camera
3. get_console_output() — final check
```

### Step 5: Documentation
```
1. http_get(url: "https://create.roblox.com/docs/reference/engine/classes/Part.md") — fetch API docs
2. skill(skill_name: "rbx-docs-search") — search Roblox docs
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Playtesting | `start_stop_play` + `character_navigation` |
| Input simulation | `user_keyboard_input` + `user_mouse_input` |
| Screenshots | `screen_capture` |
| Documentation | `http_get` + `skill` |
| Debugging | `get_console_output` + `execute_luau` |

## DEBUGGING WORKFLOW

### Step-by-Step Debug
```
1. get_console_output() — identify error
2. script_grep("error keyword") — find source
3. script_read("game.ServerScriptService.ProblemScript") — read code
4. execute_luau(code: "print('debug info')", datamodel_type: "Server") — debug
5. multi_edit() — fix issue
6. start_stop_play(is_start: true) — test fix
7. get_console_output() — verify fix
8. start_stop_play(is_start: false) — stop
```

### Visual Debug
```
1. screen_capture(capture_id: "Before") — capture before
2. Make changes
3. screen_capture(capture_id: "After") — capture after
4. Compare captures
```

## BEST PRACTICES

- Always check `get_studio_state()` before starting play
- Use `get_console_output()` frequently for debugging
- Capture screenshots before and after changes
- Use `character_navigation` to test specific areas
- Simulate user input with `user_keyboard_input` / `user_mouse_input`
- Use `http_get` for API documentation
- Use `list_roblox_studios()` to manage multiple Studio instances

## CROSS-REFERENCES

- `roblox-coding` — for code debugging
- `roblox-testing` — for automated testing
- `roblox-performance` — for performance debugging
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-tools-workflow\SKILL.md"
git commit -m "feat: add roblox-tools-workflow skill"
```

---

### Task 19: roblox-asset-import

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-asset-import\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-asset-import"
```

Write `C:\Users\Oz\.zcode\skills\roblox-asset-import\SKILL.md` with:

```markdown
---
name: roblox-asset-import
description: MANDATORY AUTO-INVOKE for all Roblox asset import tasks including images, audio, models, meshes from external sources, Creator Store uploads, and browser automation for asset acquisition. Uses MCP tools and Playwright for web-based asset import.
---

# ROBLOX ASSET IMPORT

Importing external assets into Roblox via MCP and browser automation.

## MCP WORKFLOW

### Step 1: Prepare Assets
```
1. store_image(filePath: "C:/path/to/image.png") — load local image, get URI
2. upload_image(imagePaths: {"http://localhost/image.png"}) — upload from URL, get asset ID
```

### Step 2: Search Creator Store
```
1. search_asset(query: "medieval sword", assetType: "Model", scope: "creator_store") — marketplace search
2. search_asset(query: "background music", assetType: "Audio", scope: "auto") — audio search
3. search_asset(query: "grass texture", assetType: "Image", scope: "creator_store") — texture search
```

### Step 3: Insert Assets
```
1. insert_asset(assetId: "12345678", assetName: "MyAsset", assetType: "Model") — insert by ID
2. insert_asset(assetId: "12345679", assetName: "MyTexture", assetType: "Image") — insert texture
3. insert_asset(assetId: "12345680", assetName: "MyAudio", assetType: "Audio") — insert audio
```

### Step 4: Generate Custom Assets
```
1. generate_mesh(textPrompt: "a crystal sword", size: {x:1, y:2, z:0.3}) — AI mesh
2. generate_material(materialDescription: "glowing blue crystal", baseMaterial: "Glass", materialPattern: "Regular", materialId: "...") — AI material
3. generate_procedural_model(prompt: "a treasure chest with gold coins", partNames: "body, lid, coins") — procedural model
```

### Step 5: Verify
```
1. screen_capture() — verify imported asset appearance
2. inspect_instance() — verify properties
3. Compare with reference — iterate until match
```

## SUBAGENT PROTOCOL

| Task | Agent |
|---|---|
| Image processing | `store_image` + `upload_image` MCP tools |
| Asset search | `search_asset` MCP tool |
| Mesh generation | `generate_mesh` MCP tool |
| Material creation | `generate_material` MCP tool |
| Browser automation | `browser-automation` agent (for web downloads) |
| Visual verification | `screen_capture` + comparison |

## ASSET IMPORT PIPELINE

### Image Import
```
1. Local file: store_image(filePath) → get IMAGEID_uri
2. Web URL: upload_image(imagePaths) → get assetId
3. Insert: insert_asset(assetId, name, "Image")
4. Apply: set TextureId on Part
```

### Audio Import
```
1. Search: search_asset(query, assetType: "Audio")
2. Or use web to download, then upload
3. Insert: insert_asset(assetId, name, "Audio")
4. Configure: set Sound properties
```

### Model Import
```
1. Search: search_asset(query, assetType: "Model")
2. Or generate: generate_mesh / generate_procedural_model
3. Insert: insert_asset(assetId, name, "Model")
4. Place: set position in workspace
```

## WEB ASSET ACQUISITION (Playwright)

When assets need to be downloaded from the web:

```
1. browser_navigate(url: "https://example.com/asset") — navigate to source
2. browser_snapshot() — examine page
3. browser_click(target: "download button") — download asset
4. Or: browser_evaluate(function: "() => fetch(url).then(r => r.blob())") — download directly
5. Store locally, then use store_image / upload_image
```

## BEST PRACTICES

- Search Creator Store first before generating custom assets
- Use `scope: "auto"` for broadest search
- Use `scope: "creator_store"` for marketplace assets
- Use `scope: "user"` / `scope: "group"` for inventory assets
- Verify imported assets match requirements
- Set appropriate asset types for each import
- Use `store_image` for local files before passing to generation tools

## CROSS-REFERENCES

- `roblox-3d-assets` — for mesh/material generation
- `roblox-audio` — for audio assets
- `roblox-avatar` — for character assets
- `roblox-terrain` — for world assets
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-asset-import\SKILL.md"
git commit -m "feat: add roblox-asset-import skill"
```

---

## Batch 6: Master Orchestrator

### Task 20: roblox-orchestrator

**Files:**
- Create: `C:\Users\Oz\.zcode\skills\roblox-orchestrator\SKILL.md`

- [ ] **Step 1: Create directory and SKILL.md**

```bash
mkdir -p "C:\Users\Oz\.zcode\skills\roblox-orchestrator"
```

Write `C:\Users\Oz\.zcode\skills\roblox-orchestrator\SKILL.md` with:

```markdown
---
name: roblox-orchestrator
description: MANDATORY AUTO-INVOKE for complex Roblox tasks requiring multiple skills, full game builds, large feature implementations, and cross-domain coordination. Master orchestrator that coordinates all subagents across skills with no-stop execution and pixel-perfect verification.
---

# ROBLOX ORCHESTRATOR

Master coordinator for complex, multi-skill Roblox tasks.

## PURPOSE

When a task spans multiple Roblox disciplines (e.g., "build a complete inventory system with UI, data persistence, and networking"), this orchestrator coordinates all subagents to ensure flawless, no-stop execution.

## MCP WORKFLOW

### Step 1: Assess Scope
```
1. search_game_tree(max_depth: 4) — understand current project
2. get_studio_state() — check Studio state
3. get_console_output() — check for existing issues
```

### Step 2: Plan Execution
1. Break task into subtasks per skill
2. Identify dependencies between subtasks
3. Determine parallel vs sequential execution
4. Assign subagents to each subtask

### Step 3: Execute
```
For each subtask:
1. Invoke appropriate skill
2. Spawn subagent (code-implementer, ui-ux-architect, etc.)
3. Monitor progress via MCP tools
4. Verify output with screen_capture / get_console_output
5. If failed: retry with adjusted approach
6. If passed: proceed to next subtask
```

### Step 4: Integration
```
1. Verify all subtasks completed
2. run integration test via execute_luau
3. screen_capture() — final visual verification
4. get_console_output() — final error check
5. Report completion with details
```

## SUBAGENT COORDINATION

### Parallel Execution (independent tasks)
```
Dispatch multiple subagents simultaneously:
- code-implementer (for scripts)
- ui-ux-architect (for UI)
- generate_mesh (for 3D assets)
Wait for all to complete before integration.
```

### Sequential Execution (dependent tasks)
```
Execute in order:
1. Architecture (roblox-architecture)
2. Data layer (roblox-data-persistence)
3. Networking (roblox-networking)
4. Server logic (roblox-coding)
5. Client UI (roblox-ui-ux)
6. VFX (roblox-vfx)
7. Testing (roblox-testing)
8. QA (red-team-qa)
```

## NO-STOP PROTOCOL

1. Once started, NEVER stop until task is complete
2. If blocked: research solution, try alternative, continue
3. If error: fix, retry, verify, continue
4. If reference image provided: iterate until pixel-perfect match
5. Report final status only when 100% done

## VERIFICATION PROTOCOL

1. `screen_capture()` — capture final state
2. `get_console_output()` — verify no errors
3. `execute_luau` — run integration tests
4. Compare with reference if provided
5. Only report "done" when ALL checks pass

## SKILL INVENTORY

| Skill | Use For |
|---|---|
| `roblox-coding` | Luau code, scripts, modules |
| `roblox-ui-ux` | GUI, HUD, menus |
| `roblox-vfx` | Particles, lighting, effects |
| `roblox-animation` | Tweens, keyframes, motion |
| `roblox-3d-assets` | Meshes, materials, models |
| `roblox-audio` | Sound, music, SFX |
| `roblox-terrain` | World-building, terrain |
| `roblox-networking` | RemoteEvents, replication |
| `roblox-security` | Anti-exploit, validation |
| `roblox-performance` | Profiling, optimization |
| `roblox-testing` | Unit tests, QA |
| `roblox-plugins` | Plugin development |
| `roblox-architecture` | Game structure, patterns |
| `roblox-economy` | Monetization, currency |
| `roblox-tools-workflow` | Debugging, screenshots |
| `roblox-avatar` | Character customization |
| `roblox-cinematics` | Cutscenes, camera work |
| `roblox-data-persistence` | DataStore, save/load |
| `roblox-asset-import` | External asset pipeline |

## BEST PRACTICES

- Break complex tasks into clear subtasks
- Identify dependencies before executing
- Use parallel execution for independent tasks
- Verify each subtask before proceeding
- Never skip QA — red-team-qa before completion
- Use screen_capture for visual verification at every step
- Log progress for transparency

## OUTPUT FORMAT

```text
[ROBLOX ORCHESTRATOR]
Task: {full task description}
Subtasks:
  1. {subtask} — {status}
  2. {subtask} — {status}
  ...
Total: {X}/{Y} complete
Status: {in-progress|complete}
```
```

- [ ] **Step 2: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\roblox-orchestrator\SKILL.md"
git commit -m "feat: add roblox-orchestrator skill"
```

---

## Final Task: Update Existing game-developer Skill

### Task 21: Update game-developer

**Files:**
- Modify: `C:\Users\Oz\.zcode\skills\game-developer\SKILL.md`

- [ ] **Step 1: Read existing file**

Read `C:\Users\Oz\.zcode\skills\game-developer\SKILL.md`

- [ ] **Step 2: Update description to reference Roblox skills**

Add a reference section at the top of the ROBLOX / LUAU section:

```markdown
> **Roblox MCP Integration:** For comprehensive Roblox development, see the dedicated Roblox skill suite:
> `roblox-game-dev` (orchestrator), `roblox-coding`, `roblox-ui-ux`, `roblox-vfx`, `roblox-animation`, `roblox-3d-assets`, `roblox-audio`, `roblox-terrain`, `roblox-networking`, `roblox-security`, `roblox-performance`, `roblox-testing`, `roblox-plugins`, `roblox-architecture`, `roblox-economy`, `roblox-tools-workflow`, `roblox-avatar`, `roblox-cinematics`, `roblox-data-persistence`, `roblox-asset-import`, `roblox-orchestrator`
```

- [ ] **Step 3: Commit**

```bash
git add "C:\Users\Oz\.zcode\skills\game-developer\SKILL.md"
git commit -m "feat: update game-developer with Roblox skill references"
```

---

## Summary

**Total Tasks:** 21
**Estimated Time:** ~30 minutes for all skills
**Dependencies:** None between skills (all independent SKILL.md files)
**Parallelization:** All skills can be created simultaneously via subagents

**Files Created:**
- `C:\Users\Oz\.zcode\skills\roblox-game-dev\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-coding\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-architecture\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-ui-ux\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-vfx\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-animation\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-3d-assets\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-terrain\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-audio\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-avatar\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-cinematics\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-economy\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-networking\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-security\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-performance\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-data-persistence\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-testing\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-plugins\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-tools-workflow\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-asset-import\SKILL.md`
- `C:\Users\Oz\.zcode\skills\roblox-orchestrator\SKILL.md`

**Modified:**
- `C:\Users\Oz\.zcode\skills\game-developer\SKILL.md` (added Roblox skill references)
```

Now let me exit plan mode and present this for approval.</think>Plan complete and saved to `docs/superpowers/plans/2026-07-22-roblox-skill-suite.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration. All 21 skills are independent SKILL.md files, so they can be created in parallel batches.

2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Since all skills are independent files with no dependencies, I recommend **Subagent-Driven** with parallel batches for maximum speed.<tool_call>
<function=AskUserQuestion>
<parameter=questions>[{"header": "Execution", "multiSelect": false, "options": [{"description": "Dispatch subagents to create skills in parallel batches — fastest approach for 21 independent files", "label": "Subagent-Driven (Recommended)"}, {"description": "Execute sequentially in this session with review checkpoints", "label": "Inline Execution"}], "question": "How should I execute the plan to create all 21 Roblox skills?"}]