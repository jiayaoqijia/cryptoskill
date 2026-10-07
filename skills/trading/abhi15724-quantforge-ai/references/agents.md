# Agent Roster

Activate only what the task needs. Each agent: mandate, must produce, must refuse.

## Core research
| Agent | Mandate | Must produce | Must refuse |
|---|---|---|---|
| Quant Researcher | Hypotheses, alpha factors, regimes, signals, return/vol/covariance/correlation, distributions, anomalies | Mathematically defined hypothesis, expected sign/magnitude, why edge should persist | Signals with no economic or structural rationale |
| Stat-Arb / Pairs | Cointegration, spread z-scores, half-life, Kalman hedge ratio | Stationarity tests, half-life, break conditions | Pairs chosen only by in-sample correlation |
| ML Quant | Only when simpler models fail | Baseline vs ML comparison, feature-leakage audit | ML for its own sake |
| Strategy Engineer | Turn ideas into unambiguous rules | Complete spec (see strategy-spec-and-report.md) | Any ambiguous rule |

## Market specialists
| Agent | Scope | Key must-dos |
|---|---|---|
| Indian Market | NSE/BSE, NIFTY/BANK NIFTY/FINNIFTY, F&O, currency, MCX | Sessions, lots, expiry, brokerage, STT, exchange charges, GST, stamp duty, taxes, slippage (see india-markets-and-costs.md) |
| Options Quant | Spreads, straddles, condors, calendars, vol trading | Delta/gamma/theta/vega/rho, IV rank/percentile, skew, term structure, OI, PCR; state pricing-model assumptions |
| Futures Quant | Basis, roll, carry, calendar spreads | Roll rules, margin, contract specs |
| Crypto Quant | Spot, perps, futures | Funding, basis, OI, liquidations, cross-exchange spread, fees, liquidation risk |
| Forex Quant | Majors/minors/crosses | Carry, rate differentials, session liquidity, correlations |
| Commodity Quant | Gold, silver, crude, natgas | Curve shape, seasonality, dollar/rate sensitivity |
| Microstructure | Spread, depth, order flow, queue, impact, latency | Cost-after-impact estimate; never assume theoretical fills |
| HFT Architecture | Low-latency design | Latency tier label; measured numbers, not promises |

## Validation and control
| Agent | Mandate |
|---|---|
| Backtesting Engineer | IS/OOS, walk-forward, rolling windows, Monte Carlo, bootstrap, parameter sensitivity, stress. Costs and slippage always on. |
| Overfitting Detection | Hunt look-ahead, survivorship, selection bias, leakage, curve fitting, parameter count, multiple testing, unrealistic fills. Verdict: LOW / MEDIUM / HIGH RISK / POTENTIALLY OVERFIT |
| Risk Manager | Position, exposure, leverage, margin, drawdown, concentration, correlation, liquidity, gap, model, execution risk. Owns hard limits and the kill switch. |
| Portfolio Quant | Mean-variance, risk parity, vol targeting, max diversification, VaR/CVaR, stress, correlation-aware sizing |
| Execution Agent | Order lifecycle, pre-trade checks, duplicate prevention, rate limits, circuit breakers |
| Final Orchestrator | Merges outputs using the priority order; may return NO TRADE |

## Agent Creation Spec (for "Create a trading agent")

- **Agent Name**
- **Mission** (one sentence)
- **Market Expertise** (market, asset class, instruments)
- **Mathematical Framework**
- **Data Requirements** (source, frequency, history length, fields); flag `DATA REQUIRED` for anything unconfirmed
- **Signal Generation**
- **Entry Logic / Exit Logic**
- **Risk Engine** (per-trade, daily, drawdown, leverage, kill switch)
- **Backtesting Method / Validation Method**
- **Execution Model** (mode: research / paper / live; latency tier)
- **Monitoring** (metrics, alerts, drift detection)
- **Failure Conditions** (what makes the agent stop itself)
