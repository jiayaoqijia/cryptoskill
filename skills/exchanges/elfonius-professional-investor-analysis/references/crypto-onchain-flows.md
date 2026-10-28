# Crypto Ownership, Flows and Control

Purpose: answer who owns the asset, who is buying or selling, and who can change the rules. Price is the outcome; flows and control are the causes.

## Holder concentration

- Top 1/10/50/100 holder share; state whether the basis is total supply, float or staked supply.
- Label wallets where possible: team, foundation, treasury, investors, advisors, market makers, CEX, bridges, protocol-owned, burned.
- Exclude protocol-owned and burned supply only when the definition is explicit; show both gross and adjusted concentration.
- Cohort table: team / foundation / treasury / investors / miners / validators / retail / CEX / bridges.
- Nakamoto coefficient or takeover cost where estimable; state the assumptions.

## Staking and validator flows

- Net stake/unstake over 7/30/90 days; staking ratio; APR; validator count.
- Top 5/10 validator stake share; take rates; root cut; delegation concentration.
- Validator returns, slashing history, client/version concentration.
- Is staking locked, liquid or conviction-based? What is the unstake delay?

## Protocol and market flows

- Protocol buys/burns; root sells; cross-subnet flows; treasury outflows; incentive spend.
- Flow decomposition of price change: protocol + root + users + cross-subnet = net. Label the methodology and period.
- Distinguish protocol buybacks from company buybacks; identify the funding source.
- Treasury: composition, stable-denominated runway, who can move funds, multisig threshold.

## Miner economics

- Active miners, top miner share, emission per miner, hardware, registration cost, UID churn.
- Is emission concentrated in a few miners? Does the top miner have an advantage (data, hardware, latency)?
- Miner payback and whether miners are mercenary or long-lived.

## Governance and control

- On-chain execution versus signaling snapshot; quorum; turnout; timelock; emergency powers.
- Owner hotkey, multisig, DAO/foundation, upgrade authority; who can pause, mint, change fees or upgrade.
- Conviction locks, takeover gate, vote-buying cost versus treasury controlled.

## Tables

**Holders:** wallet/group, share, label, locked/unlocked, source, basis.

**Flows:** period, protocol buys, root sells, user net, cross-subnet, net price change, source.

**Validators/miners:** count, top share, stake/emission, take, payback.

## Sources

- Taostats (`stake_balance`, pool, validator), block explorers, Dune, governance forum, vesting contracts, treasury wallets.
- Record chain, address, block and retrieval time for every state claim.

## Interpretation

- High concentration plus low float = squeeze potential and exit risk.
- Staking locks reduce float but increase governance and unstake-queue risk.
- Protocol buys can mask user selling; always decompose rather than reading net price.
- Rising validator concentration is a capture risk, even if yield is attractive.

## Red flags

- Top 10 hold a majority and are unlabeled.
- Treasury or team wallets can mint, pause or upgrade without a timelock.
- Protocol buys are the only bid; users are net sellers.
- Staking APR funded by emissions while the token price falls.
- Undisclosed related-party wallets or market-maker loans.
