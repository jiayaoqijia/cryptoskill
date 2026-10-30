# 06 — Tokenomics and Value Capture

## Purpose

Separate **network activity** from **tokenholder value**. A token can have revenue, emissions, buybacks, and a rising price while transferring no net value to a long-term holder.

## Inputs

- Circulating supply, total supply, max supply, and float.
- Emission schedule and next 12–36 months of unlocks.
- Fees, revenue, gross profit, and tokenholder distributions.
- Buyback/burn transactions and funding source.
- Holder concentration and treasury holdings.

## Method

1. Map each token to its supply definitions.
2. Separate fees, revenue, gross profit, incentives, and tokenholder revenue.
3. Compute FDV, P/S, P/F, and dilution yield with matched definitions.
4. Trace the value-capture waterfall.
5. Check the next unlock and the buyback funding source.
6. Label missing data; do not infer holder revenue from price.

## Definitions

| Term | Definition | Common error |
|---|---|---|
| Circulating supply | Tokens freely tradable now | Using total supply for market cap |
| Total supply | Issued tokens minus burned | Ignoring future minting |
| Max supply | Protocol cap, if any | Assuming the cap is enforced |
| Float | Circulating / total supply | Confusing float with liquidity |
| Emissions | New tokens issued over a period | Treating emissions as revenue |
| Unlocks | Scheduled release of locked tokens | Ignoring insider/VC supply |
| FDV | Price × fully diluted supply | Comparing FDV with circulating market cap |
| Fees | What users pay | Treating fees as protocol revenue |
| Revenue | Protocol’s share of fees | Treating revenue as tokenholder income |
| Gross profit | Revenue minus direct costs | Ignoring token incentives |
| Tokenholder revenue | Cash or burn that accrues to holders | Counting treasury inflows as holder yield |
| Buyback | Market purchase, usually to treasury or burn | Assuming all buybacks are burns |
| Burn | Permanent supply reduction | Ignoring mint/emission offset |

## Value-capture waterfall

1. User pays fees.
2. Protocol splits fees among suppliers, treasury, and tokenholders.
3. Tokenholders receive dividends, buybacks, burns, or governance rights.
4. Emissions dilute holders unless offset by burn or demand.
5. Net holder value = tokenholder revenue + burn value − dilution − risk.

Show each step. If step 3 is missing, say `no direct value capture`.

## Ratios

- `P/S = market cap / annualized revenue`; state revenue definition.
- `P/F = market cap / annualized fees`; fees are not profit.
- `P/E` only if there is a credible net-profit measure; many tokens have none.
- `FDV/S` uses fully diluted supply; useful for unlock overhang.
- `Buyback yield = annual buyback / market cap`; check funding source.
- `Emission yield = annual emissions value / market cap`; compare with buyback yield.

Do not compare ratios across tokens without matching the numerator and denominator definitions.

## Supply-overhang checklist

- Unlock schedule next 12–36 months.
- Insider/team/VC allocation and cliffs.
- Emissions rate and decay.
- Treasury holdings and sell pressure.
- Buyback funding: revenue, treasury, debt, or new tokens.
- Burn mechanism: permanent, conditional, or marketing.
- Holder concentration: top 10, top 100, exchange-held supply.
- Governance: who can change supply or fees.

## Red flags

- “Revenue” that is only token emissions.
- Buybacks funded by selling new tokens.
- Yield paid in the same token that is being diluted.
- FDV far above circulating market cap with near-term unlocks.
- A “burn” that is reversible or not on-chain.
- Treasury revenue presented as tokenholder revenue.

## Output

| Token | Circ. supply | FDV | Emissions | Next unlock | Revenue | Holder value | Buyback/burn | Dilution |
|---|---:|---:|---:|---|---:|---|---|---|
| Example | X | $X | X%/yr | Date | $X | $X or none | $X | X%/yr |

## Failure modes

- Calling TVL or volume “revenue.”
- Calling incentives “yield” without dilution.
- Ignoring the difference between buyback and burn.
- Using FDV and market cap interchangeably.
- Assuming a fixed supply if governance can mint.

## Sources

- CFA Institute, *Measuring and Managing Market Risk* (risk-factor discipline).
- DefiLlama fees/revenue endpoints and Token Terminal definitions; verify the exact definition before use.
