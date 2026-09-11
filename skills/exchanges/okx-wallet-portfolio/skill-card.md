## Description:

Checks wallet balances, token holdings, portfolio value, and DeFi positions for a provided wallet address across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up portfolio balances and token holdings for a specific wallet address across supported chains. It helps present total value, token-level balances, and related follow-up actions while routing broader PnL, DEX history, signal tracking, swap, and meme-scan requests to other skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and run a remote OKX CLI installer or update script before executing portfolio commands.

Mitigation: Preinstall and pin the CLI separately where possible, verify checksums before execution, and review installer/update behavior before deployment.

Risk: Wallet addresses are sent to a portfolio lookup service and returned token metadata may be inaccurate or untrusted.

Mitigation: Use the skill only for intentional address-specific balance checks, avoid submitting sensitive addresses unnecessarily, and verify high-value token contract addresses and prices independently.

Risk: Reference material includes broader wallet analytics behavior than the stated balance-focused purpose.

Mitigation: Limit use to specific wallet-address balance, holding, portfolio value, and DeFi position checks unless broader PnL or DEX-history behavior is explicitly intended.

## Reference(s):

- [CLI command reference](references/cli-reference.md)
- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-wallet-portfolio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and wallet balance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays USD values, token amounts, chain identifiers, and abbreviated contract addresses; treats returned token metadata as untrusted external content.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
