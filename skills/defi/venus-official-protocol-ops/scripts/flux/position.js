#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { ethers } = require('ethers');

const a = Object.fromEntries(process.argv.slice(2).map((v,i,arr)=> v.startsWith('--') ? [v.slice(2), arr[i+1] && !arr[i+1].startsWith('--') ? arr[i+1] : 'true'] : []).filter(Boolean));
if (!a.wallet) throw new Error('wallet required: --wallet 0x...');

const rpc = a.rpcUrl || 'https://bsc-dataseed.binance.org/';
const cfgPath = a.config || path.resolve(__dirname, '../../references/flux-bnb-addresses.json');
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));

const ABI = [
  'function getUserPositions(address user_) view returns (((address tokenAddress,bool eip2612Deposits,bool isNativeUnderlying,string name,string symbol,uint256 decimals,address asset,uint256 totalAssets,uint256 totalSupply,uint256 convertToShares,uint256 convertToAssets,uint256 rewardsRate,uint256 supplyRate,int256 rebalanceDifference,(bool modeWithInterest,uint256 supply,uint256 withdrawalLimit,uint256 lastUpdateTimestamp,uint256 expandPercent,uint256 expandDuration,uint256 baseWithdrawalLimit,uint256 withdrawableUntilLimit,uint256 withdrawable,uint256 decayEndTimestamp,uint256 decayAmount) liquidityUserSupplyData) fTokenDetails,(uint256 fTokenShares,uint256 underlyingAssets,uint256 underlyingBalance,uint256 allowance) userPosition)[])'
];

(async () => {
  const provider = new ethers.JsonRpcProvider(rpc);
  const resolver = new ethers.Contract(cfg.lendingResolver, ABI, provider);
  const rows = await resolver.getUserPositions(a.wallet);

  const positions = rows.map((x) => {
    const d = Number(x.fTokenDetails.decimals || 18);
    const supplyRateBps = Number(x.fTokenDetails.supplyRate); // bps (1% = 100)
    const rewardsRateRaw = Number(x.fTokenDetails.rewardsRate); // 1e12 precision (1% = 1e12)
    const rewardsRateBps = rewardsRateRaw / 1e10; // exact bps
    return {
      symbol: x.fTokenDetails.symbol,
      fToken: x.fTokenDetails.tokenAddress,
      underlying: x.fTokenDetails.asset,
      supplyRateBps,
      rewardsRateRaw,
      rewardsRateBps,
      totalApr: (supplyRateBps + rewardsRateBps) / 100,
      userSharesRaw: x.userPosition.fTokenShares.toString(),
      userAssetsRaw: x.userPosition.underlyingAssets.toString(),
      userWalletBalanceRaw: x.userPosition.underlyingBalance.toString(),
      userAssetsApprox: Number(ethers.formatUnits(x.userPosition.underlyingAssets, d)),
    };
  });

  console.log(JSON.stringify({ protocol: 'flux', chainId: cfg.chainId, wallet: a.wallet, positions }, null, 2));
})().catch((e) => {
  console.error(JSON.stringify({ error: String(e.message || e) }, null, 2));
  process.exit(1);
});
