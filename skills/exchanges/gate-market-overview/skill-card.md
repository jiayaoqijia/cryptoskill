## Description:

Market overview skill for crypto-wide market conditions, intended only for requests that do not ask for specific coin analysis or another analysis dimension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce a market-wide crypto briefing from Gate Info MCP market, ranking, DeFi, macro, and event data. It is for broad market status questions, not single-coin analysis, contract risk review, trading advice, or news-only requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a broad crypto market summary as investment advice.

Mitigation: Present outputs as informational market data, keep a neutral tone, and include the skill's not-investment-advice framing.

Risk: Unavailable or stale MCP data could make a market overview incomplete.

Mitigation: Use the documented graceful degradation behavior: omit unavailable dimensions, label missing data clearly, and avoid fabricating values.

Risk: The skill may be used for requests outside its intended scope, such as single-coin analysis, technical analysis, or contract risk review.

Mitigation: Route those requests to the more specific Gate skill instead of stretching this market overview workflow.

## Reference(s):

- [Gate Info Market Overview Skill](https://clawhub.ai/gate-exchange/skills/gate-info-market-overview)
- [Gate publisher profile](https://clawhub.ai/user/gate-exchange)
- [Gate Info MarketOverview MCP Specification](references/mcp.md)
- [Gate Info Market Overview Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Scenarios & Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown market overview report with tables and concise narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate Info MCP availability; partial outputs should clearly mark missing market, DeFi, macro, ranking, or event data.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter version 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
