## Description: <br>
Operate Sui public JSON-RPC through UXC with OpenRPC-driven discovery, mainnet fullnode defaults, and read-only query plus pubsub subscription guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover and run safe Sui JSON-RPC reads through UXC against the public mainnet fullnode, and to set up controlled pubsub subscriptions with verified WebSocket providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A compromised or untrusted UXC setup could affect JSON-RPC execution. <br>
Mitigation: Install and use the skill only with a trusted UXC setup. <br>
Risk: Using unreviewed write, signing, or unsafe Sui methods could move beyond the skill's read-only scope. <br>
Mitigation: Stay on the listed read-only methods unless a separate design and review covers broader transaction flows. <br>
Risk: An unverified WebSocket provider may not support the expected pubsub behavior. <br>
Mitigation: Verify the provider endpoint before starting subscriptions. <br>
Risk: Long-running subscription jobs can continue network and disk use. <br>
Mitigation: Write subscriptions to explicit sink files, monitor job status, and stop jobs when finished. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Sui Documentation](https://docs.sui.io/) <br>
- [Sui Public Mainnet Fullnode](https://fullnode.mainnet.sui.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/sui-jsonrpc-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only JSON-RPC query guidance by default; subscription examples write NDJSON sink files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
