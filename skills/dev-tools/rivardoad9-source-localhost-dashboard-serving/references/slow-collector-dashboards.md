# Slow-collector dashboards: snapshot file, async refresh, content assertions (5 Okt 2026)

Second dashboard built on the *same* server as `references/localhost-dashboard-serving.md` (the ZemizTracker
worked example). The user asked for a portfolio-risk page: "apps/ai tools monitor risiko portofolio …
portfolio health, token allocation, kolom news yang diverifikasi, tarik data on-chain", then "desainnya
modern ya". Route pair added to the existing `whale_board_server.py` (port 8787):

| Piece | Path |
|---|---|
| Collector CLI (single writer) | `~/.hermes/scripts/porto_risk.py` — `--save` → `~/.hermes/data/porto_risk.json`; also `--json`, `--delta`, `--token SYM`, `--ringkas` |
| Intel layer (on-chain flow + news) | `~/.hermes/scripts/porto_intel.py` |
| Page | `~/.hermes/scripts/porto_dashboard.html` (vanilla JS + inline SVG, ~25 KB, no CDN) |
| Routes | `/risk`, `/zemizrisk`, `/portofolio` (page) · `/api/risk`, `/api/porto` (JSON) |
| Delta cron | `8621c1f8d1ba` — `no_agent`, `script=porto_risk_delta.sh`, `*/30 * * * *` |

## 1. The collector takes 25 s — never call it from the HTTP handler

`/api/risk` reads the JSON file and returns it immediately, stamped with meta the UI can show:

- `_age_s` = `time.time() - os.path.getmtime(path)` → the page prints "updated Ns ago" instead of implying
  the number is live.
- `_running`, `_err` = state of the background refresh.
- Stale (`age > RISK_TTL`, default 600 s) **or** `?refresh=1` → start a **daemon thread** doing
  `subprocess.run([sys.executable, "porto_risk.py", "--save"], capture_output=True, timeout=240, cwd=…)`
  behind a `threading.Lock`, then return the *current* file with `_running: true`. Never block the request.
- `?refresh=1` is the one path worth gating on the token (`403` when `k` is wrong or missing).
- A missing snapshot returns a friendly JSON error telling the caller the refresh just started — not a 500.

Corollary: the CLI itself is the only writer, so page loads never trigger upstream API traffic. The cron
(`--delta`) keeps the file fresh on its own cadence.

## 2. Assert content, not just layout

The screenshot pass (`vision_analyze`) found truncation and an "allocation legend doesn't sum to 100%"
problem, but it MISSED a `${P(wd,1)+'M'}` render → `+0.0%M` bug and could not tell that the donut had
silently dropped a segment. A DOM read-back caught both in one pass:

```python
doc.querySelectorAll('.leg .it')      # legend rows + innerText → do the % sum to 100?
doc.querySelectorAll('.ocgrid .v')    # value cells → is every formatter output sane? ("+0.0M" vs "+0.0%M")
doc.querySelectorAll('svg circle')    # 1 track + N segments → did a segment vanish?
doc.querySelector('.donut .mid').innerText
scrollWidth - clientWidth             # 0 at 390px AND 1366px
pageerror / console 'error' listeners # a silent JS syntax error shows up here
```

Run `scripts/dashboard_content_probe.py URL "<selectors>" TAG` — it prints all of the above and asserts
`overflow == 0` + no JS errors. Then compare the printed values against the source dataset (the page is a
view, not the truth).

## 3. One number, one place

Two real inconsistencies from rendering the same quantity from different inputs:

- Hero total `$1,384` vs chart-centre `$1,385` — one derived from the raw float, the other from the sum of
  rounded segments. Fix: derive both from the same rounded parts.
- `HHI 0.38` in one pill and `HHI 0.39` in the text below — Python `round()` / `f"{x:.2f}"` and JS
  `toFixed(2)` disagree at exact halves. Fix: round **once in the source language** and reuse that value.
- Formatter rule learned the hard way: never append a unit suffix to a percent formatter
  (`P(x) + 'M'` → `+0.0%M`). Build a separate numeric formatter (`((x>=0?'+':'')+SC(x,1)+'M')`).

## 4. Disk cache with stale-fallback for rate-limited upstreams

A 20–30 s collector hitting keyless APIs every 30 min *will* hit CoinGecko 429s. An in-process TTL cache is
useless for a cron-invoked CLI, so cache to a file keyed by URL hash:

```python
cache = json.load(open(CACHE))                     # {"<hash(url)>": {"ts":…, "data":…}}
hit = cache.get(k)
if hit and time.time() - hit["ts"] < TTL: return hit["data"]
data = fetch(url)
if data is not None: cache[k] = {"ts": time.time(), "data": data}; json.dump(cache, open(CACHE, "w"))
return data if data is not None else (hit or {}).get("data")   # ← stale beats None
```

Also cache contract-address lookups with a long TTL (~7 days) — they never change.

## 5. A key/token gate on a phone UI must be enterable *in the page*

The board already had `POST /api/watchlist` add/remove, but the edit box only rendered when the URL carried
`?k=<token>`, so the user's report was "tolong dibikin gw bisa adjust/manage sndiri tickernya" — a
discoverability failure, not a backend one. Fix: an always-visible **🔑 "Masukin token"** button that
`prompt()`s once, stores to `localStorage` (`zmz_k`) and re-renders, plus making the hint text itself
tappable. Carry `?k=` into cross-page links (the 🛡️ Risk chip in the board header) so the key survives
navigation.

## 6. Pitfalls hit for real this session

- **JS syntax error → every section renders 0 while the page still "looks loaded"** (header/footer paint,
  body stays "memuat data…"; a 404 favicon also appears in the console). The culprit:
  `(r.stress||{}).btc_-30pct` — a hyphen in a property name requires `["btc_-30pct"]`. `node --check` on
  the extracted inline `<script>` is a one-shot detector; run it before the browser probe.
- **Playwright version skew**: driver wanted `chromium_headless_shell-1243`, the host had `chromium-1223`
  → `Executable doesn't exist`. Fix: pass
  `executable_path` from `glob("/home/ubuntu/.cache/ms-playwright/chromium-*/chrome-linux64/chrome")[-1]`.
  Not a broken-browser situation; do not re-install.
- **`pkill -f <script>.py` self-kill struck again** — the agent's own command line contained
  `pgrep -af "whale_board_server.py"` while the keeper (which pkills that pattern) ran in the same call, so
  the shell got SIGTERM (`exit_code: -15`). Use `pgrep -af "whale_board_[s]erver"` for every reference to a
  pkilled process, including read-only ones.
- **Don't duplicate a highlighted fact**: the unlock-cliff banner plus the same line in the negatives list
  read as two entries — filter the list item when the banner already carries it.
- **Cash belongs in the allocation chart** unless you want a legend summing to <100% and a "your numbers are
  broken" report — and label the cap per row (`cap 12%`) with a one-line explanation of what a cap is.
