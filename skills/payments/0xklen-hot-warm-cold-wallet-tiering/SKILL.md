---
name: hot-warm-cold-wallet-tiering
description: Use when deciding where signing keys and funds live across an operation. Assigns balances and authority to hot, warm, and cold tiers with concrete caps and a sweep schedule.
---

# Tier wallets hot, warm, and cold

One wallet doing everything is the standard path to total loss. This skill puts a spend cap on the online tier, hardware-gates the middle tier, and keeps the treasury behind a multisig that no single host can move.

## Procedure

1. Define three tiers by authority, not by balance:
   - **hot** — key on a networked host, used for gas and small ops. Cap at 1% of treasury or $2,000, whichever is lower.
   - **warm** — hardware-backed single signer with an allowlisted set of contracts. Cap at 10% of treasury.
   - **cold** — M-of-N multisig, keys on hardware, no hot path. Holds the remainder.
2. Give each tier its own address derived from a distinct key. Never reuse a hot key for governance.
3. Sweep the hot tier down to its float on a schedule. A daily cron that leaves only seven days of gas:
   `cast send $COLD --value $(cast to-wei 4.5 ether) --account hot --rpc-url $RPC`
4. Enforce the warm cap in the wallet policy: allowlist the destination contracts and set a per-tx and per-day limit. Deny anything off-list.
5. Require cold movements to be proposed, reviewed, and signed on separate devices, never co-located.
6. Record the address-to-tier mapping in the repo so an incident review can confirm which key was compromised.
7. Review the caps monthly against the treasury size; a cap set when the treasury was small is too small to be useful, or too large to be safe.

## Pitfalls

- "Warm" only means anything if signatures happen on the hardware device. A key exported to disk with an allowlist is a hot key with extra steps.
- A hot wallet cap is a loss cap, not a spend cap: an attacker drains the whole float at once, so keep the float small.
- Sweeping on a fixed schedule is observable; vary the timing or use a private relay for the sweep transaction.
- Automation that holds a warming key in a CI secret turns your warm tier into hot. Require human presence for every warm signature.
- A tier boundary with no monitoring is theoretical; alert on any hot-tier balance above the cap and on any warm signature outside the allowlist.

- A cold tier without a tested recovery is one lost device away from frozen funds; rehearse a sign quarterly.
- Tiering across chains needs one hot address per chain; a shared hot key multiplies the blast radius.
- If a hot key is compromised, assume every pending tx from it is attacker-controlled and cancel nonces fast.

## Verification

    cast balance $HOT --rpc-url $RPC && cast balance $COLD --rpc-url $RPC
    # expect HOT below the stated float and the ratio HOT/COLD under 1%

Report each tier's address, its balance, and the observed ratio, with the commands behind them.
