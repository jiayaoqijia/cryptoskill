---
name: kukapay-hyperliquid-info-mcp
description: "An MCP server that provides real-time data and insights from the Hyperliquid perp DEX for use in bots, dashboards, and analytics."
---

# kukapay-hyperliquid-info-mcp

_Source: [github.com/kukapay/hyperliquid-info-mcp](https://github.com/kukapay/hyperliquid-info-mcp). The body below is the upstream README.md captured at the time of registration._

---

# Hyperliquid Info MCP Server

An MCP server that provides real-time data and insights from the Hyperliquid perp DEX for use in bots, dashboards, and analytics.

![GitHub License](https://img.shields.io/github/license/kukapay/hyperliquid-info-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **User Data Queries**:
  - `get_user_state`: Fetch user positions, margin, and withdrawable balance for perpetuals or spot markets.
  - `get_user_open_orders`: Retrieve all open orders for a user account.
  - `get_user_trade_history`: Get trade fill history with details like symbol, size, and price.
  - `get_user_funding_history`: Query funding payment history with customizable time ranges.
  - `get_user_fees`: Fetch user-specific fee structures (maker/taker rates).
  - `get_user_staking_summary` & `get_user_staking_rewards`: Access staking details and rewards.
  - `get_user_order_by_oid` & `get_user_order_by_cloid`: Retrieve specific order details by order ID or client order ID.
  - `get_user_sub_accounts`: List sub-accounts associated with a main account.

- **Market Data Tools**:
  - `get_all_mids`: Get mid prices for all trading pairs.
  - `get_l2_snapshot`: Fetch Level 2 order book snapshots for a specific coin.
  - `get_candles_snapshot`: Retrieve candlestick data with customizable intervals and time ranges.
  - `get_coin_funding_history`: Query funding rate history for a specific coin.
  - `get_perp_dexs`: Fetch metadata about perpetual markets (using `meta`).
  - `get_perp_metadata` & `get_spot_metadata`: Get detailed metadata for perpetual and spot markets, with optional asset contexts.

- **Analysis Prompt**:
  - `analyze_positions`: A guided prompt to analyze user trading activity using relevant tools.

- **ISO 8601 Support**: Time-based queries (`get_candles_snapshot`, `get_coin_funding_history`, `get_user_funding_history`) accept ISO 8601 time strings for precise data filtering.

## Installation

### Prerequisites
- **Python 3.10**: Required by the Hyperliquid Python SDK.
- A valid Hyperliquid account address for user-specific queries.
- [uv](https://github.com/astral-sh/uv) or [pip](https://pip.pypa.io/en/stable/) for package management.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/hyperliquid-info-mcp.git
   cd hyperliquid-info-mcp
   ```

2. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv sync
   ```

## Usage

### Running the Server
Run the server in development mode with MCP Inspector:
```bash
mcp dev main.py
```
Or install it for use in Claude Desktop:
```bash
mcp install main.py --name "Hyperliquid Info"
```

### Example Usage

Using the MCP Inspector or Claude Desktop, you can interact with the server using natural language prompts. Below are examples of how to trigger the `analyze_positions` prompt and individual tools conversationally.

1. **Analyze Trading Positions**:
   - **Prompt**:  
     "Please analyze the trading activity for my Hyperliquid account with address 0xYourAddress. Provide insights on my positions, open orders, and recent trades."
   - **Behavior**:  
     This triggers the `analyze_positions` prompt, which uses `get_user_state`, `get_user_open_orders`, `get_user_trade_history`, `get_user_funding_history`, and `get_user_fees` to fetch data and generate a risk/performance analysis.
   - **Example Output**:  
     ```
     For account 0xYourAddress:
     - Current Positions: 0.1 BTC long at $50,000, unrealized PNL +$500.
     - Open Orders: 1 limit order to sell 0.05 BTC at $52,000.
     - Recent Trades: Bought 0.1 BTC at $50,000 on 2025-05-30.
     - Funding Payments: Paid $10 in funding fees last week.
     - Fees: Maker fee 0.02%, taker fee 0.05%.
     Recommendation: Monitor BTC price closely due to high leverage.
     ```

2. **Fetch User State**:
   - **Prompt**:  
     "Show me the current state of my Hyperliquid account 0xYourAddress, including my positions and margin details for perpetuals."
   - **Behavior**:  
     Invokes `get_user_state(account_address="0xYourAddress", check_spot=False)`.
   - **Example Output**:  
     ```
     {
       "assetPositions": [
         {
           "position": {
             "coin": "BTC",
             "szi": "0.1",
             "entryPx": "50000.0",
             "markPx": "50500.0",
             "unrealizedPnl": "500.0"
           }
         }
       ],
       "marginSummary": {
         "accountValue": "10000.0",
         "totalMarginUsed": "2000.0"
       },
       "withdrawable": "8000.0"
     }
     ```

3. **Get Candlestick Data**:
   - **Prompt**:  
     "Can you get the 1-minute candlestick data for ETH on Hyperliquid from January 1, 2025, to January 2, 2025?"
   - **Behavior**:  
     Invokes `get_candles_snapshot(coin_name="ETH", interval="1m", start_time="2025-01-01T00:00:00Z", end_time="2025-01-02T00:00:00Z")`.
   - **Example Output**:  
     ```
     [
       {
         "t": 1672531200000,
         "o": "3000.0",
         "h": "3010.0",
         "l": "2995.0",
         "c": "3005.0",
         "v": "1000.0"
       },
       ...
     ]
     ```

4. **Check Trade History**:
   - **Prompt**:  
     "What are the recent trades for my account 0xYourAddress on Hyperliquid?"
   - **Behavior**:  
     Invokes `get_user_trade_history(account_address="0xYourAddress")`.
   - **Example Output**:  
     ```
     [
       {
         "coin": "ETH",
         "px": "3000.0",
         "sz": "0.5",
         "time": 1672531200000,
         "tid": "123456"
       },
       ...
     ]
     ```

5. **Fetch Market Metadata**:
   - **Prompt**:  
     "Tell me about the perpetual markets available on Hyperliquid, including trading pairs."
   - **Behavior**:  
     Invokes `get_perp_metadata(include_asset_ctxs=False)`.
   - **Example Output**:  
     ```
     {
       "universe": [
         {
           "name": "BTC-PERP",
           "maxLeverage": 50,
           "szDecimals": 4,
           "tickSz": "0.1"
         },
         ...
       ]
     }
     ```


## License
This project is licensed under the [MIT License](LICENSE).

