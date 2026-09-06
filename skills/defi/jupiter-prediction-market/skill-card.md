## Description: <br>
A Node.js client skill that helps agents query Jupiter Prediction Market data, manage Solana prediction-market positions, claim payouts, and run portfolio and market-scanning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MoltbotTeam](https://clawhub.ai/user/MoltbotTeam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building AI agents use this skill to integrate with Jupiter Prediction Market API workflows for market discovery, order and position management, portfolio monitoring, payout claiming, and risk checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables automated financial actions for prediction-market trading, including order, position, and payout workflows. <br>
Mitigation: Require manual review for wallet signatures and orders, run claim workflows with --dry-run first, and set explicit limits for order size, total exposure, and bulk position changes. <br>
Risk: The skill requires a Jupiter API key and supports loading it from a config/api-key.json file. <br>
Mitigation: Prefer JUPITER_API_KEY from a secret store and avoid committing config/api-key.json. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MoltbotTeam/jupiter-prediction-market) <br>
- [Jupiter Portal](https://portal.jup.ag) <br>
- [Jupiter Prediction API Base](https://api.jup.ag/prediction/v1) <br>
- [API Reference](documentation/api-reference.md) <br>
- [Agent Workflows](documentation/workflows.md) <br>
- [Code Examples](documentation/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code examples and shell commands; API calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUPITER_API_KEY; trading and claim workflows should be reviewed before wallet signing.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
