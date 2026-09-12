## Description:

Produces a single-coin crypto analysis report by combining fundamentals, market snapshot, technical signals, recent news, and social sentiment from Gate MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request a standard analysis of one crypto asset and receive a neutral, data-driven Markdown report covering fundamentals, market data, technicals, news, sentiment, and risk warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat crypto market analysis as investment advice.

Mitigation: Keep the output neutral and data-driven, include the not-investment-advice disclaimer, and avoid explicit buy or sell recommendations.

Risk: External market, news, technical, or sentiment feeds may be unavailable, stale, or incomplete.

Mitigation: Label unavailable dimensions clearly, continue only with available data, and avoid fabricating missing facts or signals.

Risk: The workflow depends on the Gate MCP server and external public crypto data services.

Mitigation: Before installing or running the skill, confirm the Gate MCP server source is trusted and that users understand the analysis is informational.

## Reference(s):

- [Gate Info CoinAnalysis MCP Specification](references/mcp.md)
- [Gate Info Coin Analysis Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes degraded-data notes, data-driven risk warnings, and a not-investment-advice disclaimer.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter version 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
