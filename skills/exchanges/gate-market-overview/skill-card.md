## Description: <br>
Provides a crypto market overview for queries about overall market conditions, using Gate Info and Gate News MCP data to summarize market breadth, sector leaders, DeFi metrics, recent events, and macro context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask for a market-wide crypto briefing rather than coin-specific analysis. The skill gathers read-only market snapshot, rankings, DeFi, events, and macro data and returns a concise Markdown overview with missing data clearly labeled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Gate Info and Gate News MCP server configured in the user's environment. <br>
Mitigation: Install and run it only in environments where the configured MCP server is trusted, and use the documented Gate tools only. <br>
Risk: Market summaries may be mistaken for investment advice or over-applied to coin-specific, technical, risk, or portfolio questions. <br>
Mitigation: Treat the report as informational market context, keep the non-investment-advice disclaimer, and route specialized requests to the appropriate Gate skill. <br>
Risk: Unavailable or stale market, macro, DeFi, or event data can make the overview incomplete. <br>
Mitigation: Label missing or stale sections clearly, avoid fabricating unavailable metrics, and provide a partial report only from available data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-info-market-overview) <br>
- [Gate Info Market Overview Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Gate Info MarketOverview MCP Specification](references/mcp.md) <br>
- [Scenarios & Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown report with tables, section summaries, data freshness notes, and a non-investment-advice disclaimer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; uses documented Gate Info and Gate News MCP tools and degrades gracefully when data is unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter version: 2026.4.6-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
