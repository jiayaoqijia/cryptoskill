# perp-cli Command Reference

All commands support `--json` for structured output. Always use `--json` when calling from an agent.

## Global Flags

`--json` (required for agents) | `-e <venue>` | `-n mainnet|testnet` | `--dry-run` (only commands whose `--help` says "supports --dry-run"; others refuse with `INVALID_PARAMS`) | `--fields <f1,f2>` | `--ndjson` | `-w, --wallet <name>` | `--ows <name>` (OWS wallet) | `--no-agent` (skip agent-key routing) | `--no-builder` | `--dex <name>` (HIP-3, Hyperliquid)

Venues (`-e`, id | aliases): `pacifica|pac`, `hyperliquid|hl`, `lighter|lt`, `lighter-rh|lrh|rh`, `aster|ast`, `ondo|ondo-perps`, `arcus`, `qfex|qf`, `risex|rise` (READ-ONLY in this release — market data + account reads; trading is planned for a later release, every trade / agent / bot write refuses with CAPABILITY_UNSUPPORTED), `txflow|txf` (market data only, UNOFFICIAL API — every write refuses with CAPABILITY_UNSUPPORTED), `variational|var|omni` (market data only, official API, RFQ venue: `market book` = indicative RFQ quotes, `market funding` = current terms — every write refuses with CAPABILITY_UNSUPPORTED), `grvt|grv` (market data only in this version, official API — every write refuses with CAPABILITY_UNSUPPORTED), `extended|ext|x10` (Extended on Starknet, official API, market data only in this version — every write refuses with CAPABILITY_UNSUPPORTED). Default = `settings.defaultExchange`, else `pacifica` — always pass `-e`.
`-k <key>` is rejected (keys only via stdin / OWS vault). `--passphrase` is deprecated → `OWS_PASSPHRASE` env or stdin.

## Market Data (read-only, safe)
```bash
perp --json -e <EX> market list                # all markets with prices, funding, volume
perp --json market prices                      # cross-exchange price comparison
perp --json -e <EX> market mid <SYMBOL>        # mid price (fast)
perp --json -e <EX> market info <SYMBOL>       # mark/index price, funding, volume, OI, max leverage
perp --json -e <EX> market book <SYMBOL>       # orderbook (bids/asks)
perp --json -e <EX> market trades <SYMBOL>     # recent trades
perp --json -e <EX> market funding <SYMBOL>    # funding rate history
perp --json -e <EX> market kline <SYM> <INT>   # OHLCV candles (1m,5m,15m,1h,4h,1d)
perp --json -e hyperliquid market hip3         # list HIP-3 deployed perp dexes (needs -e hyperliquid; other -e → INVALID_PARAMS)
perp --json -e hyperliquid --dex <DEX> market list           # one HIP-3 dex's markets (e.g. --dex xyz)
perp --json -e hyperliquid --dex <DEX> market book <SYMBOL>  # any market/account/trade command takes --dex the same way
```

Hyperliquid read-path notes:
- **Venue caps that cannot be paged are refused** (`INVALID_PARAMS` naming the cap; never fewer rows than asked, silently). `trades`: the venue serves only the last 10 trades — the default `--limit` is min(20, 10) = 10, an explicit `--limit` above 10 is refused. `book`: at most 20 levels per side — `-d` above 20 is refused (`-d` cuts JSON too). `kline`: only the most recent 5000 candles per interval exist — a `--start` before now − 5000 × interval is refused before any request, naming the earliest allowed start. `backtest grid --days N` clamps its start to that window and reports `dataFrom` / `truncated`.
- **kline intervals:** `1m,3m,5m,15m,30m,1h,2h,4h,8h,12h,1d,3d,1w,1M` (anything else → `INVALID_PARAMS`, not retryable). `1M` candles are **30-day buckets**, not calendar months; `1w` candles open **Thursday 00:00 UTC**. Each candle carries `closed` (false on the in-progress last candle).
- **funding:** `--limit N` = the last N hourly settlements (paged over the venue's 500-row cap; max 5000).
- **Delisted markets** (meta `isDelisted`, e.g. `MATIC`, every asset of `--dex km`) → `SYMBOL_NOT_FOUND` with `details.reason: "delisted"` on `info` / `trades` / `funding` / `book` / `kline`; orders / positions / history still resolve them. `market hip3` lists live assets only (`assets`), plus `delistedAssets` and `delisted: true` for a dex with no live asset; `deployer` comes from `perpDexs`.
- **Symbol naming:** `market list` / `info` rows use the plain coin `BTC` (HIP-3: `xyz:XYZ100`; the wire coin is in `venueSymbol`), as `market trades` rows and the WS codec. `-PERP` arguments still resolve. Keyed `account positions` rows still show `BTC-PERP`; strip `-PERP` to compare.
- **marginTiers:** a market on a single-tier table (`marginTableId` < 50) reports `[{ lowerBound: 0, maxLeverage: <id> }]` (docs "Margin tiers"), not null.

## Account (read-only, safe)
```bash
perp --json portfolio -e <VENUE_ID>            # perp balance + spot holdings + 24h funding; venue id or alias (hl, lt, …)
perp --json -e <EX> account positions          # open positions
perp --json -e <EX> account positions --address <ADDR>   # ANY account's open positions, keyless (public data; nothing signed)
perp --json account positions --address <0xADDR>         # every supporting venue: { venues, errors?, notes? }
perp --json -e <EX> account orders             # open/pending orders
perp --json -e <EX> account history            # order history
perp --json -e <EX> account trades             # trade fill history
perp --json -e <EX> account funding-history    # funding payments
perp --json -e <EX> account settings           # per-market leverage & margin mode
perp --json -e <EX> account margin <SYMBOL>    # position margin info
perp --json -e <EX> account pnl                # realized + unrealized + funding
perp --json -e <EX> account twap-orders        # active TWAP orders
perp --json portfolio                          # cross-exchange unified view
# funding24h is null (with fundingError) when a venue's funding history is unreadable; totals.fundingIncomplete = true then
# --address (public-address positions): hyperliquid / lighter / lighter-rh / risex take a 0x address, pacifica a base58
#   Solana address (a wrong format → INVALID_PARAMS before any request); other venues → CAPABILITY_UNSUPPORTED
#   (feature publicPositions). Rows = the account positions rows with plain symbols, plus:
#   hyperliquid: native + EVERY HIP-3 dex (one read each), `dex: null | "<dex>"`; a dex that fails is in
#     meta.errors["hip3:<dex>"] + meta.warnings — its rows are missing, the others are kept (exit 0).
#   lighter / lighter-rh: every account (sub-account) of the address, `accountIndex` on each row; zero-size rows
#     dropped; --account-index <n> narrows (not an account of the address → INVALID_PARAMS). No account → [] + meta.notes.
#   --symbol <SYM> filters (GOLD matches xyz:GOLD). meta: { address, source: "public" }. MCP: get_positions_by_address.
perp --json portfolio --arb                    # full dashboard with arb top 5
```

## Trading (requires user confirmation)
```bash
# Market orders
perp --json -e <EX> trade market <SYMBOL> <buy|sell> <SIZE>
perp --json -e <EX> trade buy <SYMBOL> <SIZE>           # shorthand market buy
perp --json -e <EX> trade sell <SYMBOL> <SIZE>          # shorthand market sell
perp --json -e <EX> trade buy <SYM> <SIZE> --smart      # IOC limit at best ask + 1 tick — pacifica/hyperliquid/lighter/aster only; not with --tp/--sl or a client id
perp --json -e <EX> trade buy <SYM> <SIZE> --client-id <id>   # reused id → ok:true, data.duplicate:true (local ~/.perp/client-ids.jsonl; nothing sent)
#   id formats: pacifica full UUID; hyperliquid 0x+32 hex; lighter(-rh) integer; qfex refuses --client-id (use --auto-id)
# Opening orders: --force bypasses the local risk limits (user consent only; never quarantine)

# Split execution (orderbook-aware, for large orders)
perp --json -e <EX> trade split <SYMBOL> <buy|sell> <USD>
perp --json -e <EX> trade split <SYM> buy 5000 --max-slippage 0.5 --max-slices 5 --delay 2000 --min-slice 200
perp --json -e <EX> trade market <SYM> buy <SIZE> --split   # split via flag

# Limit / stop / TPSL
perp --json -e <EX> trade limit <SYMBOL> <buy|sell> <PRICE> <SIZE> [--tif GTC|IOC|FOK|ALO]   # default GTC on every venue; off-grid price → INVALID_TICK (never rounded)
perp --json -e <EX> trade stop <SYMBOL> <SIDE> <SIZE> <STOP_PRICE>   # reduce-only by default; --no-reduce-only to open (refused on ondo / qfex)
perp --json -e <EX> trade tpsl <SYMBOL> <long|short> --tp <P> --sl <P>   # positionSide = the open position's side
perp --json -e <EX> trade buy <SYMBOL> <SIZE> --tp <P> --sl <P>         # entry protected by TP/SL (verified fill)

# Order management
perp --json -e <EX> trade edit <SYMBOL> <ORDER_ID> <PRICE> <SIZE>
perp --json -e <EX> trade cancel <SYMBOL_OR_ORDER_ID> [orderId]
perp --json -e <EX> trade cancel-all
perp --json -e <EX> trade cancel-stop <SYMBOL> <STOP_ORDER_ID>   # pacifica / qfex only; other venues: trade cancel
perp --json -e <EX> trade cancel-twap <SYMBOL> <TWAP_ORDER_ID>
perp --json -e <EX> trade status <ORDER_ID|c:<CLIENT_ID>> [--symbol <SYM>]
#   --symbol required on ondo / arcus / qfex, and for c:<id> on lighter / lighter-rh / aster
perp --json -e <EX> trade fills [SYMBOL]                # recent fills

# Pre-flight validation
perp --json -e <EX> trade check <SYMBOL> <SIDE> <SIZE>
perp --json -e <EX> trade check <SYM> <SIDE> <SIZE> --leverage 3
# NOTE: trade check does NOT read exchange-set leverage. Always pass --leverage explicitly.

# Position management
perp --json -e <EX> trade close <SYMBOL>                # close single position
perp --json -e <EX> trade close-all                     # close all positions
perp --json -e <EX> trade flatten                       # cancel all orders + close all positions
perp --json -e <EX> trade reduce <SYMBOL> <PCT>         # reduce by percentage
perp --json -e <EX> trade leverage <SYMBOL> <N> [--isolated]

# Advanced orders
perp --json -e <EX> trade scale-tp <SYMBOL> --levels '<P1>:<PCT>,<P2>:<PCT>'
perp --json -e <EX> trade scale-in <SYMBOL> <SIDE> --levels '<P1>:<PCT>,<P2>:<PCT>' (--size-usd <USD> | --size <BASE>)   # percents sum to 100
perp --json -e <EX> trade pnl-track                     # real-time PnL tracker
perp --json -e <EX> trade twap <SYMBOL> <SIDE> <SIZE> <DURATION>   # Pacifica: seconds (native), HL: minutes (native, min $100); others client-side: --background [--slices <n>]

# Pacifica Atomic basket (pacifica only; other venues → CAPABILITY_UNSUPPORTED). Legs SYMBOL[:WEIGHT] (≤ 5 per side, each market once);
# --usd is split by weight at each mark, floored to the lot, each leg ≥ the market's USD minimum. ONE POST /orders/batch of market
# orders — NOT all-or-nothing: each leg fills or fails on its own (ORDER_PARTIAL / ORDER_REJECTED / ORDER_PENDING per basket).
# --reduce-only: --long legs must close shorts, --short legs must close longs (checked before sending). Supports --dry-run (plan + unsigned body).
perp --json -e pacifica trade atomic --long BTC:50 --short ETH:50 --usd 1000 [--reduce-only] [--slippage-bps <n>] [--force]
# A leg needs notional ≥ the market minimum × (1 + slippage bound). Legs without an order_id in the ack are traced by their client_order_id.
# A batch failure other than HTTP 400 / 429 (timeout, 5xx, unreadable answer) → ORDER_PENDING and EVERY leg is quarantined.
# Pacifica Chase / OCO / Trailing Stop / Swarm / Trigger Swarm / Conditional Market|Limit: no documented API / SDK path (as of 2026-10-19) —
# nearest here: trade twap (≈ Swarm, split market execution), trade tpsl (≈ OCO bracket exit).

# Spot helpers (any venue with spot)
perp --json -e <EX> trade spot-buy <SYMBOL> <SIZE>
perp --json -e <EX> trade spot-sell <SYMBOL> <SIZE>
perp --json -e <EX> trade spot-limit <SYMBOL> <SIDE> <PRICE> <SIZE> [--tif <tif>]
perp --json -e <EX> trade spot-cancel <SYMBOL> <ORDER_ID>
perp --json -e <EX> trade spot-orders [SYMBOL]
perp --json -e <EX> trade spot-transfer <to-spot|to-perp> <AMOUNT>
perp --json -e <EX> trade spot-balance

# Multi-leg execution (legs exchange:symbol:side:size; failed legs rolled back; unconfirmed leg → quarantined; no --dry-run)
perp --json trade multi <legs...>
```

## Outcome Markets (Hyperliquid HIP-4)

Fully-collateralized binary/range contracts on Hyperliquid. Each outcome's quote token comes from `outcomeMeta.quoteToken` (`outcome list` shows it; USDC on every listed outcome as of 2026-10-12), held on Hyperliquid spot. No leverage / no liquidation. Minimum order value 10 quote tokens (price × shares ≥ 10). Sizes are whole shares.

```bash
# List active outcome markets — parses the description string into
# class / underlying / expiry / targetPrice / period and lists each side
# with mid + assetId.
perp --json outcome list

# COMBINED VIEW — all sides' books in parallel + underlying mark price
# (HL perp mid for `description.underlying`) + gap vs targetPrice + ms
# until expiry + per-side implied probability. For a binary market the
# symmetric structure means Yes BID + No ASK ≈ 1.0; this is the
# preferred entry point for agents that need a single snapshot.
perp --json outcome view <outcome> [--depth N=10]

# Orderbook for ONE side only (use `view` if you want both at once).
# <side> accepts: 0/1, Yes/No, or #<enc> / +<enc> (the encoded form
# must match the outcome arg — mismatch throws INVALID_PARAMS).
perp --json outcome book <outcome> <side> [--depth N=10]

# Holdings + open orders.
perp --json outcome positions
perp --json outcome orders

# Place orders. ALWAYS dry-run first. [usd] = notional in the quote token, or --size <shares>; sell also --all.
perp --json --dry-run outcome buy  <outcome> <side> <usd>
perp --json --dry-run outcome sell <outcome> <side> --all

# Live execution. --limit makes it GTC; without --limit it's IoC at best ask +5% (cap 1) / best bid -5%.
perp --json outcome buy  <outcome> <side> [<usd> | --size <shares>] [--limit <px>] [--tif gtc|ioc|alo]
perp --json outcome sell <outcome> <side> [<usd> | --size <shares> | --all] [--limit <px>] [--tif gtc|ioc|alo]

# Cancel a resting order.
perp --json outcome cancel <outcome> <side> <oid>
```

### Identifier model

Same outcome side can be referenced 5 ways — the CLI normalises:

| Form | Example (BTC daily Yes) |
|---|---|
| `<outcome>, <side>` integer | `1, 0` |
| `<outcome>, <side>` name | `1, yes` |
| `#<enc>` (l2Book / candle / allMids coin) | `#10` |
| `+<enc>` (spotClearinghouseState balance coin) | `+10` |
| asset id (HL `/exchange` payload) | `100000010` |

Encoding formula: `enc = 10 * outcome + side`; asset id = `100,000,000 + enc`.

### Foot-guns enforced (Rule #2)

- **Min notional:** `price * size < 10` quote tokens → `INVALID_PARAMS`. Enforced in dry-run too. A trade leaving a remainder worth < 10 warns (it cannot be sold alone — use `sell --all`); selling more than held → `SIZE_TOO_LARGE`.
- **Encoded-side mismatch:** `outcome buy 2 #10` (where `#10` decodes to outcome=1) → `INVALID_PARAMS`, never silently routes to outcome 2.
- **Insufficient quote token:** pre-checked before order send → `INSUFFICIENT_BALANCE` (hold the outcome's quote token on Hyperliquid spot).
- **Venue rejection:** HL returns HTTP 200 with `statuses[0].error` even when an order is rejected; the CLI raises `ORDER_REJECTED` (or `INSUFFICIENT_BALANCE`) so a "placed" message never masks a failure.

### Agent workflow recommendation

```
1. perp --json outcome list                       # discover markets, parse description
2. perp --json outcome view <outcome>             # full snapshot: both books +
                                                  # underlying mark + gap vs target +
                                                  # implied probabilities + time to expiry
3. perp --json --dry-run outcome buy <outcome> <side> <usd>
                                                  # validate notional, get user approval
4. perp --json outcome buy <outcome> <side> <usd> [--limit <px>] [--tif ...]
                                                  # execute (only after explicit user OK)
5. perp --json outcome positions                  # confirm fill / monitor
```

`outcome view` replaces the old multi-call pattern (separate `book` + `market mid` lookups). One round-trip returns everything an agent needs to decide direction.

Settlement at `expiryMs` is venue-side: winning side → 1 quote token per share, losing → 0. Decide before expiry whether to self-close or let the venue settle.

## Options market data (read-only, `-e derive`)

Derive (derive.xyz, formerly Lyra) options through its official public v3 API — keyless, no orders, no account. Options venues are separate from the perp venues (not in `perp health`, arb or `market`). JSON objects carry `schema: 1`; decimals are strings; unknown is `null` (empty book side → `bid`/`ask` `null`; IV the venue could not compute → `null`; 24h high/low `null` without trades).

```bash
perp --json -e derive options underlyings                     # underlyings with options (spot price)
perp --json -e derive options expiries ETH                    # active expiries: expiry (YYYY-MM-DD UTC), expiryMs, strikes, instruments
perp --json -e derive options chain ETH                       # nearest expiry (expirySelection: "nearest"), every strike
perp --json -e derive options chain ETH --expiry 2026-12-25 --strikes 10   # 10 strikes closest to ATM (forward, else index)
perp --json -e derive options quote ETH-20261225-3500-P       # one option
```

- Chain row: `{strike, call, put}`; each side is an option quote: `bid`/`ask` `{price, size}`, `mark`, `index`, `forward`, `discountFactor`, `iv {mark, bid, ask}`, `greeks {delta, gamma, theta, vega, rho}` (venue units, verbatim), `openInterest` (contracts), `stats24h {contracts, notional, premium, trades, high, low}`, `timestampMs`. Chain level: `index`, `forward` (both of the newest ticker of the expiry, not an average), `atm {strike, reference, price}`, `strikesListed`, `missingTickers`.
- Errors: unknown underlying / expiry / instrument → `SYMBOL_NOT_FOUND` (remediation names the listing command / active expiries); a perp name in `quote` → `INVALID_PARAMS`; an active option with no live ticker (activation / expiry race) → `EXCHANGE_ERROR` (retry); other Derive rejections → `EXCHANGE_ERROR`; no `-e` or a perp venue → `CAPABILITY_UNSUPPORTED`; Derive's rate limit → `RATE_LIMITED` (retryable).
- Cost: `expiries` 1 request, `chain` 2 (instruments + ONE tickers call for the expiry), `quote` 2. Derive's public budget is 5 requests/s per IP.
- `-n testnet` reads `testnet.api.derive.xyz`. MCP: `get_option_expiries`, `get_option_chain`, `get_option_quote` (`venue: "derive"`).

## Pacifica Print (`perp print`) and vaults (`perp vault`)

Pacifica-only products: these commands always use Pacifica (`-e <other venue>` → `INVALID_PARAMS`). Reads are unauthenticated GETs and never sign; `--account <address>` reads any account without a key. Every write supports `--dry-run`, which prints the exact message to sign and the body (`signature: null`), never signs and sends nothing. `--account` on a write only plans (with `--dry-run`); a live write with `--account` is refused.

**Signer rule (perp-cli, stricter than the venue):** `vault deposit` is **master-only** (like `funds withdraw pacifica`) — an agent key must never be able to move the balance into a vault someone else manages; with only an agent key on the machine it is `NO_SIGNER_AVAILABLE`. `vault withdraw` (pays only into the own account), `print deposit` and `print cancel` are signed by the active signer (the agent key when approved, else the master). `wallet manage lake deposit|withdraw` were replaced by these commands (they now refuse with a pointer); `wallet manage lake create --initial-deposit` is refused with an agent key.

**Idempotency:** every deposit / withdraw sends a fresh `idempotency_key`. After `ORDER_PENDING` never resubmit with a new key; the only safe retry is the same command with `--idempotency-key <the reported key>` (the venue answers a duplicate with HTTP 409; how long it remembers a key is unverified). `error.details.before` holds the pre-write state (Print order count / vault shares) to compare with `print positions` / `vault positions`.

### Print — strike orders that earn a premium every cycle
A Print order locks a USDC deposit (min 10) as margin at a target price: **long** = target BELOW mark, **short** = target ABOVE mark, 0.5% … 10% / 20% / 40% from mark for a 24-hour / 7-day / 30-day cycle. Leverage 1 … product max (`print games`). The premium is credited to the order at the START of each cycle. **While resting** (before a fill) it is evaluated only at the END of each cycle: it fills AT the target (size = deposit × leverage ÷ target), rolls to a new target at the same % distance, or is liquidated; max loss = deposit + premiums. **After a fill** it is an ordinary perp position in the main account — continuous mark-price liquidation, it nets with an existing position in the same market and may be cross-margined; read it with `perp -e pacifica account positions`. Product / pool deposit caps are totals across all users (the venue refuses when full). `--cycles 1…1000` caps the cycles (default: roll until cancelled). A cancel takes effect only at the end of the running cycle — funds stay locked until then (up to 30 days on BTC_1M).
```bash
perp --json -e pacifica print games                                  # products: cycle, max lev, caps, allowed target range
perp --json -e pacifica print quote BTC_24H long 100 --strike 79000 --leverage 10 [--cycles 7]
#   read-only preview: notional, size on fill, docsLiquidationPrice, maxLoss, lock; estimatedPremium is null
#   (the venue's premium preview is a signed request — never called on a read path)
perp --json -e pacifica print positions [--account <addr>]           # current orders: printing | cancelling | filled | liquidated | cancelled | completed | ended
perp --json -e pacifica print history [--account <addr>] [--limit N] [--cursor C]
perp --json -e pacifica print events <printAddress> [--limit N] [--cursor C]   # created / premium / end_requested / position_opened / liquidated
perp --json -e pacifica --dry-run print deposit BTC_24H long 100 --strike 79000 --leverage 10 --cycles 7
perp --json -e pacifica print deposit BTC_24H long 100 --strike 79000 --leverage 10 --cycles 7   # POST /game/deposit (deposit_to_game)
perp --json -e pacifica --dry-run print cancel <printAddress>         # UNOFFICIAL: POST /game/end (end_game) is not in the API docs (apiStatus: "unofficial")
perp --json -e pacifica print cancel <printAddress> --unverified-endpoint   #   live run needs the flag; only a `printing` order
```
- `docsLiquidationPrice` is the docs formula (margin fully lost) — an outer bound, not the trigger: a liquidation was observed earlier in one live case (2026-10-16, ZEC_24H short at mark 1216.84 vs formula ≈ 1269); the venue's trigger is unpublished. For a 1× long the formula gives ≤ 0: `null` = unknown, not "no liquidation". Show the user `maxLoss`.

### Vaults (API: lakes)
A vault is a Pacifica account traded by its manager; LPs get shares at NAV (lp_balance ÷ lp_shares). Min deposit 10 USDC; `deposit_cap` caps the LP balance; the manager takes `manager_profit_share` above the high-water mark. A withdrawal redeems shares into YOUR OWN trading balance (the API has no destination) only after `deposit_min_duration_ms` since your LAST deposit (each deposit restarts the lock for your whole balance), inside the withdrawal window when one is set (open while now_s mod window < duration), and from the vault's free balance (a fully deployed vault may pay partially). APY is not published (`apy: null`).
```bash
perp --json -e pacifica vault list [--account <addr>]                 # TVL, NAV/share, fee, lock-up, window, config
perp --json -e pacifica vault info <address|nickname>                 # + live equity, positions, deposit whitelist (UNOFFICIAL endpoint, advisory), window open now?
#   a nickname must match exactly ONE vault (case-insensitive) — duplicates exist live ("Pacifica Vault" / "Pacifica vault");
#   ambiguity → INVALID_PARAMS listing every candidate's address / manager / TVL. Writes: prefer the ADDRESS.
perp --json -e pacifica vault positions [--account <addr>]            # your LP (or manager) shares and value
perp --json -e pacifica --dry-run vault deposit <vault> <amount>      # POST /lake/deposit (deposit_to_lake) — MASTER-ONLY; refused when the LP NAV is zero / undefined
perp --json -e pacifica --dry-run vault withdraw <vault> <shares>|--all   # POST /lake/withdraw (withdraw_from_lake)
```
MCP (read-only): `pacifica_print_products`, `pacifica_print_quote`, `pacifica_print_positions`, `pacifica_vaults`. Print / vault writes are CLI-only.

## Funds (deposit, withdraw, transfer, bridge, rebalance)

All fund movement lives under `perp funds`.

### Exchange in/out
```bash
perp --json funds deposit pacifica <AMOUNT>
perp --json funds deposit hyperliquid <AMOUNT>
perp --json funds deposit lighter ethereum <AMOUNT>         # L1 direct (min 1 USDC)
perp --json funds deposit lighter cctp arbitrum <AMOUNT>    # CCTP (min 5 USDC)
perp --json funds deposit lighter info                      # all Lighter deposit routes
perp --json funds withdraw pacifica <AMOUNT>              # to your own Solana wallet
perp --json funds withdraw hyperliquid <AMOUNT> [--chain arbitrum|ethereum|base] [--to <allowlisted addr>]
#   CCTP (native USDC) to your wallet (default arbitrum; 0.2 USDC forwarding fee on Arbitrum).
#   --to another address only if it is on settings withdraw.hyperliquid (else POLICY_DENIED).
perp --json funds withdraw lighter <AMOUNT>                 # -e lighter: USDC → Ethereum; -e lighter-rh: USDG → Robinhood Chain
perp --json funds deposit lighter-rh <AMOUNT>               # USDG on Robinhood Chain (min 1, mainnet only)
# Ondo Perps: NO API withdrawals — `funds withdraw ondo` → CAPABILITY_UNSUPPORTED; withdraw in the Ondo web app
perp --json funds withdraw arcus <AMOUNT>                   # USDG → the account owner (min 1)
perp --json funds deposit qfex                              # prints the USDC / Arbitrum One deposit address (sends nothing)
# RISEx: deposits / withdrawals are app-only — `funds deposit|withdraw risex` → CAPABILITY_UNSUPPORTED (app.rise.trade)
# RISEx is read-only in this release (trading later): `funds faucet risex` → CAPABILITY_UNSUPPORTED too
# QFEX: withdrawals disabled in perp-cli for now — `funds withdraw qfex` → CAPABILITY_UNSUPPORTED; withdraw in the QFEX web app
perp --json -e qfex funds transfer <AMOUNT> primary --from <account-uuid>   # between your QFEX accounts
perp --json funds deposit aster <AMOUNT> [--chain bsc|arbitrum] [--asset USDT|USDC]   # vault approve + deposit (mainnet; default BNB Chain USDT)
perp --json funds withdraw aster <AMOUNT> [--chain bsc|arbitrum] [--asset USDT|USDC]   # → the account's own address (default USDT; mainnet; agent approved with --can-withdraw --ip-whitelist)
perp --json funds deposit ondo <AMOUNT> [--chain arbitrum|ethereum] [--probe <AMT>]   # USDC transfer to the account's funding address (mainnet)
perp --json funds transfer <AMOUNT> <ADDRESS>               # HL internal transfer (instant); destination must be on settings withdraw.hyperliquid
# settings withdraw.<venue> (allowlist + limits) is set ONLY by the user in an interactive terminal
# (--json / piped → POLICY_DENIED). Agents never set or change it.
perp --json funds info                                      # combined routes & limits
```

### Cross-chain bridge (multi-provider router: cctp / relay / debridge — auto-cheapest)
```bash
perp --json funds bridge chains                             # supported chains
perp --json funds bridge quote --from <CHAIN> --to <CHAIN> --amount <AMT>
perp --json funds bridge send --from <CHAIN> --to <CHAIN> --amount <AMT>
perp --json funds bridge send --from <CHAIN> --to <CHAIN> --amount <AMT> --provider cctp [--fast]
#   exactly --amount leaves the wallet; deBridge nativeFee (ETH/SOL) is shown separately;
#   Solana-origin deBridge → NO_BRIDGE_ROUTE (use --provider cctp)
# Relay swaps (chains: robinhood, arbitrum, bsc, base, solana as destination; EVM origin; OWS master signs; recipient = your own address)
perp --json --dry-run funds bridge send --from robinhood --to arbitrum --from-asset USDG --to-asset USDC --amount <AMT>   # verified quote only
perp --json funds bridge send --from robinhood --to solana --from-asset USDG --to-asset SOL --amount <AMT> --min-out <SOL>  # stable → native needs --min-out
perp --json funds bridge send --from arbitrum --to robinhood --from-asset ETH --to-asset ETH --amount <ETH>                # native gas to Robinhood Chain
perp --json funds bridge exchange --from <EX> --to <EX> --amount <AMT>   # pacifica|hyperliquid|lighter
#   wallet → wallet: bridges the master's OWN USDC between the venues' chains (pacifica → solana,
#   lighter → arbitrum); no venue withdraw/deposit. hyperliquid: --from spends HyperCore spot USDC,
#   --to credits HyperCore perps. HyperCore → Solana → NO_BRIDGE_ROUTE.
perp --json funds bridge status <ORDER_ID>
```

### Inter-exchange rebalance (withdraw → bridge; deposit is manual)
```bash
perp --json funds rebalance check                            # balances across exchanges
perp --json funds rebalance plan                             # compute optimal moves
perp --json --dry-run funds rebalance execute --auto-bridge  # status "simulated" (moves[].status "dry_run") or "balanced"
perp --json funds rebalance execute --auto-bridge            # withdraw → bridge only (NO deposit)
perp --json funds rebalance execute --withdraw-only          # only withdraw, manual rest
```
`ok:true` even if a move failed — check every `moves[].status`: `withdrawn` | `bridged` | `same_chain` | `needs_bridge` | `withdraw_failed` | `bridge_failed`. Then deposit by hand after arrival (`funds deposit <venue> <amt>`).

## Arbitrage

All scan modes are routed through `arb scan`. Legacy aliases (`arb rates`, `arb prices`, `arb dex`, `arb spot-exec`, `arb spot-close`) are removed.

```bash
# Scan (read-only, safe)
perp --json arb scan                                        # default --mode all (perp-perp + spot-perp)
perp --json arb scan --mode perp-perp --min 10              # perp-only with min annual %
perp --json arb scan --mode spot-perp --min 10              # spot+perp only
perp --json arb scan --rates                                # funding rates across exchanges
# Which rate is compared: each venue's market-row `fundingRate` (the CURRENT rate it publishes), labelled
# per row by `rateKind` — Pacifica / Lighter / Lighter RH / Arcus / RISEx "lastSettled", Hyperliquid /
# Aster / TxFlow "accruing", null = not verified. It is NOT the WS comparator's kind:"next" (predicted
# next-period rate, where a venue publishes one: Pacifica `predictedFundingRate`).
perp --json arb scan --basis [SYMBOL]                       # cross-exchange basis
perp --json arb scan --gaps                                 # cross-exchange price gaps
perp --json arb scan --hip3                                 # HIP-3 cross-dex spreads
perp --json arb scan --history [SYMBOL]                     # historical funding
perp --json arb scan --compare <SYMBOL>                     # compare a symbol across exchanges
perp --json arb scan --positions                            # position funding impact; actual24h null + fundingHistoryErrors when a venue's history is unreadable
perp --json arb scan --live --interval 60                   # continuous monitoring
perp --json arb scan --top 10 --hold-days 7 --bridge-cost 0 --size 100  # cost-aware filtering
perp --json -e extended market list                          # Extended (read-only): rows carry assetClass, venueSymbol (TSLA_24_5-USD), tickSize, minSize, tradable, fundingRateKind "accruing"
perp --json -e extended market funding BTC -l 24            # applied hourly prints: rateKind "lastSettled", intervalHours 1, annualizedPct
perp --json arb scan --rates --include-unverified           # also show QFEX, TxFlow, Variational, GRVT and Extended (unverified funding; TxFlow rows apiStatus "unofficial"; display only, never ranked)
perp --json -e qfex market funding AAPL -l 72               # hourly windows; outside the market's funding hours: rate null + marketClosed true (not a 0 rate)
# QFEX marketClosed limits: (1) a market holiday INSIDE a configured session (e.g. SAMSUNG-KRW on
# Hangul Day, a weekday) is not in market_hours, so its 0 prints as a real-looking rate "0" with
# marketClosed false; (2) US equities DO fund in the weekday overnight gap (post_market → pre_market),
# so only an exact 0 with no part of the hour in any funding session counts as closed — a real 0
# in a gap would also read as closed. Averages / APRs skip marketClosed rows only.
# netSpread / grossSpread = annualized % (netSpread = gross minus round-trip costs amortized over --hold-days)
# spot-perp rows: netSpreadPct / grossSpreadPct, spotExchanges[], perpExchange, direction

# Execute (perp-perp or spot+perp via spot:<venue>; spot venues: hl, lt, lrh, aster, ondo)
# Sequential: long first, then the short sized to the verified long fill; reconcile always on;
# an unconfirmed leg quarantines the symbol. Supports --dry-run.
perp --json arb exec <SYM> <longEx> <shortEx> <USD>         # perp-perp dual-leg entry
perp --json arb exec <SYM> spot:hl hl <USD>                 # spot+perp via HL spot
perp --json arb exec <SYM> spot:lt pac <USD>                # spot+perp via LT spot
perp --json arb exec <SYM> <longEx> <shortEx> <USD> \
   --leverage 2 --isolated --smart --max-slippage 0.5

# Close
perp --json arb close <SYM>                                  # close perp-perp arb
perp --json arb close <SYM> --pair <longEx>:<shortEx>       # disambiguate by pair
perp --json arb close <SYM> --spot-exch hl --perp-exch hl   # close spot+perp legs
perp --json arb close <SYM> --smart                         # IOC limits at best price
perp --json arb close <SYM> --force                         # quarantined symbol — only after the user checked positions
perp --json arb close <SYM> --state-only --yes              # drop a stale state entry (no order sent)

# Status / history / config / rebalance
perp --json arb status                                      # open arb positions + PnL + funding; check unconfirmedPairs, staleStateEntries
# spot-perp entries: fundingSource actual | partial | estimate | recorded (+ fundingError) — only "actual" is complete settled funding
perp --json arb status --period 7 --symbol BTC              # filter funding lookback / symbol
perp --json arb history                                     # alias: arb log
perp --json arb history --period 30                         # past arb trade performance
perp --json arb config                                      # show arb defaults
perp --json arb rebalance --check                           # cross-exchange balance distribution (read-only)
perp --json arb rebalance --target 50:50 --amount 1000      # plan only; execute with funds rebalance execute

# Auto-execute daemon
perp --json arb auto --min-spread 30 --close-spread 5 --size 100 --max-positions 5
perp --json arb auto --background                           # tmux session
perp --json arb auto --hip3 --min-oi 50000 --min-grade C    # HIP-3 mode
perp --json --dry-run arb auto                              # simulate (--background inherits it)
```

## Wallet Management
```bash
perp --json wallet generate evm                # generate EVM wallet
perp --json wallet generate solana             # generate Solana wallet
printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp --json wallet import --name <n> [--chain evm|solana|dual] [--mnemonic]   # import a key (stdin / hidden prompt; argv key, --evm/--solana <key>, --legacy rejected)
printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set hl   # import key (stdin / hidden prompt; argv key rejected) into OWS vault → active wallet
perp --json wallet set pac --name pac          # Solana key, hidden prompt (TTY)
perp --json wallet set hl --default            # also make hyperliquid the default exchange
perp --json wallet show                        # public addresses for active wallet
perp --json wallet list                        # all named wallets
perp --json wallet use <name>                  # set active wallet
perp --json wallet rename <old> <new>
perp --json wallet remove <name>
perp --json wallet balance   # gas token + USDC/USDT per chain (Arbitrum, Ethereum, Base, BNB, Robinhood USDG, Solana); failed reads → balance null + error
perp --json wallet solana <address>            # check arbitrary Solana address
perp --json wallet arbitrum <address>          # check arbitrary Arbitrum address
perp --json wallet migrate                     # migrate legacy ~/.perp/.env config
perp --json wallet rotate --from <name> --to <name> [--chain evm]   # MUTATING: new wallet + transfers assets; no --dry-run — only on explicit user request
perp --json wallet backup                      # encrypted backup
perp --json wallet restore <file>              # restore from backup
perp --json wallet deposit <walletName> [--for <ex>|-c <chain>]   # MoonPay multi-chain deposit (auto-converts to USDC)
perp --json wallet setup --name <n> --max-tx-usd <usd> --max-daily-usd <usd> [--skip-key]
                                               # one-click: wallet + policy + agent key.
                                               # Passphrase prompt unless OWS_PASSPHRASE env is set.
```

### Agent wallet (DEX-side delegation)
```bash
# Register an agent (master-signed: user consent; passphrase via OWS_PASSPHRASE / stdin; no --dry-run).
# Default expires-in is 90d — then AGENT_EXPIRED; pass --expires-in 1y / 180d / etc to extend.
perp --json wallet agent approve <exchange> \
  [--master <name>] \
  [--agent-name <name>] \
  [--expires-in 30d|90d|180d|1y|<ISO-8601>] \
  [--can-perp|--no-perp] [--can-spot|--no-spot] [--can-withdraw|--no-withdraw] \
  [--rotate] \
  [--ip-whitelist <list>] \
  [--account-index <0-9|255>]          # Arcus subaccount
  [--api-key-index <n>]                # Lighter slot 4-254 (default: first slot free locally AND on-chain)
  [--force]                            # Lighter: overwrite an --api-key-index slot that already holds an on-chain key
# risex: READ-ONLY in this release (trading is planned for a later release) — `wallet agent approve|import|revoke|rotate
#   risex` → CAPABILITY_UNSUPPORTED (also with --dry-run); `wallet agent verify risex` (read-only) still works.
#   txflow / variational / extended: every agent command → CAPABILITY_UNSUPPORTED (market data only).

# Import a key the USER created on the exchange WEBSITE (master wallet not needed here).
# Key on stdin only (one line; ondo: key id + secret; qfex: public key + secret) — an argv key is rejected (INVALID_PARAMS).
# Verified against the venue before storing (refused → nothing stored); pacifica → "unverified".
printf '%s' "$AGENT_KEY" | perp --json wallet agent import <exchange> \
  [--master-address <addr>]            # aster / pacifica / arcus: required; hyperliquid / lighter: cross-check
  [--account-index <n>] [--api-key-index <n>]   # lighter / lighter-rh: required (arcus: optional cross-check)
  [--account-id <uuid>]                # qfex: the account the key trades (default primary; required when piped — it confirms the binding)
  [--agent-name <name>] [--expires-in <dur>] [--replace]
# → data: { source: "imported", masterAddress, agentAddress|publicKey, accountIndex, apiKeyIndex,
#           expiresAt|null, storage, verification: { status: "verified"|"unverified", method } }

perp --json wallet agent list [exchange]          # rows carry source: "approved" | "imported"
perp --json wallet agent revoke <exchange> <agentName> [--local-only]
#   imported key: refused unless --local-only (deletes local key + record; still authorized on the
#   exchange — revoke it on the website). --local-only on an approved agent = --force.
perp --json wallet agent rotate <exchange> [oldAgentName]
#   imported key: refused — create a new key on the website, then import --agent-name <name> --replace
# verify: --master (Aster/PAC; passphrase via OWS_PASSPHRASE) / --master-address (HL only) / --account-index (Lighter only).
# Aster: NOT_IMPLEMENTED (no venue endpoint lists agents) — use wallet agent list aster.
perp --json wallet agent verify [exchange] [agentName] \
  [--master <name>] [--master-address <addr>] [--account-index <n>]
```

### Builder fees (`wallet builder`) — OFF by default
```bash
# Nothing is attached unless the user configures it explicitly (strict: format, cap, increment):
perp --json settings set builder.<venue> <address|code>,<feeBps> --yes   # hyperliquid/aster: address; pacifica/ondo: code; --yes required non-interactively
perp --json settings unset builder.<venue>
perp --json wallet builder status [venue]           # support, config, venue approval, attaches?
perp --json [--dry-run] wallet builder approve <venue> [--master <name>] [--yes]   # master-signed; y/N or --yes
perp --json [--dry-run] wallet builder revoke <venue> [--master <name>] [--yes]    # pacifica / aster
perp --json --no-builder -e <EX> trade market BTC buy 0.1   # never attach on this run
# Caps: hyperliquid 10 bps (never HIP-3), pacifica 10 bps max (perp-cli cap; never spot), aster 10 bps (mainnet),
# ondo 10 bps (no approval; also on position stops). lighter / lighter-rh / arcus → CAPABILITY_UNSUPPORTED.
# Approval missing/unknown → order sent WITHOUT the fee; execution.notes says why. execution.builderFee records it.
# No master on this computer → NO_SIGNER_AVAILABLE: approve on the venue website.
```

### Exchange settings (`wallet manage`)
```bash
perp --json -e <EX> wallet manage margin <SYMBOL> <cross|isolated>
perp --json wallet manage account-mode [unified|standard|portfolio]   # Hyperliquid only; no arg = show current
perp --json wallet manage sub create <name>            # not supported (CAPABILITY_UNSUPPORTED): the subaccount wallet must co-sign — use the web app
perp --json wallet manage sub list
perp --json wallet manage sub transfer <from> <to> <amount>   # <from> must be the signing account
perp --json wallet manage lake create [--manager <address>] [--nickname <name>] [--initial-deposit <amount>]   # --initial-deposit: master-signed only
perp --json wallet manage lake deposit|withdraw …           # MOVED → perp -e pacifica vault deposit|withdraw (refused here)
perp --json wallet manage builder overview                    # Pacifica builder-OWNER tools only (user approvals: wallet builder)
perp --json wallet manage builder trades <code>
perp --json wallet manage builder leaderboard <code>
perp --json wallet manage builder update-fee <code> <feeRate>
perp --json wallet manage referral claim <code>               # Pacifica
perp --json -e hyperliquid wallet manage referral set [code]  # HL / Lighter (-e lighter): signs + sends one referral action; supports --dry-run
perp --json wallet manage apikey create
perp --json wallet manage apikey list
perp --json wallet manage apikey revoke <key>
```

### OWS (Open Wallet Standard) API key + policy — optional, scoped agent tokens
```bash
perp --json wallet key create
perp --json wallet key list
perp --json wallet key revoke <id>
perp --json wallet policy create
perp --json wallet policy list
perp --json wallet policy show <id>
perp --json wallet policy delete <id>
```

## Risk & Analytics
```bash
perp --json risk status                        # portfolio risk overview (level, violations, canTrade)
perp --json health                             # adapter health: ping venue REST endpoints (connectivity + latency)
perp --json risk liquidation-distance          # % distance from liquidation for ALL positions
perp --json risk limits                        # view current risk limits
perp --json risk limits --min-liq-distance 30 --max-leverage 5  # set risk limits (also --max-position[-pct], --max-exposure[-pct], --max-positions, --daily-loss[-pct], --max-drawdown[-pct], --max-margin, --reset)
# The order gate (trade market/buy/sell/limit/split/scale-in/twap/multi, stop --no-reduce-only) enforces
# max position / total exposure / max positions; reduce-only exempt; --force bypasses (user consent only).
perp --json risk check --notional 1000 --leverage 3             # pre-trade risk check
```

## History (execution log + analytics)
```bash
perp --json history list                       # execution audit trail
perp --json history positions                  # position lifetime tracking
perp --json history prune                      # purge old entries
perp --json history summary                    # trading performance summary (replaces former 'stats')
perp --json history pnl                        # P&L breakdown by exchange; errors + partial name venues whose reads failed (left out, not 0)
perp --json history funding                    # funding payment aggregation
perp --json history report                     # full performance report (summary + pnl + funding); errors + partial + venuesRead
perp --json history compare                    # compare strategies / accounts
perp --json history snapshot                   # equity snapshot
perp --json history track                      # PnL tracking helper
perp --json history perf --period daily        # daily PnL breakdown
perp --json history perf --period weekly       # weekly PnL breakdown
perp --json history perf --period summary      # performance summary stats
```

## Strategies (`perp strategy` — 20 algorithms + nested scripted plans)
```bash
perp --json strategy list-strategies                         # list all 20 strategies
perp --json strategy run <STRATEGY> [SYMBOL] [--exchanges <list>]   # multi-venue strategies: --exchanges must include the -e venue
perp --json --dry-run strategy run <STRATEGY> [SYMBOL]       # simulate (actions logged, never sent)
perp --json strategy run funding-auto                        # multi-exchange funding arb
perp --json strategy apex [SYMBOL]                           # APEX orchestrator
perp --json strategy reflect                                 # performance analysis
perp --json strategy preset-list
perp --json strategy preset <NAME> [SYMBOL] [--size <n>]   # grid: total base; DCA: base per order; arb: $ per leg
perp --json strategy start <CONFIG.yaml>                     # YAML/JSON config-driven
perp --json strategy quick-grid <SYMBOL>
perp --json strategy quick-dca <SYMBOL> <SIDE> <AMOUNT> <INTERVAL_SEC> [--orders <n>]   # 0 = unlimited
perp --json strategy quick-arb
perp --json strategy delta-neutral
perp --json strategy twap <SYMBOL> <SIDE> <SIZE> <DURATION>
perp --json strategy grid <SYMBOL> --upper <PRICE> --lower <PRICE> --grids <N> --size <BASE> [--close-on-stop]
#   at stop: orders cancelled; the grid's inventory stays OPEN (warning) unless --close-on-stop
perp --json strategy dca <SYMBOL> <SIDE> <AMOUNT> <INTERVAL>
perp --json strategy trailing-stop <SYMBOL>
perp --json strategy funding-arb [--auto-execute]           # monitor only unless --auto-execute

# Quarantine (unknown / unhedged outcome): global per symbol, network-scoped; blocks opening orders,
# arb exec / arb auto and bots (reduce-only passes). Clear only after the USER verified positions.
perp --json strategy quarantine
perp --json strategy quarantine-clear <SYMBOL> [--strategy <source>]

# Scripted execution plans (one-shot multi-step)
perp --json strategy plan example
perp --json strategy plan validate <FILE>
perp --json --dry-run strategy plan execute <FILE>
# No --dry-run (refused with INVALID_PARAMS): strategy start / preset / quick-* / grid / dca / twap / funding-arb / apex
```

### Available Strategies (20)
- **Market Making:** `simple-mm`, `engine-mm`, `avellaneda-mm`, `regime-mm`, `grid-mm`, `liquidation-mm`
- **Signal/Directional:** `momentum-breakout`, `mean-reversion`, `aggressive-taker`
- **Arbitrage:** `funding-arb`, `funding-arb-v2`, `funding-auto`, `basis-arb`, `spot-perp-arb`
- **Infrastructure:** `hedge-agent`, `rfq-agent`, `claude-agent`
- **Classic:** `grid`, `dca`, `apex`

## Background Process Supervisor (tmux)
```bash
perp --json background list                   # list running jobs (default subcommand)
perp --json background stop <ID> [--timeout <sec>]   # graceful: SIGINT (job cancels its orders, saves state), waits (default 90s), then kills; reports what is left on the venue
perp --json background logs <ID>              # view logs (use -f to follow)
perp --json background remove <ID>            # remove a job entry
perp --json background clean                  # purge all stopped/done jobs
```

## Backtest
```bash
perp --json backtest funding-arb              # backtest funding arb on historical data
perp --json backtest grid                     # backtest grid strategy
```

## Alerts (Telegram / Discord)
```bash
perp alerts setup                             # interactive setup wizard
perp --json alerts test                       # send test message
perp --json alerts add <SYMBOL> <PCT> [--exchange <venue>] [--below]   # annual funding % threshold (default: above)
perp --json alerts add --all <PCT>            # alert for any symbol
perp --json alerts list                       # list active rules
perp --json alerts remove <SYMBOL|all>        # remove a rule
perp alerts start [--background]              # run daemon (tmux for background)
perp alerts stop                              # stop background daemon
```

## Settings
```bash
perp --json settings show                     # show current CLI settings
perp --json settings set <key> <value>        # set a CLI default
#   keys: default-exchange, defaultSlippageBps, slippageBps.<venue>, referralCodes.{hyperliquid,lighter},
#         builder.<venue> "<address|code>,<feeBps>" (off unless set), bridge.debridgeAffiliate.{referralCode,fee}
perp --json settings unset <key>              # slippageBps.<venue> | defaultSlippageBps | builder.<venue> | withdraw.<venue> | bridge.debridgeAffiliate
# withdraw.<venue> (withdraw / HL transfer allowlist + limits): USER ONLY, interactive terminal; agents never set it (POLICY_DENIED)
perp --json settings fees show                # cached exchange fee table
perp --json settings fees sync                # refresh fee cache
perp --json settings env show                 # show ~/.perp/.env values
perp --json settings env set <name> <value>   # non-secret values only (keys / *_PRIVATE_KEY / secrets → INVALID_PARAMS; use wallet set)
perp --json settings env remove <name>
perp --json settings env path                 # config file path
```

## Init / Setup
```bash
# Interactive default — DO NOT use from agent without flags (will hang on prompts).
perp setup                                    # alias: perp init
perp init

# Agent-safe non-interactive variant (writes settings; signs nothing by default):
OWS_PASSPHRASE=<pp> perp --json [-n testnet] setup --non-interactive \
  (--wallet <existing-ows-wallet> | --wallet-name <new-name>) \
  [--venues <list>] [--default-venue <venue>] \
  [--slippage-bps <n>] [--slippage <venue>=<bps> ...]
# Agent registration (signs with the master wallet — get user consent first):
#   --approve-agents --yes [--aster-can-spot] [--lighter-api-key-index <n>]
#   [--lighter-rh-api-key-index <n>] [--arcus-account-index <0-9|255>]
#   [--ondo-secret-stdin]   # Ondo key id + secret as 2 stdin lines; passphrase then via OWS_PASSPHRASE
# Keys created on the exchange WEBSITES (no master wallet needed when every venue is imported —
# then omit --wallet / --wallet-name; owsActiveWallet is left unchanged):
#   --import-agents <venues> --yes   # subset of --venues; keys on stdin, ONE LINE PER VENUE IN THIS ORDER
#                                    # (ondo: 2 lines — key id, then secret; qfex: 2 lines — public key, then secret)
#   [--master-address <venue>=<addr> ...]   # required for aster, pacifica, arcus
#   [--allow-unverified pacifica]           # required for pacifica (no read-only check exists)
#   [--qfex-account-id <uuid>]              # required for qfex (confirms the bound account)
#   [--lighter-account-index <n>] [--lighter-api-key-index <n>]
#   [--lighter-rh-account-index <n>] [--lighter-rh-api-key-index <n>] [--arcus-account-index <n>]
#   agents[] entries: { venue, status: "imported", agentName, verification }
```

For per-exchange key registration without the wizard, use `printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp wallet set <ex>` — also agent-safe (key on stdin, never argv).
