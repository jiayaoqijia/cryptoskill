#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { ethers } = require('ethers');

const args = Object.fromEntries(process.argv.slice(2).map((v,i,a)=> v.startsWith('--') ? [v.slice(2), a[i+1] && !a[i+1].startsWith('--') ? a[i+1] : 'true'] : []).filter(Boolean));
const rpc = args.rpcUrl || 'https://bsc-dataseed.binance.org/';
const cfgPath = args.config || path.resolve(__dirname, '../../references/flux-bnb-addresses.json');
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));

const ABI = [
  'function getFTokensEntireData() view returns ((address tokenAddress,bool eip2612Deposits,bool isNativeUnderlying,string name,string symbol,uint256 decimals,address asset,uint256 totalAssets,uint256 totalSupply,uint256 convertToShares,uint256 convertToAssets,uint256 rewardsRate,uint256 supplyRate,int256 rebalanceDifference,(bool modeWithInterest,uint256 supply,uint256 withdrawalLimit,uint256 lastUpdateTimestamp,uint256 expandPercent,uint256 expandDuration,uint256 baseWithdrawalLimit,uint256 withdrawableUntilLimit,uint256 withdrawable,uint256 decayEndTimestamp,uint256 decayAmount) liquidityUserSupplyData)[])'
];

(async () => {
  const provider = new ethers.JsonRpcProvider(rpc);
  const resolver = new ethers.Contract(cfg.lendingResolver, ABI, provider);
  const rows = await resolver.getFTokensEntireData();

  const markets = rows.map((m) => {
    const supplyRateBps = Number(m.supplyRate); // Liquidity supply rate in bps (1% = 100)
    const rewardsRateRaw = Number(m.rewardsRate); // Rewards model rate in 1e12 precision where 1% = 1e12
    const rewardsRateBps = rewardsRateRaw / 1e10; // exact conversion to bps
    const totalApr = (supplyRateBps + rewardsRateBps) / 100;
    return {
      symbol: m.symbol,
      name: m.name,
      fToken: m.tokenAddress,
      underlying: m.asset,
      isNativeUnderlying: !!m.isNativeUnderlying,
      decimals: Number(m.decimals),
      totalAssetsRaw: m.totalAssets.toString(),
      totalSupplyRaw: m.totalSupply.toString(),
      supplyRateBps,
      rewardsRateRaw,
      rewardsRateBps,
      totalApr,
      notes: 'rewardsRate uses 1e12 precision in Fluid fToken code (1% = 1e12), converted exactly',
    };
  });

  console.log(JSON.stringify({ protocol: 'flux', chainId: cfg.chainId, returned: markets.length, markets }, null, 2));
})().catch((e) => {
  console.error(JSON.stringify({ error: String(e.message || e) }, null, 2));
  process.exit(1);
});
