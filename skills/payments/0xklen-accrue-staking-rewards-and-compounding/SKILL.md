---
name: accrue-staking-rewards-and-compounding
description: Use when calculating staking reward accrual, converting APR to APY, or auditing a reward-per-token accumulator. Covers rewardRate, rewardPerTokenStored, and compounding maths with worked numbers.
---

# Accrue staking rewards and compounding

A staking contract pays a fixed `rewardRate` per second split across staked weight; the accumulator is exact only if every state change updates `rewardPerTokenStored` before `totalStaked` changes, and APR is never equal to APY.

## Procedure

1. Read the accumulator state: `rewardPerTokenStored`, `rewardRate` (tokens/sec, base units), `lastUpdateTime`, `totalStaked`.

2. Global accrual: `rewardPerToken += rewardRate * (now - lastUpdateTime) * 1e18 / totalStaked`. A staker's owed = `staked * (rewardPerToken - userRewardPerTokenPaid)/1e18 + rewards`.

   ```solidity
   function rewardPerToken() public view returns (uint256) {
       if (totalStaked == 0) return rewardPerTokenStored;
       return rewardPerTokenStored
           + (rewardRate * (block.timestamp - lastUpdateTime) * 1e18) / totalStaked;
   }
   ```

3. Convert APR to APY by compounding frequency. Daily: `APY = (1 + APR/365)^365 - 1`. Continuous: `APY = e^APR - 1`.

   python3 -c "import math; print((1+0.20/365)**365-1, math.exp(0.20)-1)"
   0.22129... 0.22140...

   So 20% APR is ~22.1% APY compounded daily.

4. Worked accrual: `rewardRate = 1e18` (1 token/sec), `totalStaked = 1,000,000e18`. Daily emission = `86,400` tokens. Per-staker daily = `staked/1e6 * 86400`; a 10,000-token stake earns `864` tokens/day before compounding.

5. Check funding: `rewardRate * (periodFinish - start)` must be held by the contract. Re-notify tokens before `periodFinish` or emissions stop mid-accrual.

6. For restaking/liquid-staking tokens, add the base staking yield to the incentive yield but keep them separate — one is protocol revenue, the other is dilution.

## Pitfalls

- Changing `totalStaked` without calling `updateReward` first retroactively dilutes or overpays every staker from the last checkpoint.
- Quoting an APR on decaying emissions and compounding it to APY overstates returns; the rate is not constant.
- `periodFinish` in the past with nonzero `rewardRate`: the accumulator keeps ticking but the contract has no tokens to pay, so reads look fine until a claim reverts.

## Verification

    cast call $POOL "rewardPerToken()(uint256)" --rpc-url $RPC

Compare to `rewardPerTokenStored + rewardRate*(now-lastUpdateTime)*1e18/totalStaked`; a mismatch means a state change skipped the update.

Report the accrual rate, the compounding assumption, and the funded `periodFinish`, each with the call behind it.
