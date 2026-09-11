## Description:

Execute cross-chain token trading on EVM and Solana with Particle Network Universal Account SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmomo-ngclubs](https://clawhub.ai/user/0xmomo-ngclubs)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to set up Particle Network universal-account-example and execute or monitor cross-chain EVM and Solana token trades with wallet, slippage, and transaction status handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for wallet authority and stores a private key in a local .env file.

Mitigation: Use a fresh low-value wallet and avoid importing an existing funded private key.

Risk: First-time setup can auto-bind invite code 666666 and run a smoke test.

Mitigation: Set DISABLE_AUTO_INVITE_BIND=1 unless invite binding is intended, and skip or sandbox the smoke test before live use.

Risk: Dynamic retry buys may create more than one transaction attempt when outcomes are ambiguous.

Mitigation: Use fixed slippage for cautious trades, review retry settings before execution, and verify final transaction status before retrying manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xmomo-ngclubs/skills/universal-trading)
- [Publisher profile](https://clawhub.ai/user/0xmomo-ngclubs)
- [Environment Setup](references/env-setup.md)
- [API Reference](references/api.md)
- [Examples](references/examples.md)
- [UniversalX](https://universalx.app)
- [Particle Network dashboard](https://dashboard.particle.network/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup, wallet configuration, trading commands, slippage choices, and transaction status follow-up.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
