## Description:

OpenPump Solana MCP gives agents tools to launch pump.fun tokens, trade SOL and SPL tokens, manage OpenPump wallets, run market-making and sniping workflows, and monitor portfolio positions through the OpenPump MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstacktard](https://clawhub.ai/user/fullstacktard)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to connect an agent to OpenPump's MCP server for user-supervised pump.fun token trading, token launch workflows, wallet management, portfolio monitoring, and trading risk checks.

### Deployment Geography for Use:

Global where legally available, excluding US persons.

## Known Risks and Mitigations:

Risk: The skill gives an agent broad real-money wallet and trading authority for Solana and pump.fun activity.

Mitigation: Use low-balance, revocable, tightly scoped OpenPump credentials when available and require explicit, transaction-specific approval for buys, sells, transfers, token launches, sniping, market making, and spam launches.

Risk: The MCP server configuration uses a mutable @latest npm startup package.

Mitigation: Avoid @latest startup execution for production use; pin and review the package version before enabling the MCP server.

Risk: The skill requires an OPENPUMP_API_KEY credential that could expose trading authority if stored insecurely.

Mitigation: Store the key in a secure secret manager or protected environment and avoid committing or persisting it in plaintext.

Risk: The README states the agent is not available to US persons.

Mitigation: Verify user eligibility and legal availability before installing or operating the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fullstacktard/skills/openpump-solana-mcp)
- [OpenPump](https://openpump.io)
- [OpenPump Docs](https://docs.openpump.io)
- [@openpump/mcp npm Package](https://www.npmjs.com/package/@openpump/mcp)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENPUMP_API_KEY and Node.js/npx; may guide MCP tool calls that affect real Solana funds only after explicit user confirmation.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
