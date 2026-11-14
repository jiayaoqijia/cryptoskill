---
name: trading-setup
description: Configure the trading-skills toolkit - account size, currency, benchmark index, risk limits, data provider (free Yahoo, CSV, or broker), broker (paper or a live broker adapter), credentials and the live-trading switch. Use when the user is getting started, says "set up trading", wants to change risk per trade or limits, connect or log in to a broker, reset the paper account, or when another trading skill reports missing config.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Trading Setup (`trading-setup`)

One-time (and occasional) configuration for every skill in the pack. All state lives in
`~/.trading-skills/` (override with `TRADING_SKILLS_HOME`). Works with zero API keys:
free Yahoo data + the built-in paper broker.

Run commands from this skill's directory. Python 3.9+, standard library only.

## Quick start

Ask the user (in one message) for: account size and currency, a benchmark index or ETF for
their market, and risk per trade (suggest 0.5-1%). Then:

```bash
python3 scripts/setup.py init --equity 100000 --currency USD --benchmark SPY --risk-pct 1
python3 scripts/setup.py doctor
```

Benchmark examples (Yahoo symbols): `SPY` / `^GSPC`, `QQQ`, `^FTSE`, `^N225`, `^NSEI`, `^GDAXI`, `BTC-USD`.
Exchange suffixes follow Yahoo: `.L` London, `.TO` Toronto, `.NS` NSE, `.BO` BSE, `.T` Tokyo, `.HK`, `.AX`, `.DE`.

## Commands

| Command | Purpose |
|---|---|
| `init [--equity --currency --benchmark --provider --broker --risk-pct --exchange --product]` | create/update config |
| `show [--json]` | print config (secrets masked) |
| `set KEY VALUE` / `get KEY` | edit any dotted key, e.g. `set risk.max_daily_loss_pct 2` |
| `doctor [--symbol X]` | check Python, data provider, broker, journal, kill switch |
| `paper-reset [--cash N]` | wipe the paper account |
| `kite-login --api-key K --api-secret S` | save Kite credentials, print the login URL |
| `kite-session --request-token T` | exchange the token for a daily access token |
| `fyers-login --app-id --secret --redirect-uri` / `fyers-session --auth-code` | Fyers login (daily) |
| `upstox-login --api-key --api-secret --redirect-uri` / `upstox-session --code` | Upstox login (daily) |
| `dhan-login --client-id --access-token` | save Dhan token (24 h) |
| `groww-login --access-token` (or `--api-key --api-secret`) | save Groww token (daily) |
| `live on --i-understand-the-risks` / `live off` | enable/disable real orders |

## Risk keys (config `risk.*`)

`risk_per_trade_pct` (1.0), `max_position_pct` (20), `max_open_risk_pct` (6), `max_open_positions` (8),
`max_daily_loss_pct` (3), `max_drawdown_pct` (15), `min_reward_risk` (1.5), `max_consecutive_losses` (3).
These are enforced by **trading-risk**; change them only when the user explicitly asks.

## Connecting a live broker (optional)

Live brokers plug in through adapters in `core/tradekit/brokers/`; the paper broker needs nothing.
Adapters available now: **Zerodha Kite** (below) and beta adapters for **Fyers, Upstox, Dhan, Groww** (login steps in docs/USAGE.md section 7; Angel One is not supported). If the user's broker has no adapter yet, everything
except automatic order placement still works: they place the planned order in their broker's app.

### Zerodha Kite

1. User creates an app at developers.kite.trade. The free **Personal** plan covers orders, GTT and
   portfolio. Historical/live data needs the paid **Connect** plan - otherwise keep `data.provider=yahoo`.
2. `setup.py init --broker kite --exchange NSE --product CNC`
3. `setup.py kite-login --api-key ... --api-secret ...` -> user opens the URL and logs in
4. User pastes the `request_token` from the redirect URL -> `setup.py kite-session --request-token ...`
5. Access tokens expire daily; repeat steps 3-4 each trading day.
6. Some regulators/brokers require API orders to come from a registered static IP and carry algo
   identifiers. Tell the user to confirm their broker's API rules before enabling live trading.

Credentials can also come from env vars `KITE_API_KEY`, `KITE_API_SECRET`, `KITE_ACCESS_TOKEN`.

## Guardrails

- Never print, log or echo secrets; `show` masks them.
- Never run `live on` unless the user explicitly asks for live trading in this conversation and
  understands real money is at risk. Recommend weeks of paper trading first.
- `set` refuses `broker.live_trading_enabled`; use `live on|off`.
