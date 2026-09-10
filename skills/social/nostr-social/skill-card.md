## Description:

Nostr Social lets an OpenClaw agent create and use its own Nostr identity, Cashu ecash wallet, profile, posts, DMs, follows, reactions, and zaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnyeager](https://clawhub.ai/user/shawnyeager)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent a self-managed Nostr social presence with local cryptographic identity setup, profile management, messaging, posting, follows, and wallet-backed zaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent a public Nostr identity and spend-capable wallet.

Mitigation: Install only when that authority is acceptable, protect ~/.cocod/config.json and ~/.nostr/secret.key as high-value secrets, and avoid funding the wallet until payment confirmation behavior has been reviewed.

Risk: The security summary flags under-scoped install, network, and file behaviors that deserve review before use.

Mitigation: Review the install flow and local file access before deployment, and prefer reviewed, pinned installs over documented clone or unpinned npx flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawnyeager/skills/nostr-social)
- [Publisher Profile](https://clawhub.ai/user/shawnyeager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup and operating instructions for Nostr identity, wallet, social actions, and local configuration.]

## Skill Version(s):

1.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
