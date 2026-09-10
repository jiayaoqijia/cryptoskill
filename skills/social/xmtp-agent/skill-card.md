## Description:

Building and extending XMTP agents with the Agent SDK for setup, commands, attachments, reactions, groups, transactions, inline actions, and domain resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanagent](https://clawhub.ai/user/humanagent)

### License/Terms of Use:

MIT

## Use Case:

Developers building XMTP messaging agents use this skill for setup and feature implementation, including command routing, attachments, reactions, group management, USDC transaction flows, inline action menus, and Web3 identity resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction examples create USDC wallet requests and can affect funds if copied without user review.

Mitigation: Add explicit transaction previews and confirmations, keep token amounts as precise integer base units, and validate sender, recipient, network, and amount before sending wallet calls.

Risk: Attachment examples download, decrypt, save, and upload files, including public storage examples.

Mitigation: Sanitize attachment filenames, constrain download directories, enforce size and type limits, and use private or signed storage URLs where appropriate.

Risk: Group examples add members and change roles, which can expose private conversations or grant elevated access.

Mitigation: Require authorization checks before member, admin, super-admin, or group-gating changes.

Risk: Examples use environment secrets and log message bodies or transaction metadata.

Mitigation: Protect .env secrets, avoid logging message bodies or sensitive metadata, and redact addresses or hashes when logs are shared.

## Reference(s):

- [ClawHub XMTP Skill Release](https://clawhub.ai/humanagent/skills/xmtp-agent)
- [Circle Faucet](https://faucet.circle.com)
- [Base Faucet](https://portal.cdp.coinbase.com/products/faucet)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copy-paste XMTP Agent SDK examples that need application-specific review before deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
