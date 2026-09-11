## Description:

Autonomous prediction market agent that analyzes markets, researches news, and identifies trading opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search Polymarket markets, gather market data, research related news, estimate edge, and prepare or execute user-approved trades through the poly CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a wallet private key and the security scan notes unsafe secret handling.

Mitigation: Use only a dedicated low-value wallet, avoid commands that print secrets, and require secret redaction plus safer key storage before meaningful funds are used.

Risk: The skill can place live Polymarket orders with weak safeguards.

Mitigation: Keep autonomous mode disabled, require explicit per-trade confirmation, add dry-run behavior, validate token, price, and size inputs, and enforce per-trade limits.

Risk: Market recommendations may rely on incomplete news, social sentiment, or ambiguous market resolution criteria.

Mitigation: Verify sources, market liquidity, and resolution rules before trading, and keep position sizes small relative to the user's bankroll.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bombfuock/skills/polymarket-trading-bot)
- [Configured Skill Homepage](https://clawdhub.com/polymarket-agent)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown analysis reports with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Polymarket APIs, web search, Clawdbot config, and live trading commands when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
