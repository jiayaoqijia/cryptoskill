# Cross-Chain And Conditional Order Prompts

## Cross-Chain Bridge Planning

```text
What currencies can I bridge from Base to Solana?
Get a quote to bridge 0.2 ETH from Ethereum to Solana. Do not execute.
Draft a cross-chain swap from Base USDC to Solana USDC and show the review summary only.
Track this ChangeNow transaction and tell me its latest status.
Bridge funds to Hedera and tell me exactly which destination address format will be used.
```

## Existing Order Discovery

```text
Show all my open conditional orders across every network.
Find my position by ID and summarize its current trigger prices.
Show my pending orders for BONK, JUP, and PEPE across all chains.
I want to change my order, first show me all matching open positions.
```

## Creating New Conditional Orders

```text
Buy JUP if it drops 20% from the current price.
Set a stop-loss on my position 15% below the current market price.
Create a take-profit order 25% above the current price for my Base position.
Place a limit order to buy ETH on Base if price dips 8%.
Create a conditional order on Hedera after checking fresh token prices first.
```

## Updating And Removing Conditions

```text
Add a stop-loss to my existing position.
Replace my current take-profit with a tighter target.
Remove the stop-loss from my open order but leave take-profit unchanged.
Change my pending limit order trigger to a lower entry price.
Update my existing order after showing me the current position details first.
```

## Execute Early Vs Cancel

```text
Execute my pending conditional order early at market.
Cancel my stale BONK order but do not touch the rest.
Show me the order IDs tied to this position before deleting anything.
Explain whether I should execute early or just sell from wallet balance instead.
```
