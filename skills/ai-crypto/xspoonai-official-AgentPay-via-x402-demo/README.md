# AgentPay via X402

**AI-powered cross-chain payment automation for USDC transfers between Solana and Base.**

## 🚀 Quick Overview

AgentPay enables AI agents to execute cross-chain USDC payments autonomously with zero human intervention. No browser, no manual signing - just pure API-driven automation.

### Key Features

- 💰 **Cross-chain payments**: Send USDC from Solana or Base to any recipient
- 🔐 **Local wallet management**: Keys never leave your machine
- ⚡ **X402 protocol**: Secure authorization with EIP-712 signatures
- 🎯 **Real-time tracking**: Monitor payment status from intent to settlement
- 🏆 **Leaderboard**: Track your agent's payment activity

### How It Works

1. **Generate wallets locally** (EVM + Solana)
2. **Create payment intent** via API
3. **Sign transaction locally** with X402 authorization
4. **Submit proof** and poll until settled

Merchants always receive USDC on Base. Payers can pay from Solana or Base.

## 📚 Full Documentation

See [SKILL.md](./SKILL.md) for complete API reference, code examples, and security details.

## 🔗 Links

- **API Base**: https://api-pay.agent.tech
- **X402 Protocol**: https://x402.org
- **Supported Chains**: Base (EVM), Solana

## 📄 License

MIT License

---

**Built for the SpoonOS Skills Micro Challenge 🥄**
