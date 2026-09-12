## Description:

Provides recent crypto news briefings by retrieving Gate-News events, top headlines, and social sentiment, then deduplicating and summarizing them with source attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate concise crypto market news briefings, including recent events, trending headlines, and social sentiment. It is intended for news-only requests and routes multi-dimension analysis to other Gate skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The general briefing path may favor English sources, which can limit coverage for non-English or region-specific news.

Mitigation: Ask for the desired language or region when that coverage matters, and adjust the news query path accordingly.

Risk: MCP tool failures or sparse feeds can result in missing events, news, or sentiment sections.

Mitigation: Label degraded sections clearly, continue with available sources, and avoid fabricating missing headlines or events.

Risk: Crypto news and sentiment summaries can be mistaken for trading recommendations.

Mitigation: Keep summaries objective, preserve time range and source attribution, and state that the briefing is not investment advice.

## Reference(s):

- [Gate News Briefing Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate News Briefing MCP Specification](references/mcp.md)
- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-news-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefing with ranked events, headlines, sentiment summary, and fallback notices.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate-News MCP data; does not produce local files, credentials, or executable code.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
