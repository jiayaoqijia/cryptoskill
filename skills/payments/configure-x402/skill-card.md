## Description: <br>
Configure x402 micropayments for agent-to-agent commerce via Uniswap, enabling an agent to pay per MCP request in USDC on Base or accept x402 payments as a service provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure pay-per-request x402 payments for MCP tools and external API access, or to monetize an agent by accepting USDC micropayments. It guides wallet, chain, facilitator, pricing, tool-scope, and spending-limit configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: x402 payment configuration can lead to real USDC spending when pay mode is used at runtime. <br>
Mitigation: Use a dedicated low-balance Base USDC wallet and keep the hourly spend cap low. <br>
Risk: Accept mode can expose tools for paid public use beyond the intended service scope. <br>
Mitigation: Choose pay, accept, or both explicitly and limit accepted-payment tools to those intended for public access. <br>
Risk: Generated payment configuration or manifests may not match production intent. <br>
Mitigation: Review the generated .uniswap/x402-config.json and .well-known/x402-manifest.json before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/configure-x402) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration details and setup summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce .uniswap/x402-config.json and .well-known/x402-manifest.json with wallet, chain, facilitator, pricing, tool-gating, and spending-limit settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
