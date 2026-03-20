# Quick Start Guide

## Install
```bash
cd /root/.openclaw/skills/
tar -xzf near-intents-v2.0.0.tar.gz
cd near-intents
npm install
```

## Use
```typescript
import { executeIntent } from './index';

// NEAR → Base (no config needed for NEAR origin)
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0x...',
});

// Base → NEAR (REQUIRES refundAddress!)
await executeIntent({
  assetIn: 'base:USDC',
  assetOut: 'NEAR',
  amount: '0.5',
  recipient: 'user.near',
  refundAddress: '0x...',  // Your Base wallet
  mode: 'manual',
});
```

## ⚠️ Important
Always provide `refundAddress` when swapping FROM non-NEAR chains!

See SKILL.md for full documentation.
