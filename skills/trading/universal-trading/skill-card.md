## Description: <br>
Execute cross-chain token trading on EVM and Solana with Particle Network Universal Account SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xMomo-NGClubs](https://clawhub.ai/user/0xMomo-NGClubs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to set up Particle Network Universal Account examples, perform cross-chain buys, sells, swaps, transfers, and custom transactions, and monitor transaction outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle wallet private keys and execute real trading or transfer workflows. <br>
Mitigation: Use a new low-value wallet, avoid importing a funded private key through the command line, and require explicit confirmation of chain, token, amount, recipient, slippage, fees, and transaction ID before sending transactions. <br>
Risk: First-time setup performs account-affecting actions, including automatic invite binding, and downloads or uses an upstream trading example. <br>
Mitigation: Review the setup before installing, disable automatic invite binding if unwanted, and inspect or pin the upstream project before running setup. <br>
Risk: Demo Particle credentials may be rate-limited or unsuitable for production workloads. <br>
Mitigation: Replace demo credentials with project-specific Particle credentials for production use. <br>


## Reference(s): <br>
- [Environment Setup](references/env-setup.md) <br>
- [Universal Account SDK API Reference](references/api.md) <br>
- [Code Examples](references/examples.md) <br>
- [UniversalX](https://universalx.app) <br>
- [Particle Network Dashboard](https://dashboard.particle.network/) <br>
- [ClawHub Release Page](https://clawhub.ai/0xMomo-NGClubs/universal-trading) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction status, transactionId, explorer URL, selected slippage settings, Solana tip settings, wallet setup notes, and configuration changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
