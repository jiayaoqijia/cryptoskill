---
name: paginate-until-the-cursor-is-exhausted
description: Use when a list endpoint returns pages. Drive the loop to exhaustion with a termination condition, a cursor guard, and a count check — one page is not the dataset.
---

# Paginate until the cursor is exhausted

One page is not the dataset. Most partial-data bugs are a loop that stopped after page one, or
that quietly repeated the same page forever.

## Procedure

1. Read the page shape from the response: `{"data": [...], "next_cursor": "...", "has_more": true}` versus `{"items": [...], "total": 5210}`. They need different loops.
2. For cursor pagination loop until the cursor field is null/empty — never until the page is short:
   ```python
   items, cursor = [], None
   while True:
       r = get("/v1/items", params={"limit": 100, "cursor": cursor}).json()
       items += r["data"]
       cursor = r.get("next_cursor")
       if not cursor:
           break
   ```
3. For offset pagination stop when `len(page) < limit` or `offset >= total`. Read `total` from the first page only; it moves under you.
4. Guard a non-advancing cursor: hash each cursor and abort on the second sighting.
   ```python
   seen = set()
   if cursor in seen: raise RuntimeError("cursor did not advance")
   seen.add(cursor)
   ```
5. Set a hard max-pages ceiling (e.g. 10000) so a server bug cannot loop you forever.
6. When `has_more` and `next_cursor` disagree, trust the cursor field and log the mismatch.
7. After the loop compare `len(items)` to any reported `total` and warn on any mismatch.

## Pitfalls

- Breaking on an empty page skips items when a filter empties a middle page; break on the cursor.
- Many APIs silently cap `limit` (asked 500, got 100) — trust the returned limit, not yours.
- Offset pagination over a live table double-counts or skips rows inserted mid-scan; prefer a cursor or snapshot.
- A 200 with `data: []` and a set `next_cursor` is legal; stopping there loses the rest.
- Cursors expire (often 5-15 min); a slow consumer must restart the scan, not reuse a stale cursor.

## Verification

    wc -l out/all_items.ndjson
    python -c "import json;d=json.load(open('out/page_1.json'));print(len(d['data']),d.get('next_cursor'))"

Report: "Fetched 12,480 items over 125 pages; server total 12,480; final cursor null."
