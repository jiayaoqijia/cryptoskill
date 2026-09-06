# Solana JSON-RPC — Core Methods

Standard methods supported by any Solana RPC provider. Full reference: https://solana.com/docs/rpc

All methods are POST to the RPC URL with body:
```json
{"jsonrpc": "2.0", "id": 1, "method": "<method>", "params": [<args>]}
```

**Always include `maxSupportedTransactionVersion: 0`** in config for transaction methods — otherwise v0 transactions (most modern ones) fail with "Transaction version not supported".

---

## Accounts

### `getAccountInfo(pubkey, config?)`
Returns account state and data.
- `config.encoding`: `"base58"` | `"base64"` | `"base64+zstd"` | `"jsonParsed"` — use `"jsonParsed"` for SPL tokens
- `config.commitment`: `"processed"` | `"confirmed"` | `"finalized"`
Response: `{lamports, owner, data, executable, rentEpoch, space}`

### `getBalance(pubkey, config?)`
SOL balance in **lamports** (1 SOL = 1e9 lamports).

### `getMultipleAccounts([pubkey, ...], config?)` — **BATCH**
Up to 100 addresses per call. Same config as getAccountInfo.
**Use this instead of looping getAccountInfo.**

### `getProgramAccounts(programId, config?)` ⚠️ EXPENSIVE
Returns all accounts owned by a program.
**NEVER call without filters:**
```json
{
  "filters": [
    {"dataSize": 165},                          // for SPL token accounts
    {"memcmp": {"offset": 0, "bytes": "<mint base58>"}}
  ],
  "encoding": "jsonParsed"
}
```
For NFTs/tokens by owner or collection: **use DAS API instead** — `getProgramAccounts` routinely times out.

### `getTokenAccountBalance(tokenAccount, config?)`
Balance of a specific SPL token account.
Response: `{amount, decimals, uiAmount, uiAmountString}`

### `getTokenAccountsByOwner(owner, {mint}|{programId}, config?)`
All SPL token accounts for an owner. Can filter by specific mint or by program.
**Prefer DAS `getAssetsByOwner` with `showFungible: true`** — it returns metadata too.

### `getTokenSupply(mint, config?)`
Total supply of an SPL token.

### `getTokenLargestAccounts(mint, config?)`
Top 20 holders.

---

## Blocks

### `getSlot(config?)`
Current slot number.

### `getBlockHeight(config?)`
Current block height (different from slot — skipped slots don't increment this).

### `getLatestBlockhash(config?)`
Response includes `blockhash` and `lastValidBlockHeight`. Use for tx building.

### `getBlock(slot, config?)` ⚠️ LARGE RESPONSE
Full block contents.
- `config.encoding`: `"jsonParsed"` for readable
- `config.maxSupportedTransactionVersion: 0` REQUIRED
- `config.transactionDetails`: `"full"` (default, huge) | `"signatures"` | `"accounts"` | `"none"` — use minimal needed
- `config.rewards: false` — reduces payload

**Use HTTP timeout ≥ 30s.** Response can be megabytes. If you only need signatures, set `transactionDetails: "signatures"` for ~100× smaller response.

Error `-32009` "Slot skipped" means this slot wasn't produced — try `slot+1`.

### `getBlockTime(slot)`
Unix seconds when block was produced. **Seconds precision only** — useless for sub-second timing.

### `getBlocks(startSlot, endSlot?, commitment?)`
List of confirmed slots in range. Max 500,000 slots per call.

---

## Transactions

### `getTransaction(signature, config?)`
Full transaction.
```json
{
  "encoding": "jsonParsed",
  "commitment": "confirmed",
  "maxSupportedTransactionVersion": 0
}
```
Response shape includes: `slot`, `blockTime`, `transaction.message.instructions`, `meta.err`, `meta.fee`, `meta.preBalances/postBalances`, `meta.preTokenBalances/postTokenBalances`, `meta.innerInstructions`, `meta.logMessages`.

**Response size: ~10-20 KB per tx typically.**

### `getSignaturesForAddress(address, config?)`
Signatures referencing an address, most recent first.
```json
{
  "limit": 1000,              // max 1000 per call
  "before": "<signature>",    // cursor: sigs older than this
  "until": "<signature>",     // cursor: sigs newer than this
  "commitment": "confirmed"
}
```
Paginate by setting `before` to last sig of previous page.

**Note:** doesn't include tx for token accounts owned by this wallet — for **complete wallet history** prefer Helius `getTransactionsForAddress` (see `helius-extensions.md`).

### `getSignatureStatuses([sig, ...], config?)` — **BATCH**
Status of up to 256 signatures in one call.
- `searchTransactionHistory: true` to search beyond recent cache
Response: `confirmationStatus`, `confirmations`, `err`, `slot`.

### `simulateTransaction(transaction, config?)`
Dry-run without submitting. Great for catching errors before paying fees.
Returns `logs`, `unitsConsumed`, `returnData`, `err`, `accounts` (changed state).

### `sendTransaction(transaction, config?)`
Submit a signed tx.
- `skipPreflight: false` — if true, skips simulation (faster but risky)
- `preflightCommitment: "processed"`
- `maxRetries: 0` — let client handle retries
Returns signature string.

**For reliable landing: prefer Helius Sender or QuickNode Lil JIT (Jito bundles).**

---

## Fees & prioritization

### `getFeeForMessage(message, config?)`
Estimate cost of a serialized message. Returns null if blockhash expired.

### `getRecentPrioritizationFees(pubkeys?)`
Historical priority fees (in microlamports) from recent slots. Returns up to 150 slots.
**Manual analysis needed** to derive a good fee — prefer `getPriorityFeeEstimate` (Helius) or `qn_estimatePriorityFees` (QuickNode).

---

## Cluster info

### `getHealth()`
Returns `"ok"` or error — use as liveness check.

### `getEpochInfo(config?)`
Current epoch, slot index within epoch, slot height.

### `getVersion()`
Node version (solana-core + feature-set).

### `getClusterNodes()`
All validators. Rarely needed.

### `getStakeMinimumDelegation()`
Current min stake (in lamports).

---

## Encodings

| Encoding | Use |
|----------|-----|
| `base58` | Raw, most compact |
| `base64` | Default for binary data |
| `base64+zstd` | Compressed binary |
| `jsonParsed` | Human-readable; only works for known programs (SPL Token, Stake, Vote, System) — unknown programs fall back to base64 |

For account data: try `jsonParsed` first for SPL tokens; fall back to `base64` + manual parse otherwise.

---

## Commitment levels

| Level | When block counts |
|-------|-------------------|
| `processed` | Immediately, may revert |
| `confirmed` | 2/3 supermajority voted |
| `finalized` | 32+ confirmations (deeply final) |

Defaults:
- Reads: use `confirmed` unless building a financial history — then `finalized`
- Never `processed` for anything involving money
- `sendTransaction` preflight: `processed` OK (fast)

---

## Pagination patterns

### `getSignaturesForAddress` (cursor-based)
```python
all_sigs = []
before = None
while True:
    r = rpc.getSignaturesForAddress(addr, {"limit": 1000, "before": before})
    sigs = r.get("result", [])
    if not sigs:
        break
    all_sigs.extend(sigs)
    before = sigs[-1]["signature"]
```

### `getBlocks` (range-based)
Fetch in ranges of max 500,000 slots at a time.

### For account-heavy programs
Use DAS `searchAssets` with `page` param — supports ~500k results with pagination, way beyond raw RPC.
