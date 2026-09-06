## Description: <br>
Unified OpenClaw skill for autonomous algo and swing trading workflows: hypothesis generation, screening, technical/sentiment analysis, strategy-specific risk controls, execution gating, P&L and win-rate planning, and self-improvement loops backed by persistent trade data for ML/RL retraining. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw agents use this skill to scaffold trading-agent workflows for market research, hypothesis creation, risk-gated paper execution, reporting, and iterative strategy improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading automation can create real financial exposure if live broker credentials are configured or free-agent live mode is enabled. <br>
Mitigation: Keep the workflow in paper mode by default, review live credentials before use, require hard exposure limits, and maintain manual kill switches. <br>
Risk: The skill stores local trading databases, reports, raw snapshots, and logs that may contain sensitive operational history. <br>
Mitigation: Define retention and deletion rules before deployment and apply the included redaction and secret-reference guidance to logs and reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscraters/openclaw-trading-suite) <br>
- [OpenClaw Gateway secrets management](https://docs.openclaw.ai/gateway/secrets#secrets-management) <br>
- [Strategy profiles](references/strategy_profiles.md) <br>
- [Data retention schema](references/data_retention_schema.md) <br>
- [Autonomy modes](references/autonomy_modes.md) <br>
- [Adapter plugin contract](references/adapter_plugin_contract.md) <br>
- [Strategy builder and gates](references/strategy_builder_and_gates.md) <br>
- [Secrets management](references/secrets_management.md) <br>
- [System orchestration](references/system_orchestration.md) <br>
- [Public release scope](references/public_release_scope.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, configuration examples, and structured reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce trading hypotheses, risk-gate decisions, overnight research summaries, persistence schemas, and implementation scaffolding.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
