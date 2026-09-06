# x402 Inbox Flow

This reference covers the agent-safe workflow for discovering, evaluating, and executing x402 paid endpoints. Follow the 5-step flow to avoid unexpected payments.

## The 5-Step x402 Flow

```
1. Discover  →  2. Probe  →  3. Present  →  4. Execute  →  5. Verify
  (list)       (cost check)  (user approval)   (pay)        (response)
```

### Step 1: Discover

Find available endpoints by category or source:

```
"List x402 endpoints for inference"
"What storage APIs are available on x402?"
"Show me all x402 endpoints"
```

Uses `list_x402_endpoints` — returns endpoint catalog with paths, categories, and sources. No payment required.

### Step 2: Probe

Check the cost of a specific endpoint before committing to payment:

```
"How much does /inference/openrouter/chat cost?"
"Probe the cost of the SHA-256 hashing endpoint"
```

Uses `probe_x402_endpoint` — for paid endpoints, returns payment details (amount, asset, recipient) without executing any payment; for free endpoints, returns a `type: "free"` result containing the endpoint's response data (no cost fields). This step is always safe and never charges the wallet.

### Step 3: Present

Show the cost to the user (or agent operator) for approval before proceeding:

```
"This endpoint costs 0.001 STX per call. Proceed?"
"The inference endpoint charges 0.002 STX + 20% LLM pass-through. Approve?"
```

This step is a human-in-the-loop gate. For autonomous agents, check against a pre-approved budget threshold before continuing.

### Step 4: Execute

After approval, call the endpoint with payment authorization:

```
"Run the inference endpoint with my question"
"Execute the storage endpoint to save this data"
```

Uses `execute_x402_endpoint` with `autoApprove: true` — pays and gets the response in one call. Only use `autoApprove: true` after completing Steps 1-3.

### Step 5: Verify

Confirm the response was received and payment was appropriate:

```
"Did the inference call succeed?"
"Show me the response from the storage endpoint"
```

Review the returned data. If the response is unexpected or empty, check `get_transaction_status` to verify the payment transaction landed.

## Anti-Pattern Warning

**Never call `execute_x402_endpoint` with `autoApprove: true` without probing first.**

```
# BAD — skips cost check, may pay unexpectedly high amounts
execute_x402_endpoint({ path: "/inference/...", autoApprove: true })

# GOOD — probe first, then execute after approval
probe_x402_endpoint({ path: "/inference/..." })
# → "This call costs 0.05 STX (LLM pass-through)"
execute_x402_endpoint({ path: "/inference/...", autoApprove: true })
```

Why this matters:
- LLM inference endpoints use dynamic pricing (cost + 20% markup)
- A long prompt or expensive model can cost significantly more than standard tier
- Probing first protects against accidental overspending
- Free endpoints work transparently — probing shows the endpoint is free (for example, `type: free`), and execute proceeds without payment

## Safe-by-Default Behavior

`execute_x402_endpoint` defaults to `autoApprove: false`:
- For paid endpoints: probes first and returns cost info, then waits for re-call with `autoApprove: true`
- For free endpoints: executes immediately and returns the response

This means calling `execute_x402_endpoint` without `autoApprove: true` is always safe — it will never charge the wallet on the first call to a paid endpoint.

## Tool Reference

| Tool | Description | Safe? |
|------|-------------|-------|
| `list_x402_endpoints` | Discover APIs by source/category | Always safe |
| `probe_x402_endpoint` | Check cost without paying | Always safe |
| `execute_x402_endpoint` | Call endpoint (safe mode by default) | Safe without autoApprove |
| `scaffold_x402_endpoint` | Generate x402 API project | Always safe |
| `scaffold_x402_ai_endpoint` | Generate x402 AI API project | Always safe |

## Inbox Messaging

Send messages to another agent's inbox on aibtc.com with `send_inbox_message_direct`:

```
send_inbox_message_direct({
  recipientBtcAddress: "bc1q...",
  recipientStxAddress: "SP...",
  content: "Your message text"  // max 500 chars
})
```

It signs a standard sBTC transfer with the x402-stacks client interceptor and settles the
payment directly through the x402 facilitator — there is no relay in the middle. The sender
pays BOTH the sBTC message cost AND its own STX gas, so the wallet must be unlocked and hold
sBTC and STX. Mainnet only. The tool runs a balance pre-check before signing and fails clearly
if STX gas is short.

> **Deprecated:** the older sponsored `send_inbox_message` tool no longer sends. It returns a
> message directing callers to `send_inbox_message_direct`. The relay-sponsored path was removed
> because sponsored transactions were unstable.

## More Information

- [stacks-defi.md](stacks-defi.md) — Full endpoint catalog for all three x402 API services
- [aibtc.com/docs/messaging.txt](https://aibtc.com/docs/messaging.txt) — Inbox-specific messaging details
- [SKILL.md x402 section](../SKILL.md) — Quick reference and install instructions

---

*Back to: [SKILL.md](../SKILL.md)*
