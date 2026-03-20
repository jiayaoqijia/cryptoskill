# NEAR Intents Skill v2.0.0 — Production Release

## 🎉 Production-Ready Cross-Chain Swap & Bridge

Universal cross-chain swap and bridge tool for OpenClaw agents, powered by the official [NEAR Intents 1Click SDK](https://github.com/defuse-protocol/one-click-sdk-typescript).

---

## ✨ What's New in v2.0.0

### 🛡️ Critical Safety Features
- **Mandatory Refund Address Protection** - Prevents permanent fund loss on failed swaps
- **Cross-Chain Validation** - Automatic detection of origin chain and refund requirements
- **Clear Error Messages** - Educates users about refund address requirements
- **Updated Documentation** - Comprehensive safety guidelines for AI agents

### 🔧 Technical Improvements
- Full integration with 1Click SDK v0.1.1
- Support for 14+ blockchains (NEAR, Base, Ethereum, Arbitrum, Solana, Bitcoin, etc.)
- Automatic decimal conversion for all tokens
- Built-in token map for common assets
- Status polling with timeout handling
- Manual & Auto modes for maximum flexibility

### 📚 Documentation Updates
- **SKILL.md** - Primary reference with safety warnings
- **AI-AGENT-GUIDE.md** - Step-by-step workflows for agents
- **TOKENS.md** - Complete token reference with decimals
- **USAGE_GUIDE.md** - Common patterns and troubleshooting
- **INSTALL.md** - Quick setup instructions

---

## 🚀 Quick Start

### 1. Install the Skill

```bash
# Download and extract to OpenClaw skills directory
cd /root/.openclaw/skills/
tar -xzf near-intents-v2.0.0.tar.gz
cd near-intents

# Install dependencies
npm install
```

### 2. Configure (Optional for Auto Mode)

Create `.env` file for auto-sending from NEAR:
```env
NEAR_ACCOUNT_ID=your-account.near
NEAR_PRIVATE_KEY=ed25519:...
NEAR_RPC_URL=https://rpc.mainnet.fastnear.com
NEAR_NETWORK_ID=mainnet
ONE_CLICK_JWT=optional_jwt_token  # Avoids 0.2% fee
```

Register for JWT at: https://partners.near-intents.org

### 3. Use in Your Agent

```typescript
import { executeIntent } from './index';

// NEAR → Base USDC (Auto mode)
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0xYourBaseAddress',
});

// Base USDC → NEAR (Manual mode) - REQUIRES refundAddress!
const quote = await executeIntent({
  assetIn: 'base:USDC',
  assetOut: 'NEAR',
  amount: '0.5',
  recipient: 'your.near',
  refundAddress: '0xYourBaseAddress',  // CRITICAL!
  mode: 'manual',
});
```

---

## ⚠️ CRITICAL: Refund Address Safety

**When swapping FROM non-NEAR chains** (Base, Arbitrum, Ethereum, Solana, Bitcoin, etc.):

✅ **DO**: Always ask the user for their wallet address on the origin chain
❌ **DON'T**: Assume, guess, or skip the refund address

**Why?** If a swap fails, tokens are refunded to this address. Wrong address = **permanent fund loss**.

**Example Flow:**
```
User: "Swap 0.5 USDC from Base to ETH on NEAR"
Agent: "What's your Base wallet address? (For refunds if the swap fails)"
User: "0x123..."
Agent: [Generates quote with refundAddress: '0x123...']
```

---

## 🌐 Supported Chains

| Chain | Assets | Example Symbol |
|-------|--------|----------------|
| NEAR | NEAR, USDC, USDT, wNEAR | `NEAR`, `USDC` |
| Base | ETH, USDC | `base:ETH`, `base:USDC` |
| Ethereum | ETH, USDC | `eth:ETH`, `eth:USDC` |
| Arbitrum | ETH, ARB, USDC | `arb:ETH`, `arb:ARB` |
| Solana | SOL, USDC | `sol:SOL`, `sol:USDC` |
| Bitcoin | BTC (native only) | `btc:BTC` |
| Dogecoin | DOGE (native only) | `doge:DOGE` |
| + More | See TOKENS.md | |

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| **SKILL.md** | Primary reference - API, parameters, safety rules |
| **AI-AGENT-GUIDE.md** | AI agent workflows and decision trees |
| **TOKENS.md** | Full token list with decimals and asset IDs |
| **USAGE_GUIDE.md** | Common patterns and troubleshooting |
| **INSTALL.md** | Setup instructions |

---

## 🧪 Testing

```bash
# Run unit tests
npm test

# Test a live swap (uses real NEAR - be careful!)
npm run swap:test

# Check token list
npx ts-node lib-1click/1-get-tokens.ts
```

---

## 🔑 Key Features

- ✅ **14+ Blockchains** - NEAR, Base, ETH, Arbitrum, Solana, Bitcoin, and more
- ✅ **Auto & Manual Modes** - Agent-driven or user-driven swaps
- ✅ **Refund Protection** - Mandatory refund addresses for cross-chain safety
- ✅ **Exact Input/Output** - Specify input amount OR desired output amount
- ✅ **Status Tracking** - Real-time swap monitoring with explorer links
- ✅ **Fee Optimization** - Optional JWT for 0% platform fees
- ✅ **Production Ready** - Comprehensive error handling and validation

---

## 📊 Version History

### v2.0.0 (2026-02-15) - **Current**
- 🛡️ Added mandatory `refundAddress` for cross-chain swaps
- 📚 Comprehensive safety documentation
- ✅ Production-ready release

### v1.0.0 (2026-02-14)
- Initial 1Click SDK integration
- Support for major chains
- Auto/manual modes

---

## 🤝 Support

- **Documentation**: See `SKILL.md` and `AI-AGENT-GUIDE.md`
- **NEAR Intents Docs**: https://docs.near-intents.org
- **1Click SDK**: https://github.com/defuse-protocol/one-click-sdk-typescript
- **Partners Program**: https://partners.near-intents.org

---

## 📜 License

MIT License - See `LICENSE` file

---

## 🙏 Credits

- **Powered by**: [NEAR Intents](https://near-intents.org) & [Defuse Protocol](https://defuse.org)
- **Built for**: [OpenClaw](https://openclaw.ai)
- **Version**: 2.0.0
- **Release Date**: February 15, 2026

---

**Ready to use in production!** 🚀

For questions or issues, consult the documentation files or visit https://docs.near-intents.org
