## Description:

Virtuals Protocol integration for OpenClaw. Create, manage and trade tokenized AI agents on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rojasjuniore](https://clawhub.ai/user/rojasjuniore)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to inspect Virtuals Protocol token and agent information, check wallet balances, and receive command-line guidance for configuring a wallet and creating tokenized AI agents on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a crypto private key and persists it in a local plaintext configuration file.

Mitigation: Use only a throwaway testnet wallet, do not provide a real mainnet private key, and treat any key already entered through the documented command as exposed.

Risk: The skill advertises trading and agent-creation capabilities that the inspected release does not fully implement.

Mitigation: Verify command behavior before relying on it, and use the official Virtuals web applications for creation or trading flows until the implementation is confirmed.

Risk: Market-data and wallet-balance output can influence crypto decisions.

Mitigation: Confirm balances, prices, and transaction requirements with authoritative sources before moving funds or acting on the output.

## Reference(s):

- [Virtuals homepage](https://virtuals.io)
- [Virtuals app](https://app.virtuals.io)
- [Virtuals agent creation](https://fun.virtuals.io)
- [Virtuals whitepaper](https://whitepaper.virtuals.io)
- [GAME SDK](https://github.com/game-by-virtuals/game-node)
- [ClawHub skill page](https://clawhub.ai/rojasjuniore/skills/virtuals)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet configuration steps and blockchain/API query results; trading and create-agent flows should be treated as advisory unless verified.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
