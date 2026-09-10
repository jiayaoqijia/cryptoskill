## Description:

WalletPilot describes browser wallet automation for AI agents across popular EVM and Solana wallets with configurable permission guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreolf](https://clawhub.ai/user/andreolf)

### License/Terms of Use:


## Use Case:

Developers and external users use WalletPilot to configure an agent-controlled browser wallet for dapp interactions such as connecting, swapping, sending, signing, checking balances, and reviewing history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review identifies WalletPilot as high-impact crypto wallet automation whose claimed safeguards and implementation are not included for review.

Mitigation: Do not fund a wallet or enter a seed phrase until the complete implementation, pinned dependencies, and verifiable enforcement for spend limits, allowlists, revocation, logging, and confirmations are available.

Risk: The skill describes sends, swaps, approvals, and signatures that can move assets or authorize access.

Mitigation: Use only minimal test funds or testnets and require user confirmation for sends, swaps, approvals, and signatures.

## Reference(s):

- [WalletPilot ClawHub listing](https://clawhub.ai/andreolf/skills/wallet-pilot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup, permission configuration, and action command guidance for browser wallet automation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
