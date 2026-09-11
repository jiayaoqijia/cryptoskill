## Description:

Create and manage grid trading strategies with OpenMM. Automated buy/sell around center price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:


## Use Case:

Developers and trading agents use this skill to configure OpenMM grid trading workflows, generate dry-run and live trading commands, and tune grid parameters for supported crypto exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands without --dry-run may place real crypto exchange orders.

Mitigation: Start with --dry-run, review the proposed orders, check balances and prices, and use live mode only after explicit user approval.

Risk: Exchange API credentials are required for supported trading venues.

Mitigation: Use keys with withdrawals disabled, grant the smallest permissions possible, and apply exchange-side spending or position limits where available.

Risk: The external npm package is not pinned in the artifact.

Mitigation: Verify the exact @3rd-eye-labs/openmm package version and publisher trust before installing it or exposing credentials.

Risk: Grid trading can lose money in strong trends, low-liquidity pairs, or high-fee markets.

Mitigation: Use conservative order sizes, respect max-position and safety-reserve controls, and avoid market conditions the artifact identifies as unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adacapo21/skills/openmm-grid-trading)
- [Publisher profile](https://clawhub.ai/user/adacapo21)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run guidance, exchange setup notes, grid parameter recommendations, and risk-control reminders.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
