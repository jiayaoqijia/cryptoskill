---
name: assess-stablecoin-freeze-and-blacklist-risk
description: Use when a payments flow depends on a freezeable stablecoin. Checks whether the issuer can seize a balance, monitors denylist changes, and caps concentration so one freeze cannot strand settlement.
---

# Assess stablecoin freeze and blacklist risk

Circle freezes USDC and Tether blacklists USDT; a balance is yours only while the issuer lets it be. For a payments desk this is counterparty risk that must be measured, monitored, and capped — not discovered when a payout stalls.

## Procedure

1. Confirm the token has a denylist by reading its ABI:
   `cast interface $USDC | grep -iE "blacklist|denylist|freeze"`
   USDC exposes `isBlacklisted(address)`; USDT exposes `isBlackListed(address)` and `addBlackList`.
2. Before accepting a large payment, check the payer and the destination:
   `cast call $USDC "isBlacklisted(address)(bool)" $ADDR --rpc-url $RPC` -> `false`.
3. Re-check the operating address right before a payout; a freeze can land between invoice and send.
4. Monitor the issuer's denylist for additions touching any address you hold or route:
   `cast logs --address $USDC --from-block $LAST --topic0 $BLACKLIST_TOPIC`.
5. Measure concentration: sum balances by issuer. A policy of "no single freezeable issuer above 40% of float" limits a single freeze to a controllable share.
6. Hold a non-freezeable buffer (native asset or a decentralised stablecoin) sized to cover a week of obligations.

## Pitfalls

- A freeze is silent: no event reaches your application layer, only the issuer's log.
- Sanctions-driven freezes can cascade across every issuer at once, defeating diversification built only on two fiat-backed coins.
- Checking the denylist once at onboarding misses a freeze applied later; re-check before every send.
- Assuming a "decentralised" stablecoin cannot freeze when it retains an upgradeable blacklist implementation.
- A freeze on one chain's contract does not freeze the same issuer's token on another chain unless the issuer chooses to.
- A denylist check can pass while a freeze transaction is pending in the mempool.
- A decentralised coin retaining a blacklist can still seize via a governance upgrade; read the implementation, not the label.

## Verification

    cast call $USDC "isBlacklisted(address)(bool)" $PAYOUT_ADDR --rpc-url $RPC
    # must return false for every address in the send path

Report per-issuer concentration, the last denylist check timestamp, and the non-freezeable buffer size.
