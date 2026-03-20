# Example: Check Contract Safety

## User Prompt

```
Is the contract TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE safe to interact with?
```

## Expected Workflow

1. **Contract Info** → `getContractInfo("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → Deployer, energy settings
2. **Contract ABI** → `getContract("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → ABI for method analysis
3. **Token Info** → `getTrc20Info("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → Check if it's a token
4. **Transactions** → `getContractTransactions("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", limit=100)` → Activity
5. **Holders** → `getTrc20TokenHolders("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", limit=20)` → Concentration
6. **Deployer Account** → `getAccount(deployerAddress)` → Deployer profile

## Expected Output (Sample)

```
## Contract Safety Check: TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE

### Safety Score: Caution ⚠️

### Contract Overview
- Name: UnknownToken
- Deployer: TJZuV6A9QRdtVeJBvewCF9fLF2qnRSEv3y
- Deployed: 2026-02-28 (12 days ago)
- Open Source: No (ABI not available)

### Risk Factors
1. **Closed Source**: No ABI available — cannot verify contract behavior
2. **Very New**: Deployed only 12 days ago, limited track record
3. **High Concentration**: Top holder owns 85% of total supply
4. **Low Holder Count**: Only 45 unique holders
5. **User Pays All Energy**: consume_user_resource_percent = 100%
6. **Single Caller Dominance**: 70% of transactions from one address

### Positive Factors
- No self-destruct detected in bytecode
- Basic TRC-20 events observed (Transfer, Approval)

### Recommendation
Exercise extreme caution. This contract shows multiple red flags typical of
high-risk tokens: closed source, high concentration, new deployment, and low
holder diversity. Consider waiting for the contract to be verified and gain
more history before interacting.
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getContractInfo` | 1 | Contract settings |
| `getContract` | 1 | ABI availability check |
| `getTrc20Info` | 1 | Token identification |
| `getContractTransactions` | 1 | Activity patterns |
| `getTrc20TokenHolders` | 1 | Concentration analysis |
| `getAccount` | 1 | Deployer profile |
