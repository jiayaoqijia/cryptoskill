## Description: <br>
Use Crypto.com MCP through UXC for exchange market data workflows with help-first discovery and read-only guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover Crypto.com exchange markets and run read-only public market-data queries such as instruments, tickers, order books, trades, and candlesticks through MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Crypto.com's external MCP market-data endpoint. <br>
Mitigation: Use only public market-data parameters and avoid submitting trading credentials, account details, or private financial information. <br>
Risk: Local execution depends on the installed UXC tooling and linked command. <br>
Mitigation: Install and run the skill only in environments where the local UXC tool is trusted. <br>
Risk: Market data can be time-sensitive or incomplete for downstream decisions. <br>
Mitigation: Keep requests narrow, parse the JSON output envelope, and verify results before using them in financial workflows. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Official Crypto.com MCP Docs](https://mcp.crypto.com/docs) <br>
- [Crypto.com MCP Market Data Endpoint](https://mcp.crypto.com/market-data/mcp) <br>
- [ClawHub Release Page](https://clawhub.ai/jolestar/crypto-com-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market-data workflows; automation should parse the JSON output envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
