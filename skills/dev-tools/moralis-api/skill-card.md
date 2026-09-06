## Description: <br>
Operate Moralis EVM wallet and token reads through UXC with a curated OpenAPI schema, API-key auth, and wallet-intelligence guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Moralis API-key authentication and run read-only EVM wallet and token queries through UXC. It supports balance, token, history, swap, net-worth, metadata, and price lookups while keeping chain selection and query scope explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moralis API keys can be exposed if pasted directly into prompts, scripts, or logs. <br>
Mitigation: Use a dedicated Moralis API key through the documented secret environment variable and UXC auth binding. <br>
Risk: Wallet queries can reveal sensitive or privacy-relevant account activity. <br>
Mitigation: Query only wallets you are authorized to analyze and keep results handling consistent with privacy requirements. <br>
Risk: Broad wallet history or swap queries can be expensive, slow, or noisy. <br>
Mitigation: Start with narrow chains, small limits, and bounded query windows before expanding scope. <br>
Risk: A remotely linked OpenAPI schema can change after setup. <br>
Mitigation: Review or pin the schema used for UXC linking when repeatability matters. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/moralis-evm.openapi.json) <br>
- [Moralis Wallet Docs](https://docs.moralis.com/data-api/evm/wallet) <br>
- [Moralis Token Docs](https://docs.moralis.com/data-api/evm/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Moralis EVM operations with explicit chain parameters and API-key authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
