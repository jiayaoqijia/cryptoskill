---
name: kukapay-crypto-feargreed-mcp
description: "A mcp server that provides real-time and historical Crypto Fear & Greed Index data, powered by the Alternative.me."
---

# kukapay-crypto-feargreed-mcp

_Source: [github.com/kukapay/crypto-feargreed-mcp](https://github.com/kukapay/crypto-feargreed-mcp). The body below is the upstream README.md captured at the time of registration._

---

# Crypto Fear & Greed Index MCP Server

A mcp server that provides real-time and historical Crypto Fear & Greed Index data, powered by the Alternative.me.

This server exposes resources and tools for fetching and analyzing the Fear & Greed Index, making it easy to integrate into MCP-compatible clients, including Claude Desktop.

![GitHub](https://img.shields.io/github/license/kukapay/crypto-feargreed-mcp) 
![GitHub last commit](https://img.shields.io/github/last-commit/kukapay/crypto-feargreed-mcp) 
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Features

- **Current Index**: Retrieve the latest Fear & Greed Index value and classification.
- **Historical Data**: Fetch historical index values for a specified number of days.
- **Trend Analysis**: Analyze trends over time with statistics like average value and trend direction.
- **Tool-Only Support**: Includes tool versions of all resources for compatibility with tool-only MCP clients.
- **Prompt Generation**: Provides a prompt template for interpreting index values.

### Resources

- `fng://current`. Current crypto Fear & Greed Index. Output: 
```
Crypto Fear & Greed Index (as of 2025-03-15 00:00:00 UTC):
Value: 45
Classification: Fear
```

- `fng://history/{days}`. Historical Data of Crypto Fear & Greed Index.Output:
```
Historical Crypto Fear & Greed Index:
2025-03-15 00:00:00 UTC: 45 (Fear)
2025-03-14 00:00:00 UTC: 48 (Fear)
...
```

### Tools

- `get_current_fng_tool() -> str`. 

Current Index. Same as `fng://current`

- `get_historical_fng_tool(days: int) -> str`. 

Historical Index Data. Same as `fng://history/{days}`

- `analyze_fng_trend(days: int) -> str`. 

Index trend Analysis. Output:
```
Fear & Greed Index Analysis (30 days):
Latest Value: 45 (Fear) at 2025-03-15 00:00:00 UTC
Average Value: 47.3
Trend: falling
Data points analyzed: 30
```

### Prompts

- `interpret_fng`

Index Data Interpretation.

Output:
```
Please interpret this Crypto Fear & Greed Index value and explain what it means for cryptocurrency markets (specifically Bitcoin): 45
```

## Installation

### Installing via Smithery

To install Crypto Fear & Greed Index for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kukapay/crypto-feargreed-mcp):

```bash
npx -y @smithery/cli install @kukapay/crypto-feargreed-mcp --client claude
```

Clone the repository:

```bash
git clone https://github.com/kukapay/crypto-feargreed-mcp.git
cd crypto-feargreed-mcp
```  

Install for Claude Desktop
```
mcp install main.py --name "CryptoFearGreed"
```
Then enable it in your Claude Desktop configuration.

For other clients, add a server entry to your configuration file:

```
"mcpServers": { 
  "crypto-feargreed-mcp": { 
    "command": "uv", 
    "args": [ 
      "--directory", "/your/path/to/crypto-feargreed-mcp", 
      "run", 
      "main.py" 
    ]
  } 
}
```

## Examples

After installation, ask:

- "What's the current Crypto Fear & Greed Index?"
- "Show me the Crypto Fear & Greed Index trend for the last 30 days." 

Claude will automatically call the appropriate tools and provide responses.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).
- Data provided by [Alternative.me Fear & Greed Index API](https://api.alternative.me/fng/).