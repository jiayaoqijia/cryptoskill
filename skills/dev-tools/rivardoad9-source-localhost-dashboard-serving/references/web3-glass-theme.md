# Web3 / glass theme: from "AI slop" to a deliberate look

Feedback that produced this file (portfolio-risk dashboard, Oct 2026):
**"coba redesign lagi, soalnya terlalu ai slop, buat kayak UI jupiter gitu/web3 theme"**.
That is a *look* mandate, not a feature request. Treat "AI slop", "kayak template AI", "kurang
premium" as a standing directive for every page this user asks to be redone.

## 1. Source the direction first — do not freestyle

The user pointed at `github.com/nextlevelbuilder/ui-ux-pro-max-skill`; it is installed at
`~/.hermes/skills/creative/ui-ux-pro-max` (user-owned — read/query it, never edit it). Query it
before touching CSS:

```
python3 scripts/search.py "web3 crypto trading terminal dark neon glass" --design-system -p "<Page>"
python3 scripts/search.py "<query>" -d style|color|typography|ux|gsap --max-results 4 --json
```

`--json` key names differ per domain (`Style Category`/`Do`/`Don't`, `Primary`, `Product Type`,
`BV`/`Best For`) — print the keys once before writing a parser. The skill's top hits for this
dashboard were **glassmorphism + dark/OLED**, **Inter with -1.5px display tracking**, and its
`Don't` list named exactly the problems the user was complaining about.

**The "AI slop" anti-pattern checklist it corroborated (avoid all of these):**
- emoji used as icons (the page shipped 🛡️📊⛓️📰🪙 as its nav)
- purple→pink "AI" gradients as the dominant accent, and gold/purple corporate pairs
- futuristic display fonts (Orbitron, Exo 2) — dated crypto-template smell
- shadow/glow on everything, low-contrast micro text (<10.5px), centred prose

## 2. What the redesign actually was

```css
:root{
  --bg:#07080B; --glass:rgba(255,255,255,.035); --line:rgba(255,255,255,.075);
  --txt:#EDF1F7; --dim:#9AA7BC; --dim2:#7C8899;
  --lime:#19FB9B; --cyan:#14B8FF; --violet:#9945FF;
  --up:#19FB9B; --dn:#FF5C6C; --warn:#FFC24B;
  --grad:linear-gradient(100deg,var(--lime),var(--cyan) 55%,var(--violet));
}
body{background:
  radial-gradient(900px 520px at 15% -8%, rgba(25,251,155,.10), transparent 60%),
  radial-gradient(800px 500px at 92% 4%, rgba(153,69,255,.12), transparent 62%), var(--bg)}
.card{background:linear-gradient(180deg,rgba(255,255,255,.052),rgba(255,255,255,.02));
  border:1px solid var(--line);border-radius:20px;backdrop-filter:blur(14px) saturate(140%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.05), 0 18px 40px -24px rgba(0,0,0,.9)}
```

- **Accent budget matters more than the palette**: lime/cyan/violet appear only on the logo, the hero
  card border, the active nav pill and the score arc. Everything else is neutral glass — that is what
  separates "web3" from "neon template".
- **Icons: one inline `<svg style="display:none">` sprite of `<symbol id="i-…">` (24×24, stroke,
  `currentColor`) + `<svg class="ic"><use href="#i-…"/></svg>`** — shield, eye, eye-off, refresh,
  download, chart-pie, activity, newspaper, check-circle, alert-triangle, lock, globe, arrow-up-right.
  Emoji inside *content* (`⛔ unlock cliff`, `✅ verified`, `⚠️ note`) becomes `ic('lock')` etc. Assert
  the result: rendered text must contain **0** emoji.
- **Typography**: Inter (Google Fonts + `system-ui` fallback) with `font-variant-numeric:tabular-nums`
  on every figure; hero number in gradient text; micro-labels `10.5px / 700 / uppercase / +1.1 tracking`.
- **Motion**: `fadeUp .35s` with a 30ms stagger per card on render, `translateY(-4px)` on hover,
  `scale(.98)` on tap — all inside `@media (prefers-reduced-motion: no-preference)`.
- **Market strip** under the header: horizontally scrollable price chips with
  `mask-image:linear-gradient(90deg,#000 88%,transparent)` as the scroll affordance.
- **Score gauge** plus a labelled risk scale: gradient track, white marker **labelled with the score**,
  and range labels (`D <45 · C 45–61 · B 62–77 · A 78+`) — non-overlapping ranges, or a reviewer reads
  the scale as wrong.

## 3. The refinement round (each fix came from a vision review, keep the CSS)

| Symptom a reviewer reports | Real cause | Fix |
|---|---|---|
| 3px sideways scroll on phone, only in the on-chain card | grid tracks `repeat(4,1fr)` sized to content + 1px borders | `repeat(4,minmax(0,1fr))` on every metric grid |
| values inside a metric row don't line up | a 2-line label pushes its value down | `.k{min-height:27px}` (reserve 2 lines) + `.m{justify-content:flex-end}` + shorten labels |
| "3 columns then 2 columns" → axes look broken | mixed track counts per row | one grid scale: **2 cols phone / 4 cols desktop** for both metric rows (add a 4th metric instead of keeping 3) |
| legend chip collides with the % column | chip sat inside the value column (measured `lnm.right > pct.left`) | move the chip under the money cell: `.lus{display:flex;flex-direction:column;align-items:flex-end}`; `.lnm{overflow:hidden}` + ellipsis on the name |
| desktop: right card ends early, page looks lopsided | grid stretch with no flex column inside | `.g2{align-items:stretch}` + `.g2>.card{display:flex;flex-direction:column;justify-content:space-between}` |
| a 1.6% bar is invisible | bar scaled 0–100 | scale to the row max (`v/max*100`) with `min-width:3px`, keep the printed % |
| `+0.0M` painted green | `v>=0` on a zero-ish float | `cls = v => (v==null||Math.abs(v)<0.05) ? 'mut' : (v>=0?'up':'dn')` |
| amounts mixed `$1,382` with `0.39` | en-US grouping vs dot decimals | one locale rule: `Intl.NumberFormat('id-ID')` + `toFixed().replace('.',',')` for scores/percents/money, **and a dedicated `PX()` price formatter keeping dot decimals** (`$0.5045`) so prices don't flip to `$0,50` |
| "+2.3M" whale notional has no unit | inline `SC(v,1)+'M'` | format as `+$2.3M` / `−$2.3M`, `$0.0M` (no sign) when `|v|<0.05` |

Keep the header/nav labels short and always give icon-only buttons a `title` (a reviewer reads a bare
eye icon as "no action / ambiguous").

## 4. Verification

1. `node --check` on the extracted inline `<script>` — every pass.
2. `scripts/dashboard_visual_audit.py <url> [--hide '#btnH']` — JS errors, overflow at 390/1366,
   emoji count, `$<digit>` mask leaks, per-row value alignment, legend overlap, min font size, plus
   per-card screenshots.
3. `vision_analyze` **one card image at a time**, asking a targeted question ("are the metric values
   aligned across the row? is any text clipped?"). Whole-page questions return generic praise.
4. Re-check the tunnel serves the new build (`/risk`, `/manifest.json`, `/sw.js` → 200).

**Scope discipline**: the theme pass must not touch data binding. Keep the payload keys, formatters'
semantic meaning, the privacy mask, PWA hooks and section ids intact; change CSS/markup/icons only,
then re-run the audit — that is how the rewrite stayed verifiable in one pass.
