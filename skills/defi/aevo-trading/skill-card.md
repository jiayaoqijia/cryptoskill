## Description:

AI trading assistant for AEVO, a decentralized derivatives exchange, connecting MCP-compatible clients to tools for market data, portfolio management, order execution, risk analysis, and options strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yichulau](https://clawhub.ai/user/yichulau)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze AEVO crypto derivatives markets, review portfolio risk, and prepare or execute AEVO trades through an MCP-compatible client. It supports market analysis, position management, order workflows, options strategies, hedging, and credential-aware onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive exchange credentials and private-key material.

Mitigation: Prefer testnet or read-only credentials first, avoid pasting wallet private keys into chat, and use limited, revocable AEVO keys.

Risk: Confirmed trading or cancellation actions can place, modify, or cancel real orders and affect funds.

Mitigation: Require explicit user confirmation, run pre-trade risk checks, preview with dry-run order building when possible, and verify order state after execution.

Risk: The skill depends on an externally installed MCP server package or hosted MCP endpoint.

Mitigation: Pin and verify the MCP server package or endpoint before use and only enable live trading after reviewing the server and credential flow.

## Reference(s):

- [AEVO Trading Skill README](README.md)
- [AEVO MCP Tools Reference](references/tools.md)
- [Risk Management Rules](references/risk-rules.md)
- [Common Trading Workflows](references/workflows.md)
- [Options Strategy Reference](references/options.md)
- [AEVO Instrument Naming Conventions](references/instruments.md)
- [AEVO Exchange](https://aevo.xyz)
- [AEVO API Docs](https://docs.aevo.xyz)
- [MCP Server Package](https://pypi.org/project/mcp-aevo-server/)
- [ClawHub Skill Page](https://clawhub.ai/yichulau/skills/aevo-trading-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, tool-call plans, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AEVO MCP tools for market data, account review, risk checks, order construction, order execution, cancellation, and strategy workflows; live trading actions can affect funds and should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
