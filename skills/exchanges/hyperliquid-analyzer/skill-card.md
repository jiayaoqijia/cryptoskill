## Description:

Analyze Hyperliquid market data and provide trading insights, including real-time price monitoring, trend analysis, and risk assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b0on](https://clawhub.ai/user/b0on)

### License/Terms of Use:


## Use Case:

Developers and traders use this skill to query Hyperliquid market data, summarize trends, assess volatility, and review portfolio-related context when optional wallet configuration is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional wallet or API-key configuration could expose account context if shared with an agent or stored insecurely.

Mitigation: Review environment variables before use and provide only the access needed for the intended market-analysis task.

Risk: Market-analysis output may be mistaken for authorized trading execution or financial advice.

Mitigation: Treat outputs as informational analysis, keep trading authority separate, and review recommendations before acting.

## Reference(s):

- [Hyperliquid Analyzer on ClawHub](https://clawhub.ai/b0on/skills/hyperliquid-analyzer)
- [Hyperliquid public info API endpoint](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and market-analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use curl and jq; optional wallet and API-key environment variables can add portfolio context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
