---
name: error-handling
description: This skill should be used when any OpenOcean API call returns an error code, when token resolution fails, when transaction execution fails, or when any unexpected issue occurs during swap operations. Provides troubleshooting guidance and recovery steps.
metadata:
  tags:
    - defi
    - openocean
    - error
    - troubleshooting
    - recovery
  provider: OpenOcean
  homepage: https://openocean.finance
---

# OpenOcean Error Handling Skill

Handle errors and exceptions that occur during OpenOcean swap operations. This skill provides troubleshooting guidance, recovery steps, and fallback strategies.

## When to Use This Skill

Use this skill when:
1. Any OpenOcean API call returns a `code` other than `200`
2. Token resolution fails (symbol not found)
3. Transaction execution fails (`cast send` errors)
4. Network connectivity issues
5. Unexpected response formats
6. Rate limiting or quota exceeded

## Error Categories

### Category 1: API Errors (HTTP/JSON)

| Code | Meaning | Common Causes | Recovery Steps |
|---|---|---|---|
| 200 | Success | None | Continue normally |
| 400 | Bad Request | Invalid parameters, wrong format | 1. Check parameter formats<br>2. Verify token addresses<br>3. Ensure amount is in wei |
| 401 | Unauthorized | Missing/invalid API key | 1. Check API key configuration<br>2. Contact OpenOcean support |
| 403 | Forbidden | Access denied | 1. Check permissions<br>2. Verify chain support |
| 404 | Not Found | Endpoint or resource not found | 1. Check URL path<br>2. Verify chain slug |
| 429 | Rate Limited | Too many requests | 1. Wait 10-30 seconds<br>2. Implement exponential backoff<br>3. Consider enterprise plan |
| 500 | Internal Server Error | OpenOcean server issue | 1. Retry after 30 seconds<br>2. Check OpenOcean status page<br>3. Try alternative chain |
| 502/503/504 | Gateway/Service Unavailable | Network or service issues | 1. Wait and retry<br>2. Check network connectivity<br>3. Try different RPC endpoint |

### Category 2: Business Logic Errors

| Error Pattern | Meaning | Recovery Steps |
|---|---|---|
| `"code": 200, "data": null` | No route found | 1. Check token pair liquidity<br>2. Try different amount<br>3. Use different chain |
| `"code": 200, "data": {..., "outAmount": "0"}` | Zero output amount | 1. Check token decimals<br>2. Verify amount is sufficient<br>3. Try larger amount |
| Invalid token address | Token not recognized | 1. Verify contract address<br>2. Check chain compatibility<br>3. Use token list API |

### Category 3: Token Resolution Errors

| Error | Cause | Recovery |
|---|---|---|
| Symbol not found in registry | Token not in reference list | 1. Use OpenOcean token API<br>2. Ask user for address<br>3. Check alternative symbols |
| Multiple matches found | Ambiguous symbol | 1. Show options to user<br>2. Use market cap ranking<br>3. Ask user to specify address |
| Invalid chain for token | Token not deployed on chain | 1. Check token deployment<br>2. Suggest alternative chain<br>3. Use bridge if available |

### Category 4: Transaction Execution Errors

| Error Message | Meaning | Recovery Steps |
|---|---|---|
| `insufficient funds for gas * price + value` | Not enough native token | 1. Add funds to wallet<br>2. Reduce swap amount<br>3. Use lower gas price |
| `execution reverted: OpenOcean: insufficient output amount` | Price moved beyond slippage | 1. Increase slippage tolerance<br>2. Wait for better price<br>3. Try smaller amount |
| `execution reverted: ERC20: transfer amount exceeds allowance` | Token not approved | 1. Approve token first<br>2. Check approval amount<br>3. Reset approval if needed |
| `nonce too low` / `nonce too high` | Nonce mismatch | 1. Let wallet manage nonces<br>2. Check pending transactions<br>3. Use higher nonce |
| `transaction underpriced` | Gas price too low | 1. Increase gas price<br>2. Use current market rate<br>3. Wait for less congestion |
| `replacement transaction underpriced` | Competing transaction | 1. Use significantly higher gas<br>2. Cancel pending transaction<br>3. Wait for confirmation |

## Recovery Workflows

### Workflow 1: API Error Recovery

```
1. Check error code and message
2. If 429 (rate limited):
   - Wait 10 seconds
   - Retry once
   - If still failing, suggest waiting longer
3. If 400 (bad request):
   - Validate all parameters
   - Check token addresses
   - Verify amount format
4. If 500 (server error):
   - Wait 30 seconds
   - Retry once
   - Suggest trying later
5. If persistent:
   - Suggest alternative DEX
   - Try different chain
   - Contact OpenOcean support
```

### Workflow 2: Token Resolution Recovery

```
1. Symbol not found:
   - Query OpenOcean token API
   - If found, use it
   - If not found, ask user for address
2. Multiple matches:
   - Show top 3 by market cap
   - Ask user to choose
   - Suggest verifying on explorer
3. Invalid address:
   - Verify on block explorer
   - Check chain compatibility
   - Suggest correct address
```

### Workflow 3: Transaction Execution Recovery

```
1. Insufficient funds:
   - Calculate required amount
   - Suggest adding funds
   - Offer to reduce swap size
2. Insufficient allowance:
   - Provide approval transaction
   - Suggest approval amount
   - Explain approval process
3. Slippage exceeded:
   - Show current price vs quote
   - Suggest higher slippage
   - Offer to requote
4. Gas issues:
   - Check current gas prices
   - Suggest appropriate gas
   - Offer to wait for better conditions
```

## User Communication

### Good Error Messages

**Bad:** "Error: 400"
**Good:** "The API returned error 400 (Bad Request). This usually means one of the parameters is invalid. Let me check: are you sure the token addresses are correct for this chain?"

**Bad:** "Transaction failed"
**Good:** "The transaction failed with error: 'insufficient funds for gas * price + value'. You need at least 0.01 ETH for gas plus the swap value, but the current balance is only 0.005 ETH."

### Actionable Suggestions

Always provide:
1. **What happened** — Clear error description
2. **Why it happened** — Probable cause
3. **How to fix** — Specific steps
4. **Alternative options** — Workarounds

## Fallback Strategies

### Primary Fallback: Parameter Adjustment
- Reduce amount
- Increase slippage
- Use different gas price
- Try different chain

### Secondary Fallback: Alternative Service
If OpenOcean consistently fails:
1. Suggest other aggregators (1inch, Paraswap)
2. Direct DEX access (Uniswap, PancakeSwap)
3. Manual swap via wallet interface

### Tertiary Fallback: Manual Intervention
When automation fails:
1. Provide manual steps
2. Suggest waiting and retrying later
3. Recommend contacting support

## Monitoring and Logging

### What to Log
1. **API calls** — URL, parameters, response code
2. **Token resolutions** — Symbol, address, chain
3. **Transaction attempts** — Hash, status, gas used
4. **Errors** — Full error object, timestamp

### Alert Thresholds
- **Warning**: 3 consecutive API errors
- **Critical**: 10+ errors in 5 minutes
- **Stop**: Balance below minimum for gas

## Testing Error Scenarios

Test these scenarios regularly:
1. **Invalid token** — Non-existent symbol
2. **Insufficient balance** — Ask for more than available
3. **High slippage** — Extreme price movement
4. **Network outage** — RPC endpoint down
5. **Rate limiting** — Rapid consecutive calls

## Prevention Tips

### Before Swap
1. **Validate all inputs** — tokens, amounts, addresses
2. **Check balances** — token + gas
3. **Verify approvals** — ERC-20 allowances
4. **Monitor gas** — current market rates

### During Swap
1. **Set reasonable timeouts** — 30 seconds for API, 2 minutes for tx
2. **Implement retry logic** — with exponential backoff
3. **Monitor progress** — confirm each step

### After Swap
1. **Verify outcome** — check balances, tx status
2. **Log results** — for analysis and debugging
3. **Update state** — mark as complete/failed

## Support Resources

### OpenOcean Resources
- **API Documentation**: https://apis.openocean.finance/
- **Status Page**: Check for service outages
- **Support**: Telegram/Discord channels
- **GitHub**: Issue tracker for bugs

### Community Resources
- **Block Explorers**: Etherscan, BscScan, etc.
- **Gas Trackers**: ETH Gas Station, GasNow
- **Token Verifiers**: TokenSniffer, RugDoc

### Emergency Contacts
For critical issues involving fund loss:
1. **Immediate**: Stop all automated trading
2. **Investigation**: Check transaction on explorer
3. **Support**: Contact OpenOcean with tx hash
4. **Community**: Seek help in relevant channels

**Remember**: Most errors are recoverable with proper handling. Stay calm, follow the recovery workflows, and prioritize user fund safety above all else.