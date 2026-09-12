## Description:

Gate DEX read-only market data skill for prices, K-lines, rankings, holder analysis, liquidity, and token risk checks without executing transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and analyze Gate DEX market data, including token prices, candlestick data, rankings, token risk reports, holders, liquidity, and volume. It is not intended for swaps, wallet authentication, or transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote runtime instructions.

Mitigation: Review the referenced runtime rules before use and pin or vendor reviewed rules where operational consistency is required.

Risk: OpenAPI mode stores API credentials in a home-directory configuration file and signs API actions.

Mitigation: Prefer MCP mode for market queries, use scoped user-owned read-only credentials for OpenAPI mode, remove embedded defaults, and protect the credential file with owner-only permissions.

Risk: The installer may overwrite an existing persistent agent instruction file.

Mitigation: Back up or inspect any existing CLAUDE.md before running the installer from a project directory.

## Reference(s):

- [Gate DEX Market Skill Page](https://clawhub.ai/gate-exchange/skills/gate-dex-market)
- [Gate Publisher Profile](https://clawhub.ai/user/gate-exchange)
- [Gate DEX Market - MCP Mode Detailed Skill](references/mcp.md)
- [Market OpenAPI Shared: Environment Detection + API Call](references/openapi/_shared.md)
- [Market OpenAPI: Token Data Actions](references/openapi/token-data.md)
- [Market OpenAPI: Market Data Actions](references/openapi/market-data.md)
- [Gate DEX MCP Endpoint](https://api.gatemcp.ai/mcp/dex)
- [Gate DEX OpenAPI Endpoint](https://openapi.gateweb3.cc/api/v1/dex)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with API call instructions, command examples, and summarized market data responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP mode is read-only and does not require credentials for market queries; OpenAPI mode uses a home-directory credential file and signed requests when explicitly requested.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 2026.3.24-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
