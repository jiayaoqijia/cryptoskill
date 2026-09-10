## Description:

Monitors Aave V3 borrow positions by querying collateral, debt, and health factor across supported chains and producing liquidation-risk alerts for configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgramajo4](https://clawhub.ai/user/jgramajo4)

### License/Terms of Use:


## Use Case:

External Aave users and DeFi operators use this skill to monitor wallet health factors, review collateral and debt summaries, and receive alerts when liquidation risk approaches. It is intended for read-only monitoring and does not execute transactions or modify positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could miss financial-risk alerts if alerting or automation behavior does not match the skill documentation.

Mitigation: Run manual checks and verify scheduled checks before relying on the skill, and keep independent Aave or portfolio alerts enabled for liquidation protection.

Risk: Wallet-position details may be sent to Aave and routed through the user's configured messaging service.

Mitigation: Use private notification channels, limit channel membership, and review whether the wallet address and position summaries are acceptable to share through those services.

Risk: The monitor runs persistently when enabled.

Mitigation: Confirm scheduler status after setup, review logs periodically, and disable monitoring when it is no longer needed.

Risk: Custom alert thresholds may not be honored by the packaged implementation.

Mitigation: Test threshold behavior with representative health-factor values before using custom thresholds for risk decisions.

## Reference(s):

- [Aave V3 GraphQL API Reference](artifact/references/aave-api.md)
- [Configuration Guide](artifact/references/config-guide.md)
- [Cron Integration Guide](artifact/references/cron-integration.md)
- [Security Practices](artifact/SECURITY.md)
- [Aave V3 GraphQL API](https://api.v3.aave.com/graphql)
- [Aave Status](https://status.aave.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style alert text with command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health factor, collateral and debt summaries, borrowed and supplied assets, risk level, timestamp, and setup or scheduler guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
