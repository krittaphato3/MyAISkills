# roblox-ui-ux — HERO ITEM SHOWCASES & 3D POP-OUT ARCHITECTURE ("THE 3D PICTURE LOOK")

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
