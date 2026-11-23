# Worked example — ZemizTracker (whale dashboard), 5 Okt 2026

Context: the Whale Board CLI (`whale_scan.py`, see `third-party-monitor-cloning`) had just been
written; the user asked *"gas coba bikinin webnya, atau local host yg bisa gw akses kyk gitu"*, then
sent the single word **"zemiztracker"** — i.e. name the product that, and give me a phone-accessible
page. Both asks were delivered and verified in one pass.

## Files that ended up live

| Piece | Path | Notes |
|---|---|---|
| Data CLI (already existed) | `~/.hermes/scripts/whale_scan.py` | `--full`, `--json`, default = delta |
| Server | `~/.hermes/scripts/whale_board_server.py` | stdlib `ThreadingHTTPServer`, `127.0.0.1:8787`, TTL 60 s, `/`, `/zemiztracker`, `/api/board`, `/api/refresh`, `/healthz`, optional `WHALE_BOARD_TOKEN` (`?k=` or `X-Board-Token`) |
| Page | `~/.hermes/scripts/whale_board.html` | 14.4 KB, inline CSS/JS, no CDN, brand + inline-SVG 🐋 favicon, `theme-color`, `apple-mobile-web-app-*` |
| History | `~/.hermes/data/whale_scan_history.jsonl` | one line per refresh (bias/long/short/total), capped 576 lines → sparkline |
| State / URL | `~/.hermes/data/whale_scan_state.json`, `whale_board_url.txt`, `whale_board_url_seen.txt` | thin-state for delta alerts and the URL-change notification |
| Keeper | `~/.hermes/scripts/whale_board_up.sh` | healthz → restart server; pgrep → restart tunnel; parse URL; print only on change |
| Cron (data) | `bc64d795e52c` — `ZemizTracker — whale delta 15m (DM)` | `no_agent`, `script=whale_scan.py`, `deliver=origin` |
| Cron (keeper) | `626ece9e24fa` — `ZemizTracker web watchdog (server+tunnel, kirim URL kalau ganti)` | `no_agent`, `script=whale_board_up.sh`, `*/10 * * * *` |

Tunnel: `cloudflared tunnel --url http://localhost:8787 --no-autoupdate` (second quick tunnel on this
host; the Lynk webhook one on :8645 runs independently). URL that session:
`https://ridge-denied-deutsche-viewpicture.trycloudflare.com`.

## Verification actually run (copy these shapes)

```bash
# local routes
for p in / /zemiztracker /api/board /healthz; do
  echo "$p -> $(curl -s -m 15 -o /dev/null -w '%{http_code}' http://127.0.0.1:8787$p)"; done
# public routes + brand assert
URL=$(cat ~/.hermes/data/whale_board_url.txt)
curl -s -m 25 -o /tmp/pub.html -w 'publik -> %{http_code} %{size_download}b\n' "$URL/zemiztracker"
grep -o '<title>[^<]*</title>' /tmp/pub.html      # -> ZemizTracker · Whale Hyperliquid
```

Observed: `/, /zemiztracker, /api/board, /healthz` all 200 locally; public `/zemiztracker` 200 with
14422 bytes; `/api/board` payload 30 KB carrying 54 wallet rows and 61 coins.

## Headless render harness (node) — proves the page, not just the HTML

```js
const fs=require("fs");
const html=fs.readFileSync("whale_board.html","utf8");
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const data=JSON.parse(fs.readFileSync("board_api.json","utf8"));   // saved from /api/board
const ids=[...html.matchAll(/id="([A-Za-z0-9_]+)"/g)].map(m=>m[1]);
const el=()=>({textContent:"",innerHTML:"",className:"",style:{},classList:{toggle(){},add(){},remove(){}}});
const nodes={}; ids.forEach(i=>nodes[i]=el());
global.document={getElementById:id=>nodes[id]||(nodes[id]=el()), querySelector:()=>el()};
ids.forEach(i=>{ global[i]=nodes[i]; });        // gotcha 1: browsers expose ids as globals; the stub must too
global.setInterval=()=>0;                        // kill the countdown timer
global.fetch=async()=>({json:async()=>data});
eval(js);                                        // gotcha 2: do NOT replace setTimeout with an immediate
setTimeout(()=>{                                 // call — load() is async and resolves in a microtask, so an
  console.log(nodes.bias.textContent, nodes.notional.textContent,   // instant probe sees empty fields
              (nodes.coins.innerHTML.match(/<tr/g)||[]).length);
  exp("ETH");                                    // exercise a click handler too
}, 400);
```

Result that validated the page: `55.1% long` · `$2.25B` · `54/54` wallets · 61 coin rows · clicking a
coin injected 1 detail row · wallet tab 54 rows / 184 position chips · footer leaked the configured
thresholds. A first attempt returned all-empty fields precisely because the probe was wired to an
immediate `setTimeout` stub — the fields were fine.

## Failure transcript / pitfalls hit for real

- `pkill -f whale_board_server.py` typed as an agent terminal command → the shell running that very
  command matched the pattern and got SIGTERM (`exit_code: -15`, no output). Fix: `pkill -f
  "[w]hale_board_server"` or keep the kill inside the keeper script (whose own cmdline doesn't
  contain the script name).
- One long chained verification one-liner was rejected by the hardline parser
  ("oversized/unparseable inline command payload", saved under
  `~/.hermes/cache/blocked-scripts/`). Fix: split into small calls, or write the checks into a `.sh`.
- `patch(mode=patch)` with a loose context hint appended a duplicate line, producing `IndentationError`
  and a stray `<footer>` after `</html>`. The tool's own lint caught both; fixed with `mode=replace`
  on a unique anchor. Read back structured regions after multi-line patches.
- `systemctl --user list-units` → "Failed to connect to bus: No medium found" (gateway is a system
  service) → the keeper script + cron is the supervisor here; do not attempt user units.
- The page must never be trusted as a view of the user's own positions: it exposes public on-chain
  wallet data only. Keep the user's portfolio/secrets out of a bare quick-tunnel URL.

## Branding diff applied for "zemiztracker"

`<title>ZemizTracker · Whale Hyperliquid</title>`, `<h1>🐋 ZEMIZTRACKER</h1>`, badge
`whale board · hyperliquid`, inline data-URI SVG favicon, `theme-color`, `apple-mobile-web-app-title`,
brand in the JS-rendered footer, route alias `/zemiztracker`, and the two cron jobs renamed to the
brand. Verification after the rename: `/zemiztracker` 200 locally *and* through the tunnel, title
asserted, render harness re-run.

## Stable-URL findings (report honestly, don't guess)

- `zemiztracker.vercel.app` → HTTP 404 while the user's existing `zemizdigital.vercel.app` → 200, so
  the subdomain looks free — but deploying needs a Vercel token; `.env` had none and `~/.vercel` was
  absent, so this was reported as "needs your token", not attempted.
- RDAP (`https://rdap.org/domain/<d>`) returned 404 for `zemiztracker.com/.xyz/.id` (hint: unregistered)
  but DNS lookups returned nothing even for `zemizdigital.com`, which does exist ⇒ **the RDAP/DNS
  evidence from this host is not sufficient to assert availability**. Say "indikasi belum terdaftar,
  belum bisa gw pastiin" instead of "domainnya kosong, beli aja".
- Permanent options to offer: Cloudflare named tunnel + own domain (free, needs the user's CF login),
  or a Vercel subdomain (needs token). Quick tunnel + keeper stays the zero-setup default.
