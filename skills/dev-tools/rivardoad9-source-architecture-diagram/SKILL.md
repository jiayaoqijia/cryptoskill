---
name: architecture-diagram
description: "Dark-themed SVG architecture/cloud/infra diagrams as HTML."
version: 1.0.0
author: Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [architecture, diagrams, SVG, HTML, visualization, infrastructure, cloud]
    related_skills: [concept-diagrams, excalidraw]
---

# Architecture Diagram Skill

Generate professional, dark-themed technical architecture diagrams as standalone HTML files with inline SVG graphics. No external tools, no API keys, no rendering libraries — just write the HTML file and open it in a browser.

## Scope

**Best suited for:**
- Software system architecture (frontend / backend / database layers)
- Cloud infrastructure (VPC, regions, subnets, managed services)
- Microservice / service-mesh topology
- Database + API map, deployment diagrams
- **Process / workflow flows** (request → gate → queue → parallel workers → result): lay these out as a vertical spine, not a wide left-to-right strip, so the diagram stays legible on a phone
- Anything with a tech-infra subject that fits a dark, grid-backed aesthetic

**Look elsewhere first for:**
- Physics, chemistry, math, biology, or other scientific subjects
- Physical objects (vehicles, hardware, anatomy, cross-sections)
- Floor plans, narrative journeys, educational / textbook-style visuals
- Hand-drawn whiteboard sketches (consider `excalidraw`)
- Animated explainers (consider an animation skill)

If a more specialized skill is available for the subject, prefer that. If none fits, this skill can also serve as a general SVG diagram fallback — the output will just carry the dark tech aesthetic described below.

Based on [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT).

## Workflow

1. User describes their system architecture (components, connections, technologies)
2. Generate the HTML file following the design system below
3. Save with `write_file` to a `.html` file (e.g. `~/architecture-diagram.html`)
4. User opens in any browser — works offline, no dependencies

### Output Location

Save diagrams to a user-specified path, or default to the current working directory:
```
./[project-name]-architecture.html
```

### Preview

After saving, suggest the user open it:
```bash
# macOS
open ./my-architecture.html
# Linux
xdg-open ./my-architecture.html
```

## Delivering as an Image (chat, Telegram, docs)

HTML is for when the user opens the file themselves. When the diagram *is* the answer in a chat, render a PNG and send that.

1. **Render the SVG standalone.** Then screenshot pixels equal viewBox pixels: `html, body { margin: 0; padding: 0 }` and an explicit `<svg width="1100" height="1240" viewBox="0 0 1100 1240">`. Put the title *inside* the SVG. With a padded page wrapper or an HTML header above the SVG, viewBox coordinates no longer map to image coordinates and every pixel probe or crop is misaligned.
2. **Screenshot a known rect, not the scrolling page height:**
   `cdp('Emulation.setDeviceMetricsOverride', width=1100, height=1240, deviceScaleFactor=1, mobile=False)` then
   `cdp('Page.captureScreenshot', format='png', captureBeyondViewport=True, clip={'x':0,'y':0,'width':1100,'height':1240,'scale':2})`
   and write `base64.b64decode(res['data'])` to the target `.png`.
3. **Never stack scaling.** `deviceScaleFactor: 2` already doubles; adding `clip.scale: 2` multiplies to 4x (a 2200x2480 image silently becomes 4580x6556) and chat clients recompress it to mush. Pick one: `deviceScaleFactor=1` + `clip.scale=2`, or `deviceScaleFactor=2` + `clip.scale=1`.
4. **Size for the phone.** ~1100 px wide by 1200-1600 px tall keeps 12-16 px labels readable at full width on a phone; a 1680 px landscape strip downscales to ~7 px text that gets squinted at instead of read.
5. Send with `MEDIA:/absolute/path.png` and put the reading order in the message text: the image carries the shape, the caption carries the meaning.
6. **No interactive browser session, or the CDP capture stalls:** render the same fixed-size HTML with the Playwright headless shell in one shot — `--window-size` sets the exact output size, `--force-device-scale-factor=2` the sharpness, `--virtual-time-budget=9000` gives webfonts time to land. Full command and traps: the `claude-design` skill carries the export recipe (its html-to-image-export reference).

## Verify Before Sending

A diagram that looks right in the SVG source is not verified. After every render, load the PNG with `vision_analyze` and ask specifically about: text clipped by its box, text overlapped by connectors, arrows stopping short of a box, lines hidden behind components, missing stage numbers, and content cut at the edges. Then fix and **re-render**; never report a fix you have not seen in a new render.

Defects this check routinely catches:
- A caption running along the top edge of a dashed boundary gets crossed by the connector entering that boundary. Split it (`4 · NAME` left-anchored, detail right-anchored with `text-anchor="end"`), or move the label outside the boundary.
- Captions inside a dashed group must clear the boxes: label at the top, boxes started ~35 px lower, so merge lines below the boxes never run through the text.
- Number every stage, including fan-out regions; an unnumbered block reads as an omission in an otherwise 1..6 flow.
- When a queue fans out to parallel workers, label each worker with the unit it owns (ticket/job id). Identical unlabelled workers imply one unit split three ways, which is the wrong model.
- Connectors drawn early sit behind boxes by design; confirm each merge line is still visible in the gaps between boxes, not swallowed by the group's own dashed border.

## Design System & Visual Language

### Color Palette (Semantic Mapping)

Use specific `rgba` fills and hex strokes to categorize components:

| Component Type | Fill (rgba) | Stroke (Hex) |
| :--- | :--- | :--- |
| **Frontend** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| **Database** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| **AWS/Cloud** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| **Security** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

### Typography & Background
- **Font:** JetBrains Mono (Monospace), loaded from Google Fonts
- **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny labels)
- **Background:** Slate-950 (`#020617`) with a subtle 40px grid pattern

```svg
<!-- Background Grid Pattern -->
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

## Technical Implementation Details

### Component Rendering
Components are rounded rectangles (`rx="6"`) with 1.5px strokes. To prevent arrows from showing through semi-transparent fills, use a **double-rect masking technique**:
1. Draw an opaque background rect (`#0f172a`)
2. Draw the semi-transparent styled rect on top

### Connection Rules
- **Z-Order:** Draw arrows *early* in the SVG (after the grid) so they render behind component boxes
- **Arrowheads:** Defined via SVG markers
- **Security Flows:** Use dashed lines in rose color (`#fb7185`)
- **Boundaries:**
  - *Security Groups:* Dashed (`4,4`), rose color
  - *Regions:* Large dashed (`8,4`), amber color, `rx="12"`

### Spacing & Layout Logic
- **Standard Height:** 60px (Services); 80-120px (Large components)
- **Vertical Gap:** Minimum 40px between components
- **Message Buses:** Must be placed *in the gap* between services, not overlapping them
- **Legend Placement:** **CRITICAL.** Must be placed outside all boundary boxes. Calculate the lowest Y-coordinate of all boundaries and place the legend at least 20px below it.

## Document Structure

For image delivery (see *Delivering as an Image*), drop the card wrapper and put the header inside the SVG so a fixed-size screenshot needs no page chrome. When the user opens the HTML themselves, the full four-part layout applies:

1. **Header:** Title with a pulsing dot indicator and subtitle
2. **Main SVG:** The diagram contained within a rounded border card
3. **Summary Cards:** A grid of three cards below the diagram for high-level details
4. **Footer:** Minimal metadata

### Info Card Pattern
```html
<div class="card">
  <div class="card-header">
    <div class="card-dot cyan"></div>
    <h3>Title</h3>
  </div>
  <ul>
    <li>• Item one</li>
    <li>• Item two</li>
  </ul>
</div>
```

## Output Requirements
- **Single File:** One self-contained `.html` file
- **No External Dependencies:** All CSS and SVG must be inline (except Google Fonts)
- **No JavaScript:** Use pure CSS for any animations (like pulsing dots)
- **Compatibility:** Must render correctly in any modern web browser

## Template Reference
`templates/workflow-spine.html` is a ready-to-relabel process flow: 6 numbered stages on a vertical spine, a gate with a rejection branch, a fan-out group of three parallel workers (each labelled with the unit it owns), a side supervision panel, an attention note, and the legend — already sized 1100x1240 for phone-legible chat delivery. Copy it and swap labels instead of rebuilding the geometry; if a stage needs more text, grow its height and push later stages down together.

Load the full HTML template for the exact structure, CSS, and SVG component examples:

```
skill_view(name="architecture-diagram", file_path="templates/template.html")
```

The template contains working examples of every component type (frontend, backend, database, cloud, security), arrow styles (standard, dashed, curved), security groups, region boundaries, and the legend — use it as your structural reference when generating diagrams.
