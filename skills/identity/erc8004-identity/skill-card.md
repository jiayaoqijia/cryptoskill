## Description: <br>
Deploy and manage an AI agent's onchain identity, reputation, and task capabilities on Avalanche using the ERC-8004 NFT standard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ijaack](https://clawhub.ai/user/ijaack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to register an AI agent identity, deploy supporting contracts, set metadata, configure task prices, and check deployment status on Avalanche. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys and can spend AVAX or make persistent public blockchain changes. <br>
Mitigation: Use a dedicated low-balance wallet, keep PRIVATE_KEY out of commits, logs, screenshots, and shell history, and review commands before execution. <br>
Risk: Deployment and metadata commands depend on Avalanche RPC endpoints and contract addresses. <br>
Mitigation: Verify the Avalanche RPC URL and contract addresses before running deploy or set commands. <br>


## Reference(s): <br>
- [ERC-8004 Spec](https://github.com/ava-labs/ERC-8004) <br>
- [Avalanche Docs](https://docs.avax.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript snippets; the CLI emits terminal text and JSON deployment state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create config/agent.config.js and deployment.json, print Snowtrace links, and submit Avalanche transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
