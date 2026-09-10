## Description:

Manage crypto wallets, transfers, swaps, and balances via the Sponge Wallet API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabluthra](https://clawhub.ai/user/rishabluthra)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide agents through Sponge Wallet REST API operations, including wallet registration, balance checks, transfers, swaps, bridges, Polymarket actions, Amazon checkout, and x402 paid fetches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward real-money actions, including transfers, trading, bridge operations, withdrawals, checkout, and paid x402 fetches.

Mitigation: Use low-balance or tightly scoped API keys, prefer testnet, and require explicit human confirmation before any funds movement, trade, purchase, or paid fetch.

Risk: SPONGE_API_KEY exposure could give broad wallet authority.

Mitigation: Restrict permissions on ~/.spongewallet/credentials.json, avoid broad environment exports, keep keys out of logs and screenshots, and rotate keys if exposure is suspected.

Risk: x402 URLs and Amazon checkout inputs can cause the agent to spend funds or place orders.

Mitigation: Treat x402 URLs and checkout inputs as high-risk, verify destination and purchase details, and use dry-run checkout behavior when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishabluthra/skills/wallet-skills)
- [Sponge Wallet homepage](https://wallet.paysponge.com)
- [Sponge Wallet API base](https://api.wallet.paysponge.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API endpoint tables, JSON examples, and curl command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Doc-only skill; agents call the Sponge Wallet REST API directly and use SPONGE_API_KEY for authenticated requests.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
