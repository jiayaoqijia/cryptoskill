---
name: compress-and-page-large-payloads
description: Use when an endpoint returns multi-megabyte JSON and serialization or transfer dominates latency — project only needed fields, paginate with a cursor, and compress on the wire.
---

# Compress and page large payloads

A 5 MB JSON response costs CPU to serialize, memory to buffer, bytes to transfer, and time to parse on the client. Most of it is fields nobody reads. Project fewer columns, page the rest, and compress what remains.

## Procedure

1. Measure the response first:
```bash
curl -s -o /dev/null -w 'bytes=%{size_download} time=%{time_total}\n' https://api/items
curl -s --compressed -o /dev/null -w 'bytes=%{size_download}\n' https://api/items
```
2. Project only the fields the caller uses — drop the `SELECT *`. Reference data (country names, avatars) belongs in one joined-and-deduped set, not repeated per row.
3. Paginate with a cursor, not `OFFSET`: `WHERE id > $cursor ORDER BY id LIMIT 100`. `OFFSET 100000` reads and discards 100k rows on every page.
4. Cap page size server-side: `limit = min(requested, 500)`. An unbounded page is a memory DoS.
5. Enable compression with `Content-Encoding` and `Vary: Accept-Encoding`. JSON compresses 5-10x; encode at gzip level 5-6, since the last levels cost CPU for little gain, and prefer compressing at the CDN edge.
6. Stream large responses (`Transfer-Encoding: chunked`) instead of buffering the whole payload; buffering doubles memory and delays the first byte.
7. For genuinely huge exports, switch to a file endpoint plus a signed URL rather than streaming gigabytes through the request path.

## Pitfalls

- Compressing an already-compressed payload (images, gzip) wastes CPU for no gain.
- `Vary: Accept-Encoding` missing, so a CDN caches the uncompressed body and serves it to a gzip client.
- Breaking `ETag`/`Content-Length` caching by compressing per request with a random encoding.
- Double serializing: build a dict, `json.dumps`, then re-parse just to filter fields.
- `OFFSET` pagination that gets slower each page and can skip or duplicate rows under concurrent writes.
- Compressing tiny responses, where gzip headers make a 200-byte body larger.

## Verification

    curl -s -H 'Accept-Encoding: gzip' -o /dev/null -w 'enc_bytes=%{size_download}\n' https://api/items
    curl -s -o /dev/null -w 'raw_bytes=%{size_download} time=%{time_total}\n' https://api/items
    # pass: response drops by >70% with gzip, p99 down, page ceiling enforced

Report payload bytes before and after compression, the page size limit and cursor field, the fields dropped, and the p99 change.
