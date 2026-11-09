## Description:

Use to discover The Graph subgraphs by chain, protocol, entity or contract and turn a goal into a bounded GraphQL query. Bring-your-own Studio key (set up by a human operator) for execution; discovery never executes queries or signs payments, and x402 is an explicitly paid external option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this MCP skill to discover and compare The Graph subgraphs, inspect deployment details, and prepare bounded GraphQL queries for a specific goal. Live schema checks and query execution are opt-in and use an operator-managed Studio key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flexible dependency ranges and unpinned setup commands can make installations vary over time.

Mitigation: Use the documented version-pinned 0.12.0 install command and review dependency changes before deployment.

Risk: The security scan inspected only part of the release, so its benign verdict has limited coverage.

Mitigation: Review the release and its dependencies before installation, especially if the deployment has elevated access.

Risk: Live query execution uses the operator’s Graph Studio quota, and an external x402 client can incur a payment.

Mitigation: Keep execution opt-in; require explicit approval for any x402 payment and never share Studio keys in chat.

## Reference(s):

- [Subgraph Registry project homepage](https://github.com/PaulieB14/subgraph-registry)
- [The Graph supported networks](https://thegraph.com/docs/en/supported-networks/)
- [GraphOps subgraph MCP reference](https://github.com/graphops/subgraph-mcp)

## Skill Output:

**Output Type(s):** [JSON, Code, Guidance]

**Output Format:** [Structured JSON tool responses with GraphQL query text and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include discovery results, bounded query proposals, confidence and limitations; execution is opt-in.]

## Skill Version(s):

0.12.0 (source: package.json and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
