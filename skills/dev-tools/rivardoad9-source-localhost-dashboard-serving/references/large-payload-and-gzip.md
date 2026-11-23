# Large payloads, gzip, and the "buffering" complaint (Zemiz Chain, 10 Oct 2026)

## Symptom vs cause

User: "yg zemiz chain buffering" (page loads, then spins). The instinct is "server mati" — it was not.
Measured first, and the numbers contradicted the instinct:

```bash
ss -ltnp | grep 8790                                   # listener alive
curl -s http://127.0.0.1:8790/healthz                  # {"ok": true, ...}
curl -s -o /dev/null -w '%{http_code} %{time_total}s %{size_download}B\n' http://127.0.0.1:8790/
#  200 0.0009s 19703B      <- HTML is FAST
curl -s -o /dev/null -w '%{http_code} %{time_total}s %{size_download}B\n' http://127.0.0.1:8790/api/chain
#  200 7.248s 8688449B     <- cold cache: 7.2 s build
#  200 0.171s 8688449B     <- warm cache, still 8.69 MB EVERY request (Cache-Control: no-store)
curl -s -o /dev/null -w '%{http_code} %{time_total}s %{size_download}B\n' <tunnel>/api/chain
#  200 6.789s 8688449B     <- same 8.69 MB over the quick tunnel
```

Health checks all pass, so "is it down" is the wrong question. The right question:
**how many bytes does one page view pull?** Rule of thumb: a phone-accessible JSON API should be
well under 1 MB; anything over ~2 MB explains a spinner on mobile data.

Why it got that big: `hl_insider_edges.jsonl` (16 MB, 39,069 rows) was serialised row-by-row into the
payload, unaggregated and uncompressed. The client already aggregated (`agg.get(k)` keyed by
`src|dst` in the HTML) — 39,069 rows collapsed to 1,738 unique pairs client-side, i.e. the wire
carried ~22x more than the view used.

## The fix (4 lines of behaviour, no UI change)

`insider_board_server.py`:

1. `import gzip`.
2. gzip in `_send` when the client accepts it and the body is worth compressing:

```python
def _send(self, code, body: bytes, ctype: str, cache: str = "no-store"):
    # Payload papan ini ~8,7 MB JSON; gzip turunin ke ~0,6 MB biar HP nggak buffering.
    if len(body) > 1024 and "gzip" in (self.headers.get("Accept-Encoding") or "").lower():
        body = gzip.compress(body, 6)
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Vary", "Accept-Encoding")
    else:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
    self.send_header("Content-Length", str(len(body)))
    self.send_header("Cache-Control", cache)
    self.end_headers()
    self.wfile.write(body)
```

3. cache TTL `12` → `60` seconds in `payload()`.
4. prewarm the cache so nobody pays the build:

```python
def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    print(f"Zemiz Chain jalan di :{PORT}")
    threading.Thread(target=payload, daemon=True).start()
    srv.serve_forever()
```

## Verification (do all of it, in this order)

```bash
# 1. compression is actually negotiated and the header is real
curl -s -o /dev/null -D /tmp/h_gz.txt -H "Accept-Encoding: gzip" -w 'http=%{http_code} bytes=%{size_download}\n' <url>/api/chain
grep -i 'content-encoding\|content-length' /tmp/h_gz.txt    # Content-Encoding: gzip / 629598

# 2. same thing through the tunnel (proves the proxy passes it through)
curl -s --compressed -o /dev/null -w 'http=%{http_code} waktu=%{time_total}s bytes=%{size_download}\n' <tunnel>/api/chain

# 3. NO DATA LOSS: gunzip one variant, diff the hashes
curl -s -H "Accept-Encoding: gzip" <url>/api/chain | gunzip -c > /tmp/a.json
curl -s <url>/api/chain > /tmp/b.json
sha256sum /tmp/a.json /tmp/b.json     # identical hashes
```

Measured result: `LOKAL + gzip 629,598 B` vs `LOKAL tanpa gzip 8,688,449 B`; public tunnel
`0.95 s`; HTML `0.32 s`. Byte-identical sha256 `265c4a54…`.

Use Python's `gzip` for the size estimate rather than shelling out when the payload is already on
disk (`/tmp/zc_size.py` pattern): it also prints the unique-pair count that tells you whether
server-side aggregation is worth doing later.

## Sequencing notes

- Edit the server file → `python3 -m py_compile <file>` → restart only the board process (the keeper
  cron relaunches it) → re-measure. Backup first: `cp -a <file> <file>.bak-YYYYMMDD`.
- Restarting just the Python server does NOT rotate the quick-tunnel URL, so the user's saved link
  stays valid. Say that explicitly in the report.
- The service worker in this app is `network-only` for `/api/*` (see `references/pwa-installability.md`),
  so a server-side fix needs no cache-name bump: tell the user to reload the page (close/reopen the
  tab) and nothing more.
- A browser-side confirmation would need a Chromium; when none is launched on the host, the
  curl + sha256 pair is the honest substitute — state which one you used instead of implying a
  render was checked.
