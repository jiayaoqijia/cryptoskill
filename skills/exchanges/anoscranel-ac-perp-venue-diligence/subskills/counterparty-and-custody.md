---
name: "counterparty-and-custody"
domain: "crypto-trading/counterparty-and-custody"
trigger: "When asked about exchange solvency, withdrawal rail resilience, stablecoin depeg risk, or custody models"
anti_trigger: "When analyzing API rate limits or historical funding rate distributions"
scope: "Custody models, mid-cascade withdrawal rail resilience, stablecoin counterparty risks, and exit timing."
status: "seedling"
---

# Counterparty and Custody

## Standard

- **Basel Committee on Banking Supervision (BCBS) / IOSCO Crypto-Asset Custody Standards**: Institutional custody requires clear legal segregation of client assets, robust private key management infrastructure, and insolvency-remote custodial wrappers that prevent exchange commingling. <⚠️ cited without URL.>
- **Tether (USDT) / Circle (USDC) Reserve Attestations & Depeg Risk**: Perpetual swap margin collateral relies heavily on stablecoin liquidity; during severe market cascades, stablecoin depeg risks and withdrawal rail congestion (e.g., Ethereum gas spikes or L2 bridge halts) can trap collateral exactly when liquidation defense requires immediate funding. <https://tether.to/en/transparency/>
- ⚠️ House standard: exchange withdrawal rails that experience latency spikes or manual review queues during high-volatility events represent critical single points of failure that invalidate risk models.

## Decision rules

1. Verify whether client margin collateral is held in bankruptcy-remote segregated accounts or commingled with exchange operational treasury funds.
2. Test withdrawal rail responsiveness across various network conditions; verify whether automated withdrawals function without artificial manual review bottlenecks during market stress.
3. Evaluate stablecoin collateral stability and reserve backing quality (USDT/USDC liquidity depth and redemption mechanics) to guard against collateral depeg shocks.
4. Review historical exchange solvency incidents, withdrawal freezes, or creditor restructuring processes.
5. If custody arrangements are opaque or withdrawal rails are prone to arbitrary freezing, assign an unverified ⚠️ warning flag and avoid capital deposit.

## Procedure

1. Inspect official custody disclosures and third-party attestation reports (e.g., Tether Transparency: <https://tether.to/en/transparency/>).
2. Conduct small-scale live withdrawal tests across supported blockchain networks during normal and volatile hours, measuring execution latency.
3. Review exchange user agreements regarding asset ownership, hypothecation rights, and bankruptcy priority hierarchies.
4. Monitor stablecoin liquidity pools on decentralized exchanges to gauge secondary market peg resilience.
5. Record counterparty and custody risk ratings in the venue diligence scorecard.

## Anti-patterns

- Leaving substantial trading capital on custodial exchanges longer than necessary for active strategy execution.
- Assuming stablecoins maintain a rigid $1.00 peg during systemic liquidation cascades without maintaining off-ramp buffers.
- Neglecting to test withdrawal rail processing times until an emergency capital evacuation is required.

## Done checklist

- [ ] Custodial segregation and bankruptcy-remote asset structures reviewed.
- [ ] Withdrawal rail latency and automated processing limits tested.
- [ ] Stablecoin collateral backing and reserve transparency verified (<https://tether.to/en/transparency/>).
- [ ] Historical solvency and freeze records audited (<⚠️ cited without URL.>).
- [ ] Counterparty risk score logged in the venue diligence scorecard.

## Sources

- Bank for International Settlements (BIS) and BCBS Crypto Custody Standards. <⚠️ cited without URL.>
- Tether Operations Limited Transparency and Reserve Reports. <https://tether.to/en/transparency/>
- Circle Financial USDC Transparency and Reserve Attestations. <https://www.circle.com/en/transparency>
- IOSCO Principles for the Regulation of Crypto-Asset Markets. <⚠️ cited without URL.>
- CFTC Customer Protection and Segregated Fund Requirements. <https://www.cftc.gov/PressRoom/PressReleases/9252-26>
