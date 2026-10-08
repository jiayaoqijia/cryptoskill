---
name: classify-a-stablecoin-peg-mechanism
description: Use when you must decide how a stablecoin holds its peg before relying on it. Separates fiat-backed, crypto-backed, and algorithmic designs and names the exact failure mode of each.
---

# Classify a stablecoin peg mechanism

A stablecoin holds its peg for a specific structural reason, and that reason dictates how it breaks. Classify the design from the contracts and reserves before treating any "1 dollar" price as durable.

## Procedure

1. Find the issuance contract and read who can mint and burn:
   `cast call $TOKEN "minter()(address)" --rpc-url $RPC` (or `owner()`, `governor()`).
2. Bucket the design:
   - Fiat-backed: off-chain reserves at a custodian, 1:1 redemption, peg enforced by the issuer's bank account (USDC, USDT).
   - Crypto-backed: on-chain collateral above 100% with liquidation (DAI). Peg enforced by collateral value plus arbitrage.
   - Algorithmic / seigniorage: peg enforced by mint-and-burn of a partner token, no hard collateral (UST).
3. For fiat-backed, trace the custody chain: reserve attestation URL from the issuer, custodian names, redemption counterparty.
4. For crypto-backed, read the collateral ratio and liquidation parameters:
   `cast call $VAT "ilks(bytes32)(uint256,uint256,uint256,uint256,uint256)" $ILK --rpc-url $RPC`.
5. For algorithmic, identify the stabilisation token and whether supply is elastic; a design that pays yield in its own token is a Ponzi-shaped peg, not a collateralised one.
6. Record the peg band actually traded: pull the deepest pool's price and depth — the peg is only as good as the market that arbitrages it.
7. Write the failure mode in one line: bank run on the custodian, collateral crash plus liquidation cascade, or reflexive death spiral.

## Pitfalls

- Attestation is not audit: a monthly letter from a custodian does not verify liabilities or completeness.
- A crypto-backed stablecoin at 150% collateral is safe only while the collateral is liquid; ETH down 40% in a day turns 150% into 90%.
- "Decentralised" stablecoins often keep a privileged minter; check roles, not the marketing.
- Treating an algorithmic design's yield as revenue when it is dilution is how the reflexivity is missed.
- A peg can hold in the market while redemption is suspended; a closed redemption window is a peg break the price has not yet shown.

## Verification

    cast call $TOKEN "totalSupply()(uint256)" --rpc-url $RPC && cast call $TOKEN "minter()(address)" --rpc-url $RPC
    # minter and total supply returned; reserve URL located for a fiat-backed coin

Report the design class, the exact mechanism enforcing the peg, and the single failure mode you expect.
