# Quick Commands

## 1) Check USDT market now
```bash
python scripts/venus_check.py --symbol vUSDT
```

## 2) Auto-read wallet exposure onchain (no manual numbers)
```bash
python scripts/venus_check.py \
  --symbol vUSDT \
  --wallet 0xYourWallet
```

## 3) Auto-read wallet + what-if borrow simulation
```bash
python scripts/venus_check.py \
  --symbol vUSDT \
  --wallet 0xYourWallet \
  --extra-borrow 120 \
  --target-health 1.30
```

## 4) Manual mode (fallback)
```bash
python scripts/venus_check.py \
  --symbol vUSDT \
  --wallet 0xYourWallet \
  --weighted-collateral 1500 \
  --debt 1000
```

## 5) English brief output (Telegram-friendly)
```bash
python scripts/venus_check.py --symbol vUSDT --wallet 0xYourWallet --output brief --lang en
```

## 6) Deposit preview (safe, no transaction)
```bash
node scripts/venus_deposit.js --asset vUSDT --amount 10 --wallet 0xYourWallet --mode simulate
```

## 7) Deposit broadcast (real tx, explicit confirmation)
```bash
node scripts/venus_deposit.js \
  --asset vUSDT \
  --amount 10 \
  --private-key 0xYourPrivateKey \
  --mode broadcast \
  --confirm YES
```

## 8) Withdraw preview with HF safety prediction
```bash
node scripts/venus_withdraw.js \
  --asset vUSDC \
  --amount 1 \
  --wallet 0xYourWallet \
  --safe-hf 1.2 \
  --mode simulate
```

## 9) Withdraw broadcast (blocks if predicted HF < safety line)
```bash
node scripts/venus_withdraw.js \
  --asset vUSDC \
  --amount 1 \
  --private-key 0xYourPrivateKey \
  --by underlying \
  --safe-hf 1.2 \
  --mode broadcast \
  --confirm YES
```

## 9.1) Force-risk withdraw (not recommended)
```bash
node scripts/venus_withdraw.js ... --force-risk YES
```

## 10) Borrow preview
```bash
node scripts/venus_borrow.js --asset vUSDT --amount 1 --wallet 0xYourWallet --mode simulate
```

## 11) Borrow broadcast
```bash
node scripts/venus_borrow.js --asset vUSDT --amount 1 --private-key 0xYourPrivateKey --mode broadcast --confirm YES
```

## 12) Repay preview
```bash
node scripts/venus_repay.js --asset vUSDT --amount 1 --wallet 0xYourWallet --mode simulate
```

## 13) Repay broadcast
```bash
node scripts/venus_repay.js --asset vUSDT --amount 1 --private-key 0xYourPrivateKey --mode broadcast --confirm YES
```

## 14) Collateral enable/disable
```bash
node scripts/venus_collateral.js --asset vUSDT --action enable --wallet 0xYourWallet --mode simulate
node scripts/venus_collateral.js --asset vUSDT --action disable --wallet 0xYourWallet --mode simulate
```

## 15) HF monitor (custom safe line)
```bash
python scripts/hf_monitor.py --wallet 0xYourWallet --safe-hf 1.2 --warn-hf 1.35 --critical-hf 1.15
```

## Notes
- Auto mode reads onchain balances via `getAccountSnapshot`.
- Manual mode expects USD values for `weighted-collateral` and `debt`.
- BNB Chain mainnet uses `--chain-id 56` (default).
- `--output brief --lang en` returns concise English summary lines.
- Execution scripts default to simulation; broadcast requires `--confirm YES`.
