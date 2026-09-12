## Description:

Use Gate MCP through UXC for public spot and futures market data workflows with a fixed streamable-http endpoint and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data analysts use this skill to inspect and run read-only Gate MCP public spot and futures market-data commands with help-first discovery and JSON output parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries are sent to Gate's remote MCP endpoint.

Mitigation: Use the skill only when remote public market-data requests to Gate are acceptable.

Risk: The reusable gate-mcp-cli link could be used outside the documented read-only workflow.

Mitigation: Keep usage limited to the documented /mcp endpoint and avoid trading, wallet, account, funding, and API-key workflows.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Official Gate for AI / MCP docs](https://www.gate.com/gate-mcp-skills)
- [Gate MCP setup article](https://www.gate.com/ru/help/gateforai/gateforaibasics/50102/gate-for-ai-one-click-integration-with-major-ai-agents-no-api-keys-required-zero-barriers)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and JSON-oriented output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to public market-data reads through the fixed Gate MCP streamable-http endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
