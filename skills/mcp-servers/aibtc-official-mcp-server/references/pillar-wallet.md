# Pillar Smart Wallet

Pillar is an sBTC smart wallet with built-in DeFi integration via Zest Protocol.

## Two Modes

### Browser Handoff Mode (`pillar_*` tools)

For human users with passkey authentication:
1. MCP creates operation intent
2. Opens Pillar in browser
3. Sign with passkey (biometric/PIN)
4. MCP polls for completion

### Agent Direct Mode (`pillar_direct_*` tools)

For autonomous agents - no browser needed:
1. Generate signing key: `pillar_key_generate`
2. Create wallet: `pillar_direct_create_wallet`
3. Execute operations: `pillar_direct_send`, `pillar_direct_boost`, etc.
4. Keys auto-unlock using derived password from `PILLAR_API_KEY`

**Recommended for agents**: Use `pillar_direct_*` tools for headless automation.

## Connection

Connect to your existing Pillar wallet:

```
"Connect my Pillar wallet"
```

Uses `pillar_connect` - opens browser, auto-connects if logged in, returns your wallet address.

Check connection status:

```
"Am I connected to Pillar?"
```

Uses `pillar_status` - shows wallet address if connected.

## Sending sBTC

Send to BNS names, Pillar wallet names, or Stacks addresses:

```
"Send 10000 sats to muneeb.btc"
"Send 50000 sats to my-friend wallet on Pillar"
"Send 25000 sats to SP2..."
```

Uses `pillar_send` with recipient types:
- `bns` - BNS names (alice.btc)
- `wallet` - Pillar wallet names
- `address` - Raw Stacks addresses (SP...)

## Funding Your Wallet

Three funding methods available:

### From Exchange (Coinbase, Binance, etc.)

```
"Fund my Pillar wallet from an exchange"
```

Uses `pillar_fund` with `method: "exchange"` - generates a deposit address.

### From Leather/Xverse (BTC)

```
"Deposit BTC from my Leather wallet"
```

Uses `pillar_fund` with `method: "btc"` - auto-converts BTC to sBTC.

### From Leather/Xverse (sBTC)

```
"Transfer sBTC from my Xverse wallet"
```

Uses `pillar_fund` with `method: "sbtc"` - direct sBTC transfer.

## Yield with Zest Protocol

### Supply sBTC

Deposit sBTC to earn yield:

```
"Supply my sBTC to Zest"
```

Uses `pillar_supply` - deposits to Zest Protocol lending pool.

### Boost Position

Create leveraged exposure (up to 1.5x):

```
"Boost my sBTC position"
"Boost 100000 sats"
```

Uses `pillar_boost` - supplies sBTC, borrows against it, re-supplies. Large amounts (>100k sats) automatically use DCA mode.

### Check Position

View your current position:

```
"What's my Pillar position?"
```

Uses `pillar_position` - shows balance, collateral, borrowed amount, LTV, liquidation price.

### Unwind Position

Close or reduce your leverage:

```
"Unwind 50% of my position"
```

Uses `pillar_unwind` - repays borrowed sBTC and withdraws collateral.

## Tool Reference

### Browser Handoff Tools

**Connection & Transactions:**
| Tool | Description |
|------|-------------|
| `pillar_connect` | Connect to wallet (opens browser) |
| `pillar_disconnect` | Clear local session |
| `pillar_status` | Check connection |
| `pillar_send` | Send sBTC |
| `pillar_fund` | Fund wallet |

**DeFi (Zest Protocol):**
| Tool | Description |
|------|-------------|
| `pillar_supply` | Supply to Zest |
| `pillar_boost` | Leverage position |
| `pillar_unwind` | Close position |
| `pillar_auto_compound` | Configure auto-compound |
| `pillar_position` | View position |

**Wallet Management:**
| Tool | Description |
|------|-------------|
| `pillar_create_wallet` | Create new wallet |
| `pillar_add_admin` | Add backup admin |
| `pillar_invite` | Get referral link |

**DCA Partnerships:**
| Tool | Description |
|------|-------------|
| `pillar_dca_invite` | Invite DCA partner |
| `pillar_dca_partners` | View DCA partners |
| `pillar_dca_leaderboard` | View leaderboard |
| `pillar_dca_status` | Check DCA status |

### Agent Direct Tools (Recommended for Agents)

**Key Management:**
| Tool | Description |
|------|-------------|
| `pillar_key_generate` | Generate signing keypair |
| `pillar_key_unlock` | Unlock signing key |
| `pillar_key_lock` | Lock signing key |
| `pillar_key_info` | Show key status |

**Direct Operations:**
| Tool | Description |
|------|-------------|
| `pillar_direct_create_wallet` | Create wallet + register key |
| `pillar_direct_send` | Send sBTC |
| `pillar_direct_supply` | Supply to Zest |
| `pillar_direct_boost` | Leverage position |
| `pillar_direct_unwind` | Close position |
| `pillar_direct_withdraw_collateral` | Withdraw sBTC from Zest |
| `pillar_direct_auto_compound` | Configure auto-compound |
| `pillar_direct_add_admin` | Add backup admin |
| `pillar_direct_position` | View position |
| `pillar_direct_quote` | Get boost quote |

**Direct DCA Tools:**
| Tool | Description |
|------|-------------|
| `pillar_direct_dca_invite` | Invite DCA partner |
| `pillar_direct_dca_partners` | View DCA partners |
| `pillar_direct_dca_leaderboard` | View leaderboard |
| `pillar_direct_dca_status` | Check DCA status |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PILLAR_API_URL` | API base URL (default: https://pillarbtc.com) |
| `PILLAR_API_KEY` | Bearer token for auth |

## More Information

- [Pillar Website](https://pillarbtc.com)
- [Twitter @pillar_btc](https://x.com/pillar_btc)
- [CLAUDE.md Pillar Section](../../CLAUDE.md#pillar-smart-wallet)

---

*Back to: [SKILL.md](../SKILL.md)*
