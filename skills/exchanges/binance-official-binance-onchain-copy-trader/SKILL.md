---
name: binance-onchain-copy-trader
description: |
  Scaffold for assembling on-chain copy-trading strategies on Binance Agentic Wallet. Wires the
  existing capabilities — address monitoring, signal subscription, address scoring, token audit,
  order placement, on-chain take-profit/stop-loss — into one runnable pipeline, and exposes every
  strategy decision as a hook. Ships no strategy of its own.
  Trigger on: copy trade, copy trading, follow smart money, follow a wallet, mirror trades,
  copy-trade bot, auto-buy on signal, monitor a wallet and trade, smart money copy trading,
  signal-driven trading, pick addresses to copy, copy-trade strategy, copy-trade status,
  copy-trade post-mortem.
  NOT for: single manual trades (use binance-agentic-wallet), signal queries alone
  (binance-trading-signal), address analysis alone (binance-wallet-tracker / binance-leaderboard).
metadata:
  version: '0.6.0'
  requiredCliVersion: '1.9.1'
  requires:
    skills:
      - binance-agentic-wallet
      - binance-wallet-tracker
      - binance-leaderboard
      - binance-trading-signal
      - query-token-audit
---

# Binance On-Chain Copy Trader

A scaffold for a copy-trading pipeline. **This skill provides no strategy.** What it provides is:
a capability index, an event contract, an assembly structure, and three strategy hooks. The
strategy itself is yours to build and refine.

> ## Read this first
>
> **Every risk control, position-management scheme, and parameter value in this skill is a
> *suggestion* and an *example*. None of it is mandatory, and none of it constitutes a safety
> guarantee or investment advice.**
>
> - The scaffold guarantees only that **it will run the checks you configure**. It does not
>   guarantee those checks are sufficient to protect your funds. Budget caps, stop-loss distance,
>   liquidity floors — you choose all of them. Set them wide, leave them out, or switch off the
>   honeypot block, and the scaffold will do exactly as told.
> - The three bundled hooks are a **minimal reference implementation that proves the pipeline
>   runs**. They are not a recommended strategy and carry **no evidence of positive expectancy**.
>   Running them live as-is means funding an unvalidated strategy with real money.
> - On-chain transactions are irreversible. Any automated strategy can lose money through market
>   conditions you did not anticipate, changes in platform behavior, or defects in this scaffold.
>   **The risk is yours.**
> - Suggested path: run `dry-run` long enough to matter → read `events.jsonl` and build your own
>   baseline → switch to `live` with an amount you can afford to lose entirely → tune from there.

## Dependencies

Confirm the following skills are available in your current environment. This skill only
orchestrates; every underlying capability comes from them:

| Skill | Provides | Used here |
|---|---|---|
| `binance-agentic-wallet` | Wallet, market orders, limit orders, quota, chain info | `wallet` `market-order` `limit-order` |
| `binance-wallet-tracker` | Address monitoring, real-time push, group management | `tracker ws` `tracker token/tx` `tracker group/address` |
| ↳ | Must include the **Connection lifecycle** and **Signal field nullability** sections — this skill's connection-supervision split and its first-push field assumptions depend on them directly | — |
| `binance-leaderboard` | Trader rankings, address scoring, holder lookup | `leaderboard query/analyze/alpha-radar` |
| `binance-trading-signal` | Smart-money signals, custom strategies, backtests | `signal list` `signal strategy` `signal backtest` |
| `query-token-audit` | Token security audit | Audit HTTP endpoint |
| `query-token-info` | *(optional)* Live token price and market data | Only if a hook needs a live price when the event does not carry one |

Verify:

```bash
baw --version
baw cli-check --required-version "$(grep -m1 requiredCliVersion SKILL.md | tr -dc '0-9.')" --json
#   ↑ the frontmatter `requiredCliVersion` is the single source of truth for the version floor.
#     Below it, `tracker ws --duration 0` has no keepalive and no reconnect, and the scaffold
#     refuses to start.
```

Missing any one of them disables the corresponding stage: without `binance-leaderboard` there is
no systematic way to pick addresses; without `binance-trading-signal` you cannot create custom
signal strategies; without `query-token-audit` there is no audit data and `hard_gate` falls back
to `require_audit` to decide whether to pass or reject.

Install source: `https://github.com/binance/binance-skills-hub`

## Getting started

The order that takes you from nothing to a scored dry-run. Each step points at the section below.

**Note the ordering.** Writing the strategy comes *after* the first dry-run, not before. That is
deliberate: the whole premise of this scaffold is that thresholds should come from your own data,
and before the first run you have none. So the first pass runs the bundled reference hooks
unchanged — not because they are any good, but because they produce the dataset you need in order
to write something better.

**1 · Environment check** → see "Pre-flight checks"
Confirm the wallet is CONNECTED, the target chain supports both `market-order` and `limit-order`,
and that quote-token and gas balances are sufficient. On a chain where `limit-order` is
unavailable you cannot place on-chain protective orders — accept that before continuing.

**2 · Pick your trigger sources** → see "Trigger sources"
Address subscription, signal subscription, or both. This determines how you select sources next.

**3 · Select sources**
- Address source: `leaderboard query` for candidates → `leaderboard analyze` for the 6-dimension
  score on each (`follow_friendly` is the most relevant dimension here) → write addresses into
  `addrs.txt`, one per line, `#` for comments, **max 100**
- Signal source: `signal explore` to browse official strategies / `signal strategy create` to
  build your own / `signal strategy follow` to subscribe — or just use `--smy` and let the
  platform's own judgement drive it, with no configuration at all

The sort dimension materially changes the character of the candidate pool
(`--sort-by` 0=PnL 20=win rate 30=volume 50=trade count …), and individual dimensions can
saturate — over a short period, for instance, many addresses can tie at 100% win rate. Add your
own secondary criteria to break ties.

**4 · Write the config** → see "Configuration"
The first run writes an empty template to `$COPYTRADER_HOME` (default `~/.local/copytrader`) and
refuses to start until every required field is filled, listing exactly which are missing.
Mechanism parameters (budget / per-trade size / concurrency / gas floor) are separate from
`policy`, which is passed through to your hooks. **Leave `mode` as `dry-run`.**

The values here are decisions, not defaults to be guessed — `budget_usd` in particular should be
an amount whose total loss is acceptable, because that is the number you will be asked to
acknowledge at step 9.

**5 · Dry-run with the bundled hooks unchanged**
```bash
cd <skill-dir>/scripts && python3 copytrader.py
```
Do not edit the hooks yet. What ships filters almost nothing (direction and freshness only), which
makes it a poor strategy but a good instrument: it lets through a broad sample so you can see what
the stream actually contains before you start rejecting things.

**6 · Decide whether the plumbing works**
```bash
tail -f $COPYTRADER_HOME/copytrader.log
```
Check:
- the startup log's `sources` and `policy` match what you intended
- `events.jsonl` is being written, and the `decision` distribution is sane — are the rejection
  reasons the ones you wanted?
- passing events have values for `lag_s`, `tax`, `audit_risk`, `liquidity`, `price` — a missing
  value means some upstream call returned nothing
- `conn_seq` is not climbing fast (frequent reconnects mean an unstable stream)
- `outcomes.jsonl` starts filling in once the first horizon elapses
- `state.json`'s `deployed` stays at 0 under dry-run

This step is about the pipeline, not the strategy. Fix anything here before reading meaning into
the data.

**7 · Now write your strategy** → see "Strategy hooks" and "Scoring decisions without spending money"
With a dataset in hand, edit the three functions in the `══`-delimited block at the top of
`scripts/copytrader.py`: `should_enter` / `size_position` / `exit_plan`.

Join `events.jsonl` and `outcomes.jsonl` on `key` and let that decide your thresholds. Every gate
you add should be one you can point at in the data — and you should be able to see, in the
`decision` distribution, exactly what it rejected. Which parameters your hooks read is up to you;
put them in the `policy` section of `config.json` and they arrive verbatim.

**8 · Iterate**
Change hooks → re-run → score again. **This all works in dry-run**, which is the point: outcome
sampling does not need a fill, so a strategy can be evaluated from recorded data instead of from
real money. Accumulating a usable sample size is otherwise the expensive part.

Resist concluding early. A handful of scored decisions tells you nothing, and a mean carried by
one or two outliers tells you nothing either.

**9 · Switch to live**
Set `mode` to `live` **and** acknowledge the amount being risked — live mode refuses to start
until the acknowledgement file contains the current `budget_usd`:

```bash
echo <budget_usd> > $COPYTRADER_HOME/I_UNDERSTAND_THE_RISK
```

**The operator has to confirm the amount; an agent may write the file once they have.** What the
gate is for is that the decision was made, and made about this specific number — not that a human
typed the command. So the natural flow is: the agent states the budget and what a full loss of it
would mean, the operator confirms, the agent writes the file and starts the run.

Why the amount rather than a bare `touch`: it cannot be inherited by copying someone else's
runtime directory, the number has to come from whoever decided it, and **raising `budget_usd`
later invalidates the acknowledgement** — more money at risk deserves a fresh decision rather
than a stale one.

Before this point you should already have: run dry-run long enough to accumulate a meaningful
sample, scored those decisions from `outcomes.jsonl` rather than from intuition, and concluded
that losing `budget_usd` in full is acceptable.

**Dry-run does not record positions, so the budget and concurrency guardrails never fire — the
dry-run pass count will therefore be higher than the number of positions live would actually
open.** Do not size live from a dry-run pass rate.

## Capability map

Every stage of the pipeline maps to an existing capability. **The tables below are an index of
where to look; treat each skill's own documentation and `--help` as authoritative for parameters.**

### Source selection — pick addresses for the address source; pick or build strategies for the signal source

| Capability | Command | Returns | Key parameters |
|---|---|---|---|
| Trader ranking | `baw leaderboard query` | address · winRate · realizedPnl · realizedPnlPercent · totalVolume · totalTxCnt · buyTxCnt · tags · addressLabel | `-c` chain · `-p` 7d/30d/90d · `-t` ALL/KOL/MPC · `--sort-by` 0=PnL 20=win rate 30=volume 50=trades 60=activity 70=rate 80=token count · `--page` · `--size` (≤20) |
| Single-address score | `baw leaderboard analyze` | 6-dimension score (winrate / stability / drawdown / tags / pnl / **follow_friendly**) plus an AI archetype | `-c` · `-a` address · `-p` · `--top-n` (≤5000) |
| Reverse lookup by holding | `baw leaderboard alpha-radar` | Addresses holding a given token | `-c` · `-t` comma-separated token addresses · `-m` minimum hits · `-p` |
| Token-level monitoring | `baw tracker token` | Recent token activity | `-c` · `-g` group · `--tag-type` kol/smy · `--token-size` · `--period` 1m/5m/1h/4h/24h · `--filter-risk` |
| Trade-level monitoring | `baw tracker tx` | Individual trades | same as above |
| Followed addresses | `baw tracker follow` | The current follow list (read-only) | `-c` |
| Group management | `baw tracker group` / `address` | Create groups, bulk import, label, link | see wallet-tracker docs |

### Trigger sources — two peer real-time subscriptions

Both go through `baw tracker ws` and both are WebSocket push with latency of the same order.
The difference is **who decides what is worth looking at**: with the address source you name the
wallets; with the signal source the platform (or a strategy you built) decides. Run either alone
or both together (`sources: ["address","signal"]`).

#### A · Address subscription — you pick the wallets, it pushes every trade they make

| Command | Event semantics |
|---|---|
| `baw tracker ws --address-list <file> -c <chain>` | Every on-chain trade by the listed addresses, **max 100 addresses** |
| `baw tracker ws --address <addr> -c <chain>` | A single address |
| `baw tracker ws --following -c <chain>` | The current follow list; requires login, mutually exclusive with the other flags |

- **How to select**: `leaderboard query/analyze/alpha-radar`, plus `tracker group/address` to build groups
- **Event granularity**: one trade, one event; no re-pushes
- **Direction**: `tradeSideCategory` — buys `{11,19}`, sells `{21,29}`
- **Chains**: `-c` applies; single chain
- **Entry price**: the event carries `tokenPrice` (the counterparty's actual fill price)
- **Delivery latency**: measure it yourself. Expect a median on the order of seconds but a heavy
  tail (P90 can reach minutes). Record real latency from the event timestamp rather than assuming.

#### B · Signal subscription — the platform or your strategy decides, and pushes the verdict

| Command | Event semantics |
|---|---|
| `baw tracker ws --smy` | Smart-money signals (multi-address consensus). **All chains; `-c` has no effect** |
| `baw tracker ws --kol -c <chain>` | KOL-level events |
| `baw tracker ws --wallet BSC,SOL,BASE,ETH` | Chain-level wallet activity, comma-separated |

- **How to select**: `signal explore` to browse official strategies, `signal strategy create/follow`
  to build or subscribe to custom ones (meme-rush / fomo-call), `signal backtest` to backtest
- **Event granularity**: **the same `signalId` is pushed repeatedly with state updates** — on the
  order of tens to hundreds of pushes per signal. Deciding "this is a new signal" requires
  deduping by `signalId`
- **Signal-only fields**: `smartMoneyCount` (how many smart-money addresses agree) · `exitRate`
  (share already exited) · `maxGain` · `status`
- **`status` semantics**: `valid`/`active` live · `timeout` expired (one push at T+120min after
  the trigger) · `outDecline` · `exitRate`
- **Chains**: all-chain push; filter by `chainId` yourself
- **Entry price**: `currentPrice` (often `null`) or `alertPrice` (the historical price at trigger
  time — **not a currently tradable price**)
- **Delivery latency**: measure it yourself, and mind the methodology — you **must take the
  minimum lag per `signalId` and count only genuine first pushes**. Otherwise re-pushes turn "the
  signal's current age" into "latency" and the result comes out orders of magnitude too high.

#### Choosing between them

| | Address source | Signal source |
|---|---|---|
| Who decides what to watch | You (address selection) | Platform verdict / your custom strategy |
| Meaning of one event | One person's single trade | Consensus across several addresses |
| Coverage | Bounded by the 100-address cap | Platform-wide, all chains |
| Dedupe required | No | **Yes** (by `signalId`) |
| Timestamp field | `ts` | `signalTriggerTime` |
| Event density | Depends on how active your chosen addresses are, and how many | Depends on platform verdicts and is unevenly distributed across chains — subscribing to one chain may mean long stretches with no events |

Shared parameter: `--duration <sec>` (0 or omitted = unlimited). Each source occupies one reader
thread in the scaffold; events are normalized by `norm_address()` / `norm_signal()` and merged
into a single queue.

### Signal query and strategy management (REST, not push)

> The **real-time path for smart-money signals is `tracker ws --smy`** in the table above. This
> group is REST query and strategy management — for backfill, filtering, building custom
> strategies, and backtesting. It has nothing to do with latency.

| Capability | Command | Key parameters |
|---|---|---|
| Signal feed (backfill) | `baw signal list` | `-c` chain · `-s` all/user/meme/smart-money · `--time-range` 5m/1h/24h (filters on `signalTriggerTime`) · `--sort-by` time/maxGain · `-n` (≤100) |
| Custom strategies | `baw signal strategy create/update/delete/follow/unfollow/list/list-followed` | `-c` · `-t` meme-rush/fomo-call · `--job-id` · `--config` |
| Backtests | `baw signal backtest list/detail/retry/schedule` | `--interval` 4H/6H/12H/24H/OFF |
| Backtest credits | `baw signal credits` | — |
| Official strategy hall | `baw signal explore` | — |

`signal list` returns fields from the same source as `tracker ws --smy` pushes (`signalId` values
line up), but neither is a superset of the other.

### Risk control and execution

> The capabilities below are **available tools**. Whether and how you combine them is decided by
> your hooks and your config. This skill does not mandate any particular check — it only
> guarantees that the checks you asked for run at the right moment.

| Capability | Command / endpoint |
|---|---|
| Token audit | `POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit`, body `{binanceChainId, contractAddress, requestId}`. Returns `hasResult` `isSupported` `riskLevel` `extraInfo.buyTax/sellTax` `riskItems[].details[].isHit` |
| Market data | `GET .../buw/wallet/market/token/dynamic/info/ai?chainId=&contractAddress=` → `price` `liquidity` `holders` `volume24h` |
| Quote | `baw market-order quote --fromTokenQty --fromToken --toToken --binanceChainId --slippage` |
| Market order | `baw market-order swap` (same parameters plus `--mev` `--gasLevel`) → returns `orderId` |
| Order lookup | `baw market-order list` → `status` `toTokenActualQty` `txHash` |
| Limit order | `baw limit-order buy/sell --triggerPrice --fromTokenQty --fromToken --toToken --binanceChainId --slippage --mev --gasLevel` |
| Cancel / list | `baw limit-order cancel --strategyId` · `baw limit-order list` |
| Guardrail readings | `baw wallet balance` · `left-quota` · `tx-lock` · `settings` · `chains` |

## Event schema

Both sources are normalized by `norm_address()` / `norm_signal()` into one structure. Hooks only
ever see this:

```python
{
  "src":   "address" | "signal",
  "key":   dedupe key (address stream = txHash; signal stream = "sig:" + signalId),
  "ca":    token contract address,
  "token": token name,
  "price": entry reference price (address stream = counterparty fill price `tokenPrice`;
           signal stream = `currentPrice` or `alertPrice`),
  "ts":    event time (epoch seconds) — time.time() - ts is the delivery latency,
  "chain": chain ID,
  "side":  11/19 = buy, 21/29 = sell (always 11 on the signal stream),
  "who":   source identity (address stream = wallet label; signal stream = "SMY×N"),
  "usd":   USD size of the counterparty's trade,
  "risk":  tokenRiskLevel,
  "top10": top-10 holder concentration,
  "tags":  token tag array,
  "extra": source-specific fields
}
```

`extra` differs by source:

| Source | `extra` contents |
|---|---|
| address | `addr` |
| signal | `signalId` `status` `smy` (consensus count) `exitRate` `liq` `entry_liq` `holders` `is_alpha` `launch_ms` `mcap` `sig_seq` |

For the **full set of raw push fields** (including those dropped during normalization) see the
field tables in `binance-wallet-tracker`. Extend the `norm_*` functions to carry more of them
into `extra` when you need them.

### Signal stream: field availability on first push vs re-push

**Know this before you write any strategy.** `--smy` is a state stream, not an event stream — the
same `signalId` is pushed repeatedly throughout its lifetime, and **the first push and the
re-pushes carry different fields**. A strategy can only use fields that are present on the first
push, because the decision has to be made then.

The authoritative definition lives in the **Signal field nullability** section of
`binance-wallet-tracker/references/cli.md`. The table below is how that lands at the assembly
layer:

| Field | First push | Usable for an entry decision? |
|---|---|---|
| `signalId` `ticker` `chainId` `contractAddress` | carried | Yes |
| **`signalTriggerTime`** | **carried** | **Yes — compute delivery freshness from it** |
| `alertPrice` `alertMarketCap` | carried | Yes (but note: historical price at trigger time, not a tradable price) |
| `alertLiquidity` `entryLiquidity` | carried | Yes |
| `top10` `holders` `smartMoneyCount` `isAlpha` `launchTime` | carried | Yes |
| `status` | **usually `null`** | **No — see note 1** |
| `exitRate` `maxGain` `currentPrice` | **usually `null`** | **No — see note 2** |

Notes:

1. **A `status` gate may only reject explicit bad values; a missing value must pass.** `status` is
   usually `null` on the first push (the lifecycle states `timeout` / `outDecline` / `exitRate`
   are stamped on later pushes). Writing `if st not in ("valid","active")` silently drops almost
   every genuine first push, **and the symptom is indistinguishable from "there are no signals on
   this chain"**, which makes it very hard to diagnose. Correct form:

   ```python
   if st is not None and st not in ("valid", "active"):
       return False, f"status={st}"
   ```

2. **Do not use `exitRate` / `maxGain` / `currentPrice` as entry conditions.** They describe how a
   signal evolved *after* it fired; the server has not computed them at first-push time. A
   threshold gate on them never fires on a first push and only misjudges older signals you joined
   mid-life. Use them for exit logic or post-hoc correlation analysis instead — the fields are
   still written to `events.jsonl` in full.

3. **Do not place orders against `alertPrice` as if it were tradable.** It is the historical price
   at trigger time; combined with delivery latency, using it as a fill price books an order that
   cannot fill. This scaffold treats it purely as a **reference price handed to the hooks**, while
   protective-order triggers are always derived from the real entry price computed as
   `usd / actual filled quantity`. Keep the two apart. If a hook needs a live price, query market
   data (`query-token-info`) and skip when unavailable.

4. **You do not need a market-data call for liquidity** — `alertLiquidity` is present on the first
   push, and market data often has no index for newly launched tokens, making it less reliable
   than the event's own field. Also note the signal source already filters on liquidity, so
   **a liquidity floor on the signal stream is close to a no-op**; do not expect it to carry your
   filtering.

5. **Expired re-pushes must be caught by a freshness gate, not by `status`.** The `status=timeout`
   expiry notice always arrives at T+120min after the trigger; it carries `status` but its
   `signalTriggerTime` is old. The two gates back each other up: `status` catches explicit bad
   values, freshness catches anything stale in time.

## Assembly structure

```
ws_reader(source)          one thread per source; timestamps and enqueues only, never blocks
      ↓ queue
worker × N
      ↓
  norm_* ─────────────► normalized event `ev`
      ↓
  should_enter(ev, ctx)    ← hook ①  ctx.audit / liquidity are still None here
      ↓ pass
  gate_ok()                mechanism guardrails: budget / positions / gas / tx-lock / quota / STOP
      ↓
  audit() ∥ token_market()  fetch audit and market data concurrently, completing ctx
      ↓
  hard_gate(ctx)            mechanism-forced check: audit has a result + honeypot (configurable)
      ↓
  should_enter(ev, ctx)    ← hook ① again, now with audit and liquidity
      ↓ pass
  size_position(ev, ctx)   ← hook ②  returns a USD amount
      ↓
  market-order swap → actual_qty() reads toTokenActualQty from market-order list
      ↓
  exit_plan(ev, ctx, entry, qty) ← hook ③  returns [(trigger_price, qty, slippage), ...]
      ↓
  place_protection()        places limit-order sells in the returned order
      ↓
  reconcile()               periodic: once any protective order fills, re-place against the
                            actual remaining balance
```

### Why it is assembled this way

Three non-obvious choices in the pipeline, each resting on an interface contract. Confirm the
contract still holds before changing them:

| Choice | Contract it rests on |
|---|---|
| Filled quantity comes from `market-order list`, not from polling the wallet balance | `market-order swap` returns `orderId` and **neither a txHash nor a filled quantity**; the quantity is `toTokenActualQty` in `market-order list` |
| `exit_plan` can express a stop-loss | `limit-order sell` accepts a `triggerPrice` **below market** and stays `status: WORKING` rather than filling immediately |
| `ws_reader` **only restarts at the process level** | Connection-level care is built into `tracker ws --duration 0` (PING keepalive + auto-reconnect + backoff); the required CLI version is in the frontmatter's `requiredCliVersion`. The **Connection lifecycle** section of `binance-wallet-tracker` explicitly asks callers not to add a second layer — an outer rotation would kill a healthy connection, and an outer watchdog would abort a reconnect the CLI is already backing off for |

Two more choices affect how readings are interpreted: `ws_reader` records `conn_uptime_s` so
server-side delay can be told apart from post-reconnect replay; and the reader thread makes no
blocking calls, because otherwise processing time accumulates and inflates the arrival timestamps
of later events.

## Strategy hooks

> The three hooks are **where you write your strategy**. What ships in the repository is only an
> example that makes the pipeline run — every judgement and every threshold in it should be
> replaced by whatever your own analysis shows.

The three functions sit at the top of `scripts/copytrader.py`; the mechanism layer never touches
them. Signatures:

```python
should_enter(ev, ctx) -> (bool, reason)
size_position(ev, ctx) -> float            # USD; the mechanism layer then clamps to
                                           # min(value, position_usd, remaining budget)
exit_plan(ev, ctx, entry_price, qty) -> [(trigger_price, sell_qty, slippage_pct), ...]
```

`ctx` contents:

| Key | Meaning |
|---|---|
| `audit` | Raw audit response (`None` on the first hook call) |
| `liquidity` | Liquidity from market data (`None` on the first call; the signal stream can fall back to `extra.liq`) |
| `price` | Entry reference price |
| `positions` | Current positions dict |
| `deployed` | USD deployed so far |
| `cfg` | Full config |
| `policy` | The `policy` section of `config.json`, **passed through verbatim; the mechanism layer does not interpret its keys** |

`should_enter` is called **twice**: once **before spending anything on audit and market data**
(only the event's own fields are available), and once **after both are ready**. Put cheap
judgements in the first call and anything that needs audit data in the second.

Helper: `audit_tax(a)` pulls `buyTax + sellTax` out of an audit response.

## Mechanism guardrails

**Two different things.** *Running* a guardrail is the mechanism layer's job and hooks cannot get
around it; the *values and switches* are your decision.

| | Who decides | Note |
|---|---|---|
| When a check runs and who runs it | The scaffold | e.g. "check the budget before every entry" cannot be switched off |
| **What threshold a check uses, and whether it is enabled** | **You** | How large `budget_usd` is, whether `block_honeypot` stays on — the scaffold executes whatever the config says |
| What to buy, how much, and how to exit once a check passes | **Your hooks** | The mechanism layer only clamps ceilings; it does not pick instruments |

So what follows is a **suggested set of guardrails, not a safety guarantee**. A config with
`budget_usd: 1000000` and the honeypot block switched off will run perfectly happily.

### The guardrail list

| Item | Behavior |
|---|---|
| Budget | Cumulative deployment never exceeds `budget_usd`; `size_position`'s return value is clamped |
| Per trade | Never exceeds `position_usd` |
| Concurrency | Never exceeds `max_positions` |
| Gas | Stops opening when the native balance is below `gas_floor_native`; **also stops if the balance cannot be read** |
| Serialization | No orders while `tx-lock` reports LOCKED |
| Quota | No orders when `left-quota` is insufficient |
| Same token | A token already held is not opened again |
| Single instance | pidfile lock; a second start exits immediately |
| Gates | `STOP` halts new entries (existing protective orders are untouched); `KILL` exits the process |
| Mode | Under `mode: dry-run` no order request is issued at all |
| Live acknowledgement | `mode: live` refuses to start unless `$COPYTRADER_HOME/I_UNDERSTAND_THE_RISK` contains the current `budget_usd`. Cannot be inherited by copying a runtime directory, and raising the budget invalidates it |

**Switching `mode` from `dry-run` to `live` requires the operator's explicit decision about a
specific amount**, and the scaffold enforces that with the acknowledgement file above rather than
trusting a config edit alone. An agent may write the file after the operator confirms the amount.

### The connection-supervision split

**Connection-level care belongs to the CLI; process-level care belongs to this scaffold.** Do not
do both.

| Layer | Owner | What it does |
|---|---|---|
| Connection | **CLI** | `tracker ws --duration 0` has it built in: a 30s application-level PING, auto-reconnect and re-SUBSCRIBE on `onclose`, exponential backoff (reset on any received push) |
| Process | **This scaffold** | Restarts the child process only when it actually exits (fixed short delay, `proc_restart_sec`), and writes a `state["stream_alarm"]` |

Why they must not be stacked (the **Connection lifecycle** section of `binance-wallet-tracker`
states this explicitly):

- an outer "active rotation" periodically kills a connection the CLI was maintaining perfectly well
- an outer "silence watchdog" force-kills the child while the CLI is mid-backoff, aborting a pending reconnect
- two nested backoffs make the real reconnect interval unpredictable

`--duration N > 0` is **different semantics**: a single connection that rejects on disconnect and
does not reconnect. Use it for one-off sampling, never for a long-running process.

> **The version floor is hard.** Built-in keepalive is a precondition of this scaffold. Below the
> required CLI version, `--duration 0` has neither keepalive nor reconnect, and the scaffold no
> longer carries its own connection-level reconnect — running it anyway goes permanently silent
> after the first disconnect, **and that is indistinguishable from a quiet market**. The startup
> check verifies the version and refuses to run. The required version is the frontmatter's
> `requiredCliVersion`; `CLI_MIN` in the script matches it.

### Check liveness with the right field

`state["last_push_ms"]` is the liveness signal — every push updates it, re-pushes included.

**Do not use `last_event_ms`.** It is written after deduplication, so it only reflects whether a
**new** `signalId` arrived. Half an hour of quiet on the signal stream is entirely normal, and
using that field for liveness turns a normal quiet spell into a false outage.

### Profitable-exit bonus allowance (`state.bonus_slots`) — suggested, can be disabled

> This is **an example of one position-management idea**, not a recommendation. It assumes "a
> profitable exit shows the strategy works in current conditions, so exposure can grow" — an
> assumption that holds in a trending market and amplifies drawdown in a choppy one. If you do not
> want it, make `position_usd` an exact divisor of `budget_usd` and ignore the field.

Every exit that **settles at a profit** adds one `position_usd` slot of allowance:

```
position ceiling = max_positions + bonus_slots
capital ceiling  = budget_usd    + bonus_slots × position_usd
```

Losing exits add nothing. **Nothing is added when proceeds cannot be determined
(`proceeds is None`) either** — fail-closed: better to withhold allowance than to expand risk on a
guess. Proceeds are read from the on-chain receive amount of the filling transaction.

### Same-token cooldown (`policy.same_token_cooldown_h`) — suggested default 24, adjustable, can be disabled

Within the cooldown window, the same contract address is bought **only on the earliest signal**.
"Do I currently hold it?" is not enough on its own — once a position closes, later signals for the
same token would pass again (a single token can produce several distinct `signalId`s in a day).
The cooldown origin is recorded in `state.json.ca_last[ca]`, independent of position state.

## Configuration

`$COPYTRADER_HOME/config.json` (default `~/.local/copytrader`). The first run generates an
**entirely empty template**.

> **Resource guardrails and strategy parameters have no defaults — a missing one refuses startup.**
> Values like stop-loss distance and per-trade size have to be the result of your own decision,
> not something copied. A stop-loss distance you never thought about is exactly as dangerous as a
> position size you never thought about, so the scaffold would rather not start.
> The one exception is `mode`: absent means `dry-run`, so an omission can never turn into live
> trading.

**Required (mechanism layer)**

| Key | Meaning | How to decide it |
|---|---|---|
| `chain` | Chain ID | `baw wallet chains --json` for the currently supported set |
| `quote_token` | Quote-token contract address | A stablecoin on that chain; **must be lowercase** |
| `sources` | Trigger sources | `["address"]` / `["signal"]` / both |
| `budget_usd` | Cumulative deployment cap | No reinvestment; monotonically increasing. Decide whether losing all of it is acceptable |
| `position_usd` | Per-trade size | Together with stop-loss distance, this sets the worst case per trade |
| `max_positions` | Concurrent position cap | Bounds total exposure together with `budget_usd` |
| `gas_floor_native` | Native-token floor | Stops opening below this; **also stops if the balance cannot be read** |

**Required (strategy parameters, read by the reference hooks)**

The `policy` section is passed to hooks verbatim and the mechanism layer does not interpret its
keys — replace the hooks and this table changes with them. The reference implementation requires:

| Key | Meaning |
|---|---|
| `follow_sides` | Which `tradeSideCategory` values to follow on the address stream |
| `max_event_age_sec` | Delivery freshness ceiling, in seconds |
| `sl_mult` / `tp_mult` | Stop-loss / take-profit trigger = entry price × this |
| `tp_fraction` | Fraction of the position sold at take-profit |
| `buy_slippage` / `sl_slippage` / `tp_slippage` | Slippage tolerance per stage (%). **Stop-loss slippage should be wider than take-profit** — a stop that cannot fill during a crash is not protection |

**Has defaults (plumbing that does not affect capital safety)**

`mode` (`dry-run`) · `address_list` (`addrs.txt`) · `reconcile_sec` · `proc_restart_sec` ·
`workers` · `outcome_horizons_min` (`[5, 15, 60]`; set to `[]` to switch outcome sampling off)

**Optional**

`policy.block_honeypot` (default `true`; disabling it is not advised) · `policy.require_audit` ·
`policy.enrich_srcs` · `policy.same_token_cooldown_h` · `policy.min_liquidity_usd` ·
`policy.block_risk_levels` · `policy.max_sell_tax_pct` · `policy.max_commit_ratio`

Run `dry-run` for a while first and read the `decision` distribution in `events.jsonl` to confirm
what each gate is actually rejecting, before deciding whether to go `live`.

## Platform behavior notes

### What `cli-check` actually returns

In `baw cli-check --required-version X --json`, `success` **only reports that the command ran, and
is always `true`**. Whether the version passes is in `data.needUpdateCli`:

```json
{"success": true, "data": {"currentCliVersion": "x.y.z", "needUpdateCli": true}}
```

Treating `success` as "version is fine" makes the version gate useless: the command always
"succeeds", so the gate always passes. The correct test is `data.needUpdateCli === false`.

### Address casing is not consistent across chains

**Lowercase every contract address you pass to the CLI.** Chains differ in how strictly they
validate address format — some accept EIP-55 mixed case, others reject it outright:

```
[20003002] Invalid fromToken address
```

The difference is not documented, and the error points at "invalid address" rather than "wrong
format", which reads as though the wrong token were configured.

**The dangerous part is how it presents**: every order on that leg fails, and "never filling
anything" looks exactly like "this chain has no signals" in every liveness metric. Unless failed
orders are counted explicitly, this can hide for a long time. That is why `state["buy_fails"]`
and the most recent error belong in whatever reporting you build.

### Scoring decisions without spending money

`events.jsonl` alone cannot tell you whether a decision was any good — it records the decision,
not the result. So every decision that *would* have opened a position (dry-run included, where
nothing is bought) schedules price re-reads at `outcome_horizons_min` and appends them to
`outcomes.jsonl`:

```json
{"key":"sig:…","ca":"0x…","token":"…","src":"signal","horizon_min":15,
 "t0_ms":…,"entry":0.0123,"price":0.0141,"ret_pct":14.63,"sampled_ms":…}
```

Join on `key` to get one row per decision with its features and its forward return:

```bash
python3 - <<'EOF'
import json, collections
ev = {}
for l in open("events.jsonl"):
    r = json.loads(l)
    if r.get("decision") in ("DRY_RUN", "OPENED"): ev[r["key"]] = r
by = collections.defaultdict(dict)
for l in open("outcomes.jsonl"):
    o = json.loads(l)
    if o["key"] in ev and o.get("ret_pct") is not None:
        by[o["key"]][o["horizon_min"]] = o["ret_pct"]
print(f"{len(by)} scored decisions")
for h in sorted({h for d in by.values() for h in d}):
    v = sorted(d[h] for d in by.values() if h in d)
    if v:
        n = len(v)
        print(f"  {h:>3}min  n={n:<4} median {v[n//2]:+7.1f}%  "
              f"win rate {sum(1 for x in v if x > 0)/n*100:.0f}%")
EOF
```

From there, split by whatever feature you are testing (`liquidity`, `top10`, `tax`, `smy`,
`audit_risk`, token age from `launch_ms`, …) and compare the distributions.

**Read these numbers for what they are:**

- **They are marks, not fills.** No slippage, no fees, no token tax, no gas, and no check that the
  position could actually have been exited at that price. Treat them as an *upper bound* on what
  the strategy could have captured.
- **A horizon is an instant, not a path.** A `+40%` at 60 min does not mean a stop-loss was never
  touched on the way. Read several horizons together, and remember that a stop-loss between them
  changes the real outcome entirely.
- **Sample size still governs everything.** A handful of scored decisions tells you nothing, and
  if the mean is carried by one or two outliers it tells you nothing either. Look at the median
  and the distribution, not the average.
- Samples read very late (after an outage, say) are marked `sampled_late` rather than being
  quietly folded into the series.

### Build your own baseline; do not use someone else's numbers

The quantities below shift with platform changes, chain, token type, and time of day, so **any
hard-coded value goes stale**. The scaffold writes them all into `events.jsonl` /
`orders.jsonl` precisely so that you can measure your own baseline:

| What to measure | How | The trap in the measurement itself |
|---|---|---|
| Delivery latency | `lag_s` = arrival time − event time | **On the signal stream, take the minimum lag per `signalId` and count only genuine first pushes** (test: `lag` in the seconds range). Treating every re-push as an independent observation turns "the signal's current age" into latency and can be orders of magnitude off |
| Cause of latency | Use `conn_uptime_s` to separate "the server was slow" from "we just reconnected and got a replay" | Without that field there is no attribution, only a blended number |
| Execution time | Per-step timings in `latency_ms` | If the reader thread makes blocking calls, processing time accumulates into the measured latency of later events |
| Audit / market coverage | Distribution of `hasResult` and `px_src` | Newly launched tokens are often unindexed in market data; coverage correlates strongly with token age, so pooling all ages together is meaningless |
| Gas cost per trade | Native-balance delta across trades ÷ number of trades | Placing and cancelling limit orders also costs gas; counting only swaps understates the cost of a full position lifecycle |
| Predictive power of token-quality features | Correlate `top10` / `tags` / `liquidity` / `tax` / `audit_risk` in `events.jsonl` against outcomes | **Sample size.** A single-digit number of fills teaches you nothing about expectancy; if returns concentrate in one or two trades, the mean is meaningless |

> **Do not set token-quality thresholds by intuition.** Metrics like tax tags and top-10 holder
> concentration are distributed very differently on newly launched tokens than intuition suggests
> — a threshold set by feel rejects most legitimate candidates, and that over-rejection **looks
> exactly like "there are no signals"**, which makes it hard to notice. Log first, test second,
> gate last.

## Pre-flight checks

**Chain support, quote-token allowlists, and order quotas all change as the platform evolves — do
not rely on any hard-coded table.** Query current state before each start and let the results
define what is available:

```bash
baw wallet status --json                    # must be CONNECTED
baw wallet chains --json                    # which chains are supported right now
baw wallet settings --json                  # daily limit / tradeAllTokens / abnormalTxnHandling
baw wallet left-quota --json                # remaining quota today
baw wallet balance --binanceChainId <c> --json   # quote-token and native (gas) balances

# Does the target chain support what you need? Probe with a quote — it prices a route without
# placing anything on-chain.
baw market-order quote --fromTokenQty 1 --fromToken <quote> --toToken <any token> --binanceChainId <c> --json
baw limit-order list --binanceChainId <c> --json     # does the chain answer for limit orders at all
```

**Whether `limit-order` works decides whether you can place on-chain protective orders at all** —
on a chain without it, protection depends entirely on the process staying alive. Neither probe
above proves placement will succeed; the first real protective order does. Treat a chain as
unverified until you have seen one reach `WORKING`, and start there with the smallest position
size you are willing to hold unprotected.

Error codes: `1001001` chain or operation unsupported · `1001002` invalid parameters · `100`
server error (on a chain that is not wired up this can also surface as "no liquidity", so
distinguish it from `1001001`).

Commands and parameters for each dependency are authoritative in that skill's own docs and
`--help`; this document does not duplicate their capability tables.

## Running

```bash
cd <skill-dir>/scripts && python3 copytrader.py            # foreground
nohup python3 -u copytrader.py >> runner.log 2>&1 & disown  # long-running
```

| Action | Command |
|---|---|
| Stop opening new positions | `touch ~/.local/copytrader/STOP` |
| Exit the process | `touch ~/.local/copytrader/KILL` |
| Acknowledge the amount at risk (required before `mode: live` runs) | `echo <budget_usd> > ~/.local/copytrader/I_UNDERSTAND_THE_RISK` |
| Restore the live gate | `rm ~/.local/copytrader/I_UNDERSTAND_THE_RISK` |

Process exit **does not cancel protective orders already on-chain**; cancelling requires an
explicit `baw limit-order cancel`.

Data files (`~/.local/copytrader/`):

| File | Contents |
|---|---|
| `events.jsonl` | One line per event with the decision and all its inputs — **what the strategy decided** |
| `outcomes.jsonl` | Price re-reads at each horizon for every decision that would have opened — **whether the decision was any good**. Join to `events.jsonl` on `key` |
| `orders.jsonl` | Order / limit-order / cancel log |
| `state.json` | Positions, deployed capital, handled keys |
| `copytrader.log` | Chronological log |

Diagnostic fields in `events.jsonl`: `lag_s` (delivery latency) · `conn_uptime_s` (how long the
connection had been stable on arrival — **use this to separate server-side delay from
post-reconnect replay**) · `conn_seq` (which connection) · `replay` (event predates this
connection) · `latency_ms` (per-step timings) · `decision` (pass, or the rejection reason) ·
`tax` `audit_risk` `liquidity` `top10` `px_src`.

**The daemon has no external supervisor.** Configure your own liveness checks: is the process
alive; is `state.json.last_push_ms` advancing (**not `last_event_ms`** — it is written after
deduplication and only reflects new `signalId`s, and half an hour of quiet on the signal stream is
normal); how fast is `conn_seq` growing; is `baw wallet status` still CONNECTED; does the active
order count from `baw limit-order list` match the position count in `state.json`.

## Known limitations

These are **inherent properties** of the scaffold, not a to-do list. Make sure you accept them
before going live.

| Limitation | Detail |
|---|---|
| **No strategy edge whatsoever** | The three bundled hooks are a minimal reference implementation for proving the pipeline runs. **They are not a recommended strategy and carry no evidence of expectancy.** The strategy is your work |
| **Guardrails are not safety** | The scaffold runs the checks you configure; it does not judge whether they are sufficient. Set thresholds wide, or switch optional blocks off, and it will comply — **risk-control effectiveness depends on your values, not on this skill** |
| **Structurally behind** | Your fill is necessarily later than the party you copy (push latency + decision + order). If they are an issuer or have a private execution path, their gains are not reproducible while their losses are copied in full |
| **There is an unprotected window** | Time passes between the buy filling and the protective order being placed, bounded by settlement and API round-trips. The position has no downside protection in that window. It cannot be eliminated, only shortened |
| **Quantities drift after a partial fill** | Once any protective order partially fills, the remaining orders no longer match the remaining position. The reconcile thread re-places against the actual balance, but a process exit inside the reconcile interval leaves over-sized orders behind |
| **A stop-loss cannot save an illiquid token** | Being able to place an order is not the same as being able to fill it. A liquidity floor is the tool for that tail risk; a stop-loss is not |
| **Dry-run is not equivalent to live** | Dry-run records no positions, so budget and concurrency guardrails never fire and the pass count is necessarily higher than live would open. Do not estimate live fill frequency from a dry-run pass rate |
| **Process exit does not self-heal** | The scaffold restarts its child process when that exits; **the scaffold itself exiting has no external supervisor.** Configure process-level supervision yourself (launchd / systemd / container restart policy) |
| **Latency measures "platform record → delivery"** | The relationship between the event timestamp and on-chain block time is undefined. If the event time already lags the chain, true end-to-end latency is larger than what you measure |
| **Failed orders may consume daily quota** | Both consuming and not consuming have been observed. Not a constraint while the daily limit is generous, but do not assume failed orders are free when quota is tight |

## Disclaimer

**This is a scaffold, not a trading product, and it carries no strategy of its own.**

- The bundled hooks are a minimal reference implementation provided to demonstrate that the
  pipeline runs. They have **no evidence of positive expectancy** and are not a recommendation.
- Every risk control, position-management scheme and parameter value in this skill is a
  **suggestion**, not a safeguard. The scaffold runs the checks you configure; it does not judge
  whether those checks are sufficient, and it will comply with thresholds set arbitrarily wide or
  with optional protections switched off.
- **Nothing here is investment, financial, or trading advice.** No representation is made that any
  strategy assembled with this scaffold will be profitable or will avoid losses.
- On-chain transactions are **irreversible**. Automated trading can lose money through market
  conditions you did not anticipate, changes in platform or protocol behavior, defects in this
  software, or defects in the strategy you write. Copy trading is additionally disadvantaged by
  construction: your fill is always later than the party you copy, and if they are an issuer or
  hold a private execution path, their gains are not reproducible while their losses are.
- This software is provided **as-is, without warranty of any kind**, express or implied. To the
  maximum extent permitted by law, no liability is accepted for any loss or damage arising from
  its use.
- **You are solely responsible** for what you run, for the parameters you choose, for complying
  with the laws and regulations that apply to you, and for any funds you commit.

If you are not prepared to lose the full amount you configure as `budget_usd`, do not switch
`mode` to `live`.
