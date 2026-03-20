# Flux (Power by Fluid) Quick Commands

Protocol-specific scripts are under `scripts/flux/` (separate from Venus Core scripts).

## 1) List all Flux lending markets + APY details

```bash
node scripts/flux/fetch_markets.js
```

APY math used:
- `supplyRateBps`: already bps (`1% = 100`)
- `rewardsRateRaw`: Fluid rewards precision (`1% = 1e12`)
- `rewardsRateBps = rewardsRateRaw / 1e10`
- `totalApr = (supplyRateBps + rewardsRateBps) / 100`

## 2) Check wallet Flux positions

```bash
node scripts/flux/position.js --wallet 0xYourWallet
```

## 3) Simulate lend

```bash
node scripts/flux/lend.js --asset fUSDC --amount 10 --wallet 0xYourWallet --mode simulate
```

## 4) Broadcast lend

```bash
node scripts/flux/lend.js --asset fUSDC --amount 10 --wallet 0xYourWallet --mode broadcast --private-key 0x... --confirm YES
```

## 5) Simulate withdraw

```bash
node scripts/flux/withdraw.js --asset fUSDC --amount 5 --wallet 0xYourWallet --mode simulate
```

## 6) Broadcast withdraw

```bash
node scripts/flux/withdraw.js --asset fUSDC --amount 5 --wallet 0xYourWallet --mode broadcast --private-key 0x... --confirm YES
```

## Addresses source
- `references/flux-bnb-addresses.json`
- derived from Instadapp `fluid-contracts-public/deployments/bnb`
