---
name: icp-brand-design
description: "ICP / DFINITY visual design system v2: tokens, color, typography, layout, components, accessibility for DFINITY and Internet Computer surfaces. Pairs with icp-brand-voice. Use when building or reviewing visual surfaces (NNS, ICP.app, Internet Identity, dashboards, the main website, developer docs, marketing). Enforces the system that ships on internetcomputer.org: three faces (Newsreader, Inter, JetBrains Mono), single rust accent, light editorial parchment as the default theme with an opt-in dark theme for product surfaces that need it, sentence case, italic for asides only, no em-dashes (U+2014), tamperproof spelled as one word. Triggers: ICP design, DFINITY design, brand tokens, design review ICP, color palette, typography ICP, NNS redesign, light or dark mode ICP. OISY, Caffeine, and ecosystem products with their own brand are out of scope."
---

# ICP / DFINITY Brand Design v2.1

**Current version:** v2.1 (2026-05-08). See the Changelog section at the bottom for history. Every change to this skill bumps the minor version and adds a line to the changelog.

## When to Use This Skill

Load this skill when the user works on any **visual** surface under the DFINITY or Internet Computer mark. That includes:

- **Products**: NNS, ICP.app, Internet Identity, the IC dashboard, developer portals, explorers, internal tools
- **The main website**: internetcomputer.org and its subpages
- **Developer documentation**: docs pages, API references, tutorials, SDK sites
- **Marketing material**: landing pages, campaign pages, investor pages, press pages, decks
- **Reviews**: design reviews, brand checks, compliance audits, PR or mockup reviews

Also load when the user says "make this on brand visually", "ICP style", "DFINITY look", "brand tokens", "match the website".

For **what to say** (positioning, voice, vocabulary), load `icp-brand-voice`. The two skills are designed to be used together.

Do NOT use this skill for:

- **OISY wallet.** Own product identity. Out of scope.
- **Caffeine.** Own brand. Out of scope.
- **Any other ecosystem product with its own established visual system.**
- Third-party dapps that happen to run on ICP but are not DFINITY products.

## North Star

Every DFINITY product should feel like it came from the same studio: editorial, factual, calm. The reference implementation is the **ICP Brand Guidelines v2** site (link in `Resources` below) and the live `internetcomputer.org`.

Three non-negotiables:

1. **Light editorial parchment is the default theme.** This matches the live site, which ships light only today. A dark theme is documented and available as opt-in via `data-theme="dark"` on `<html>`, for product surfaces that genuinely benefit from one (NNS late-night use, dashboards, terminal-style developer tools). Marketing and the main site stay on the light default. Never auto-switch on `prefers-color-scheme`.
2. **One primary accent on a page: rust `#a8482b`.** Section stripes (the small set below) are scoped strictly to category coding, never on body text, CTAs, or emphasis.
3. **Three faces, three roles.** Newsreader for what you read. Inter for what you click. JetBrains Mono for what the system reports. No other typefaces.

## Instructions

### 1. Load the tokens

Use `assets/tokens.css` as the single source of truth for color, type, spacing, radii, and themes. Ship it untouched, or mirror the same values into your framework config.

```html
<link rel="stylesheet" href="/tokens.css">
```

Never redefine the accent, background, or text colors with literal hex values in product code. Always reference the CSS custom properties (`var(--icp-bg)`, `var(--icp-fg)`, `var(--icp-accent)`, etc.).

The tokens file ships the light theme at `:root` (so it loads by default with no attribute) and the dark theme under `[data-theme="dark"]` (opt-in).

### 2. Color

#### Primary accent (one and only)

| Token                  | Light (default) | Dark (opt-in) | Notes                          |
| ---------------------- | --------------- | ------------- | ------------------------------ |
| `--icp-accent`         | `#a8482b`       | `#c25a37`     | rust, the single brand color   |
| `--icp-accent-strong`  | `#8e3b22`       | `#d96a45`     | hover, focus ring              |
| `--icp-accent-dim`     | rgba 0.10       | rgba 0.16     | accent washes only             |

The accent paints heading emphasis words, key inline terms, primary CTA fills, and focus rings. Body text, nav, and chrome stay in `--icp-fg`. Never use the accent on chart fills, banners, large blocks, or anything where it would compete with itself across the page.

The dark accent is warmed to `#c25a37` because the same rust at `#a8482b` does not pass AA on a dark surface for small UI text. Both values resolve to `var(--icp-accent)` once the theme is set.

#### Light theme (default, editorial parchment)

Mirrors the live `internetcomputer.org` exactly.

| Role             | Token                  | Value      | Notes                                  |
| ---------------- | ---------------------- | ---------- | -------------------------------------- |
| Page bg          | `--icp-bg`             | `#faf9f5`  | parchment, never pure white            |
| Sunk bg          | `--icp-bg-sunk`        | `#f3f1ea`  | alternating sections, sunk panels      |
| Elevated bg      | `--icp-bg-elev`        | `#ffffff`  | small lift for cards that read as raised |
| CTA bar bg       | `--icp-bg-cta-inverse` | `#1a1a1a`  | near-black inversion (deliberate)      |
| Card bg          | `--icp-bg-card`        | `#ffffff`  |                                        |
| Foreground       | `--icp-fg`             | `#1a1a1a`  | ink, never pure black                  |
| Body text        | `--icp-fg-body`        | `#1a1a1a`  | same as fg, the live site uses one ink |
| Secondary        | `--icp-fg-secondary`   | `#4b4943`  | meta strips, secondary copy            |
| Muted            | `--icp-fg-muted`       | `#868078`  | captions, attributions                 |
| Hairline         | `--icp-rule`           | `#e7e3da`  | warm ivory hairline, not gray          |
| Strong rule      | `--icp-rule-strong`    | `#4b4943`  | hover underlines, emphasized borders   |
| Grid line        | `--icp-grid-line`      | `rgba(26,26,26,0.04)` | the hero grid paper texture |

#### Dark theme (opt-in, `[data-theme="dark"]`)

For product surfaces that need a dark reading environment. The live site does not ship dark today, but the tokens are documented so a product can offer it later without diverging from the master system.

| Role             | Token                  | Value      | Notes                                  |
| ---------------- | ---------------------- | ---------- | -------------------------------------- |
| Page bg          | `--icp-bg`             | `#14110d`  | deep bark, never pure black            |
| Sunk bg          | `--icp-bg-sunk`        | `#1b1812`  | alternating sections in dark           |
| Elevated bg      | `--icp-bg-elev`        | `#1b1812`  | card lift                              |
| CTA bar bg       | `--icp-bg-cta-inverse` | `#ffffff`  | flips to white on dark                 |
| Card bg          | `--icp-bg-card`        | `#1b1812`  |                                        |
| Foreground       | `--icp-fg`             | `#f0ebe0`  | bone, never pure white                 |
| Body text        | `--icp-fg-body`        | `#f0ebe0`  |                                        |
| Secondary        | `--icp-fg-secondary`   | `#a29a8d`  |                                        |
| Muted            | `--icp-fg-muted`       | `#7a7367`  |                                        |
| Hairline         | `--icp-rule`           | `#2d2820`  | soil                                   |
| Strong rule      | `--icp-rule-strong`    | `#5a5446`  |                                        |
| Grid line        | `--icp-grid-line`      | `rgba(240,235,224,0.05)` | hero grid paper in dark    |

The CTA bar token always inverts the surface around it. In light mode it goes near-black, in dark mode it goes white. This is intentional: it gives the strongest call-to-action on the page a different visual register from everything else.

#### Section stripes (category coding only)

The live site uses three stripe colors today, scoped strictly to 3px card top stripes and category markers. They never appear on body text, CTAs, or running emphasis. Two additional muted accents are reserved in the tokens file for sections that do not yet exist on the live site, so a product can introduce them without inventing new colors.

| Section role                                 | Token                       | Light (default) | Dark (opt-in) |
| -------------------------------------------- | --------------------------- | --------------- | ------------- |
| Default / hero / page-level                  | `--icp-section-default`     | rust `#a8482b`  | ember `#c25a37` |
| Ecosystem, spotlight, governance             | `--icp-section-teal`        | `#0b5e5c`       | `#2c8a85`     |
| Build, docs, developers                      | `--icp-section-blue`        | `#1c3d5a`       | `#4a7da8`     |

Indicator dots (live tickers, status pills) use a brighter teal `#14938e` (`--icp-indicator-teal`) and the rust accent `--icp-indicator-rust`.

Use a section stripe only where it earns the label. If a card or section does not belong to a category, it does not get a section stripe, the page-level rust is used instead.

#### Surface rhythm: parchment, sunk parchment, grid paper

The brand has **two parchment tones** plus **one near-invisible texture**. Together they let a long page breathe without resorting to boxes, shadows, color blocks, or gradients. Mirrors the live site exactly.

**Parchment, the page default.** `--icp-bg` (`#faf9f5` light, `#14110d` dark). The default surface for every section. Body text reads on parchment, prose reads on parchment.

**Sunk parchment, for alternating sections.** `--icp-bg-sunk` (`#f3f1ea` light, `#1b1812` dark). Use to differentiate adjacent sections on long pages, sunk panels, code-example wrappers, and any container that should read as recessed below the page surface. The contrast against parchment is small on purpose, the goal is rhythm, not visual weight. Always pair with a 1px hairline above and below for the section seam.

**Grid paper, the hero texture.** Two crossed `linear-gradient` layers draw a 24x24px hairline grid in `--icp-grid-line` (4% ink on parchment, 5% bone on dark). Apply at 80% layer opacity, offset `-1px -1px`. This is the texture under the hero on `internetcomputer.org`. Use it sparingly: hero, feature surface, the occasional editorial canvas. Never as a background for body prose.

The tokens file ships two utility classes:

```css
/* Apply directly to a container as the background. */
.icp-grid-paper { ... }

/* Apply as a positioned overlay layer (preferred, on a hero with content above). */
.icp-grid-paper-overlay { ... }
```

When using the overlay variant, parent must be `position: relative` and `overflow: hidden`. Content sits above with `position: relative; z-index: 1;`.

**Section rhythm pattern.** On long pages, alternate parchment with sunk parchment. Six sections becomes parchment / sunk / parchment / sunk / parchment / sunk. The hero gets the grid paper overlay on top of parchment. Hairlines remain at every section seam.

**Do not.**

- Do not increase the grid line opacity past 6% on either theme. The texture should read as paper grain, not a wireframe grid.
- Do not change the tile from 24px. Smaller tiles read as noise. Larger tiles read as graph paper.
- Do not invent a third parchment tone. Two is the system. If you need more contrast, the design needs an elevated card (`--icp-bg-elev`) or a hairline.
- Do not stack grid paper inside sunk parchment, the texture is for the parchment surface only.
- Do not apply grid paper to body prose. The contrast against text is fine for AA but reads visually noisy under long-form reading.

#### Color rules

- One primary accent on the page. Section stripes do not count as a second primary, they are 3px category labels.
- No gradients on brand surfaces. Flat color.
- No pure `#000` text in light mode and no pure `#fff` body text in dark mode (use `--icp-fg` and `--icp-fg-body`).
- Hairlines are 1px in `--icp-rule`. No heavy borders.
- Card stripes are 3px (`--icp-card-stripe-w`), not 2px. Live-site value.
- Never invent a new accent. If the design needs another color, the design is wrong.

### 3. Typography

The system has **three faces, each with one job**.

| Face          | Role                                                              | Token             | Weight        | Where it shows up                                                        |
| ------------- | ----------------------------------------------------------------- | ----------------- | ------------- | ------------------------------------------------------------------------ |
| Newsreader    | Editorial: display, body, long-form reading                       | `--icp-serif`     | 380 / 400 / 500 | Hero, all headings, body prose, callout text                          |
| Inter         | UI chrome: things you click and navigate                          | `--icp-ui`        | 400 / 500 / 600 | Top nav, eyebrows, button labels, footer, breadcrumbs                |
| JetBrains Mono| Technical readouts: things the system reports                     | `--icp-mono`      | 400 / 500     | Network stats, section markers (`§ 03`), card markers (`№ 01`), code |

**Type scale**

| Token                | Value                  | Used for                              |
| -------------------- | ---------------------- | ------------------------------------- |
| `--icp-fz-h1`        | `clamp(40px, 6.4vw, 86px)` | Hero, page-opener headlines       |
| `--icp-fz-h2`        | `36px`                 | Section headings                      |
| `--icp-fz-h3`        | `24px`                 | Subsection / card titles              |
| `--icp-fz-body`      | `17px`                 | Default reading text                  |
| `--icp-fz-body-sm`   | `15px`                 | Meta strips, dense panels             |
| `--icp-fz-eyebrow`   | `11px`                 | Inter UPPERCASE 0.18em eyebrows       |
| `--icp-fz-marker`    | `12px`                 | JetBrains Mono `§` and `№` markers    |

**Tracking and line-height**

- Display Newsreader: `letter-spacing: -0.015em` (live-site value, `-1.29px` at 86px), `line-height: 1.05` to `1.15`
- Body Newsreader: tracking 0, `line-height: 1.55`
- Inter eyebrows: UPPERCASE, `letter-spacing: 0.18em`, weight 500
- JetBrains Mono markers: UPPERCASE, `letter-spacing: 0.04em`, weight 400 to 500

**Casing**

- **Sentence case** for all headlines, body, and prose.
- **UPPERCASE** is reserved for two specific patterns and only those two: Inter eyebrows above sections, and JetBrains Mono markers (`§ 01`, `№ 03`, metadata strips like `DEFAULT THEME · LIGHT`).
- Buttons and CTAs are UPPERCASE Inter at small sizes (11 to 13px), tracked. This matches the live site and is the one place Inter goes uppercase outside eyebrows.
- Match the live site's casing technique: write the source string in sentence case and apply UPPERCASE in the markup or class, not via `text-transform: uppercase`. This keeps screen-reader output natural.
- Proper nouns and acronyms (DFINITY, ICP, NNS) keep their natural case in any context.

**Italic**

- Newsreader italic carries a single emphasis word inside an otherwise roman headline ("Sovereign *frontier* cloud", "What *ICP* is"), captions, attributions, and asides. The emphasis word is colored in the rust accent on the live site. The italic word is always **the subject of the heading**, the noun or noun phrase the line is about, never a verb, copula, article, or connector. Test, can the heading still stand if the italic word is removed; if yes, the emphasis is on the wrong word.
- Never italic for stress in body copy. Never italic for entire paragraphs.

**Weights**

- Newsreader 380 for display (hero, the live-site value), 400 for body, 500 for emphasis inside body.
- Inter 400 for nav and most chrome, 500 for eyebrows and tab labels, 600 for primary button labels.
- JetBrains Mono 400 for markers and meta, 500 for stat numerals.
- Never bold (700+). 600 only on Inter button labels and rare inline emphasis.

### 4. Layout and spacing

- **Container max width**: `1280px` (`--icp-container`). The live site uses this.
- **Prose max width**: `720px` (`--icp-prose`). Never run body text wider than this.
- **Horizontal gutter**: `32px` (`--icp-gutter`).
- **Section rhythm**: 144px between major sections (`--icp-space-section`), separated by 1px hairlines in `--icp-rule`. No boxes.
- **Vertical scale**: spacing tokens go 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 144. Use the tokens, not raw pixels.

### 5. Radii

- Inline code, mono badges: `3px` (`--icp-radius-inline`)
- Cards, code blocks, meta panels: `6px` (`--icp-radius-card`)
- Inputs, search bars: `8px` (`--icp-radius-input`)
- Pill CTAs only: `9999px` (`--icp-radius-pill`)

Pills are scoped strictly to the CTA pattern. Cards, panels, and inputs never go fully rounded. Avatars are circular.

### 6. Iconography and imagery

- Line icons, 1.5px stroke, rounded joins. No filled or duotone icons in product chrome.
- External-link affordance: trailing `↗` (U+2197) in Inter or JetBrains Mono. Never an SVG.
- Photography is rare. When used, warm-toned, documentary, no stock illustrations.
- No 3D renders, no isometric illustrations, no crypto iconography (no chains, no shields, no padlocks).
- The DFINITY infinity logo is the only mark. Always paired with the wordmark in nav, never alone outside small avatar contexts.

### 7. Motion

- Default transition: `0.15s ease` on `background`, `color`, and `border-color`.
- No bounce, no slide-ins on load. Respect `prefers-reduced-motion`.
- Hover on links: color shifts to `--icp-accent`, no underline animation.

### 8. Components

Use these patterns directly. Never invent a new primary button, card, or callout without a brand review.

#### Pill CTA (primary)

Rust fill, white text, fully rounded (`--icp-radius-pill`). Inter UPPERCASE 11 to 13px, weight 600, tracking 0.06em. Used as the single primary action on a page.

```
[ START AT OPENCLOUD.ORG ]
```

#### Pill CTA (inverse)

White fill on near-black surfaces (CTA bar). Dark text, rust trailing arrow. Used inside the CTA bar pattern.

```
[ BROWSE THE LIBRARY → ]
```

#### Pill CTA (secondary)

Outlined: 1px `--icp-rule-strong` border, transparent fill, foreground text, trailing arrow. Used beside a primary or as a standalone soft action.

```
( READ THE SOURCE → )
```

#### CTA bar (inverse strip)

Always near-black `#1a1a1a` background, regardless of theme. White Newsreader heading, white meta line, inverse pill or arrow CTA. This is the page's most assertive call to action and gets a different visual register from the rest of the surface.

```
┌──────────────────────────────────────────────┐
│ JOIN THE FRONTIER                            │
│ Create a sovereign cloud engine in minutes.  │
│                                  START →     │
└──────────────────────────────────────────────┘
```

#### Editorial card

3px top stripe in `--icp-section-default` (rust) by default, or a section stripe color when used inside a category. JetBrains Mono `№ 01` marker top-left. Newsreader 500 title, Newsreader 400 body. 1px hairline border, `--icp-radius-card` corners.

#### Network stats ticker

JetBrains Mono numerals at h2 size, Inter eyebrow caption beneath. Used for live metrics (block rate, query throughput, fault tolerance). Small indicator dot in `--icp-indicator-teal`. Never use Newsreader for stat numerals.

#### Section marker

`§ 01`, `§ 02`, etc. JetBrains Mono 12px, `--icp-fg-secondary`. Sits in the left gutter of a section, vertically aligned with the section heading. Same treatment as the live site.

#### Card marker

`№ 01`, `№ 02`, etc. Same face and size as section markers, used inside cards to enumerate sequence.

#### Eyebrow (Inter)

UPPERCASE, 11px, weight 500, tracking 0.18em, `--icp-fg-secondary`. Sentence case is broken here on purpose because it is system label, not editorial copy.

#### Metadata strip

Inter UPPERCASE label, JetBrains Mono value, separated by `·`. Example: `DEFAULT THEME · LIGHT`. Use for deck-style annotations beneath hero copy.

#### "Ask how this works" pattern

Inline soft prompt: `+ ASK HOW THIS WORKS –`. Inter UPPERCASE, hairline. Invites a chat or canister-call interaction without shouting.

#### List row

1px bottom hairline in `--icp-rule`, Newsreader label on the left, `--icp-fg-muted` value on the right. No boxes, no zebra stripes.

#### Code block

Sand background (`--icp-code-bg`), JetBrains Mono, no syntax colors beyond fg + muted. 6px radius. Never colorful syntax highlighting.

### 9. Accessibility

- WCAG AA contrast minimum on every surface. The light theme passes for `#1a1a1a` on `#faf9f5` at body sizes. The dark theme passes for `#f0ebe0` body on `#14110d` at body sizes. Verify any custom pairings against a contrast checker before shipping.
- Real `<button>` and `<a>` elements. No div-buttons. Keyboard navigable.
- Focus rings must be visible: 2px `--icp-focus` outline with 2px offset.
- Never convey meaning by color alone. Section stripes are paired with `§ 0X` markers and Inter labels.
- Every product ships a visible skip-link to main content.
- Respect `prefers-reduced-motion`. Do not use `prefers-color-scheme` to auto-switch theme: light is the deliberate default. If a product offers a dark theme, expose it as an explicit user toggle that sets `data-theme="dark"` and persists in `localStorage`.
- Alt text is specific, not decorative. Describe what matters, skip "image of".

### 10. Theme switching pattern

For products that ship both themes, the toggle should:

- Default to **light** (no attribute on `<html>`, tokens load from `:root`).
- Set `<html data-theme="dark">` to opt into dark.
- Persist the choice in `localStorage` under a product-scoped key (e.g. `nns-theme`, `icp-theme`).
- Read `localStorage` on first paint to avoid a theme flash.
- Expose the toggle as a visible button in chrome, labeled "Light" / "Dark", not as a hidden setting.
- Never auto-switch on `prefers-color-scheme`. The user picks.

The live `internetcomputer.org` ships light only and does not expose a toggle today. The dark theme tokens are documented for future use and for product surfaces that need them now (NNS late-night, dashboards, terminal-style developer tools).

### 11. Design review checklist

Before merging any ICP / DFINITY visual change, confirm:

- [ ] Uses `tokens.css` variables, no hardcoded brand hex values
- [ ] Light editorial parchment is the default (no `data-theme` attribute on `<html>`). Dark is opt-in via `data-theme="dark"`, exposed as an explicit toggle, never auto from `prefers-color-scheme`
- [ ] Newsreader for editorial type, Inter for UI chrome, JetBrains Mono for technical readouts. No other faces.
- [ ] Sentence case for headlines and body. UPPERCASE only on Inter eyebrows, JetBrains Mono markers, and small CTA labels.
- [ ] Italic used only for asides, captions, attributions, or a single heading emphasis word
- [ ] One primary accent on the page (rust `#a8482b` light, `#c25a37` dark). Section stripes scoped to 3px category coding only.
- [ ] No section-stripe fills on CTAs, body text, or emphasis
- [ ] Body prose capped at 720px
- [ ] Long pages alternate parchment with sunk parchment (`--icp-bg-sunk`) for section rhythm. Hairlines at every section seam.
- [ ] Grid paper texture (`.icp-grid-paper-overlay`) reserved for hero and rare feature surfaces, not body prose. Tile is 24px, line opacity does not exceed 6%.
- [ ] 1px hairlines in `--icp-rule`, no heavy borders. Card stripes 3px.
- [ ] Pill radius (`9999px`) used only for CTAs
- [ ] CTA bar background is near-black `#1a1a1a` in both themes
- [ ] Focus states visible, AA contrast verified
- [ ] No emoji, no stock illustration, no 3D render, no crypto iconography
- [ ] No gradients, no drop shadows
- [ ] External links use `↗` affordance, not an SVG icon
- [ ] No em-dashes anywhere (U+2014)
- [ ] "Tamperproof" written as one word, never "tamper-proof" or "tamper proof"

If any box is unchecked, the work is not on brand.

### 12. Migrating from v1

If a product currently ships v1 (older Newsreader + Source Serif 4, no Inter, no JetBrains Mono):

1. **Theme.** Keep light as the default. Drop any auto `prefers-color-scheme` switch. If you offered a dark theme, swap it onto the new `data-theme="dark"` token set, do not invent your own dark hex values.
2. **Type.** Keep Newsreader for editorial. Replace any Source Serif 4 body text with Newsreader 400. Add Inter for nav, buttons, eyebrows, footer, breadcrumbs. Add JetBrains Mono for stats, markers, code.
3. **Casing.** Convert all-caps tracked labels in your old serif eyebrows to Inter eyebrows (already UPPERCASE there by design). Convert numeric stat displays to JetBrains Mono. Apply UPPERCASE in markup, not via `text-transform`.
4. **Accent.** v2 keeps the same rust accent in light mode. In dark mode it warms to `#c25a37` for AA on dark surfaces.
5. **Section colors.** If you used the live site's older neon palette (e.g. `#bbe9ff`, `#ff00f7`, `#00f9e1`), swap to the muted section stripes in this skill (rust, deep teal `#0b5e5c`, ink-blue `#1c3d5a`).
6. **Pills.** Add the pill radius `9999px` for CTAs. Old 6px button radius is now reserved for cards.
7. **CTA bar.** Add the inverted near-black CTA strip. Theme-stable (always `#1a1a1a`).

### 13. When in doubt

Defer to the **ICP Brand Guidelines v2** site (link in `Resources`) and the live `internetcomputer.org` as the joint reference. If they disagree, the brand guide wins because it has been edited for consistency. If this skill and the brand guide disagree, the brand guide wins and this skill should be updated.

## Versioning

This skill follows semantic versioning at the brand level.

- **Major** (v2, v3, ...): a new visual system. Color palette, type stack, or core component model changes. Existing surfaces require migration.
- **Minor** (v2.1, v2.2, ...): a refinement to the current system. New rule, corrected example, tightened token, audit fix. Existing surfaces remain valid; the change clarifies or sharpens.
- **Every edit to this skill bumps the minor version.** When you save a new version, update the version line at the top of the file and add a row to the Changelog section. Mirror the bump in the brand guide HTML (hero eyebrow, hero meta-row, footer changelog) and in the paired `icp-brand-voice` skill so the version is consistent across all three.

## Changelog

- **v2.1** (2026-05-08). Italic emphasis rule clarified: italic word lands on the subject of the heading (the noun the line is about), never a verb, copula, article, or connector. Removal test added. Headings on the canonical guide audited; "What ICP *is*" corrected to "What *ICP* is". Versioning rule introduced.
- **v2.0** (2026-05-08). Initial v2 release. Light editorial parchment as the default theme, opt-in dark theme via `data-theme="dark"`, three-face system locked (Newsreader, Inter, JetBrains Mono), single rust accent `#a8482b`, sunk parchment (`--icp-bg-sunk` `#f3f1ea`) for section rhythm, hero grid paper texture (`.icp-grid-paper-overlay`), muted section stripes (rust, deep teal `#0b5e5c`, ink-blue `#1c3d5a`) replacing the v1 neon palette.

## Resources

- **Canonical brand guide v2**: the deployed HTML reference page (URL shared in conversation)
- **Tokens file**: `assets/tokens.css` in this skill. Drop into any product as the single source of truth.
- **Reference site**: [internetcomputer.org](https://internetcomputer.org)
- **Paired skill**: `icp-brand-voice` for positioning, voice, and vocabulary.
- **Out of scope**: products with their own brand identity (OISY wallet, Caffeine, and any future ecosystem product that ships under its own visual and verbal system).

## Examples

**Example 1. Reviewing a mockup**

User: "Here's a mockup for the new NNS proposal detail page. Does it fit our brand visually?"

Response: Walk the design review checklist. Confirm light parchment default with a visible Light/Dark toggle (NNS is a fair candidate for a dark mode), three-face split (Newsreader heading, Inter nav and tabs, JetBrains Mono for proposal IDs and vote counts), rust accent only on the primary CTA and the proposal-status indicator. Flag any neon section colors, any `prefers-color-scheme` auto-switch, any em-dashes in copy, any "tamper-proof" or "on-chain". Recommend pill radius on the primary CTA, hairline lists for the vote breakdown, JetBrains Mono for the canister IDs.

**Example 2. New developer tool**

User: "I'm shipping a new IC explorer dashboard. Give me the starter styles."

Response: Hand over `tokens.css`, the Newsreader + Inter + JetBrains Mono Google Fonts link (`Newsreader:wght@0,380;0,400;0,500;1,380;1,400;1,500`), the pill primary / outline secondary CTA CSS, the metadata strip pattern (`LATEST BLOCK · 12,847,231`), the network stats ticker pattern, a reminder that light is the default and a dark toggle is one `data-theme="dark"` away. Point to `icp-brand-voice` for headline and copy decisions.

**Example 3. Marketing landing page**

User: "Build a landing page for an ICP campaign on agent-deployable apps."

Response: Hero in Newsreader 380 with one italic emphasis word in the rust accent, sentence case, capped at 86px, tracking -0.015em. Inter UPPERCASE eyebrow above. JetBrains Mono metadata strip beneath ("AVAILABILITY · GENERAL · CADENCE · ROLLING"). Rust pill CTA as the only primary action. Editorial cards with 3px section stripes if the page belongs to a category, plain rust stripes if not. CTA bar before the footer in near-black `#1a1a1a`. Light theme only, matching the live site.
