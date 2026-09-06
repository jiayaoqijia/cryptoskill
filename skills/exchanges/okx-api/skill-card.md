## Description: <br>
OKX API helps agents work with OKX REST API v5 and WebSocket workflows for market data, account and position queries, and order management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XHFkindergarten](https://clawhub.ai/user/XHFkindergarten) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading automation teams use this skill to help an agent prepare OKX API calls, configuration, and example code for market data, account checks, and order lifecycle tasks. It is most relevant when the agent is expected to guide REST or WebSocket access to OKX with user-provided credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live OKX financial account access and order placement. <br>
Mitigation: Use demo mode first, prefer read-only or least-privilege API keys, disable withdrawals, consider IP allowlisting, and require manual confirmation before any live order, amendment, or cancellation. <br>
Risk: The release includes an unrelated local git-push permission. <br>
Mitigation: Remove or review the git-push permission before deployment unless it is intentionally needed in the target environment. <br>
Risk: Misconfigured or over-privileged API credentials could expose account data or enable unwanted trading activity. <br>
Mitigation: Store credentials only in the intended environment mechanism, keep secrets out of prompts and logs, and scope keys to the minimum OKX permissions required for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XHFkindergarten/okx-api) <br>
- [OKX](https://www.okx.com) <br>
- [Authentication Reference](references/authentication.md) <br>
- [Market Data Endpoints Reference](references/market-data-endpoints.md) <br>
- [Trading Endpoints Reference](references/trading-endpoints.md) <br>
- [WebSocket Reference](references/websocket.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, Python examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live API request guidance requiring configured OKX credentials and user confirmation for trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
