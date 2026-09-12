## Description:

Operate Sui public JSON-RPC through UXC with OpenRPC-driven discovery, mainnet fullnode defaults, and read-only query plus pubsub subscription guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover and execute safe Sui mainnet JSON-RPC reads through UXC and to set up controlled pubsub subscriptions that write event data to sink files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a local UXC command alias.

Mitigation: Review the alias command before installation and keep it pointed at the intended Sui public mainnet fullnode endpoint.

Risk: Subscription workflows can start long-running jobs that write event data under the user's home directory.

Mitigation: Write subscriptions to explicit sink files, monitor job status, and stop subscription jobs when finished.

Risk: Pubsub behavior depends on the selected Sui WebSocket provider.

Mitigation: Use only verified WebSocket providers that explicitly support JSON-RPC subscriptions.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Sui Documentation](https://docs.sui.io/)
- [Sui Public Mainnet Fullnode](https://fullnode.mainnet.sui.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes JSON output envelopes, read-only methods, verified WebSocket providers for subscriptions, and sink files for subscription data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
