---
name: check-stablecoin-issuer-freeze-controls
description: Use when holding or accepting a fiat-backed stablecoin and you need to know the issuer can freeze addresses, how to detect a freeze, and what it means for funds you custody.
---

# Check stablecoin issuer freeze controls

Most large stablecoin contracts include a blacklist and a freeze function controlled by the
issuer. That control is a counterparty risk on your balance sheet: the tokens can be stopped
without your consent, and the code path is public.

## Procedure

1. Identify the contract you actually hold and read its freeze surface before trusting a balance:

       cast call $USDC "isBlacklisted(address)(bool)" $HOLDER --rpc-url $RPC
       cast call $USDC "paused()(bool)" --rpc-url $RPC
       cast call $USDC "owner()(address)" --rpc-url $RPC

2. Check the code, not just the ABI: confirm whether `blacklist` is callable by an EOA, a
   multisig, or a role, and whether it can be invoked for any address at any time.

       cast call $USDC "getBlacklistStatus(address)(bool)" $HOLDER --rpc-url $RPC

3. Monitor the freeze events on your addresses and on those you transact with. A freeze shows up
   as event activity with no transfer of value:

       cast logs --from-block $START --address $USDC \
         "Blacklisted(address)" --rpc-url $RPC | head

4. Measure the exposure: how much of the float is in freezeable tokens, in which addresses, and
   what fraction of the obligation could be stopped in one transaction. Report it as a number.

5. Decide the operating rule: how much freezeable balance you are willing to hold, whether you
   sweep to a cold address the issuer does not know, and what the fallback asset is if a freeze
   lands.

6. Write the runbook for a freeze: it is not a bug and not reversible by you. The path is issuer
   contact, evidence of source of funds, and legal route — and the first hour is about preserving
   records.

## Pitfalls

- Assuming a freeze is limited to sanctioned addresses. Issuers act on law-enforcement requests
  and on their own policy, and the contract does not constrain them to published lists.
- Holding a single large hot balance, which turns one freeze call into a total stop.
- Confusing a paused contract (all transfers stop) with a per-address blacklist (one address
  stops). The impact and the response differ.
- Treating a freeze as a crypto-market event when it is a contractual and legal event; nobody on
  the engineering side can unfreeze it.
- Ignoring freeze risk in token choice for payments, where a swapped token could leave a
  merchant with a frozen receivable.

## Verification

    cast call $USDC "isBlacklisted(address)(bool)" $HOT_WALLET --rpc-url $RPC
    cast logs --from-block 0 --address $USDC "Blacklisted(address)" --rpc-url $RPC | wc -l

The first call must return `false` for every operating address you hold; the second gives the
programme's lifetime freeze-event count as a scale check.

Report the contract, the freeze authority and its controller, the freezeable exposure by address,
and the runbook pointer. Whether a frozen balance can be recovered, and by what route, is a legal
question for counsel.
