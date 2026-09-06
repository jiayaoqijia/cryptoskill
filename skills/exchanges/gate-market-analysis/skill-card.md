## Description: <br>
Gate Exchange MarketAnalysis provides read-only Gate market tape analysis for liquidity, slippage, funding arbitrage, basis, manipulation risk, technical signals, and portfolio allocation review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route Gate market-analysis requests to read-only MCP market-data tools and produce structured reports on liquidity, momentum, liquidations, funding arbitrage, basis, manipulation risk, slippage, technical signals, and allocation review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce trading or allocation suggestions that may be broader than market-metrics analysis. <br>
Mitigation: Treat recommendations as informational, include the data-based-not-investment-advice disclaimer, and require human review before any trading or portfolio action. <br>
Risk: Authenticated MCP deployments may ask for Gate credentials even though most market-data calls are read-only or public. <br>
Mitigation: Use read-only API credentials when a key is required and do not grant trading, transfer, or withdrawal permissions. <br>
Risk: The skill makes an external Gate runtime-rules document authoritative, so behavior may depend on mutable remote guidance. <br>
Mitigation: Review the external runtime rules before use and pin or approve the referenced rules where a stable deployment policy is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-market-analysis) <br>
- [Gate Market Analysis MCP Specification](references/mcp.md) <br>
- [Gate Market Analysis Scenarios](references/scenarios.md) <br>
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Gate MCP Setup](https://github.com/gateio/gate-mcp) <br>
- [Gate](https://www.gate.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown structured report with tables, risk flags, conclusions, and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are data-driven market-analysis summaries; the skill does not place trades or move funds.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved ClawHub release metadata; artifact frontmatter version: 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
