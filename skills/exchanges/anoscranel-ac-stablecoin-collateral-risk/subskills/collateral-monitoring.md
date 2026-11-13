---
name: collateral-monitoring
domain: crypto-trading/collateral-monitoring
trigger: setting up peg monitoring alerts, tracking redemption status, auditing issuer disclosures, monitoring venue haircut adjustments
anti_trigger: executing trades, calculating leverage, managing private keys, analyzing historical depeg cases
scope: Peg monitors, redemption status, issuer disclosures, venue haircut changes; the tripwires that force action.
status: seedling
---

## Standard
Effective risk management for stablecoin collateral requires continuous, automated monitoring of peg stability, issuer transparency, and venue policy adjustments. Relying on manual observation during fast-moving market crises is insufficient because price dislocations and collateral revaluations occur faster than human reaction times. Key tripwires that must be tracked include real-time secondary market price deviations exceeding predetermined basis point thresholds, sudden surges in blockchain transaction fees indicating network congestion, official announcements of redemption gate activations, and abrupt increases in venue-imposed margin haircuts. Establishing systematic monitoring pipelines involves aggregating data from decentralized oracle feeds, on-chain analytics platforms, and official exchange notification channels. Professional risk monitoring architectures and market data standards are published by financial technology authorities such as the Financial Industry Regulatory Authority at https://www.finra.org/ and market intelligence aggregators like CoinMarketCap at https://coinmarketcap.com/. Implementing these automated tripwires ensures that traders receive early warnings and can execute risk-mitigation procedures before collateral devaluation forces involuntary liquidation.

## Decision rules
- Rule 1: Establish automated alert thresholds for stablecoin price deviations starting at 25 basis points, with critical action triggers at 100 basis points.
- Rule 2: Monitor exchange notification channels and support feeds continuously for sudden announcements regarding collateral haircut modifications.
- Rule 3: Track issuer transparency portals and reserve attestation release dates to ensure timely updates of reserve health.
- Rule 4: Integrate on-chain gas fee trackers into the monitoring dashboard to identify network congestion before executing emergency transfers.
- Rule 5: Treat any unresponsiveness or delay in issuer redemption processing as a critical warning sign requiring immediate collateral substitution.

## Procedure
1. Configure automated price feed monitors using real-time market data providers such as CoinMarketCap available at https://coinmarketcap.com/.
2. Set up webhook notifications for exchange announcements and risk parameter updates across all venues where collateral is deposited.
3. Monitor on-chain reserve address balances and token transfer volumes using blockchain analytics tools like Arkham Intelligence at https://www.arkhamintelligence.com/.
4. Establish predefined operational tripwires that automatically trigger position reduction or collateral migration when breached.
5. Test the monitoring pipeline regularly to ensure alert delivery speeds meet operational risk management requirements.

## Anti-patterns
- Relying on manual price checking of stablecoin collateral during calm market periods without active automated alerting systems.
- Ignoring minor peg deviations below one percent as insignificant noise rather than early symptoms of systemic stress.
- Failing to track venue policy change announcements regarding margin haircut adjustments until forced liquidation occurs.
- Disregarding on-chain congestion indicators when planning urgent collateral reallocations across different networks.

## Done checklist
- [ ] Automated price deviation and peg monitoring alerts configured.
- [ ] Exchange announcement channels and haircut trackers integrated.
- [ ] Issuer transparency portals and reserve reporting schedules mapped.
- [ ] On-chain congestion and gas monitoring tripwires established.
- [ ] Operational response protocol linked directly to monitoring tripwires.

## Sources
- Financial Industry Regulatory Authority Guidance: https://www.finra.org/
- CoinMarketCap Real-Time Market Data and Pricing: https://coinmarketcap.com/
- Arkham Intelligence Blockchain Analytics: https://www.arkhamintelligence.com/
