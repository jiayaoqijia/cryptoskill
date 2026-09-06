# Bitcoin Inscription Workflow

Bitcoin inscriptions are permanent data stored on the Bitcoin blockchain. This reference covers the complete inscription process from creation to verification.

## Overview

Bitcoin inscriptions use a two-step process:
1. **Commit transaction** - Lock funds and commit to the inscription script
2. **Reveal transaction** - Broadcast the actual inscription data (after commit confirms)

The inscription data lives in the witness field of the reveal transaction, making it part of the permanent Bitcoin record.

## Complete Workflow

### 1. Check Balance

Inscriptions require BTC for both commit and reveal transactions. Check your balance first:

```
"What's my BTC balance?"
```

Uses `get_btc_balance` - ensure you have enough confirmed satoshis.

### 2. Estimate Fees

Calculate the total cost before creating an inscription:

```
"Estimate fee for a text inscription"
```

Uses `estimate_inscription_fee` - provide content type and base64-encoded content. Returns:
- **Commit fee** - Cost to broadcast commit transaction
- **Reveal fee** - Cost to broadcast reveal transaction
- **Reveal amount** - Total locked in commit (includes reveal fee + dust)
- **Total cost** - Sum of commit fee + reveal amount

### 3. Create Commit Transaction

Broadcast the commit transaction (does NOT wait for confirmation):

```
"Create an inscription with 'Hello, Bitcoin!'"
```

Uses `inscribe` - broadcasts commit tx and returns immediately with:
- `commitTxid` - Transaction ID of commit (save this)
- `revealAddress` - Taproot address where inscription will be created
- `revealAmount` - Amount locked in commit output (save this)
- `feeRate` - Fee rate used (save this)

**Important**: The commit transaction must confirm before you can proceed to the reveal step.

### 4. Wait for Confirmation

Check commit transaction status using the `commitExplorerUrl` from the inscribe response. Typical confirmation times:
- **Fast fees** (~10 sat/vB) - 10-20 minutes
- **Medium fees** (~5 sat/vB) - 30-60 minutes
- **Slow fees** (~2 sat/vB) - 1+ hours

### 5. Broadcast Reveal Transaction

Once the commit confirms, complete the inscription:

```
"Reveal my inscription"
```

Uses `inscribe_reveal` with:
- `commitTxid` - From step 3 inscribe response
- `revealAmount` - From step 3 inscribe response
- `contentType` - Same as step 3 (must match)
- `contentBase64` - Same as step 3 (must match)

Returns:
- `inscriptionId` - Unique ID (`{revealTxid}i0`)
- Commit and reveal transaction details
- Explorer URLs for both transactions

### 6. Verify Inscription

Fetch and parse the inscription content:

```
"Get inscription from transaction abc123..."
```

Uses `get_inscription` with reveal txid. Returns:
- Content type and size
- Body (base64 and text if applicable)
- Metadata (pointer, metaprotocol, encoding)

## Tool Reference

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_taproot_address` | Get wallet's Taproot address for receiving inscriptions | None |
| `estimate_inscription_fee` | Calculate inscription cost | `contentType`, `contentBase64`, `feeRate?` |
| `inscribe` | Broadcast commit transaction (non-blocking) | `contentType`, `contentBase64`, `feeRate?` |
| `inscribe_reveal` | Broadcast reveal transaction (after commit confirms) | `commitTxid`, `revealAmount`, `contentType`, `contentBase64`, `feeRate?` |
| `get_inscription` | Fetch inscription content from reveal tx | `txid` |
| `get_inscriptions_by_address` | List all inscriptions owned by address (mainnet only) | `address?` |

## Content Types and Encoding

All content must be base64-encoded before inscription.

### Text Inscription

**Content Type**: `text/plain`

```bash
echo -n "Hello, Bitcoin!" | base64
# SGVsbG8sIEJpdGNvaW4h
```

**Example**:
```
"Inscribe 'Hello, Bitcoin!' as text/plain"
```

### HTML Inscription

**Content Type**: `text/html`

```bash
echo -n '<html><body><h1>GM</h1></body></html>' | base64
# PGh0bWw+PGJvZHk+PGgxPkdNPC9oMT48L2JvZHk+PC9odG1sPg==
```

**Example**:
```
"Create an HTML inscription with <html>...</html>"
```

### Image Inscription

**Content Type**: `image/png`, `image/jpeg`, `image/svg+xml`

For images, read the file and encode to base64:

```bash
base64 -i image.png
```

**Example**:
```
"Inscribe this PNG image (provide base64 data)"
```

### JSON Inscription

**Content Type**: `application/json`

```bash
echo -n '{"type":"brc-20","tick":"ordi"}' | base64
# eyJ0eXBlIjoiYnJjLTIwIiwidGljayI6Im9yZGkifQ==
```

## Error Cases

### Insufficient Funds

**Symptom**: Inscribe fails with "No UTXOs available"

**Solution**:
1. Check balance with `get_btc_balance`
2. Ensure confirmed balance > total cost (from estimate)
3. Send more BTC to wallet if needed

### Unconfirmed Commit

**Symptom**: Reveal fails with broadcast error

**Solution**:
1. Verify commit transaction has at least 1 confirmation
2. Check explorer URL from inscribe response
3. Wait longer if still pending

### Content Mismatch

**Symptom**: Reveal creates different inscription than expected

**Cause**: Different `contentType` or `contentBase64` used in reveal vs commit

**Solution**: Use exact same parameters from inscribe call when calling inscribe_reveal

### Wallet Not Unlocked

**Symptom**: "Wallet not unlocked" error

**Solution**: Run `wallet_unlock` with your password before inscribing

## Taproot Address Usage

Inscriptions are created at Taproot (P2TR) addresses following BIP86 derivation:

| Network | Prefix | Derivation Path |
|---------|--------|----------------|
| Mainnet | `bc1p...` | `m/86'/0'/0'/0/0` |
| Testnet | `tb1p...` | `m/86'/1'/0'/0/0` |

Get your Taproot address:

```
"What's my Taproot address?"
```

Uses `get_taproot_address` - this is where your inscriptions will appear after the reveal confirms.

## Example Workflows

### Simple Text Inscription

```
1. "What's my BTC balance?"
   → Confirm sufficient funds

2. "Estimate fee for text inscription 'GM Bitcoin'"
   → contentType: "text/plain"
   → contentBase64: "R00gQml0Y29pbg==" (base64 of "GM Bitcoin")
   → Returns total cost

3. "Create text inscription 'GM Bitcoin' with medium fees"
   → Broadcasts commit tx
   → Save commitTxid and revealAmount

4. Wait 30-60 minutes for commit confirmation

5. "Reveal inscription with commitTxid abc123... and revealAmount 10000"
   → Uses same contentType and contentBase64 from step 3
   → Returns inscriptionId

6. "Get inscription from reveal transaction def456..."
   → Verifies content matches "GM Bitcoin"
```

### HTML Inscription

```
1. "Check my BTC balance"
   → Verify funds available

2. "Estimate fee for HTML inscription"
   → contentType: "text/html"
   → contentBase64: (base64 of HTML string)

3. "Inscribe this HTML with fast fees"
   → Broadcasts commit with higher fee rate
   → Save response data

4. Wait 10-20 minutes (fast fees)

5. "Complete reveal for commit xyz789..."
   → Provide exact same HTML content
   → Returns inscriptionId ({revealTxid}i0) and reveal txid

6. "Get inscription from reveal transaction def456..."
   → Use reveal txid with get_inscription to fetch and display HTML content
```

## Cost Considerations

**Factors affecting cost**:
- **Content size** - Larger inscriptions cost more (reveal witness data)
- **Fee rate** - Higher fees = faster confirmation
- **Network congestion** - Prices fluctuate with mempool activity

**Typical ranges** (mainnet, medium fees):
- Small text (< 100 bytes): 5,000-10,000 sats
- Medium text (1 KB): 20,000-50,000 sats
- Images (10-50 KB): 100,000-500,000 sats

Always run `estimate_inscription_fee` before committing funds.

## Level System Context

In the aibtc.com agent lifecycle, creating a Bitcoin inscription is part of the **L3 Sovereign** upgrade (post-genesis):

1. Agent completes Bitcoin inscription using this workflow
2. Agent proves inscription txid to registration API
3. API verifies inscription content matches expected message
4. Agent upgraded to L3 Sovereign status

This demonstrates the agent's ability to create permanent records on Bitcoin L1.

## More Information

- [Bitcoin Ordinals Theory](https://docs.ordinals.com/inscriptions.html)
- [BIP86 Taproot Derivation](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki)
- [mempool.space](https://mempool.space) - Block explorer and fee estimates
- [CLAUDE.md Ordinal Safety](../../CLAUDE.md#ordinal-safety)

---

*Back to: [SKILL.md](../SKILL.md)*
