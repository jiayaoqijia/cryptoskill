## Description: <br>
Okx Onchain Gateway helps agents estimate gas, simulate transactions, broadcast signed transactions, and track transaction status across XLayer, Solana, Ethereum, Base, BSC, Arbitrum, Polygon, and other supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to check gas, simulate a prepared transaction, broadcast a signed transaction, or track broadcast status across supported chains. <br>

### Deployment Geography for Use: <br>
Global, subject to OKX service availability and regional restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: Signed blockchain transactions can be irreversible once broadcast. <br>
Mitigation: Before broadcasting, show the chain, sender, recipient or contract, value, calldata or signed transaction summary, and estimated fees, then require explicit user confirmation. <br>
Risk: The skill can install or update an external onchainos CLI. <br>
Mitigation: Verify installer and binary SHA256 checksums before use, stop on any mismatch, and report installation failures without retrying unsafe paths. <br>
Risk: Transaction simulation is informational and does not prove that a transaction is safe. <br>
Mitigation: Treat simulation results as one review signal and require user review before any on-chain submission. <br>


## Reference(s): <br>
- [Onchain OS Gateway CLI Command Reference](references/cli-reference.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chain, wallet address, gas estimates, simulation status, transaction hash, order ID, and broadcast status.] <br>

## Skill Version(s): <br>
3.1.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
