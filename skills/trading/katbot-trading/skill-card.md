## Description:

Live crypto trading on Hyperliquid via Katbot.ai. Signal-triggered research, recommendation, and execution workflow with market intelligence and configurable signal monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claytantor](https://clawhub.ai/user/claytantor)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to configure signal-triggered Hyperliquid paper or live trading workflows through Katbot.ai, review market intelligence and research, request trade recommendations, and execute or close positions after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Hyperliquid agent trading private key may be transmitted to the Katbot API for recommendations, execution, position close, and portfolio timeseries operations.

Mitigation: Warn the user before onboarding or trading calls, proceed only after acknowledgement, use only trusted Katbot API endpoints, and avoid custom KATBOT_BASE_URL values unless the endpoint is controlled and trusted.

Risk: Live trading and unattended automation can place or close real Hyperliquid positions.

Mitigation: Prefer paper or testnet mode first, require explicit confirmation before any live trade or position close, and keep auto_execute_trade disabled unless the user makes a clear informed choice.

Risk: Local identity files can contain the agent trading key and session tokens.

Mitigation: Store identity files outside the project tree with owner-only permissions, never print or summarize secret values, and never place wallet or agent private keys in env files or shell profiles.

## Reference(s):

- [ClawHub Katbot Trading Skill Page](https://clawhub.ai/claytantor/skills/katbot-trading)
- [Katbot API](https://api.katbot.ai)
- [Hyperliquid App](https://app.hyperliquid.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python calls, JSON configuration examples, and API response summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local identity and trigger configuration files during onboarding and setup; trading execution requires explicit user confirmation.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
