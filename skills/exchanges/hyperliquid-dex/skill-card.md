## Description:

Query Hyperliquid DEX for account balances, positions, PnL, and margin data via ClawdBot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipagosfinest](https://clawhub.ai/user/chipagosfinest)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Hyperliquid perpetuals account balances, open positions, unrealized PnL, liquidation prices, leverage, and margin usage for a supplied or configured wallet address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and portfolio details may be sent through ClawdBot infrastructure to Hyperliquid for account and position lookup.

Mitigation: Use only wallet addresses you are comfortable querying through the configured service path, and invoke the skill with explicit Hyperliquid wording when other crypto or portfolio skills are installed.

## Reference(s):

- [Hyperliquid DEX Integration on ClawHub](https://clawhub.ai/chipagosfinest/skills/hyperliquid-dex)
- [Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs)
- [Hyperliquid Public Info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, guidance, API calls]

**Output Format:** [Markdown or plain text summaries of account and position data, with structured JSON handled by the ClawdBot API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account lookup; may use TRADING_WALLET_ADDRESS when no wallet address is supplied.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release, released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
