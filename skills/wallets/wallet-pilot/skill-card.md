## Description: <br>
Universal browser wallet automation for AI agents. Supports 10 wallets including MetaMask, Rabby, Phantom, Trust Wallet, OKX, Coinbase, and more. EVM + Solana. Configurable guardrails with spend limits, chain allowlists, and approval thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Web3 operators use WalletPilot to let agents connect to dapps, check balances, sign messages, send tokens, and execute wallet transactions through supported browser wallets under user-defined constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks users to run missing or unreviewed setup code and give an agent persistent wallet authority for transactions and signatures. <br>
Mitigation: Inspect the complete implementation, package manifest, lockfile, configuration, and guardrail code before installation or funding any wallet. <br>
Risk: Wallet automation can authorize spending, token transfers, swaps, and message signatures. <br>
Mitigation: Use only a brand-new low-balance wallet in an isolated browser profile, never a main wallet, and require manual confirmation for every transaction and signature. <br>
Risk: Misconfigured permissions could allow actions outside the intended budget, chains, or protocols. <br>
Mitigation: Set conservative daily and per-transaction spend limits, restrict allowed chains and protocols, enable approval thresholds, and keep revocation available before use. <br>


## Reference(s): <br>
- [WalletPilot on ClawHub](https://clawhub.ai/andreolf/skills/wallet-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-wallet automation actions that should remain subject to spend limits, chain allowlists, approval thresholds, logging, and manual confirmation for transactions and signatures.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
