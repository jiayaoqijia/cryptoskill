---
name: trading-broker
description: Place, cancel and track orders through the paper broker (default, simulated) or a connected live broker (through its adapter) using a two-step preview-and-confirm flow tied to a trading-risk approval, with protective stop-loss/take-profit, position and account views, broker-side GTT stops, a kill switch to halt all trading and paper fill processing that keeps the journal in sync. Use when the user wants to buy, sell, enter, exit, close, cancel, check positions/orders/balance, halt trading, or practise with paper trading.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Broker (`trading-broker`)

The only skill that touches orders. Paper by default; live only when the user has enabled it.

## The flow (never skip a step)

1. **trading-risk** `check` -> must PASS for opening orders (approval is tied to symbol/side/qty/stop).
2. `preview` -> prints the exact order and a 6-character **CONFIRM CODE**.
3. Show the preview to the user and ask for an explicit yes **for that exact order**.
4. Only after the user confirms in the conversation: `submit --confirm CODE`.

```bash
python3 scripts/router.py preview --symbol AAPL --side buy --qty 70 --type limit --limit-price 195 \
    --stop-loss 188 --take-profit 212
python3 scripts/router.py submit --confirm 7KQ2XD
python3 scripts/router.py preview --symbol AAPL --side sell --qty 70 --type market --close   # exit
python3 scripts/router.py positions | account | orders --open
python3 scripts/router.py cancel P1a2b3c4d5
python3 scripts/router.py process                 # paper: fill resting/stop/target orders + sync journal
python3 scripts/router.py kill on --reason "..."  # halt everything   (kill off / kill status)
python3 scripts/router.py kill on --flatten       # paper: cancel + close all; live: cancel open orders
python3 scripts/router.py preview --protect --symbol NSE:INFY --qty 10 --stop-price 1450   # broker-side GTT stop
```

## Hard rules for the agent

- **Never** run `submit` without the user's explicit confirmation of the previewed order in this
  conversation. A request like "buy it" before the preview is not confirmation of the preview.
- Never invent, reuse or guess a confirm code; never edit files in `~/.trading-skills/pending/` or `approvals/`.
- Never turn the kill switch off unless the user asks. If it is on, explain and stop.
- Live trading requires `broker.live_trading_enabled` (set only through `trading-setup live on`).
  If the user wants live trading, first confirm they have paper-traded the strategy.
- Before a live order, show a fresh price (trading-data `quote`, ideally from the broker) - free data may lag.
- Prefer limit orders. Market orders can fill far from the last price in fast or thin markets.
- If a broker MCP server is connected instead, still run trading-risk first and
  still get explicit confirmation of the exact order before calling it.

## Paper broker

Simulated account in `~/.trading-skills/paper/` (starting cash = `account.equity`). Market orders
fill at the latest price +/- slippage; limit/stop orders rest until `process` sees a bar trade through;
`--stop-loss/--take-profit` become an OCO exit pair after the entry fills. Commissions and slippage
come from config `costs`. Run `process` daily (or schedule it) to fill resting orders and auto-close
journal trades when stops/targets hit. Reset with `trading-setup paper-reset`.

## Live brokers

Live orders go through a broker adapter (`core/tradekit/brokers/`); `trading-setup` lists the ones
available and how to connect. The flow, gate and confirm step are identical for every broker.

**Fyers, Upstox, Dhan, Groww adapters (beta):** symbol formats differ (Fyers `NSE:SBIN-EQ`, Upstox `NSE_EQ|INE...`, Dhan `NSE_EQ:11536`, Groww `NSE:RELIANCE`); products `CNC`/`MIS`/`NRML` map to each broker's names. Entry orders do not carry the stop - place a stop order after the fill. Upstox refuses market orders. See docs/USAGE.md section 7.

**Zerodha Kite adapter:** symbols `EXCHANGE:SYMBOL`; product from `--product` or `broker.default_product` (CNC/MIS/NRML).
Entry orders do not carry the stop: after the fill, place a protective GTT (`preview --protect`)
or a stop order. Check your broker's API rules (static IP registration, algo IDs, market-order
restrictions) before going live. Every action is logged to `~/.trading-skills/audit.log`.
