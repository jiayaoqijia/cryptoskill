## Description:

An AI agent skill that orchestrates cryptocurrency trade judgment, risk control, order drafting, explicit confirmation, execution, and post-trade management on Gate Exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to move from Gate Exchange market analysis to a risk-gated trading brief, order draft, explicit confirmation, execution, and post-trade verification for spot and USDT perpetual futures workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real trading authority can place or modify orders when authenticated Gate execution tools are available.

Mitigation: Use narrowly scoped Gate API permissions and an agent/runtime that enforces confirmations outside natural-language skill text before any write action.

Risk: The release evidence says the manifest overstates some supported capabilities.

Mitigation: Treat the supported execution scope as spot and USDT perpetual futures only; block options, Alpha trading, DeFi execution, copy trading, wealth products, and unsupported products.

Risk: Mutable external runtime rules or missing MCP tools can change the quality of analysis and execution coverage.

Mitigation: Verify the current runtime tool list before relying on a tool, label sparse results as supporting context, and block new-trade drafting when required analysis or execution surfaces are unavailable.

Risk: Market analysis and order drafts may be mistaken for certainty or automatic trading authority.

Mitigation: Require a Trading Brief with GO, CAUTION, or BLOCK; produce an Order Draft only when hard blocks are absent; execute only after fresh explicit confirmation.

## Reference(s):

- [Gate Exchange Trading Copilot skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-trading-copilot)
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [MCP orchestration specification](references/mcp.md)
- [Runtime dependencies](references/runtime-dependencies.md)
- [Scenarios and prompt examples](references/scenarios.md)
- [Routing and analysis](references/routing-and-analysis.md)
- [Execution and guardrails](references/execution-and-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown trading briefs, order drafts, execution results, and guidance with structured MCP tool-use recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before private trading actions; unsupported or under-evidenced flows stay in analysis-only or draft-only mode.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
