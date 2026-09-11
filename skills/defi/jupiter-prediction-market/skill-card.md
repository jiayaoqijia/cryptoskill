## Description:

Complete Node.js client for Jupiter Prediction Market API for agents that query prediction market data, manage trading positions, claim payouts, and build market scanning, portfolio monitoring, and risk workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotteam](https://clawhub.ai/user/moltbotteam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to integrate with Jupiter Prediction Market on Solana for market discovery, order and position operations, payout claiming, and portfolio health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports live financial actions, including creating orders, closing positions, and claiming payouts.

Mitigation: Require human approval before any order, claim, or position-closing action, and avoid unattended auto-claim or close-position workflows.

Risk: The security summary flags local API-key storage without enough guardrails.

Mitigation: Prefer the JUPITER_API_KEY environment variable over config/api-key.json, keep local key files out of shared workspaces, and do not commit secrets.

Risk: Automated market scanning and opportunity recommendations can encourage financial decisions without sufficient review.

Mitigation: Treat generated opportunities as analysis only, verify market data independently, and enforce position-size and total-exposure limits before trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltbotteam/skills/jupiter-prediction-market)
- [Jupiter Portal](https://portal.jup.ag)
- [Jupiter Prediction API](https://api.jup.ag/prediction/v1)
- [API Reference](documentation/api-reference.md)
- [Code Examples](documentation/examples.md)
- [Agent Workflows](documentation/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request guidance, market and portfolio summaries, and transaction-oriented workflow recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact package.json and SKILL.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
