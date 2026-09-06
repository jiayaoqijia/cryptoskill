## Description: <br>
Operate Binance Spot market, account, and order APIs through UXC with a curated OpenAPI schema, Binance query signing, and separate mainnet/testnet link flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure UXC access to Binance Spot REST APIs, inspect market and account data, and prepare or execute order-related operations with testnet-first guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Binance Spot credentials can expose account data or allow order placement and cancellation. <br>
Mitigation: Use least-privilege API keys with withdrawals disabled, keep mainnet and testnet keys separate, and require explicit confirmation before any live trade or cancellation. <br>
Risk: Mainnet writes can create real financial exposure if an agent executes an unintended order. <br>
Mitigation: Start on testnet, validate order shape with order/test before real writes, and treat all mainnet write operations as high-risk. <br>
Risk: Exported API keys or signing material can be exposed through the local environment. <br>
Mitigation: Clear exported secrets after use and revoke keys promptly if exposure is suspected. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated Binance Spot OpenAPI schema](references/binance-spot.openapi.json) <br>
- [Official Binance Spot API docs](https://github.com/binance/binance-spot-api-docs) <br>
- [Binance Spot skill source material](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/spot) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/binance-spot-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes JSON output envelopes, separate mainnet and testnet credentials, and explicit confirmation before live mainnet writes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
