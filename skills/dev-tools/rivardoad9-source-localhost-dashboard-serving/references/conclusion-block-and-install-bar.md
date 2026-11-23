# Computed conclusion block + install bar (the two follow-ups that always come next)

Both asks arrived in the same session as the page itself: *"kasih conclusion section, kayak sekarang
lagi pada apa"* and *"buat appsnya bs di instal dong"*. Ship both with the page instead of waiting for
the follow-up.

## The conclusion block ("lagi ngapain")

The page already shows the data; what the user asks for is the **read**. Compute it server-side into
the payload (`payload["concl"]`) — no LLM call, no hand-typed numbers. Every figure is recomputed each
refresh from the same state/ledger the rest of the page reads, so it can never drift from the table
below it.

```python
{"asof": "09 Oct 07:59 WIB",
 "headline": "Lagi nambah amunisi: duit masuk $5,5jt dari 13 wallet, posisi dominan SHORT BTC $12,2jt.",
 "rows": [{"k": "Duit masuk HL 24 jam", "v": "$5,5jt dari 13 wallet",
           "note": "terbesar B0c17 $1,2jt jam 11:19 WIB"}, ...],
 "bias": {"long": 3747061, "short": 13357143, "net": -9610082},
 "spot": {"UBTC": 1500000},
 "src": {"wallet": 65, "loncatan": 1156}}
```

Reusable recipe (wallet/flow tracker):

1. **24 h inflow** — walk the deposit/bridge list, keep entries within `now - 24h`, report count +
   total + the single biggest sender with its WIB time.
2. **Side bias** — sum open perp notionals into LONG vs SHORT, count the dominant `(coin, side)` pair,
   and state the gap explicitly ("SHORT $13,4jt vs LONG $3,7jt, selisih $9,6jt").
3. **Biggest position** — label, side, coin, notional, leverage, entry, uP/L, liquidation.
4. **Spot accumulation** — only coins ≥ ~$5K (below that is dust), report total, coin count, top coin
   and how many wallets hold it.
5. **Chain + activity** — `loncat maks`, how many wallets are ≥3 hops, and the alert count in the last
   24 h from the log.
6. **Headline** — join the pieces already computed (`"Lagi " + verb + ": " + ", ".join(bits) + "."`);
   if a piece is empty, drop it instead of asserting it. `verb` can key off the inflow
   ("nambah amunisi" when money moved in, "diam" when it didn't).

Renderer: first card under the stat chips, `left-accent` border, one row per metric
(`cl-k` label / `cl-v` value / `cl-n` note), footer `dihitung <asof> · dari N wallet & M loncatan`.

Formatting traps hit in practice:

- `:.4g` turned a liquidation price into `9.288e+04` → use `{v:,.6g}` (or `{v:,.2f}`).
- A `%H:%M`-only timestamp for *yesterday's* deposit reads as a future time → print `%d %b %H:%M` when
  the timestamp is not from today (`when.date() == now.date()`).
- Bare numbers read as typos → always carry the unit/plural ("13 wallet", "6 koin", "$1,9jt").
- Keep `usd_id()`-style shortening (`$5,5jt` / `$212rb`) consistent with the rest of the page so the
  card and the tables agree.

## Installability, end to end (verified)

Assets: `manifest.json` (name, short_name, `start_url: "/"`, `scope: "/"`, `display: "standalone"`,
192+512 PNG, one `purpose: "maskable"`), a root-scope service worker with a fetch handler, and icons.
Serve from the existing stdlib server (no build step):

| path | content-type | cache |
|---|---|---|
| `/manifest.json` | `application/manifest+json; charset=utf-8` | `public, max-age=600` |
| `/sw.js` | `application/javascript; charset=utf-8` | `public, max-age=300` |
| `/icon-*.png`, `/apple-touch-icon.png` | `image/png` | `public, max-age=86400` |

Read binaries with `"rb"` (serving a PNG through the text path yields a broken image). Route these
BEFORE the generic `/api/*` branch. Two `<meta>` families are needed: `mobile-web-app-capable` +
`apple-mobile-web-app-*` + `<link rel="apple-touch-icon">`.

Install bar JS (Android fires `beforeinstallprompt`, iOS never does):

```js
let deferredInst = null;
const standalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
function showInst(txt, btn){
  if (standalone || localStorage.getItem("zc_inst_off")) return;   // installed or dismissed
  $("insttxt").innerHTML = txt; $("instbtn").textContent = btn; $("instbar").hidden = false;
}
addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferredInst = e;
  showInst("Bisa dipasang sebagai <b>app</b> di HP ini.", "Pasang"); });
$("instbtn").onclick = async () => {
  if (deferredInst) { deferredInst.prompt(); await deferredInst.userChoice; deferredInst = null; return; }
  alert(isIOS ? 'iPhone: Share → "Add to Home Screen"' : 'Chrome: menu → "Install app"');
};
$("instx").onclick = () => { $("instbar").hidden = true; localStorage.setItem("zc_inst_off", "1"); };
if (isIOS && !standalone) setTimeout(() => showInst("iPhone: ketuk <b>Share</b> lalu <b>Add to Home Screen</b>.", "ngerti"), 2500);
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
```

Cache rules for the SW: navigation network-first but cached **under the requested URL** (`put(req,c)` /
`match(req)`) so a multi-page origin can't serve page A's HTML for page B; `/api/*` network-only; static
assets cache-first. Bump the cache name when the shell changes.

Verification that actually proves installability (playwright + chromium, phone viewport, over the
public tunnel — not localhost):

```python
cdp = ctx.new_cdp_session(pg)
man = cdp.send("Page.getAppManifest")        # errors == [] is the gate, NOT the 200
sw  = pg.evaluate("""async()=>{const r=await navigator.serviceWorker.getRegistration();
     return r?{scope:r.scope,active:!!r.active,state:(r.active||{}).state}:null}""")
```

Pass = `manifest.errors == []`, `sw.active == True`, `state == "activated"`, zero `pageerror`s, plus
`curl -w '%{content_type}'` on the four asset paths through the tunnel (`application/manifest+json`,
`application/javascript`, `image/png`).

## Pitfalls

- **Icon generator: `str.format()` eats CSS braces.** An SVG held in a Python string rendered via
  `.format(S=…, R=…)` needs every literal brace doubled (`html,body{{margin:0;padding:0}}`) or it dies
  with `KeyError: 'margin'`.
- **Killing the server before restarting it.** `pkill -f board_server.py` matches the agent's own shell
  command line (also when only the *launch* half of the command names the file) → exit `-15`, no output,
  and sometimes the server dies while your restart never runs. Kill the listener by PID instead:
  `PID=$(ss -ltnp | grep ':8790' | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2); [ -n "$PID" ] && kill "$PID"`.
- **A route-serving stdlib handler should bind `127.0.0.1`**, with the quick tunnel as the only public
  path — check this when adding new asset routes to an older server that was written with `0.0.0.0`.
