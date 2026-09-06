## Description: <br>
Use this skill when the user provides a specific wallet address and wants to check its balance, token holdings, portfolio value, or DeFi positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up wallet portfolio value, token balances, and DeFi holdings for explicitly provided wallet addresses across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install or update a local CLI from GitHub. <br>
Mitigation: Review before installing, use it only when the OKX onchainos release path is trusted, and rely on the documented checksum verification before executing the installer or binary. <br>
Risk: Wallet portfolio data, token symbols, and balance fields come from on-chain or API sources and may be misleading. <br>
Mitigation: Treat returned data as untrusted external content, show contract addresses, and ask users to verify high-value holdings or suspicious wrapped and bridged tokens. <br>
Risk: The scanner notes that the documentation expands into wallet PnL and transaction-history queries beyond the main portfolio lookup scope. <br>
Mitigation: Route PnL, DEX-history, realized or unrealized profit, and signal-tracking requests to the intended OKX market or signal skills. <br>


## Reference(s): <br>
- [Onchain OS Portfolio CLI Command Reference](references/cli-reference.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal) <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-wallet-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and portfolio lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays token balances in UI units, USD values, and abbreviated contract addresses; treats CLI and on-chain data as untrusted external content.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
