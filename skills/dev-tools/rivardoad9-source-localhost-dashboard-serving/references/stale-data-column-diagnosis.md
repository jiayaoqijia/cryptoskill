# "This column looks stale" — diagnose the filter before the feed

Proven 5 Oct 2026 on the Zemiz Risk dashboard (`porto_dashboard.html` + `/api/risk` + cron `*/30`).
The user's complaint was about the **News** column: *"news yang ada zemiz risk udh kek lama bgt"*.

## 1. Measure freshness the way the UI sees it

The collector was healthy — the items table had rows from the current hour. What was stale was the
**per-entity view** the renderer actually reads. So the first measurement is never
`select max(published_utc) from items`; it is:

```sql
select sym, count(*), max(pub_utc) from <per_entity_table> group by sym order by max(pub_utc);
```

and the same over the merged, tiered structure the API returns (`news.by_token[sym][0].utc`).
Result that day: whole-table max = today 22:09 WIB, but per-holding max = ONDO 25 Sep, WLD 17 Sep,
TAO/BOME **zero rows** — tier-1 crypto press simply doesn't write about small tickers. The fix was
adding per-entity official sources (`hermes-cron-automation` →
`references/walled-platform-news-via-search-index.md`), not touching the feed.

Rule: when a lane can go quiet for structural reasons, report the per-entity freshness distribution
in the same breath as the fix, so the user can see which entities were starved and which were fine.

## 2. Put a clock in the section header

A fixed "30 hari terakhir" window reads as static no matter how fresh the data is. Carry
`updated_utc` (max publish time across the merged per-entity set) in the JSON API and render it:

```js
`${nver} lolos verifikasi · update terbaru ${nw.updated_utc ? ago(nw.updated_utc) : '—'} · ${nw.dropped} noise dibuang`
```

`ago()` was already in the page's helpers, so this was a one-line change — and it ends the staleness
conversation even when the newest legitimate item is hours old. Add "N noise dibuang" next to it:
showing what the filter rejected is what makes a sparse column credible.

## 3. Data-layer details that matter for dashboard lanes

- **Adding a source class should not require a UI change.** Write new rows into the same DB the
  dashboard already reads, and merge/tier them inside the reader function (`news_for()`), so the page
  and the delta-alert job both pick them up. The card's existing `it.source` label then carries the
  new provenance ("X resmi @opentensor", "world.org (situs resmi)").
- **Label confidence in the row, not in a legend.** Two similar-looking sources with different trust
  levels (posts by the official account vs third-party posts mentioning it) must be visually distinct
  on the card, otherwise the user reads mentions as official statements.
- **Re-filter stored rows, don't just fix the filter.** With `INSERT OR IGNORE` on a stable key,
  junk written before a filter change sits in the table forever and keeps rendering. On every save:
  load `(key, title)`, delete rows failing the current junk/noise rules, then insert.
- **Service worker**: network-first for navigations (fetch → fall back to cache) is enough for these
  pages; no cache-name version bump needed when the HTML changes. Still tell the user
  "hard-refresh kalau masih keliatan versi lama" in the same reply as the change.

## 4. Verification pass before reporting

1. `curl -s http://127.0.0.1:<port>/api/<data>` → assert the new field is present and the timestamp
   is recent, per entity.
2. `curl -s http://127.0.0.1:<port>/<route> | grep -o "update terbaru[^<]*"` → confirm the template
   edit shipped (the text appears inside the JS template even before render).
3. Run the lane's own delta job by hand (`bash <lane>_delta.sh`) and read its output: it must print
   only the material new items and exit 0, and stay empty on the next run.
