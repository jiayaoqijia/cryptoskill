# Bottom-nav / section-nav wiring, number locale, and tile-grid overflow

Session-proven on the ZEMIZ RISK dashboard (`~/.hermes/scripts/porto_dashboard.html`, served on 8787
at `/risk`, phone-first PWA). All of it applies to any inline-JS dashboard page.

## 1. "The bottom nav can't be clicked" → a global function shadowed `window.scrollTo`

The page had:

```js
function scrollTo(id){ const el = document.getElementById(id); if(el) window.scrollTo({top: el.offsetTop-60, behavior:'smooth'}); }
```

Two bugs stacked, and **neither throws an error**:

1. `function scrollTo(...)` is a global declaration, so it OVERWRITES the native `window.scrollTo`.
   Inside it, `window.scrollTo({...})` therefore calls *itself* (`id` becomes an options object →
   `getElementById(object)` → `null` → return). Result: every tap is a silent no-op.
2. `el.offsetTop` is relative to the offset parent (`.wrap{position:relative}`), not the document —
   so even a working call would scroll to a wrong place.

Symptom seen in the browser: the tap reaches the button (`document.elementFromPoint(...)` returns
`BUTTON`), `scrollY` stays 0, the active class never changes, and `pageerror` is empty. Don't trust
"no JS errors" as proof the wiring works — *exercise the click* (see `scripts/nav_tap_probe.py`).

Working version (renamed so it cannot shadow anything, doc-position math, optimistic highlight,
and an observer that doesn't fight the smooth scroll):

```js
let navTarget = null, navSettle = 0;
function goSection(id){
  const el = document.getElementById(id); if(!el) return;
  const hdr = document.querySelector('.top')?.offsetHeight || 66;
  const y = el.getBoundingClientRect().top + window.pageYOffset - hdr - 14;
  navTarget = id;                                    // freeze the observer
  window.scrollTo({top: Math.max(0, y), behavior:'smooth'});
  document.querySelectorAll('.nav button').forEach(b=>{
    const on = b.dataset.go === id;
    b.classList.toggle('on', on);
    on ? b.setAttribute('aria-current','true') : b.removeAttribute('aria-current');
  });
}
window.addEventListener('scroll', ()=>{            // release when the scroll settles
  if(!navTarget) return;
  clearTimeout(navSettle);
  navSettle = setTimeout(()=>{ navTarget = null; }, 140);
}, {passive:true});
function initNav(){
  document.querySelectorAll('.nav button').forEach(b=>{
    if(b._bound) return; b._bound = 1;
    b.addEventListener('click', ev=>{ ev.preventDefault(); goSection(b.dataset.go); });
  });
  const io = new IntersectionObserver(es=>{
    if(navTarget) return;                          // don't yank the tab back mid-animation
    es.forEach(e=>{ if(e.isIntersecting)
      document.querySelectorAll('.nav button').forEach(b=>b.classList.toggle('on', b.dataset.go===e.target.id)); });
  }, {rootMargin:'-64px 0px -70% 0px'});
  ['ringkasan','onchain','news','token'].map(i=>document.getElementById(i)).filter(Boolean).forEach(s=>io.observe(s));
}
```

Notes that mattered:
- **A fixed time lock is not enough** (a 700 ms `Date.now()` guard let the observer flip the tab back
  on a desktop-width long scroll). Use the *scroll-settle* pattern above; it is distance-independent.
- Tap affordance: `touch-action:manipulation` (kills the 300 ms tap delay), `:active{transform:scale(.93)}`,
  `-webkit-tap-highlight-color:transparent`, `transition:transform .14s ease`.
- `section{scroll-margin-top:88px}` (+ `aria-current`) for keyboard/anchor jumps.
- Keep `initNav()` idempotent with a `b._bound` flag — it is re-called after every `render(d)`.
- **Never name a page-level function after a `window` built-in** (`scrollTo`, `open`, `focus`, `print`,
  `close`, `name`, `status`, `top`, `parent`, `length`). Same for `id="..."` colliding with globals.

## 2. Number locale: match the user's other channels

The dashboard showed `$1,382` / `0.39` while every Telegram report the user reads is Indonesian
(`$1.389,15`). Fixes used:

```js
const F  = n => (n==null||isNaN(n)) ? '—' : new Intl.NumberFormat('id-ID',{maximumFractionDigits:0}).format(n);
function SC(x,d){ if(x==null||isNaN(x)) return '—'; return Number(x).toFixed(d==null?1:d).replace('.',','); }
// FU(): group with F(), and swap the decimal point in M/B suffixes too
const PX = p => p==null ? '—' : (p>=1 ? '$'+(p>=100?p.toFixed(0):p.toFixed(2)) : '$'+Number(p).toPrecision(4));
```

- Keep a **separate `PX()` for prices** and leave those dot-decimal (`$0.5045`, `$2.14`) — crypto
  convention; only the money/percent/score figures go Indonesian. Doing it piecemeal (SC for one
  price path, toPrecision for another) produced `$2,14` next to `$0.5045` in the same card.
- **Never feed an `SC()`/`F()` output into a CSS/SVG numeric context** (`style="width:${...}%"`,
  `stroke-dasharray`) — the comma breaks the value. Compute widths with raw arithmetic.
- Privacy toggle interplay: the hide-nominal layer must mask **JS-formatted** figures *and* figures
  embedded in Python-generated sentences (`"di posisi $579"`, `"±$894M"`) — mask with a regex at
  render time (`s => HH ? String(s).replace(/\$\s?[\d][\d.,]*\s?[KMBT]?/gi, '$••••') : s`) and also mask
  price fields, otherwise the leak check in the probe fails.

## 3. Metric-tile grids: `1fr` is not enough — use `minmax(0,1fr)`

A 4-column tile row whose tiles each carry a 1 px border made the grid's min-content 3 px wider than
the card, so `documentElement.scrollWidth` was 393 on a 390 viewport (invisible at a glance, real on a
phone). Fix and the rest of the tile hygiene:

```css
.tiles,.oct,.whalerow{display:grid;gap:7px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media(min-width:760px){ .tiles,.oct,.whalerow{grid-template-columns:repeat(4,minmax(0,1fr))} }
.oct .k,.whalerow .k{min-height:16px}               /* label reserves one line */
.mx .m{display:flex;flex-direction:column;justify-content:flex-end;min-height:66px}
.mx .k{min-height:27px}                             /* reserves TWO lines */
```

- **Labels wrap differently → values stop aligning.** Reserve a fixed label height (2 lines for metric
  tiles) *and* shorten the labels (`Suplai terkunci`→`Terkunci`, `Swing 1 sigma`→`1-sigma`) instead of
  relying on `justify-content:space-between`.
- Keep every tile row on the **same column count** in a card (a 3-col row above a 2-col row reads as
  "broken axis"); add a 4th metric (e.g. `Transaksi 24j`) rather than mixing 3 and 2.
- Right-aligned money + a small chip: make the money cell a flex column
  (`.lus{display:flex;flex-direction:column;align-items:flex-end;gap:3px}`) so the chip drops *below*
  the number. Putting the chip inline in the same cell breaks the right edge for every other row, and a
  long chip (`USDT nganggur`) overlaps the `%` column — shorten it (`idle`) and add
  `overflow:hidden;text-overflow:ellipsis;min-width:0` on the label cell.
- Bars scaled 0–100 hide tiny categories; scale to the **max value in the group** (`v/mx*100`) with
  `min-width:3px` so a 1.6 % item is still visible.
- `cls(v)` should treat |v|<0.05 as neutral — otherwise a `+0.0M` / `0.0%` renders green.

## 4. Verification checklist for a nav/tap change

1. `node --check` on the extracted inline `<script>` (cheap syntax gate) — extract with
   `h[h.rindex('<script>')+8 : h.rindex('</script>')]`.
2. `scripts/nav_tap_probe.py <url>` — taps every nav button and asserts each section lands at the same
   offset with the right tab active; also asserts `window.scrollTo` is not shadowed.
3. Re-run the layout probe (`scripts/mobile_probe.py`) — overflow must stay 0 at 390 AND 1366.
4. Bump the service-worker cache name (`zemizrisk-v1` → `-v2`) whenever the shell changes, and tell the
   user to close/reopen the installed app; then `curl` the tunnel and grep for a new symbol to prove the
   public URL serves the fixed build.
5. `vision_analyze` the post-tap screenshot (the section under the sticky header, the highlighted tab).
