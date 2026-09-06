## Description: <br>
Gate DEX Market helps agents retrieve Gate DEX market data such as token prices, K-lines, rankings, holder information, liquidity, and token risk checks without initiating swaps or wallet actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route read-only Gate DEX market-data requests through MCP by default, or through Gate OpenAPI when explicitly requested. It supports price lookup, candlestick data, token rankings, token security checks, tradable-token discovery, holder analysis, and liquidity-event review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary rates the release as suspicious because it can introduce persistent Gate API credentials, mutable remote runtime rules, installer-side agent routing changes, and broad signed API access. <br>
Mitigation: Install only after reviewing the release, constraining or avoiding OpenAPI mode where possible, and using a dedicated low-privilege Gate API key instead of broadly privileged credentials. <br>
Risk: OpenAPI mode stores Gate API credentials locally and uses signed API requests. <br>
Mitigation: Prefer MCP mode for unauthenticated market queries; when OpenAPI is required, protect the local credential file, mask secrets in responses, and rotate credentials if exposed. <br>
Risk: The installer can modify agent routing files and may affect existing local configuration. <br>
Mitigation: Back up existing agent configuration before running the installer and review generated routing changes before relying on them. <br>
Risk: The skill depends on remote runtime rules, and server-resolved provenance for this release is unavailable. <br>
Mitigation: Review the remote runtime rules before use and do not infer source provenance from artifact text when assessing release origin. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-dex-market) <br>
- [Gate DEX Market MCP reference](references/mcp.md) <br>
- [Market OpenAPI shared reference](references/openapi/_shared.md) <br>
- [Market OpenAPI token data reference](references/openapi/token-data.md) <br>
- [Market OpenAPI market data reference](references/openapi/market-data.md) <br>
- [Gate DEX MCP endpoint](https://api.gatemcp.ai/mcp/dex) <br>
- [Gate DEX OpenAPI endpoint](https://openapi.gateweb3.cc/api/v1/dex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tool-call guidance, shell command examples, configuration snippets, and JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market-data posture in MCP mode; OpenAPI mode may use persistent local Gate API credentials when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
