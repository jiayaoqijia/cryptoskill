---
name: binance-prediction-updown
description: |
  Scaffold for assembling prediction-market strategies on Binance Agentic Wallet, for recurring
  BTC Up/Down rounds. Wires round enumeration, market screening, two-step ordering, fill and
  settlement confirmation and redemption into one runnable pipeline, and exposes every probability
  judgement as a hook. Ships no strategy of its own.
  Trigger on: up down prediction, BTC up or down, prediction market bot, hourly prediction rounds,
  trade up/down automatically, prediction market strategy, prediction calibration, redeem winnings
  automatically.
  NOT for: single manual predictions (use binance-agentic-wallet), on-chain token copy trading
  (binance-onchain-copy-trader), signal queries (binance-trading-signal).
metadata:
  version: '0.1.0'
  requiredCliVersion: '1.9.1'
  requires:
    skills:
      - binance-agentic-wallet
---

# Binance Prediction Up/Down

A scaffold for trading recurring BTC Up/Down rounds: a round scheduler, screening gates, a
decision contract that compares your probability against the quote, order and settlement
handling, redemption, and two offline evaluation harnesses.

> ## Read this first
>
> **Every risk control, stake size and threshold here is a *suggestion*, not a safeguard.**
>
> - **This skill ships no strategy.** The bundled hook is an example that makes the pipeline run;
>   the numbers it reads are ones you measure and supply. The reference signal documented under
>   "Strategy hooks" nets roughly +0.65% per round against a ±1.9pp error bar — a worked example
>   of the bar, not a configuration to copy.
> - **A hit rate is not an edge.** If the market already prices the state your signal keys on,
>   a 58% hit rate earns zero. Only step 3 of the walkthrough can rule that out.
> - Positions can expire worthless; max loss per round is the stake. There is no stop-loss to
>   place — the position resolves itself.

## Dependencies

| Skill | Used for |
|---|---|
| `binance-agentic-wallet` | `prediction *`, `wallet *` |

Candles come from the public Binance market-data endpoint (`api/v3/klines`) — no key, no session.

```bash
baw --version
baw cli-check --required-version "$(grep -m1 requiredCliVersion SKILL.md | tr -dc '0-9.')" --json
```

> **Not published.** This skill lives only where you installed it. `binance-agentic-wallet` comes
> from `https://github.com/binance/binance-skills-hub`; this one does not ship from there yet.

## Getting started

Steps 1 and 3 cost nothing and either can kill the idea. Do both before live mode.

**1 · Backtest offline** — no login, no config, no money.
```bash
python3 backtest.py fetch --symbol BTCUSDT --interval 1h
python3 backtest.py eval  --interval 1h --hurdle 0.521
```
Use the interval of the rounds you will trade (`5m`/`15m`/`1h`/`1d`) — the same signal measures
very differently across them. `eval` prints a `hit_table` to paste into the config.

**2 · Write the config** — the first run writes an empty template and exits.
```bash
python3 updown.py                        # writes the template
$EDITOR $UPDOWN_HOME/config.json         # mode: dry-run, expected_slippage_bps: 0
```

**3 · Collect quotes, then test whether the signal is already priced in.**
```bash
python3 updown.py                        # dry-run: decides and records, places nothing
python3 backtest.py pricedin             # reads it back
```
```
 streak  dir     n  implied P(up)  realized P(up)     gap   read as
      3    1    64          0.421           0.428  +0.007   PRICED IN — no edge here
```
A gap near zero where your signal fires means the market already knows — **stop there**. Needs a
few dozen occurrences: at `1h` with `min_streak` 3 that is several days.

**4 · Check the plumbing** — `tail -f $UPDOWN_HOME/updown.log`. Expect long stretches of nothing;
the `HEARTBEAT` tally, not the absence of orders, is how you tell working from stuck.

**5 · Write your own hook** — `rounds.jsonl` has probability, both asks, overround, breakeven and
edge per round.

**6 · Go live** — minimum stake until the money path proves itself, then set
`expected_slippage_bps` from the `ALL-IN` lines your fills log.

## Capability map

| Stage | Command |
|---|---|
| Enumerate rounds | `prediction market list --l1Category crypto --l2Category up-down` |
| Book / last price | `prediction market order-book` · `market last-trade-price` |
| Price, place, cancel | `prediction trade quote` · `place-order` · `cancel` |
| Positions, settlement | `prediction position list` · `settled-history` · `pnl` |
| Redeem | `prediction trade redeem` |
| Order status | `prediction order history` |
| Guardrail reads | `wallet balance` · `left-quota` · `settings` |

## Round lifecycle

Twelve topics are listed at any time — **three symbols × four cadences** (`5 min`, `15 min`,
`1 hour`, `daily`), each with its own book, fee and price feed. `symbol` and `timeframe` are
required config; one daemon trades exactly one combination.

```
enumerate → gates → probability hook (cannot see quotes) → compare to quote
  → guards → quote → place → confirm fill → settlement → redeem
```

Two differences from a spot pipeline:

- **No stop-loss and no exit plan.** The position resolves itself; the whole decision is at entry.
- **Winning does not pay you.** Payouts sit in `PENDING_CLAIM` until redeemed. The daemon sweeps
  on a timer; `PENDING_CLAIM` should be empty in steady state.

### Which feed settles your round

| Cadence | Feed |
|---|---|
| 5 min, 15 min | `CHAINLINK` |
| 1 hour, daily | `BINANCE` spot |

Published per topic as `variantData.priceFeedProvider` — **read it, do not assume**. It decides
which series your backtest must use. The topic also publishes `startPrice`, so an outcome can be
checked independently once the round closes.

## Decision contract

**The quote is the implied probability.** Three branches, and the third is the common one:

| Branch | Condition |
|---|---|
| Buy Up | `P(up) − up_ask − cost > edge_threshold` |
| Buy Down | `(1 − P(up)) − down_ask − cost > edge_threshold` |
| **No trade** | everything else |

Breakeven hit rate is the quoted price plus costs — buying Up at 0.55 with a 2% fee needs better
than 57%. Computed and logged every round by the mechanism layer, not left to the strategy.

**Cost = topic `feeRateBps` + `expected_slippage_bps`.** The order's `slippage_bps` is a
*tolerance*, not a cost; charging it taxes every round for a worst case that rarely happens.

### Screening gates

Three hard gates run in the mechanism layer, before the hook is consulted:

| # | Gate | Source |
|---|---|---|
| 1 | **Overround** `up_ask + dn_ask − 1` | `market order-book` |
| 2 | Spread per side | same |
| 3 | Time to close | topic `endDate` |

Gate 1 does the most work: an observable fact about the book rather than a forecast. Measured
live on one BTC 1-hour round: asks 0.55 / 0.46 → **overround 1.0%**, spread 0.01 — and **3.0% on
the same round 22 seconds later**. Screen immediately before ordering.

A fourth check runs at sizing rather than screening, because it depends on the stake:

| Check | Behaviour |
|---|---|
| **Depth at the best ask** | The order is refused if the stake exceeds the USDT resting at the top of the book. The screen was done against that price; an order larger than it walks into worse prices and the number the decision was made on stops being the number that fills. **$5 at the best ask has been observed** — size against the book, not the budget |

Fair-value deviation and "breakeven ≤ demonstrated calibration" are **your hook's job**, not the
mechanism layer's: both depend on a model the scaffold does not have. They are listed here so the
division is explicit, not because the daemon enforces them.

Thresholds ship unset. A number from someone else's venue describes their book.

### Two kinds of market

| Type | Fair value | Consequence |
|---|---|---|
| At-the-money | naturally ≈0.50 | **No model edge.** Only mispricing of that 0.50 |
| Strike or band | computable from time and volatility | Deviation is measurable; tails are where crowds err |

## Strategy hooks

```python
estimate_probability(rnd, ctx) -> float | None   # P(round closes UP); None skips
size_position(rnd, ctx, edge)  -> float          # USD; clamped to stake_usd and budget
```

`ctx` carries `cfg`, `policy` (verbatim), `streak`, `streak_dir`, `open`, `now_ms`.

> **`ctx` contains no quote, deliberately.** An estimator that can see the price anchors on it,
> and the calibration report then measures something that looks accurate while holding no edge.
> Enforced at the interface, not left to discipline. Out-of-range or non-numeric returns are
> rejected with an `ALERT`, not clamped.

### What ships, and what is known about the signal it reads

> The hook is **where you write your strategy**. What ships is an example that makes the pipeline
> run — every judgement and every number in it should be replaced by what your own analysis shows.

The bundled implementation reads one mechanical feature — how long the current run of
same-direction candles is — and looks the answer up in **`policy.hit_table`, which you supply**.
It ships with no numbers, because a table describes one symbol at one cadence and borrowing one
describes nothing. `backtest.py eval --interval <iv>` prints a table ready to paste.

For reference, the same family measured on the settlement series at every listed cadence:

| Candle | streak 2 | 3 | 4 | 5 | monotonic? |
|---|---|---|---|---|---|
| 5m (n≈9.8k) | 0.520 | 0.509 | 0.512 | 0.514 | no |
| 15m (n≈9.6k) | 0.536 | 0.538 | 0.544 | 0.540 | no |
| 1h (n≈5.8k) | 0.539 | 0.544 | 0.552 | 0.559 | yes |
| 1d (n≈1.6k) | 0.538 | 0.531 | 0.536 | 0.535 | no |

- A **broad reversal tendency of ~+3pp** is present at 15m, 1h and 1d. That replicates.
- **"Longer streak, stronger reversal" does not** — it appears in one cadence out of four and
  shifts with the sample window. One in four is what noise looks like.

Net of measured costs, at `streak ≥ 3` on an at-the-money round:

| | |
|---|---|
| hit rate | 0.544 |
| − fair value | −0.500 |
| − overround, one side | −0.005 |
| − fee, 200 bps | −0.020 |
| − slippage observed on a fill | −0.0125 |
| **net per round** | **+0.0065** |

The error bar on the hit rate is **±0.019 — 2.9× the edge**. Telling +0.65% from zero needs about
**22,700 rounds**: 11.5 years at `min_streak` 3. That is neither "it loses money" nor "it makes
money" — it is **unverifiable at the rate these rounds occur**, and every figure assumes the round
is quoted at fair value, which step 3 of the walkthrough exists to check.

**Treat the table above as a worked example of the bar, not as a configuration to copy.**

### What `budget_usd` does and does not cap

It caps **loss**, not turnover. A round is allowed only while

```
realised losses  +  capital currently at risk  +  this stake   ≤   budget_usd
```

so the worst case — every open round settling to zero — still lands inside the number you
acknowledged. Winning stakes return to the pool and the daemon keeps going.

This matters for long runs. An earlier build treated the figure as cumulative turnover and never
released it at settlement, which stopped a `$50` budget at `$1` stakes after **50 rounds whatever
the outcome** — a halt unrelated to risk, and incompatible with the sample sizes this strategy
family needs. If you want to stop after a fixed number of rounds, use `max_rounds_per_day`.

## Mechanism guardrails

Enforced here; hooks cannot bypass them. Values are yours.

| Guard | Behaviour |
|---|---|
| `budget_usd` | **Cap on total loss**, enforced as `realised losses + capital currently at risk ≤ budget_usd`. The stake is released back when a round settles, so the gate tracks risk rather than turnover |
| `stake_usd` | Per-round cap, after the sizing hook. Floor is **1 USDT** (platform minimum) |
| `max_open_rounds` | Concurrent unsettled rounds |
| `max_rounds_per_day` | Resets at UTC midnight — the real cost control at this cadence |
| `max_consecutive_losses` | Halts new entries, records the reason |
| Single instance | `flock`, released by the kernel if the holder dies |
| Live gate | Refuses to start unless the ack file holds the current `budget_usd` |
| `STOP` / `KILL` | Stop opening / exit |

## Configuration

`$UPDOWN_HOME/config.json` (default `~/.local/updown`). First run writes an **empty template**.

> **Nothing that touches capital has a default.** The one exception is `mode` — absent means
> `dry-run`, so an omission cannot become live trading.

**Required (mechanism)**

| Key | How to decide it |
|---|---|
| `chain` | `baw wallet chains --json` |
| `symbol` | `BTCUSDT` / `ETHUSDT` / `BNBUSDT` |
| `timeframe` | `5 min` / `15 min` / `1 hour` / `daily` — exact strings; a typo is rejected at startup with the live catalogue |
| `budget_usd` | An amount whose total loss is acceptable. Enforced literally: a round opens only if losing it, plus everything already lost and everything currently at risk, still fits inside this number. You type it again to go live |
| `stake_usd` | ≥ 1 USDT, and under the size resting at the best ask |
| `max_open_rounds` | 1 until the money path is proven on your account |
| `max_rounds_per_day` | A cadence control, independent of the budget. At 2% a round, this is what bounds fees on a quiet strategy — it is not derived from `budget_usd` |
| `max_consecutive_losses` | At ~55%, four in a row is unremarkable |

**Required (policy — read by the bundled hook)**

| Key | How to decide it |
|---|---|
| `min_streak` | 4+ fires rarely but measures strongest; 2 fires often and measures weakest |
| `edge_threshold` | Above the uncertainty in your own hit-rate estimate, or you trade noise |
| `max_overround` | Watch the book for an hour first. Observed 1%–3% minutes apart |
| `max_spread` | Same method. Observed 0.01 on liquid BTC rounds |
| `min_seconds_to_close` / `max_seconds_to_close` | Market orders near settlement have failed outright. Leave room |
| `slippage_bps` | Order **tolerance**, not a cost |
| `hit_table` | `{"2": 0.53, "3": 0.54, …}` for **the cadence you trade**, from `backtest.py eval --interval <iv>`. No default — a borrowed table describes nothing |
| `expected_slippage_bps` | **Start at 0**, run the minimum stake, read the `ALL-IN … = +N bps` each fill logs, subtract the fee, set what you saw. One fill: +325 bps all-in against a 200 bps fee |

**Optional** — `kline_interval` (defaults to the round's cadence) · anything else your hook reads

**Has defaults (plumbing)** — `mode` · `poll_sec` · `settle_poll_sec` · `kline_refresh_sec` ·
`l1_category` · `l2_category`

## Runtime files and evaluation

`$UPDOWN_HOME` holds `config.json` · `state.json` · `rounds.jsonl` (every decision, including
traded ones) · `orders.jsonl` · `outcomes.jsonl` · `quotes.jsonl` · `updown.log`.
`rounds.jsonl` and `outcomes.jsonl` join on `key`.

| Harness | What it answers |
|---|---|
| `backtest.py eval` | Does the signal clear the cost hurdle out of sample? Offline, auditable by someone who does not trust the daemon |
| `backtest.py pricedin` | Is it already in the price? The question a backtest cannot reach |

`eval` enforces a train/test split, prints confidence intervals rather than point estimates,
counts hypotheses tested, and checks dose-response on the full sample. Any non-live run writes
`quotes.jsonl`, recording **every book it can read, including ones your gates reject** — sampling
only tradable books biases the priced-in analysis.

Three columns matter in calibration: your probability, a constant 0.50, and the quote. **Failing
to beat the quote column means there is no strategy**, however good the hit rate looks.

## Platform behavior notes

**A dead session must never look like a quiet market.** Every prediction read needs an
authenticated session and sessions expire. Pre-flight probes the prediction endpoint itself
(`wallet status` can answer while the prediction session is dead); at runtime any auth failure is
logged `ALERT` and recorded as that round's skip reason.

**`order-book` takes `--marketId`, not `--marketTopicId`.** Different identifiers; a topic
contains markets.

**The minimum order is 1 USDT** — `quote` rejects less.

**A placed order can still fail.** Observed: `place-order` returns success, the order settles to
`FAILED` ("Failed to execute the market order") with zero filled. Placement is a receipt. The
daemon polls to a terminal status and on failure **returns the stake to the budget and drops the
round** — otherwise a failed order consumes budget forever and leaves a phantom open round.

**Settled PnL is in `realizedPnl`; `pnl` comes back null.** Reading the wrong one books every win
as zero and destroys the calibration ledger.

**Redemption is account-wide**, not daemon-scoped: the sweep claims everything claimable in the
account, including positions this daemon never opened. Settlement bookkeeping covers only rounds
in its own `state.json`.

**Quotes expire** between quote and place; the daemon refetches once.

**Resting sell orders can co-reserve the same shares** and only release at resolution, after which
further sells fail for insufficient position while the market is still open. Keep at most one
resting order per position.

## Pre-flight checks

Read-only — **do not probe by placing an order**.

```bash
baw wallet status --json
baw wallet chains --json
baw wallet balance --binanceChainId <chain> --json
baw prediction category list --json             # confirm crypto / up-down exists
baw prediction position list --limit 1 --json   # confirm the prediction session is alive
```

## Running

```bash
cd <skill-dir>/scripts && python3 updown.py                     # foreground
nohup python3 -u updown.py >> runner.log 2>&1 & disown          # long-running
python3 updown.py --collect-quotes                              # records only
```

| Action | Command |
|---|---|
| Stop opening new rounds | `touch $UPDOWN_HOME/STOP` |
| Exit the process | `touch $UPDOWN_HOME/KILL` |
| Acknowledge the amount at risk | `echo <budget_usd> > $UPDOWN_HOME/I_UNDERSTAND_THE_RISK` |
| Restore the live gate | `rm $UPDOWN_HOME/I_UNDERSTAND_THE_RISK` |

**Going live**: set `mode` to `live`. The run refuses to start unless the ack file contains the
current `budget_usd` — so it cannot be inherited by copying a runtime directory, and **raising
`budget_usd` invalidates it**. An agent may write it once the operator has confirmed the number.

**Exiting does not close open rounds.** They settle on their own and still need redeeming.

### Keeping it running

This is a **foreground process with an internal loop**, not a Unix daemon: no fork, no setsid.
`nohup … &` survives a logout, not a reboot. What the process does and does not guarantee:

| | |
|---|---|
| Survives a transient error | **Yes** — the loop catches, logs `ERROR main loop`, and backs off 15s → 300s |
| Survives a crash or reboot | **No** — nothing restarts it. That is your supervisor's job |
| Safe to restart | **Yes** — `state.json` holds budget, open rounds and daily counters; `flock` prevents two instances |
| Recovers missed settlements | **Yes** — the sweep re-reads positions and `PENDING_CLAIM` on each pass |
| Survives session expiry | **No** — it keeps running but skips every round, loudly (`ALERT`). Re-authenticate |

launchd (macOS) — `~/Library/LaunchAgents/local.updown.plist`:

```xml
<plist version="1.0"><dict>
  <key>Label</key><string>local.updown</string>
  <key>ProgramArguments</key>
  <array><string>/usr/bin/python3</string><string>/ABSOLUTE/PATH/scripts/updown.py</string></array>
  <key>EnvironmentVariables</key><dict><key>UPDOWN_HOME</key><string>/Users/you/.local/updown</string></dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/Users/you/.local/updown/runner.log</string>
  <key>StandardErrorPath</key><string>/Users/you/.local/updown/runner.log</string>
</dict></plist>
```
`launchctl load ~/Library/LaunchAgents/local.updown.plist`

systemd (Linux) — `~/.config/systemd/user/updown.service`:

```ini
[Service]
Environment=UPDOWN_HOME=%h/.local/updown
ExecStart=/usr/bin/python3 /ABSOLUTE/PATH/scripts/updown.py
Restart=always
RestartSec=30
[Install]
WantedBy=default.target
```
`systemctl --user enable --now updown`

**The supervisor restarts the process; it does not re-authenticate.** A session that expires
stops all trading until someone signs in again — plan for that separately, and watch for `ALERT`
lines rather than assuming quiet means healthy.

## Known limitations

| Limitation | Detail |
|---|---|
| **Bundled strategy is unverifiable** | ~+0.65%/round against a ±1.9pp error bar; ~22,700 rounds to confirm. A worked example of the bar your signal must clear, not a signal to fund |
| **Hit rate is not edge** | If the quote reflects the state, a winning hit rate earns zero. Only `pricedin` rules it out |
| At-the-money rounds | Fair value ≈0.50; anything won there is mispricing, not forecasting |
| Fee dominates | 200 bps per round, published by the platform |
| No exit, no stop-loss | The whole decision is at entry |
| Redemption is required | Winnings sit unclaimed until swept |
| Sessions expire | Mitigated by alerting, not solved. A long run needs re-authentication |
| Dry-run misses the money path | Ordering, fills, settlement and redemption only run live |
| Thin depth | Single-digit dollars at the best ask has been observed |
| No supervisor | Use launchd, systemd or a container restart policy |

## Disclaimer

**This is a scaffold, not a trading product.**

- The bundled strategy is a measured reference with **no demonstrable positive expectancy net of
  costs**, provided to show that the pipeline runs and the harnesses discriminate.
- Every risk control and parameter here is a **suggestion**, not a safeguard. The daemon runs the
  checks you configure; it does not judge whether they suffice.
- **Nothing here is investment, financial or trading advice.**
- Positions can expire worthless. Automated trading can lose money through market conditions you
  did not anticipate, platform behavior changes, defects in this software, or defects in the
  strategy you write.
- Provided **as-is, without warranty**. To the maximum extent permitted by law, no liability is
  accepted for any loss arising from its use.
- **You are solely responsible** for what you run, the parameters you choose, compliance with the
  laws that apply to you, and any funds you commit.

If you are not prepared to lose the full `budget_usd`, do not set `mode` to `live`.
