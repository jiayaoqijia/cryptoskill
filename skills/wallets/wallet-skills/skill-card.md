## Description: <br>
Manage crypto wallets, transfers, swaps, and balances via the Sponge Wallet API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabluthra](https://clawhub.ai/user/rishabluthra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use Sponge Wallet to manage crypto balances and execute wallet actions through REST API requests, including transfers, swaps, bridging, x402 payments, Polymarket activity, and Amazon checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent durable authority over wallet funds, transfers, swaps, bridging, withdrawals, prediction-market activity, paid x402 requests, and Amazon purchases. <br>
Mitigation: Use testnet or low-balance accounts, keep API-key permissions narrow, and require human confirmation before any transaction, trade, paid request, checkout, or withdrawal. <br>
Risk: Agent-first registration can issue an API key before a human owner claims the wallet. <br>
Mitigation: Avoid agent-first registration for real funds; prefer a human-approved device flow and revoke or rotate the key when the task is finished. <br>
Risk: Leaked Sponge Wallet API keys can expose funds or purchasing authority. <br>
Mitigation: Store credentials only in the documented credential file, avoid logging or screenshotting keys, restrict file permissions, and rotate exposed keys immediately. <br>


## Reference(s): <br>
- [Sponge Wallet Skill on ClawHub](https://clawhub.ai/rishabluthra/skills/wallet-skills) <br>
- [Sponge Wallet](https://wallet.paysponge.com) <br>
- [Sponge Wallet API](https://api.wallet.paysponge.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPONGE_API_KEY; wallet actions may spend funds, place trades, make paid x402 requests, or initiate purchases.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
