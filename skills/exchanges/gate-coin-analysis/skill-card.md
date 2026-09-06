## Description: <br>
Single-coin comprehensive analysis for crypto assets, combining fundamentals, market data, technical signals, news, and social sentiment into a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze one identified crypto asset and receive a concise, data-driven market report. It is intended for standard single-coin analysis, not multi-coin comparison, risk-only checks, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may route broad crypto questions to this single-coin workflow when a specialized risk, security, news, technical-analysis, or comparison skill would be more appropriate. <br>
Mitigation: Use the skill only for standard single-coin comprehensive analysis and route comparison, risk-only, news-only, technical-only, address, or multi-dimension requests to the dedicated skill. <br>
Risk: Crypto analysis outputs can be mistaken for financial advice or trade recommendations. <br>
Mitigation: Keep conclusions neutral and data-driven, avoid explicit buy/sell advice and price predictions, and include a clear investment-advice disclaimer. <br>
Risk: Required market, fundamentals, news, or sentiment data may be unavailable if the Gate Info or Gate News MCP tools are missing or fail. <br>
Mitigation: Confirm tool availability before use, continue with available feeds when possible, label degraded sections clearly, and do not fabricate missing data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-coin-analysis) <br>
- [Gate Info CoinAnalysis MCP Specification](references/mcp.md) <br>
- [Gate Info Coin Analysis Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured analysis report with tables, bullet points, links, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate Info and Gate News MCP data when available; unavailable dimensions are labeled rather than fabricated.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
