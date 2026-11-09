# roblox-ui-ux — COLOR HARMONY & ANTI-CANCELLATION DOCTRINE

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
