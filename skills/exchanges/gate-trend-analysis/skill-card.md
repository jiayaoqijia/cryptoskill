## Description:

Performs read-only, single-coin trend and technical analysis on Gate using K-line, market snapshot, indicator history, and multi-timeframe signal data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate technical and trend-analysis reports for one cryptocurrency at a time, including current market snapshot, indicators, support and resistance, multi-timeframe signals, and risk warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mandatory shared runtime-rule files in the parent directory that were outside the reviewed package.

Mitigation: Before installing, verify the parent shared rule files are trusted, versioned with the package, and contain only expected Gate Info or Gate News operating rules.

Risk: Technical analysis may be mistaken for investment advice or used as a basis for trading decisions.

Mitigation: Treat outputs as read-only market analysis, preserve the skill's no-trading-advice warnings, and do not rely on the report for trading decisions.

Risk: Market data or indicator responses can be unavailable, partial, or conflicting across timeframes.

Mitigation: Disclose missing data, label timeframes clearly, downgrade confidence when signals conflict, and avoid fabricating indicator values.

## Reference(s):

- [Gate Info TrendAnalysis MCP Specification](artifact/references/mcp.md)
- [Scenarios and Prompt Examples](artifact/references/scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-info-trend-analysis)

## Skill Output:

**Output Type(s):** [analysis, markdown, API calls, guidance]

**Output Format:** [Markdown report with tables and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate Info MCP data; reports unavailable data explicitly and does not provide trading advice.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
