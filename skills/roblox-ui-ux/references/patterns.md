# roblox-ui-ux — PATTERNS

StarterGui.MainInterface (ScreenGui)
  ResetOnSpawn = false
  IgnoreGuiInset = false
  ScreenInsets = CoreUISafeInsets        -- prevents notch and core UI overlap
  ZIndexBehavior = Sibling
  ├─ HUDLayer (Frame, Size 1,1)          -- Persistent stats & hotbars
  │   ├─ HealthGroup (Frame + Scrim)
  │   │   ├─ Scrim (UICorner 8px, BackgroundTransparency 0.3)
  │   │   ├─ HealthIcon (ImageLabel, AspectRatio 1)
  │   │   ├─ BarBackground (Frame + UIStroke + UIGradient)
  │   │   │   └─ Fill (Frame, Tweened)
  │   │   └─ ValueLabel (TextLabel + UIStroke 1.5px dark)
  │   └─ CurrencyGroup (Frame + Scrim)
  │       ├─ CurrencyIcon (ImageLabel)
  │       └─ AmountLabel (TextLabel + UIStroke)
  ├─ ToastLayer (Frame, Size 1,1)        -- Transient alerts & banners
  └─ ModalLayer (Frame, Size 1,1)        -- Menus, shops, inventories (modal-controlled)
      ├─ DimBackground (Frame, Black, Transparency 0.45)
      └─ DialogCard (Frame + UICorner + UIStroke with Emboss Gradient + DropShadow)
```

	### 2. Tactile Button with Embossed Rim and Tween Interaction
	```lua
	local TweenService = game:GetService("TweenService")
	local function SetupTactileButton(button: GuiButton, onClick: () -> ())
	    local originalSize = button.Size
	    local hoverInfo = TweenInfo.new(0.12, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
	    local pressInfo = TweenInfo.new(0.08, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	    local function setScale(m: number, info: TweenInfo)
	        TweenService:Create(button, info, {
	            Size = UDim2.new(originalSize.X.Scale * m, originalSize.X.Offset, originalSize.Y.Scale * m, originalSize.Y.Offset)
	        }):Play()
	    end
	    button.MouseEnter:Connect(function() setScale(1.05, hoverInfo) end)
	    button.MouseLeave:Connect(function() setScale(1.0, hoverInfo) end)
	    button.MouseButton1Down:Connect(function() setScale(0.95, pressInfo) end)
	    button.MouseButton1Up:Connect(function() setScale(1.05, hoverInfo) end)
	    button.Activated:Connect(onClick)
	end
	```

### 3. Embossed UIStroke Construction
```lua
local function ApplyEmbossedBorder(frame: GuiObject, baseColor: Color3, thickness: number)
    local stroke = Instance.new("UIStroke")
    stroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
    stroke.Thickness = thickness or 2
    stroke.Color = Color3.fromRGB(255, 255, 255)
    stroke.Parent = frame

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = 90 -- Top-to-bottom light incidence
    gradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0.0, Color3.fromRGB(255, 255, 255)),   -- Specular top rim
        ColorSequenceKeypoint.new(0.4, baseColor),                       -- True border color
        ColorSequenceKeypoint.new(1.0, Color3.fromRGB(20, 24, 30))       -- Shaded bottom rim
    })
    gradient.Parent = stroke
    return stroke
end
```

### 4. Dual-Boundary Text Isolation
```lua
local function FormatIsolatedText(label: TextLabel)
    label.TextColor3 = Color3.fromRGB(250, 252, 255)
    label.TextStrokeTransparency = 1 -- Disable deprecated legacy stroke
    
    local stroke = label:FindFirstChildOfClass("UIStroke") or Instance.new("UIStroke")
    stroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual
    stroke.Thickness = 2
    stroke.Color = Color3.fromRGB(12, 16, 24) -- Dark charcoal boundary
    stroke.Transparency = 0.15
    stroke.Parent = label
end
```

### 5. Button Intent with Rollback (Anti-Desync)
```lua
buyButton.Activated:Connect(function()
    buyButton.Active = false
    -- Show brief loading indicator or spinner
    local ok, message = Remotes.RequestPurchase:InvokeServer(itemId) -- Bounded, pcall'd
    if not ok then
        HUD:Toast(message or "Purchase failed")                      -- Server rejected
        -- Roll back any local optimistic state
    end
    buyButton.Active = true
end)
```
Never deduct coins or inventory counts locally before server confirmation.

### 6. Console / 10-Foot Pass
- Body text ≥24 px equivalent at 1080p, larger for critical combat and countdown labels.
- Focus order must be explicit (`Selectable`, `NextSelection*`), with a distinct high-contrast selection cursor.
- Never use hover tooltips as the only hint; display gamepad button icons (e.g. `(A) Select`, `(B) Back`) inline.
- Maintain a modal selection group (`GuiService.SelectedObject`) so navigation cannot escape behind open dialogs.

### 7. 3D ViewportFrame Hero Showcase with Telephoto Camera & Idle Spin
```lua
local RunService = game:GetService("RunService")
local function SetupHero3DViewport(viewportFrame: ViewportFrame, itemModel: Model): () -> ()
    viewportFrame.Ambient = Color3.fromRGB(160, 170, 190)
    viewportFrame.LightColor = Color3.fromRGB(255, 250, 240)
    viewportFrame.LightDirection = Vector3.new(-1, -1.5, -1).Unit

    local camera = Instance.new("Camera")
    camera.FieldOfView = 30 -- Telephoto isometric sweet spot: eliminates wide-angle distortion
    camera.Parent = viewportFrame
    viewportFrame.CurrentCamera = camera

    local clone = itemModel:Clone()
    local _, size = clone:GetBoundingBox()
    local maxDim = math.max(size.X, size.Y, size.Z)
    local distance = (maxDim / 2) / math.tan(math.rad(camera.FieldOfView / 2)) * 1.25
    clone:PivotTo(CFrame.new(Vector3.zero))
    clone.Parent = viewportFrame
    camera.CFrame = CFrame.new(Vector3.new(0, size.Y * 0.15, distance), Vector3.zero)

    local rotAngle = 0
    local conn = RunService.RenderStepped:Connect(function(dt)
        rotAngle = (rotAngle + dt * math.rad(30)) % (2 * math.pi)
        clone:PivotTo(CFrame.Angles(0, rotAngle, 0))
    end)
    return function()
        conn:Disconnect()
        clone:Destroy()
        camera:Destroy()
    end
end
```

### 8. Diagonal Sweeping Sheen / Foil Gloss (`UIGradient` Offset)
```lua
local TweenService = game:GetService("TweenService")
local function AttachFoilSheen(cardFrame: GuiObject)
    local sheen = Instance.new("Frame")
    sheen.Name = "FoilSheen"
    sheen.Size = UDim2.fromScale(1, 1)
    sheen.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
    sheen.ZIndex = 5
    sheen.Parent = cardFrame
    local corner = cardFrame:FindFirstChildOfClass("UICorner")
    if corner then corner:Clone().Parent = sheen end

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = 45
    gradient.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0.0, 1.0), NumberSequenceKeypoint.new(0.42, 1.0),
        NumberSequenceKeypoint.new(0.50, 0.15), NumberSequenceKeypoint.new(0.58, 1.0),
        NumberSequenceKeypoint.new(1.0, 1.0)
    })
    gradient.Offset = Vector2.new(-1, -1)
    gradient.Parent = sheen

    local tweenInfo = TweenInfo.new(0.85, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    return function()
        gradient.Offset = Vector2.new(-1, -1)
        TweenService:Create(gradient, tweenInfo, { Offset = Vector2.new(1, 1) }):Play()
    end
end
```

### 9. Rotating Sunburst / Rayburst Energy Backdrop
```lua
local RunService = game:GetService("RunService")
local function SetupRayburstBackdrop(container: GuiObject, rarityColor: Color3): () -> ()
    local rayburst = Instance.new("ImageLabel")
    rayburst.Name = "Rayburst"
    rayburst.AnchorPoint = Vector2.new(0.5, 0.5)
    rayburst.Position = UDim2.fromScale(0.5, 0.5)
    rayburst.Size = UDim2.fromScale(1.8, 1.8)
    rayburst.BackgroundTransparency = 1
    rayburst.Image = "rbxassetid://13847844005"
    rayburst.ImageColor3 = rarityColor
    rayburst.ImageTransparency = 0.65
    rayburst.ZIndex = 2
    rayburst.Parent = container

    local conn = RunService.RenderStepped:Connect(function(dt)
        rayburst.Rotation = (rayburst.Rotation + 25 * dt) % 360
    end)
    return function()
        conn:Disconnect()
        rayburst:Destroy()
    end
end
```

---
