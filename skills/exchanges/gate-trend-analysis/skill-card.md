## Description: <br>
Performs read-only, single-coin trend and technical analysis using Gate-Info MCP market snapshots, K-line data, indicator history, and technical signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer single-coin technical or trend-analysis requests by gathering read-only Gate market data and producing a structured technical report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Gate-Info MCP server or shared Gate runtime rule files may not be trusted or available. <br>
Mitigation: Install only when the user trusts the local Gate-Info MCP server and review the shared Gate runtime rules before use. <br>
Risk: Market data or indicator tools may be unavailable or incomplete. <br>
Mitigation: Label unavailable data explicitly, skip missing indicators, and downgrade confidence rather than fabricating values. <br>
Risk: Technical analysis may be mistaken for trading advice. <br>
Mitigation: Frame outputs as historical technical interpretation and avoid buy, sell, long, short, or specific price-prediction recommendations. <br>


## Reference(s): <br>
- [Gate Info TrendAnalysis MCP Specification](references/mcp.md) <br>
- [Scenarios & Prompt Examples](references/scenarios.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-trend-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured technical analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market analysis; missing data must be labeled and outputs must avoid trading advice or specific price predictions.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; packaged frontmatter version 2026.4.3-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
