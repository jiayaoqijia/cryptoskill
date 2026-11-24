# Example — Yield Farm Review (Anon, EOA Owner, Unaudited, 200% APY ⇒ Avoid)

> **Illustrative example.** "MoonHarvest Finance" and all details below are
> fictional, used to demonstrate the skill's output format. Not a real protocol
> and not financial advice. This example deliberately depicts a textbook rug
> profile.

## Header

| | |
|---|---|
| **Protocol** | MoonHarvest Finance (illustrative) |
| **Chain(s)** | A new alt-L1 with thin tooling/audits |
| **Category** | Yield farm / staking pools |
| **TVL & trend** | ~$22M, **spiked from ~$2M in 6 days** after an influencer push |
| **Token** | `MOON` — minted as farm rewards; team holds a large unvested share |
| **Key contracts** | MasterChef `0xM0…`, `MOON` token `0xMn…` — owner is an **EOA** `0xEa…` |
| **Reviewed** | Landing page + thin docs, explorer (source **unverified** on MasterChef), no audit found |

## Risk Matrix

| Dimension | Severity | Key finding |
|---|---|---|
| (a) Smart-contract control | **Critical** | MasterChef and `MOON` token owned by a **single EOA**; owner can **`mint` MOON arbitrarily**, change pool allocations, and call `emergencyWithdraw`-style functions. No timelock, no multisig. |
| (b) Audits & track record | **Critical** | **No audit**, MasterChef source **unverified** on the explorer, no bug bounty, no track record — funds sit behind unreviewed, unreadable code. |
| (c) Economic design | **High** | Advertised **"fixed 200% APY"** is paid entirely in **freshly minted MOON** — pure emissions/inflation, no real revenue; classic reflexive ponzi dynamic. |
| (d) Liquidity & TVL | **High** | **Recent 10× TVL spike** in days; LP "locked" only by a **claim** (no lock contract shown); a few wallets dominate deposits. |
| (e) Oracle dependency | **High** | Reward/pricing references the project's **own MOON/USDC spot pool** — fully team-controllable and manipulable. |
| (f) Team & transparency | **High** | **Fully anonymous** team, copy-paste docs, hype-only Telegram, large insider token allocation with no vesting transparency. |
| (g) Composability / contagion | **Medium** | Relies on a thin alt-L1 bridge for inflows; exit liquidity evaporates if the bridge or the single MOON pool breaks. |

## Top Risks

1. **EOA owner with mint + withdraw powers (Critical).** A single private key
   `0xEa…` controls the token supply and pool logic. That key can **mint
   unlimited MOON**, redirect rewards, or pull deposits at any moment, with no
   timelock to warn users. This alone is a funds-at-immediate-risk rug vector.
2. **Unaudited, unverified code (Critical).** The contract holding the money is
   not even source-verified, let alone audited. There is no way to know what the
   `deposit`/`withdraw` functions actually do — the code could contain a hidden
   backdoor.
3. **"Fixed 200% APY" funded by minting (High).** The yield is the token. Early
   exiters are paid by later depositors' capital and inflation; when inflows
   stop, MOON price and APY collapse together.
4. **Anon team + 10× TVL spike (High).** The anonymous team, claim-only "locked"
   LP, and a sudden influencer-driven TVL spike together form the textbook
   rug-pull setup.

## "If You Still Deposit" — Risk-Mitigation Note

There is **no mitigation that makes this safe.** A single key can drain or
dilute funds and the code is unreviewable, so any deposit should be treated as
money you have **already lost**. If you ignore that: deposit only a trivial,
disposable amount from a **throwaway wallet**, **revoke approvals immediately**
after any interaction, never approve unlimited token allowances, and do not add
more chasing the APY. Watch the owner EOA for a mint or large transfer — by the
time you see it, it is usually too late.

## Verdict

**Avoid.** MoonHarvest hits nearly every red flag at once: an **EOA owner that
can mint the token and move funds**, **no audit** on **unverified** code, a
**"fixed 200% APY"** paid purely in inflation, a **10× TVL spike** in days,
claim-only "locked" liquidity, a **team-controlled spot oracle**, and a **fully
anonymous** team. Any one of the two Critical findings forces an **Avoid**
verdict on its own; together they are the textbook rug profile. There is no
position size or mitigation that makes this an acceptable risk. *Illustrative;
not financial advice — verify on-chain yourself.*
