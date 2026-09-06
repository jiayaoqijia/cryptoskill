## Description: <br>
Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sum-li](https://clawhub.ai/user/Sum-li) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading-system operators use this skill to prepare Binance Spot API requests, including market-data queries and authenticated account or order operations. It is suitable for agents that need Binance request parameters, signing guidance, and JSON-oriented API interaction support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through live Binance Spot trading and account-changing actions. <br>
Mitigation: Require fresh explicit user confirmation before every mainnet order, cancellation, or account-changing request. <br>
Risk: The skill requires Binance API keys and secret keys for authenticated endpoints. <br>
Mitigation: Use restricted API keys, disable withdrawals, enable IP allowlisting, and avoid storing raw secrets in agent instruction files. <br>
Risk: Local credential handling guidance may expose sensitive exchange credentials if copied or displayed carelessly. <br>
Mitigation: Mask credentials in responses, keep testnet credentials separate from mainnet, and prefer testnet validation before mainnet use. <br>


## Reference(s): <br>
- [Authentication reference](references/authentication.md) <br>
- [Binance Spot API mainnet](https://api.binance.com) <br>
- [Binance Spot testnet](https://testnet.binance.vision) <br>
- [ClawHub skill page](https://clawhub.ai/Sum-li/binance-spot-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated endpoints require Binance API credentials and signed request parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
