---
name: concentration-and-single-points
domain: crypto-trading/concentration-and-single-points
trigger: "concentration risk, single point of failure, stablecoin concentration, venue risk"
anti_trigger: "capital allocation, rebalancing, portfolio review"
scope: Auditing venue, stablecoin, strategy, and custody concentration points.
status: seedling
---

# Concentration And Single Points

## Standard

Concentration risk arises when a portfolio relies excessively on a single venue, stablecoin issuer, custody provider, or trading strategy. A single-point-of-failure failure—such as an exchange freezing withdrawals during a crash, a stablecoin de-pegging from its fiat peg, or a core bridge exploiting—can cause catastrophic capital loss regardless of underlying strategy profitability. Portfolio construction mandates continuous auditing and strict caps on all concentration vectors to ensure structural resilience against unforeseen operational black swan events. Identifying and mitigating these systemic vulnerabilities is essential for preserving long-term trading capital across decentralized and centralized financial ecosystems. Continuous oversight prevents silent accumulation of hidden structural risk.

Primary sources for the claims here: <https://www.newyorkfed.org/> and <https://www.iosco.org/>.

## Decision rules

- Total exposure to any single trading venue or centralized exchange must not exceed a pre-specified percentage of aggregate portfolio capital under any market condition.
- Stablecoin holdings must be diversified across multiple distinct token issuers and backing mechanisms to eliminate single-issuer de-peg vulnerability.
- Custody arrangements must separate operational hot wallets from long-term cold storage reserves and third-party institutional custody providers.
- Strategy concentration must be monitored continuously to ensure no single trading methodology dominates total portfolio return variance or risk exposure.

## Procedure

1. Map all portfolio assets across venues, stablecoin types, custody providers, and underlying strategy classes into a comprehensive inventory matrix.
2. Calculate exact concentration ratios for each identified risk vector against established portfolio limits and risk tolerance thresholds.
3. Identify single points of failure where an operational disruption, hack, or regulatory enforcement action halts portfolio functionality.
4. Execute capital re-allocation to reduce exposures exceeding maximum allowed concentration caps across venues and stablecoin issuers.
5. Maintain an active concentration risk register updated regularly with counterparty health scores, audit reports, and regulatory status.

## Anti-patterns

- Holding 100 percent of stablecoin margin in a single token issuer to chase marginal yield advantages in lending pools.
- Relying on a single exchange API or custody provider for all execution, settlement, and collateral management operations.
- Overlooking indirect concentration risks, such as multiple distinct strategies depending on the same underlying liquidity provider or oracle.

## Done checklist

- [ ] Venue, stablecoin, and custody concentration ratios are within mandated portfolio caps.
- [ ] Single points of failure are identified, analyzed, and documented in a risk register.
- [ ] Diversification safeguards are active and enforced across all operational vectors.

## Sources

- Financial Stability Board (FSB): https://www.fsb.org/
- Bank for International Settlements (BIS): https://www.bis.org/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/
- Federal Reserve Bank of New York: https://www.newyorkfed.org/
