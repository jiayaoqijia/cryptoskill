---
name: configure-x402
description: Configure x402 micropayments for agent-to-agent commerce via Uniswap. Set up your agent to pay per MCP request in USDC on Base (~200ms settlement) or accept x402 payments as a service provider. Use when the user wants to enable pay-per-use API access or monetize their agent's services.
model: sonnet
---

# Configure x402

## Overview

Configures the x402 HTTP-native payment protocol for agent-to-agent micropayments settled on Base. x402 uses the HTTP 402 "Payment Required" status code to enable pay-per-request billing — agents pay fractions of a cent per API call in USDC, with ~200ms settlement, no API keys, no accounts, and no subscriptions.

This skill supports two modes:
- **Pay mode**: Configure your agent to pay for MCP tool calls and external API access via x402
- **Accept mode**: Configure your agent as an x402 service provider that accepts micropayments for its services
- **Both**: Enable bidirectional x402 payments

x402 has processed 100M+ agent-to-agent transactions across 80+ ecosystem projects (Feb 2026). It eliminates API key onboarding friction and creates revenue streams from every agent interaction.

## When to Use

Activate when the user says:

- "Set up x402 payments for my agent"
- "Enable pay-per-swap via x402"
- "Configure my agent to accept x402 payments"
- "Set up micropayments on Base"
- "Enable x402 for my MCP server"
- "Monetize my agent's API"
- "Configure pay-per-request billing"
- "Set up agent-to-agent payments"

## Parameters

| Parameter         | Required | Default     | Description                                                                                           |
|-------------------|----------|-------------|-------------------------------------------------------------------------------------------------------|
| `mode`            | No       | both        | Payment mode: "pay" (pay for services), "accept" (accept payments), or "both"                         |
| `walletAddress`   | Yes      | --          | USDC wallet address on Base for sending/receiving payments                                            |
| `chain`           | No       | base        | Settlement chain (Base recommended for ~200ms settlement)                                             |
| `pricePerCall`    | No       | see pricing | Price per MCP tool call in USDC (for accept mode). Defaults to recommended pricing below.             |
| `supportedTools`  | No       | all         | Which MCP tools to gate behind x402 payments (for accept mode). "all" or comma-separated list.        |
| `maxSpendPerHour` | No       | $1.00       | Maximum x402 spend per hour (for pay mode). Safety limit to prevent runaway costs.                    |
| `facilitator`     | No       | auto        | x402 facilitator to use. "auto" selects the best available facilitator on Base.                       |

### Recommended Pricing (Accept Mode)

| Tool Category      | Price per Call | Examples                                       |
|--------------------|----------------|-------------------------------------------------|
| Price quotes       | $0.001         | `get_token_price`, `get_quote`                  |
| Pool analytics     | $0.003         | `get_pool_info`, `get_pool_volume_history`       |
| Route optimization | $0.005         | `get_pools_by_token_pair`, `search_tokens`       |
| Simulation         | $0.01          | `simulate_transaction`                           |
| Execution          | $0.05          | `execute_swap`, `add_liquidity`                  |

## Workflow

1. **Parse configuration** from the user's request. Determine the payment mode, wallet address, chain, pricing, and tool scope. Validate the wallet address format.

2. **Validate wallet**: Verify the wallet address exists on the target chain and has a USDC balance (for pay mode) or can receive USDC (for accept mode). Check that the chain supports x402 settlement.

3. **Write x402 configuration**: Generate the x402 configuration file at `.uniswap/x402-config.json` with:
   - Payment mode (pay/accept/both)
   - Wallet address and chain
   - Facilitator endpoint
   - Per-tool pricing (accept mode)
   - Spending limits (pay mode)
   - Supported tools list

   For accept mode, also generate the `.well-known/x402-manifest.json` that advertises the agent's x402-enabled endpoints to other agents.

4. **Verify setup**: Confirm the configuration is valid by checking:
   - Wallet connectivity on the settlement chain
   - Facilitator availability
   - USDC token approval for the facilitator contract (if pay mode)
   - Configuration file is properly formatted

## Output Format

```text
x402 Configuration Complete

  Mode:         Both (pay + accept)
  Chain:        Base (8453)
  Wallet:       0x1234...abcd
  Facilitator:  Auto-selected (Coinbase x402)

  Pay Mode:
    Max Spend:  $1.00/hour
    USDC Balance: $50.00 (sufficient)

  Accept Mode:
    Pricing:
      Price quotes:       $0.001/call
      Pool analytics:     $0.003/call
      Route optimization: $0.005/call
      Simulation:         $0.010/call
      Execution:          $0.050/call
    Tools Gated:  All (17 tools)

  Config Files:
    .uniswap/x402-config.json
    .well-known/x402-manifest.json

  Status: Ready for x402 payments
```

## Important Notes

- x402 settles on Base by default (~200ms). Ethereum mainnet settlement is possible but slower and more expensive.
- USDC is the only supported payment token for x402. The wallet must hold USDC on the settlement chain.
- The `maxSpendPerHour` safety limit prevents runaway costs in pay mode. Adjust based on expected usage.
- x402 uses the HTTP 402 "Payment Required" status code. When a client hits an x402-gated endpoint without payment, it receives a 402 response with payment instructions.
- Facilitators handle the payment settlement. The "auto" option selects the best available facilitator on the target chain.
- For accept mode, the `.well-known/x402-manifest.json` file makes your agent discoverable on Coinbase Bazaar (12,365+ services).
- x402 payments are per-request. There are no subscriptions, API keys, or accounts. Each request includes a micropayment.
- All x402 transactions are logged for treasury management and can be tracked via the `manage-treasury` skill.
- This skill does not execute any on-chain transactions. It only generates configuration files. The actual x402 payment flow happens at runtime when the MCP server processes requests.

## Error Handling

| Error                  | User-Facing Message                                                        | Suggested Action                              |
|------------------------|----------------------------------------------------------------------------|-----------------------------------------------|
| Invalid wallet         | "Invalid wallet address format."                                           | Provide a valid Ethereum address (0x...)       |
| No USDC balance        | "Wallet has no USDC on [chain]. x402 payments require USDC."               | Fund the wallet with USDC on Base              |
| Chain not supported    | "[chain] does not support x402 settlement."                                | Use Base (recommended) or Ethereum             |
| Facilitator unavailable| "No x402 facilitator available on [chain]."                                | Try Base (most facilitators available)         |
| Config write failed    | "Could not write x402 configuration: [reason]."                           | Check file permissions                         |
| Wallet not configured  | "No agent wallet found. Set up a wallet first."                            | Use `setup-agent-wallet` skill first           |
| Invalid pricing        | "Price per call must be positive and in USDC."                             | Provide valid pricing values                   |
