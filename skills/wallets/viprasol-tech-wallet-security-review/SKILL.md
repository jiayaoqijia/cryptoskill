---
name: wallet-security-review
description: Review a crypto wallet signature request, token approval, or wallet's exposure for drainer & phishing risk — unlimited approvals, Permit/Permit2, setApprovalForAll, eth_sign blind signing, and EIP-7702 delegations. Outputs a sign/don't-sign verdict and remediation. Use before signing anything, or to audit a wallet's approvals.
version: 1.0.0
---

# Wallet Security Review

A disciplined, repeatable methodology for reviewing what a crypto wallet is
about to **sign** — or what it has **already approved** — before a drainer or
phishing site empties it. Approval-based attacks drained **over $200M in
2024–2025**, and the new EIP-7702 delegation vector (live since the 2025 Pectra
upgrade) is overwhelmingly malicious: **>90% of observed on-chain 7702
delegations are linked to malicious contracts**, with single phishing signs
costing victims seven figures.

The core skill is reading a signature/approval request precisely, naming the
**blast radius** of what it grants, and returning a blunt **sign / don't-sign**
verdict plus remediation.

---

## When to Activate

Activate when the user:

- Pastes a **signature or transaction request** (or its raw JSON / typed-data
  payload) and asks *"is this safe to sign?"*
- Shares a **wallet address's approvals** (e.g. a revoke.cash or Etherscan
  Token Approval Checker export) and wants them reviewed.
- Suspects they hit a **drainer or phishing site**, clicked a "claim/airdrop"
  popup, or already signed something and wants to know their exposure.
- Wants a **wallet hygiene / approval audit** ("clean up my approvals", "how
  exposed am I?").
- Mentions any of: *unlimited approval, Permit, Permit2, setApprovalForAll,
  eth_sign, blind signing, 7702 / delegation, drainer, address poisoning,
  revoke.cash*.

> **You cannot fetch on-chain state.** This skill reasons over what the user
> gives you. If you need the approval list or the request payload, **ask for
> it** (Step 1) — never invent allowances, spenders, or balances.

---

## Step 1: Scope & Context

Establish exactly what you are reviewing before saying anything about safety.

1. **What are we reviewing?**
   - **(A) A LIVE request** — a signature or transaction the user is about to
     approve in their wallet right now. *Highest urgency: a wrong answer here
     can cost them everything in one click.*
   - **(B) An existing wallet's approvals** — an audit of standing grants
     (allowances, operator approvals, delegations) the wallet already made.
   - **(C) A suspicious site / dApp / message** — triage before they interact
     ("is this airdrop real?", "is this the real Uniswap?").
2. **Which chain(s)?** Ethereum mainnet, an L2 (Arbitrum, Base, Optimism,
   Polygon), BNB Chain, etc. Approvals and revocation are **per-chain** — an
   approval on Base is separate from the same token on mainnet.
3. **What wallet / signer?** Software (MetaMask, Rabby, Phantom) vs **hardware**
   (Ledger, Trezor, Keystone). Hardware materially lowers key-theft risk **but
   does not stop you from signing a malicious approval** — you can hardware-sign
   a wallet-draining permit just fine. Note whether **clear signing** is on.
4. **Get the artifact.** Ask for whichever applies:
   - the **raw request payload** (the JSON your wallet shows: `method`, `params`,
     typed-data `domain`/`message`, or the `to`/`data` calldata), and/or
   - the **approval list** (from **revoke.cash** or the **Etherscan Token
     Approval Checker**), including spender addresses and allowance amounts,
     and/or
   - the **site URL** and how they arrived at it (Discord DM? X link? Google ad?).

Do not proceed to a verdict until you know **what** is being signed/audited and
**on which chain**.

---

## Step 2: Severity Model

Rate every finding by **blast radius × likelihood of loss**.

| Severity | Meaning |
|---|---|
| 🔴 **Critical** | Can drain everything **now**, or the wallet is likely already compromised. Includes any `eth_sign`/blind-sign of an unknown payload, a Permit2 full-balance sig to a hostile spender, or an **unknown EIP-7702 delegation**. Act immediately. |
| 🟠 **High** | Large, standing exposure: an **unlimited** ERC-20 allowance or a `setApprovalForAll` to an unverified/unknown spender. Not auto-draining, but one rug away from total loss of that asset. |
| 🟡 **Medium** | Real but bounded: a finite allowance larger than needed, a stale approval to a known-but-dormant contract, a Permit2 allowance with sane limits. |
| 🟢 **Low** | Tight, intentional, scoped grants to verified contracts; finite allowance ≈ the amount being spent. |
| ℹ️ **Info** | Context/hygiene notes (dApp disconnected ≠ revoked; bookmark the real domain; enable clear signing). |

**Blast radius** = *how much can be taken if this is malicious* (one token? the
whole NFT collection? every token ever approved to Permit2? the entire EOA?).
**Likelihood** = *how plausibly hostile* (unverified spender, phishing delivery,
no simulation, urgency).

---

## Step 3: Signature & Approval Taxonomy (the core)

For each request type: **what it does · blast radius · how to recognize it ·
safe vs dangerous.** This is the heart of the review — name the exact type
before judging it.

### 1. ERC-20 `approve(spender, amount)`
- **Does:** grants `spender` the right to pull up to `amount` of one token from
  your wallet, repeatedly, until changed or revoked.
- **Blast radius:** that one token, up to `amount`. **Unlimited** if `amount` is
  `uint256` max (`2^256 − 1` = `115792089237316195423570985008687907853269984665640564039457584007913129639935`, often shown as a huge number or `∞`/"Unlimited").
- **Recognize:** an on-chain tx, `data` begins `0x095ea7b3`; wallet shows
  "Approve TOKEN — spending cap".
- **Safe:** a **finite** cap ≈ the amount you're about to trade, to a **verified,
  intended** contract. **Dangerous:** **unlimited** cap, or any cap to an
  unverified/random spender. *Disconnecting the dApp does NOT revoke an approval.*

### 2. `increaseAllowance(spender, addedValue)`
- Same risk class as `approve` — it **raises** an existing allowance. Treat an
  `increaseAllowance` to unlimited or to an unknown spender exactly like a
  dangerous `approve`.

### 3. Permit — EIP-2612 (`permit`)
- **Does:** an **off-chain, gasless signature** that authorizes a spender's
  allowance without an on-chain approve tx.
- **Blast radius:** up to the permitted `value` of that token — potentially the
  full balance.
- **Recognize:** a `signTypedData_v4` request whose typed-data `message` has
  fields like `owner`, `spender`, `value`, `nonce`, `deadline`; **no gas, no
  transaction**, so it **leaves no trace in your tx history** — invisible until
  the attacker pulls funds.
- **Safe:** a permit to a contract you intend to use, with a sane `value`/
  `deadline`. **Dangerous:** any permit whose `spender` you don't recognize, or
  a far-future `deadline`. Because it's invisible and gasless, drainers love it.

### 4. Permit2 (Uniswap's universal approval contract)
- **Does:** a single signature authorizes the **Permit2** contract's transfer of
  your tokens to a spender. One signature is the entire authorization.
- **Blast radius:** **enormous.** A single phishing Permit2 signature can let the
  spender drain allowances across **every token you have ever approved to the
  Permit2 contract** — and drainer payloads default to **full balance + a long
  expiry**. This is one of the highest-blast-radius signatures in the ecosystem.
- **Recognize:** `signTypedData_v4` with the **Permit2** domain (`name:
  "Permit2"`) and a `PermitSingle`/`PermitBatch`/`PermitTransferFrom` message
  containing `details` (token, `amount`, `expiration`), a `spender`, and a
  `sigDeadline`.
- **Safe:** a Permit2 sig **on Uniswap itself (or another protocol you
  deliberately chose)**, with a bounded `amount` and short `expiration`.
  **Dangerous:** a Permit2 sig on **any site that isn't the one you intended**,
  an `amount` near full balance, or a long/odd `expiration` → ⛔.

### 5. `setApprovalForAll(operator, true)` — ERC-721 / ERC-1155
- **Does:** grants `operator` blanket control of your **entire NFT collection**
  from that contract.
- **Blast radius:** **every NFT** in that collection — all of them, transferable
  at will, until revoked.
- **Recognize:** tx with `data` `0xa22cb465`; wallet shows "Approve all" /
  "Set approval for all"; `approved = true`.
- **Safe:** to a major, verified marketplace you're actively listing on.
  **Dangerous:** requested by a **"mint" / "claim" / "airdrop"** flow (a mint
  never needs operator rights over your existing NFTs), or to an unknown
  operator → 🟠/🔴.

### 6. `eth_sign` — raw-hash blind signature
- **Does:** signs an **arbitrary 32-byte hash** with no human-readable context.
  An attacker can craft that hash to authorize **any** transaction or message.
- **Blast radius:** **unbounded** — effectively a blank check.
- **Recognize:** `method: "eth_sign"`; wallets warn with red banners like
  *"Signing this message can be dangerous"* / *"this could let someone control
  your account."*
- **Verdict: NEVER sign `eth_sign`.** No legitimate modern dApp requires it. Its
  presence is itself a 🔴 red flag. (This differs from the safe, structured
  `personal_sign`/`signTypedData` — but see below.)

### 7. `personal_sign` / `signTypedData` — disguised intents
- **Does:** normally benign (login / "Sign-In with Ethereum" / message
  acknowledgement). **But** attackers stuff a **disguised permit, order, or
  approval** into the payload.
- **Blast radius:** whatever the payload actually authorizes — for a hidden
  Permit/Permit2/order, that's your tokens.
- **Recognize:** read the **decoded message**. A real login is human-readable
  ("Sign in to … nonce …"). Treat as dangerous any typed-data with
  `Permit`/`PermitSingle`/order structs, a `spender`/`seller`, `value`/`amount`,
  or unreadable hex.
- **Safe:** a clearly human-readable login/nonce with no spend authorization.
  **Dangerous:** any spend/transfer/approval semantics hiding inside a "sign-in".

### 8. EIP-7702 authorization / delegation (set EOA code)
- **Does:** authorizes your **EOA** (your normal wallet address) to **delegate
  its code to a contract** — the account now executes that contract's logic.
- **Blast radius:** **the entire account.** A malicious delegate can include a
  fallback that **auto-forwards any incoming balance in the same block**, so the
  wallet drains itself on every deposit. This is not a single token — it's the
  whole address.
- **Recognize:** an **authorization / "set code" / "delegate" / upgrade-account**
  request (EIP-7702 `authorizationList` with `chainId`, an `address` to delegate
  to, and a `nonce`); wallet language about "smart account" / "delegate" /
  "upgrade".
- **Critical rule:** an **unknown or unverified delegation target = treat the
  wallet as FULLY COMPROMISED**, not "just revoke it." Over **90% of observed
  7702 delegations are malicious.** Redelegating to a safe address may not undo
  what a hostile delegate already armed — **move assets to a fresh wallet** (see
  Step 6). Legitimate 7702 (e.g. a known wallet's batching/gas-sponsorship
  upgrade) delegates to a **verified, audited** implementation you chose.

---

## Step 4: Wallet Approval Audit

When given an approval list (revoke.cash / Etherscan export), enumerate **every
active grant** and flag each of these:

- **Unlimited allowances** — any ERC-20 allowance at `uint256` max → 🟠 (🔴 if
  the spender is unverified). Recommend reducing to needed amount or revoking.
- **Unknown / unverified spender** — spender contract is unverified on the block
  explorer, has no recognizable name, or you can't tie it to a dApp you use → 🔴.
- **Stale approvals** — grants to contracts you no longer use (old DEX, dead
  farm). Even "safe" ones are standing risk if that contract is later exploited →
  🟡, revoke.
- **`setApprovalForAll` grants** — list every NFT-collection operator approval;
  flag any to a marketplace you no longer use or don't recognize → 🟠/🔴.
- **Permit2 allowances** — surface Permit2 `amount`/`expiration` per token;
  flag full-balance amounts or long expiries → 🟡/🟠.
- **EIP-7702 delegations** — does the EOA have delegated code? If the target is
  unknown/unverified → 🔴 **compromised** (Step 6 fresh-wallet path), not a
  routine revoke.

Also screen the wallet's **history and surroundings**:

- **Address poisoning** — dust or **$0 transfers from a lookalike vanity
  address** (matching first/last characters of an address you really use),
  planted so you later **copy the wrong address** from history. Warn the user to
  never copy a destination from tx history; verify the full address.
- **Drainer-kit delayed draining** — off-the-shelf drainer kits (Inferno/
  Pink-style) frequently **wait days** after the malicious signature before
  pulling funds. *"Nothing happened yet"* is **not** safety — if a bad signature
  or approval exists, treat it as live and revoke/move now.

---

## Step 5: Red-Flags Quick Scan

Any one of these flips the review toward ⛔ / 🚨:

- **Unlimited approval to an unverified / random contract.**
- **ANY `eth_sign` request** — never legitimate; refuse outright.
- **A Permit2 signature on a site you didn't intend** (anything that isn't the
  protocol you deliberately chose) — full-balance blast radius.
- **`setApprovalForAll` requested by a "mint" / "claim"** — mints never need
  operator rights over your existing NFTs.
- **Urgency / countdown / FOMO** — "limited time", "claim before it's gone",
  weekend "limited mint".
- **Blind signing — no human-readable decode, no simulation/preview** of what
  changes. Missing preview is itself a warning.
- **Lookalike domain** — extra hyphen, swapped letters, non-Latin/punycode
  characters, `.app`/`.xyz` clone of a real `.org`.
- **Dust from a near-identical address** in history (address poisoning).
- **EIP-7702 delegation to an unknown contract** → assume compromise.
- **"Free airdrop / claim / giveaway / mint" sites** — the dominant drainer lure.
- **Delivery via Discord DM, hacked/large X account, or fake support**
  (fake "MetaMask"/"Coinbase"/"Ledger" help) — legitimate support never DMs you
  to sign.

---

## Step 6: Output Format

Lead with a **verdict banner**, then the findings, then remediation.

### Verdict banner (pick one)

- ✅ **LIKELY SAFE TO SIGN** — recognized intent, scoped/finite, verified
  spender, human-readable, on the intended site.
- ⚠️ **CAUTION — VERIFY FIRST** — plausible but with unconfirmed elements
  (verify domain, reduce to finite, confirm the spender) before signing.
- ⛔ **DO NOT SIGN** — a dangerous pattern is present (unlimited to unverified,
  Permit2 on the wrong site, disguised permit, mint asking `setApprovalForAll`,
  any `eth_sign`).
- 🚨 **WALLET MAY BE COMPROMISED — ACT NOW** — an unknown 7702 delegation, or a
  live drainer approval/permit already signed with funds still at risk. Go
  straight to the fresh-wallet remediation.

### Findings table

| # | Item | Type | Blast radius | Severity |
|---|---|---|---|---|
| 1 | … (token/spender/site) | unlimited approve / Permit2 / 7702 / … | one token / whole NFT collection / all Permit2 tokens / entire EOA | 🔴/🟠/🟡/🟢/ℹ️ |

For **each finding**, state **"what this grants"** in one plain sentence, then a
**recommendation** (sign / don't sign / reduce to N / revoke / move funds).

### Remediation playbook

- **Revoke** standing approvals via **revoke.cash** or the **Etherscan Token
  Approval Checker** — **per chain** (each revoke costs gas; do the highest-
  blast-radius ones first: unlimited, `setApprovalForAll`, Permit2).
- **Approve only what's needed** going forward — set finite caps, not unlimited.
- **If a malicious EIP-7702 delegation or a live drainer approval/permit is
  found and funds remain → move assets to a FRESH wallet immediately.** A
  compromised key or hostile delegation can't always be safely "cleaned";
  transfer assets out (to a brand-new seed you generate offline) **before**
  attempting any revoke, and assume the old address is burned.
- **Use a hardware wallet** and enable **clear signing (ERC-7730)** so you read
  exactly what you sign instead of a blind hash.
- **Burner / vault split** — a **vault** wallet that never touches experimental
  sites and holds the bulk of funds, and a **burner/spending** wallet with
  limited funds for minting and new dApps.
- **Simulate** transactions (Tenderly / wallet preview) before signing; **no
  preview = warning.**
- **Verify domains** by typing them yourself or using a bookmark — never via a
  DM/ad/search link. Type seed phrases **nowhere online**; keep them offline.
- **2FA via an authenticator app**, not SMS, on every exchange/email tied to
  your crypto.

### Disclaimer (always include)

> **Educational security guidance — not financial, legal, or investment advice,
> and not a guarantee of safety.** On-chain risk is real and transactions are
> **irreversible**; this review reasons only over the information you provided
> and cannot see live chain state. A "looks safe" here is not a warranty —
> verify the spender, the domain, and the decoded payload yourself. **If you
> believe your wallet is compromised, act immediately** (move funds to a fresh
> wallet) and consult a qualified security professional.

---

## Related Viprasol Skills

- **`smart-contract-audit`** — audit the Solidity/EVM contract *behind* a
  spender or 7702 delegation target for vulnerabilities and backdoors.
- **`defi-protocol-review`** — assess whether the protocol asking for an
  approval is itself trustworthy (admin keys, audits, oracle/TVL risk).

*Not affiliated with or endorsed by Anthropic.*
