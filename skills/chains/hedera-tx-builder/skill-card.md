## Description: <br>
Build, sign, and submit Hedera transactions including HBAR transfers, token operations, and smart contract calls to the Hedera network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to draft Hedera SDK setup steps and transaction-building examples for HBAR transfers, token associations, account creation, topic messages, and smart contract calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users toward signing and submitting real Hedera transactions. <br>
Mitigation: Use testnet first and require explicit confirmation of transaction details before any mainnet signing or submission. <br>
Risk: Private keys or wallet credentials could be exposed if pasted into chat or source files. <br>
Mitigation: Prefer wallet-mediated signing and do not paste private keys into chat, prompts, generated code, or source files. <br>
Risk: Unpinned SDK dependencies can change transaction behavior or introduce supply-chain risk. <br>
Mitigation: Pin @hashgraph/sdk in a lockfile before using generated setup guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HarleysCodes/hedera-tx-builder) <br>
- [Hedera Hashio mainnet API endpoint](https://mainnet.hashio.io/api) <br>
- [Hedera Hashio testnet API endpoint](https://testnet.hashio.io/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transaction examples require user review before signing or network submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
