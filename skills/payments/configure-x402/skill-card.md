## Description:

Configure x402 micropayments for agent-to-agent commerce via Uniswap, enabling agents to pay per MCP request in USDC on Base or accept x402 payments as service providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure agents that pay for MCP or API calls through x402, accept per-request USDC payments, or support both payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated x402 configuration can cause future agent requests to send or request USDC payments.

Mitigation: Confirm the wallet address, payment mode, gated tools, public manifest behavior, and maxSpendPerHour limit before using the configuration.

Risk: Incorrect wallet, chain, balance, or facilitator settings can prevent settlement or route payments incorrectly.

Mitigation: Validate the wallet address, confirm USDC availability on the selected chain, and verify facilitator availability before deployment.

Risk: Accept mode can publish a manifest that exposes x402-enabled endpoints and payment parameters.

Mitigation: Review .well-known/x402-manifest.json and the supportedTools scope before publishing the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/configure-x402)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Text summary with JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates .uniswap/x402-config.json and, for accept mode, .well-known/x402-manifest.json.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
