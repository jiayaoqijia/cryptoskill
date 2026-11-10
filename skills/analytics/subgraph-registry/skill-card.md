## Description:

Use to discover The Graph subgraphs by chain, protocol, entity or contract and turn a goal into a bounded GraphQL query. Bring-your-own Studio key (set up by a human operator) for execution; discovery never executes queries or signs payments, and x402 is an explicitly paid external option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers use this MCP server to find relevant subgraphs on The Graph and prepare bounded GraphQL queries from a goal. With an operator-configured Studio API key, they can separately opt in to schema validation, health checks, and query execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reported a benign verdict with medium confidence, but only 7 of 11 components were fully inspected and static tool-misuse analysis was degraded.

Mitigation: Review the partially inspected components, any unpinned npx references, and host environment and network permissions before installation. Use the reviewed pinned release and keep API keys in the MCP host's secret store.

## Reference(s):

- [Project repository (Clawdis homepage metadata)](https://github.com/PaulieB14/subgraph-registry)
- [The Graph supported networks documentation](https://thegraph.com/docs/en/supported-networks/)
- [ClawHub release page](https://clawhub.ai/paulieb14/skills/subgraph-registry)

## Skill Output:

**Output Type(s):** [JSON, GraphQL query text, Guidance]

**Output Format:** [Structured MCP tool responses, including discovery results and query text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery uses snapshot data; schema and execution tools are separate opt-in actions requiring an operator-configured Studio API key.]

## Skill Version(s):

0.13.2 (source: server-resolved release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
