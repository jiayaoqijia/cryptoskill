## Description:

Query EVM chain data via Etherscan API v2 for balances, transactions, token transfers, contract source and ABI, gas prices, event logs, and transaction completion checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xv4l3nt1n3](https://clawhub.ai/user/0xv4l3nt1n3)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query supported EVM-chain data through Etherscan API v2 without guessing chains, endpoints, pagination, or transaction finality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send wallet addresses, transaction hashes, and lookup parameters to Etherscan.

Mitigation: Use it only for lookups you are comfortable sharing with Etherscan and avoid submitting unnecessary sensitive addresses or transaction details.

Risk: An Etherscan API key may be stored in a plaintext credentials file under ~/.config/etherscan.

Mitigation: Prefer ETHERSCAN_API_KEY or a credential manager, and restrict file permissions if a local credentials file is used.

Risk: Wrong chain selection or endpoint choice can return empty or misleading lookup results.

Mitigation: Fetch the chain list, map the requested chain explicitly, and verify transaction finality with receipt or transaction-status endpoints.

## Reference(s):

- [Etherscan API v2 LLM documentation](https://docs.etherscan.io/llms.txt)
- [Etherscan API dashboard](https://etherscan.io/apidashboard)
- [ClawHub skill page](https://clawhub.ai/0xv4l3nt1n3/skills/etherscan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include Etherscan API endpoints, chain IDs, pagination advice, and transaction verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
