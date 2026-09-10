## Description:

ERC-8004 Trustless Agents - Register and manage AI agent identities on TRON and BSC blockchains with on-chain reputation tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyderjr](https://clawhub.ai/user/spyderjr)

### License/Terms of Use:

CC0-1.0

## Use Case:

Developers and agent builders use this skill to register, query, update, and submit reputation feedback for AI agent identities on TRON and BNB Smart Chain networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys are required for TRON and BSC write transactions.

Mitigation: Use a testnet or low-value dedicated wallet, prefer environment variables over persistent plaintext key storage, and avoid exposing private keys in logs or shared files.

Risk: Mainnet registration, feedback, and URI update commands can create irreversible blockchain transactions.

Mitigation: Verify the selected network and contract addresses, test on Nile or BSC testnet first, and review every mainnet transaction before signing or running write commands.

## Reference(s):

- [EIP-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [8004.org](https://8004.org)
- [TRON Developer Documentation](https://developers.tron.network/)
- [TronWeb](https://github.com/tronprotocol/tronweb)
- [A2A Protocol](https://a2a-protocol.org/)
- [Awesome ERC-8004](https://github.com/sudeepb02/awesome-erc8004)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require a user-selected chain and network plus a wallet private key.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
