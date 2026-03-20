#!/usr/bin/env node
/**
 * 🦈 YieldShark - 收益优化建议
 * 分析当前持仓，推荐最优收益策略
 */

import fetch from 'node-fetch';

const DEFI_LLAMA_API = 'https://yields.llama.fi/pools';

// 配置 - 用户钱包地址
const USER_WALLETS = {
  usdt: '0x33f943e71c7b7c4e88802a68e62cca91dab65ad9',
  usdc: '0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44'
};

// 参数解析
const args = process.argv.slice(2);
const params = {
  token: 'USDT',
  amount: 1000,
  help: false
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--help' || args[i] === '-h') params.help = true;
  else if (args[i] === '--token') params.token = args[++i].toUpperCase();
  else if (args[i] === '--amount') params.amount = parseFloat(args[++i]);
}

function showHelp() {
  console.log(`
🦈 YieldShark - 收益优化建议

用法:
  node scripts/optimize.mjs [选项]

示例:
  node scripts/optimize.mjs                    # 默认分析 1000 USDT
  node scripts/optimize.mjs --token USDC --amount 5000

选项:
  --token <symbol>     代币符号 (USDT/USDC/DAI), 默认：USDT
  --amount <number>    投资金额，默认：1000
  --help, -h           显示帮助
`);
}

// 获取数据
async function fetchData() {
  const response = await fetch(DEFI_LLAMA_API);
  const result = await response.json();
  return result.data || result || [];
}

// 计算预期收益
function calculateReturns(data, token, amount) {
  const tokenUpper = token.toUpperCase();
  
  // 筛选稳定币池
  const pools = data.filter(pool => {
    const symbol = (pool.symbol || '').toUpperCase();
    const tvl = pool.tvlUsd || 0;
    const apy = pool.apy || 0;
    
    // 必须包含目标代币，TVL > $1M，APY > 5%
    return symbol.includes(tokenUpper) && tvl > 1e6 && apy > 5;
  });
  
  // 按 APY 排序
  pools.sort((a, b) => (b.apy || 0) - (a.apy || 0));
  
  return pools.slice(0, 10).map(pool => ({
    platform: pool.project || 'Unknown',
    chain: pool.chain || 'Unknown',
    apy: pool.apy || 0,
    tvl: pool.tvlUsd || 0,
    risk: pool.ilRisk || 'B',
    daily: amount * (pool.apy || 0) / 100 / 365,
    monthly: amount * (pool.apy || 0) / 100 / 12,
    yearly: amount * (pool.apy || 0) / 100
  }));
}

// 显示优化建议
function displayOptimization(returns, token, amount) {
  console.log('\n🦈 YieldShark - 收益优化建议\n');
  console.log(`分析：${amount.toLocaleString()} ${token}`);
  console.log(`钱包：${USER_WALLETS[token.toLowerCase()] || USER_WALLETS.usdt}\n`);
  
  console.log('排名  平台 (链)        APY      日收益    月收益    年收益    TVL');
  console.log('─'.repeat(90));
  
  returns.forEach((item, i) => {
    const rank = String(i + 1).padEnd(4);
    const name = `${item.platform} (${item.chain})`.slice(0, 18).padEnd(18);
    const apy = `${item.apy.toFixed(2)}%`.padEnd(10);
    const daily = `$${item.daily.toFixed(2)}`.padEnd(10);
    const monthly = `$${item.monthly.toFixed(2)}`.padEnd(10);
    const yearly = `$${item.yearly.toFixed(2)}`.padEnd(10);
    const tvl = `$${(item.tvl / 1e6).toFixed(1)}M`.padEnd(8);
    
    console.log(`${rank} ${name} ${apy} ${daily} ${monthly} ${yearly} ${tvl}`);
  });
  
  console.log('─'.repeat(90) + '\n');
  
  // 最优推荐
  if (returns.length > 0) {
    const best = returns[0];
    console.log('🏆 最优推荐：');
    console.log(`   ${best.platform} (${best.chain}) - APY: ${best.apy.toFixed(2)}%`);
    console.log(`   预期年收益：$${best.yearly.toFixed(2)} (vs 银行活期 ~$0.50)`);
    console.log(`   超额收益：+$${(best.yearly - 0.50).toFixed(2)} 🚀\n`);
  }
  
  // 对比银行
  const bankApy = 0.05; // 银行活期 ~0.05%
  const bankYearly = amount * bankApy / 100;
  const bestYearly = returns[0]?.yearly || 0;
  const extra = bestYearly - bankYearly;
  
  console.log('📊 收益对比：');
  console.log(`   银行活期：$${bankYearly.toFixed(2)}/年 (0.05% APY)`);
  console.log(`   DeFi 最优：$${bestYearly.toFixed(2)}/年 (${returns[0]?.apy.toFixed(2)}% APY)`);
  console.log(`   超额收益：+$${extra.toFixed(2)}/年 (${(extra / bankYearly * 100).toFixed(0)}x) 🚀\n`);
  
  console.log('💰 赞助收款地址：');
  console.log(`   USDT (ERC20): ${USER_WALLETS.usdt}`);
  console.log(`   USDC (ERC20): ${USER_WALLETS.usdc}\n`);
  
  console.log('⚠️ 风险提示：DeFi 存在智能合约风险，建议分散投资');
  console.log('💡 查询实时收益率：node scripts/monitor.mjs USDT\n');
}

// 主函数
async function main() {
  if (params.help) {
    showHelp();
    process.exit(0);
  }
  
  try {
    console.log('📡 正在分析 DeFiLlama 数据...\n');
    const data = await fetchData();
    const returns = calculateReturns(data, params.token, params.amount);
    displayOptimization(returns, params.token, params.amount);
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
