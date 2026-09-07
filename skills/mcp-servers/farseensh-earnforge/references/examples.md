# Worked Examples

10 end-to-end examples demonstrating common EarnForge workflows. Every command
here is executed against the real CLI by the live suite.

## 1. List Vaults by Asset

Find all USDC vaults sorted by APY:

```bash
earnforge top --asset USDC --limit 5
```

```json
[
  {
    "name": "STEAKUSDC",
    "slug": "morpho:8453:_:0xbeef...",
    "chain": "Base",
    "apy": 3.85,
    "tvl": "$33.8M",
    "protocol": "morpho",
    "risk": { "score": 7.8, "label": "low" }
  }
]
```

## 2. Compare Two Vaults

Side-by-side comparison of Morpho vs Aave USDC vaults:

```bash
earnforge compare morpho:8453:_:0xbeef... aave:1:_:0x9277... --json
```

Output includes APY difference, TVL ratio, risk score delta, and protocol tier comparison.

## 3. Build a Deposit Quote

Quote depositing 1000 USDC into a Base vault:

```bash
earnforge quote --vault morpho:8453:_:0xbeef... --amount 1000 --wallet 0xYourWallet --json
```

The SDK automatically:
- Sets `toToken = vault.address` (Pitfall #5)
- Uses 6 decimals for USDC (Pitfall #9)
- Validates `isTransactional` (Pitfall #13)
- Checks `underlyingTokens` is non-empty (Pitfall #15)

Returns an unsigned transaction for the user to sign.

## 4. Portfolio Allocation

Get a diversified allocation for $50,000 in USDC:

```bash
earnforge suggest --amount 50000 --asset USDC --max-chains 3 --strategy diversified --json
```

```json
{
  "totalAmount": 50000,
  "expectedApy": 4.52,
  "allocations": [
    { "vault": "STEAKUSDC", "amount": 20000, "percentage": 40.0, "apy": 3.85 },
    { "vault": "Aave USDC", "amount": 15000, "percentage": 30.0, "apy": 5.20 },
    { "vault": "Euler USDC", "amount": 10000, "percentage": 20.0, "apy": 4.10 },
    { "vault": "Pendle USDC", "amount": 5000, "percentage": 10.0, "apy": 6.50 }
  ]
}
```

## 5. Withdraw from a Vault

Build a redeem quote to exit a position:

```bash
earnforge withdraw --vault morpho:8453:_:0xbeef... --amount 500 --wallet 0xYourWallet --json
```

Checks `isRedeemable` and `redeemPacks` before building the quote. Warns if the vault is non-redeemable.

## 6. Cross-Chain Deposit

Deposit from Ethereum into a Base vault using LI.FI routing:

```bash
earnforge quote --vault morpho:8453:_:0xbeef... --amount 1000 --wallet 0xYourWallet --from-chain 1 --json
```

The Composer API handles the bridge + swap + deposit in a single quote. To
compare costs across source chains, add `--optimize-gas` to the same `quote`
command. There is no separate `gas-optimize` command:

```bash
earnforge quote --vault morpho:8453:_:0xbeef... --amount 1000 --wallet 0xYourWallet --optimize-gas --json
```

## 7. Risk Analysis

Get a full risk breakdown for a vault:

```bash
earnforge risk morpho:8453:_:0xbeef... --json
```

```json
{
  "slug": "morpho:8453:_:0xbeef...",
  "name": "STEAKUSDC",
  "score": 9.7,
  "breakdown": {
    "tvl": 10,
    "apyStability": 10,
    "protocol": 9,
    "redeemability": 10,
    "assetType": 9,
    "verification": 10,
    "rewardDependency": 10
  },
  "label": "low",
  "flags": []
}
```

Seven dimensions, weighted:

| Dimension | Weight | What it reads |
|---|---|---|
| `verification` | 0.22 | LI.FI's own `verificationStatus`. The heaviest input. |
| `tvl` | 0.18 | Deeper liquidity, more scrutiny. $100M+ scores 10. |
| `protocol` | 0.18 | Track record and audit surface, not size. |
| `apyStability` | 0.14 | Divergence between current and trailing APY. |
| `redeemability` | 0.10 | Exitable via Composer, or a liquidity trap. |
| `assetType` | 0.10 | Stablecoin exposure vs volatile, plus IL risk. |
| `rewardDependency` | 0.08 | Yield from incentives can stop; lending fees usually do not. |

`verification` carries 0.22 deliberately: a flagged vault caps at **7.96** even
with a perfect showing everywhere else, so **no flagged vault can ever be
labelled low risk**. Labels are `low >= 8`, `medium >= 6`, `high` below that.

`flags` is a plain-language array: `"96% of APY comes from token incentives"`,
`"TVL under $100k"`, `"flagged by LI.FI verification: apy_outlier"`: ordered
roughly by severity.

## 8. Portfolio Suggestion with Strategy

Use the conservative strategy for a safe allocation:

```bash
earnforge suggest --amount 100000 --asset USDC --strategy conservative --json
```

The conservative strategy applies these filters:
- Only stablecoin-tagged vaults
- TVL > $50M
- Blue-chip protocols only (aave, morpho, euler, pendle, yearn)

Other strategies: `max-apy` (no filters, pure APY sort), `diversified` (3+ chains, $1M+ TVL), `risk-adjusted` (risk score >= 7).

## 9. Full Deposit Flow with Allowance Check

The complete deposit flow has 3 steps: quote, approve, deposit.

```bash
# Step 1: Build deposit quote
earnforge quote --vault morpho:8453:_:0xbeef... --amount 100 --wallet 0xYour --json
# Note the approvalAddress in the response

# Step 2: Check if approval is needed
earnforge allowance --token 0xUSDC --owner 0xYour --spender 0xApprovalAddr --amount 100000000 --chain 8453 --rpc https://mainnet.base.org --json
# If sufficient: false, sign the approvalTx first

# Step 3: Execute deposit (user signs the transactionRequest from step 1)
```

The SDK's `buildDepositQuote()` handles toToken, decimals, and pitfall validation automatically. The allowance check uses a raw JSON-RPC `eth_call` to read the ERC-20 contract.

## 10. Withdraw from a Vault

Withdrawal reverses the deposit: fromToken is the vault share token, toToken is the underlying.

```bash
# Check if vault is redeemable
earnforge vault morpho:8453:_:0xbeef... --json | jq '.isRedeemable'

# Build withdrawal quote
earnforge withdraw --vault morpho:8453:_:0xbeef... --amount 50 --wallet 0xYour --json
```

The Composer uses the same `/v1/quote` endpoint with swapped tokens. Cross-chain withdrawals are supported: add `--to-chain` and `--to-token` for the destination.
