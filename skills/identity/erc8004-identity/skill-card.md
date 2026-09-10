## Description:

Deploy and manage an AI agent's onchain identity, reputation, and task capabilities on Avalanche using the ERC-8004 NFT standard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijaack](https://clawhub.ai/user/ijaack)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to initialize configuration and run CLI commands that register an ERC-8004 agent identity, deploy validation and task contracts, set agent metadata, set task prices, and check deployment status on Avalanche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys and may lead users to store valuable keys in a plaintext .env file.

Mitigation: Use only a low-funds deployment wallet, prefer keychain or environment injection, and avoid storing a valuable private key in plaintext.

Risk: Deploy, metadata, and price commands can submit irreversible Avalanche mainnet transactions without sufficient confirmation or dry-run guardrails.

Mitigation: Verify the target chain, balances, contract constructor arguments, and agent configuration before running transaction commands; do not run deploy or update commands until confirmation and dry-run gaps are addressed.

Risk: Security evidence reports a deploy bug involving a missing ValidationRegistry constructor argument that can leave users with a paid partial setup.

Mitigation: Fix and review the ValidationRegistry deployment path before use, then test with a low-funds wallet before any mainnet deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ijaack/skills/erc8004-identity)
- [ERC-8004 Spec](https://github.com/ava-labs/ERC-8004)
- [Avalanche Docs](https://docs.avax.network)
- [Example ERC-8004 agent on Snowtrace](https://snowtrace.io/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/1599)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of a Node.js CLI that can write local configuration and deployment files and submit Avalanche transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
