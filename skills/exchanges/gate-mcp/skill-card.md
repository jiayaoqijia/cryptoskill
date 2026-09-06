## Description: <br>
Use Gate MCP through UXC for public spot and futures market data workflows with a fixed streamable-http endpoint and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and run read-only Gate MCP public spot and futures market-data workflows, including market discovery, tickers, order books, trades, candlesticks, funding rates, and premium data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public market-data requests to Gate's MCP endpoint through uxc. <br>
Mitigation: Use it only when you trust uxc and are comfortable contacting the fixed Gate MCP endpoint. <br>
Risk: Using the skill outside its documented read-only scope could expose private account, wallet, credential, or trading information. <br>
Mitigation: Keep requests within the documented read-only commands and do not provide Gate API keys, wallet details, account credentials, or private trading instructions. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Official Gate for AI / MCP docs](https://www.gate.com/gate-mcp-skills) <br>
- [Gate MCP setup article](https://www.gate.com/ru/help/gateforai/gateforaibasics/50102/gate-for-ai-one-click-integration-with-major-ai-agents-no-api-keys-required-zero-barriers) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and MCP operation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market-data requests should use the documented JSON output envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
