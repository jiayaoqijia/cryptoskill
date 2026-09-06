## Description: <br>
ERC8004 Agent helps agents create or use Ethereum wallets, register ERC-8004 onchain identities, prepare registration metadata, and authenticate to services with SIWA signed challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limone-eth](https://clawhub.ai/user/limone-eth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to manage ERC-8004 registration state, prepare agent metadata, perform wallet-backed registration, and complete SIWA authentication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can append SIWA session tokens to MEMORY.md, which may be a shared or public markdown file. <br>
Mitigation: Keep session tokens out of MEMORY.md and any shared workspace files; store them in a secret manager or encrypted local storage. <br>
Risk: Wallet registration and bundled full-flow commands can perform funded onchain actions. <br>
Mitigation: Require an explicit human checkpoint before any registration, URI update, or command sequence that spends gas. <br>
Risk: Private-key handling is security-sensitive even when signing is delegated to a keyring proxy. <br>
Mitigation: Use the keyring proxy with a secret manager or encrypted keystore, and avoid raw private keys in environment variables except for tightly controlled CI or migration use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limone-eth/skills/erc8004-agent) <br>
- [ERC-8004 Registration Guide](references/registration-guide.md) <br>
- [SIWA - Sign In With Agent](references/siwa-spec.md) <br>
- [ERC-8004 Contract Addresses and ABIs](references/contract-addresses.md) <br>
- [Security Model](references/security-model.md) <br>
- [SIWA deployment guide](https://siwa.builders.garden/docs/deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, public registration state, metadata JSON, and human checkpoints before funded onchain actions] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
