## Description: <br>
ERC-8004 Trustless Agents helps agents and developers register on-chain identities, query ERC-8004 registries, submit reputation feedback, and manage registration URIs on Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sp0oby](https://clawhub.ai/user/sp0oby) <br>

### License/Terms of Use: <br>
CC0 - Public Domain <br>


## Use Case: <br>
Developers and engineers use this skill to prepare ERC-8004 registration metadata, interact with Identity and Reputation registries, and manage agent reputation records on Ethereum mainnet or Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live blockchain transactions can spend funds or permanently change on-chain registration, URI, or reputation records. <br>
Mitigation: Use Sepolia or dry-run mode first, review the network, registry, agent ID, URI, and transaction details before signing, and use a dedicated low-value wallet. <br>
Risk: The scripts can use raw private keys from PRIVATE_KEY, command-line key arguments, or a local deployer key file. <br>
Mitigation: Use a dedicated low-value key, avoid primary funded wallets, restrict local key-file permissions, and avoid exposing secrets in shell history or logs. <br>
Risk: Pinata/IPFS uploads and on-chain URIs or feedback can be public and difficult to remove. <br>
Mitigation: Do not include secrets, private endpoints, personal data, or sensitive operational details in registration JSON, feedback URIs, endpoints, or uploaded files. <br>
Risk: The workflow depends on external tooling and RPC endpoints, including Foundry/cast, jq, public RPC URLs, and Pinata for uploads. <br>
Mitigation: Verify the Foundry installation source and binaries, confirm RPC and contract addresses before use, and review command output before broadcasting transactions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sp0oby/skills/erc-8004) <br>
- [EIP-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 Official Website](https://8004.org) <br>
- [ERC-8004 Reference Implementation](https://github.com/erc-8004/erc-8004-contracts) <br>
- [A2A Protocol](https://a2a-protocol.org/) <br>
- [ERC-721 Specification](https://eips.ethereum.org/EIPS/eip-721) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that sign and broadcast Ethereum transactions; dry-run modes are available for transaction simulation in supported scripts.] <br>

## Skill Version(s): <br>
1.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
