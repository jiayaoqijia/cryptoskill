---
name: localhost-dashboard-serving
description: Use when serving agent data as a phone-accessible page.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dashboard, localhost, cloudflared, tunnel, watchdog, web-ui, mobile]
    related_skills: [third-party-monitor-cloning, hermes-cron-automation, webhook-receivers, cron-output-style]
---

# Serving agent data as a localhost dashboard (and getting it onto the user's phone)

## When to Use

Load when the user asks to *see* something the agent already computes, instead of only getting
Telegram messages: "bikin webnya", "atau localhost yg bisa gw akses kyk gitu", "bikin dashboard
dong", "gw mau liat sendiri", "bisa dibuka dari HP ga", or names a product ("zemiztracker") for
such a page.

Typical trigger chain: a CLI tool/monitor was just built (see `third-party-monitor-cloning`) and the
next ask is always "bisa gw akses sendiri nggak?". Answer: **stdlib HTTP server on 127.0.0.1 +
cloudflared quick tunnel + a keeper cron**. No dependencies, no account, no inbound port.

Deliver it BRANDED (title, `/<name>` route, favicon, mobile-app meta) — the user treats this as a
product of theirs, not a debug view. Terse one-word messages like "zemiztracker" mean *name it that*.

## Architecture (4 parts, all cheap)

1. **Server** — Python stdlib `ThreadingHTTPServer`, bound to `127.0.0.1` only (never `0.0.0.0`;
   the tunnel is the only public path). Routes: `/` plus `/<name>` (same page), `/api/<data>` (JSON),
   `/api/refresh` (force), `/healthz`. See `templates/localhost_dashboard_server.py`.
2. **Cache + history** — a daemon thread refreshes the upstream data every `TTL` (60 s) into memory;
   requests never hit the upstream API. Append one JSONL row per refresh (`~/.hermes/data/<tool>_history.jsonl`,
   trimmed to a few hundred lines) so the page can draw a real trend chart instead of a single number.
   Reuse the CLI tool's own functions by loading it with `importlib.util.spec_from_file_location`.
3. **Page** — one self-contained HTML file next to the server (no CDN, no build step, inline CSS/JS),
   rendered client-side from the JSON API with a `fetch` refresh loop. Dark theme, tabular numbers,
   `@media(max-width:620px)` for phone. Put a brand in `<title>` + `<h1>`, an inline data-URI SVG
   favicon, and `theme-color` + `apple-mobile-web-app-*` so "Add to Home Screen" looks like an app.
   Multi-module app (tabs: overview / content / calendar / automation / accounts): split into
   `static/index.html` + `app.js` + `styles.css` and route on `location.hash` (`#/konten`), with one
   render function per tab hitting its own `/api/*`. Each tab then has its own URL he can bookmark
   and share, the shell (sidebar, top bar, mobile nav) is written once, and the CSS design tokens
   carry straight over from the approved mockup.
4. **Exposure + keeper** — `cloudflared tunnel --url http://localhost:<port>` (quick tunnel, no
   account) and `templates/service_keeper.sh` running from a `no_agent` cron every 5–10 min that
   restarts the server/tunnel if dead and **prints the URL only when it changed**.

## Keeper + cron: the no-notification-spam pattern

Quick-tunnel URLs rotate on every restart, so never hand the user a bare URL without a way to learn
the new one. The keeper script is idempotent and does three things:

```bash
curl -sf -m 5 "http://127.0.0.1:$PORT/healthz" >/dev/null || restart_server   # pkill + setsid nohup
pgrep -f "cloudflared tunnel --url http://localhost:$PORT" >/dev/null || restart_tunnel
URL=$(grep -ho 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUN_LOG" | tail -1)
# write URL to data/<tool>_url.txt; print the message ONLY if it differs from the *_seen.txt copy
```

The `pgrep` line proves a process exists, not that the tunnel works. cloudflared can sit in a
reconnect loop (`ERR failed to serve tunnel connection … Retrying connection in up to 1m4s`) with the
URL already dead, and a pgrep-only keeper stays silent for hours. Gate on the public URL too:
`curl -s -o /dev/null -w '%{http_code}' -m 15 "$URL<route>"`; on a non-200 kill the tunnel and
restart it, accepting the URL rotation rather than keeping a link that 404s.

Register it as `no_agent=true`, `deliver=origin`, `script=<keeper>.sh`: empty stdout = no message, so
the cron is silent on the happy path and only pings the user when the link actually changes. That is
the same delta-only rule as the alert lanes (`cron-output-style`, `hermes-cron-automation`). A second
`no_agent` job runs the data scanner itself on its own cadence.

**`script=` must be a plain file living inside `~/.hermes/scripts/`.** An absolute path is rejected
outright, and a symlink to the project copy is rejected as `escapes the scripts directory via
traversal` — so `ln -s ~/studio/keep.sh ~/.hermes/scripts/` fails registration even though the file
reads fine. Copy the keeper in (`cp`, then `chmod +x`) and remember the cron now runs the *copy*:
after editing the project version, re-copy it, or the job keeps firing the stale script.

Restart durability: the detached child must be started **inside the script file** with
`setsid nohup ... >>log 2>&1 </dev/null &`. Do that from the script, not from an agent terminal call.
On hosts where `systemctl --user` fails with "Failed to connect to bus: No medium found" (Hermes
gateway as a system service), script + cron keeper IS the supervisor — don't fight systemd.

**After a host reboot/upgrade, bring lanes back one script per call.** Each keeper script starts a
server *and* a tunnel and waits ~20 s for health, so a loop over four of them blows past the 420 s
tool timeout and you lose which lane failed. Run `timeout 70 bash <script>.sh` per call, then verify
the layer that matters: every port 200 locally **and** every saved tunnel URL 200 publicly. Cron jobs
that logged an error during the boot window (`exit -15`) are not broken jobs — the gateway was still
starting; they reschedule themselves, and the only follow-up needed is re-running a data job whose
slot was missed. Quick tunnels rotate on reboot, so any external webhook pointed at the old hostname is
silently dead: hand the new URL over in the same reply.

## Verify before reporting (all three layers)

1. **Local**: `curl -s -o /dev/null -w '%{http_code}'` on `/`, `/<name>`, `/api/<data>`, `/healthz`.
2. **Public**: repeat the same curls against the tunnel URL and assert the real payload — a 200 with
   `size_download` near the file size, and `grep -o '<title>[^<]*</title>'` matching the brand.
3. **Layout in a REAL browser** (best signal — do this whenever the ask is about looks/mobile).
   A Playwright chromium build already exists on this host: binary
   `/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome` (no `chromium`/`google-chrome`
   on PATH, but this works). Install the driver once into a throwaway venv:
   `~/.hermes/bin/uv venv /tmp/pwenv && ~/.hermes/bin/uv pip install --python /tmp/pwenv/bin/python playwright`
   then `p.chromium.launch(executable_path=<that path>, args=["--no-sandbox","--disable-dev-shm-usage"])`.
   Screenshot at the phone viewport (`viewport={"width":390,"height":844}, device_scale_factor=2,
   is_mobile=True, has_touch=True`, `full_page=True`) and then READ THE IMAGE with `vision_analyze`
   — your model can't see pixels directly, but the vision tool can.
   Measure numerically too, in the same pass: `document.documentElement.scrollWidth` vs `clientWidth`
   (equal = no sideways scroll) and every element whose `getBoundingClientRect().right > vw` (the
   overflow offenders), plus per-row heights of `tr.row`. Copy `scripts/mobile_probe.py` and
   `scripts/mobile_probe_row.py` from this skill.
   Fallback when no browser: run the inline JS under `node` with a DOM stub and print the rendered
   fields (`references/localhost-dashboard-serving.md` has the harness).
   `node --check` on the extracted inline `<script>` is the cheap syntax gate — always run it first.
Then compare the numbers shown against the source dataset one last time — the page is a view, so a
data-parity check is still required.

## Making it actually look good on a phone (and proving it)

Tables are the #1 mobile breakage: a 6-column table with `white-space:nowrap` chips forces its
min-content width past the card, so the WHOLE page scrolls sideways and columns squash/wrap. The fix
that worked (ZemizTracker, 390px): keep the `<table>` markup on desktop and turn each row into a
**grid card** under `@media(max-width:620px)` — never a horizontal scroller.

```css
@media(max-width:620px){
  html,body{overflow-x:hidden;-webkit-text-size-adjust:100%}
  *{-webkit-tap-highlight-color:transparent}
  .hidesm{display:none!important}          /* columns dropped on phone */
  .onlysm{display:inline!important}        /* bits that exist ONLY on phone */
  table,thead,tbody,tr,td{display:block}   /* kill the table box */
  thead{display:none}
  tr.row{display:grid;grid-template-columns:auto 1fr auto auto;
    grid-template-areas:"coin coin coin coin" "px chg net del";gap:5px 10px;padding:10px 12px}
  tr.row td{display:block;border:0;padding:0;text-align:left!important}
  .tw tr.row td:nth-child(1){grid-area:coin}  /* …map each td to an area by nth-child */
  }
```

Rules of thumb that came out of it:
- Map cells to grid areas by `nth-child`; the headers are hidden, so re-add micro-labels with a
  phone-only `<span class="onlysm nl">net </span>` inside the cell.
- Duplicate info you want in two places (e.g. the long/short chips) rather than trying to overlay
  cells — one copy gets `class="onlysm"`, the other stays inside a `class="hidesm"` cell.
- Chips/`white-space:nowrap` are what blow up min-content width. Give them the full row width by
  spanning their cell across all columns; if they must fit a narrow cell, count the pixels first
  (measure `getBoundingClientRect().width` of every chip) instead of guessing.
- Aim for ≤3 lines and ~85px per row (from 138px when it was wrapping), ≤60px on desktop.
- Sticky tab bar (`position:sticky;top:0`) so switching tabs doesn't need a scroll back up; equal
  `flex:1 1 0` on the tabs so they fill the width; `#input{font-size:16px}` so iOS doesn't auto-zoom.
- Header: one line only — shorten badge text with `<span class="hidesm">` (e.g. `54 wallet<span
  class="hidesm"> Hyperliquid</span>`), icon-only refresh button whose label span also carries
  `hidesm`. Watch out: click handlers that rewrite `textContent` must restore the `hidesm` span
  (`b.innerHTML='↻<span class="hidesm"> Refresh</span>'`) and use `event.target.closest('button')`.
- Flat trend charts: if `max-min < 0.2`, draw a **dashed line at mid-height** and label it "stabil"
  instead of a scaled polygon — otherwise the 0-range case renders a fake curve.
- Always screenshot BEFORE and AFTER, stitch them side by side with PIL, and send the image to the
  user (Telegram `MEDIA:` path) — the visual diff is the proof, not prose.

## Pitfalls

- **Wallet/flow graphs: aggregate edges or you ship spaghetti.** 1,000+ raw transfers between ~80
  nodes render as an unreadable bundle (vision-check confirms "spageti"). Three cheap fixes, in order:
  (1) aggregate every `src→dst` pair into one line — sum USD, count `n`, label `$1,2jt ×7`;
  (2) cap what you draw (`sort by usd` → top ~55 pairs; keep the funding-chain `hop-src` links
  unconditionally, dashed) instead of drawing everything above a floor;
  (3) put the floor in the COLLECTOR, not the view, so the JSONL stays clean
  (USDC < ~$1K and HL transfers < ~$10K are dust — token spam like a $500M memecoin to `0x0` also
  has to be filtered by token allow-list).
  Draw edges before nodes (nodes then mask lines crossing them) and give same-lane edges a routed
  bezier so they don't loop through the node boxes.
- **Layered graphs: wrap each depth into lanes.** One column per hop-depth explodes vertically when a
  depth holds 29 nodes (~2,200 px tall inside a horizontal scroller = nested-scroll misery on a phone).
  Chunk each depth into lanes of ~12 (`for(i=0;i<col.length;i+=12) lanes.push(col.slice(i,i+12))`) and
  lay lanes left→right — height caps at ~800 px and the wide scroller stays usable.
- **Trackers adopt `0x000…0` as a "wallet".** A bridge/withdraw destination of the zero address gets
  added like any fresh wallet, and its on-chain "spot" balances are junk (billions of dust tokens).
  Keep an `IGNORE_ADDRS` set in the collector, delete it from state, and remap the zero address to a
  named `jembatan`/bridge node in the view so inflow/outflow still shows.
- **`/healthz` must never build the payload, and must not take the build lock.** In the Zemiz Chain
  board the probe called `payload()`, which rebuilt an 8.7 MB / 7 s payload on a cold cache while
  holding `_lock`; the keeper's `curl -m 5` timed out, killed a healthy server, the restart reset the
  cache, and the loop ran 3,500+ times (visible as a log full of "server jalan di :PORT"). Liveness =
  read two globals and answer in microseconds; data builds belong on `/api/*` or a refresh thread.
- **A TTL cache that rebuilds on the request path stalls every first hit.** A 60 s cache means the
  first request after idle pays the whole build (5 s through a quick tunnel vs 0,3 s warm), which the
  user reports as "lambat/rusak", not as "cold cache". Serve the stale payload and rebuild behind it;
  take the lock only to read the cache and set a `_building` flag, never while `build()` runs:

```python
with _lock:
    d = _cache
    fresh = d is not None and time.time() - _cache_at < 60
    kick = (not fresh) and (not _building)
    if kick:
        _building = True
if fresh:
    return d
if d is not None:
    if kick:
        threading.Thread(target=_rebuild, daemon=True).start()
    return d          # stale now, refreshed seconds later
_rebuild()            # cold start only, when no payload exists yet
return _cache
```

  `_rebuild()` assigns `_cache` / `_cache_at` and clears `_building` in a `finally`, so a failed build
  cannot wedge the flag and leave every request waiting on a cache that never arrives.
- **Unbounded edge logs turn a graph page into a timeout.** 1.05M raw transfer rows made `/api/chain`
  never answer (>2 min) and the JSON 226 MB, because (a) `any(a == e["dst"] for e in edges)` inside a
  per-node comprehension is O(nodes x edges) — precompute `dst_seen = {e["dst"] for e in edges}` — and
  (b) the page aggregates by `src>dst` anyway. Aggregate server-side into one row per pair (`usd` sum,
  `n` count), keep the raw total for the headline stat: 226 MB → 5 MB, 869 KB gzipped, 145 ms.
- **A dedupe function that is never called is not a dedupe.** `insider_chain_build.py` had `prune()`
  and `--prune`, but the refresh path only appended, so 54% of the JSONL was duplicate rows and the
  file grew every 6 h. Call `prune()` at the end of the refresh run (it rewrites the file, ~17 s for
  420 MB → 191 MB) and verify with `wc -l` plus a unique-key count.
- **A silent refresh job hides its own failures.** `no_agent` + empty stdout = no message, so a
  crashed data-builder looks identical to a quiet tick. Capture the child's exit code in the `.sh`
  wrapper and print one line on non-zero — with `deliver=local` for data jobs, so the error lands in
  the local cron output instead of spamming the chat.
- **A service worker registered by ONE page can hijack EVERY page on the origin.** A risk dashboard's
  SW matched `req.mode === 'navigate'` (all navigations) and cached every fetched HTML under the key
  `/risk`; opening the tracker at `/` then showed the cached RISK page, and `/risk`'s cache got
  overwritten with the tracker's HTML. The symptom the user reports is "error / blank" that you CANNOT
  reproduce with curl (server returns 200 every time) because it only happens in the browser holding
  the SW. FIX: scope the fetch handler to the SW's own paths (`if (!RISK_PATHS.includes(pathname)) return;`),
  cache under the requested path, bump the cache name so the old cache is dropped on activate, and serve
  the SW with a short `Cache-Control` (max-age=300) so phones pick the fix up fast. Prove it with the
  offline trick: `ctx.set_offline(True)` then navigate to the OTHER page — with the bug it serves the
  wrong cached page, with the fix it fails normally.
- **Cross-link every page of a multi-page app.** The tracker had no visible link to `/risk` and the risk
  page none back — on a phone that reads as "the link doesn't exist". Add the counterpart link in both
  headers and click-test the round trip.
- **Dict-valued API fields print as `[object Object]`.** If the payload returns `age`/`ttl` as a
  per-section dict, format it (`Object.entries(age).map(([k,v])=>k+' '+Math.round(v)+'s').join(' · ')`)
  instead of concatenating it into a string.
- **Layout: phone cards, desktop 2 columns.** A horizontal table scroller is the #1 mobile breakage —
  render each row as a card (date + total on line 1, per-item chips below). Wrap cards in a `.cards`
  container and switch to `grid-template-columns:1fr 1fr` at `min-width:900px` with the hero card
  `grid-column:1/-1`; a 760px-max single column on a 1280px screen reads as unpolished. Cap chip lists
  (top 6 by absolute value + a `lainnya` residual) so a busy day doesn't wrap to three lines.
- **Label/value pairs must not split across lines on mobile** — wrap each pair in a `white-space:nowrap`
  span, or the label ends one line and its number starts the next.
- **Read the page from disk per request.** Serve the HTML with `open(path).read()` inside `do_GET` (not
  a module-level constant) so you can iterate on the UI without restarting the server each time.
- **The keeper silently stops working after its first restart — flock fd inheritance.** If step 0 does
  `exec 9>lock; flock -n 9` and then launches the server/tunnel with `setsid nohup … &`, the children
  **inherit fd 9** and hold the lock for their whole lifetime. Every later run exits at
  `flock -n 9 || exit 0`, so the keeper can never restart anything again — and never announces a URL
  change (the run that would print it exits first). Symptom: the URL file is stale, the user's saved
  link 404s, and the cron output files all say "silent (empty output)". Diagnose with
  `fuser -v <lockfile>` — if the *server*/*tunnel* PIDs show up, this is it. Fix: close the fd for the
  children — `… >>"$LOG" 2>&1 </dev/null 9>&- &` on both launches (clearing it needs one restart of
  those children, which rotates a quick-tunnel URL). Verify after: `fuser -v <lockfile>` empty, then
  run the keeper twice → second run must be silent.
- **Two keepers sharing one seen-file = the user never gets the new URL.** If a `@reboot`/system
  crontab entry runs the same script with stdout appended to a *log*, it consumes the URL-change and
  writes the seen-file; the Hermes cron run (the one with `deliver=origin`) then sees nothing new and
  stays silent. Give the log-only caller its own watermark via an env override
  (`WHALE_BOARD_SEEN_FILE=…seen.sys.txt`, i.e. make `SEEN_FILE="${VAR:-default}"` in the script) so
  the Telegram-facing keeper stays the one that announces.
- **`pkill -f <script>.py` from an agent terminal call kills your own shell** — the pattern matches
  the shell's own command line (exit `-15`, no output). The bracket trick (`pkill -f "[w]hale_.."`)
  only protects you when that literal text appears NOWHERE else in the command you send: inside a
  heredoc or `python -c` payload that mentions the path (`trade/server.py`), the regex matches your own
  shell and kills the very server you were restarting. The same trap applies to daemons matched by full
  command line (`pkill -f "cloudflared tunnel --url http://localhost:8787"` kills the shell that runs
  it). Safest: keep the pkill inside the keeper script
  file and run it as a script, or resolve the PID from the port and kill that:
  `PID=$(ss -ltnpH "sport = :8790" | grep -oP 'pid=\K[0-9]+' | head -1); kill "$PID"` — the command
  line then never contains the daemon's name at all. Confirm with `pgrep -af "[w]..."`.
- **A live tunnel process can serve a dead URL.** Process-existence keepers report healthy while the
  quick tunnel is stuck reconnecting: `pgrep` matches, the URL file is stale, and every `curl` to the
  old host fails. Diagnose from the tunnel log's tail (`ERR failed to serve tunnel connection`,
  `Retrying connection in up to 1m4s`) and from a real request to the public URL — not from `ps`.
  Kill by PID (`pgrep -af cloudflared` → `kill <pid>`) and rerun the keeper; the URL changes, so hand
  the new one over in the same reply.
- **Keeper logging into `data/` fails before the server can create that dir.** `nohup python3 app.py
  > data/server.log` applies the redirect in the *shell*, before Python runs its `mkdir`, so a fresh
  app dies with exit 1 and an empty log while `app.py` itself is fine. `mkdir -p data` in the keeper
  (and before any manual first run) — and check `ls data/` before debugging the server.
- **Long inline shell payloads get hardline-blocked** (parser limit, saved to
  `~/.hermes/cache/blocked-scripts/`). Split into small calls or write a `.sh` file and run that.
- **`patch` in V4A mode can append a duplicated line instead of replacing it** when the context guess
  is loose, and the file then fails with `IndentationError`. Always read back (`read_file` around the
  region) or rely on the tool's own lint result, then fix with `mode=replace` on a unique anchor.
- **Dense snapshots eat the chart window.** A monitor that appends a history row every 15 min fills a
  240-point sparkline with ~2,5 days and pushes the rest off the left edge. Downsample ON READ, don't
  thin the writer: one point per hour, latest per hour —
  `SELECT ts,v FROM t WHERE ts IN (SELECT MAX(ts) FROM t GROUP BY substr(ts,1,13)) ORDER BY ts DESC LIMIT 240`,
  then reverse in Python. Raw rows stay intact.
- **Don't re-verify by grepping the served HTML alone** — the header may render only after JS runs.
  Check the JSON API, then the render harness. Cheap first pass: drive the browser CLI at the tunnel URL
  and read the rendered fields (`document.getElementById('eq').textContent`, the body `innerText`), plus
  a screenshot to send the user — a 200 on `/` proves nothing about JS-rendered content.
- Cache the upstream in memory (TTL) and report in the footer which thresholds/staleness are in
  effect, plus a visible "update berikutnya dalam Ns" countdown, so the user trusts the numbers.
- Optional light gate: token in `?k=` or an `X-Board-Token` header, enabled by env var; leave OFF by
  default for convenience, and say plainly that anyone with the link can view it (public on-chain data
  only — never put the user's own positions/secrets behind a bare quick-tunnel URL).
- Stable URL options to offer when the user wants a permanent name: Cloudflare **named tunnel + own
  domain** (free, needs their CF login), or a `<name>.vercel.app` static page (needs a Vercel token —
  check `~/.vercel` and `.env` first and report what's missing rather than assuming).

## Agent profile panel

When the ask is a screenshot of an agent profile screen (Model / Skills / Integrations / Work), build a
read-only panel over local Hermes state — never expose `hermes dashboard` through a bare tunnel. Data
sources, the `gateway_state.json` / `gateway.pid` traps and the token-gate details are in
`references/theming-to-reference-ui.md` §6.

### Getting the link to actually open on his phone

- **Put the secret in the PATH, not the query** (`/p/<token>`), and accept the same value as a cookie
  (`ap=<token>`) so follow-up requests stay authorised. Query strings get dropped or mangled by in-app
  browsers; when he says "ga bs buka" while your `curl` returns 200, this is the first thing to change.
- **The page's `fetch` must resolve the token from the pathname**
  (`location.pathname.match(/^\/p\/([^/]+)/)`, falling back to `location.search`). A relative
  `fetch('api?k=…')` issued from `/p/<token>` resolves to `/p/api`, which fails the check — the page
  renders with numbers once and then silently stops refreshing, which reads as "stuck".
- **Keep a second tunnel provider ready for exactly this complaint.** `ssh -R 80:localhost:<port>
  nokey@localhost.run` prints `https://<id>.lhr.life` with no account and no setup. Hand over both
  links, then ask which failure he saw — blank page, `403`, or "site can't be reached" have three
  different causes (JS/browser, truncated link, ISP blocking the tunnel domain) and guessing wastes a
  round trip.

## References


- Multi-agent chat UI ("kantor") for several persona bots: see the `agent-chat-office` skill — it reuses
  this skill's server/tunnel/keeper pattern and adds per-persona dispatch plus a token gate.
- `references/localhost-dashboard-serving.md` — worked example (ZemizTracker: paths, ports, cron IDs,
  the node render harness, verification transcript, branding diff) and the failure transcript of the
  pitfalls above.
- `scripts/mobile_probe.py` — real-browser (playwright/chromium) mobile + desktop layout probe:
  overflow offenders, row heights, tabs/header height, phone screenshots for `vision_analyze`.
- `scripts/mobile_probe_row.py` — per-`td` / per-chip measurement of one row; catches the wrapped-chip
  case that makes mobile cards too tall.
- `templates/localhost_dashboard_server.py` — stdlib ThreadingHTTPServer + TTL cache + history +
  optional token, ready to copy and re-point at any data source.
- `templates/service_keeper.sh` — idempotent keeper: healthz, pgrep, tunnel URL parse, print-on-change.
