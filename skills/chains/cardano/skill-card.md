## Description:

Sign and submit Cardano transactions with explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to sign and broadcast pre-built Cardano transaction CBOR through a connected wallet after the agent summarizes the transaction and receives explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign and broadcast real Cardano transactions using wallet secrets.

Mitigation: Use only wallets and funds the user is prepared to risk, and independently verify every transaction in a trusted wallet or explorer before approval.

Risk: A process with access to wallet secrets can expose or misuse funds.

Mitigation: Prefer a pinned and audited MCP package, a hardware wallet or scoped signer instead of a raw seed phrase, and strict isolation for any process that can access wallet secrets.

Risk: Submitted Cardano transactions are irreversible once confirmed on-chain.

Mitigation: Require a plain-language transaction summary and explicit user confirmation before calling submit_transaction.

## Reference(s):

- [Cardano Transactions ClawHub Page](https://clawhub.ai/adacapo21/skills/cardano-transactions)
- [Transaction Concepts](artifact/references/concepts.md)
- [Transaction MCP Tools Reference](artifact/references/mcp-tools.md)
- [Submit a Transaction](artifact/sub-skills/submit-tx.md)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown or plain text transaction summary, confirmation prompt, and transaction result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports transactionHash and timestamp on success; signing or submission errors may be reported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
