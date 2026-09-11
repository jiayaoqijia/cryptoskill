## Description:

Operates Breeze x402 payment-gated endpoints for balance checks, deposits, and withdrawals on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keeganthomp](https://clawhub.ai/user/keeganthomp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to check Breeze balances, build deposit or withdrawal transactions, and execute paid x402 API calls for Solana positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Solana wallet private key and can sign transactions.

Mitigation: Use a dedicated low-balance Solana wallet, avoid plaintext private-key storage, and redact secrets from all logs and outputs.

Risk: The skill signs server-supplied deposit or withdrawal transactions.

Mitigation: Require explicit review of destination, amount, token, strategy, fees, and decoded transaction instructions before signing or broadcasting.

Risk: Runtime dependencies and paid x402 API calls can affect wallet funds.

Mitigation: Pin dependencies and confirm x402 payment amounts, selected tokens, and transaction fees before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keeganthomp/skills/breeze-x402-payment-api)
- [Breeze](https://breeze.baby)
- [Breeze x402 API](https://x402.breeze.baby)
- [Solana Mainnet RPC](https://api.mainnet-beta.solana.com)
- [Breeze x402 Example Implementation](https://github.com/anagrambuild/breeze-agent-kit/tree/main/apps/examples/agent-using-x402)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, command snippets, API workflow guidance, balance summaries, and transaction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include required environment variables, Solana transaction signatures, explorer URLs, converted token amounts, and explicit pre-signing review steps.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
