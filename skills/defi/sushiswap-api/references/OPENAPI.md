# OpenAPI usage guide

This skill relies entirely on the OpenAPI schema located at:

[openapi.yaml](openapi.yaml)

That file is the **single source of truth** for all endpoints, parameters, and responses.

## Versioning model

- `openapi.yaml` always represents the latest supported version
- When the API changes, this file is replaced in place

Agents must not assume backward compatibility beyond what the schema describes.

## Endpoint categories

Endpoints are grouped using OpenAPI tags:

- `swap` — quoting and swap transaction generation
- `price` — token price lookups
- `token` — token metadata
- `liquidity-providers` — routing liquidity sources

Use these tags to quickly identify relevant endpoints.

## Quotes vs swaps

- Quote endpoints return **pricing and routing information**
- Swap endpoints return **executable transaction data**
  - `tx.to`
  - `tx.data`
  - `tx.value`
  - `tx.gas`

Agents must never attempt to fabricate transaction calldata.

## Parameters and defaults

- Optional parameters have safe defaults defined in the schema
- Numeric tolerances (slippage, price impact) are decimals (e.g. `0.005 = 0.5%`)
- Comma-separated lists (DEXes, pools, tokens) must be passed as strings

## Handling API updates

If a request fails unexpectedly:
1. Re-read `openapi.yaml`
2. Verify the endpoint path and parameters still exist
3. Adjust request construction to match the updated schema

No other skill files require modification when the API updates.
