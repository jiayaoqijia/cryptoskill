# Example — Permit2 phishing signature from a fake "airdrop claim"

> Illustrative walkthrough. Addresses, names, and amounts are fabricated for
> teaching. This is educational security guidance, not financial advice.

## The request (what the user pasted)

> "I clicked **Claim** on `app.arbitrum-airdrop-claim[.]xyz` (found it in a
> Discord DM saying I have an unclaimed ARB allocation). My wallet popped up
> asking me to sign this — is it safe?"

Raw request payload (illustrative):

```json
{
  "method": "eth_signTypedData_v4",
  "params": [
    "0xYourWallet…",
    {
      "domain": {
        "name": "Permit2",
        "chainId": 42161,
        "verifyingContract": "0x000000000022D473030F116dDEE9F6B43aC78BA3"
      },
      "primaryType": "PermitSingle",
      "message": {
        "details": {
          "token": "0x912CE59144191C1204E64559FE8253a0e49E6548",
          "amount": "1461501637330902918203684832716283019655932542975",
          "expiration": "1999999999",
          "nonce": "0"
        },
        "spender": "0x9F1cE0…dRaInEr",
        "sigDeadline": "1999999999"
      }
    }
  ]
}
```

---

## Step 1 — Scope & context

- **What:** a **LIVE off-chain signature** request (case A — highest urgency).
- **Chain:** `chainId 42161` = **Arbitrum One**.
- **Signer:** software wallet (no hardware mentioned).
- **Delivery:** a **Discord DM** link to a **lookalike domain**
  (`arbitrum-airdrop-claim.xyz`) — not the official Arbitrum domain.

## Step 2–3 — Classify the request

- `method: eth_signTypedData_v4` with `domain.name = "Permit2"` and
  `primaryType: PermitSingle` → this is a **Permit2 signature** (taxonomy #4),
  *not* a harmless "sign-in".
- `details.amount = 1461501637330902918203684832716283019655932542975` = the
  Permit2 **uint160 max** → **full-balance** approval of token
  `0x912C…6548` (ARB).
- `expiration` and `sigDeadline` ≈ year 2033 → effectively **never expires**.
- `spender = 0x9F1cE0…dRaInEr` → an **unknown, unverified** address, not Uniswap.

**What this grants:** one signature lets `spender` pull the **full ARB balance**
(and, via Permit2, potentially **every token you've ever approved to the Permit2
contract**) for ~8 years — gaslessly, with **no transaction in your history**
until the funds are gone.

## Step 4–5 — Red flags

| Red flag | Present? |
|---|---|
| Permit2 signature on a site you didn't intend (not Uniswap) | ✅ |
| Full-balance amount (uint160 max) | ✅ |
| Far-future expiry / sigDeadline | ✅ |
| Unverified spender address | ✅ |
| "Free airdrop / claim" lure | ✅ |
| Delivered via Discord DM + lookalike domain | ✅ |

Six independent red flags. There is no legitimate reason an *airdrop claim*
needs a full-balance Permit2 signature to an unknown spender.

---

## Verdict

# ⛔ DO NOT SIGN — this is a Permit2 drainer

| # | Item | Type | Blast radius | Severity |
|---|---|---|---|---|
| 1 | Permit2 sig to `0x9F1cE0…dRaInEr` on `arbitrum-airdrop-claim.xyz` | Permit2 `PermitSingle`, full-balance, ~2033 expiry | All ARB + every token approved to Permit2 | 🔴 Critical |

### Recommendation
- **Reject the signature.** Close the site. Do not retry.
- A real airdrop **claim** is a normal transaction that *sends you* tokens — it
  never asks you to *grant* a full-balance Permit2 allowance to a stranger.

### Remediation
1. **Don't sign.** If you haven't signed, you've lost nothing — just reject and
   leave the site.
2. If you **already signed**: go to **revoke.cash** on **Arbitrum**, open your
   **Permit2** allowances, and **revoke** the allowance to that spender
   immediately — and revoke any other Permit2 token allowances too.
3. If meaningful funds are still at risk and you're unsure whether you signed
   anything else, **move assets to a fresh wallet** (new seed, generated
   offline) and treat the exposed address as burned.
4. Going forward: only claim airdrops from the **official domain you typed or
   bookmarked**, ignore Discord-DM "claim" links, and enable **clear signing**
   so Permit2 requests are unmistakable.

> Educational security guidance, not financial advice. On-chain actions are
> irreversible — verify the domain and decoded payload yourself before signing.
