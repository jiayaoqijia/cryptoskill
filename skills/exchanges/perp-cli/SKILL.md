---
name: perp-cli
description: "Multi-DEX perpetual futures trading via the perp-cli command-line tool. Use when user asks to: trade perps, check funding rates, scan/execute arbitrage (perp-perp or spot-perp), run delta-neutral strategies, bridge USDC across chains, manage positions/orders/leverage, deposit/withdraw, hedge spot+perp, trade HIP-3 DEXes, read Derive options chains, use Pacifica Print or Pacifica vaults, or mentions perp-cli, hypurrquant, Pacifica, Hyperliquid, Lighter, Aster, Lighter RH, Ondo Perps, Arcus, QFEX, RISEx, TxFlow, Variational, GRVT, Extended, Derive, HyperEVM, funding arb, or U-tokens (UBTC/UETH/USOL). Covers Pacifica (Solana), Hyperliquid (HyperEVM), Lighter (Ethereum), Aster (BNB Chain), Lighter RH and Arcus (Robinhood chain), Ondo Perps and QFEX (off-chain), RISEx (RISE chain), TxFlow (market data only, UNOFFICIAL API) Variational Omni (market data only, official API), GRVT and Extended (Starknet) (market data only for now, official API), Derive options (read-only), and Pacifica Print / vaults."
license: MIT
allowed-tools: "Bash(perp:*), Bash(bash scripts/preflight.sh:*), Bash(bash scripts/arb-monitor.sh:*), Bash(bash scripts/funding-analysis.sh:*), Bash(bash scripts/spot-perp-scan.sh:*), Bash(bash scripts/validate-arb.sh:*)"
compatibility: "Requires Node.js 20 or newer and the perp-cli npm package installed by the user (version must be >= 0.16.0; the user runs `npm install -g perp-cli` — never install it yourself). Network access required for exchange APIs and bridge providers. Mutating commands need a wallet key imported into the OWS vault via 'perp wallet set EXCHANGE' (key on stdin or hidden prompt — never argv). Skill is portable across Claude Code, Claude.ai, Cursor, Codex, and Gemini CLI — no platform-specific features."
metadata:
  author: hypurrquant
  version: "0.16.0"
---

# perp-cli

Multi-DEX perpetual futures CLI + MCP server for Pacifica (Solana), Hyperliquid (HyperEVM), Lighter (Ethereum), Aster (BNB Chain), Lighter RH (`lighter-rh`, Robinhood chain, USDG), Ondo Perps (`ondo`), QFEX (`qfex`, custodial TradFi perps — import-only API key; resting reduce-only limits and automation are refused for now, see "QFEX" below), Arcus (`arcus`, Robinhood chain, USDG), RISEx (`risex|rise`, RISE chain, USDC — READ-ONLY in this release: market data + account reads; trading is planned for a later perp-cli release, see "RISEx" below), TxFlow (`txflow|txf`, MARKET DATA ONLY through an UNOFFICIAL API — no official API exists; it may break without notice, see "TxFlow" below), Variational Omni (`variational|var|omni`, MARKET DATA ONLY through its official read-only API — RFQ venue, no public trading API yet, see "Variational" below), GRVT (`grvt|grv`, MARKET DATA ONLY in this version through its official API — trading is planned for a later release, see "GRVT" below), Extended (`extended|ext|x10`, Starknet, formerly X10 — MARKET DATA ONLY in this version through its official public API, see "Extended" below). v0.13.0+ also supports Hyperliquid Outcome markets (HIP-4) — fully-collateralized binary/range contracts; each outcome's quote token comes from `outcomeMeta.quoteToken` (USDC on every listed outcome as of 2026-10-12), minimum order value 10 quote tokens.

## Instructions

### When to use this skill

Activate whenever the user wants to do anything against perp-cli, including: scanning funding-rate arbitrage, executing perp-perp or spot+perp legs, running long-running strategy bots, moving USDC between chains/exchanges, checking account/portfolio state, configuring wallets, or troubleshooting any of the above.

**Do NOT** answer trading questions from memory — always run the actual CLI command and parse its JSON output.

### Reference files (load only when needed)

This skill uses progressive disclosure. Read these on demand:

- `references/commands.md` — full command tree for every group (market, account, trade, outcome, options, print, vault, arb, funds, wallet, risk, history, strategy, background, alerts, settings, backtest)
- `references/agent-operations.md` — non-interactive setup flows, idempotency rules, error codes, common mistakes
- `references/strategies.md` — funding-arb decision framework + risk-management playbook (read before designing arb strategy)
- `references/ws-library.md` — WebSocket library (shipped since 0.15.0, @experimental), published standalone as **`@hypurrquant/perp-ws`** (zero dependencies; recommended for integrators — `npm install @hypurrquant/perp-ws`) and inside perp-cli as `perp-cli/ws` (same code, use it when perp-cli is already installed): build a live dashboard / funding comparison / account feed in the browser or Node (streams, events, nullability, comparator, user channels, errors, capability matrix). Cross-venue subscriptions use `canonicals` (e.g. `{ kind: "allMarkets", canonicals: ["BTC"] }`), never `symbols` (those are per-venue directory symbols); always surface `ready` rejections — an `idle` venue is not "fine"

Also bundled under `scripts/`: `preflight.sh`, `arb-monitor.sh`, `funding-analysis.sh`, `spot-perp-scan.sh`, `validate-arb.sh`. Use these for repeatable multi-step diagnostics. They need `perp` on PATH (else they exit 1 with `PERP_NOT_FOUND` — ask the user to install it) and exit non-zero on a failed read; `funding-analysis.sh` / `spot-perp-scan.sh` take `-n mainnet|testnet`, `spot-perp-scan.sh --no-portfolio` scans without a wallet.

### Critical rules

1. **Always pass `--json`.** Without it, output is human-formatted and hard to parse. `ok:false` also exits 1.
2. **Always pass `-e <venue>`** on venue-scoped commands. The default is `settings.defaultExchange`, else `pacifica` — never rely on it.
3. **Always run `--dry-run` first** for any mutating command that supports it, show the result, get user confirmation, then execute without `--dry-run`. `--help` is NOT a reliable indicator — the 0.16.0 list: every `trade` write (market / buy / sell / limit / split / cancel / cancel-all / stop / tpsl / scale-tp / scale-in / edit / atomic / leverage / close / close-all / flatten / reduce / spot-buy / spot-sell / spot-limit / spot-cancel / spot-transfer), `arb exec|close|auto|rebalance`, `funds deposit|withdraw|transfer|faucet|bridge send|bridge exchange|rebalance execute|address-book add`, `outcome buy|sell`, `print deposit|cancel`, `vault deposit|withdraw`, `wallet builder approve|revoke`, `wallet manage referral set`, `strategy run`, `strategy plan execute`. Everything else (read-only commands too; `trade twap|multi|cancel-stop|cancel-twap`; the moved stubs `wallet manage lake deposit|withdraw` → use `vault deposit|withdraw`) refuses `--dry-run` with `INVALID_PARAMS` — that refusal means "unsupported", nothing ran (see "Safety rules").
4. **Always use `--fields`** when you only need specific data — saves tokens.
5. **Avoid bare `perp setup` / `perp init` / `perp wallet setup`** — they prompt and will hang an agent. Use `printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set <exchange>` for key registration (key on stdin; a key on argv or `-k` is rejected), or `perp --json setup --non-interactive --wallet <ows-wallet> --venues <list> [--default-venue <v>] [--slippage-bps <n>] [--slippage <venue>=<bps>]` (new wallet: `--wallet-name <name>` with the passphrase in `OWS_PASSPHRASE`; agent registration only with `--approve-agents --yes`, after user confirmation) (and `OWS_PASSPHRASE=<pp> perp wallet setup --name <n> --max-tx-usd <usd> --max-daily-usd <usd>`) when the wizard is required. The passphrase goes in `OWS_PASSPHRASE` or stdin — the root `--passphrase` flag is deprecated (visible in `ps`).
6. **NEVER trade without explicit user confirmation.** A dry-run is not consent.
7. **NEVER read `~/.perp/.env` or other key files.** The CLI reads them — you should not.
8. **NEVER manually add `-PERP` suffix** to symbols. Use bare names (`BTC`, `SOL`, `ICP`); the CLI resolves exchange-specific naming.
9. **NEVER resubmit after `ORDER_PENDING`** (or any unknown outcome). See "Safety rules".

### Step 1: Verify install, version, venue health

```bash
perp --version         # must be >= 0.16.0
perp --json health     # keyless venue connectivity
```

If `perp` is missing or older, STOP and ask the user to install / upgrade it (`npm install -g perp-cli`) — never install it yourself and never switch to `npx`. `health`: `data.healthy` = every OFFICIAL-API venue is up (use this); `allHealthy` also counts unofficial APIs (TxFlow, listed under `unofficial[]`); `skipped[]` = venues with no environment on this network (not probed). Don't use a venue whose `exchanges[].status` is not `"ok"`.

### Step 2: Verify wallet + balance

```bash
perp --json wallet show               # with an OWS wallet, `exchanges: []` is normal — owsActiveWallet serves every venue
perp --json portfolio -e <venue>      # per-exchange perp.available (aliases like hl / pac accepted)
```

If any required exchange is missing, register it (user supplies the key):

```bash
printf '%s' "$EVM_HEX_KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set hl          # Hyperliquid / Lighter / Aster (EVM)
printf '%s' "$SOLANA_BASE58_KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set pac   # Pacifica (Solana)
```

The key is read from stdin (never argv — an argv key is rejected) and imported into the OWS vault; the imported wallet becomes `owsActiveWallet`, which serves every venue. The same EVM key works for Hyperliquid, Lighter and Aster. Lighter trading additionally needs `perp wallet agent approve lighter`.

Lighter RH / Ondo Perps / Arcus have no `wallet set` path — register an agent / API key (user runs it; Ondo reads key id + secret from stdin):

```bash
perp --json wallet agent approve lighter-rh
printf '%s\n%s\n' "$KEY_ID" "$SECRET" | perp --json wallet agent approve ondo
perp --json wallet agent approve arcus --master <ows-wallet>   # address must be on the Arcus access whitelist
```

**No master wallet on this computer?** The user can create the agent / API key on the exchange website and import it — key on stdin only, verified against the venue before it is stored (`verification.status` is `"unverified"` only for Pacifica, which lists bindings master-signed only):

```bash
printf '%s' "$AGENT_KEY" | perp --json wallet agent import hyperliquid               # master read from HL
printf '%s' "$AGENT_KEY" | perp --json wallet agent import aster --master-address 0x…  # also Aster testnet
printf '%s' "$AGENT_KEY" | perp --json wallet agent import pacifica --master-address <SOL>
printf '%s' "$API_KEY" | perp --json wallet agent import lighter --account-index <n> --api-key-index <slot>
printf '%s' "$ED25519_KEY" | perp --json wallet agent import arcus --master-address 0x…
```

Imported keys trade; `funds deposit|withdraw|transfer|bridge`, `wallet manage referral set` and `wallet agent approve` need the master → `NO_SIGNER_AVAILABLE` (tell the user to do it on the website or `perp wallet import` the master). `wallet agent revoke` of an imported key needs `--local-only` and does NOT revoke it on the exchange; `rotate` is refused (new key on the website → `import --replace`).

**QFEX** (`-e qfex`, testnet = QFEX UAT): keys are created on the QFEX website and imported by the USER (`perp wallet agent import qfex [--account-id <uuid>]` — the resolved account UUID must be confirmed). Rules an agent must follow:
- Works: market / IOC reduce-only closes (`trade close/close-all/flatten/reduce`), reduce-only stop-market orders (`trade stop`, `trade tpsl` TP/SL legs, `--tp/--sl` as separate stops after the verified fill; cancel with `trade cancel <S> <id>` or `trade cancel-stop`), `trade edit` of a plain LIMIT / ALO (the venue assigns a new order id; the client id is kept).
- Refused with `CAPABILITY_UNSUPPORTED` (do not work around): resting reduce-only limits (GTC / ALO / FOK, `scale-tp`), stop-limit and opening stops, amend of a reduce-only order, `--client-id`, non-USD-quoted markets, unattended automation (bots / plans / TWAP / DCA / grid / background jobs), QFEX as a funding-arb / funding-bot leg.
- After a close, reduce-only / stop orders left on a now-flat symbol are listed as a WARNING (the venue does not cancel them) — cancel them, or use `trade flatten`, which cancels them.
- Limit GTC / ALO returns `status: accepted, finality: pending` after the ACK; `open` only via `perp --json trade status c:<id> --symbol <S> -e qfex`.
- `ORDER_PENDING` = outcome unknown: NEVER resubmit; check with the `c:<id>` in the remediation.
- Funding rates on QFEX are unverified: excluded everywhere unless `perp --json arb scan --rates --include-unverified` (display only).
- Withdrawals are disabled in perp-cli for now: `funds withdraw qfex` → `CAPABILITY_UNSUPPORTED` (also under `--dry-run`). Withdraw in the QFEX web app. Ondo Perps has no API withdrawals either.

**RISEx** (`-e risex`, testnet = `-n testnet`, official API): **READ-ONLY in this perp-cli release** — RISEx trading is planned for a later release. Rules an agent must follow:
- Works: market data (`market list|prices|info|book|trades|kline|funding -e risex`), `perp health`, RISEx rows in `perp --json arb scan` / `arb scan --rates` (funding is hourly and verified), MCP market-data tools, and account reads with only the master address selected (`portfolio`, `account positions|orders|history|trades|funding-history -e risex` — public by address, nothing is signed). `wallet agent verify risex` (read-only) still checks a signer registered by an earlier build.
- Refused with `CAPABILITY_UNSUPPORTED` ("RISEx trading is planned for a later perp-cli release; in this version RISEx is read-only") before any key is read or request is sent — also under `--dry-run`: every `trade …` write (market / buy / sell / limit / cancel / cancel-all / leverage / close / stop / tpsl / edit / twap / …), `trade multi` legs, `arb exec|auto` legs, every `strategy …` command (bots, plans, TWAP / grid / DCA, `--exchanges` legs), `wallet agent approve|import|revoke|rotate risex` (`revoke --force` only clears the local record), `perp setup --venues risex`, `funds faucet risex`, and the MCP `trade_preview` / `trade_execute` / `trade_close` tools. Never try to trade RISEx through perp-cli — the user trades in app.rise.trade. `arb scan --basis` lists trading venues only, so RISEx is not in it; in `arb scan` a pair with a RISEx leg is `executable: false` (`readOnlyLegs`) — data only.
- Deposits and withdrawals are app-only: `funds deposit|withdraw risex` → `CAPABILITY_UNSUPPORTED` (also under `--dry-run`), remediation app.rise.trade.
- Funding: hourly, `current_funding_rate` = the last settled hourly print (verified against funding payments).

**TxFlow** (`-e txflow`): UNOFFICIAL — TxFlow has no official API; perp-cli reads the undocumented API its web app uses, READ-ONLY. It may change or be blocked at any time; every JSON row says `venueApi: "unofficial"` (`apiStatus` in mixed tables, MCP meta), human output carries a footnote. Rules an agent must follow:
- Works: `market list|prices|info|book|trades|kline -e txflow`, and TxFlow rows in `perp --json arb scan --rates --include-unverified` (display only). Funding is percent per hour on the venue, shown as a FRACTION per hour, and is UNVERIFIED (a live estimate) — never rank or trade on it.
- Refused with `CAPABILITY_UNSUPPORTED` before any request: every trade / account / portfolio / funds / agent / builder / bot command, and funding history (`market funding`). Never try to trade TxFlow through perp-cli; the user trades on the TxFlow website.
- A blocked read (`EXCHANGE_ERROR` "unofficial API refused …") is not retried and has no fallback; there is no testnet.

**Variational** (`-e variational`, aliases `var`, `omni`): Variational Omni, read-only (market data) in perp-cli through its OFFICIAL documented API (`GET /metadata/v2/stats`, one call for all ~575 markets, cached ~5 s; venue limit 10 requests / 10 s per IP). Variational has no public trading API yet. It is an RFQ venue: one market maker (the OLP) quotes every trade — there is no order book.
- Works: `market list|prices|info|funding|book -e variational`, `perp health` (official), and Variational rows in `perp --json arb scan --rates --include-unverified` / `--compare <sym> --include-unverified` only — display only, never ranked or traded: funding is UNVERIFIED (a moving predicted rate, not checked against settled payments). `US500-PERP` is the SPDR S&P 500 ETF, compared as `SPY`; SPX (SPX6900) and QNT (Quant) are never matched.
- `market book` shows the OLP's INDICATIVE RFQ quotes at fixed notionals (min order, $1k, $100k, $1M when published; `kind: "rfqQuotes"`), never order-book levels; they may be up to 600 s old (`updatedAt`). `market mid|trades|kline` are refused (`CAPABILITY_UNSUPPORTED`).
- Funding: the interval is PER MARKET (1h / 4h / 8h perps; `fundingHours` on each row), positive = longs pay. `fundingRate` is the fraction for one interval; `market funding <sym>` shows the current terms (`kind: "currentFunding"`: per interval, hourly, APR %, next time) — there is no funding history. `rateKind` is `predicted`: the rate for the window ending at `nextFundingTime`, recomputed during the window.
- Perp symbols are the base (`BTC`); swaps keep their suffix (`XAU-SWAP`): daily-funded TradFi swaps with separate long / short rates, `fundingRate` null and never matched across venues. Open interest is published in USD, single-sided (`openInterestUsd`); base-unit `openInterest` is null. No index price, tick, lot or leverage is published (null).
- Refused with `CAPABILITY_UNSUPPORTED` before any request: every trade / account / portfolio / funds / agent / builder / bot command (also with `--dry-run`). The user trades on omni.variational.io. No testnet. Variational's terms exclude US / Canada persons and sanctioned regions (perp-cli only warns).

**GRVT** (`-e grvt`, testnet = `-n testnet`): official Market Data API (api-docs.grvt.io), READ-ONLY in this version. Rules an agent must follow:
- Works: `market list|prices|info|book|trades|funding|kline -e grvt`, `perp health` (counted among the official venues), and GRVT rows in `perp --json arb scan --rates --include-unverified` (display only).
- Symbols are the base ticker (`BTC`, `KPEPE`, `XAU`, `AAPL`; `BTC_USDT_Perp` also accepted); `venueSymbol` is GRVT's instrument name. Unknown symbols → `SYMBOL_NOT_FOUND`. Pre-IPO markets (OPENAI, ANTHROPIC, SPACEX) are never matched across venues.
- Funding interval is PER MARKET (8 h or 4 h — `fundingHours`); rates are fractions per that interval (GRVT publishes percent). `market list|prices|info` rows carry the INDICATIVE rate of the running interval (`fundingRateKind: "predicted"`, moves until `nextFundingTime`); `market funding` is the settled history (`rateKind: "lastSettled"`, `intervalHours` per row). Funding is UNVERIFIED (not yet checked against settled payments) — never rank or trade on it.
- `stepSize` is null (GRVT publishes a minimum size, `minSize`, but no lot step); `maxLeverage` / `marginTiers` come from GRVT's margin rules and are filled by `market list|prices|info` only (cached up to 6 h — `leverageAsOf` says when they were read) — MCP `get_markets` / `get_prices` rows have them null (price-only path). Equities match other venues only when reviewed; an unreviewed new GRVT equity has `canonical: null`.
- Refused with `CAPABILITY_UNSUPPORTED` before any request (also under `--dry-run`): every trade / account / portfolio / funds / agent / builder / bot command and `setup` venue selection — remediation "GRVT is read-only (market data) in this version; trading is planned for a later release". GRVT trading needs KYC and is banned in restricted jurisdictions (US, CA, SG, HK, …) — relevant once trading lands.

**Extended** (`-e extended`, aliases `ext` / `x10`; testnet = Sepolia via `-n testnet`): official public API (api.docs.extended.exchange), READ-ONLY in this version — counted as an official venue in `perp health`. Rules an agent must follow:
- Works: `market list|prices|info|book|trades|funding|kline -e extended`, and Extended rows in `perp --json arb scan --rates --include-unverified` (display only — funding is UNVERIFIED: never rank or trade on it). `market list` rows carry `assetClass` (crypto / equity / etf / index / commodity / fx / preIpo; human table "Class" column), `venueSymbol` (wire name, e.g. `TSLA_24_5-USD`), `tickSize`, `minSize`, `tradable` (false while `REDUCE_ONLY` or `isOffHours`), `isRfq`, `tradingHours`.
- Symbols: `assetName` without the `_24_5` suffix (`TSLA_24_5-USD` → `TSLA`, `SPX500m-USD` → `SPX500M`); `-e extended market book TSLA-USD` and the wire name also resolve. The crypto `SPX` market is SPX6900, not the S&P 500 (index = `SPX500M`). RWA tickers that are also crypto tickers (PURR = Hyperliquid Strategies Inc., QNT, BB, ON, ADI, BOT), XIAOMI and the crypto SPX are never matched across venues.
- Funding: applied hourly; `fundingRate` in market rows = the current hour's ACCRUING rate (fraction per hour, recomputed every minute, rounded to 6 decimals by the venue — no public source is more precise; `fundingRateKind: "accruing"`, `nextFundingTime`), `market funding` = applied hourly prints (`rateKind: "lastSettled"`, `annualizedPct`). `_24_5` equities print 0 while their underlying is closed (weekends / holidays), so an annualized rate overstates them.
- Refused with `CAPABILITY_UNSUPPORTED` before any request ("Extended is read-only (market data) in this version; trading is planned for a later release"): every trade / account / portfolio / funds / agent / builder / bot command, also under `--dry-run`. RFQ markets' REST order book is the indicative book.

Venue rules for these: `trade limit` defaults to `--tif GTC` on every venue (arcus maps it to GTT; ondo offers GTC|IOC|ALO; FOK is never emulated → `CAPABILITY_UNSUPPORTED` where not offered); market orders on every venue are bounded by `--slippage-bps <n>` → `settings.slippageBps.<venue>` → `settings.defaultSlippageBps` (shipped default 50). Ondo (US, PA) and Arcus (US, CA, GB) print a one-time restricted-region notice on stderr when used with credentials (warn only, never blocks).

### Step 3: Discover (read-only)

```bash
perp --json arb scan                              # all modes (perp-perp + spot-perp), default --min 10 (% annual)
perp --json arb scan --mode perp-perp --top 10
perp --json arb scan --mode spot-perp --top 10
perp --json arb scan --rates                      # raw funding rates
perp --json arb scan --basis [<symbol>]           # cross-exchange basis
perp --json arb scan --gaps                       # cross-exchange price gaps
perp --json arb scan --hip3                       # HIP-3 cross-dex spreads
perp --json arb scan --history <symbol>           # LOCAL snapshots only (written by earlier `arb scan --rates` runs; often `rates: {}`)
perp --json -e <ex> market funding <symbol> -l 24 # real settled history (newest first; rate per `intervalHours`)
perp --json arb scan --compare <symbol>           # one symbol across all exchanges
perp --json arb scan --positions                  # funding impact on open positions
perp --json arb scan --live --interval 60         # continuous monitoring
```

Common knobs: `--min <pct>`, `--top <n>`, `--hold-days <n>` (default 7), `--bridge-cost <usd>`, `--size <usd>`.

Prices: `perp --json -e <ex> market mid <SYM>` is the canonical price read; cross-venue: `arb scan --compare <SYM>`. `market prices` takes no symbol (every market). There is no spot price / book read (`market *` are perp markets; `HYPE/USDC`, `@107`, `HYPE-SPOT` → `SYMBOL_NOT_FOUND`), and `arb scan --basis` is cross-venue PERP basis, not spot-perp.

**Reading scan rows** — act only on these fields (detail: `references/commands.md` → "Arbitrage"):
- perp-perp rows (`mode: "perp-perp"`): `longExch` / `shortExch`, `netSpread` / `grossSpread` (= `netSpreadPct` / `grossSpreadPct`, annual %), `estFeesPct` (estimated round trip on BOTH legs incl. 0.1 % slippage — e.g. hl+hl 0.24 %; `perp settings fees show` is the per-fill taker rate it is built from).
- spot-perp rows (`mode: "spot-perp"`): `spotExchanges[]`, `perpExchange`, `direction`, `netSpread`, `estFeesPct`, `breakEvenDays` — no `longExch` / `shortExch`. Executable ONLY when `direction == "long-spot-short-perp"`: `arb exec <SYM> spot:<one of spotExchanges> <perpExchange> <USD>`. `arb exec spot:` does not look at the funding sign — it always buys spot and shorts the perp, so on a `sell-spot-long-perp` row it would PAY the funding. Never act on `sell-spot-long-perp` rows.
- `--rates` / `--compare` rows: `longExchange` / `shortExchange` / `maxSpreadAnnual` (all null when fewer than two verified rates), `executable`, `readOnlyLegs`, `unverifiedLegs`, `mixedKinds` (the legs' rates are of different kinds — lastSettled / accruing / predicted); `--rates` top level has `minSpread` / `belowMinSpread`. Act only when `executable === true`. `--compare <unknown>` is `ok:true` with `data.available: false`.
- **Testnet funding rates and spreads are meaningless** (thousands of % / yr). Never report them as opportunities; do yield analysis on mainnet public reads (keyless, `-n mainnet`).

#### HIP-3 dexes (part of Hyperliquid, not a separate venue)

HIP-3 dexes are selected on the Hyperliquid venue with the root `--dex <name>` flag; every market / account / trade command works the same way. Same account and wallet as native Hyperliquid perps.

```bash
perp --json -e hyperliquid market hip3                               # deployed dexes: name, deployer, assets, delistedAssets, delisted
perp --json -e hyperliquid market list --hip3                        # native + every HIP-3 dex market
perp --json -e hyperliquid --dex xyz market list                     # markets on dex "xyz"
perp --json -e hyperliquid --dex xyz market info GOLD                # symbols WITHOUT the "xyz:" prefix
perp --json -e hyperliquid --dex xyz account positions               # positions on that dex only
perp --json -e hyperliquid account positions --hip3                  # native + every HIP-3 dex
perp --json -e hyperliquid --dex xyz --dry-run trade market GOLD buy 0.01
```

- `--dex` with any other `-e` venue → `INVALID_PARAMS` (never ignored).
- A dex symbol without `--dex` (e.g. `-e hyperliquid market mid xyz:GOLD`) → `SYMBOL_NOT_FOUND` with remediation `--dex xyz`; it is never read from the native dex.
- `portfolio --dexes` works only with `--serve` (web dashboard); for HIP-3 positions use `account positions --hip3` / `--dex <name>` or `--address`. Builder fees are never attached on HIP-3.
- Symbols: input is bare (`BTC`; HIP-3 `TSLA` + `--dex xyz`). Output differs: market rows are plain, keyed HL native position / order rows show `<COIN>-PERP`, HIP-3 rows `xyz:TSLA` — pass the bare name back (`BTC`, `TSLA` + `--dex xyz`).
- MCP tools cover native Hyperliquid perps only, except `get_positions_by_address` (reads every HIP-3 dex) — use the CLI for the rest of HIP-3.

#### Options market data (Derive, read-only)

Derive (derive.xyz) options via the official public API — keyless, never trades. Not a perp venue (`-e derive` works only with `perp options`).

```bash
perp --json -e derive options expiries ETH                              # active expiries
perp --json -e derive options chain ETH --expiry 2026-12-25 --strikes 10 # calls/puts per strike: bid/ask, mark, IV, greeks, OI
perp --json -e derive options quote ETH-20261225-3500-P                 # one option
```

`schema: 1`; decimals are strings; `null` = unknown (empty side, uncomputable IV). Unknown underlying / expiry / instrument → `SYMBOL_NOT_FOUND`. Full reference: `references/commands.md` → "Options market data".

### Step 4: Validate before mutating

For arb:

```bash
perp --json portfolio -e <longEx>                     # perp.available (long leg)
perp --json portfolio -e <shortEx>                    # perp.available (short leg)
perp --json --dry-run arb exec <SYM> <longEx> <shortEx> <USD>
```

Spot-perp (`spot:<venue>` long leg, only for `direction == "long-spot-short-perp"` rows): the spot leg needs the full spot notional in the spot venue's quote (`perp --json -e <venue> trade spot-balance`; separate-margin venues transfer the shortfall perp→spot) plus perp margin on the perp leg — the dry-run checks both and refuses an empty book or a > 5% spot/perp price gap.

For a single trade:

```bash
perp --json -e <ex> market info <SYM>                                    # markPrice, stepSize (lot), maxLeverage
perp --json -e <ex> trade check <SYM> <SIDE> <SIZE> --leverage <N>
perp --json --dry-run -e <ex> trade buy <SYM> <SIZE>                     # market entry
perp --json --dry-run -e <ex> trade buy <SYM> <SIZE> --tp <PX> --sl <PX> # entry + TP/SL
perp --json --dry-run -e <ex> trade buy <SYM> <SIZE> --smart             # IOC at best ask + 1 tick (no TP/SL)
```

> `trade check` does NOT read exchange-set leverage. Always pass `--leverage` explicitly.
>
> `--tp` / `--sl` are ABSOLUTE trigger prices (not %). Market entries: every venue (venues that place TP/SL as separate orders need a market / IOC entry); `trade limit --tp/--sl`: ondo / arcus on any entry, elsewhere only with `--tif IOC`. TP/SL on an already open position: `trade tpsl <SYM> long|short --tp <PX> --sl <PX>` (side = the position's side).
>
> `--smart` (IOC at best bid/ask ± 1 tick) exists only on pacifica / hyperliquid / lighter / aster, and is refused (`CAPABILITY_UNSUPPORTED`) together with `--tp`/`--sl` or `--client-id`/`--auto-id` — need TP/SL → plain market entry (or `--smart`, then `trade tpsl`).
>
> Pacifica basket (pair trade): `perp --json --dry-run -e pacifica trade atomic --long BTC:50 --short ETH:50 --usd 1000` — one batch of market orders, NOT all-or-nothing (a leg can fill while another is refused → `ORDER_PARTIAL`; an unconfirmed leg → `ORDER_PENDING` + quarantine). A batch failure other than HTTP 400 / 429 quarantines every leg. Pacifica's Chase / OCO / Trailing Stop / Swarm / Trigger Swarm / Conditional orders have no documented API / SDK path (as of 2026-10-19); nearest here: `trade twap` (≈ Swarm) and `trade tpsl` (≈ OCO bracket exit).

Show the dry-run output to the user. Wait for confirmation.

#### Minimum order size and tick (not in `market info`; `trade check` and `--dry-run` do NOT enforce the minimum)

| Venue | Min order value (USD notional) |
|---|---|
| hyperliquid | $10 (also spot; HIP-4 outcomes: 10 quote tokens) |
| pacifica | $10 (per market `min_order_size`) |
| lighter, lighter-rh | $10 (per market `min_quote_amount`; a few markets 0) |
| aster | $5 (`MIN_NOTIONAL`) |
| arcus | $5 (`minOrderNotional`; reduce-only exempt; perp-cli refuses below it, `SIZE_TOO_SMALL`) |
| ondo, qfex | unknown (not published) |

Values read from the venues' public market data on 2026-10-26; keyless MCP `get_markets` (no credentials configured) returns them per market as `minNotional`, with `tickSize` / `minSize`. **Default smallest order = $15 notional** (on every venue, including the $5 ones and the unknown ones): `mark` = `market mid <SYM>`, `step` = `stepSize` from `market info`; `size = ceil(15 / mark / step) × step`, then `trade check` + dry-run. The $15 buffer over the $10 venue minimum absorbs price moves between sizing and the fill, step rounding and fees; below the venue minimum the live order is rejected. Use the bare venue minimum only when the user explicitly asks for it. Anything that splits a position must keep every piece ≥ $15 too: `trade reduce 50` / `scale-tp` / partial `tpsl --size` need a position of ≥ $30 (≥ $15 × number of pieces), and an arb's matched size must clear $15 on both legs. Tick: off-grid limit / trigger prices are refused with `INVALID_TICK` on the live send (never rounded, nothing sent) — Hyperliquid: ≤ 5 significant figures; elsewhere take `tickSize` from keyless MCP `get_markets` or the price steps of `market book <SYM>`.

### Step 5: Execute

After explicit user confirmation:

```bash
# Perp-perp arb: legs are SEQUENTIAL — long first, then the short sized to the verified long fill;
# reconcile is always on (the long is trimmed reduce-only to the short's verified fill).
# An unconfirmed leg quarantines the symbol (see "Safety rules").
perp --json arb exec <SYM> <longEx> <shortEx> <USD> --smart

# Spot+perp arb (spot has 0 funding cost; spot:<venue> = hl, lt, lrh, aster, ondo)
# ONLY for a spot-perp scan row with direction == "long-spot-short-perp": buys spot, shorts the perp.
perp --json arb exec <SYM> spot:hl hl <USD>
perp --json arb exec <SYM> spot:lt pac <USD>

# Single trade
perp --json -e <ex> trade buy  <SYM> <SIZE> --smart
perp --json -e <ex> trade sell <SYM> <SIZE> --tp <PX> --sl <PX>
perp --json -e <ex> trade split <SYM> buy <USD> --max-slippage 0.5
```

#### Orders: limit / status / edit / cancel

```bash
perp --json -e <ex> trade limit <SYM> buy|sell <PRICE> <SIZE> [--tif GTC|IOC|FOK|ALO] [--reduce-only]   # default GTC
perp --json -e <ex> account orders                                # open orders + ids
perp --json -e <ex> trade status <ORDER_ID> [--symbol <SYM>]      # --symbol required on ondo / arcus / qfex
perp --json -e <ex> trade edit <SYM> <ORDER_ID> <PRICE> <SIZE>    # SIZE = new open (unfilled) size
perp --json -e <ex> trade cancel <SYM> <ORDER_ID>                 # one order
perp --json -e <ex> trade cancel <SYM>                            # every order on that symbol
```

All of these writes take `--dry-run`. **`trade edit` may return a NEW `orderId` — always continue with the id it returns**: pacifica (ALO → native edit, GTC / TOB → cancel+replace; new id either way, TIF kept), ondo (cancel+replace), qfex (venue assigns a new id); hyperliquid / lighter / lighter-rh / aster / arcus amend natively — use the returned id anyway. `trade edit --tif` only on ondo / pacifica.

HL spot uses U-tokens (`BTC→UBTC`, `ETH→UETH`, `SOL→USOL`) — auto-resolved.

### Step 6: Monitor

```bash
perp --json arb status                              # open arb positions, PnL, funding earned
perp --json portfolio                               # cross-exchange equity + risk
perp --json risk status                             # canTrade, level, violations
perp --json risk liquidation-distance               # % from liq for ALL positions
perp --json -e <ex> account positions --address <ADDR> [--symbol BTC] [--account-index <n>]   # keyless, ANY account
perp --json -e <ex> account balance --address <ADDR> [--account-index <n>]                  # keyless balances of ANY account
```

`arb status` reads every configured venue and fails as a whole (`EXCHANGE_ERROR`) when one venue's read fails — there is no venue filter; check the venues one by one with `perp --json -e <ex> account positions` and report which one failed. Never read the failure as "no positions".

`account positions --address` (keyless, nothing signed; without `-e`: every venue that supports it): hyperliquid (0x; native + every HIP-3 dex, rows carry `dex`), lighter / lighter-rh (0x; every account of the address, rows carry `accountIndex`, narrow with `--account-index`), pacifica (Solana address), risex (0x). Other venues → `CAPABILITY_UNSUPPORTED`. MCP `get_positions_by_address` returns the same rows (HIP-3 included). `account balance --address` (same venues and address rules; MCP `get_balance_by_address`): `data = { exchange, address, balance, spot }` — `balance` = `{ equity, available, marginUsed, unrealizedPnl }` (+ Pacifica `usdcBalance` / `borrowedUsdc` / `pendingInterest` / `availableToWithdraw`), `spot` = token rows or null (RISEx). Hyperliquid: `accountMode` decides equity (unified / portfolio → the spot collateral row; standard / default → perp `accountValue`; read `meta.notes`), `dexes` = HIP-3 dexes with a non-zero value, a failed dex → `meta.errors["hip3:<dex>"]` + `meta.warnings` (unknown, not zero). Lighter: top-level `balance` / `spot` null, one row per account in `accounts: [{ accountIndex, balance, spot }]`; no account → `[]` + note. `account balance` WITHOUT `--address` is the renamed-command error — your own balance is `perp portfolio`.

If `risk status.canTrade === false`, do NOT open new positions. If liquidation distance falls below the user's `--min-liq-distance`, recommend reducing position size.

For continuous monitoring, run `bash scripts/arb-monitor.sh --json`.

### Step 7: Close

```bash
perp --json arb close <SYM>                                     # perp-perp arb
perp --json arb close <SYM> --pair <longEx>:<shortEx>           # disambiguate
perp --json arb close <SYM> --spot-exch hl --perp-exch hl       # spot+perp
perp --json arb close <SYM> --smart                             # IOC limits
perp --json arb close <SYM> --force                             # quarantined symbol — only after the user checked positions
perp --json arb close <SYM> --state-only --yes                  # drop a stale state entry (arb status staleStateEntries); sends no order

# Single trade (dry-run first, then confirm)
perp --json -e <ex> trade close <SYM>                           # close one symbol
perp --json -e <ex> trade close-all                             # close all positions on this exchange
perp --json -e <ex> trade flatten                               # cancel ALL orders, then close ALL positions
```

`trade close` / `close-all` close positions only — perp-cli does not cancel resting TP/SL / stop / limit orders (QFEX lists the leftovers as a WARNING). After a close, run `account orders` and cancel what is left (`trade cancel <SYM> <id>`), or use `trade flatten`, which cancels every order on the venue first.

### Pacifica Print and vaults (`perp print`, `perp vault`)

Pacifica-only, details in `references/commands.md`. Reads first (`print games`, `print quote`, `print positions`, `vault list|info|positions`); every write is `--dry-run` first and needs the user's confirmation:
- **Print** (`print deposit <game> long|short <usd> --strike <px> --leverage <n> [--cycles 1-1000]`) locks the deposit until a fill or until a cancel settles at the END of the running cycle (up to 30 days on `BTC_1M`). Before asking, show the user: cycle length, `--cycles`, leverage, `maxLoss` (deposit + premiums), and that `docsLiquidationPrice` is only an outer bound (a liquidation was observed earlier in one live case; the venue trigger is unpublished). Checkpoint-only evaluation applies while resting; after a fill it is an ordinary position in the main account (continuous liquidation, nets with an existing position) — `account positions`. The premium is not quoted by perp-cli. `print cancel` uses an UNOFFICIAL endpoint: live runs need `--unverified-endpoint`.
- **Vaults** (`vault deposit <vault> <usd>`, `vault withdraw <vault> <shares>|--all`): third-party trading pools (can lose the whole deposit); every deposit restarts the lock-up for the whole balance; withdrawals only go to the own account, inside the vault's window. **`vault deposit` is master-only** (never an agent key). Pass the vault ADDRESS and confirm the shown manager with the user — nicknames are not unique (an ambiguous one is refused with the candidates).
- `ORDER_PENDING` on any of them → NEVER resubmit with a new key; check `print positions` / `vault positions` against `error.details.before`. The only safe retry is the same command with `--idempotency-key <reported key>` (dedupe window unverified).

### Funds workflow (deposit / withdraw / transfer / bridge / rebalance)

All money movement lives under `perp funds`:

```bash
# Exchange in/out
perp --json funds deposit hyperliquid 100
perp --json funds deposit pacifica 100
perp --json funds deposit lighter ethereum 100              # L1 direct
perp --json funds deposit lighter cctp arbitrum 100         # via CCTP
perp --json funds withdraw hyperliquid 100 [--chain arbitrum|ethereum|base]   # CCTP to your own wallet
perp --json funds transfer 100 <ADDRESS>                    # HL internal (instant) — allowlisted destinations only

# Cross-chain bridge (auto-cheapest cctp/relay/debridge)
perp --json funds bridge quote --from solana --to arbitrum --amount 100
perp --json funds bridge send  --from solana --to arbitrum --amount 100
perp --json funds bridge status <orderId>                   # poll until success

# Inter-exchange rebalance
perp --json funds rebalance check
perp --json funds rebalance plan
perp --json --dry-run funds rebalance execute --auto-bridge   # status "simulated" (moves[].status "dry_run"), or "balanced" (nothing to move)
perp --json funds rebalance execute --auto-bridge             # withdraw → bridge ONLY; no deposit
```

Always run `funds bridge quote` before `funds bridge send` so the user sees fees + ETA.

- `funds rebalance execute` returns `ok:true` even when a move failed: check EVERY `moves[].status` (`withdrawn`, `bridged`, `same_chain`, `needs_bridge`, `withdraw_failed`, `bridge_failed`). It never deposits — after the bridge arrives, deposit manually (`funds deposit <venue> <amt>`).
- `funds transfer <amt> <addr>` (HL) and `funds withdraw hyperliquid --to <other address>` require the destination on the `settings withdraw.hyperliquid` allowlist (`POLICY_DENIED` otherwise). Only the user can set it, in an interactive terminal (`--json` / piped → `POLICY_DENIED`). NEVER try to set or change `withdraw.<venue>` yourself.
- HL withdraw goes over CCTP (native USDC); on Arbitrum a 0.2 USDC forwarding fee is deducted (an amount ≤ the fee → `SIZE_TOO_SMALL`).
- Bridges: exactly `--amount` leaves the wallet (fees come out of it); a deBridge `nativeFee` is shown separately and is paid in the source chain's native token. Solana-origin deBridge is refused (`NO_BRIDGE_ROUTE`) → `--provider cctp`. `--fast` = fast CCTP finality (higher fee).
- `funds bridge exchange --from <ex> --to <ex>` bridges the master wallet's OWN USDC between the venues' chains (pacifica → solana, lighter → arbitrum); it does NOT withdraw from / deposit into Pacifica or Lighter. Exception hyperliquid: `--from hyperliquid` spends HyperCore spot USDC, `--to hyperliquid` credits HyperCore perps. HyperCore → Solana is refused (`NO_BRIDGE_ROUTE`).

Relay swaps between assets (`--from-asset` / `--to-asset`, chains `robinhood`, `arbitrum`, `bsc`, `base`, destination `solana`): run `perp --json --dry-run funds bridge send ...` first — it prints the locally verified quote (amount in, expected out, protocol-guaranteed minimum, fees, ETA) and the min-out verdict without loading a key. Stable → native (e.g. USDG → SOL / ETH) needs `--min-out`. The recipient is always the master wallet's own address; an `ORDER_PENDING` result carries the Relay request id — never bridge again before checking it.

### Strategy engine (20 algorithms + scripted plans)

```bash
perp strategy list-strategies                                 # 20 registered
perp strategy run <strategy> [symbol]                         # run any strategy (multi-venue: --exchanges must include the -e venue)
perp --json --dry-run strategy run <strategy> [symbol]        # simulate: actions logged, never sent
perp strategy apex [symbol]                                   # APEX orchestrator
perp strategy reflect                                         # performance analysis
perp --json strategy plan validate <FILE>                     # validate scripted plan
perp --json strategy plan execute <FILE> --dry-run            # dry-run scripted plan
```

**Strategies:** `grid`, `dca`, `simple-mm`, `engine-mm`, `avellaneda-mm`, `regime-mm`, `grid-mm`, `liquidation-mm`, `momentum-breakout`, `mean-reversion`, `aggressive-taker`, `funding-arb`, `funding-arb-v2`, `funding-auto`, `basis-arb`, `spot-perp-arb`, `hedge-agent`, `rfq-agent`, `claude-agent`, `apex`.

Background daemon (tmux):

```bash
perp --json --dry-run arb auto --min-spread 30 --size 100     # simulate first (--background inherits --dry-run)
perp --json arb auto --min-spread 30 --size 100 --background
perp --json background list
perp --json background logs <id> -f
perp --json background stop <id> [--timeout 90]   # graceful: SIGINT, job cancels its orders, waits, reports what is left on the venue
```

`strategy funding-arb` is monitor-only unless `--auto-execute`. Bots: `equity` is `null` when a balance read fails — arb strategies then skip new entries and the bot stops after 10 consecutive unknown ticks; `ordersPlaced` counts orders sent, `fills` only venue-reported fills — a resting order is placed, not filled.

Background jobs inherit the parent's `-n`, `--dry-run`, `-e`, `--ows`, `-w`, `--no-agent`, `--dex`, and never receive key material (argv/env): they resolve credentials from the OWS vault / agent keystores / `~/.perp/.env` themselves. `--background` with `-k`, `--passphrase`, `--ows-key` or a shell-exported key / `OWS_PASSPHRASE` → `INVALID_PARAMS` — register an agent (`perp wallet agent approve <venue>`), which signs without the master passphrase.

### Position sizing & safety

- Single position notional < **80%** of that exchange's available balance.
- Leverage 1–3x for arb; never above 5x for arb positions.
- `arb exec` sizes the short to the verified long fill and always reconciles; still check `arb status` (`unconfirmedPairs`, `staleStateEntries`) afterwards.
- ALWAYS follow `longExch`/`shortExch` (perp-perp) or `longExchange`/`shortExchange` (`--rates` / `--compare`) — NEVER reverse direction. Spot-perp: only `direction == "long-spot-short-perp"`.
- NEVER enter if `netSpread <= 0` or `netSpread < estimated round-trip slippage`.
- Capital that's mid-bridge is "at risk" and unhedged — factor it in.

For deeper risk-management framework, read `references/strategies.md`.

## Examples

### Example 1: "Find funding-rate arb opportunities"

```bash
# 1. Discover
perp --json arb scan --min 10 --top 10
# 2. Show top 3 to user; ask which to evaluate
# 3. Check balances on the two exchanges
perp --json portfolio -e <longEx>
perp --json portfolio -e <shortEx>
# 4. Recommend size + dry-run
perp --json --dry-run arb exec BTC <longEx> <shortEx> 100
# 5. After user confirmation:
perp --json arb exec BTC <longEx> <shortEx> 100 --smart
perp --json arb status
```

### Example 2: "ETH spot+perp arb, $100"

```bash
perp --json arb scan --mode spot-perp --min 0       # ETH row must say direction "long-spot-short-perp"
perp --json --dry-run arb exec ETH spot:hl hl 100
# → show dry-run, ask confirmation
perp --json arb exec ETH spot:hl hl 100
perp --json arb status
# Later, to close both legs:
perp --json arb close ETH --spot-exch hl --perp-exch hl
```

### Example 3: "Long SOL 0.5 on Hyperliquid with 2x leverage"

```bash
perp --json -e hl trade check SOL buy 0.5 --leverage 2
perp --json --dry-run -e hl trade leverage SOL 2 --isolated
perp --json --dry-run -e hl trade buy SOL 0.5 --smart
# → show both dry-runs (isolated 2x + the order), ask confirmation; only then:
perp --json -e hl trade leverage SOL 2 --isolated
perp --json -e hl trade buy SOL 0.5 --smart
perp --json -e hl account positions
```

### Example 4: "Move 500 USDC from Pacifica to Hyperliquid"

```bash
perp --json --dry-run funds withdraw pacifica 500
perp --json funds bridge quote --from solana --to arbitrum --amount 500
# → show the withdraw plan + bridge fee / ETA, ask confirmation; only then:
perp --json funds withdraw pacifica 500
perp --json funds bridge send  --from solana --to arbitrum --amount 500
perp --json funds bridge status <orderId>             # poll until completed
perp --json funds deposit hyperliquid 500
```

`funds rebalance execute --auto-bridge` only withdraws and bridges — check every `moves[].status`, then deposit by hand (`funds deposit hyperliquid <amt>`) after the bridge arrives.

### Example 5: "Run a delta-neutral funding bot in background"

```bash
perp --json --dry-run arb auto --min-spread 30 --close-spread 5 --size 100 --max-positions 5
# → show the simulation, ask confirmation
perp --json arb auto --min-spread 30 --close-spread 5 --size 100 --max-positions 5 --background
perp --json background list
perp --json background logs <id> -f
# To stop:
perp --json background stop <id>
```

## Troubleshooting

Every response is `{ "ok": true, "data": ... }` or `{ "ok": false, "error": { "code": "...", "retryable": true|false, "remediation"?: "..." } }`; `ok:false` exits 1. Always check `ok` first and follow `error.remediation`. `retryable: true` → wait and retry ONCE, and only for read-only commands — a write is never blindly retried.

| Error code | Meaning | Action |
|---|---|---|
| `ORDER_PENDING` | A write was sent, outcome unknown | NEVER resubmit. See "Safety rules". |
| `ORDER_PARTIAL` | Part of a multi-leg / close succeeded | Don't retry; check positions per venue, close residuals by hand (may be quarantined). |
| `ORDER_REJECTED` / `ACTION_REJECTED` | Definitely not placed / not executed | Fix the cause from `error.message`; a new attempt is a new decision (ask the user). |
| `RISK_VIOLATION` | Local risk limit breached, or symbol quarantined | Report to the user. `--force` only with explicit user consent, and never bypasses quarantine. |
| `CAPABILITY_UNSUPPORTED` | Venue/feature combination not offered | Do NOT work around it (no emulation via other orders/venues); tell the user. |
| `INVALID_TICK` | Limit/trigger price off the venue grid (HL: ≤ 5 significant figures) | Refused, never rounded — re-price on the grid and confirm with the user. |
| `INVALID_PARAMS` | Bad argument (incl. strict sizes: `1,000` / `1e3` / `10abc` refused; `--dry-run` on a command without dry-run) | Fix the argument. |
| `CLI_ERROR` | Command parse error (unknown command / missing option) | Check `<cmd> --help`. |
| `NO_SIGNER_AVAILABLE` | No key that may sign this (e.g. imported agent key for a master-only action) | User does it on the website, or `perp wallet import`s the master. |
| `AGENT_NOT_REGISTERED` / `AGENT_EXPIRED` | Agent key missing, on the other network, or expired | Follow `remediation`: master on this computer → `perp wallet agent approve <venue> [--rotate]` (master-signed: user consent); imported key → new key on the website, `wallet agent import <venue> --replace`. |
| `POLICY_DENIED` | Local withdraw gate / OWS policy refused | Never change `withdraw.<venue>` — only the user can, in a terminal. |
| `PASSPHRASE_REQUIRED` | Vault passphrase needed | Ask the user to provide `OWS_PASSPHRASE` (or stdin); never put it on argv. |
| `LOCK_HELD` | Another perp process holds a state lock | Wait ~5s and retry once; check `background list`. |
| `NO_BRIDGE_ROUTE` | No supported bridge route (e.g. deBridge from Solana, HyperCore → Solana) | Use the route in `remediation` (e.g. `--provider cctp`). |
| `RATE_LIMITED` / `EXCHANGE_UNREACHABLE` | Throttled / API down (reads) | Wait 5–10s (or `retryAfterMs` when present — Pacifica sets it from its credit headers), retry once; then skip that venue. |
| `INSUFFICIENT_BALANCE` | Not enough collateral on that venue | Reduce size or move funds first (user-confirmed). |
| `SYMBOL_NOT_FOUND` | Not listed on this venue | `market list`. Don't add `-PERP`. |
| `SIZE_TOO_SMALL` | Below venue minimum (HL TWAP: $100 total) | Compute `size × price`; raise size (minimum table in Step 4). |
| `UNKNOWN` | Unclassified failure (the message matched no known code) | Read `error.message`. After a write: treat the outcome as unknown — check `account orders` / `account positions` / `portfolio` before anything else, never resubmit blindly; report to the user. |

Lighter / Lighter RH "account not found" (venue code `21100`): the address has no account on that venue / network — the user must fund (create) the account first, then `perp wallet agent approve lighter` (or `lighter-rh`).

`--client-id` (`trade market/buy/sell/limit`): an id already recorded in `~/.perp/client-ids.jsonl` (and not marked failed) returns `ok:true` with `data.duplicate: true` and sends nothing — local tracking only, not a venue check (it is NOT a `DUPLICATE_ORDER` error). Formats: Pacifica a full UUID, Hyperliquid `0x` + 32 hex; QFEX refuses `--client-id` (use `--auto-id`); `--smart` + client id → `CAPABILITY_UNSUPPORTED`.

## Safety rules

- **Unknown outcome (`ORDER_PENDING`) on ANY write** — orders, cancels, edits, leverage, withdraw / deposit / bridge / transfer: do NOT resubmit. Check `perp --json -e <ex> trade status c:<id> --symbol <S>` (the id in `remediation`), `account orders` / `account positions` / `portfolio`, and the tx hash / request id in `error.details` (`funds bridge status <id>` for bridges). Report to the user.
- **Quarantine**: an unknown or unhedged outcome (arb, bots, `trade close`, `trade multi`, `trade atomic`) quarantines the symbol — global per symbol, scoped by network. It blocks opening orders, `arb exec`, `arb auto` and bots (`RISK_VIOLATION`); reduce-only orders pass. List: `perp --json strategy quarantine`. Clear only after the USER has verified the positions on the venues: `perp --json strategy quarantine-clear <SYM>`. `arb close` on a quarantined symbol needs `--force`.
- **Risk gate**: `trade market / buy / sell / limit / split / market --split / scale-in / twap / multi / atomic / stop --no-reduce-only` check `~/.perp/risk.json` (`perp risk limits ...`); reduce-only is exempt. `--force` bypasses the limits (never quarantine) — only with explicit user consent.
- **Stops** (`trade stop`, `tpsl`) are reduce-only by default; `--no-reduce-only` is refused on ondo and qfex. `trade tpsl <SYM> long|short` = the OPEN position's side; legs are sized to the live position.
- **Dry-run is default-deny**: commands that cannot simulate refuse `--dry-run` with `INVALID_PARAMS` (e.g. `trade twap`, `trade multi`, `trade cancel-stop`, `trade cancel-twap`, `strategy start / preset / grid / dca / quick-* / funding-arb`, `wallet agent approve`, `wallet rotate`). Simulate bots with `perp --json --dry-run strategy run <strategy>` / `perp --json --dry-run arb auto`.
- **A dry-run is not a full venue check**: it validates arguments, the risk gate and quarantine, but some venue rules are enforced only on the live send — e.g. an off-grid limit price (`INVALID_TICK`) or `--no-reduce-only` on ondo / qfex (`CAPABILITY_UNSUPPORTED`). Those refusals happen before anything is sent.
- **`wallet rotate`** creates a new wallet and transfers assets, with no dry-run — only on the user's explicit request.

### Common mistakes

- **Forgetting `--json`** → output becomes unparseable human text. The very first thing to check when parsing fails.
- **Using legacy command names** — `arb rates`/`arb prices`/`arb dex`/`arb spot-exec`/`arb spot-close` are removed. Use `arb scan --rates|--gaps|--hip3` and `arb exec spot:<exch>` / `arb close <SYM> --spot-exch <ex>`.
- **Calling `trade check` without `--leverage`** → cost estimate doesn't match what the exchange applies.
- **Retrying a non-idempotent trade** without checking `account positions` → opens a duplicate position.
- **Bridging without quoting first** → user sees no fee/ETA and can't approve cleanly.
- **Treating `bridge send` as instant** → always `funds bridge status <orderId>` before depositing on the destination.
- **Manually adding `-PERP` suffix** → CLI auto-resolves; let it.

For a full troubleshooting + non-interactive flow guide, read `references/agent-operations.md`.

## Referrals (optional, ask once per setup)

```bash
perp --json --dry-run -e hyperliquid wallet manage referral set   # preview (nothing signed)
perp --json -e hyperliquid wallet manage referral set [code]      # signs + sends ONE referral action
perp --json -e lighter wallet manage referral set [code]          # Lighter (needs an agent key)
```

Referral codes are never applied implicitly (adapter creation signs nothing). When the user first sets up a wallet, ask:
> "perp-cli development is supported by optional referrals. Apply the referral code? It signs one referral action on the venue; no extra fees — only exchange rebates are used."

## Builder fees (OFF by default — never enable on your own)

Builder fees are extra fees on the USER's perp orders, paid to a third-party builder. perp-cli attaches none unless the user explicitly set `settings builder.<venue>` AND the venue approval is confirmed. Do not configure or approve a builder unless the user asks for it.

```bash
perp --json wallet builder status [venue]                 # support, config, approval, attaches?
perp --json --dry-run wallet builder approve <venue>      # plan only — show it to the user
perp --json wallet builder approve <venue> --yes          # only after explicit user consent (master-signed)
perp --json --no-builder -e <ex> trade market BTC buy 0.1   # one run without the fee
```

qfex: `builder.qfex <uuid>` is a fee share (no extra fee, no approval; mainnet only). Unsupported: lighter, lighter-rh, arcus (`CAPABILITY_UNSUPPORTED`). An order whose approval is missing or unknown is sent without the fee (`execution.notes`); `execution.builderFee` records what was attached.

## MCP Server

The package also ships a 30-tool MCP server (no API keys required for read-only market data — `get_markets`, `get_orderbook`, `get_funding_rates`, `get_prices`, `get_outcome_markets`, `get_outcome_view`, `get_outcome_book`, `get_option_expiries`, `get_option_chain`, `get_option_quote` (Derive options), the read-only Pacifica Print / vault tools `pacifica_print_products`, `pacifica_print_quote`, `pacifica_print_positions`, `pacifica_vaults`, plus 16 account/advisor tools, incl. keyless `get_positions_by_address`):

MCP `portfolio` totals (`totalEquity`, `totalAvailable`, `totalMarginUsed`, `totalUnrealizedPnl`, `riskMetrics.marginUtilization`) are `null` when no balance was read — check `accountState` (`"ok"` | `"unread"` = credentials but no balance read | `"noAccount"`) and `totalsCover` (the venues the totals include) before quoting a total. The CLI `portfolio` shape differs: `totals.{equity,marginUsed,marginPct,funding24h,fundingIncomplete}`, `risk.{level,marginPct}`.

MCP network: `PERP_NETWORK=mainnet|testnet` (validated; unset = mainnet); every result's `meta.network` says which. The only write tools, `trade_execute` / `trade_close`, run the same local risk gate as `perp trade` (no override over MCP), refuse non-reduce-only orders on quarantined symbols, and log every order.

```json
{
  "mcpServers": {
    "perp-cli": {
      "command": "npx",
      "args": ["-y", "-p", "perp-cli", "perp-mcp"]
    }
  }
}
```

**`perp-guardrail`** (third binary): not run by hand — the OWS Policy Engine spawns it before an agent API key signs anything; it allows / denies by chain + contract whitelist, per-tx and daily USD limits, withdrawal limits and blocked selectors. Set it up through `perp wallet setup` or `perp wallet policy create --perp-defaults`; it is a second line of defence, not a replacement for perp-cli's risk gate.

[![Glama MCP server](https://glama.ai/mcp/servers/hypurrquant/perp-cli/badges/score.svg)](https://glama.ai/mcp/servers/hypurrquant/perp-cli)
