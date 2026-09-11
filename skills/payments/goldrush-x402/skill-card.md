## Description:

GoldRush x402 provides pay-per-request blockchain data access through the x402 protocol, letting agents and applications use GoldRush Foundational API endpoints with wallet-based micropayments instead of API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gane5h](https://clawhub.ai/user/gane5h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add autonomous, no-account access to GoldRush blockchain data through x402 payments. It helps agents discover endpoints, evaluate pricing, configure a wallet, and call paid blockchain data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic wallet payments can spend funds without sufficient local limits.

Mitigation: Use a dedicated low-balance wallet, preferably testnet-only, and enforce local controls for chain, token, recipient, per-request amount, retries, and total spend before autonomous use.

Risk: Wallet private keys may be exposed if copied into code, logs, or shared environments.

Mitigation: Store private keys in a secrets manager or protected environment variable and never reuse a wallet that holds valuable assets.

Risk: Payment client dependencies can affect transaction signing and payment behavior.

Mitigation: Pin and audit the x402 dependencies before deployment.

## Reference(s):

- [GoldRush x402 Overview](references/overview.md)
- [x402 for AI Agents](references/ai-agents.md)
- [x402 Endpoints](references/endpoints.md)
- [x402 Protocol](https://x402.org)
- [Goldrush X402 on ClawHub](https://clawhub.ai/gane5h/skills/goldrush-x402)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint discovery, pricing, wallet setup, and x402 payment guidance.]

## Skill Version(s):

3.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
