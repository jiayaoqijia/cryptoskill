---
name: capital-allocation
domain: crypto-trading/capital-allocation
trigger: "capital allocation, margin rails, lockups, withdrawal rails, venue distribution"
anti_trigger: "risk budgeting, correlation regime, drawdown budget"
scope: Distributing capital across venues, margin modes, lockups, and withdrawal rails.
status: seedling
---

# Capital Allocation

## Standard

Capital allocation governs the physical and logical placement of funds across different trading venues, margin accounts, settlement structures, and lockup periods. In crypto trading, capital distribution cannot be optimized by risk-return metrics alone; operational constraints, counterparty risk, margin modes (cross versus isolated), and withdrawal rail speeds dictate feasible allocation limits. Capital must be segregated across multiple counterparties to prevent a single venue insolvency or liquidity freeze from incapacitating total operations. Properly managing capital rails ensures liquidity access during high-stress market contractions when withdrawal congestion and network delays frequently impede standard fund transfers and asset rebalancing. Maintaining robust segregation rules protects core solvency across all trading venues.

Primary sources for the claims here: <https://www.cfainstitute.org/> and <https://www.iosco.org/>.

## Decision rules

- Total trading capital must be distributed across multiple independent venues and custody providers to mitigate single-counterparty insolvency and withdrawal suspension risks.
- Capital deployed into locked staking, vesting contracts, or slow-withdrawal liquidity pools must be classified as illiquid and excluded from active trading drawdowns.
- Margin allocation across perpetual and derivatives venues must respect strict leverage caps and collateral hair-cut schedules defined by the risk mandate.
- Emergency reserve capital must be held in low-risk, highly liquid rails with immediate withdrawal access unaffected by exchange congestion or network freezes.

## Procedure

1. Inventory all available trading venues, custody solutions, and settlement rails under consideration for capital deployment.
2. Establish maximum capital exposure limits per venue based on rigorous counterparty risk scores and historical operational reliability.
3. Categorize capital by liquidity tier: active trading margin, strategic reserve, and illiquid locked assets in vesting pools.
4. Allocate active trading capital across approved venues while maintaining adequate unallocated emergency reserves in secure external storage.
5. Audit capital distribution regularly to ensure strict adherence to venue concentration caps and minimum liquidity requirements.

## Anti-patterns

- Concentrating trading capital on a single centralized exchange or margin venue to maximize short-term capital efficiency.
- Failing to account for withdrawal lockups or network congestion delays when calculating emergency liquidity availability.
- Mixing active trading margin with long-term strategic holdings in the same custodial trading account.

## Done checklist

- [ ] Capital is distributed across multiple independent venues and custody rails securely.
- [ ] Liquidity tiers (active, reserve, locked) are clearly defined, categorized, and tracked.
- [ ] Emergency reserve capital is held in fast-withdrawal rails independent of trading venues.

## Sources

- Bank for International Settlements (BIS): https://www.bis.org/
- Financial Stability Board (FSB): https://www.fsb.org/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/
- CFA Institute: https://www.cfainstitute.org/
