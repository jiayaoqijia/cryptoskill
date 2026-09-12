## Description:

Use CoinMarketCap MCP through UXC for crypto market quotes, technical analysis, on-chain metrics, global market overview, narratives, macro events, news, and semantic search with help-first schema inspection and API-key auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure UXC access to CoinMarketCap MCP and run read-only cryptocurrency market data, metrics, technical analysis, news, narrative, and semantic search queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party MCP service and the UXC command-line tool.

Mitigation: Confirm that CoinMarketCap MCP and UXC are trusted before installing or running the skill.

Risk: Authenticated CoinMarketCap calls may consume account quota or require a paid plan.

Mitigation: Use a user-controlled CoinMarketCap API key or secret-manager path and verify account tier, quota, and plan-gated endpoint access before broad queries.

Risk: API credentials could be exposed if copied into prompts, logs, or unprotected files.

Mitigation: Provide the API key through the documented environment variable or secret-manager binding rather than embedding the secret in commands or skill text.

Risk: Users may mistake market-data access for trading authority.

Mitigation: Treat the skill as read-only market-data guidance; it does not request trading authority or provide order-routing access.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key setup steps and read-only query patterns; authenticated calls may consume CoinMarketCap quota.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
