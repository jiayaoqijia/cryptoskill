## Description:

Builds dapps on Monad blockchain for contract deployment, frontend setup with viem/wagmi, and contract verification on Monad testnet or mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[portdeveloper](https://clawhub.ai/user/portdeveloper)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build Monad dapps, deploy smart contracts with Foundry, configure frontend integrations, and verify deployed contracts across Monad explorers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that wallet private keys may be created or stored by the skill.

Mitigation: Use testnet wallets by default, avoid funded or mainnet wallets unless explicitly approved, and choose a secure storage method with restrictive permissions.

Risk: The security review notes that contract source code and build metadata may be sent to a third-party verification API.

Mitigation: Confirm the upload contents and that agents.devnads.com is an acceptable intermediary before contract verification.

## Reference(s):

- [Monad documentation](https://docs.monad.xyz)
- [Monad LLM documentation index](https://docs.monad.xyz/llms.txt)
- [ClawHub skill page](https://clawhub.ai/portdeveloper/skills/monad-development)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash, Solidity, TOML, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment workflows, wallet handling guidance, and contract verification requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
