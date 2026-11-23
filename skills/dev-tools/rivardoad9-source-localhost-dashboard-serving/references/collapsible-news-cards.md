# Collapsible feed cards ("headline-nya aja yang ijo, isinya ada pencet more…")

The ask, verbatim: *"yg bagian news kan semua font warna ijo ya, paling dibikin ijo headline post aja,
isinya ada pencet kayak more…, jadi kalau mau baca bisa klik."* Two separate problems hide in that
sentence — a **colour-scope** bug and a **progressive-disclosure** request. Fix them in one edit.

## 1. Why the whole card is green

A blanket anchor rule paints every link, headline included:

```css
a{color:var(--lime);text-decoration:none}     /* the offender */
```

Scope the accent to the one element that should carry it and hand the body back to normal text:

```css
.ni .t{color:var(--up);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.ni .t a{color:var(--up)}
```

Rule of thumb: **never let a global `a{}`/`body{}` colour decide the information hierarchy** — a card
with two levels of emphasis (headline + body) must set both levels explicitly.

## 2. The reveal pattern (collapsed by default, click to expand)

Keep ONE card element and toggle a class; do **not** re-render on click (that kills scroll position and
any open state).

```css
.ni .more{display:inline-block;margin-top:7px;font-size:11px;font-weight:700;letter-spacing:.4px;
  color:var(--cyan);cursor:pointer;user-select:none;border-bottom:1px dashed rgba(20,184,255,.5)}
.ni .nfull{display:none}
.ni.open .t{display:block;-webkit-line-clamp:unset;overflow:visible;color:var(--txt)}
.ni.open .nfull{display:block}
.ni .nb{font-size:13px;line-height:1.5;color:var(--txt);margin-top:7px;padding-top:7px;
  border-top:1px dashed var(--line)}
.ni.open .more{color:var(--dim2);border-bottom-color:transparent}
```

Markup from a helper so the token list and the "Pasar" list share one renderer:

```js
const nit = (it,i) => `<div class="ni rv" style="animation-delay:${i*35}ms">
    <div class="t">${esc(it.title)}</div><span class="more">more…</span>
    <div class="nfull"><div class="nb">${esc(it.title)}</div>
      <div class="m">${nbadge(it)}<span>${esc(it.source||'')}</span><span>·</span><span>${ago(it.utc)}</span>
        ${it.link?`<a href="${esc(it.link)}" target="_blank" rel="noopener" style="margin-left:auto;color:var(--cyan)">${ic('link','sm')} sumber</a>`:''}</div>
    </div></div>`;
```

**One delegated listener registered ONCE at boot** — the feed re-renders every refresh, so a listener
attached inside the render would leak/multiply:

```js
document.addEventListener('click', e=>{
  const more = e.target.closest('.ni .more'); if(!more) return;
  const card = more.closest('.ni'); if(!card) return;
  more.textContent = card.classList.toggle('open') ? 'tutup' : 'more…';
}, {passive:true});
```

Design notes that made it read right:
- The headline is **not** an `<a>` in the collapsed state — clicking a headline must expand, not
  navigate away. The link lives inside the expanded body ("sumber").
- Flip the affordance label (`more…` → `tutup`) so the card is obviously reversible; keep a dashed
  underline while collapsed, drop it when open.
- 2-line clamp for the collapsed headline; when open, show the same text again as the body (`--txt`)
  plus the badges/source/time, so the reader gets metadata only after opting in.
- Add one line to the section's footer note: `klik "more…" buat baca isi penuh` — the user should not
  have to discover the interaction.

## 3. Prove it in a real browser (this is the cheap gate)

`node --check` on the extracted inline script catches syntax only. Assert the *behaviour*:

```python
import time, json
from playwright.sync_api import sync_playwright
CHROME = "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"
JS = """(() => {
  const f=document.querySelector('.ni'), t=f.querySelector('.t'), cs=getComputedStyle(t);
  return {color:cs.color, clamp:cs.webkitLineClamp, more:f.querySelector('.more').innerText,
          body:getComputedStyle(f.querySelector('.nfull')).display};
})()"""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"], executable_path=CHROME)
    pg = b.new_page(viewport={"width":420,"height":950}, device_scale_factor=2)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8787/risk", wait_until="networkidle", timeout=45000); time.sleep(3)
    print("BEFORE", pg.evaluate(JS))                       # expect green + clamp "2" + nfull "none"
    pg.eval_on_selector(".ni .more", "e => e.click()"); time.sleep(.5)
    print("AFTER ", pg.evaluate(JS))                       # expect --txt + clamp "none" + nfull "block"
    pg.eval_on_selector_all(".sent", "els => els[0].scrollIntoView({block:'center'})")
    pg.screenshot(path="/tmp/sent.png")                    # then vision_analyze the shots
    print("ERRORS", errs)
```

Pass = colour/clamp/display flip exactly as above, `pageerror` list empty, and the screenshot shows the
new widget where it belongs. Assert **each new field's text** in the DOM (see the SKILL.md pitfall about
`fng.v` vs `fng.value`) — a green API check proves nothing about the page.

Deliver the proof as images: screenshot the collapsed card, the expanded card, and the new widget, send
all three over the chat (`MEDIA:` paths) — the user judges a UI change visually, not from prose.
