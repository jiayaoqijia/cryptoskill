## Description:

Register and manage agent identity, reputation, and feedback on Solana and EVM chains using the multi-chain ERC-8004 Agent Registry protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montecrypto999](https://clawhub.ai/user/montecrypto999)

### License/Terms of Use:

MIT

## Use Case:

Developers and autonomous-agent builders use this MCP server to discover, register, update, and evaluate agents across Solana and EVM registry networks. It supports read-only registry lookups as well as wallet-backed write operations such as registration, feedback, metadata updates, and payment-linked reputation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external MCP package can access wallet, signing, mainnet transaction, and storage capabilities.

Mitigation: Pin and audit the package version, run it in a restricted environment with a clean allowlisted environment, keep testnet as the default, and require explicit user confirmation before signing or mainnet transactions.

Risk: Shared or public IPFS storage can make wallet, endpoint, payment, or feedback metadata public and persistent.

Mitigation: Avoid publishing sensitive metadata to shared IPFS storage unless the data is intentionally public and persistent; use controlled storage for private data.

Risk: Wallet-backed write operations can spend real funds or submit irreversible on-chain updates.

Mitigation: Use dry-run or cost-estimation flows before broadcasting, keep wallets minimally funded, and prefer testnets or lower-cost L2 networks for routine work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/montecrypto999/skills/8004-mcp)
- [README](artifact/README.md)
- [AI agent integration guide](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with code examples and JSON-like MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction hashes, unsigned transaction payloads, wallet status, registry records, reputation summaries, feedback records, cost estimates, and troubleshooting guidance.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
