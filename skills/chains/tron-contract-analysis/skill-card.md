## Description:

Analyze TRON smart contracts including deployment info, ABI methods, transaction patterns, top callers, energy costs, and safety assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to inspect TRON smart contracts, understand contract behavior, summarize activity and energy costs, and produce advisory safety assessments before interacting with a contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's safety score may be mistaken for a definitive approval to interact with a contract.

Mitigation: Treat the score as advisory, review the underlying contract data and risk factors, and do not approve or sign transactions based only on the report.

Risk: Contract analysis depends on public TronGrid data and may be incomplete for closed-source or newly deployed contracts.

Mitigation: Call out missing ABI, limited history, or low activity as uncertainty and recommend additional verification before user action.

Risk: The agent may query TronGrid or related MCP tools with user-provided contract addresses.

Mitigation: Confirm users are comfortable with read-only public blockchain lookups and never request private keys, seed phrases, or signing credentials.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Guidance]

**Output Format:** [Markdown contract report with tables, safety scoring, risk factors, positive factors, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only TronGrid MCP queries for public blockchain data; safety scores are advisory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
