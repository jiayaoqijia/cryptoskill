---
name: "venue-scorecard"
domain: "crypto-trading/venue-scorecard"
trigger: "When asked to synthesize venue diligence, score an exchange, weigh risk dimensions, or build a decision record"
anti_trigger: "When executing single API requests or reading raw liquidation feeds"
scope: "Written diligence record, scored dimensions, weighted risk thresholds, and decision gating."
status: "seedling"
---

# Venue Scorecard

## Standard

- **ISO/IEC 25010 Software and Data Quality Models**: Systematic evaluation requires multi-attribute weighted scoring frameworks where qualitative risks and quantitative metrics are aggregated into a standardized decision record. <https://www.iso.org/standard/35733.htmlstandard/35733.html>
- **Theta Desk Operational Protocol (2026)**: Diligence is a decision record, not a recommendation engine; venues must be evaluated across seven scored dimensions with explicit red lines that trigger absolute capital exclusion regardless of trading edge. <⚠️ cited without URL.>
- ⚠️ House standard: any venue failing a single red-line dimension (such as opaque liquidation feeds, unbacked insurance funds, or regulatory blacklisting) receives an overall FAIL verdict, overriding all positive fee or liquidity metrics.

## Decision rules

1. Score each of the seven venue diligence dimensions on a 0 to 10 scale: Liquidity Realism, Fee Stack & Clearance, Backstop & Continuity, Data Transparency, Jurisdiction & Access, Counterparty & Custody, and Operational Resilience.
2. Apply mandatory weighted multipliers based on strategy capital allocation size; institutional size requires minimum scores of 8/10 across custody and backstop pillars.
3. Enforce absolute red-line criteria: any venue with missing public liquidation APIs, commingled client funds, or active regulatory criminal enforcement receives an automatic rejection.
4. Maintain a dated written diligence record capturing baseline metrics, observation timestamps, and specific source URLs for every scored claim.
5. Never treat a scorecard as a permanent certification; re-audit venue risk parameters quarterly or following any major market stress event.

## Procedure

1. Aggregate findings from all seven subskills into the master venue evaluation template.
2. Calculate the weighted composite score and verify compliance against established red-line thresholds.
3. Document the final operational verdict (PASS, RESTRICTED, or FAIL) along with specific risk constraints.
4. Archive the completed scorecard in the local research repository with full date and version metadata.
5. Present the summary decision record to decision-makers without providing financial recommendations.

## Anti-patterns

- Averaging across dimensional scores to mask a catastrophic failure in a critical pillar such as custody or backstop solvency.
- Relying on outdated venue audits conducted more than 90 days prior in fast-moving derivatives markets.
- Treating the scorecard as a trading recommendation rather than an objective risk-bounding mechanism.

## Done checklist

- [ ] All seven diligence dimensions scored and documented.
- [ ] Weighted composite score calculated and checked against thresholds.
- [ ] Red-line criteria verified for absolute compliance.
- [ ] ISO/IEC quality standards referenced for evaluation rigor (<https://www.iso.org/standard/35733.html>).
- [ ] Final diligence decision record archived with timestamp.

## Sources

- International Organization for Standardization (ISO/IEC 25010 Quality Models). <https://www.iso.org/standard/35733.htmlstandard/35733.html>
- CFTC Derivatives Clearing and Risk Management Standards. <https://www.cftc.gov/PressRoom/PressReleases/9241-26>
- Financial Stability Board (FSB) Global Regulatory Framework for Crypto-Asset Activities. <⚠️ cited without URL.>
