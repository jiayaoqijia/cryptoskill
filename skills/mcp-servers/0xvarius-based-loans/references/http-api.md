# Based Loans HTTP API

For agents without MCP support. Base URL: `https://mcp.based.loans`. All endpoints are `GET`, need no key, and return JSON. Rate limit: 30 requests per minute per IP.

## Read-only

| MCP tool | HTTP |
|---|---|
| `get_protocol_info` | `/v1/protocol` |
| `list_markets` | `/v1/markets?only_with_funds=true` |
| `get_market` | `/v1/market?asset=WETH` |
| `get_risk_report` | `/v1/risk?asset=HYDX` |
| `quote_borrow` | `/v1/quote?asset=WETH&collateral=0.5&term=short` (optional `loan_usdc`) |
| `get_borrower_loans` | `/v1/loans?borrower=<wallet>` |
| `get_lender_position` | `/v1/lender?address=<wallet>` |
| `request_token_listing` | `/v1/request-token?token=<address>` |
| `explain_collateral_types` | `/v1/collateral-types` |

## Transactions (unsigned)

Each returns `{ chainId, summary, warnings, calls }`. `calls` is an ordered list of `{ to, data, value, description }` for chain ID 8453, in the shape `wallet_sendCalls` expects. The user's wallet signs and sends them in order. `value` is always `0`.

| MCP tool | HTTP |
|---|---|
| `build_borrow` | `/v1/tx/borrow?asset=&collateral=&term=&borrower=<wallet>` (optional `loan_usdc`) |
| `build_buyback` | `/v1/tx/buyback?loan_id=&borrower=<wallet>` (optional `payment_usdc`; omit to repay in full) |
| `build_deposit` | `/v1/tx/deposit?amount_usdc=&lender=<wallet>&limits=WETH:250,cbBTC:250` |
| `build_set_limits` | `/v1/tx/limits?lender=<wallet>&limits=WETH:500` |
| `build_withdraw` | `/v1/tx/withdraw?amount_usdc=<amount or max>&lender=<wallet>` (optional `as_musdc=true`) |
| `build_claim_proceeds` | `/v1/tx/claim-proceeds?loan_ids=1,2` (optional `mode=redeploy`) |
| `build_claim_collateral` | `/v1/tx/claim-collateral?loan_ids=1,2` |

Errors come back as `{ error, code }` with a plain-language message, for example `NOTHING_TO_WITHDRAW`. `GET /v1` lists every endpoint.
