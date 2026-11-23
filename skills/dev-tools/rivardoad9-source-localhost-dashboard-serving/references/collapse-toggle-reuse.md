# Reusing a collapsible card's `more…` toggle for a second card class

Companion to `collapsible-news-cards.md` (which builds the first card, `.ni`). Hit when the user asks
for a *second* collapsible widget on the same page (e.g. a per-token reasoning block, class `.th`).

## The two halves, both mandatory

```js
document.addEventListener('click', e=>{
  const more = e.target.closest('.ni .more, .th .more'); if(!more) return;
  const card = more.closest('.ni, .th'); if(!card) return;
  more.textContent = card.classList.toggle('open') ? 'tutup' : 'more…';
}, {passive:true});
```

```css
.ni .more,.th .more{ /* one paired rule, never a duplicated block */ }
.th .nfull{display:none}              /* ← the half everyone forgets */
.th.open .nfull{display:block}
.th.open .td{display:block}           /* only if the summary line is line-clamped */
```

Extending the JS selector alone leaves the new class **fully expanded**: the collapsed default lives in
CSS, not JS. The symptom misleads — everything is visible, yet the label still flips to `tutup` when
clicked, so it reads like a JS bug. It is not.

## Probe it correctly

Assert `is_visible()` on the collapsed body, not the button label:

```python
print(await pg.locator(".th .nfull").first.is_visible())   # expect False before the click
await pg.locator(".th .more").first.click()
print(await pg.locator(".th .nfull").first.is_visible())   # expect True after
```

The label flips in both the broken and the fixed version, so a label-only assertion passes on the bug.

## Reminders that outlive the edit

- Keep the listener registered **once** at boot (delegation) — cards re-render on every refresh.
- Different card classes can carry different collapsed defaults: clamp the summary line (2–3 lines) for
  dense blocks, and re-render the verdict/summary line **outside** the collapsed region so the user
  always sees the conclusion without clicking.
- Every page change needs a new service-worker `CACHE` string, or the installed PWA keeps the old HTML
  and the user reports "gak ada yang berubah".
