# Phone legibility, centering, and a privacy ("hide nominal") mode

Feedback that produced this file (portfolio-risk dashboard, Oct 2026):
**"rapihin dong, masi berantakan itu"** → then **"tambahin hide wallet, biar nominalnya bisa di
hide, terus bikin center gitu"**. Treat both as defaults for any dashboard that shows the user's own
money, not as one-off requests.

## 1. Legibility rules that fixed "berantakan"

The user's complaint was not structure — it was *small, dim, misaligned numbers*.

- **Minimum font 10.5px** for metric labels (`.oct .k`, `.mx .k`, `.tile .k`, `.whalerow .k`, `.chip`).
  9.5px uppercase+letterspaced reads as "kecil dan redup" and got called out explicitly.
- **Raise label contrast**: secondary labels `#7f93b5` on card `#101828` — not `#5f7396`.
- **NEVER `text-transform:uppercase` on a label containing a symbol or Greek letter** — the transform
  turns `σ` into `Σ` and the user/vision review reads the label as wrong. Use words instead:
  `Volatilitas`, `Swing 1 sigma`.
- **Align numeric columns with a grid, not inline text**: legend row
  `grid-template-columns:9px 1fr auto auto` + `font-variant-numeric:tabular-nums`; percentage column
  right-aligned, money column right-aligned with `min-width`.
- **A flex child set to `flex:1` shrinks to content when the parent flips to `column`** — on phone the
  metric grid came out 266px inside a 390px viewport. Fix: `.hcol{width:100%}` (then `.tiles` spans).
- Keep **prose left-aligned even in a centered design** (`h2`/hero centered is fine; `.why li`, `.note`,
  `.pn li` stay left). Centering a bulleted risk list makes it unreadable.

## 2. Centered, app-like column

```css
.wrap{max-width:720px;margin:0 auto;padding:0 12px}          /* was 1120px — looked like a web page */
@media(max-width:759px){
  h2,.sub{text-align:center}
  #hpill{display:none}                                       /* score pill duplicated in the hero */
  .hero{flex-direction:column;align-items:center;text-align:center;gap:12px}
  .hcol{width:100%}
  .ring{margin:0 auto} .hrow{justify-content:center}
  .dwrap{flex-direction:column;align-items:center} .leg{width:100%;min-width:0}
  .ochead,.ngt,.ni .m,.act,.unl,.tokhead{justify-content:center}
  .why li,.note,.pn li{text-align:left} footer{text-align:center}
}
```

- **Bottom tab nav** is what makes it feel like an app instead of a long scroll:
  4 tabs (`Ringkasan · On-chain · News · Token`), each `scrollTo(el.offsetTop-58, smooth)`, plus an
  `IntersectionObserver({rootMargin:'-60px 0px -70% 0px'})` to highlight the section in view.
  Add `scroll-margin-top:62px` to sections so the sticky header doesn't cover the heading.
- On desktop the same nav can render as centered pills (`position:static`) — one markup, two looks.

## 3. Donut + legend parity (looks like sloppiness, is arithmetic)

- **Include idle cash as a segment.** Ex-cash legend summed to 80% and the user reads that as broken;
  add `KAS (USDT)` with the idle amount so the legend totals 100%.
- **One total, one source**: the hero total and the donut center must both come from the donut's own
  sum, otherwise rounding shows `$1,384` in the hero and `$1,385` in the donut.
- **Round the metric once before formatting**: `hhi = round(sum(...), 2)` then use that value in both
  the advisory text and the payload, else Python `f"{hhi:.2f}"` and JS `toFixed(2)` disagree
  (`0.38` vs `0.39`) and the page contradicts itself.
- Do not shrink a 1–2% segment to invisibility — keep `min-width:2px` on the bar and always print the
  number next to it.

## 4. Privacy mode: "hide the nominal"

A one-tap eye toggle in the header; the numbers are the user's own money and they screen-share.

```js
let HH = localStorage.getItem('zmz_hide') === '1';           // persists across app relaunch
const MSK = '$••••';
const FU = n => { if (n==null) return '—'; if (HH) return MSK; return '$' + /* B/M/k */ ; };
const MV = v => (v==null||isNaN(v)) ? '—' : (HH ? '••••' : (v>=0?'+':'')+SC(v,1)+'M');
// mask amounts embedded in BACKEND-generated prose:
const MS = s => HH ? String(s==null?'':s).replace(/\$\s?[\d][\d.,]*\s?[KMBT]?/gi, '$••••') : (s??'');
$('#btnH').onclick = ()=>{ HH=!HH; localStorage.setItem('zmz_hide',HH?'1':'0'); paintEye(); if(LAST) render(LAST); };
```

- **Masking the formatters is NOT enough.** Two real leaks in one pass: `di posisi $579` and
  `±$894M` came from *narrative strings built in Python*, not from the JS formatters. Wrap **every**
  narrative field with `MS()`: `why[]`, `potensi[]`, `negatif[]`, `action`, `flags[]`,
  `unlock.amount`, and the macro/regime line.
- Keep the **last payload in a module-level `LAST`** and re-render on toggle — no refetch, instant.
- Also mask the token price if you want one simple rule to explain: *"mode privasi = tidak ada angka
  dolar yang kelihatan"*.
- **State what stays visible**: percentages, scores/grades, RSI, β, token quantities (`1,71B ONDO`) and
  wallet counts. The user may then ask for quantities too — don't silently hide them.
- Icon feedback: `👁` → `🙈` plus a tinted `.onhide` button state, so the state is obvious at a glance.

## 5. Wiring the render to the payload (two silent bugs in one session)

- **Dump the payload keys before writing render code.** Guessed field names render as a silent `—`:
  `r.beta` (actual `r.weighted_beta`) and `oc.vol24` (actual `oc.vol24_usd`) both shipped to the user
  as empty cells. One `print(sorted(d['assets'][0].keys()))` prevents it.
- **Formatter thresholds**: extending `$` formatting to B (not just M) is required or market cap prints
  as `$2471.70M` instead of `$2.45B`.
- Keep a `title`/tooltip or unit in the label (`Swing 1 sigma`) when the unit glyph is risky.

## 6. Verification ladder (cheapest first, vision last)

1. `node --check` on the extracted inline `<script>` — caught `.btc_-30pct` (invalid property access)
   and a malformed nested ternary in this session. Always first.
2. `scripts/dashboard_content_probe.py URL` — overflow, counts, per-selector innerText, JS errors.
3. `scripts/dashboard_card_shot_probe.py URL "sel1,sel2" [--hide '#btnH']` — element screenshots per
   card, min computed font size, mask-leak assertion, persistence after reload.
4. `vision_analyze` **one card image at a time** with a targeted question ("is any text cut off, are
   columns aligned?"). Asking about the whole page at once returns generic praise.

**Prefer element screenshots over full-page slices.** `locator(sel).screenshot(path=...)` captures the
whole card regardless of scroll position, and avoids the fixed bottom-nav overlay that makes a
full-page slice look like the legend is "terpotong" when it is not (it cost two review cycles here).
