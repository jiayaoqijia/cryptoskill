## Description:

ERC8004 Agent helps agents create or manage an Ethereum wallet, register an ERC-8004 onchain identity, build registration metadata, and authenticate to services with SIWA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limone-eth](https://clawhub.ai/user/limone-eth)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register agents under the ERC-8004 Trustless Agents standard, manage public identity state, prepare registration metadata, and perform SIWA authentication. It is intended for workflows where an agent needs an onchain identity and controlled wallet-signing boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad wallet-signing authority could authorize unintended transactions, identity changes, or resets.

Mitigation: Restrict signer operations to approved chains, contracts, functions, and domains, and require clear user confirmation before transactions, resets, and identity changes.

Risk: SIWA session tokens may be written to readable memory.

Mitigation: Store session tokens in a real secret store instead of MEMORY.md and use short-lived sessions.

Risk: Mutable external SDK or CLI installs can change behavior after review.

Mitigation: Use a pinned and verified SDK or CLI version before installing or executing the skill.

Risk: The shared keyring proxy secret could be exposed to general agent context.

Mitigation: Isolate KEYRING_PROXY_SECRET from normal agent context and expose it only to the signing boundary that needs it.

## Reference(s):

- [ERC8004 Agent on ClawHub](https://clawhub.ai/limone-eth/skills/erc8004-agent)
- [ERC-8004 Registration Guide](artifact/references/registration-guide.md)
- [SIWA Protocol Specification](artifact/references/siwa-spec.md)
- [ERC-8004 Contract Addresses and ABIs](artifact/references/contract-addresses.md)
- [Security Model](artifact/references/security-model.md)
- [Keyring Proxy Deployment Guide](https://siwa.builders.garden/docs/deploy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON templates, TypeScript examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose wallet, registration, SIWA, and keyring proxy operations that require user confirmation before transactions or identity changes.]

## Skill Version(s):

0.0.2 (source: server release metadata; artifact frontmatter and package.json remain 0.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
