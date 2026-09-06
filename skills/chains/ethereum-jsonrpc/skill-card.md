## Description: <br>
Operate Ethereum execution JSON-RPC through UXC with the official execution OpenRPC schema, public EVM read methods, and eth_subscribe pubsub guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to link a UXC Ethereum JSON-RPC CLI, inspect schema-backed read operations, run safe public state queries, and manage provider-verified eth_subscribe streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ethereum RPC endpoint or live OpenRPC schema trust can affect command behavior. <br>
Mitigation: Use trusted RPC providers and schema sources before linking or automating requests. <br>
Risk: Wallet, signing, write, admin, debug, engine, or txpool calls can exceed the skill's documented safety scope. <br>
Mitigation: Keep usage to documented read-only methods and eth_subscribe unless a separate design and review approves broader methods. <br>
Risk: Subscription jobs can continue writing local event logs longer than intended. <br>
Mitigation: Monitor subscription status, use explicit sink files, and stop jobs when collection is complete. <br>


## Reference(s): <br>
- [Ethereum JSON-RPC usage patterns](references/usage-patterns.md) <br>
- [Ethereum execution API specs](https://github.com/ethereum/execution-apis) <br>
- [Ethereum execution OpenRPC schema](https://raw.githubusercontent.com/ethereum/execution-apis/assembled-spec/refs-openrpc.json) <br>
- [Ethereum JSON-RPC overview](https://ethereum.org/developers/docs/apis/json-rpc/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on read-only JSON-RPC methods and file-backed subscription streams.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
