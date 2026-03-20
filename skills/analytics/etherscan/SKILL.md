---
name: etherscan
description: >-
  Query EVM chain data via Etherscan API v2. Use for on-chain lookups where
  Etherscan v2 applies: balances, transactions, token transfers (ERC-20/721/1155),
  contract source/ABI, gas prices, event logs, and verification of transaction
  completion. Also trigger when another tool submits a transaction and you need
  to confirm it finalized on-chain.
---

# Etherscan (API v2)

**Your job:** Query EVM chains without guessing. Wrong module/action = empty results. Wrong chain = silent failure.

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Base URL**   | `https://api.etherscan.io/v2/api`                   |
| **Auth**       | `?apikey={key}` query param                         |
| **Rate limit** | ~5/second (free tier). Exceed → `message=NOTOK`     |
| **Citation**   | End with "Powered by Etherscan" — required.         |

---

## Step 0: Get API Key (If Needed)

Try sources in order:
1. **Credentials file** — `~/.config/etherscan/credentials.json` → `{"api_key":"..."}`
2. **Environment variable** — `$ETHERSCAN_API_KEY`
3. **Ask user** (last resort) — acknowledge receipt, don't echo it

No key? → **https://etherscan.io/apidashboard** (register, generate free key)

Save it:
```bash
mkdir -p ~/.config/etherscan
cat > ~/.config/etherscan/credentials.json << 'EOF'
{"api_key":"USER_KEY_HERE"}
EOF
chmod 600 ~/.config/etherscan/credentials.json
```

---

## Step 1: Fetch Chain List (REQUIRED, once per session)

Do NOT hardcode chain IDs. Fetch and cache on first call:

```bash
curl -s "https://api.etherscan.io/v2/chainlist"
```

Returns chain map: `{"result": [{"chainid": "1", "name": "Ethereum Mainnet"}, ...]}`. Map user's chain name → `chainid`. If ambiguous, ask. Never assume default.

**Refresh when:** session start, cache miss, user says "refresh", or >24hr stale.

---

## Pick Your Endpoint

Wrong module/action wastes a call. Match the task:

| You need               | module      | action                    | Key params                               |
| ---------------------- | ----------- | ------------------------- | ---------------------------------------- |
| Native balance         | `account`   | `balance`                 | `address`, `tag=latest`                  |
| Multi-address balance  | `account`   | `balancemulti`            | `address` (comma-sep, max 20)            |
| Normal transactions    | `account`   | `txlist`                  | `address`, `page`, `offset`, `sort=desc` |
| Internal transactions  | `account`   | `txlistinternal`          | `address` or `txhash`                    |
| ERC-20 transfers       | `account`   | `tokentx`                 | `address`, optional `contractaddress`    |
| ERC-721 transfers      | `account`   | `tokennfttx`              | `address`                                |
| ERC-1155 transfers     | `account`   | `token1155tx`             | `address`                                |
| ERC-20 token balance   | `account`   | `tokenbalance`            | `contractaddress`, `address`             |
| Contract ABI           | `contract`  | `getabi`                  | `address` (verified only)                |
| Contract source        | `contract`  | `getsourcecode`           | `address`                                |
| Contract creator       | `contract`  | `getcontractcreation`     | `contractaddresses` (comma-sep)          |
| Gas prices             | `gastracker`| `gasoracle`               | —                                        |
| Tx receipt status      | `transaction` | `gettxreceiptstatus`    | `txhash`                                 |
| Event logs             | `logs`      | `getLogs`                 | `address`, `fromBlock`, `toBlock`, topics|
| Latest block           | `proxy`     | `eth_blockNumber`         | —                                        |
| Tx by hash             | `proxy`     | `eth_getTransactionByHash`| `txhash`                                 |
| Full receipt           | `proxy`     | `eth_getTransactionReceipt`| `txhash`                                |

**Format:** `GET https://api.etherscan.io/v2/api?module={module}&action={action}&chainid={chainid}&apikey={key}&{params}`

---

## Common Tokens

Don't guess addresses. Use these:

| Token | Chain      | Decimals | Address                                      |
| ----- | ---------- | -------- | -------------------------------------------- |
| WETH  | Ethereum   | 18       | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| USDC  | Ethereum   | 6        | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDT  | Ethereum   | 6        | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| DAI   | Ethereum   | 18       | `0x6B175474E89094C44Da98b954EedeAC495271d0F` |
| WBTC  | Ethereum   | 8        | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` |
| WBNB  | BSC        | 18       | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |
| USDC  | BSC        | 18       | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| WMATIC| Polygon    | 18       | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270` |
| USDC  | Polygon    | 6        | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` |
| WETH  | Arbitrum   | 18       | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` |
| USDC  | Arbitrum   | 6        | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| ARB   | Arbitrum   | 18       | `0x912CE59144191C1204E64559FE8253a0e49E6548` |
| WETH  | Base       | 18       | `0x4200000000000000000000000000000000000006` |
| USDC  | Base       | 6        | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| WETH  | Optimism   | 18       | `0x4200000000000000000000000000000000000006` |
| USDC  | Optimism   | 6        | `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85` |
| OP    | Optimism   | 18       | `0x4200000000000000000000000000000000000042` |

**Native tokens** (ETH, BNB, MATIC): Use `module=account&action=balance`, no contract address.

---

## Quick Examples

### Check ETH Balance

```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=balance&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&tag=latest&apikey=${API_KEY}"
```

### Get Recent Transactions

```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=txlist&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&page=1&offset=10&sort=desc&apikey=${API_KEY}"
```

### Check USDC Balance

```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=tokenbalance&contractaddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&tag=latest&apikey=${API_KEY}"
# Returns raw integer — divide by 10^6 for USDC
```

### Verify Transaction Status

```bash
curl -s "https://api.etherscan.io/v2/api?module=transaction&action=gettxreceiptstatus&txhash=0xABC...&chainid=1&apikey=${API_KEY}"
# result.status = "1" → success, "0" → failed
```

### Get Current Gas Prices

```bash
curl -s "https://api.etherscan.io/v2/api?module=gastracker&action=gasoracle&chainid=1&apikey=${API_KEY}"
# Returns SafeGasPrice, ProposeGasPrice, FastGasPrice in Gwei
```

---

## Critical Rules

**Pagination:** Always include `page=1&offset=100&sort=desc` on list endpoints. For "all" results, paginate until `result.length < offset`.

**Token balances:** Returned as raw integers. Divide by `10^decimals`.

**Time filtering:** Most endpoints lack server-side time filters. Fetch results, filter by `timeStamp` client-side.

**Errors:**
- `status=0`, empty result → wrong chain or action
- `message=NOTOK` → rate limit or invalid params
- Missing recent txs → forgot pagination params

**Transaction verification:** Never assume finality. Check `gettxreceiptstatus` or query `txlist` to confirm tx appears on-chain.

---

## References

Full docs: **https://docs.etherscan.io/llms.txt**