# Transfers And Safety Prompts

## Review-Only Transfers

```text
Prepare a transfer of 0.1 ETH to 0x1234... for review only.
Draft a USDC transfer from Base to Ethereum but do not execute.
Show the exact transaction summary before any wallet action.
Prepare a Solana token transfer and stop before signing.
Draft a 100 USDC transfer on Hedera but do not execute.
```

## Risk Framing

```text
Explain the risks before sending USDC from Base to Ethereum.
Tell me what could go wrong with this transfer and how to verify the destination.
Review this planned transfer and list the approval checkpoints.
Explain what gas tokens I need before attempting this move.
Check whether I have enough native gas to complete this transfer safely.
```

## Safety Constraints

```text
Do not execute anything. Only prepare the transfer details for approval.
Stop before signing or submitting and ask me to confirm the final transaction summary.
Use review-only mode and flag any missing chain or token details.
Leave enough native gas in the wallet and do not send the full balance.
If the destination address looks wrong for the selected chain, stop and explain why.
```

## Full-Balance And Contact-Aware Transfers

```text
Prepare a near-full ETH transfer but leave room for fees.
Send funds to Alice on Base using my saved contact, but only show the draft transaction first.
Before sending, show me the resolved contact address, chain, token, amount, and fees.
```
