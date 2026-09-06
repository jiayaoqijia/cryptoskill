## Description: <br>
Aave Liquidation Monitor monitors Aave V3 borrow positions across supported chains, checks health factor and collateral/debt data, and sends alerts when liquidation risk crosses configured thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgramajo4](https://clawhub.ai/user/jgramajo4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External DeFi users and operators use this skill to monitor Aave V3 borrowing health, receive liquidation-risk alerts, and tune thresholds or check intervals for positions they manage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet checks, health factors, alerts, and logs can reveal sensitive financial metadata. <br>
Mitigation: Use a private notification channel, review OpenClaw log retention, and avoid sharing alert output publicly. <br>
Risk: Periodic monitoring continues until disabled and may keep querying Aave or sending alerts after it is no longer needed. <br>
Mitigation: Disable or remove the cron job when monitoring is no longer required. <br>
Risk: Alerts depend on the selected messaging channel and OpenClaw routing configuration. <br>
Mitigation: Configure and test Telegram, Discord, or Slack delivery before relying on the monitor for liquidation-risk notifications. <br>


## Reference(s): <br>
- [Aave V3 GraphQL API Reference](references/aave-api.md) <br>
- [Configuration Guide](references/config-guide.md) <br>
- [Cron Integration Guide](references/cron-integration.md) <br>
- [Security Practices](SECURITY.md) <br>
- [Aave V3 GraphQL API](https://api.v3.aave.com/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, command examples, JSON configuration, and alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only monitoring results, risk-level summaries, and scheduled alert messages routed through the user's configured OpenClaw channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
