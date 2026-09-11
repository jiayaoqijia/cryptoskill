## Description:

Unified OpenClaw skill for autonomous algo and swing trading workflows: hypothesis generation, screening, technical/sentiment analysis, strategy-specific risk controls, execution gating, P&L and win-rate planning, and self-improvement loops backed by persistent trade data for ML/RL retraining.

This skill is for research and development only.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and external OpenClaw users use this skill to scaffold trading-agent workflows for market research, hypothesis generation, paper trading, risk gating, retention, and controlled promotion planning. Live trading should remain user-governed and strategy-gated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live or autonomous trading controls are under-scoped for real-money use.

Mitigation: Keep deployments in research or paper-trading mode until order validation, free-agent limits, promotion-policy enforcement, kill switches, and retention/deletion controls are strengthened and tested.

Risk: Broker or exchange credentials could enable real-money actions if connected before controls are ready.

Mitigation: Do not connect live broker or exchange credentials until the control gaps identified by security evidence are resolved; use SecretRefs and redaction guidance when configuring non-live providers.

## Reference(s):

- [Strategy Profiles](references/strategy_profiles.md)
- [Data Retention Schema](references/data_retention_schema.md)
- [Autonomy Modes](references/autonomy_modes.md)
- [Adapter Plugin Contract](references/adapter_plugin_contract.md)
- [Strategy Builder and Promotion Gates](references/strategy_builder_and_gates.md)
- [Secrets Management](references/secrets_management.md)
- [System Orchestration](references/system_orchestration.md)
- [OpenClaw Secrets Management](https://docs.openclaw.ai/gateway/secrets#secrets-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces research, paper-trading, risk-gating, retention, and promotion-planning guidance for an agent; live trading requires user governance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
