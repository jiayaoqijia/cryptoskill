## Description:

ERC-8004 Trustless Agents helps agents register, discover, query, update, and submit reputation feedback for ERC-8004 identities on Ethereum networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sp0oby](https://clawhub.ai/user/sp0oby)

### License/Terms of Use:

CC0

## Use Case:

Developers and agent operators use this skill to work with ERC-8004 agent identity, reputation, and validation registries. It supports preparing registration metadata, querying registered agents, updating agent URIs, and submitting reputation feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can submit real Ethereum transactions for registration, URI updates, and feedback.

Mitigation: Use Sepolia and dry-run modes first, verify the target network and contract addresses, and treat mainnet commands as irreversible transactions that may cost ETH.

Risk: Wallet private keys are accepted through environment variables, command-line flags, or a documented default file path.

Mitigation: Use a dedicated low-balance wallet, avoid command-line private key arguments, and do not store broad-use deployer keys in the default wallet path.

Risk: The setup guidance includes installing Foundry by piping a remote script into bash.

Mitigation: Install Foundry through a verifiable method and review installer integrity before execution.

Risk: IPFS uploads use a Pinata JWT when available.

Mitigation: Scope and rotate Pinata credentials, avoid committing them to files, and review uploaded registration metadata before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sp0oby/skills/erc-8004)
- [EIP-8004 specification](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8004 website](https://8004.org)
- [ERC-8004 reference implementation](https://github.com/erc-8004/erc-8004-contracts)
- [A2A Protocol](https://a2a-protocol.org/)
- [Ethereum Magicians discussion](https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local shell scripts that query Ethereum RPC endpoints or submit transactions when the user supplies wallet credentials.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
