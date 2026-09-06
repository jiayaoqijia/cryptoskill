## Description: <br>
Register and manage ERC-8004 Identity NFTs on Monad for CEO Protocol registration and other ERC-8004-integrated flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to mint and manage an ERC-8004 on-chain identity NFT, publish registration metadata, and preserve the resulting agent identity for CEO Protocol onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadcast wallet-signed transactions to register identities and update agent URIs. <br>
Mitigation: Use a dedicated wallet with limited funds and confirm the transaction details before broadcasting. <br>
Risk: Identity metadata uploaded to IPFS may be public and difficult to remove. <br>
Mitigation: Review registration metadata before upload and avoid secrets, private endpoint details, or sensitive personal data. <br>
Risk: The scripted flow requires wallet and Pinata credentials. <br>
Mitigation: Provide credentials only in a trusted environment and avoid using a primary wallet private key. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fabriziogianni7/8004-skill-monad) <br>
- [EIP-8004 Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 Identity contract on MonadScan](https://monadscan.com/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create JSON registration files and an agent identity Markdown file during scripted workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
