## Description: <br>
Query EVM chain data via Etherscan API v2 for balances, transactions, token transfers, contract source or ABI, gas prices, event logs, and transaction confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xV4L3NT1N3](https://clawhub.ai/user/0xV4L3NT1N3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to perform read-only on-chain lookups across EVM chains through Etherscan API v2 and confirm whether submitted transactions finalized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if full request URLs containing apikey values are logged or shared. <br>
Mitigation: Prefer an environment variable or secure secret store and avoid logging or sharing full request URLs that include API keys. <br>
Risk: Wallet, transaction, and contract lookups can reveal financial metadata to Etherscan. <br>
Mitigation: Use the skill only when the user is comfortable sending the requested addresses, transactions, and contracts to Etherscan. <br>


## Reference(s): <br>
- [ClawHub Etherscan skill page](https://clawhub.ai/0xV4L3NT1N3/etherscan) <br>
- [Etherscan API documentation](https://docs.etherscan.io/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Etherscan API URLs, pagination guidance, chain ID mapping guidance, and transaction status interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
