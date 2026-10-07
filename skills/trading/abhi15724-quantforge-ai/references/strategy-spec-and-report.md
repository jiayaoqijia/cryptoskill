# Strategy Spec (input to backtest) and Research Report (output)

## 1. Strategy spec: every field required
Market, Instrument, Timeframe, Entry, Exit, Position sizing, Stop-loss, Take-profit, Hedging, Max exposure, Max drawdown, Trading session, Transaction costs, Slippage assumption, Re-entry rules, Failure conditions.
If a field is unknown, write `UNSPECIFIED` and do not backtest until resolved (or label the result INCOMPLETE).

## 2. Backtest quality declaration (state before any result)
Data source, Frequency, Date range, Market, Instrument, Survivorship treatment, Corporate actions, Costs, Slippage, Liquidity assumptions, Sizing, Leverage, Execution assumptions, Look-ahead prevention, Train/test split, OOS period.
Any unknown means `INCOMPLETE`.

## 3. Research report template

```
STRATEGY NAME
Market / Instrument / Timeframe
CORE IDEA
MATHEMATICAL LOGIC
ENTRY / EXIT
POSITION SIZING / HEDGING
RISK MANAGEMENT
TRANSACTION COST ASSUMPTIONS
BACKTEST RESULTS            (stage label + declaration status)
OUT-OF-SAMPLE RESULTS
WALK-FORWARD RESULTS
MONTE CARLO RESULTS
MAX DRAWDOWN | SHARPE | SORTINO | PROFIT FACTOR | EXPECTANCY
ROBUSTNESS SCORE
OVERFITTING RISK            (LOW / MEDIUM / HIGH / POTENTIALLY OVERFIT)
EXECUTION FEASIBILITY
KNOWN FAILURE MODES
FINAL VERDICT               (REJECT / NEEDS MORE DATA / PAPER-TRADE ONLY / NO TRADE / CANDIDATE)
```
Unrun sections say `NOT RUN`. The verdict never says "profitable"; at most `CANDIDATE FOR PAPER TRADING`.

## 4. Scoring (0-100, never raw profit alone)
Suggested weights (adjust and disclose): risk-adjusted return 20, drawdown 15, robustness/stability 20, cost sensitivity 10, execution feasibility 10, liquidity 5, overfitting risk (penalty) 15, simplicity 5.
Example: 100% return with 80% drawdown should score below 30% return with 10% drawdown.
