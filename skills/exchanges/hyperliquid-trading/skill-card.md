## Description:

Trade and monitor Hyperliquid perpetual futures, including balances, positions with P&L, market analysis, order placement, market trades, and order cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anajuliabit](https://clawhub.ai/user/anajuliabit)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor Hyperliquid perpetual futures portfolios, analyze market momentum, and prepare or execute trading actions through agent-guided CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Hyperliquid trades and cancel orders when a private key is available.

Mitigation: Use testnet first, keep only minimal funds in a dedicated wallet, and require manual confirmation before every trade or cancel action.

Risk: Market analysis and CoinGecko-based momentum signals can be wrong, stale, or unsuitable for a user's financial situation.

Mitigation: Treat signals as decision support, not financial advice, and independently verify market data, sizing, and risk limits before trading.

Risk: NPM dependencies run in the same environment that may receive a trading private key.

Mitigation: Review or sandbox dependencies before exposing private keys and avoid using a wallet with broad or unnecessary funds.

Risk: The position monitor attempts to write local trading state outside the skill directory.

Mitigation: Inspect or redirect the state path and run the skill with filesystem permissions limited to expected locations.

## Reference(s):

- [Hyperliquid API Reference](artifact/references/api.md)
- [Official Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [Hyperliquid Mainnet API](https://api.hyperliquid.xyz)
- [Hyperliquid Testnet API](https://api.hyperliquid-testnet.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trading operations require HYPERLIQUID_PRIVATE_KEY; read-only portfolio checks can use HYPERLIQUID_ADDRESS.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
