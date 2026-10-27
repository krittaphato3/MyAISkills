---
name: ui-layout-spacing
description: >-
  Governs visual layout, whitespace hierarchy, spatial rhythm, and component arrangement across
  web and Roblox interfaces: 8pt/4pt proportional spacing scale, spatial nesting law (decreasing
  inward), container enclosure formula (outer padding >= inner gap), concentric corner radius
  geometry, squish padding for buttons/badges, optical vs mathematical alignment, and intrinsic
  responsive CSS Grid / Roblox UIListLayout arrangements. Use when designing, arranging, spacing,
  or fixing gaps, padding, margins, visual clutter, cramped layouts, or misaligned interface elements.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G3
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: ui-ux-architect
---

# UI Layout & Spacing Architecture

A mathematically rigorous, perception-grounded spatial system for web and Roblox interfaces. White space is not empty canvas—it is visual grammar that establishes relationships, reading flow, and hierarchical grouping without artificial borders or dividers.

## WHEN TO USE

- Defining, refactoring, or auditing UI whitespace, padding, margins, and component layout gaps.
- Fixing cramped layouts, uneven gutter rhythms, visual clutter, or awkward element clustering.
- Calculating nested corner radii to ensure visual concentricity across bordered or cards-in-card containers.
- Aligning asymmetric icons (play triangles, chevrons), mixed-case headings, or badges with buttons.
- Configuring responsive flexbox/grid containers or Roblox Studio `UIListLayout` / `UIPadding` structures.
- Eliminating arbitrary "magic pixel" offsets (e.g., 7px, 13px, 19px, 27px) in favor of systematic scales.

## WHEN NOT TO USE

- Choosing overall visual art direction, theme mood, or brand aesthetic (use `impeccable`).
- Palette generation, color contrast tuning, or elevation shadows (use `refactoring-ui`).
- Studio 3D viewport hero icons, rayburst backdrops, or material shaders (use `roblox-ui-ux`).
- Pure WCAG AA assistive tech / screen-reader accessibility auditing (use `accessibility-audit`).

---

## 1. SPATIAL FOUNDATIONS: 8-POINT & 4-POINT GRID SYSTEM

Every dimension, padding, margin, and gap adheres to an integer multiple of 8 (with 4 as the half-step sub-grid for tight inline components and icons).

### The Spatial Token Scale

| Token | Pixels | Rem (16px base) | Tailwind Class | Primary Role / Usage Context |
|---|---|---|---|---|
| `space-0.5` | 2px | 0.125rem | `gap-0.5` / `p-0.5` | Hairline offsets, optical nudges, tight borders |
| `space-1` | 4px | 0.25rem | `gap-1` / `p-1` | Compact icon gaps, badge vertical padding |
| `space-2` | 8px | 0.5rem | `gap-2` / `p-2` | Tight inline item spacing, input internal padding |
| `space-3` | 12px | 0.75rem | `gap-3` / `p-3` | Medium button vertical padding, form field gaps |
| `space-4` | 16px | 1.0rem | `gap-4` / `p-4` | Standard card internal padding, list row gaps |
| `space-6` | 24px | 1.5rem | `gap-6` / `p-6` | Large card padding, modal content padding |
| `space-8` | 32px | 2.0rem | `gap-8` / `p-8` | Section sub-group gaps, modal padding |
| `space-12` | 48px | 3.0rem | `gap-12` / `p-12` | Major section breaks, hero content spacing |
| `space-16` | 64px | 4.0rem | `gap-16` / `p-16` | Page section dividers, viewport margins |
| `space-24` | 96px | 6.0rem | `gap-24` / `p-24` | Landing page hero separators, chapter transitions |

---

## 2. THE SPATIAL NESTING LAW (LAW OF PROXIMITY)

Elements that are related must be closer together than elements that are unrelated. In hierarchical UI, **spacing must strictly decrease as nesting depth increases**:

$$\text{Outer Section Margin} > \text{Card Container Padding} > \text{Element Group Gap} > \text{Label-to-Input Gap}$$

### Spatial Hierarchy Ladder

1. **Page Section Margin / Grid Gutter (`48px – 96px`)**: Separates autonomous conceptual domains.
2. **Container Padding (`24px – 32px`)**: Bounds a cohesive module or card.
3. **Component Group Gap (`16px – 24px`)**: Separates sibling cards, form blocks, or button rows.
4. **Item Sibling Gap (`8px – 12px`)**: Space between list items, table rows, or button groups.
5. **Atomic Internal Gap (`4px – 8px`)**: Distance from label to input, icon to text, or badge to title.

*Failure Mode*: When an inner gap is equal to or larger than an outer gap, visual grouping shatters and the user cannot perceive container boundaries.

---

## 3. THE CONTAINER ENCLOSURE RULE

To preserve the perceptual unity of a container (Gestalt law of common region), the inner child spacing must never overwhelm the outer frame:

$$\text{Outer Container Padding} \ge \text{Inner Child Gap}$$

- If a card has an inner gap between children of `16px`, container padding must be **at least 16px** (ideally `20px` or `24px`).
- If an inner gap is `24px` while padding is `16px`, children will feel visually ejected out of the container towards neighboring sections.
- **Rule of Thumb**: Set outer padding to $1.25\times$ to $1.5\times$ the child element gap.

---

## 4. CONCENTRIC CORNER RADIUS GEOMETRY

When nesting a rounded element inside a rounded container with a border or padding, uniform radii look distorted and pinched. To achieve perfect optical concentricity:

$$R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$$

$$\text{Conversely: } R_{\text{inner}} = \max(0, R_{\text{outer}} - \text{Padding})$$

### Radius Calculation Examples

| Outer Radius ($R_{\text{outer}}$) | Padding ($P$) | Inner Radius ($R_{\text{inner}}$) | Visual Appearance |
|---|---|---|---|
| 24px | 8px | 16px | Perfectly concentric curve |
| 16px | 8px | 8px | Smooth parallel border flow |
| 16px | 16px | 0px (Square) | Inner element reaches straight edge |
| 12px | 16px | 0px | Inner element cannot be rounded |

*Pitfall*: Setting both outer container and inner card to `rounded-xl` (12px) with `p-4` (16px) makes the inner card look detached and warped at the corners.

---

## 5. SQUISH PADDING LAW (ASYMMETRIC BUTTONS & BADGES)

Text is wider than it is tall, and letterforms already carry inherent vertical whitespace (ascenders and descenders). Pure square padding makes pills, buttons, and badges look uncomfortably tall and choked horizontally.

$$\text{Horizontal Padding} = 1.5\times \text{ to } 2.0\times \text{Vertical Padding}$$

### Standard Squish Scale

- **Compact Badge / Tag**: `py-0.5 px-2` (2px vertical, 8px horizontal — ratio 4.0×) or `py-1 px-2.5` (4px vertical, 10px horizontal — ratio 2.5×)
- **Small Button**: `py-1.5 px-3` (6px vertical, 12px horizontal — ratio 2.0×)
- **Standard Button**: `py-2 px-4` (8px vertical, 16px horizontal — ratio 2.0×)
- **Large CTA Button**: `py-3 px-6` (12px vertical, 24px horizontal — ratio 2.0×)
- **Hero Button**: `py-4 px-8` (16px vertical, 32px horizontal — ratio 2.0×)

---

## 6. OPTICAL VS MATHEMATICAL ALIGNMENT

Geometric centers frequently conflict with human perceptual centers. Mathematical alignment produces visually drifting elements.

### 1. Play Icon Triangle Optical Center
- A play button triangle inside a circle has its centroid skewed toward its base.
- **Correction**: Shift the triangle horizontally toward the tip by **+10% to +14%** of its width (or +1px to +2px for a 16px icon) to align its perceptual mass with the circle's center.

### 2. Cap-Height Text Alignment
- Digital fonts place text within a bounding box that includes space for accents, descenders, and ascenders.
- Aligning an icon to a text bounding box aligns the icon to the box, not the capital letters.
- **Correction**: Align icons and badges to font **cap-height** using flexbox `items-center` with explicit line-height control (`leading-none` or manual relative translate `top-[1px]`).

### 3. Circle vs Square Visual Weight
- A circle inscribed inside an $N \times N$ square occupies only $\frac{\pi}{4} \approx 78.5\%$ of the square's area.
- Next to a square or rounded card of identical height, a circle looks noticeably smaller.
- **Correction**: Scale circular avatars and icon badges up by **10% to 15%** in diameter compared to adjacent rectangular buttons or inputs to balance visual weight.

---

## 7. IMPLEMENTATION GUIDES

### A. Web Implementation (Tailwind CSS, Flexbox & CSS Grid)

```tsx
// Modern responsive card grid adhering to spatial nesting & concentric radii
export function FeatureCardGroup() {
  return (
    <section className="my-16 max-w-7xl mx-auto px-6"> {/* Outer Section: 64px / 24px */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6"> {/* Sibling Gap: 24px */}
        
        {/* Outer Card: R_outer = 24px (rounded-3xl), Padding = 24px (p-6) */}
        <div className="rounded-3xl p-6 bg-slate-900 border border-slate-800 flex flex-col gap-4">
          
          {/* Inner Highlight: R_inner = 24px - 8px = 16px (rounded-2xl) */}
          <div className="rounded-2xl p-4 bg-slate-800/60 flex items-center gap-3">
            <span className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
              {/* Optical center: nudge play icon right by 1px */}
              <PlayIcon className="w-5 h-5 text-indigo-400 translate-x-[1px]" />
            </span>
            <span className="text-sm font-medium text-slate-200">Active Pipeline</span>
          </div>

          <div className="space-y-1"> {/* Tight text nesting: 4px */}
            <h3 className="text-lg font-semibold text-white tracking-tight">Spatial Hierarchy</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Padding decreases inwardly to preserve natural visual groupings.
            </p>
          </div>

          <div className="mt-auto pt-2 flex items-center justify-between">
            {/* Squish padding: py-1.5 px-3 (1:2 ratio) */}
            <span className="py-1 px-2.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400">
              Verified
            </span>
            {/* Squish padding button */}
            <button className="py-2 px-4 rounded-xl text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-500 transition-colors">
              Configure
            </button>
          </div>

        </div>

      </div>
    </section>
  );
}
```

### B. Roblox Studio Implementation (UDim2, UIListLayout, UIPadding)

```lua
-- Roblox spatial layout builder conforming to concentric radii and 8pt grid
local function createConcentricCard(parent: Instance, name: string): Frame
    -- Outer Card Container
    local card = Instance.new("Frame")
    card.Name = name or "ConcentricCard"
    card.Size = UDim2.new(0, 320, 0, 240)
    card.BackgroundColor3 = Color3.fromRGB(24, 27, 36)
    card.BorderSizePixel = 0
    
    -- Outer Corner Radius: 20px
    local outerCorner = Instance.new("UICorner")
    outerCorner.CornerRadius = UDim.new(0, 20)
    outerCorner.Parent = card
    
    -- Outer Padding: 16px on all sides
    local padding = Instance.new("UIPadding")
    padding.PaddingTop = UDim.new(0, 16)
    padding.PaddingBottom = UDim.new(0, 16)
    padding.PaddingLeft = UDim.new(0, 16)
    padding.PaddingRight = UDim.new(0, 16)
    padding.Parent = card
    
    -- Vertical flow layout with 12px child gap (outer padding 16px > inner gap 12px)
    local listLayout = Instance.new("UIListLayout")
    listLayout.FillDirection = Enum.FillDirection.Vertical
    listLayout.SortOrder = Enum.SortOrder.LayoutOrder
    listLayout.Padding = UDim.new(0, 12)
    listLayout.Parent = card
    
    -- Inner Child Item: R_inner = R_outer - Padding = 20 - 16 = 4px
    local innerHeader = Instance.new("Frame")
    innerHeader.Name = "HeaderFrame"
    innerHeader.Size = UDim2.new(1, 0, 0, 48)
    innerHeader.BackgroundColor3 = Color3.fromRGB(35, 40, 52)
    innerHeader.BorderSizePixel = 0
    innerHeader.LayoutOrder = 1
    
    local innerCorner = Instance.new("UICorner")
    innerCorner.CornerRadius = UDim.new(0, 4)
    innerCorner.Parent = innerHeader
    innerHeader.Parent = card
    
    -- Squished Action Button: Height 36px, horizontal padding 16px vs vertical 8px
    local button = Instance.new("TextButton")
    button.Name = "ActionButton"
    button.Size = UDim2.new(1, 0, 0, 40)
    button.BackgroundColor3 = Color3.fromRGB(79, 70, 229)
    button.Font = Enum.Font.GothamBold
    button.TextSize = 14
    button.TextColor3 = Color3.fromRGB(255, 255, 255)
    button.Text = "Collect Reward"
    button.LayoutOrder = 2
    
    local btnCorner = Instance.new("UICorner")
    btnCorner.CornerRadius = UDim.new(0, 8)
    btnCorner.Parent = button
    button.Parent = card
    
    card.Parent = parent
    return card
end
```

---

## 8. VERIFICATION CHECKLIST

Every UI layout review or authoring task must pass these checks:

1. **The Squint Test (Blur Check)**:
   - Squint your eyes or apply `filter: blur(5px)`.
   - Distinct cards, panels, and sections must remain identifiable as discrete blocks. If related items dissolve into unrelated clusters, inner gaps are too large or outer padding is too small.
2. **Spacing Cadence Audit**:
   - Check all CSS / UDim2 values: every gap, margin, and padding must come from the 8pt/4pt token table (0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96). Zero arbitrary values.
3. **Nesting Ratio Check**:
   - Verify: $\text{Outer Container Padding} \ge \text{Inner Child Gap}$.
   - Verify: $\text{Element Group Gap} > \text{Label-to-Input Gap}$.
4. **Concentricity Verification**:
   - If an inner element is rounded within a rounded card, compute $R_{\text{inner}} = R_{\text{outer}} - \text{Padding}$. Verify no optical corner warping occurs.
5. **Button & Badge Squish Check**:
   - Confirm horizontal padding is at least $1.5\times$ to $2.0\times$ vertical padding.
6. **Optical Centering Audit**:
   - Triangles, chevrons, and directional arrows inside centered containers have appropriate offset compensation (+10–14%).

---

## VERIFICATION GATE

- All layout spacing values strictly adhere to the 4pt/8pt scale token dictionary.
- No container violates the enclosure formula (Outer padding >= inner child gap).
- Concentric corner radii satisfy $R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$.
- Buttons and badges satisfy the squish ratio ($P_x \ge 1.5 P_y$).
- The interface passes the Squint Test with distinct visual chunking.
