## Description:

Operate Ethereum execution JSON-RPC through UXC with the official execution OpenRPC schema, public EVM read methods, and eth_subscribe pubsub guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query public Ethereum execution RPC data, inspect schema-backed method help, and manage validated eth_subscribe streams while keeping agents on a read-first Ethereum workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription streams can create long-running jobs and local event log files.

Mitigation: Review subscription use, require a verified WebSocket RPC provider, write events to a sink file, and stop subscription jobs when finished.

Risk: Broader Ethereum RPC authority could allow methods outside the documented read-only scope.

Mitigation: Keep the documented read-only and eth_subscribe guardrails unless a separate review approves transaction, admin, debug, engine, or provider-specific authority.

## Reference(s):

- [Ethereum JSON-RPC usage patterns](references/usage-patterns.md)
- [Ethereum execution API specs](https://github.com/ethereum/execution-apis)
- [Ethereum execution OpenRPC schema](https://raw.githubusercontent.com/ethereum/execution-apis/assembled-spec/refs-openrpc.json)
- [Ethereum JSON-RPC overview](https://ethereum.org/developers/docs/apis/json-rpc/)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/ethereum-jsonrpc-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only RPC guidance by default; subscription examples use sink files for event review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
