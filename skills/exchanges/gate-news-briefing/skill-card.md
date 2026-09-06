## Description: <br>
Gate News Briefing produces crypto news briefings from recent events, trending headlines, and social sentiment returned by the read-only Gate-News MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate timely crypto market news briefings, including general market updates, coin-specific news, major events, trending headlines, and social sentiment. It is intended for news-only requests and routes multi-dimension analysis to other skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto news queries and topics are shared with the enabled Gate-News MCP service. <br>
Mitigation: Install and use this skill only with a trusted Gate-News MCP server, and avoid sending private or sensitive trading context. <br>
Risk: Crypto headlines, event feeds, and sentiment summaries can be incomplete, stale, or misleading. <br>
Mitigation: Verify important crypto headlines independently before acting, and treat the briefing as news context rather than investment advice. <br>
Risk: Required Gate-News MCP tools can be unavailable or partially fail. <br>
Mitigation: Label degraded sections, continue only with available sources, and do not fabricate missing headlines, events, or sentiment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-news-briefing) <br>
- [Gate News Briefing Runtime Rules](artifact/references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md) <br>
- [Gate News Briefing MCP Specification](artifact/references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefing with sections for major events, trending headlines, social sentiment, and watch items.] <br>
**Output Parameters:** [1D; optional coin, time_range, and topic inputs guide the briefing.] <br>
**Other Properties Related to Output:** [Requires Gate-News MCP availability; partial tool failures are labeled or omitted rather than fabricated.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
