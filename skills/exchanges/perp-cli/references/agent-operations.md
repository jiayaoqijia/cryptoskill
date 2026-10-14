# Agent Operations Guide

Complete reference for non-interactive CLI operations. Every command here is safe for agents — no prompts, no hangs.

## Interactive vs Non-Interactive Commands

### Avoid bare interactive forms (they prompt and will hang an agent):
```
perp setup                       # interactive wizard — asks questions via stdin
perp init                        # alias for setup
perp wallet setup                # one-click setup — passphrase prompt
```

### Agent-safe non-interactive variants:
```bash
# Setup wizard with explicit args (no prompts):
OWS_PASSPHRASE=<pp> perp --json [-n testnet] setup --non-interactive \
  (--wallet <existing-ows-wallet> | --wallet-name <new-name>) \
  [--venues <pacifica,hyperliquid,lighter,aster,lighter-rh,ondo,arcus,qfex>] \
  [--default-venue <venue>] \
  [--slippage-bps <n>] [--slippage <venue>=<bps> ...]
# Writes settings only. Agent registration signs with the master wallet — only with
# explicit user consent: add --approve-agents --yes (passphrase via OWS_PASSPHRASE;
# Ondo key id + secret as 2 stdin lines with --ondo-secret-stdin). A failed venue
# returns APPROVE_FAILED with per-venue results in error.details.result.agents.
# No master wallet on this machine: the user creates keys on the exchange websites and
# pipes them in — --import-agents <venues> --yes (one stdin line per venue in order; ondo
# 2 lines: key id, secret; qfex 2 lines: public key, secret) [--master-address <venue>=<addr>]
# (required for aster / pacifica / arcus) [--allow-unverified pacifica] (required for pacifica)
# [--qfex-account-id <uuid>] (required for qfex) [--lighter-account-index <n> --lighter-api-key-index <n>];
# omit --wallet. Imported keys trade only: deposit / withdraw / transfer / bridge / referral
# set / agent approve then fail with NO_SIGNER_AVAILABLE → the user does them on the website.

# wallet setup (one-click) only prompts for passphrase — set OWS_PASSPHRASE env to skip:
OWS_PASSPHRASE=<pp> perp --json wallet setup --name <name> --max-tx-usd <usd> --max-daily-usd <usd>
```

### ALWAYS use these (non-interactive, agent-safe):
```bash
printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set <exchange>   # import key (stdin) into OWS vault → active wallet
perp --json wallet generate evm             # generate EVM wallet
perp --json wallet generate solana          # generate Solana wallet
perp --json wallet show                     # check configured wallets
perp --json wallet list                     # list named wallets
perp --json wallet balance   # gas token + USDC/USDT per chain (Arbitrum, Ethereum, Base, BNB, Robinhood USDG, Solana); failed reads → balance null + error
perp --json portfolio -e <EX>               # per-exchange balance + positions (account balance was renamed in v0.12)
perp --json -e <EX> account positions       # open positions
perp --json -e <EX> market list             # available markets
perp --json -e <EX> trade market ...        # execute trade
perp --json -e <EX> trade buy ...           # alias for market buy
perp --json -e <EX> trade sell ...          # alias for market sell
perp --json risk status                     # risk assessment
perp --json risk liquidation-distance       # % from liquidation for all positions
perp --json risk limits [--max-position <usd> ...]   # view (no flags) / set risk limits
perp --json risk check --notional <$> --leverage <L>  # pre-trade risk check
```

**Rule: every command MUST include `--json`.** Without it, output is human-formatted and harder to parse.

## Zero to Trading: Complete Setup Flow

### Single Exchange Setup
```bash
# 1. Install
npm install -g perp-cli@latest
# or use npx -y perp-cli@latest as the prefix

# 2. Register wallet (user provides key — on stdin, never argv)
printf '%s' "$USER_PRIVATE_KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set hl

# 3. Verify
perp --json wallet show
# → check "ok": true and address appears

# 4. Check balance
perp --json portfolio -e hyperliquid
# → if balance is 0, tell user to deposit USDC

# 5. Ready to trade
perp --json -e hl market list
```

### Multi-Exchange Setup (for Funding Rate Arb)
To run arb, you need wallets on AT LEAST 2 exchanges. Each exchange needs:
- A wallet key in the OWS vault (EVM for HL / Lighter / Aster, Solana for Pacifica)
- USDC balance deposited on-exchange

```bash
# 1. Register wallets (any 2+ of: hl, pac, lt, aster). The active OWS wallet serves every
#    venue, so EVM + Solana venues need one multi-chain wallet (perp wallet generate <name>)
#    or two vault wallets selected per command with --ows <name>:
printf '%s' "$EVM_KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set hl --name evm
printf '%s' "$SOLANA_KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set pac --name sol   # now active; HL: --ows evm
perp --json wallet agent approve lighter     # Lighter trading key

# 2. Verify
perp --json wallet show

# 3. Check balances (each exchange holds its own balance)
perp --json portfolio -e hyperliquid
perp --json portfolio -e pacifica
perp --json portfolio -e lighter
perp --json portfolio -e aster

# 4. If one side needs funding, bridge USDC via funds bridge
perp --json funds bridge quote --from solana --to arbitrum --amount 500
# → show quote to user, get confirmation
perp --json funds bridge send --from solana --to arbitrum --amount 500
perp --json funds bridge status <orderId>     # wait for completion

# 5. Verify both sides have balance, then start arb
perp --json arb scan --min 5
```

### Lighter API Key Setup
Lighter uses a separate API key for trading. Two paths:

1. **No implicit registration**: setting a key (`wallet set lt`, env) never registers a Lighter API key — adapter creation signs nothing. Register explicitly with `perp wallet agent approve lighter`.
2. **Managed agent (recommended for long-running agents)**: `perp wallet agent approve lighter --master <wallet> --api-key-index <slot>` registers a per-agent slot with explicit expiry tracking + 3-tier signer routing.

Register / retry:
```bash
perp --json wallet agent approve lighter --master <wallet>
```

### Using the Same EVM Key for Multiple Exchanges
One EVM private key works for Hyperliquid, Lighter and Aster — `wallet set` imports it once as the active OWS wallet:
```bash
printf '%s' "$KEY" | OWS_PASSPHRASE=<pp> perp --json wallet set hl
```

## Wallet Key Types

| Venue (`-e` id \| aliases) | Settles on | Credentials |
|----------|-------|-----------|
| `pacifica` \| `pac` | Solana | Solana key (`wallet set pac`), or agent (`wallet agent approve/import pacifica`) |
| `hyperliquid` \| `hl` | HyperCore (deposit from Arbitrum) | EVM key, or API wallet agent |
| `lighter` \| `lt` | Ethereum (Lighter L2) | EVM master + API key (`wallet agent approve lighter` / `import`) |
| `lighter-rh` \| `lrh` \| `rh` | Robinhood Chain (USDG) | API key (`wallet agent approve lighter-rh` / `import`) |
| `aster` \| `ast` | BNB Chain / Arbitrum | EVM key, or API wallet agent |
| `ondo` \| `ondo-perps` | off-chain (USDC deposits from Arbitrum / Ethereum) | API key id + secret (stdin) |
| `arcus` | Robinhood Chain (USDG) | Ed25519 API key (`wallet agent approve arcus --master <w>` / `import`) |
| `qfex` \| `qf` | custodial (USDC on Arbitrum One) | website key, imported by the user only (`wallet agent import qfex`) |
| `risex` \| `rise` | RISE chain (USDC; deposit / withdraw in the RISEx app only) | EVM master + session signer registered and restricted to trading-only on-chain (`wallet agent approve risex --master <w>`; import refused) |
| `txflow` \| `txf` | — | none: MARKET DATA ONLY through an UNOFFICIAL API (every write → `CAPABILITY_UNSUPPORTED`) |

Default `-e` = `settings.defaultExchange`, else `pacifica` — always pass `-e`.

## Deposit & Withdraw Flows

### Check On-Chain vs Exchange Balance
```bash
perp --json wallet balance   # gas token + USDC/USDT per chain (Arbitrum, Ethereum, Base, BNB, Robinhood USDG, Solana); failed reads → balance null + error
perp --json portfolio -e hyperliquid     # USDC deposited on exchange
```

**On-chain balance ≠ exchange balance.** USDC in your wallet must be deposited to the exchange before trading.

### Deposit to Exchange (`funds deposit`)
```bash
# Hyperliquid (from Arbitrum wallet)
perp --json funds deposit hyperliquid 100

# Pacifica (from Solana wallet)
perp --json funds deposit pacifica 100

# Lighter (multiple routes)
perp --json funds deposit lighter info                # show all available routes
perp --json funds deposit lighter ethereum 100        # L1 direct (min 1 USDC)
perp --json funds deposit lighter cctp arbitrum 100   # via CCTP from Arbitrum (min 5 USDC)
```

RISEx: deposits are app-only (`funds deposit risex` → `CAPABILITY_UNSUPPORTED`, remediation app.rise.trade). Testnet: `perp --json -n testnet funds faucet risex`.

### Withdraw from Exchange (`funds withdraw`)
```bash
perp --json --dry-run funds withdraw hyperliquid 100   # plan first (every withdraw supports --dry-run)
perp --json funds withdraw hyperliquid 100 [--chain arbitrum|ethereum|base]   # CCTP to your own wallet
perp --json funds withdraw pacifica 100                # to your own Solana wallet
perp --json -e lighter funds withdraw lighter 100      # USDC → Ethereum (-e lighter-rh: USDG → Robinhood Chain)
```

### Internal Transfer (Hyperliquid)
```bash
perp --json funds transfer 100 <ADDRESS>     # instant HL→HL transfer
```

`funds transfer` and `funds withdraw hyperliquid --to <other address>` require the destination on the `settings withdraw.hyperliquid` allowlist (else `POLICY_DENIED`). That setting can be created / changed ONLY by the user in an interactive terminal (`--json` / piped → `POLICY_DENIED`, no `--yes`). Never try to set it; ask the user.

### Bridge Between Chains (`funds bridge`)
When you need to move USDC between chains (different networks):
```bash
# 1. Withdraw from source exchange to wallet
perp --json funds withdraw pacifica 500

# 2. Quote the bridge (auto-cheapest of cctp / relay / debridge)
perp --json funds bridge quote --from solana --to arbitrum --amount 500

# 3. Send (after user confirmation; pin --provider to override auto)
perp --json funds bridge send --from solana --to arbitrum --amount 500
perp --json funds bridge send --from solana --to arbitrum --amount 500 --provider cctp

# 4. Wait for completion
perp --json funds bridge status <orderId>

# 5. Deposit to destination exchange
perp --json funds deposit hyperliquid 500
```

### Inter-Exchange Rebalance (withdraw → bridge; deposit is manual)
```bash
perp --json funds rebalance check                        # current distribution
perp --json funds rebalance plan                         # compute optimal moves
perp --json --dry-run funds rebalance execute --auto-bridge   # status "simulated" or "balanced"
perp --json funds rebalance execute --auto-bridge        # withdraw → bridge only — NO deposit
perp --json funds rebalance execute --withdraw-only      # only withdraw, manual rest
```
The envelope is `ok:true` even when a move failed: check every `moves[].status` (`withdrawn`, `bridged`, `same_chain`, `needs_bridge`, `withdraw_failed`, `bridge_failed`). Deposit by hand (`funds deposit <venue> <amt>`) after `funds bridge status` confirms arrival.

## Order Types & Execution

### Market Orders (immediate execution)
```bash
perp --json -e hl trade market BTC buy 0.01       # market buy
perp --json -e hl trade market BTC sell 0.01      # market sell
perp --json -e hl trade buy BTC 0.01              # shorthand
perp --json -e hl trade sell BTC 0.01             # shorthand
perp --json -e hl trade buy BTC 0.01 --smart      # IOC limit at best ask (less slippage)
```

> **Risk gate:** `trade market / buy / sell / limit / split / market --split / scale-in /
> twap / multi / stop --no-reduce-only` enforce the local risk limits in `~/.perp/risk.json`
> (`maxPositionUsd` / `maxTotalExposureUsd` / `maxPositions`, set with `perp risk limits
> --max-position <usd> --max-exposure <usd> --max-positions <n>` or the `-pct` variants).
> A breach fails with `RISK_VIOLATION`, also in dry-run. `--force` overrides the limits —
> only with explicit user consent; it NEVER bypasses a quarantine (also `RISK_VIOLATION`).
> Reduce-only orders are exempt. Defaults are loose (`maxPositionUsd` 100000).

### Split Orders (orderbook-aware, for large orders)
```bash
perp --json -e hl trade split BTC buy 5000        # split $5000 into depth-based slices
perp --json -e hl trade split BTC sell 10000 --max-slippage 0.5 --max-slices 5
perp --json -e hl trade market BTC buy 0.5 --split   # split via market command flag
```
Returns `{ slices[], filledUsd, avgPrice, totalSlippagePct, status }`.
Status: `complete` (all filled), `partial` (some filled), `failed` (none filled).

### Limit / Stop / TPSL
```bash
perp --json -e hl trade limit BTC buy 60000 0.01     # buy 0.01 BTC at $60k
perp --json -e hl trade stop BTC sell 0.01 58000     # stop sell at $58k (reduce-only by default)
perp --json -e hl trade tpsl BTC long --tp 65000 --sl 58000   # long|short = the OPEN position's side
```

### Close / Reduce
```bash
perp --json -e hl trade close BTC                 # close entire position
perp --json -e hl trade close-all                 # close all positions on this exchange
perp --json -e hl trade flatten                   # cancel all orders + close all positions
perp --json -e hl trade reduce BTC 50             # reduce position by 50%
```

### Cancel Orders
```bash
perp --json -e hl account orders                  # list open orders
perp --json -e hl trade cancel BTC                # cancel by symbol
perp --json -e hl trade cancel <orderId>          # cancel specific order
perp --json -e hl trade cancel-all                # cancel all orders
perp --json -e pac trade cancel-stop BTC <stopId> # cancel stop order (pacifica / qfex; other venues: trade cancel)
perp --json -e hl trade cancel-twap BTC <twapId>  # cancel TWAP order
```

### Pre-Flight Validation
ALWAYS run before executing a trade:
```bash
perp --json -e hl trade check BTC buy 0.01 --leverage 3
```
Returns estimated fees, slippage, and whether the trade is within risk limits.

> **Important:** `trade check` does NOT read the exchange-set leverage. Always pass `--leverage` explicitly so the cost estimate matches what the exchange will apply.

## Parsing JSON Output

Every command returns this envelope:
```json
{
  "ok": true,
  "data": { ... },
  "meta": { "timestamp": "2026-05-02T..." }
}
```

Error case:
```json
{
  "ok": false,
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Not enough USDC",
    "retryable": false
  }
}
```

**Always check `ok` field first** (`ok:false` also exits 1). If `ok` is `false`, read `error.code` and follow `error.remediation`. If `error.retryable` is `true` AND the command is read-only, wait 5 seconds and retry once. Never retry a write — writes surface an unknown outcome as `ORDER_PENDING` (non-retryable).

In scripts, capture exactly one JSON document and read `.ok` — do NOT append a fallback (`$(perp … || echo '{"ok":false}')` yields two documents on failure):
```bash
out=$(perp --json -e hl account positions 2>/dev/null; true)
jq -e '.ok == true' >/dev/null <<<"$out" || echo "failed: $(jq -r '.error.code // "no output"' <<<"$out")"
```

## Idempotency & Safety

### Safe to retry (idempotent):
- `wallet show`, `wallet list`, `wallet balance` — read-only
- `portfolio`, `portfolio -e <ex>`, `account positions`, `account orders`, `account margin` — read-only (note: `account balance` was renamed to `portfolio` in v0.12)
- `market list`, `market mid`, `market book`, `market info`, `market funding` — read-only
- `arb scan` (any mode), `arb status`, `arb history`, `arb config` — read-only
- `portfolio`, `risk status`, `risk liquidation-distance` — read-only
- `funds bridge quote`, `funds bridge status`, `funds rebalance check`, `funds rebalance plan` — read-only
- `funds info`, `funds deposit lighter info` — read-only

### NOT safe to retry blindly:
- `trade market`, `trade buy`, `trade sell`, `trade limit`, `trade tpsl` — will open duplicate positions
- `trade close`, `trade close-all`, `trade flatten` — usually safe (no-op when nothing to close), but verify
- `funds bridge send` — will send duplicate transfers
- `funds deposit *`, `funds withdraw *`, `funds transfer` — will move funds twice
- `arb exec`, `arb close`, `arb auto` — open/close real positions
- `funds rebalance execute` — sends withdrawals / bridges

**For non-idempotent commands:** always verify the result before retrying. Check positions or balances to confirm whether the first attempt succeeded.

### Unknown outcome (`ORDER_PENDING`) — every write
Orders, cancels, edits, leverage, withdraw / deposit / bridge / transfer: `ORDER_PENDING` means the request was sent and its outcome is unknown. Do NOT resubmit. Check, in order: `perp --json -e <ex> trade status c:<id> --symbol <SYM>` (id from `remediation`), `account orders` / `account positions` / `portfolio`, the tx hash / request id in `error.details` (`funds bridge status <id>`). Unknown arb / bot / close / multi outcomes also quarantine the symbol (`perp --json strategy quarantine`); only the user clears it after verifying (`strategy quarantine-clear <SYM>`).

### Idempotency Key
`--client-id <id>` / `--auto-id` on `trade market/buy/sell/limit`. An id already recorded locally (`~/.perp/client-ids.jsonl`, not marked failed) returns `ok:true` with `data.duplicate: true` and sends nothing — this is local tracking, not a venue-side check and not an error. Formats: Pacifica a full UUID; Hyperliquid `0x` + 32 hex; Lighter / Lighter RH an integer; QFEX refuses `--client-id` (`CAPABILITY_UNSUPPORTED`; `--auto-id` works). `--client-id`/`--auto-id` with `--smart` → `CAPABILITY_UNSUPPORTED`.

## Symbol Naming Across Exchanges

Symbols are auto-resolved by the CLI. **Always use bare symbols** (e.g., `BTC`, `SOL`, `ICP`) — the CLI handles exchange-specific naming automatically:

| Input | Pacifica | Hyperliquid | Lighter | Aster |
|-------|----------|-------------|---------|-------|
| `ICP` | → `ICP` | → `ICP-PERP` | → `ICP` | → `ICP` |
| `BTC` | → `BTC` | → `BTC` | → `BTC` | → `BTC` |
| `SOL` | → `SOL` | → `SOL` | → `SOL` | → `SOL` |

- `arb scan` returns bare symbols — pass them directly to trade/leverage commands on any exchange.
- Do NOT manually add `-PERP` suffix — the CLI resolves this automatically.
- For HL spot+perp: BTC→`UBTC`, ETH→`UETH`, SOL→`USOL` are auto-resolved.

## Exchange-Specific Constraints

| Venue | Notes |
|-------|-------|
| Pacifica | client ids = full UUID; `cancel-stop` / native TWAP (seconds) |
| Hyperliquid | **$10** min order; prices ≤ 5 significant figures (off-grid → `INVALID_TICK`); native TWAP in minutes, min $100 |
| Lighter / Lighter RH | min varies by symbol (`market info`); `trade status c:<id>` needs `--symbol` |
| Aster | funding interval per symbol; `trade status c:<id>` needs `--symbol` |
| Ondo / Arcus | `trade status` needs `--symbol`; restricted-region notice on stderr |
| QFEX | `--client-id` refused; no resting reduce-only limits, opening stops or automation; funding unverified (display only) |

`--smart` only on pacifica / hyperliquid / lighter / aster. Stops are reduce-only by default; `--no-reduce-only` is refused on ondo / qfex. Limit and trigger prices off the venue grid are refused with `INVALID_TICK`, never rounded.

**`trade check` is advisory only** — it returns `valid: true/false` but does NOT block execution. The exchange itself enforces minimums and will reject with an error if the order is too small.

## Common Agent Mistakes

1. **Using `perp setup` / `perp init` / `perp wallet setup`** — interactive, will hang forever. Use `wallet set` (key on stdin) or `setup --non-interactive` instead.
2. **Forgetting `--json`** — output becomes unparseable human text.
3. **Trading with zero balance** — check `perp --json portfolio -e <ex>` first, tell user to deposit.
4. **Retrying a trade without checking** — leads to double positions. Always check `account positions` after a trade, even if it seemed to fail.
5. **Bridging without quoting** — always run `funds bridge quote` first to show the user fees and estimated time.
6. **Assuming deposit is instant** — after `funds bridge send`, wait for `funds bridge status` to confirm completion before depositing to the destination exchange.
7. **Manually adding `-PERP` suffix** — the CLI auto-resolves symbols. Just use bare names like `ICP`, `SOL`, `BTC`.
8. **Order below exchange minimum** — Hyperliquid requires $10+ notional. Compute `size × price` before submitting.
9. **Using legacy command names** — `arb rates`/`prices`/`dex`/`spot-exec`/`spot-close` are removed; use `arb scan --rates`/`--gaps`/`--hip3` and `arb exec spot:<exch>` / `arb close <SYM> --spot-exch <ex>` instead.
10. **Calling `trade check` without `--leverage`** — the CLI does not read exchange-set leverage, so cost estimates will be wrong.
11. **Resubmitting after `ORDER_PENDING`** — the first request may have executed. Check status / positions / tx first.
12. **Working around `CAPABILITY_UNSUPPORTED`** (another order type, venue or emulation) — report it to the user instead.
13. **`--dry-run` on a command without dry-run support** → `INVALID_PARAMS` (e.g. `trade twap`, `trade multi`, `strategy grid`, `wallet agent approve`). Simulate bots with `perp --json --dry-run strategy run <s>` or `perp --json --dry-run arb auto`.
14. **Omitting `-e`** — the default venue is `settings.defaultExchange`, else `pacifica`.
