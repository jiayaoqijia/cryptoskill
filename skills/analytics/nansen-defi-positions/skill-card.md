## Description:

Helps an agent summarize a wallet's DeFi positions, assets, debts, rewards, and token balances across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet analysts and developers use this skill to inspect DeFi exposure by protocol and chain alongside spot token balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet portfolio queries use the agent's Nansen CLI account or API key.

Mitigation: Review the nansen-cli package source and grant only the account or API-key access you are comfortable sharing.

Risk: An empty DeFi response may not reflect all wallet holdings.

Mitigation: Check spot balances alongside DeFi positions and explain when no tracked positions are returned.

## Reference(s):

- [Nansen DeFi Positions skill listing](https://clawhub.ai/nansen-devops/skills/nansen-defi-positions)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with bash commands and wallet exposure summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports protocol, chain, asset, debt, and reward values where available; untracked wallets may have no DeFi positions.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
