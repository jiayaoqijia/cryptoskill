## Description: <br>
Use The Graph Subgraph MCP through UXC via native SSE with a fixed linked command for subgraph discovery, schema retrieval, deployment selection, and GraphQL query execution with help-first inspection and explicit auth handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to discover The Graph subgraphs, inspect schemas, choose stable deployments, and execute scoped GraphQL queries through The Graph Subgraph MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a The Graph Gateway API key for authenticated MCP calls. <br>
Mitigation: Use a dedicated or revocable API key and store it through the documented UXC credential binding rather than in prompts or logs. <br>
Risk: The fixed local command name could conflict with an existing command. <br>
Mitigation: Check `command -v thegraph-mcp-cli` before linking and stop for maintainer review if the command cannot be safely reused. <br>
Risk: Unscoped GraphQL queries can fetch more data than intended. <br>
Mitigation: Inspect operation help and schema first, then start with `_meta` or narrow selections using limits and filters. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [The Graph Subgraph MCP documentation](https://thegraph.com/docs/en/ai-suite/subgraph-mcp/introduction/) <br>
- [ClawHub release page](https://clawhub.ai/jolestar/thegraph-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and GraphQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses UXC JSON envelopes and expects The Graph Gateway API key handling through configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
