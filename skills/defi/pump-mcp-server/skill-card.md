## Description: <br>
Model Context Protocol server exposing 7 tools, 3 resource types, and 3 prompts for AI agent consumption: Solana wallet operations, vanity address generation, message signing, and address validation over stdio transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speraxos](https://clawhub.ai/user/speraxos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate and inspect Solana wallet keypairs, create vanity addresses, validate addresses, and sign or verify messages through MCP tools and prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Solana private keys and message signing, which can expose funds or credentials if used with real wallets. <br>
Mitigation: Use only throwaway development wallets until the implementation, dependencies, and install instructions are reviewed. <br>
Risk: The submitted artifact provides prose behavior descriptions but no auditable implementation or dependency manifest. <br>
Mitigation: Require source code, dependency manifests, and run instructions before relying on this skill in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/speraxos/pump-mcp-server) <br>
- [Project homepage](https://github.com/nirholas/pump-fun-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON tool and resource responses with prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Session keypair state is ephemeral, and artifact evidence says secret key bytes are not exposed in resources.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
