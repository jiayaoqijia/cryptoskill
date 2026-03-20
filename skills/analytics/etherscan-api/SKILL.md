---
name: etherscan-api
description: Use when you need to query Etherscan API V2 for onchain activity, contract metadata, ABI/source retrieval, proxy implementation discovery, and transaction/log analysis across EVM chains.
---

# Etherscan API V2

## Overview
Use this skill to fetch onchain data from Etherscan-compatible explorers using the unified V2 API.

Core model:
- One base URL: `https://api.etherscan.io/v2/api`
- One API key
- Switch chains via `chainid`

Explorer URLs relevant to this workspace:
- Ethereum mainnet: `https://etherscan.io/`
- Ethereum hoodi: `https://hoodi.etherscan.io/`
- Taiko mainnet: `https://taikoscan.io/`
- Taiko hoodi: `https://hoodi.taikoscan.io/`

Read first:
- `references/network-map.md`
- `references/endpoint-cheatsheet.md`
- `references/rate-limits.md`
- `references/explorer-url-patterns.md`

## Required Inputs
Collect these before querying:
- `ETHERSCAN_API_KEY`
- Target `chainid`
- Address / tx hash / block range
- Endpoint intent (activity, logs, source, ABI, status)

## Deterministic Workflow
1. Pick `chainid` from `references/network-map.md`.
2. Choose endpoint by intent from `references/endpoint-cheatsheet.md`.
3. Build request on `https://api.etherscan.io/v2/api` with required params.
4. Parse `status`, `message`, `result`.
5. If contract endpoint returns proxy metadata (`Proxy == "1"`), follow `Implementation`.
6. For large history, paginate (`page`, `offset`) and/or narrow block ranges.

## Method Selection
| Goal | Module / Action |
| --- | --- |
| Address normal tx history | `account` / `txlist` |
| Address internal tx history | `account` / `txlistinternal` |
| ERC20 transfer history | `account` / `tokentx` |
| Event logs | `logs` / `getLogs` |
| Contract ABI | `contract` / `getabi` |
| Contract source + proxy fields | `contract` / `getsourcecode` |
| Contract deployer + creation tx | `contract` / `getcontractcreation` |
| Tx execution status | `transaction` / `getstatus` |
| Tx receipt status | `transaction` / `gettxreceiptstatus` |

## Quick Commands
Set key once:
```bash
export ETHERSCAN_API_KEY="<your_key>"
```

Get ABI (Taiko mainnet example):
```bash
curl -s "https://api.etherscan.io/v2/api?chainid=167000&module=contract&action=getabi&address=<contract>&apikey=$ETHERSCAN_API_KEY"
```

Get source + proxy metadata (Taiko hoodi example):
```bash
curl -s "https://api.etherscan.io/v2/api?chainid=167013&module=contract&action=getsourcecode&address=<contract>&apikey=$ETHERSCAN_API_KEY"
```

Get address activity in block window:
```bash
curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address=<address>&startblock=<from>&endblock=<to>&page=1&offset=100&sort=desc&apikey=$ETHERSCAN_API_KEY"
```

Get logs for a contract in block window:
```bash
curl -s "https://api.etherscan.io/v2/api?chainid=560048&module=logs&action=getLogs&address=<contract>&fromBlock=<from>&toBlock=<to>&page=1&offset=1000&apikey=$ETHERSCAN_API_KEY"
```

## Proxy-Aware Contract Handling
When `getsourcecode` returns:
- `Proxy: "1"`
- non-empty `Implementation`

then:
1. Keep runtime call target as proxy address.
2. Fetch ABI/source from implementation address.
3. Decode selectors against implementation ABI.
4. Re-check implementation before privileged write analysis.

## Safety Rails
Never skip these checks:
- Always set correct `chainid`; wrong chain silently yields wrong context.
- Respect plan limits and add client-side throttling/retries.
- Treat `status: "0"` as non-success even with HTTP 200.
- For analytics windows, lock `startblock`/`endblock` explicitly.
- For logs, remember `offset` max is 1000 per query and paginate.
- Keep retries idempotent and resume scans from stored cursors/block checkpoints.

## Expected Output
Return:
- exact URL/query used (without exposing secret key)
- chain (`chainid` + explorer)
- endpoint (`module`/`action`)
- parsed status/result summary
- proxy follow-up decisions (`Proxy`, `Implementation`) when contract-related
