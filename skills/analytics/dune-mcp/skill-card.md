## Description:

Use Dune MCP through UXC for blockchain table discovery, SQL query creation/execution, execution result retrieval, and visualization with help-first schema inspection, explicit auth binding, and guarded credit-consuming operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to discover Dune blockchain tables, draft and run SQL queries, retrieve execution results, and generate visualizations through UXC-mediated Dune MCP commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Dune operations can consume credits or create, update, execute, publish, or visualize queries.

Mitigation: Use explicit user confirmation before credit-consuming or state-changing operations, and check usage before heavy experimentation.

Risk: Dune API credentials, SQL, and query metadata may be exposed if handled carelessly.

Mitigation: Use a least-privilege Dune API key through UXC credential binding and confirm privacy settings before making queries public.

Risk: Unbounded SQL queries can increase cost, latency, or result volume.

Mitigation: Inspect operation schemas and table metadata first, prefer partition-aware filters such as block_date or evt_block_date, and keep initial result sets small.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Dune MCP endpoint](https://api.dune.com/mcp/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, SQL snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON command output envelopes when automating Dune MCP calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
