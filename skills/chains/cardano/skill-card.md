## Description: <br>
Sign and submit Cardano transactions with explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review, sign, and broadcast pre-built Cardano transaction CBOR through a connected wallet after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real, irreversible Cardano wallet transactions. <br>
Mitigation: Require explicit user confirmation after summarizing recipient addresses, assets, amounts, fees, and network; use a wallet with limited funds. <br>
Risk: Invalid or misleading transaction interpretation could cause the user to approve the wrong transaction. <br>
Mitigation: Treat transaction summaries as review aids and ask the user to verify all transaction details independently before confirmation. <br>
Risk: The connected wallet environment depends on a seed phrase. <br>
Mitigation: Keep seed phrases outside the agent context and avoid using a primary wallet or high-value seed phrase. <br>


## Reference(s): <br>
- [Cardano Transactions ClawHub Page](https://clawhub.ai/adacapo21/cardano-transactions) <br>
- [Transaction Concepts](references/concepts.md) <br>
- [Transaction MCP Tools Reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown transaction summary, confirmation prompt, and transaction hash or status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires unsigned Cardano transaction CBOR and explicit user confirmation before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
