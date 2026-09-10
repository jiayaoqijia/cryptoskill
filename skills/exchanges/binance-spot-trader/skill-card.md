## Description:

Autonomous Binance spot trading bot that combines technical indicators with LLM sentiment analysis to place and track trades across Binance spot pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanthbellary](https://clawhub.ai/user/srikanthbellary)

### License/Terms of Use:


## Use Case:

External developers and trading operators use this skill to configure and run an automated Binance spot trading workflow with momentum, mean reversion, or DCA strategies and optional LLM sentiment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Binance spot market orders when configured with valid Binance API credentials.

Mitigation: Use API keys with withdrawals disabled, IP restrictions, and limited funds; verify or add dry-run mode and confirmation gates before live use.

Risk: Documented trading safety limits are incomplete or unenforced for position caps, DCA scheduling, exchange filters, and stop-loss or take-profit behavior.

Mitigation: Review and implement those controls before enabling cron execution or using real funds.

Risk: API keys are loaded from environment or .env files and may be stored on disk.

Mitigation: Restrict file permissions, secure the host, and rotate keys if the environment or logs are exposed.

## Reference(s):

- [Binance REST API Reference](references/binance-api.md)
- [Technical Indicators](references/indicators.md)
- [Publisher homepage](https://github.com/srikanthbellary)
- [ClawHub skill page](https://clawhub.ai/srikanthbellary/skills/binance-spot-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live Binance spot market orders and write trade history to trades.jsonl when configured with valid API keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
