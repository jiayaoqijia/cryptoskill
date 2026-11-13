---
name: carry-risk-register
domain: crypto-trading/carry-risk-register
trigger: "Build and monitor carry and basis trade risk registers, funding regime shifts, and exit liquidity."
anti_trigger: "Maintain carry positions during severe funding regime reversals without protective stop limits."
scope: "Registers risks, monitoring triggers, funding regime shifts, counterparty exposure, and exit liquidity."
status: seedling
---

## Standard
Operating basis and carry strategies requires a formalized risk register to monitor latent vulnerabilities that can erode principal during adverse market regimes. The primary risks include structural funding regime shifts where persistently positive funding turns negative, converting positive carry into a steady capital drain. Additional risks involve hedge-leg liquidation where rapid upward price spikes force liquidations on the short derivative leg before spot collateral can be transferred or liquidated to cover margin calls.

Counterparty and operational risks demand rigorous oversight. Venue continuity, exchange solvency, API connectivity stability, and insurance fund adequacy dictate counterparty exposure limits. Stablecoin depeg risks threaten collateral integrity when margins are denominated in USD-pegged tokens. Finally, exit liquidity constraints can trap carry positions during market stress, as wide bid-ask spreads and thin order books prevent simultaneous unwinding of spot and derivative legs without severe price impact slippage.

Primary sources for the claims in this step: <https://www.fsb.org/work-of-the-fsb/financial-innovation-and-structural-change/crypto-assets-and-global-stablecoins/> and <https://www.isda.org/a/g8gEE/Counterparty-Credit-Risk-Management.pdf>.

## Decision rules
- Establish automated alert thresholds for funding rate regime changes that trigger position review or unwinding.
- Monitor short derivative margin health continuously, enforcing strict collateral buffer rules against price shocks.
- Diversify carry capital across multiple reputable venues to mitigate single-exchange counterparty and operational risks.
- Audit stablecoin collateral holdings and maintain emergency conversion pathways to native assets or fiat.
- Assess exit liquidity and order book depth before entering large carry positions to ensure smooth unwinding capability.

## Procedure
1. Compile the carry strategy risk register incorporating funding regime, liquidation, counterparty, and liquidity hazards.
2. Define quantitative monitoring triggers and threshold limits for each identified risk factor.
3. Configure automated alerting systems for funding rate reversals and margin buffer depletion.
4. Establish contingency protocols for emergency position unwinding during extreme market dislocation.
5. Review risk register compliance weekly and update monitoring parameters based on prevailing market volatility.

## Anti-patterns
- Operating carry strategies without stop-loss or automated unwinding triggers for negative funding regimes.
- Concentrating all carry capital on a single exchange without evaluating venue backstop and insurance fund health.
- Ignoring stablecoin depeg risks when holding large collateral balances in secondary-tier pegged assets.
- Failing to test emergency exit execution pathways under simulated low-liquidity market conditions.

## Done checklist
- [ ] Carry risk register established with comprehensive hazard categories.
- [ ] Quantitative monitoring triggers and alert thresholds configured.
- [ ] Venue counterparty and stablecoin collateral risks evaluated.
- [ ] Emergency unwinding contingency protocols documented.
- [ ] Weekly risk review schedule established.

## Sources
- ISDA Guidelines on Derivative Counterparty Credit Risk Management: https://www.isda.org/a/g8gEE/Counterparty-Credit-Risk-Management.pdf
- Financial Stability Board Report on Crypto-Asset Market Structural Risks: https://www.fsb.org/work-of-the-fsb/financial-innovation-and-structural-change/crypto-assets-and-global-stablecoins/
