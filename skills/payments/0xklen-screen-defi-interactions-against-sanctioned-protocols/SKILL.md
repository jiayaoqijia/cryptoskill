---
name: screen-defi-interactions-against-sanctioned-protocols
description: Use when a transaction or integration touches a DeFi protocol, router or relayer that has itself been designated, and you must decide what to block and what to record.
---

# Screen DeFi interactions against sanctioned protocols

Designations have landed on protocols and on individual addresses inside them. The control point
is the address, but the risk surface is any path that routes value through a designated contract,
including relayers and aggregators that hide the hop.

## Procedure

1. Resolve the transaction's full call path, not just its top-level `to`. An aggregator or router
   can carry a designated pool address in calldata while the outer target looks clean.

       cast tx $HASH --rpc-url $RPC --json | jq -r '.to, .input'
       cast calldata-decode "swapExactTokensForTokens(uint256,uint256,address[],address,uint256)" \
         0x38ed1739...

2. Extract every address the call touches — the router, each pool, the recipient, any relayer —
   and screen each one, not the protocol name:

       for a in $(cast tx $HASH --rpc-url $RPC --json | jq -r '.to'); do
         grep -iq "${a#0x}" sdn.csv && echo "HIT $a"
       done

3. Check inbound as well as outbound. Value withdrawn from a designated pool is as reportable as
   value sent in, and a faucet-style claim can pull from a designated contract.

4. Distinguish the protocol from the address. A designated individual address inside an otherwise
   unsanctioned protocol does not sanction the whole protocol, and vice versa; record which one
   you actually matched.

5. For integrations, pin the allow-list of contracts the app will route through, so a new
   aggregator cannot silently introduce a designated hop:

       grep -v '^#' allowlist.txt | wc -l   # every entry reviewed and dated

6. Log the screen per transaction with the addresses checked and the list digest, and block on a
   hit before broadcast.

## Pitfalls

- Blocking by protocol name in a UI string while the contract address is a clone that is not
  designated — or the reverse, letting a designated address through because the name looked
  familiar.
- Screening only the sender's wallet and missing the recipient or the pool in calldata.
- Assuming a front-end block is a compliance control; direct contract calls and private
  transactions bypass the UI entirely. The control is at the transaction-relay boundary you own.
- Treating "the protocol was delisted" as universal. Delisting can be jurisdiction-specific and
  does not retroactively clear historical flows.
- Ignoring gas relayers and paymasters, which can be the designated party even when the user is
  not.

## Verification

    for a in $(cat touched-addresses.txt); do grep -iq "${a#0x}" sdn.csv || echo "clear $a"; done

Every touched address must appear either as a HIT or as a clear line; an address missing from the
list entirely means the extraction missed a hop.

Report the touched addresses with per-address results, the list digest, and the blocking action
taken. Whether a particular interaction is prohibited is a legal question that requires qualified
counsel's determination given the current designation and any licence.
