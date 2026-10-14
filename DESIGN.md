---
name: Municipal Telemetry & Civic Trust
colors:
  surface: '#0f131c'
  surface-dim: '#0f131c'
  surface-bright: '#353942'
  surface-container-lowest: '#0a0e16'
  surface-container-low: '#181c24'
  surface-container: '#1c2028'
  surface-container-high: '#262a33'
  surface-container-highest: '#31353e'
  on-surface: '#dfe2ee'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dfe2ee'
  inverse-on-surface: '#2c3039'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#adc6ff'
  on-secondary: '#002e6a'
  secondary-container: '#0566d9'
  on-secondary-container: '#e6ecff'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#1bbd85'
  on-tertiary-container: '#00452e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0f131c'
  on-background: '#dfe2ee'
  surface-variant: '#31353e'
typography:
  headline-xl:
    fontFamily: Geist
    fontSize: 3rem
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Geist
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Geist
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 0.9375rem
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  body-sm:
    fontFamily: Inter
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: '1.45'
    letterSpacing: 0.005em
  telemetry-value:
    fontFamily: JetBrains Mono
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  telemetry-meta:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: '1.3'
    letterSpacing: 0.04em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.08em
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-2xs: 0.125rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system serves a dual mandate: mission-critical municipal operational intelligence and radically transparent public civic engagement. 

The aesthetic is anchored in **Instrumental Precision**: authoritative, institutional, high-density, and utilitarian. It rejects generic SaaS decoration, vague drop shadows, and ornamental organic blobs in favor of structural grid lines, micro-borders, dense data readouts, and calibrated contrast tiers. 

The dual personas adapt seamlessly:
- **Operations Command Mode (Dark):** Tailored for emergency response leads, urban planners, public works dispatchers, and council monitors. Evokes the high-stakes situational awareness of aerospace mission control and aerospace telemetry: obsidian canvases, glowing signal cyan indicators, monospaced coordinate markers, and instant optical triage.
- **Citizen Portal Mode (Light):** Geared toward community residents reporting infrastructure faults, tracking civic resolutions, and inspecting municipal audits. Evokes democratic clarity, stability, and public institutional trust: warm alabaster-slate backdrops, crisp editorial line weights, accessible indigo-slate contrast, and digestible civic communication.

## Colors

The system uses an intentional functional palette where color strictly communicates state, telemetry density, and operational urgency rather than decoration.

### Operational Command (Dark Mode - Primary System State)
- **Base Canvas (`bg-base`):** `#0B0F17` — Deep void navy-black, minimizing eye fatigue during continuous control-room shifts.
- **Surface Elevation 1 (`surface-subtle`):** `#111827` — Base containment for instrument panels and secondary trays.
- **Surface Elevation 2 (`surface-panel`):** `#162032` — Interactive cards, telemetry modules, and popover contexts.
- **Structural Rules & Grid Lines:** `#1E293B` (low-contrast structural grid) and `#334155` (active interactive borders).
- **Signal Primaries:** Cyan (`#06B6D4`) for system focus, operational hooks, and active spatial coordinates; Signal Blue (`#3B82F6`) for confirmed commands and baseline directional actions.

### Citizen Portal (Light Mode Extension)
- **Base Canvas:** `#F8FAFC` (Slate-50) paired with `#FFFFFF` card substrates.
- **Typography Base:** Deep Navy Slate (`#0F172A`) providing high-contrast readability exceeding WCAG AAA standards.
- **Civic Blue Accent:** `#2563EB` delivering dependable, institutional authority for primary public CTAs and feedback loops.
- **Subtle Partitioning:** `#E2E8F0` and `#CBD5E1` for delicate, physical division without visual noise.

### Telemetry & Severity Status Tokens
Semantic indicators remain strictly standardized across both modes to prevent cognitive disorientation during cross-system handoffs:
- **Critical / Emergency (`status-crimson`):** `#EF4444`
- **Warning / Pending Dispatch (`status-amber`):** `#F59E0B`
- **Nominal / Resolved (`status-emerald`):** `#10B981`
- **Automated AI Routing / Advisory (`status-violet`):** `#8B5CF6`

## Typography

The typography framework balances technical rigor with broad civic legibility:

- **Headlines (Geist):** Clean, machined, and authoritative. Tabular figures and condensed horizontal proportion support information-dense dashboards without feeling cramped.
- **Body & Continuous Prose (Inter):** Highly legible across varied screen resolutions and brightness conditions, with tall x-height and open apertures suited for municipal briefs and resident communications.
- **Telemetry, Metrics & Identifiers (JetBrains Mono):** Reserved for technical instrumentation: GPS coordinates, timestamp logs, dispatch incident codes (e.g., `#INC-8092-B`), model confidence scores, and raw infrastructural metrics.
- **Text Transformations:** Section tags, radar indicators, and telemetry statuses utilize uppercase tracking via `label-caps` to reinforce the operational control aesthetic.

## Layout & Spacing

The structural layout is based on a rigid 8px unit grid (with a 4px sub-grid for dense micro-telemetry cards). 

### Layout Architecture
- **Operations Command (Dark):** Fixed, full-viewport dashboard arrangement (`100vh`, non-scrolling parent shell). Uses a dense multi-pane dock system: collapsible left vertical rail (56px collapsed / 240px expanded), central fluid spatial map or chart viewport, and fixed 380px contextual telemetry right rail. Panes are divided by 1px solid border rules without floating margins.
- **Citizen Portal (Light):** Responsive 12-column layout maxing out at `1200px` centered canvas with generous `margin-desktop` gutters to guide resident eye-tracking and prioritize single-column action funnels.

### Breakpoints & Reflow
- **Desktop (>= 1280px):** Full telemetry triage; multi-column metrics; persistent tactical map view.
- **Tablet (768px - 1279px):** Contextual sidebars collapse to slide-over drawers; 6-column modular card layout.
- **Mobile (< 768px):** Linear single-column flow; spatial maps degrade to card feeds with toggleable full-screen map mode; high-priority triage metrics pinned to persistent bottom utility bar.

## Elevation & Depth

This system intentionally bypasses heavy blur-based ambient drop shadows and skeuomorphic gradients in favor of **Structural Micro-Borders** and **Tonal Planar Stacking**.

### Operational Mode (Dark)
- **Level 0 (Canvas):** Pure base tone (`#0B0F17`).
- **Level 1 (Panels):** Tonal lift (`#111827`) bounded by a hairline border (`1px solid #1E293B`).
- **Level 2 (Interactive Modules):** `#162032` encased in `1px solid #334155`.
- **Level 3 (Alert Overlays & Modals):** Elevated surface `#1E293B` highlighted with a sharp top-edge highlight (`1px solid #06B6D4`) and a constrained dark perimeter rim (`0 0 0 1px #06B6D4, 0 16px 32px -8px rgba(0, 0, 0, 0.8)`).
- **Focus / Tactical Ping:** Subtle electric cyan glow (`0 0 0 1px #06B6D4, 0 0 12px rgba(6, 182, 212, 0.25)`).

### Citizen Mode (Light)
- **Level 0 (Canvas):** Crisp `#F8FAFC`.
- **Level 1 (Cards):** `#FFFFFF` bordered with `1px solid #E2E8F0`.
- **Level 2 (Active Focus):** `#FFFFFF` paired with an offset hairline shadow (`0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`) and clear civic outline (`1px solid #CBD5E1`).

## Shapes

The design uses a **Level 0 (Sharp)** shape geometry. 

Cards, modals, data inputs, tags, and operational buttons utilize razor-sharp `0px` border radii. This reinforces the municipal terminal, hardware-console paradigm:
- Rectilinear panels create clear, uncompromised screen division, eliminating visual dead space at corner intersections.
- Tactical pill exceptions (`rounded-full`) are strictly forbidden for layout wrappers and cards; only status dot indicators and circular mini-avatars may deviate from the strict rectilinear rule.
- Input elements, telemetry badges, and buttons sit as crisp geometric rectangles, aligning flush against neighboring modules.

## Components

### Buttons
- **Command Primary:** Sharp-cornered, filled Cyan `#06B6D4` with contrasting dark `#0B0F17` bold typography. Hover triggers opacity shift to `#22D3EE` with an inner 1px white border flash.
- **Civic Primary (Citizen Mode):** Sharp-cornered `#2563EB` with `#FFFFFF` text. Hover shifts to `#1D4ED8`.
- **Secondary / Tactical Outline:** Transparent fill, `1px solid #334155` border, monospaced uppercase typography. On hover, background shifts to `#162032` with border shifting to `#06B6D4`.

### Telemetry Badges & Chips
- **Structural Spec:** Monospaced `0.6875rem`, all-caps, `padding: 2px 6px`, `0px` radius.
- **States:**
  - *Critical:* Dark crimson background (`rgba(239, 68, 68, 0.15)`), borders `#EF4444`, text `#FCA5A5`. Includes a blinking 6px square status indicator.
  - *Active Route / Processing:* Dark violet background (`rgba(139, 92, 246, 0.15)`), borders `#8B5CF6`, text `#DDD6FE`.
  - *Nominal:* Dark emerald background (`rgba(16, 185, 129, 0.15)`), borders `#10B981`, text `#6EE7B7`.

### Input Fields & Controls
- **Command Inputs:** Background `#0B0F17`, hairline border `1px solid #334155`, text `#F8FAFC`. Focus ring utilizes a sharp cyan outline (`0 0 0 1px #06B6D4`) without soft blur.
- **Citizen Inputs:** Background `#FFFFFF`, border `1px solid #CBD5E1`, text `#0F172A`, focus border `1px solid #2563EB`.
- **Checkboxes & Radios:** Squared `0px` frames. Checked state fills with cyan (Command) or blue (Citizen) with a centered solid square icon rather than soft curves.

### Telemetry Cards & Panels
- Constructed with high-density card headers featuring monospaced tracking IDs (`#REF-4091`) aligned opposite status markers.
- Internal card splitters use `1px solid #1E293B` rules.
- Numerical values feature large tabular figures (`telemetry-value`) with stacked lowercase units directly adjacent (e.g., `42.8 ms` or `94.2 %`).

### Specialized Domain Components
- **Geospatial Crosshair Callout:** Rectangular dark badge anchored by 1px vector leader lines linking map markers to real-time coordinate data (`LAT/LONG` format in monospaced font).
- **Incident Severity Escalator:** 4-stage segmented bar indicator rendered as contiguous sharp rectangles that illuminate progressively from emerald to amber to crimson.
- **Audit Verification Stamp:** Citizen-facing verified cryptographic confirmation badge using monospace serial codes, structured date blocks, and high-contrast seal boundaries.