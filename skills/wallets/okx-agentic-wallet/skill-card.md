## Description: <br>
Okx Agentic Wallet guides agents through OKX wallet authentication, balances, transfers, signing, transaction history, smart contract calls, and Gas Station stablecoin gas flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate an OKX Agentic Wallet for account management, wallet reads, token transfers, transaction history, message signing, contract calls, and Gas Station stablecoin gas workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an OKX Agentic Wallet with real transaction authority and can affect real funds. <br>
Mitigation: Install and use it only when that authority is intended; review wallet actions and require explicit confirmation before broadcasts. <br>
Risk: Gas Station first-time setup can persist per account and chain, and disabling Gas Station may not revoke the underlying on-chain delegation. <br>
Mitigation: Explain the persistent per-chain setup before enabling Gas Station, use documented management commands, and do not represent disable as full on-chain revocation. <br>
Risk: The pre-flight flow can download and run a remote OKX CLI installer. <br>
Mitigation: Proceed only when the OKX source is trusted; verify installer and binary checksums as documented before running wallet commands. <br>


## Reference(s): <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX OnchainOS Developer Portal](https://web3.okx.com/zh-hans/onchainos/dev-portal) <br>
- [OKX Agentic Wallet Policy](https://web3.okx.com/portfolio/agentic-wallet-policy) <br>
- [OKX OnchainOS API Access and Usage](https://web3.okx.com/onchainos/dev-docs/home/api-access-and-usage) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Gas Station Reference](references/gas-station.md) <br>
- [EIP-7702 Upgrade Flow Reference](references/eip7702-upgrade.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Pre-flight Checks](_shared/preflight.md) <br>
- [Chain Support](_shared/chain-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured wallet-command results when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require wallet credentials, user confirmations, chain selection, and review before actions that can affect funds.] <br>

## Skill Version(s): <br>
3.1.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
