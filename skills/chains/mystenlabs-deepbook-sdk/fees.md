# Fee Structure and DEEP Staking

## Fee payment options

DeepBook supports two fee payment methods per order, controlled by the `payWithDeep` flag:

- **DEEP (default):** The pool prices fees using its on-chain DEEP conversion rate. This is the cheaper option.
- **Input token:** The pool charges a 25% premium over DEEP-denominated fees.

Paying in DEEP requires the pool to have a DEEP price point. Established pools have one. A brand-new permissionless pool can only charge input-token fees until an operator adds a price point from a reference pool.

## DEEP fee calculation

Pools maintain a `DeepPrice` object storing up to 100 recent conversion-rate points between the pool's asset and DEEP. The system:

1. Divides cumulative rate by point count to calculate `deep_per_asset`
2. Multiplies by trade size to determine the fee in DEEP

Since this rate fluctuates, fees cannot be hardcoded — always read them on-chain.

## Fee tiers

Taker fee, maker fee, and stake requirement are per-pool governance parameters. Read them on-chain rather than hardcoding, because governance can change them.

Fee bounds by pool type:

| Pool type | Taker fee range | Maker fee range |
|-----------|----------------|-----------------|
| Whitelisted (DEEP/SUI, DEEP/USDC) | 0 bps | 0 bps |
| Stable pairs (e.g., WUSDT/USDC, AUSD/USDC) | 0.1–1 bps | 0–0.5 bps |
| Volatile pairs (e.g., BETH/USDC, NS/SUI) | 1–10 bps | 0–5 bps |

## DEEP staking for fee discounts

Staking DEEP can halve your taker fee when both conditions are met:

1. Active stake meets the pool's minimum stake requirement
2. Trading volume meets the pool's volume threshold

DEEP deposits into BalanceManager serve dual purposes: paying trading fees and enabling staking for fee discounts. The same DEEP balance handles both functions.

## Maker rebates

Maker rebates activate when users exceed minimum stake thresholds and contribute maker volume. Rebate availability correlates inversely with trading volume relative to 28-day medians — lower-volume epochs have higher rebate rates.

## Governance

Users with non-zero DEEP stake can propose parameter changes to any pool. Proposals cover:

- Taker fee adjustment
- Maker fee adjustment
- Stake requirement adjustment

Voting power follows a formula combining linear and square-root components, capped at 100,000 DEEP. Proposals require 50% quorum of active stake to pass and take effect the following epoch.

## Acquiring DEEP on testnet

Two methods:

1. **Token-request form (recommended):** Use the DeepBook testnet token request form to receive DEEP directly.
2. **Swap SUI for DEEP:** Convert faucet SUI to DEEP on the whitelisted `DEEP_SUI` pool (liquidity-dependent).

## Funding a BalanceManager with DEEP

### Reading DEEP requirements

Use `getQuantityOut` to simulate a trade and determine the exact DEEP needed for fees:

```typescript
const result = await client.deepbook.deepBook.getQuantityOut({
  poolKey: "SUI_USDC",
  baseQuantity: 10,
  quoteQuantity: 0,
});
// result includes the DEEP fee amount
```

### Depositing DEEP

```typescript
const tx = new Transaction();
client.deepbook.balanceManager.depositIntoManager("MANAGER_1", "DEEP", 100)(tx);
await signAndExecute(tx);
```

### Bootstrapping DEEP via swap

If you have SUI but no DEEP, swap on the whitelisted DEEP/SUI pool (0% fees):

```typescript
const tx = new Transaction();
const [baseCoin, quoteCoin, deepCoin] = tx.add(
  client.deepbook.deepBook.swapExactQuoteForBase({
    poolKey: "DEEP_SUI",
    amount: 1,            // SUI to spend
    deepAmount: 0,        // whitelisted pool — no DEEP needed for fees
    minOut: 0,
  })
);

// Transfer returned coins back to sender — required or coins are destroyed
tx.transferObjects([baseCoin, quoteCoin, deepCoin], keypair.toSuiAddress());
await signAndExecute(tx);
```

## Referral system

### Pool-level referrals

- `mintReferral(poolKey, multiplier)` — create a referral object (multiplier: 0.1–2.0, multiples of 0.1)
- `updatePoolReferralMultiplier(poolKey, id, multiplier)` — adjust fee allocation
- `claimPoolReferralRewards(poolKey, id)` — collect accumulated rewards
- `getPoolReferralBalances(poolKey, id)` — view current reward balances
- `poolReferralMultiplier(poolKey, id)` — check current multiplier

### BalanceManager referrals

- `setBalanceManagerReferral(managerKey, referralId, tradeCap)` — link a referral to a BalanceManager for a specific pool
- `unsetBalanceManagerReferral(managerKey, poolKey, tradeCap)` — remove the referral link
- `getBalanceManagerReferralId(managerKey, poolKey)` — check linked referral
