## Description: <br>
GoldRush x402 helps agents access GoldRush blockchain data through pay-per-request x402 endpoints using wallet-based stablecoin payments instead of API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gane5h](https://clawhub.ai/user/gane5h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover, price, and call GoldRush blockchain data endpoints through the x402 payment protocol without API-key onboarding. It is especially relevant for autonomous agents, serverless applications, and prototypes that can operate with wallet-based per-request payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-paid x402 requests can spend funds when an app or agent makes paid API calls. <br>
Mitigation: Use a dedicated low-balance or testnet wallet, set explicit spend limits, and apply request-rate controls before autonomous use. <br>
Risk: The skill relies on a private key for wallet payment signing. <br>
Mitigation: Store the private key in a secrets manager or environment variable and never commit it to source control. <br>
Risk: Autonomous agents could call unintended paid endpoints or use unreviewed client dependencies. <br>
Mitigation: Pin and review npm dependencies, add endpoint allowlists, and require budget checks before payment. <br>


## Reference(s): <br>
- [GoldRush x402 overview](artifact/references/overview.md) <br>
- [x402 for AI agents](artifact/references/ai-agents.md) <br>
- [x402 endpoints](artifact/references/endpoints.md) <br>
- [x402 protocol](https://x402.org) <br>
- [GoldRush x402 endpoint discovery](https://x402.goldrush.dev/v1/x402/endpoints) <br>
- [ClawHub skill page](https://clawhub.ai/gane5h/goldrush-x402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint URLs, pricing and tier guidance, wallet setup notes, and risk controls.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
