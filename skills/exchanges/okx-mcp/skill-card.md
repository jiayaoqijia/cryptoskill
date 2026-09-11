## Description:

Use OKX OnchainOS MCP through UXC for token discovery, market data, wallet balance, and swap execution planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to access OKX MCP workflows for token discovery, market data, wallet balance checks, and swap planning through a help-first command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a shared demo OKX API key and flags the skill as suspicious for regular wallet and swap-related use.

Mitigation: Use a user-owned least-privilege OKX key from an environment variable or secret manager, and avoid embedding or pasting secrets into shell commands.

Risk: Swap, approval, and transaction-instruction operations can affect user assets if executed without review.

Mitigation: Require explicit confirmation before approve, swap, or transaction-instruction operations, and inspect operation schemas before execution.

Risk: Authentication failures can cause incomplete or misleading OKX MCP results.

Mitigation: Verify credential binding and the OK-ACCESS-KEY header configuration before relying on results.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [OKX OnchainOS MCP endpoint](https://web3.okx.com/api/v1/onchainos-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OKX MCP data returned through uxc command invocations; high-impact swap and transaction-instruction operations require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
