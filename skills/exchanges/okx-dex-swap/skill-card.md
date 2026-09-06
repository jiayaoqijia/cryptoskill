## Description: <br>
Provides agent guidance for quoting, approving, executing, and preparing calldata for OKX DEX aggregated token swaps across supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through OKX DEX aggregated token swaps, swap quotes, token approvals, transaction broadcasts, and unsigned calldata generation. It is intended for wallet-connected crypto workflows where the user reviews route, amount, slippage, spender, and transaction details before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real token approvals and wallet-signed swap broadcasts, which may result in fund loss if details are wrong or unsafe. <br>
Mitigation: Use a limited-purpose wallet and require the user to review token addresses, chain, amount, route, slippage, spender or approval details, and expected receive amount before signing. <br>
Risk: The skill can install or update the onchainos CLI before use. <br>
Mitigation: Install only from a trusted OKX/onchainos release source and verify installer and binary checksums before running swap commands. <br>
Risk: Silent mode and force execution can bypass normal per-transaction review or risk warnings. <br>
Mitigation: Avoid silent mode unless explicitly authorized, and never use force unless the user understands and confirms the fund-loss warning. <br>
Risk: Diagnostics and transaction output may expose wallet addresses or transaction details. <br>
Mitigation: Redact wallet addresses, transaction hashes, and sensitive transaction details before sharing diagnostics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-dex-swap) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX DEX Aggregator API Reference](https://web3.okx.com/onchainos/dev-docs/trade/dex-api-reference) <br>
- [Onchain OS DEX Swap CLI Command Reference](references/cli-reference.md) <br>
- [Swap Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, parameter summaries, warnings, and transaction result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, token addresses, quote details, approval data, calldata, and transaction hashes that should be reviewed and redacted when shared.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
