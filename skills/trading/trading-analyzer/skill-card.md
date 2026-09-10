## Description:

Multi-source trading analyzer (`/drunk-trading-analyzer`) combining crypto data from TradingView, stock data from Alpha Vantage, and market intelligence from Yahoo Finance into unified analysis reports with price trends, technical indicators, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baoduy](https://clawhub.ai/user/baoduy)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and market analysts use this skill to gather crypto and stock market data, screen assets, and produce consolidated market analysis reports. Outputs should be treated as informational analysis rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable third-party MCP packages and broad MCP discovery can run unexpected server code or expose local context.

Mitigation: Review configured MCP servers before use, pin package versions instead of relying on @latest examples, and run market-data MCP servers with a limited environment.

Risk: The skill handles an Alpha Vantage API key for stock analysis.

Mitigation: Use a dedicated revocable Alpha Vantage key and avoid exposing unrelated environment variables to MCP servers.

Risk: Generated trading signals may be incomplete, stale, or misleading.

Mitigation: Treat outputs as informational market analysis only and do not rely on them as investment advice.

## Reference(s):

- [Trading Analyzer ClawHub Skill Page](https://clawhub.ai/baoduy/skills/drunk-trading-analyzer)
- [mcporter Documentation](https://github.com/steipete/mcporter)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/spec)
- [TradingView](https://www.tradingview.com/)
- [Alpha Vantage Documentation](https://www.alphavantage.co/documentation)
- [Yahoo Finance](https://finance.yahoo.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and JSON data, with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require configured MCP servers and ALPHAVANTAGE_API_KEY for stock analysis.]

## Skill Version(s):

0.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
