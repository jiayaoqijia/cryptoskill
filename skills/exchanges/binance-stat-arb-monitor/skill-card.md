## Description:

Monitors Binance ETH/BTC perpetual futures price ratios, calculates z-scores, generates mean-reversion trading signals, and can send alerts to Telegram or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemonea](https://clawhub.ai/user/lemonea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quant researchers, and trading operations users can use this skill to configure and run an ETH/BTC statistical-arbitrage monitor that emits signal files and optional chat alerts. The alerts are informational and should be reviewed before any live trading action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals and PnL estimates may be incorrect, stale, or unsuitable for live market conditions.

Mitigation: Treat alerts as informational, validate the strategy on test data or testnet, and require human review before acting with real funds.

Risk: Telegram bot tokens, chat IDs, Feishu webhooks, and cron logs can expose sensitive notification channels.

Mitigation: Keep tokens and webhooks private, restrict log permissions, and avoid committing live credentials in configuration files.

Risk: Binance API access may be unavailable or region-limited, and fallback mock data can generate non-market signals.

Mitigation: Confirm the active data source before relying on output and clearly separate mock or testnet runs from production monitoring.

Risk: Unpinned dependencies can change behavior between installations.

Mitigation: Pin and review dependency versions before production use.

## Reference(s):

- [Binance API reference](references/binance_api.md)
- [Statistical arbitrage theory](references/stat_arb_theory.md)
- [Binance Futures API documentation](https://binance-docs.github.io/apidocs/futures/cn/)
- [ClawHub skill page](https://clawhub.ai/lemonea/skills/binance-stat-arb-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance, shell commands, JSON signal files, and plain-text alert messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signal JSON includes timestamp, signal type, direction, z-score, ratio, thresholds, prices, recommendation, estimated PnL, strength, reason, and volatility.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
