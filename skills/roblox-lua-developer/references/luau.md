# Luau Language Reference (on-demand)

Load only for Luau coding tasks (syntax, idioms, module patterns).

### Language model

- **Type inference**: Luau infers types from literals and usage; annotate public module boundaries with `type` aliases. Example: `type PlayerData = { Coins: number, Level: number, Inventory: {[string]: number} }`. Use `typeof(...)` for structural types. This is documentation and lint-verified — catch errors before runtime.
- **Tables**: the single data structure; arrays (integer keys, use `ipairs`/`#`) vs dictionaries (`pairs`). Never mix sparse integer keys with `#`. `table.create(n, v)` pre-fills a table; `table.freeze` makes read-only tables (use for configs/constants).
- **Metatables**: OO and operator overloading via `__index`, `__newindex`, `__call`, `__tostring`, `__eq`. Pattern: `local C = {}; C.__index = C; function C.new(...) return setmetatable({...}, C) end`. Overriding `__index` on hot paths adds a lookup cost.
- **Closures**: first-class functions with upvalues; use them for callbacks and encapsulating private state (module-local "private" variables). Beware closure capture in loops — capture the loop variable by copy when needed.
- **Task library**: `task.spawn`, `task.delay`, `task.wait`, `task.cancel`, `task.defer` replace the legacy `spawn`/`delay`/`wait` and do not yield on the main thread incorrectly. Prefer them everywhere.
- **Safety**: `pcall`/`xpcall` for expected failures (DataStore, MarketplaceService, remote calls). `math.clamp` for numeric ranges. No global mutable state; every module returns a single table or function.

### Performance idioms (O(n) and frame-budget discipline)

- **Cache property access** — hoist `local pos = part.Position`; do not re-read properties inside per-frame loops when stable; property reads are reflection + occasional allocation.
- **Avoid per-frame allocations** — hoist table/vector construction out of `Heartbeat`/`RenderStepped`. Prefer pooling (`ParticleEmitter:Emit(n)`, object pools for projectiles/VFX) over `Instance.new` in hot loops.
- **Batch iteration** — process large collections in chunks (e.g. 100/frame) and `task.wait()` between batches to keep frame time flat.
- **Connection hygiene** — every `:Connect` returns a `RBXScriptConnection`; disconnect when done or route through a connection manager. Leaked connections accumulate listeners and memory.
- **Minimize `WaitForChild` in hot paths** — cache resolved instances at startup; `WaitForChild` yields and can stall scripts.
- **Profile before optimizing** — measure with `collectgarbage("count")`, `os.clock()`, and the Studio Performance Console before changing anything. Do not guess.
- **Streaming-friendly design** — keep always-needed scripts/assets in `ReplicatedStorage`; treat `Workspace` content as load-on-demand.

### Code patterns (shared)

**Module class factory** — the canonical reusable-module shape; use for DataStore wrappers, managers, and systems:

```lua
-- ReplicatedStorage.Modules.MyModule (or ServerScriptService for server-only)
local MyModule = {}
MyModule.__index = MyModule

function MyModule.new(config)
    return setmetatable({ config = config or {} }, MyModule)
end

function MyModule:DoSomething()
    -- implementation
end

return MyModule
```

**Private state via closure** — module-local variables are invisible to callers:

```lua
local State = {}
do
    local secret = {}
    function State.Get(key) return secret[key] end
    function State.Set(key, value) secret[key] = value end
end
return State
```

**Typed table at module boundary**:

```lua
-- Document shape, validated by the Luau type checker.
type PlayerData = { Coins: number, Level: number, Inventory: {[string]: number} }
local DEFAULT_DATA: PlayerData = table.freeze({ Coins = 0, Level = 1, Inventory = {} })
```

**Event-dispatch helper** (avoid anonymous listener sprawl):

```lua
local E = {}
local listeners = {}
function E:On(name, fn)
    local bucket = listeners[name]
    if not bucket then
        bucket = {}
        listeners[name] = bucket
    end
    table.insert(bucket, fn)
end
return E
```

**Loop-capture guard** — closures capture loop variables by reference; bind a copy when needed:

```lua
local buttons = { ... }
for i, button in ipairs(buttons) do
    local index = i
    button.Activated:Connect(function() print("clicked", index) end)
end
```
