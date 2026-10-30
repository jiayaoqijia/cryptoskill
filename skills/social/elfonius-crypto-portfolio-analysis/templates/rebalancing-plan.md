# Rebalancing Plan

**As of:** {{AS_OF}}  
**Base currency:** {{BASE_CURRENCY}}  
**Data coverage:** {{DATA_COVERAGE}}  
**Mode:** Conditional plan — no execution

## 1. Current vs target

| Position | Current weight | Target weight | Delta | Band | Action |
|---|---:|---:|---:|---|---|
| {{POSITION}} | {{CURRENT}} | {{TARGET}} | {{DELTA}} | {{BAND}} | {{ACTION}} |

## 2. Why change?

- **Risk reason:** {{RISK_REASON}}
- **Mandate reason:** {{MANDATE_REASON}}
- **Liquidity reason:** {{LIQUIDITY_REASON}}
- **Valuation/fundamental reason:** {{VALUE_REASON}}

## 3. Implementation constraints

| Constraint | Value | Effect |
|---|---:|---|
| Liquidity | {{LIQUIDITY}} | {{LIQUIDITY_EFFECT}} |
| Tax | {{TAX}} | {{TAX_EFFECT}} |
| Fees/slippage | {{COST}} | {{COST_EFFECT}} |
| Lock/vesting | {{LOCK}} | {{LOCK_EFFECT}} |
| Custody/legal | {{CUSTODY}} | {{CUSTODY_EFFECT}} |

## 4. Options

| Option | Risk after | Liquidity after | Cost | Tax | Reversible? |
|---|---|---|---|---|---|
| Do nothing | {{RISK_NONE}} | {{LIQ_NONE}} | {{COST_NONE}} | {{TAX_NONE}} | Yes |
| Rebalance to bands | {{RISK_BAND}} | {{LIQ_BAND}} | {{COST_BAND}} | {{TAX_BAND}} | Partly |
| Full target | {{RISK_FULL}} | {{LIQ_FULL}} | {{COST_FULL}} | {{TAX_FULL}} | No |

## 5. Recommendation

{{RECOMMENDATION}}

**Size range:** only if the IPS-lite contains constraints: {{SIZE_RANGE}}  
**What would make this smaller:** {{SMALLER_TRIGGER}}  
**What would falsify the plan:** {{FALSIFIERS}}

## 6. Review

- Review date: {{REVIEW_DATE}}
- Triggers: {{TRIGGERS}}
- Owner: {{OWNER}}

> This is a decision aid. The skill does not execute, sign, approve, bridge, or deposit.
