## Description:

Guides agents to discover The Graph subgraphs, inspect schemas, select deployments, and run scoped GraphQL queries through The Graph MCP with explicit API-key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to explore The Graph subgraphs, inspect schemas, choose stable deployments, and run small GraphQL queries after confirming operation help and authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to store or reference a The Graph API key in uxc and create a scoped auth binding.

Mitigation: Review the local uxc credential and auth binding entries before use, and rotate or remove the credential when access changes.

Risk: The skill creates or uses a local linked command named thegraph-mcp-cli.

Mitigation: Confirm the command name does not conflict with an existing local tool before linking, and remove the link during uninstall if it is no longer needed.

Risk: GraphQL queries against subgraphs can be too broad or target an unstable latest-version reference.

Mitigation: Inspect operation help and schema first, prefer deployment-oriented identifiers for stable workflows, and start with narrow queries using filters, limits, and required fields only.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [The Graph Subgraph MCP Documentation](https://thegraph.com/docs/en/ai-suite/subgraph-mcp/introduction/)
- [The Graph Subgraph MCP SSE Endpoint](https://subgraphs.mcp.thegraph.com/sse)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/thegraph-mcp-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON envelope parsing guidance for MCP responses and recommends small, schema-informed GraphQL queries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
