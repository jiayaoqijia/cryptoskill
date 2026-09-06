# Troubleshooting

Common issues and solutions when using the Bitcoin wallet tools.

## Wallet Issues

### "Wallet not unlocked"

**Symptom**: Transaction fails with unlock error.

**Solution**: Run `wallet_unlock` with your password before sending transactions.

```
"Unlock my wallet"
```

After completing transactions, lock for security:

```
"Lock my wallet"
```

### "No wallet configured"

**Symptom**: Tools fail without wallet.

**Solution**: Create or import a wallet first:

```
"Create a new wallet"
"Import wallet from mnemonic"
```

### "Wrong password"

**Symptom**: Unlock fails.

**Solution**: Use `wallet_list` to find and confirm the correct wallet `id` (not just the name). If needed, run `wallet_switch <walletId>`, then retry `wallet_unlock` with that wallet ID and the correct password.

## Balance Issues

### "Insufficient balance"

**Symptom**: Transfer fails due to low balance.

**Solution**: Check balance includes fees:

```
"What's my BTC balance?"
"What are current fees?"
```

For Bitcoin, you need: amount + (fee_rate * ~200 vBytes).

### "Unconfirmed balance"

**Symptom**: Balance shows but can't spend.

**Solution**: Wait for confirmations. `get_btc_balance` shows confirmed vs unconfirmed. Most transfers need 1+ confirmations.

## Transaction Issues

### "Transaction pending"

**Symptom**: Transaction broadcast but not confirmed.

**Solution**: Use the `explorerUrl` returned by `transfer_btc` to check status on mempool.space. Bitcoin transactions can take 10 min to 1+ hour depending on fee rate. Use "fast" fees for quicker confirmation.

### "Transaction failed"

**Symptom**: Broadcast error.

**Possible causes**:
- Insufficient balance
- Invalid address
- Network issues

**Solution**: Check error message, verify address format, retry.

### "Invalid address"

**Symptom**: Address rejected.

**Solution**: Verify address matches network:

| Network | BTC Address | STX Address |
|---------|-------------|-------------|
| Mainnet | `bc1...` | `SP...` |
| Testnet | `tb1...` | `ST...` |

## Network Issues

### "Network timeout"

**Symptom**: API calls fail.

**Solution**:
1. Check internet connection
2. Retry after a moment
3. Check mempool.space (BTC) or Hiro API (Stacks) status

### "Rate limited"

**Symptom**: Too many requests error.

**Solution**: Wait a few seconds between calls. Avoid rapid polling.

## Pillar Issues

### Browser Handoff Mode

#### "Browser didn't open"

**Symptom**: Pillar operation stuck.

**Solution**: Manually open https://pillarbtc.com and check if logged in.

#### "Operation timed out"

**Symptom**: Pillar action never completes.

**Solution**:
1. Check browser for pending approval
2. Ensure you're logged into Pillar
3. Cancel and retry

### Agent Direct Mode

#### "No signing key found"

**Symptom**: `pillar_direct_*` tools fail.

**Solution**: Create a signing key and wallet first:

```
"Create a Pillar wallet for my agent"
```

Uses `pillar_direct_create_wallet` - generates key, deploys wallet, registers pubkey.

#### "Signing key locked"

**Symptom**: Operations fail with lock error.

**Solution**: Keys auto-unlock if `PILLAR_API_KEY` is set. If not:

```
"Unlock my Pillar signing key"
```

#### "Wallet pending"

**Symptom**: Operations fail, wallet not ready.

**Solution**: Wait 20-30 seconds after `pillar_direct_create_wallet` for on-chain deployment to complete.

## Stacks/DeFi Issues

### "Mainnet only"

**Symptom**: ALEX or Zest tools fail on testnet.

**Solution**: ALEX DEX and Zest Protocol are mainnet-only. Switch network or use testnet alternatives.

### "Contract call failed"

**Symptom**: Smart contract error.

**Solution**: Check error message for:
- Insufficient tokens
- Invalid arguments
- Contract paused

### "Slippage too high"

**Symptom**: Swap rejected.

**Solution**:
1. Get fresh quote
2. Increase slippage tolerance
3. Try smaller amount

## Getting Help

### Debug Information

Gather this info before reporting:

```
"Check wallet status"
"Get network status"
```

### Report Issues

- [GitHub Issues](https://github.com/aibtcdev/aibtc-mcp-server/issues)
- Include: error message, command attempted, network (mainnet/testnet)

### Environment Check

Verify configuration:

```
"Get wallet info"
```

Shows: wallet address, network, API URL.

---

*Back to: [SKILL.md](../SKILL.md)*
