# perp-cli Command Reference

All commands support `--json` for structured output. Always use `--json` when calling from an agent.

## Global Flags

`--json` (required for agents) | `-e <pac|hl|lt|aster>` (exchange) | `--dex <name>` (HIP-3) | `-w, --wallet <name>` | `--dry-run` | `--fields <f1,f2>` | `--ndjson`

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
perp --json market hip3                        # list HIP-3 deployed perp dexes (Hyperliquid)
```

## Account (read-only, safe)
```bash
perp --json -e <EX> account balance            # perp balance + spot holdings + 24h funding
perp --json -e <EX> account positions          # open positions
perp --json -e <EX> account orders             # open/pending orders
perp --json -e <EX> account history            # order history
perp --json -e <EX> account trades             # trade fill history
perp --json -e <EX> account funding-history    # funding payments
perp --json -e <EX> account settings           # per-market leverage & margin mode
perp --json -e <EX> account margin <SYMBOL>    # position margin info
perp --json -e <EX> account pnl                # realized + unrealized + funding
perp --json -e <EX> account twap-orders        # active TWAP orders
perp --json portfolio                          # cross-exchange unified view
perp --json portfolio --arb                    # full dashboard with arb top 5
```

## Trading (requires user confirmation)
```bash
# Market orders
perp --json -e <EX> trade market <SYMBOL> <buy|sell> <SIZE>
perp --json -e <EX> trade buy <SYMBOL> <SIZE>           # shorthand market buy
perp --json -e <EX> trade sell <SYMBOL> <SIZE>          # shorthand market sell
perp --json -e <EX> trade buy <SYM> <SIZE> --smart      # IOC limit at best ask (less slippage)

# Split execution (orderbook-aware, for large orders)
perp --json -e <EX> trade split <SYMBOL> <buy|sell> <USD>
perp --json -e <EX> trade split <SYM> buy 5000 --max-slippage 0.5 --max-slices 5 --delay 2000 --min-slice 200
perp --json -e <EX> trade market <SYM> buy <SIZE> --split   # split via flag

# Limit / stop / TPSL
perp --json -e <EX> trade limit <SYMBOL> <buy|sell> <PRICE> <SIZE>
perp --json -e <EX> trade stop <SYMBOL> <SIDE> <SIZE> <STOP_PRICE>
perp --json -e <EX> trade tpsl <SYMBOL> <SIDE> --tp <P> --sl <P>

# Order management
perp --json -e <EX> trade edit <SYMBOL> <ORDER_ID> <PRICE> <SIZE>
perp --json -e <EX> trade cancel <SYMBOL_OR_ORDER_ID> [orderId]
perp --json -e <EX> trade cancel-all
perp --json -e <EX> trade cancel-stop <SYMBOL> <STOP_ORDER_ID>
perp --json -e <EX> trade cancel-twap <SYMBOL> <TWAP_ORDER_ID>
perp --json -e <EX> trade status <ORDER_ID>             # check order state
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
perp --json -e <EX> trade scale-in <SYMBOL> <SIDE> --levels '<P1>:<SIZE>,<P2>:<SIZE>'
perp --json -e <EX> trade pnl-track                     # real-time PnL tracker
perp --json trade twap <SYMBOL> <SIDE> <SIZE> <DURATION>  # native TWAP order

# Spot helpers (Hyperliquid / Lighter)
perp --json -e <EX> trade spot-buy <SYMBOL> <SIZE>
perp --json -e <EX> trade spot-sell <SYMBOL> <SIZE>
perp --json -e <EX> trade spot-balance

# Multi-leg atomic execution
perp --json trade multi <legs...>
```

## Outcome Markets (Hyperliquid HIP-4)

Fully-collateralized binary/range contracts on Hyperliquid. **Quote token: USDH (NOT USDC)**. No leverage / no liquidation. Min order $10 USDH (price × size ≥ 10). Currently 1 live market on mainnet (BTC binary daily settling at 06:00 UTC).

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

# Place orders. ALWAYS dry-run first.
perp --json outcome buy  <outcome> <side> <usd> --dry-run
perp --json outcome sell <outcome> <side> <usd> --dry-run

# Live execution. --limit makes it GTC; without --limit it's IoC at top-of-book +/-5%.
perp --json outcome buy  <outcome> <side> <usd> [--limit <px>] [--tif gtc|ioc|alo]
perp --json outcome sell <outcome> <side> <usd> [--limit <px>] [--tif gtc|ioc|alo]

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

- **Min notional:** `price * size < 10 USDH` → `INVALID_PARAMS` with remediation. Enforced in dry-run too.
- **Encoded-side mismatch:** `outcome buy 2 #10` (where `#10` decodes to outcome=1) → `INVALID_PARAMS`, never silently routes to outcome 2.
- **Insufficient USDH:** pre-checked before order send → `INSUFFICIENT_BALANCE` with "bridge USDC→USDH" remediation. Resolves the user address through the OWS-stored agent meta when no master pk is configured.
- **Venue rejection:** HL returns HTTP 200 with `statuses[0].error` even when an order is rejected; the adapter throws `EXCHANGE_ERROR` so a "placed" success message never masks a failure.

### Agent workflow recommendation

```
1. perp --json outcome list                       # discover markets, parse description
2. perp --json outcome view <outcome>             # full snapshot: both books +
                                                  # underlying mark + gap vs target +
                                                  # implied probabilities + time to expiry
3. perp --json outcome buy <outcome> <side> <usd> --dry-run
                                                  # validate notional, get user approval
4. perp --json outcome buy <outcome> <side> <usd> [--limit <px>] [--tif ...]
                                                  # execute (only after explicit user OK)
5. perp --json outcome positions                  # confirm fill / monitor
```

`outcome view` replaces the old multi-call pattern (separate `book` + `market mid` lookups). One round-trip returns everything an agent needs to decide direction.

Settlement at `expiryMs` is venue-side: winning side → 1 USDH per share, losing → 0. Decide before expiry whether to self-close or let the venue settle.

## Funds (deposit, withdraw, transfer, bridge, rebalance)

All fund movement lives under `perp funds`.

### Exchange in/out
```bash
perp --json funds deposit pacifica <AMOUNT>
perp --json funds deposit hyperliquid <AMOUNT>
perp --json funds deposit lighter ethereum <AMOUNT>         # L1 direct (min 1 USDC)
perp --json funds deposit lighter cctp arbitrum <AMOUNT>    # CCTP (min 5 USDC)
perp --json funds deposit lighter info                      # all Lighter deposit routes
perp --json funds withdraw pacifica <AMOUNT>
perp --json funds withdraw hyperliquid <AMOUNT>
perp --json funds withdraw lighter <AMOUNT>
perp --json funds transfer <AMOUNT> <ADDRESS>               # HL internal transfer (instant)
perp --json funds info                                      # combined routes & limits
```

### Cross-chain bridge (multi-provider router: cctp / relay / debridge — auto-cheapest)
```bash
perp --json funds bridge chains                             # supported chains
perp --json funds bridge quote --from <CHAIN> --to <CHAIN> --amount <AMT>
perp --json funds bridge send --from <CHAIN> --to <CHAIN> --amount <AMT>
perp --json funds bridge send --from <CHAIN> --to <CHAIN> --amount <AMT> --provider cctp
perp --json funds bridge exchange --from <EX> --to <EX> --amount <AMT>   # between exchanges
perp --json funds bridge status <ORDER_ID>
```

### Inter-exchange rebalance (orchestrated withdraw → bridge → deposit)
```bash
perp --json funds rebalance check                            # balances across exchanges
perp --json funds rebalance plan                             # compute optimal moves
perp --json funds rebalance execute --auto-bridge            # withdraw → bridge → deposit
perp --json funds rebalance execute --withdraw-only          # only withdraw, manual rest
```

## Arbitrage

All scan modes are routed through `arb scan`. Legacy aliases (`arb rates`, `arb prices`, `arb dex`, `arb spot-exec`, `arb spot-close`) are removed.

```bash
# Scan (read-only, safe)
perp --json arb scan                                        # default --mode all (perp-perp + spot-perp)
perp --json arb scan --mode perp-perp --min 10              # perp-only with min annual %
perp --json arb scan --mode spot-perp --min 10              # spot+perp only
perp --json arb scan --rates                                # funding rates across exchanges
perp --json arb scan --basis [SYMBOL]                       # cross-exchange basis
perp --json arb scan --gaps                                 # cross-exchange price gaps
perp --json arb scan --hip3                                 # HIP-3 cross-dex spreads
perp --json arb scan --history [SYMBOL]                     # historical funding
perp --json arb scan --compare <SYMBOL>                     # compare a symbol across exchanges
perp --json arb scan --positions                            # position funding impact
perp --json arb scan --live --interval 60                   # continuous monitoring
perp --json arb scan --top 10 --hold-days 7 --bridge-cost 0 --size 100  # cost-aware filtering

# Execute (perp-perp or spot+perp via spot:<exch> prefix)
perp --json arb exec <SYM> <longEx> <shortEx> <USD>         # perp-perp dual-leg entry
perp --json arb exec <SYM> spot:hl hl <USD>                 # spot+perp via HL spot
perp --json arb exec <SYM> spot:lt pac <USD>                # spot+perp via LT spot
perp --json arb exec <SYM> <longEx> <shortEx> <USD> \
   --leverage 2 --isolated --smart --reconcile --max-slippage 0.5

# Close
perp --json arb close <SYM>                                  # close perp-perp arb
perp --json arb close <SYM> --pair <longEx>:<shortEx>       # disambiguate by pair
perp --json arb close <SYM> --spot-exch hl --perp-exch hl   # close spot+perp legs
perp --json arb close <SYM> --smart                         # IOC limits at best price

# Status / history / config / rebalance
perp --json arb status                                      # open arb positions + PnL + funding earned
perp --json arb status --period 7 --symbol BTC              # filter funding lookback / symbol
perp --json arb history                                     # alias: arb log
perp --json arb history --period 30                         # past arb trade performance
perp --json arb config                                      # show arb defaults
perp --json arb rebalance --check                           # cross-exchange balance distribution
perp --json arb rebalance --target 50:50 --amount 1000 --dry-run

# Auto-execute daemon
perp --json arb auto --min-spread 30 --close-spread 5 --size 100 --max-positions 5
perp --json arb auto --background                           # tmux session
perp --json arb auto --hip3 --min-oi 50000 --min-grade C    # HIP-3 mode
perp --json arb auto --dry-run                              # simulate
```

## Wallet Management
```bash
perp --json wallet generate evm                # generate EVM wallet
perp --json wallet generate solana             # generate Solana wallet
perp --json wallet import [privateKey]         # import an existing key
perp --json wallet set hl <KEY>                # set Hyperliquid key
perp --json wallet set pac <KEY>               # set Pacifica key
perp --json wallet set lt <KEY>                # set Lighter key (auto-generates API key)
perp --json wallet set aster <API_KEY>         # set Aster API key
perp --json wallet set hl <KEY> --default      # set + make default exchange
perp --json wallet show                        # public addresses for active wallet
perp --json wallet list                        # all named wallets
perp --json wallet use <name>                  # set active wallet
perp --json wallet rename <old> <new>
perp --json wallet remove <name>
perp --json wallet balance                     # on-chain USDC balances
perp --json wallet solana <address>            # check arbitrary Solana address
perp --json wallet arbitrum <address>          # check arbitrary Arbitrum address
perp --json wallet migrate                     # migrate legacy ~/.perp/.env config
perp --json wallet rotate                      # rotate keys + transfer assets
perp --json wallet backup                      # encrypted backup
perp --json wallet restore <file>              # restore from backup
perp --json wallet deposit <walletName>        # deposit prompt for a stored wallet
perp --json wallet setup                       # **interactive — DO NOT use from agent**
```

### Agent wallet (DEX-side delegation)
```bash
perp --json wallet agent approve <exchange> [--master <name>] [--api-key-index <n>]
perp --json wallet agent list [exchange]
perp --json wallet agent revoke <exchange> <agentName>
perp --json wallet agent rotate <exchange> [oldAgentName]
perp --json wallet agent verify [exchange] [agentName]
```

### Exchange settings (`wallet manage`)
```bash
perp --json wallet manage margin <SYMBOL> <cross|isolated>
perp --json wallet manage withdraw <amount> <address>          # generic on-exchange withdraw
perp --json wallet manage account-mode [standard|big-blocks]   # Hyperliquid only
perp --json wallet manage sub create <name>
perp --json wallet manage sub list
perp --json wallet manage sub transfer <from> <to> <amount>
perp --json wallet manage lake create <symbol> <amount>
perp --json wallet manage lake deposit <lakeId> <amount>
perp --json wallet manage lake withdraw <lakeId> <amount>
perp --json wallet manage builder approve <code> <maxFeeRate>
perp --json wallet manage builder revoke <code>
perp --json wallet manage builder list
perp --json wallet manage builder overview
perp --json wallet manage builder trades <code>
perp --json wallet manage builder leaderboard <code>
perp --json wallet manage builder update-fee <code> <feeRate>
perp --json wallet manage referral claim <code>               # Pacifica
perp --json wallet manage apikey create <name> <maxFeeRate>
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
perp --json risk health                        # health-check summary
perp --json risk liquidation-distance          # % distance from liquidation for ALL positions
perp --json risk limits                        # view current risk limits
perp --json risk limits --min-liq-distance 30 --max-leverage 5  # set risk limits
perp --json risk check --notional 1000 --leverage 3             # pre-trade risk check
```

## History (execution log + analytics)
```bash
perp --json history list                       # execution audit trail
perp --json history stats                      # aggregated execution stats
perp --json history positions                  # position lifetime tracking
perp --json history prune                      # purge old entries
perp --json history summary                    # trading performance summary
perp --json history pnl                        # P&L breakdown by exchange
perp --json history funding                    # funding payment aggregation
perp --json history report                     # full performance report (summary + pnl + funding)
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
perp --json strategy run <STRATEGY> [SYMBOL]                 # run any registered strategy
perp --json strategy run funding-auto                        # multi-exchange funding arb
perp --json strategy apex [SYMBOL]                           # APEX orchestrator
perp --json strategy reflect                                 # performance analysis
perp --json strategy preset-list
perp --json strategy preset <NAME> [SYMBOL]
perp --json strategy start <CONFIG.yaml>                     # YAML/JSON config-driven
perp --json strategy quick-grid <SYMBOL>
perp --json strategy quick-dca <SYMBOL> <SIDE> <AMOUNT> <INTERVAL>
perp --json strategy quick-arb
perp --json strategy delta-neutral
perp --json strategy twap <SYMBOL> <SIDE> <SIZE> <DURATION>
perp --json strategy grid <SYMBOL> --range <PCT> --grids <N> --size <USD>
perp --json strategy dca <SYMBOL> <SIDE> <AMOUNT> <INTERVAL>
perp --json strategy trailing-stop <SYMBOL>
perp --json strategy funding-arb                             # legacy alias for run funding-arb

# Scripted execution plans (one-shot multi-step)
perp --json strategy plan example
perp --json strategy plan validate <FILE>
perp --json strategy plan execute <FILE> --dry-run
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
perp --json background stop <ID>              # stop a job
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
perp --json alerts add <SYMBOL> <PCT>         # add alert rule
perp --json alerts add --all <PCT>            # alert for any symbol > N%
perp --json alerts list                       # list active rules
perp --json alerts remove <ID>                # remove a rule
perp alerts start [--background]              # run daemon (tmux for background)
perp alerts stop                              # stop background daemon
```

## Settings
```bash
perp --json settings show                     # show current CLI settings
perp --json settings set <key> <value>        # set a CLI default
perp --json settings referrals on|off         # toggle referral codes
perp --json settings fees show                # cached exchange fee table
perp --json settings fees sync                # refresh fee cache
perp --json settings env show                 # show ~/.perp/.env values
perp --json settings env set <name> <value>
perp --json settings env remove <name>
perp --json settings env path                 # config file path
```

## Init / Setup
```bash
perp init                                     # interactive — DO NOT use from agent
perp setup                                    # alias for init — DO NOT use from agent
```

Use `perp wallet set <ex> <key>` instead — non-interactive and agent-safe.
