# Roblox Code Patterns (on-demand reference)

Consolidated, production-grade patterns. Load only the pattern needed.

### State machine (game/UI state transitions)

```lua
local SM = {}
SM.__index = SM

function SM.new()
    return setmetatable({ states = {}, currentState = nil }, SM)
end

function SM:AddState(name, state) self.states[name] = state end

function SM:Transition(newName)
    if self.currentState then self.currentState:Exit() end
    self.currentState = self.states[newName]
    if self.currentState then self.currentState:Enter() end
end

function SM:Update(dt)
    if self.currentState then self.currentState:Update(dt) end
end

return SM  -- Avoids opaque if/else if/else chains; states are first-class tables.
```

### DataStore wrapper (pcall + cache + UpdateAsync)

```lua
local DataStoreService = game:GetService("DataStoreService")

local Store = {}
Store.__index = Store

function Store.new(name, version)
    return setmetatable({
        store = DataStoreService:GetDataStore(name .. "_v" .. (version or 1)),
        cache = {},
    }, Store)
end

function Store:GetAsync(key)
    if self.cache[key] ~= nil then return self.cache[key] end     -- read cache, O(1)
    local ok, data = pcall(function() return self.store:GetAsync(key) end)  -- never uncaught
    if ok then self.cache[key] = data end
    return ok and data or nil
end

function Store:SetAsync(key, value)
    local ok, err = pcall(function() return self.store:SetAsync(key, value) end)
    if ok then self.cache[key] = value end
    return ok, err
end

function Store:UpdateAsync(key, fn)
    -- UpdateAsync guarantees atomic read-modify-write; use for economy/numeric state.
    local ok, result = pcall(function() return self.store:UpdateAsync(key, fn) end)
    if ok then self.cache[key] = result end
    return ok, result
end

return Store
```

### Object pool (avoid per-frame Instance.new churn)

```lua
local Pool = {}
Pool.__index = Pool

function Pool.new(template, size)
    local self = setmetatable({ template = template, available = {}, active = {} }, Pool)
    for _ = 1, (size or 10) do
        local obj = template:Clone()
        obj.Parent = nil
        table.insert(self.available, obj)
    end
    return self
end

function Pool:Get()
    local obj = table.remove(self.available) or self.template:Clone()
    table.insert(self.active, obj)
    return obj
end

function Pool:Return(obj)
    obj.Parent = nil
    self.active[table.find(self.active, obj)] = nil   -- O(1) index removal
    table.insert(self.available, obj)
end

return Pool
```

### Connection manager (leak prevention)

```lua
local Connections = { list = {} }

function Connections:Add(conn)
    table.insert(self.list, conn)
    return conn
end

function Connections:Clean()
    for _, conn in ipairs(self.list) do
        if conn.Connected then conn:Disconnect() end
    end
    self.list = {}
end

return Connections
```

### Server-authoritative remote (validate BEFORE acting)

```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Event = ReplicatedStorage:WaitForChild("Events"):WaitForChild("MoveRequest")

Event.OnServerEvent:Connect(function(player, target)
    -- 1) type-check, 2) range-check via clamp, 3) allowlist, 4) rate limit
    if typeof(target) ~= "Vector3" then return end
    local root = player.Character and player.Character.PrimaryPart
    if not root then return end                     -- no character, no action
    local MAX = 64
    if (target - root.Position).Magnitude > MAX then
        return                                      -- reject out-of-range teleport
    end
    -- 5) apply ONLY after validation
    root.CFrame = CFrame.new(target)
end)
```

### Rate limiter (per-actor, sliding window)

```lua
local Limits = {}
function Limits.accept(player, action, maxPerWindow, windowSec)
    local key = player.UserId .. ":" .. action
    local now = tick()
    local buf = Limits[key] or {}
    local valid = {}
    -- keep only fresh entries to bound memory
    for _, t in ipairs(buf) do if now - t < windowSec then table.insert(valid, t) end end
    if #valid >= maxPerWindow then Limits[key] = valid; return false end
    table.insert(valid, now); Limits[key] = valid; return true
end
```

### UI responsive pattern (viewport-aware)

```lua
local camera = workspace.CurrentCamera
local frame = script.Parent.Frame  -- inside a ScreenGui in StarterGui

local function relayout()
    local vp = camera.ViewportSize
    local mobile = vp.X < 768
    frame.Size = mobile and UDim2.new(0.9, 0, 0.4, 0) or UDim2.new(0.3, 0, 0.5, 0)
end

camera:GetPropertyChangedSignal("ViewportSize"):Connect(relayout)
relayout()
```
Keep GUI scripts in StarterPlayerScripts / under PlayerGui; set ResetOnSpawn = false for persistent HUDs.
