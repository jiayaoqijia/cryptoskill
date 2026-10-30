# Risk Dashboard

**As of:** {{AS_OF}}  
**Base currency:** {{BASE_CURRENCY}}  
**Data coverage:** {{DATA_COVERAGE}}  
**Benchmark:** {{BENCHMARK}}

## 1. Exposure

| Measure | Value | Limit | Status |
|---|---:|---:|---|
| Top-1 weight | {{TOP1}} | {{TOP1_LIMIT}} | {{TOP1_STATUS}} |
| Top-2 weight | {{TOP2}} | {{TOP2_LIMIT}} | {{TOP2_STATUS}} |
| Largest cluster | {{CLUSTER_WEIGHT}} | {{CLUSTER_LIMIT}} | {{CLUSTER_STATUS}} |
| Stablecoin weight | {{STABLE_WEIGHT}} | {{STABLE_LIMIT}} | {{STABLE_STATUS}} |
| Liquid bucket | {{LIQUID_BUCKET}} | {{LIQUID_LIMIT}} | {{LIQUID_STATUS}} |

## 2. Market risk

| Measure | Value | Window | Method | Limitation |
|---|---:|---|---|---|
| Annualized volatility | {{VOLATILITY}} | {{VOL_WINDOW}} | Historical | Past regime |
| Max drawdown | {{MAX_DRAWDOWN}} | {{DD_WINDOW}} | Daily marks | Stale prices |
| VaR 95% 1d | {{VAR}} | {{VAR_WINDOW}} | Historical | Tail underestimation |
| CVaR 95% 1d | {{CVAR}} | {{CVAR_WINDOW}} | Historical | Sparse tail |
| Beta vs benchmark | {{BETA}} | {{BETA_WINDOW}} | OLS | Regime-dependent |
| Top risk contribution | {{RISK_CONTRIB}} | {{RC_WINDOW}} | Component CVaR | Model-dependent |

## 3. Liquidity

| Position | 1% exit days | 5% exit days | Stressed exit days | Gate |
|---|---:|---:|---:|---|
| {{POSITION}} | {{D1}} | {{D5}} | {{D_STRESS}} | {{LOCK}} |

## 4. Scenario summary

| Scenario | Loss | % | First breach |
|---|---:|---:|---|
| Risk-off | {{LOSS_RISK_OFF}} | {{PCT_RISK_OFF}} | {{BREACH_RISK_OFF}} |
| Stablecoin depeg | {{LOSS_DEPEG}} | {{PCT_DEPEG}} | {{BREACH_DEPEG}} |
| Liquidity shock | {{LOSS_LIQ}} | {{PCT_LIQ}} | {{BREACH_LIQ}} |
| Reverse stress | {{LOSS_REVERSE}} | {{PCT_REVERSE}} | {{BREACH_REVERSE}} |

## 5. Flags

- {{FLAG_1}}
- {{FLAG_2}}
- {{FLAG_3}}

## 6. What is not assessable

{{NOT_ASSESSABLE}}

> VaR is not a maximum loss. A risk dashboard is not a substitute for the mandate and liquidity analysis.
