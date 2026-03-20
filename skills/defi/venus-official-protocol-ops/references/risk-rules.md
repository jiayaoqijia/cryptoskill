# Venus Risk Rules

## Core formulas
- `health = weightedCollateralUSD / debtUSD`
- `bufferPct = (health - 1.0) * 100`

Where `weightedCollateralUSD` uses collateral factors or liquidation thresholds (pool-specific).

## Default thresholds
- **High risk**: `health < 1.15`
- **Medium risk**: `1.15 <= health < 1.35`
- **Low risk**: `health >= 1.35`

Conservative policy for new borrow proposals:
- Target post-action health `>= 1.30`
- Prefer `>= 1.40` for volatile collateral

## Heuristics
1. **Concentration risk**
   - If >70% collateral in a single volatile asset, bump risk by one level.
2. **Borrow cap / pool liquidity**
   - If available borrow liquidity is thin (<2x requested amount), warn as execution risk.
3. **Rate shock awareness**
   - High utilization markets can spike borrow APY quickly; warn if utilization >85%.
4. **Oracle/event risk**
   - During major market moves/news, recommend extra buffer (+0.10 health).

## User-facing language
- Use: "based on current data", "estimated", "not guaranteed".
- Avoid: "safe for sure", "cannot be liquidated".
