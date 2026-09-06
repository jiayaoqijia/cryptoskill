## Description: <br>
Register and manage agent identity, reputation, and feedback on Solana and EVM chains using the multi-chain ERC-8004 Agent Registry protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[montecrypto999](https://clawhub.ai/user/montecrypto999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to an ERC-8004 MCP server for registry lookup, reputation review, wallet-backed registration, feedback, transfer, URI update, and validation workflows across supported Solana and EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact crypto wallet and blockchain transaction authority. <br>
Mitigation: Use testnet and dry-run modes first, prefer a dedicated low-balance wallet, and require explicit approval before mainnet switches, wallet imports, transfers, registrations, feedback submissions, URI updates, or other write operations. <br>
Risk: Wallet material and master passwords are sensitive and may be exposed if copied into chat, examples, or broad environment variables. <br>
Mitigation: Avoid putting real passwords or private keys into prompts or copied examples, and pass only the environment variables needed for the intended operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/montecrypto999/skills/8004-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and TypeScript examples with MCP tool-call guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-only registry queries and wallet-backed blockchain write operations; dry-run options are documented for supported writes.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
