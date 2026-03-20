# Strategy Profiles

This file defines reusable strategy archetypes for OpenClaw agents. These include the four strategies from `4-bots-competition.md`, converted into operational profiles.

## 1) Whale Mirror (Flow-Following)

- Objective: mirror high-conviction smart-money flows for steady participation.
- Inputs:
  - top wallet list and rolling wallet quality score
  - on-chain transfer/trade events
  - market liquidity and slippage estimates
- Entry:
  - top-ranked wallet takes a position above a configured notional threshold
  - asset passes liquidity and spread filters
- Exit:
  - mirrored unwind event
  - time stop or trailing stop
- Risk profile:
  - moderate conviction, low leverage
  - cap concurrent mirrored positions
  - avoid concentrated exposure to one wallet

## 2) Contrarian Skew (Crowd Fade)

- Objective: take the other side of extreme consensus when skew is crowded.
- Inputs:
  - prediction market implied probability
  - side concentration, open interest, and volume
  - optional external baseline probability
- Entry:
  - one side confidence at or above configured extreme (example: 80%+)
  - concentration and liquidity thresholds met
  - skew persists through debounce window
- Exit:
  - mean reversion in implied probability
  - event resolution
  - hard invalidation window
- Risk profile:
  - sparse but high-conviction entries
  - one position at a time by default
  - cooldown after large loss

## 3) Latency Convergence (Scalper/Arb)

- Objective: exploit short-lived pricing lag across venues.
- Inputs:
  - fast venue mid-price stream
  - slower venue implied price stream
  - measured delay, spread, fees, and expected slippage
- Entry:
  - actionable delta exceeds all costs + minimum edge buffer
  - stale/lag condition is present
- Exit:
  - convergence target reached
  - timeout reached
  - edge collapses before fill
- Risk profile:
  - smallest position sizing
  - strict kill-switch after repeated slippage or edge decay
  - disable when latency edge regime degrades

## 4) Weather/Event Consensus

- Objective: trade only when independent forecast models align and market is mispriced.
- Inputs:
  - three independent model forecasts
  - market implied outcome probability
  - event liquidity and horizon
- Entry:
  - full model agreement on directional outcome
  - model-implied probability diverges from market by threshold
- Exit:
  - hold to settlement or early close if model consensus breaks
- Risk profile:
  - low trade frequency is expected
  - medium sizing for high-confidence consensus events
  - disallow trades when data freshness is uncertain

## 5) Swing Baseline (Default)

- Objective: multi-day trend/momentum/reversion trades for equities and crypto.
- Inputs:
  - OHLCV, RSI/MACD/ATR/MA context
  - support/resistance and regime filters
  - lightweight sentiment/news summary
- Entry:
  - indicator confluence meets strategy template
  - setup has defined invalidation and risk/reward floor
- Exit:
  - stop loss, profit target, trailing, or thesis invalidation
- Risk profile:
  - strategy-specific max risk per trade
  - exposure cap by asset and correlation bucket
  - drawdown-based throttle

## Self-Improvement hooks for all profiles

- Log every hypothesis and outcome with strategy ID and parameter version.
- Track regime tags (trend/chop/volatility) to diagnose edge stability.
- Run champion-vs-challenger tests before promoting model/parameter changes.
- Promote recurring failure patterns into guardrails and feature engineering tasks.
