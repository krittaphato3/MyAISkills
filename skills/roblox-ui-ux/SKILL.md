---
name: roblox-ui-ux
description: 'Designs and builds Roblox interfaces with AAA visual polish: ScreenGui structure, UDim2
  sizing, safe areas, HUD state binding, tactile micro-interactions, curated vector icons, anti-cancellation
  contrast, and 3D pop-out hero showcases (interactive ViewportFrames, burst-out cards, sheen gloss, rayburst
  backdrops, studio lighting). Use when building or styling any HUD, menu, shop, inventory, modal, prompt,
  crate/gacha showcase, or badge needing front-page quality. World lighting and geometry route to roblox-world-building;
  tweened character motion to roblox-animation.'
metadata:
  version: 1.3.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-11-09'
  authored-by: roblox-ui-designer
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

Full detail: `references/color-harmony-anti-cancellation-doctrine.md`.

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

Full detail: `references/hero-item-showcases-3d-pop-out-architecture-the-3d-picture-l.md`.

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

### 1.
AAA ScreenGui & Layer Hierarchy
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

Full detail: `references/patterns.md`.

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

## REFERENCES

- `roblox-assets` - icons, textures, and 9-slice assets these patterns consume.
- `ui-layout-spacing` - the spacing, radius, and enclosure math.
- `roblox-vfx-artist` - UI particles, sheen, and sound.
- `roblox-world-building` - the lighting that glass and embossed surfaces are tuned for.
- `accessibility-audit` - contrast targets adapted for game HUDs.
