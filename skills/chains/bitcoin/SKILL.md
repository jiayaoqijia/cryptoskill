---
name: Bitcoin
description: Assist with Bitcoin transactions, wallets, Lightning, and security decisions.
metadata: {"clawdbot":{"emoji":"₿","os":["linux","darwin","win32"]}}
---

## Wallet Compatibility Traps
- Same seed phrase in different wallets can show zero balance — derivation paths differ (BIP44 for legacy, BIP84 for native segwit, BIP86 for taproot). Ask which wallet created the seed before troubleshooting "missing funds"
- Importing a seed into a watch-only wallet won't show funds if the wallet defaults to a different address type than the original
- Some exchanges still reject bc1p (taproot) addresses for withdrawals — verify before giving the user a taproot address

## Fee Timing
- Bitcoin fees follow predictable patterns: weekends and UTC night hours (00:00-06:00) are typically 50-80% cheaper than weekday peaks
- mempool.space/api/v1/fees/recommended gives current sat/vB rates — wallet built-in estimates are often 12-24 hours stale
- A transaction at 1 sat/vB during high congestion can stay unconfirmed for 2+ weeks, but will eventually drop from mempools (not fail, just disappear)

## Stuck Transaction Recovery
- RBF (Replace-By-Fee): sender broadcasts new tx with higher fee — only works if original was flagged replaceable (most modern wallets do this by default now)
- CPFP (Child-Pays-For-Parent): receiver creates a high-fee tx spending the unconfirmed output, incentivizing miners to confirm both — useful when sender didn't enable RBF
- If user is the receiver and stuck tx has no change output to them, CPFP won't help — they must wait or ask sender to RBF

## Lightning Network Gotchas
- Lightning invoices expire (default 1 hour on many wallets) — an expired invoice cannot receive payment even if the payer tries
- "Inbound liquidity" limits how much a user can receive — a fresh channel can send but not receive until the balance shifts
- Closing a channel during high on-chain fees can cost more than the channel balance — warn users before force-closing small channels
- Lightning payments are not automatically retried — if a route fails, the user must manually retry or the payment fails permanently

## Privacy and Security Patterns
- Dust attacks: tiny amounts sent to addresses to link them when user spends — advise not to consolidate dust with main UTXOs
- Address reuse lets anyone see full transaction history of that address — each receive should use a fresh address
- Clipboard malware silently replaces copied addresses — always verify first and last 6 characters match on both devices before confirming send
- Hardware wallet "verify on device" step is critical — if malware changed the address, only the device screen shows the real destination

## Scam Recognition
- "Send X BTC, receive 2X back" is always a scam — no exceptions, even if the account looks official
- "Recovery services" that ask for seed phrase will steal everything — legitimate recovery never needs the seed
- Fake wallet apps in app stores with slight name variations — verify publisher and download count before recommending
- "Support" DMing users on social media asking to "validate wallet" or "sync" — real support never initiates contact

## Verification APIs
- mempool.space is the current standard block explorer — blockchain.info is outdated and less reliable for fee data
- Transaction confirmed = included in a block. 1 confirmation is minimum, 6 is standard for high-value, some exchanges require 3
- Check raw tx with: `curl -s "https://mempool.space/api/tx/{txid}"` — returns full transaction details including fee, size, confirmation status
- For address balance: `curl -s "https://mempool.space/api/address/{address}"` — shows funded/spent totals
