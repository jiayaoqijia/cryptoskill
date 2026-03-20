# Staking Concepts

## Delegation

Cardano uses a delegated proof-of-stake (DPoS) system. ADA holders delegate their stake to a stake pool, which produces blocks on their behalf. Delegation does not lock or move ADA — it stays in the wallet.

## Stake Pools

Stake pools are run by operators who maintain Cardano nodes. Each pool has a unique pool ID (bech32 format starting with `pool1...`). Pool performance and fees affect reward distribution.

## Rewards

Staking rewards are distributed every epoch (~5 days). Rewards accumulate automatically and can be claimed at any time. The `availableAdaRewards` field shows the total unclaimed rewards in ADA.

## Epochs

A Cardano epoch lasts 5 days (432,000 slots). Delegation changes take effect 2 epochs later. Rewards from staking begin 2 epochs after initial delegation.
