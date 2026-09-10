## Description:

Creates Farcaster accounts, configures profiles, manages signer credentials, and posts casts through an agent-guided workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishavmukherji](https://clawhub.ai/user/rishavmukherji)

### License/Terms of Use:


## Use Case:

Developers and external agent operators use this skill to create and manage Farcaster identities, register usernames, set profile details, and publish casts from an autonomous agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles funded crypto wallets and Farcaster accounts.

Mitigation: Use throwaway wallets with minimal funds and review every on-chain transaction before authorizing it.

Risk: Private keys and signer credentials may be saved in plaintext.

Mitigation: Disable auto-save or use secure local secret storage before using the skill with any valuable account.

Risk: The install command runs npm install outside the reviewed artifact.

Mitigation: Review the package manifest, lockfile, and source repository before installing dependencies.

Risk: Casts and on-chain actions are public and difficult to undo.

Mitigation: Confirm cast text, profile changes, and transaction intent before running commands that publish or transact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishavmukherji/skills/farcaster-agent)
- [Farcaster Agent source repository](https://github.com/rishavmukherji/farcaster-agent)
- [Neynar Hub API](https://hub-api.neynar.com)
- [Neynar REST API](https://api.neynar.com)
- [Farcaster Fname Registry](https://fnames.farcaster.xyz)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup, credential handling, API endpoint, profile configuration, and cast publishing guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
