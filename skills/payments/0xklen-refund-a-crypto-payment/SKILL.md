---
name: refund-a-crypto-payment
description: Use when returning a crypto payment to a customer. Handles the same-asset-only rule, the network fee, and the irreversible and taxable nature of the refund send.
---

# Refund a crypto payment

A refund is a new, irreversible transaction, not a reversal. Return the same asset on the same chain to the sending address, keep the fee policy explicit, and account for the disposal.

## Procedure

1. Identify the original payment: tx hash, from-address, asset contract, chain, amount, and block timestamp.
   `cast tx $TXHASH --rpc-url $RPC | jq '{from,to,value,blockNumber}'`
2. Refund the same asset on the same chain by default. A cross-asset refund is a second trade with its own price, tax event, and slippage — treat it as such.
3. Return to the from-address, or to an address the customer nominates in writing; treat a new address as a fresh counterparty check.
4. Decide who pays gas and state it in the terms. Default policy: the merchant absorbs gas for refunds; disclose the amount.
5. Compute the refund: original amount, or net of the original processing fee if the terms say so. Floor in base units.
6. Broadcast, then verify the tx is mined and the recipient balance increased:
   `cast receipt $REFUND_TX --rpc-url $RPC | grep -E "status|from|to"`.
7. Record the refund tx hash against the original invoice and payment for audit and tax (it is a disposal of the refunded asset).

## Pitfalls

- Refunding to a customer's exchange deposit address without the memo/tag: the funds are lost or need support to recover.
- Refunding a different asset "for convenience" and silently creating a taxable trade at a bad rate.
- Sending a refund with too low a fee and leaving it stuck; a replacement tx on the same nonce is needed.
- Assuming the original payment is still unspent; refund from a balance that covers it.
- Treating a refund of a suspected-stolen payment as safe: it can be tainted funds and the send is irreversible.
- A refund to a contract that cannot receive the token reverts and the fee is spent for nothing.
- The customer's original address may be flagged by a compliance tool; refunding to it can be a policy breach.
- Refunds issued after the invoice period land in a different tax period than the receipt, splitting one event across two.

## Verification

    cast receipt $REFUND_TX --rpc-url $RPC | grep -E "status|from|to"
    # status 1, to == nominated address, value == base-unit refund

Report the refund tx hash, amount, asset, chain, destination, and the gas paid.
