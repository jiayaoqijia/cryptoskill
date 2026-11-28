# Example — Wallet approval audit (with an unknown EIP-7702 delegation)

> Illustrative walkthrough. Addresses and amounts are fabricated for teaching.
> This is educational security guidance, not financial advice.

## The request (what the user provided)

> "Here's my approval list from revoke.cash for my main Ethereum wallet
> `0xMain…1234`. Can you tell me what's risky and what I should clean up?"

Approval list (revoke.cash-style, illustrative):

| Asset | Type | Spender / operator | Allowance / detail | Spender verified? |
|---|---|---|---|---|
| USDC | ERC-20 `approve` | `0xA11ce…Bad1` ("YieldFarmX") | **Unlimited** (uint256 max) | ❌ unverified |
| BoredApeXYZ | `setApprovalForAll` | `0xDeadMkt…00` ("NiftyBazaar" — defunct 2022) | Approved for **all** | ⚠️ dead project |
| WETH | Permit2 allowance | `0xUniversalRouter…` | `amount` = full balance, `expiration` = +6 months | ✅ Uniswap router |
| — (account) | **EIP-7702 delegation** | `0x7702…UNKNOWN` | EOA delegated to unknown code | ❌ unverified |

---

## Step 1 — Scope & context

- **What:** an **existing wallet's approvals** (case B) — an audit, not a live sign.
- **Chain:** **Ethereum mainnet** (revocation is per-chain; other chains would
  need separate review).
- **Signer:** main wallet; treat as software unless stated otherwise.

## Step 3–4 — Classify and flag each grant

1. **USDC — unlimited `approve` to an unverified spender.** Grants `0xA11ce…Bad1`
   the right to pull **any amount of USDC, forever**. Unverified contract → if
   it's malicious or later exploited, your entire USDC balance is gone. → 🔴.
2. **BoredApeXYZ — `setApprovalForAll` to a defunct marketplace.** `0xDeadMkt…00`
   has operator rights over your **entire BAYC holdings** in that contract. A
   dead project's contracts are prime takeover/exploit targets, and you're not
   using it → standing risk over the whole collection. → 🟠.
3. **WETH — Permit2 allowance to the Uniswap router.** Intended and verified, but
   the `amount` is **full balance** with a **6-month expiry** — larger and longer
   than needed. Bounded, recognized spender. → 🟡 (tighten, not panic).
4. **EIP-7702 delegation to `0x7702…UNKNOWN`.** Your **EOA itself** is delegated
   to **unverified code**. This is not a token allowance — it is control of the
   **whole account**, and a hostile delegate can auto-forward any incoming funds
   in the same block. >90% of observed 7702 delegations are malicious. → 🔴
   **compromise**, not a routine revoke.

## Step 5 — Red flags present

- Unlimited approval to an **unverified** contract. ✅
- `setApprovalForAll` to an **unknown/dead** operator. ✅
- **EIP-7702 delegation to an unknown contract** → assume compromise. ✅

---

## Verdict

# 🚨 WALLET MAY BE COMPROMISED — ACT NOW

The unknown EIP-7702 delegation means the **account itself** may be under
attacker control. Do **not** start by revoking allowances one by one — get the
assets out first.

| # | Item | Type | Blast radius | Severity |
|---|---|---|---|---|
| 1 | EOA delegated to `0x7702…UNKNOWN` | EIP-7702 delegation | **Entire account** (auto-drain on deposit) | 🔴 Critical |
| 2 | USDC unlimited → `0xA11ce…Bad1` | Unlimited `approve`, unverified | All USDC | 🔴 Critical |
| 3 | BAYC `setApprovalForAll` → dead `NiftyBazaar` | NFT operator approval | Whole BAYC collection | 🟠 High |
| 4 | WETH Permit2 → Uniswap router | Permit2, full balance, +6mo | All WETH (intended spender) | 🟡 Medium |

### Recommendation & remediation (in order)
1. **Move assets to a FRESH wallet first.** Generate a new seed **offline**,
   then transfer NFTs and tokens out of `0xMain…1234`. Because the EOA is
   delegated to unknown code, **assume any funds left behind — or sent in — can
   be auto-drained**; don't deposit anything more into the old address.
2. **Stop using the old address.** Treat `0xMain…1234` as burned. Revoking the
   7702 delegation may *not* undo what the hostile delegate already armed.
3. Once funds are safe, on the **old** wallet you may **revoke** the USDC
   unlimited approval (#2) and the BAYC `setApprovalForAll` (#3) via revoke.cash
   on Ethereum — but only as cleanup; the fresh wallet is your real fix.
4. On the **fresh** wallet: enable a **hardware wallet + clear signing
   (ERC-7730)**, set **finite** approvals only, and split into a **vault**
   (cold, never touches new dApps) + **burner** (limited funds) setup.
5. Tighten the Permit2 WETH allowance (#4) to the amount you actually trade with
   a short expiry on the new setup.

> Educational security guidance, not financial advice. If you believe your
> wallet is compromised, act immediately and consult a qualified security
> professional — on-chain transactions are irreversible.
