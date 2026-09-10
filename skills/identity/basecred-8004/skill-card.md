## Description:

Interactive ERC-8004 agent registration via chat. Guides users through a prefill form, shows draft, confirms, then registers on-chain using agent0-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmedas69](https://clawhub.ai/user/callmedas69)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent operators use this skill to collect registration metadata, preview it, and submit ERC-8004 agent registrations, updates, searches, or feedback on supported EVM mainnets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use raw wallet private keys from environment variables for signed on-chain actions.

Mitigation: Use a dedicated low-value wallet, avoid primary funded wallets, and prefer pasting a public address or using an external signer when possible.

Risk: Registration, update, and feedback flows can publish persistent on-chain data and spend gas.

Mitigation: Review the draft carefully, require explicit confirmation before execution, and use dry-run or search/update flows before creating duplicate registrations.

Risk: An untrusted .env file could provide signing credentials or RPC settings to the agent.

Mitigation: Only run the skill in trusted workspaces and inspect environment files before allowing the agent to source them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/callmedas69/skills/basecred-8004-registration)
- [ERC-8004](https://8004.org)
- [OpenClaw](https://openclaw.ai)
- [Agent0 SDK](https://github.com/agent0lab/agent0-ts)
- [Supported Chains](references/chains.md)
- [Agent0 SDK Reference](references/sdk-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON registration data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute on-chain registration, update, search, and feedback commands after user confirmation.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
