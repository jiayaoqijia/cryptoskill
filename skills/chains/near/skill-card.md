## Description: <br>
Universal cross-chain swap & bridge skill for OpenClaw using the NEAR Intents 1Click SDK. Supports 14+ blockchains including NEAR, Base, Ethereum, Solana, and Bitcoin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuongdcdev](https://clawhub.ai/user/cuongdcdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this documentation-only skill as a reference for integrating NEAR Intents 1Click SDK swap and bridge workflows into OpenClaw agents, including quote retrieval, manual deposit instructions, and optional NEAR-origin auto transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward cryptocurrency swaps or transfers from a configured NEAR account. <br>
Mitigation: Prefer manual mode, require explicit user approval before signing or broadcasting any transfer, and verify the recipient address before funds move. <br>
Risk: A wrong refund address for non-NEAR origins can cause permanent fund loss if a swap fails. <br>
Mitigation: Ask the user for the origin-chain refund wallet, confirm the chain and address, and never infer or reuse a refund address from unrelated context. <br>
Risk: Auto mode depends on NEAR account credentials and private keys. <br>
Mitigation: Keep private keys out of shared environments, avoid committing environment files, and use the smallest practical account permissions and balances. <br>


## Reference(s): <br>
- [Server-resolved source repository path](https://github.com/cuongdcdev/openclaw-near-skills/tree/main/near-intents) <br>
- [ClawHub skill page](https://clawhub.ai/cuongdcdev/skills/near-intents) <br>
- [NEAR Intents 1Click API documentation](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api) <br>
- [Defuse Protocol 1Click TypeScript SDK](https://github.com/defuse-protocol/one-click-sdk-typescript) <br>
- [NEAR Intents documentation](https://docs.near-intents.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples and environment configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only release; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
