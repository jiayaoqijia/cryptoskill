# Wallet And Portfolio Prompts

## Addresses And Holdings

```text
What are my wallet addresses across all supported chains?
Show my balances across all chains in a clear table.
Which chains currently hold most of my funds?
List my top token positions by USD value.
Return my wallet addresses as a JSON object keyed by chain.
```

## Cross-Chain Balance Views

```text
Get all balances across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin.
Show my Bitcoin, Solana, and EVM balances side by side.
List every supported chain where I currently have a non-zero balance.
Show me which networks I have enough native gas on to trade right now.
```

## Portfolio Views

```text
Summarize my portfolio performance over the last 7 days.
Show my portfolio grouped by chain and token category.
What percentage of my holdings are in stablecoins right now?
Give me a concise portfolio snapshot with the top 5 positions.
Show my portfolio grouped into majors, stablecoins, meme tokens, and long-tail assets.
```

## Machine-Readable Output

```text
List all balances as JSON.
Show my balances in a CSV-style table with chain, token, amount, and USD value.
Return a compact JSON summary of my top holdings and wallet addresses.
Export my balances as a table I can paste into a spreadsheet.
```

## Network-Specific Wallet Checks

```text
Show me my Solana balances and top SPL positions.
Show me my Ethereum balances and top ERC-20 positions.
Show me my Hedera balances in a clear table.
Show me my Bitcoin wallet balances across taproot, nested segwit, and legacy-compatible assets.
```
