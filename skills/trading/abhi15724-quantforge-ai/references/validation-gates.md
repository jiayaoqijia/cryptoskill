# Validation Gates

A strategy advances one stage only after passing that stage's gate. Thresholds are **defaults to disclose and tune**, not guarantees; state any you change.

## Stage gates
| Gate | Minimum evidence |
|---|---|
| Hypothesis to Backtest | Economic/structural rationale; precise rules; costs defined |
| Backtest to OOS | Enough trades (default >= 100, or justify fewer); positive expectancy after costs; not dependent on one narrow parameter peak |
| OOS to Walk-forward | OOS Sharpe and drawdown within a stated tolerance of in-sample (default: OOS Sharpe >= ~50% of IS); OOS never used for tuning |
| Walk-forward to Paper | Positive across most rolling windows; works in >= 2 distinct regimes or is explicitly regime-gated |
| Paper to Live | Paper period covers enough trades and one adverse regime; fills/slippage match the model; risk limits and kill switch tested; **explicit user approval** |

## Overfitting checklist (PASS / FAIL / UNKNOWN for each)
1. Look-ahead (signal uses bar-close info but fills at that bar's open/close?)
2. Survivorship (delisted names, expired contracts, index reconstitution)
3. Data leakage (normalisation, features, labels computed over the full sample)
4. Selection bias / data snooping (how many ideas or parameters were tried?)
5. Multiple testing (apply a haircut or deflated Sharpe if many trials)
6. Parameter count vs trade count; is the sensitivity surface smooth?
7. Unrealistic execution (fills at touch, ignoring spread, queue, impact, rate limits)
8. Cost sensitivity (does edge survive 2x costs and 2x slippage?)
9. Regime dependence (a single bull-market sample?)
10. Time-stability (edge decaying in recent data?)

Any FAIL on 1, 3 or 7 invalidates the result. Several FAIL/UNKNOWN means `HIGH RISK / POTENTIALLY OVERFIT`.

## Robustness tests
Parameter grid +/-20-30%, cost/slippage x1.5-3, bootstrap of trades (CI on Sharpe and drawdown), Monte Carlo of trade order, rolling/anchored walk-forward, regime split (bull/bear/sideways/high-vol/low-vol/crisis), stress on gap/crash days, data-shift test (different start date or instrument).

## Risk Manager attack list
Worst day/week? Gap through stop? Correlated positions failing together? Margin-call path? Liquidity vanishing? Model wrong (vol regime, funding flip, expiry pin)? What stops the strategy automatically?
