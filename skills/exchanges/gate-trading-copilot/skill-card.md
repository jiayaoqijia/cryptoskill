## Description: <br>
Orchestrates cryptocurrency trade judgment, risk control, order drafting, explicit-confirmation execution, and post-trade management on Gate Exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users and trading agents use this skill to analyze a specific crypto trade, produce a risk-gated Trading Brief and Order Draft, and execute or manage spot and USDT perpetual futures actions only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live trading accounts through order placement, cancellation, amendment, close, reverse, leverage, or margin-mode actions. <br>
Mitigation: Use a restricted Gate API key, preferably without withdrawal permission, and require fresh explicit confirmation for every write action. <br>
Risk: The release evidence flags unclear boundaries around unsupported triggers and products. <br>
Mitigation: Keep use to supported spot and USDT perpetual futures workflows; block Alpha, TradFi, margin borrowing, DeFi, options, and other unsupported products unless future evidence explicitly supports them. <br>
Risk: Runtime behavior depends partly on a remote mutable rules file and available MCP tools. <br>
Mitigation: Review the runtime rules at use time, verify the current tool surface before relying on it, and stay in analysis-only or draft-only mode when required tools or authentication are unavailable. <br>


## Reference(s): <br>
- [Gate Exchange Trading Copilot on ClawHub](https://clawhub.ai/gate-exchange/gate-exchange-trading-copilot) <br>
- [MCP orchestration specification](references/mcp.md) <br>
- [Routing and analysis](references/routing-and-analysis.md) <br>
- [Execution and guardrails](references/execution-and-guardrails.md) <br>
- [Runtime dependencies](references/runtime-dependencies.md) <br>
- [Scenario examples](references/scenarios.md) <br>
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown trading briefs, order drafts, execution results, and concise guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before trade actions; execution depends on available Gate MCP tools and authentication.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
