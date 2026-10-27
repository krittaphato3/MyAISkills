---
name: roblox-ui-ux
description: 'Designs and builds Roblox interfaces with AAA visual polish: ScreenGui structure, UDim2
  sizing, safe areas, HUD state binding, tactile micro-interactions, curated vector icons, anti-cancellation
  contrast, and 3D pop-out hero showcases (interactive ViewportFrames, burst-out cards, sheen gloss, rayburst
  backdrops, studio lighting). Use when building or styling any HUD, menu, shop, inventory, modal, prompt,
  crate/gacha showcase, or badge needing front-page quality. World lighting and geometry route to roblox-world-building;
  tweened character motion to roblox-animation.'
metadata:
  version: 1.2.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-24'
  owned-by-agent: roblox-ui-designer
---


# Roblox UI/UX

Roblox UI is a layout system with a state-binding problem attached and a visual polish standard
demanded by top-tier front-page experiences. The layout half is solved by constraints, scale, and
safe-area insets; the state half is where games break — a HUD showing last frame's health, a button
that fires before the server confirms, or a menu trapping a console player. The visual half is what
separates amateur prototypes from hit games: tactile 3D depth, embossed borders, multi-layered
drop shadows, curated vector iconography, responsive micro-interactions, and rigorous anti-cancellation
color harmony that remains razor-sharp against unpredictable 3D scene lighting.

## WHEN TO USE

- Any HUD, menu, shop, inventory, quest log, dialog system, prompt, notification, or floating feedback.
- Hero item showcases, pet/weapon display cards, gacha/crate reveals, and badges with a 3D pop-out "picture look".
- Interactive 3D ViewportFrames with isometric telephoto cameras (~30° FOV), idle rotation, and mouse tilt micro-interactions.
- Burst-out-of-frame card layering (`ClipsDescendants = false`), rotating rayburst backdrops, and diagonal sweeping sheen gloss.
- Styling interfaces to match AAA front-page games (tactile buttons, embossed borders, drop shadows, glassmorphism).
- A UI that breaks on phones, tablets, or TVs; text that washes out against bright skyboxes or dark shadows.
- Adding gamepad navigation, touch targets, keyboard shortcuts, and tactile audio-visual micro-interactions.
- Accessibility and readability: anti-cancellation contrast, text sizing, reduced motion, and multi-modal cues.
- Binding server state into UI cleanly with one-directional data flow and optimistic rollback.

## WHEN NOT TO USE

- In-world 3D signage or surface GUIs that are part of level architecture — `roblox-world-building`.
- Camera cutscenes, rigging, and character animation tracks — `roblox-animation`.
- Full-screen atmosphere (color grading, bloom, screen distortion) as mood — `roblox-vfx`.
- Non-Roblox web or native application frontends — `frontend-web-engineer`.

---

## COLOR HARMONY & ANTI-CANCELLATION DOCTRINE

In Roblox games, the camera rotates across dynamic environments: blazing neon skies, dark interiors,
vibrant particle explosions, and specular terrain. UI elements that rely on plain flat colors instantly
wash out or cause severe visual fatigue. Follow these non-negotiable optical rules:

### 1. Optical Anti-Vibration (Ban Chromostereopsis)
- **Never place pure saturated red on pure saturated green** (`#FF0000` on `#00FF00` or vice versa).
- **Never place pure saturated blue on pure saturated red** (`#0000FF` on `#FF0000` or vice versa).
- *Why:* Chromatic aberration in human eye lenses focuses red and blue light at different retinal depths,
  causing severe optical vibration, depth distortion, and headache-inducing strain. Separate high-chroma
  elements with neutral barriers or desaturate backing layers.

### 2. Ban Isoluminant Pairings
- **Never place yellow on white** (`#FFFF00` / `#FFFFFF`).
- **Never place saturated blue on black or dark charcoal** (`#0000FF` / `#121212`).
- **Never place light gray on white or dark gray on dark slate**.
- *Why:* Human edge perception relies on luminance contrast (L*), not color hue difference. If two
  different colors have identical luminance, text edges become invisible and completely unreadable.

### 3. Dual-Boundary Isolation (Anti-Washout Stroke)
- Every text label and floating icon rendered over the 3D scene **must** feature a contextual `UIStroke`:
  - **Light text / elements**: Dark outer stroke (`Color3.fromRGB(12, 16, 24)`, thickness `1.5–2.5px`, `Transparency = 0.15–0.25`).
  - **Dark text / elements**: Crisp light halo stroke (`Color3.fromRGB(240, 244, 250)`, thickness `1.5px`, `Transparency = 0.3`).
- *Effect:* Regardless of whether a player looks at direct sunlight, glowing laser beams, or a pitch-black cave,
  text and icons maintain constant, razor-sharp edge contrast.

### 4. Protective Scrim Backing
- Critical HUD elements (health bars, hotbars, minimaps, quest trackers) must sit on a protective scrim frame:
  - Material tone: Slate or Deep Carbon (`Color3.fromRGB(16, 20, 28)` to `Color3.fromRGB(24, 28, 38)`).
  - `BackgroundTransparency = 0.25 - 0.35` (retains game immersion while suppressing background noise).
  - `UICorner` radius `6–10px`.

### 5. Multi-Modal Cues (Colorblindness Defense)
- **Never encode state by color alone.** Every status color must be accompanied by two redundant signals:
  - *Icon/Shape*: Cross for health, lightning for stamina, shield for armor, skull for fatal/danger.
  - *Numeric / Text Label*: Display "HP: 100/100" or status badges alongside the color fill.

---

## AAA BIG-GAME VISUAL POLISH & DESIGN SYSTEM ("HOW FRONT-PAGE GAMES DO IT")

Front-page Roblox experiences (Blox Fruits, Pet Simulator 99, BedWars, Doors) stand out because their UI
feels physically tangible, layered, and responsive.

### 1. Tactile 3D Depth & Embossed Borders
Flat single-color borders look unfinished. Professional games simulate top-lit beveling:
- Insert a `UIStroke` (Thickness `2px` to `3px`, `ApplyStrokeMode = Border`).
- Insert a child `UIGradient` inside the `UIStroke`:
  - `Rotation = 90` (vertical gradient).
  - `Color`: Top color lighter (e.g. `Color3.fromRGB(255, 255, 255)` with subtle transparency `0.1`),
    bottom color darker (e.g. `Color3.fromRGB(70, 80, 100)` with transparency `0.4`).
- This creates an embossed, tactile metallic or acrylic rim that captures light from above.

### 2. Layered 9-Slice Drop Shadows & Ambient Occlusion
- Floating cards and dialogs must not touch the 3D world directly.
- Add an underlying shadow frame:
  - A slightly larger backing frame with `ZIndex = card.ZIndex - 1`.
  - Use a 9-slice soft blurred shadow texture or offset black frame (`BackgroundTransparency = 0.5 - 0.7`, offset `UDim2.new(0, 0, 0, 4)`).
  - Prevents the card from looking pasted-on and visually anchors the modal.

### 3. Curated Iconography Over Bare Text
- **Zero bare text buttons:** Every button, tab, stat row, and inventory slot must pair text with a clean vector icon.
- Use standardized vector icon sets (Lucide Roblox icon suite or consistent asset IDs).
- Enforce `UIAspectRatioConstraint` (Aspect Ratio 1) on all icon `ImageLabel` containers.
- Maintain consistent icon fill and stroke color hierarchy matching the typography.

### 4. Tactile Micro-Interactions
UI must acknowledge player physical input instantly with smooth, spring-like motion:
- **Hover Affordance**: Scale button up to `1.05x` using `TweenService` (Duration `0.12s`, `EasingStyle.Back` or `Quad`, `EasingDirection.Out`).
- **Click Affordance (Depression)**: Scale down to `0.95x` and slightly darken fill on mouse down/tap.
- **Audio Feedback**: Every interaction triggers a dedicated client sound effect (`UISound` service or localized `Sound` instance):
  - Subtle pop/tick on hover.
  - Crisp mechanical click on activation.
  - Distinctive chimes on purchase, claim, or error.

### 5. Glassmorphism & Frosted Card Containers
- Containers utilize dark translucent surfaces with layered depth:
  - Container Background: `Color3.fromRGB(20, 24, 34)`, `BackgroundTransparency = 0.25`.
  - Inner padding: `UIPadding` (Top/Bottom/Left/Right `12–16px`).
  - Corner rounding: `UICorner` (Radius `8–10px`).
  - Subtle inner sheen: A thin top-edge highlight frame or vertical background gradient.

### 6. Rarity Tier Visual Language
Item cards, loot drops, and badges follow standardized color tokens with paired gradient strokes:

| Rarity | Primary Accent | Border Gradient (Top → Bottom) | Token Hex |
|---|---|---|---|
| **Common** | Cool Slate | `#CBD5E1` → `#64748B` | `#94A3B8` |
| **Uncommon** | Vivid Emerald | `#6EE7B7` → `#059669` | `#10B981` |
| **Rare** | Electric Cobalt | `#93C5FD` → `#2563EB` | `#3B82F6` |
| **Epic** | Royal Amethyst | `#C4B5FD` → `#7C3AED` | `#8B5CF6` |
| **Legendary** | Radiance Gold | `#FDE047` → `#D97706` | `#F59E0B` |
| **Mythic** | Crimson Ruby | `#FCA5A5` → `#DC2626` | `#EF4444` |

### 7. Typographic Hierarchy
Use modern, readable geometric sans-serif fonts (`BuilderSans`, `Gotham`, or `Montserrat`):
- **Title / Hero**: `24–32pt`, Weight: `Bold` (used for modal headers, shop titles).
- **Header / Section**: `18–22pt`, Weight: `SemiBold` (card titles, prominent counters).
- **Body / Interactive**: `14–16pt`, Weight: `Medium` (button labels, descriptions).
- **Caption / Metadata**: `11–13pt`, Weight: `Regular` (hotkey hints, rarity tags, level requirements).

---

## HERO ITEM SHOWCASES & 3D POP-OUT ARCHITECTURE ("THE 3D PICTURE LOOK")

Front-page Roblox titles (Pet Simulator, Blox Fruits, Sol's RNG, Deepwoken) achieve icons and item cards that look like cinematic 3D renders jumping off the screen. This "picture look" is an optical engineering pipeline combining five techniques:

### Technique 1: Live Interactive 3D ViewportFrames
Rather than flat 2D sprites, items (weapons, pets, artifacts, helmets) are rendered using a `ViewportFrame`:
- **Narrow FOV Telephoto Camera**: Standard camera FOV (70°) creates wide-angle barrel distortion that flattens items into fish-eyes. Set `Camera.FieldOfView = 25–35°` (isometric sweet spot is ~30°) and position the camera further back along the look vector. This produces orthographic-like isometric compression where silhouettes appear monumental, heroic, and cinematic.
- **Controlled Subject Positioning**: Calculate the model's bounding box using `:GetBoundingBox()`, center the model at `Vector3.zero`, and point `Camera.CFrame` toward `Vector3.zero` offset by `Vector3.new(0, heightOffset, distance)`.
- **Lighting & Studio Shading**: `ViewportFrame.Ambient = Color3.fromRGB(160, 170, 190)`, `ViewportFrame.LightColor = Color3.fromRGB(255, 250, 240)`, and `LightDirection = Vector3.new(-1, -1.5, -1).Unit`. For high-end pop, place small bright `PointLight` instances or secondary illuminated neon parts inside the ViewportFrame to cast localized specular highlights.
- **Dynamic Idle & Micro-Interactions**:
  - *Idle Spin*: Connect to `RunService.RenderStepped` to rotate the primary model CFrame along the Y axis at a smooth rate (`dt * math.rad(30)`).
  - *Mouse Tilt / Gyro Reaction*: On desktop hover, calculate mouse offset from the icon center `(mouseX - centerX) / cardWidth` and apply a subtle roll/pitch tilt (`math.clamp(offset * 0.15, -0.2, 0.2)` radians) toward the cursor, creating the tangible illusion of holding a physical collectible card in your hands.

### Technique 2: "Burst-Out-of-Frame" Layering (`ClipsDescendants = false`)
Flat icons look boxed in when clipped by rectangular card borders. Top games break the boundary:
- **Disabling Container Clipping**: The card container sets `ClipsDescendants = false`. The card background (the rounded rectangle or shield with `UICorner` and `UIStroke`) remains clipped or sized normally, but the hero item layer sits at a higher `ZIndex`.
- **Breaking the Boundary**: The `ViewportFrame` or hero icon is intentionally sized to `1.2x–1.4x` the parent card container (e.g. `UDim2.new(1.3, 0, 1.3, 0)`), with an AnchorPoint and Position that shifts the weapon's tip, dragon wings, or character's head past the top and side borders.
- **Depth Occlusion Layering**:
  1. *Backdrop Layer* (`ZIndex = 1`): Card background scrim, rarity gradient, drop shadow.
  2. *Back VFX Layer* (`ZIndex = 2`): Rotating sunburst / halo effect.
  3. *Hero Item Layer* (`ZIndex = 3`): ViewportFrame or hero silhouette breaking through borders (`ClipsDescendants = false`).
  4. *Frame Rim Layer* (`ZIndex = 4`): Embossed frame border or bottom banner (e.g. rarity badge, level ribbon) that partially overlaps the base of the item, locking it in place as if anchored inside a real display case.
  5. *Glass & Sheen Layer* (`ZIndex = 5`): Diagonal sweeping gloss sheen overlay.

### Technique 3: Rotating Sunburst / Rayburst Backdrop
Legendary and rare items project radiant energy with a circular rayburst behind the subject:
- **Asset Structure**: A circular `ImageLabel` displaying a 12-to-24 ray starburst/sunburst pattern with transparent gaps between rays.
- **Color & Transparency**: Tinted to the item's rarity accent color (e.g. Gold `#F59E0B` for Legendary, Purple `#8B5CF6` for Epic) with `ImageTransparency = 0.55–0.70` so it illuminates without overpowering the item silhouette.
- **Continuous Ambient Rotation**: Driven via `RunService.RenderStepped` updating `rayburst.Rotation = (rayburst.Rotation + 30 * dt) % 360` (see Pattern 9).
- **Pulsing Scale Breathing**: A subtle tweening loop oscillating `Size` between `1.0x` and `1.12x` over 2 seconds (`EasingStyle.Sine`, `EasingDirection.InOut`, repeat count -1, reverses true) adds a living heartbeat.

### Technique 4: Diagonal Sweeping Sheen / Foil Gloss (`UIGradient` Shine)
Collectibles and front-page loot have a dynamic holographic foil shine that sweeps diagonally across the surface:
- **Overlay Setup**: An empty `Frame` placed above the card (`ZIndex = 5`) matching the card dimensions, with `BackgroundTransparency = 0`, `BackgroundColor3 = Color3.fromRGB(255, 255, 255)`, and matching `UICorner`.
- **Diagonal `UIGradient` Configuration**: `Rotation = 45` with a 5-keypoint sequence creating a crisp central light band (edges transparency 1.0, central gleam at 0.50 with transparency 0.15; see Pattern 8).
- **Offset Sweeping Tween**: Start at `Offset = Vector2.new(-1, -1)` (off-screen top-left) and tween to `Offset = Vector2.new(1, 1)` (past bottom-right) over 0.75–1.1s (`EasingStyle.Quad`). Sweep once on card reveal, then repeat every 3 to 5 seconds on rare/legendary items.

### Technique 5: Multi-Point Studio Lighting in 2D
To make subjects pop against dark backgrounds without muddying:
- **Key Light (Top-Left)**: Strong directional light (`LightDirection = Vector3.new(-1, -1.2, -0.8).Unit`, bright warm white `Color3.fromRGB(255, 252, 245)`) that defines form and surface normals.
- **Fill Light (Bottom-Right)**: Softer ambient fill (`Ambient = Color3.fromRGB(140, 150, 175)`) tinted slightly cool slate to simulate environmental bounce light and prevent pure black shadows under crevices.
- **Rim / Back Light**: A high-intensity backlight or contrasting silhouette rim (`UIStroke` on 2D cutouts or neon rim geometry in 3D ViewportFrames) separating dark subject edges from dark card backings. This silhouette halo is what human vision interprets as crisp "studio isolation".

---

## DECISION TREE

```text
1. WHAT DECISION DOES THE PLAYER MAKE?
   Every screen answers one question (what is my status? what can I buy? where do I go?).
   If a screen has no decision or feedback purpose, cut it.

2. WHERE DOES IT LIVE?
   Persistent HUD          → StarterGui ScreenGui, ResetOnSpawn = false
   Per-round / per-death   → StarterGui, ResetOnSpawn = true
   Menus & Modals          → one ScreenGui with frames toggled, not many ScreenGuis
   Floating Prompts/FX     → ReplicatedStorage template cloned by client controller

3. HOW DOES IT SIZE & ANCHOR?
   Scale for responsive layout and anchors; Offset strictly for padding, borders, and tactile details.
   AnchorPoint set intentionally (e.g. Vector2.new(0.5, 0.5) for centered cards).
   Constraints: UIAspectRatioConstraint for icons, UISizeConstraint for button limits.
   Verify at: Phone (320×480, 390×844), Tablet (768×1024), Desktop (1920×1080), TV/Console (4K/10-foot).

4. DOES IT SATISFY THE VISUAL POLISH STANDARD?
   - Anti-cancellation: Dual-boundary stroke on text; scrim backing behind HUD groups.
   - Depth: Embossed UIGradient on UIStroke; subtle 9-slice drop shadow behind container.
   - Tangibility: Tweened hover scale (1.05x), click depression (0.95x), and audio ticks.
   - Iconography: Vector icon paired with every interactive button or stat value.

5. HOW DOES IT GET STATE?
   Server → RemoteEvent → client controller → UI API (e.g. HUD:SetHealth(n)).
   UI never computes authoritative values and never writes gameplay state directly.
   Buttons send intent; server validates; UI reflects result with optimistic rollback on rejection.

6. HOW DOES IT GET INPUT ON EVERY DEVICE?
   Touch: ≥44×44 px targets, respect ScreenInsets = CoreUISafeInsets (avoid notches/controls).
   Gamepad: explicit focus order, NextSelection*, visual cursor highlight, Back button closes modal.
   Keyboard/Mouse: hotkey badges visible in UI, hover states active, Esc closes topmost modal.

7. IS IT READABLE AND INCLUSIVE?
   Contrast ≥4.5:1; no chromostereopsis; no isoluminant text; multi-modal cues for colorblindness.
   Respect PreferredTextSize, ReducedMotionEnabled (replace springs with fades), PreferredTransparency.
```

---

## PATTERNS

### 1. AAA ScreenGui & Layer Hierarchy
```text
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

## FAILURE MODES & MITIGATIONS

1. **Chromostereopsis Eye Strain**: Pure red button on pure green background or saturated blue on red.
   *DETECT:* Optical vibration or depth illusion during visual testing.
   *FIX:* Desaturate backing layers; insert dark neutral isolation strokes or neutral scrim boundaries.
2. **Isoluminant Text Washout**: Yellow text on white modal; blue text on dark gray/black background.
   *DETECT:* Grayscale conversion renders text and background as the same shade of gray; text unreadable in bright environments.
   *FIX:* Ensure luminance contrast ≥4.5:1; apply Dual-Boundary `UIStroke` (`Color3.fromRGB(12,16,24)`).
3. **Bare Text Amateur Buttons**: Rectangular buttons with centered plain text and no icons.
   *DETECT:* UI lacks polish; resembles debugging placeholder.
   *FIX:* Pair with vector icons (Lucide icon style); add `UICorner` (6–8px), embossed `UIStroke`, and drop shadow.
4. **Flat / Dead Affordances**: Buttons that do not react when hovered, pressed, or clicked.
   *DETECT:* Player clicks and wonders if the game registered the input.
   *FIX:* Add tactile micro-interactions (1.05x hover spring, 0.95x click depression, `UISound` click trigger).
5. **Washout Over Dynamic 3D Worlds**: White text disappearing when camera pans into the skybox or a bright explosion.
   *DETECT:* In-game camera movement causes UI illegibility.
   *FIX:* Enforce protective scrim frames (`BackgroundTransparency = 0.3`) and Dual-Boundary `UIStroke`.
6. **Respawn HUD Wipe**: `ResetOnSpawn` left true on persistent HUDs.
   *DETECT:* Player dies and HUD blinks out or state bindings break.
   *FIX:* Set `ResetOnSpawn = false` on persistent HUD ScreenGuis.
7. **Offset-Only Breakage**: UI laid out using absolute pixel offsets.
   *DETECT:* Elements clip or overlap on mobile phones or ultra-wide monitors.
   *FIX:* Lay out with Scale + AnchorPoint + `UIAspectRatioConstraint`/`UISizeConstraint`.
8. **Client-Authoritative UI**: UI deducts gold locally before server responds.
   *DETECT:* Coin balance snaps back or desyncs from server inventory.
   *FIX:* One-way data binding: client sends intent → server confirms → UI renders.

---

## QUANTITATIVE RULES

- **Luminance Contrast**: Body text ≥4.5:1; large text/headers ≥3:1 against backing scrim or background.
- **Dual-Boundary Stroke**: Thickness `1.5–2.5px`, `Transparency = 0.15–0.25` on all scene-overlay text.
- **Scrim Backing**: Slate/Carbon tint, `BackgroundTransparency = 0.25–0.35`, `UICorner` `6–10px`.
- **Embossed Rim**: `UIStroke` `2–3px` with vertical `UIGradient` (top specular highlight → bottom ambient shade).
- **Touch Targets**: Minimum `44×44 px` interactive area on mobile devices.
- **Micro-Interaction Timings**: Hover tween `100–140ms` (`EasingStyle.Back` or `Quad`); Press `60–90ms`.
- **Typographic Scale**: Title `24–32pt`, Header `18–22pt`, Body `14–16pt`, Caption `11–13pt`.
- **Viewport Verification**: Must test at 320×480 (compact phone), 768×1024 (tablet), 1920×1080 (standard desktop), and TV 10-foot viewing distance.

---

## VERIFICATION GATE

- [ ] Original purpose and user decision clearly supported by the screen.
- [ ] Hero 3D Showcases configured with narrow FOV camera (~30°), 3-point lighting, and idle spin/tilt.
- [ ] Burst-Out-of-Frame layering enforced (`ClipsDescendants = false` on hero card containers).
- [ ] Rotating rayburst and diagonal foil sheen gloss applied to rare/legendary showcases.
- [ ] Optical Anti-Vibration enforced: zero chromostereopsis (no pure red/green or blue/red collisions).
- [ ] Anti-cancellation verified: zero isoluminant text pairings; dual-boundary `UIStroke` on all scene-overlay text.
- [ ] Scrim backing frames present behind floating HUD clusters (`BackgroundTransparency 0.25–0.35`).
- [ ] AAA Visual Polish applied: embossed gradient borders, subtle drop-shadow frames, and glassmorphic styling.
- [ ] Curated vector icons paired with all stats, tabs, action buttons, and inventory slots (no bare text buttons).
- [ ] Tactile micro-interactions functional: hover expansion (1.05x), click depression (0.95x), and audio chimes.
- [ ] Rarity tokens and color accents adhere to standard tier palette (Common Slate to Mythic Ruby).
- [ ] Multi-modal cues present: no state or rarity communicated by hue alone (icon + label + value).
- [ ] Responsive layout validated across mobile (phone/tablet) and desktop viewports without clipping.
- [ ] Gamepad navigation path explicit and tested; Back button closes topmost modal.
- [ ] One-way state binding: server authoritative, client optimistic with rollback, no direct remote writes from UI.
