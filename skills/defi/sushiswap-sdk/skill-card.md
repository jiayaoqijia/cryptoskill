## Description: <br>
TypeScript SDK guidance for interacting with the SushiSwap Aggregator and related primitives, including typed helpers for token amounts, prices, quotes, and swap transaction generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmasayoshi](https://clawhub.ai/user/0xmasayoshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to integrate SushiSwap quote and swap flows into TypeScript or JavaScript applications with typed token, amount, price, and transaction helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Swap execution examples can lead to live mainnet transactions using an environment private key if copied into an agent runtime. <br>
Mitigation: Do not expose a primary wallet private key to an agent or environment, and require human review of chain, token addresses, amount, recipient or router, calldata, value, slippage, fees, and expected output before any transaction is signed or broadcast. <br>
Risk: Unvalidated swap inputs can produce unsafe quote or transaction requests. <br>
Mitigation: Validate chain ID, token addresses, amount, slippage, supported network, and referrer before requesting quotes or transaction data. <br>


## Reference(s): <br>
- [SushiSwap SDK Reference](references/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes quote and swap transaction examples; swap execution requires human review before signing or broadcasting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
