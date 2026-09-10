## Description:

Register and manage ERC-8004 Identity NFTs on Monad. Use when the agent needs to mint an on-chain identity for CEO Protocol registration or other ERC-8004-integrated protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register an agent identity NFT on Monad, prepare ERC-8004 registration metadata, upload it to IPFS through Pinata, set the token URI, and verify ownership for CEO Protocol or other ERC-8004-integrated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys may be exposed to commands that do not need signing.

Mitigation: Use a minimal environment and provide AGENT_PRIVATE_KEY only to registration or URI-setting commands that must sign transactions.

Risk: Verification can fetch tokenURI metadata from externally controlled IPFS content.

Mitigation: Verify trusted identities only and use trusted, restricted IPFS gateways before relying on fetched metadata.

Risk: Pinata uploads publish agent registration metadata externally.

Mitigation: Review registration JSON for secrets or sensitive operational details before uploading.

Risk: On-chain registration and URI updates spend gas and create persistent blockchain state.

Mitigation: Review transaction details, chain ID, registry address, agent ID, and wallet ownership before broadcasting.

## Reference(s):

- [EIP-8004 Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8004 Registration Schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [Monad ERC-8004 Identity Contract](https://monadscan.com/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- [ClawHub Skill Page](https://clawhub.ai/fabriziogianni7/skills/8004-skill-monad)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ERC-8004 registration JSON, IPFS token URIs, transaction hashes, verification JSON, and a local agent identity Markdown file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
