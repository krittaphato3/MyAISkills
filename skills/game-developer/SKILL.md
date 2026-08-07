---
name: game-developer
description: Build game code and systems across engines — Unity (C#), Unreal (C++/Blueprint), Godot (GDScript)—plus game design patterns. Use when writing gameplay or engine-specific code on these engines. Roblox (Luau) work routes to the roblox-lua-developer skill.
version: 0.2.0
grade: G2
domain: delivery
status: active
last-reviewed: 2026-08-07
owned-by-agent: game-developer
---

# GAME DEVELOPER

Expert game development across multiple engines and platforms.

## ROBLOX / LUAU

> **Roblox integration:** For comprehensive Roblox development with direct Studio integration, see the consolidated skill: `roblox-lua-developer` (routes any Roblox/Luau task to the correct domain workflow).

### Script Structure
```lua
-- Server Script
local Players = game:GetService("Players")

Players.PlayerAdded:Connect(function(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player
    
    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = leaderstats
end)
```

### Common Patterns
```lua
-- Remote Event handling
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RemoteEvent = ReplicatedStorage:WaitForChild("MyEvent")

RemoteEvent.OnServerEvent:Connect(function(player, data)
    -- Handle client request
end)

-- Tween animation
local TweenService = game:GetService("TweenService")
local tween = TweenService:Create(
    part,
    TweenInfo.new(1, Enum.EasingStyle.Quad),
    {Position = Vector3.new(0, 10, 0)}
)
tween:Play()
```

## UNITY / C#

### MonoBehaviour Pattern
```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    [SerializeField] private float jumpForce = 10f;
    
    private Rigidbody rb;
    private bool isGrounded;
    
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }
    
    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        Vector3 movement = new Vector3(horizontal, 0, vertical) * speed;
        rb.AddForce(movement, ForceMode.Acceleration);
        
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }
    
    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
            isGrounded = true;
    }
    
    void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
            isGrounded = false;
    }
}
```

## GODOT / GDSCRIPT

### Character Controller
```gdscript
extends CharacterBody2D

@export var speed = 300.0
@export var jump_velocity = -400.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
    if not is_on_floor():
        velocity.y += gravity * delta
    
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    
    var direction = Input.get_axis("left", "right")
    velocity.x = direction * speed
    
    move_and_slide()
```

## GAME DESIGN PATTERNS

### State Machine
```lua
-- Roblox State Machine
local StateMachine = {}
StateMachine.__index = StateMachine

function StateMachine.new()
    return setmetatable({states = {}, currentState = nil}, StateMachine)
end

function StateMachine:AddState(name, state)
    self.states[name] = state
end

function StateMachine:Transition(newState)
    if self.currentState then
        self.currentState:Exit()
    end
    self.currentState = self.states[newState]
    self.currentState:Enter()
end

function StateMachine:Update(dt)
    if self.currentState then
        self.currentState:Update(dt)
    end
end
```

### Object Pooling
```csharp
// Unity Object Pool
public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int poolSize = 10;
    
    private Queue<GameObject> pool = new Queue<GameObject>();
    
    void Start()
    {
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }
    
    public GameObject GetObject()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        return Instantiate(prefab);
    }
    
    public void ReturnObject(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

## OUTPUT
```text
[GAME DEV]
Engine: {Roblox|Unity|Godot|Unreal}
Platform: {PC|Mobile|Console}

DELIVERABLES:
- {script/component 1}
- {script/component 2}

PATTERNS USED:
- {pattern 1}
- {pattern 2}
```

## WHEN TO USE
- Writing gameplay code, engine-specific logic (Unity/C#, Unreal/C++/Blueprint, Godot/GDScript), or a game system that must run in an engine.
- You need a canonical script/pattern (state machine, object pooling, movement, input, animation tweening) in a game context.
- Debugging or extending an existing gameplay feature in one of these engines.
- Designing a game mechanism (spawning, scoring, physics response) that must be implemented in-engine. (Roblox/Luau work routes to `roblox-lua-developer`.)

## WHEN NOT TO USE
- **Roblox (Luau) development** — that is the consolidated domain of `roblox-lua-developer`.
- **Game-design-adjacent but not code**: balancing spreadsheets, narrative/level design prose without an implementation target.
- **Non-engine game backend** (matchmaking API, auth, telemetry) — platform/service code is devops/api, not in-engine.
- **One-off native UI outside the engine** — leave to mobile/UI skills unless it's an in-engine HUD.

## DECISION TREE
```text
1. ENGINE → Unity/C#? Unreal (C++ / Blueprint)? Godot/GDScript? Roblox/Luau?
   Roblox → roblox-lua-developer. Else continue.
2. WHAT  → gameplay logic (movement/combat)? A reusable system (state machine / pool)?
   A mechanism (physics/animation/audio)? → select the matching pattern section.
3. PATTERN → for a recurring need pick the canonical pattern from GAME DESIGN PATTERNS
   (state machine, object pooling, factory, event bus) and adapt to the engine.
4. INTEGRATE → wire it to the engine's update/input/collision hooks; respect tick/authority model.
5. VERIFY → test the edge cases in-engine (empty/high concurrency, framerate). Record the result.
```
Never pick a pattern before you know the engine and whether it's gameplay vs a reusable system.

## FAILURE MODES & MITIGATIONS
- **Wrong engine idioms.** DETECT: code uses the wrong API or foreign conventions (e.g., a C# MonoBehaviour used as a static utility), and build/runtime issues surface in-engine.
  FIX: follow the engine's official script model (Component/MonoBehaviour in Unity, Node in Godot, Actor in Unreal), and choose the section matching the engine.
- **Missing tick/framerate discipline.** DETECT: heavy work in `Update`/`_physics_process` causes frame drops or desync under spawn storms.
  FIX: use delta-time (`delta`/`Time.deltaTime`) everywhere, move non-per-frame work to fixed timestep or a coroutine/async, and keep hot paths allocation-light.
- **State-machine spaghetti.** DETECT: `if`/`switch` on state littered across the class; states become hard to add and test.
  FIX: use the canonical state-machine pattern with explicit `Enter/Exit/Update` states; keep transitions data-driven.
- **Object-pool misuse / GC hitches.** DETECT: instantiation/deletion churns in hot paths produces GC stalls (Unity/Godot) or object churn.
  FIX: pool frequently-reused objects, warm the pool, disable rather than destroy, and re-enable on get with zeroed state. (see Object Pooling)
- **Network/authority desync.** DETECT: clients disagree on a shared game state; writes happen on the wrong authority.
  FIX: put authoritative logic on the server/authoritative host, replicate only the smallest data, and validate client input.
- **Cross-engine confusion in one codebase.** DETECT: Godot, Unity, and Roblox snippets mixed into the same file/function.
  FIX: keep one engine per script and per subsystem; isolate engine adapters behind a thin interface when code must be portable.

## VERIFICATION GATE
- **In-engine run**: the feature builds and runs in the target engine with no console errors or warnings introduced.
- **Behavioral edge cases pass**: high-concurrency/empty/boundary inputs handled without crash (spawn storm, zero entities, max capacity).
- **Framerate discipline honored**: no fixed-cost-per-frame work in the active loop; hot path is measured to hold the target frame rate.
- **State machine test**: transitions are exercised (empty→running→paused→exit); no illegal transition reachable.
- **red-team-qa review**: adversarial check for framerate-sinking code, network desync, or a state machine that can be wrong-commanded.

## REFERENCES
- Unity Learn / scripting docs — MonoBehaviour, physics, pooling.
- Unreal Engine docs — Actors, Blueprints, Gameplay Framework.
- Godot documentation — Nodes, GDScript, physics and signal flow.
- Game Programming Patterns (Nystrom) — state machine, object pool, command, observer.
