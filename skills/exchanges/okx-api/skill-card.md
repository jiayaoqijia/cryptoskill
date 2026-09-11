## Description:

Provides guidance for interacting with OKX REST API v5 including authentication, market data, and order management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhfkindergarten](https://clawhub.ai/user/xhfkindergarten)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query OKX market data, inspect balances and positions, and prepare authenticated REST or WebSocket interactions for account and order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose OKX exchange credentials broadly when live API keys are injected into agent environments.

Mitigation: Use demo mode or separate least-privilege OKX API keys, prefer read-only keys for account queries, and avoid global credential injection for live trading keys.

Risk: The skill can support live order placement, amendment, and cancellation against a real OKX account.

Mitigation: Require explicit confirmation before any live order placement, amendment, or cancellation, and keep OKX_DEMO enabled for testing.

Risk: The artifact includes an unrelated pre-approved git push permission.

Mitigation: Remove the packaged .claude git-push allow rule before installing or running the skill.

## Reference(s):

- [OKX API Skill README](README.md)
- [Authentication Reference](references/authentication.md)
- [Market Data Endpoints](references/market-data-endpoints.md)
- [Trading Endpoints](references/trading-endpoints.md)
- [WebSocket Reference](references/websocket.md)
- [OKX](https://www.okx.com)
- [ClawHub Skill Page](https://clawhub.ai/xhfkindergarten/skills/okx-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated OKX API request patterns, environment variable configuration, and example scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
