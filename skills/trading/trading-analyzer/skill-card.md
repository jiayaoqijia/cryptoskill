## Description: <br>
Multi-source trading analyzer combining cryptocurrency data, stock data, and market intelligence into unified reports with price trends, technical indicators, and sentiment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baoduy](https://clawhub.ai/user/baoduy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query configured MCP market-data tools and produce cryptocurrency, stock, and market screening analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on mcporter and configured MCP server packages that can access third-party market-data providers. <br>
Mitigation: Install only trusted MCP packages and prefer pinned package versions for repeatable review. <br>
Risk: Stock analysis requires an Alpha Vantage API key and examples show shell-profile configuration. <br>
Mitigation: Store API keys in appropriate environment or secret-management channels and avoid committing or syncing shell profiles that contain credentials. <br>
Risk: Market queries, watchlists, and trading research may be sent to configured third-party providers. <br>
Mitigation: Avoid submitting confidential watchlists or proprietary trading research unless sharing those queries with the configured providers is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baoduy/drunk-trading-analyzer) <br>
- [Alpha Vantage API](https://www.alphavantage.co/api/) <br>
- [Alpha Vantage Documentation](https://www.alphavantage.co/documentation) <br>
- [Model Context Protocol Specification](https://modelcontextprotocol.io/spec) <br>
- [TradingView](https://www.tradingview.com/) <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured MCP servers and external market-data providers; report completeness depends on provider availability and configured credentials.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
