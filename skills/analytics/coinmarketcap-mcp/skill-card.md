## Description: <br>
Use CoinMarketCap MCP through UXC for crypto market quotes, technical analysis, on-chain metrics, global market overview, narratives, macro events, news, and semantic search with help-first schema inspection and API-key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and query CoinMarketCap MCP through uxc for read-only cryptocurrency quotes, market metrics, narratives, news, and semantic search. It emphasizes help-first schema inspection, API-key setup, and focused read workflows before broader or plan-gated calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CoinMarketCap MCP requires an API key, and incorrect credential handling could expose or misuse the key. <br>
Mitigation: Use a dedicated CoinMarketCap API key, store it through uxc credential binding or a secret manager, and verify the binding targets only https://mcp.coinmarketcap.com/mcp. <br>
Risk: Queries may reveal confidential portfolio, trading, or business strategy information to the external data service. <br>
Mitigation: Avoid sending confidential portfolio details or business strategy in searches; keep queries focused and use non-sensitive identifiers where possible. <br>
Risk: CoinMarketCap plan limits, quotas, or pay-per-call scope can affect availability or cost. <br>
Mitigation: Start with focused read-only requests, inspect operation help before use, and verify the account tier before retrying quota or plan-gated failures. <br>
Risk: The upstream MCP tool surface can change independently of this skill. <br>
Mitigation: Run help-first schema inspection for each operation before execution and avoid assuming argument names from memory. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/coinmarketcap-mcp-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jolestar) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect live MCP operation schemas before execution and to parse the JSON envelope returned by uxc.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
