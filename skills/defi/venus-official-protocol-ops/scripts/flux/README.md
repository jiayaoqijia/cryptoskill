# Flux Scripts (BSC) — Operational Guide

These scripts are protocol-specific for **Flux/Fluid on BNB Chain**.

## Safety Rules
1. Always run `--mode simulate` first.
2. Start with small amount before production size.
3. Ensure `--wallet` matches signer address (enforced in scripts).
4. Keep private key out of git-tracked files.
5. Prefer single-step changes (one deposit/withdraw at a time).

## Common Commands

### Market snapshot
```bash
node scripts/flux/fetch_markets.js
```

### Position
```bash
node scripts/flux/position.js --wallet 0xYourWallet
```

### Simulate lend
```bash
node scripts/flux/lend.js --asset fUSDC --amount 1 --wallet 0xYourWallet --mode simulate
```

### Broadcast lend
```bash
node scripts/flux/lend.js --asset fUSDC --amount 1 --wallet 0xYourWallet --mode broadcast --private-key 0x... --confirm YES
```

### Simulate withdraw
```bash
node scripts/flux/withdraw.js --asset fUSDC --amount 1 --wallet 0xYourWallet --mode simulate
```

### Broadcast withdraw
```bash
node scripts/flux/withdraw.js --asset fUSDC --amount 1 --wallet 0xYourWallet --mode broadcast --private-key 0x... --confirm YES
```

## Production Templates

### Conservative (small size)
- amount: 0.1 to 1 units
- flow: simulate -> broadcast -> verify position

### Standard (normal size)
- amount: 1 to 20 units
- flow: simulate -> explicit human confirm -> broadcast -> verify position + wallet balance

## Troubleshooting
- `wallet and private key address mismatch`: wrong signer/private key for target wallet.
- `insufficient underlying balance`: wallet token balance too low for requested amount.
- `requested amount exceeds maxWithdraw`: requested withdraw exceeds protocol max withdraw at this time.
