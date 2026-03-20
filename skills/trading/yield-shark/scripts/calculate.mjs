#!/usr/bin/env node

/**
 * DeFi Yield Monitor - 收益计算器
 * 计算净收益 (扣除 Gas 费)
 * 
 * 使用方式:
 * node calculate.mjs --token USDT --amount 5000 --platform aave
 * node calculate.mjs --amount 10000 --apy 8.5 --gas-cost 20
 */

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    token: 'USDT',
    amount: null,
    apy: null,
    gasCost: null,
    platform: null,
    duration: 365, // days
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) {
      options.token = args[i + 1].toUpperCase();
      i++;
    } else if (args[i] === '--amount' && args[i + 1]) {
      options.amount = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--apy' && args[i + 1]) {
      options.apy = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--gas-cost' && args[i + 1]) {
      options.gasCost = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--platform' && args[i + 1]) {
      options.platform = args[i + 1].toLowerCase();
      i++;
    } else if (args[i] === '--duration' && args[i + 1]) {
      options.duration = parseInt(args[i + 1]);
      i++;
    }
  }
  
  return options;
}

function calculate(options) {
  if (!options.amount) {
    console.error('❌ 请指定金额：--amount <USDT>');
    process.exit(1);
  }
  
  // 如果没提供 APY，使用平台默认值
  let apy = options.apy;
  let gasCost = options.gasCost;
  let platformName = options.platform || 'Unknown';
  
  const platformDefaults = {
    aave: { apy: 7.8, gas: 18 },
    compound: { apy: 7.5, gas: 3 },
    curve: { apy: 6.9, gas: 1 },
    spark: { apy: 8.2, gas: 15 },
    morpho: { apy: 8.0, gas: 20 },
  };
  
  if (options.platform && platformDefaults[options.platform]) {
    const defaults = platformDefaults[options.platform];
    if (!apy) apy = defaults.apy;
    if (!gasCost) gasCost = defaults.gas;
    platformName = options.platform.charAt(0).toUpperCase() + options.platform.slice(1);
  }
  
  if (!apy) {
    apy = 7.5; // 默认 APY
  }
  if (!gasCost) {
    gasCost = 10; // 默认 Gas
  }
  
  // 计算
  const grossYield = options.amount * (apy / 100) * (options.duration / 365);
  const netYield = grossYield - gasCost;
  const netApy = (netYield / options.amount) * (365 / options.duration) * 100;
  const breakevenMonths = gasCost > 0 ? (gasCost / (grossYield / 12)) : 0;
  const gasPercentage = (gasCost / options.amount) * 100;
  
  // 输出
  console.log(`\n📊 净收益计算器\n`);
  console.log('─'.repeat(60));
  console.log(`代币：${options.token}`);
  console.log(`平台：${platformName}`);
  console.log(`本金：$${options.amount.toLocaleString()}`);
  console.log(`APY:  ${apy.toFixed(2)}%`);
  console.log(`Gas:  $${gasCost} (${gasPercentage.toFixed(2)}%)`);
  console.log(`周期：${options.duration} 天`);
  console.log('─'.repeat(60));
  console.log(`\n收益详情:\n`);
  
  console.log(`📈 毛收益：$${grossYield.toFixed(2)} (${apy.toFixed(2)}% APY)`);
  console.log(`⛽ Gas 成本：$${gasCost} (一次性)`);
  console.log(`💰 净收益：$${netYield.toFixed(2)} (${netApy.toFixed(2)}% APY)`);
  
  if (breakevenMonths > 0 && isFinite(breakevenMonths)) {
    console.log(`⏱️  回本时间：${breakevenMonths.toFixed(1)} 个月`);
  }
  
  console.log('\n' + '─'.repeat(60));
  console.log('\n💡 建议:\n');
  
  if (gasPercentage > 5) {
    console.log('❌ Gas 占比过高 (>5%) 建议增加存款金额或选择 L2 网络');
  } else if (gasPercentage > 2) {
    console.log('⚠️  Gas 占比适中 (2-5%) 建议中长期持有 (3 个月+)');
  } else {
    console.log('✅ Gas 占比合理 (<2%) 存款金额合适');
  }
  
  if (options.amount < 500) {
    console.log('\n💰 小额存款建议 (<$500):');
    console.log('   优先选择 Gas 低的平台 (Arbitrum/Base > Ethereum)');
  } else if (options.amount < 5000) {
    console.log('\n💰 中等存款建议 ($500-$5000):');
    console.log('   综合考虑 APY 和 Gas，Aave/Optimism 是不错的选择');
  } else {
    console.log('\n💰 大额存款建议 (>$5000):');
    console.log('   优先选择 APY 最高的平台，Gas 占比可忽略');
    console.log('   建议分散到 2-3 个平台降低风险');
  }
  
  console.log('\n' + '─'.repeat(60));
  console.log(`\n💰 赞助作者：0x33f943e71c7b7c4e88802a68e62cca91dab65ad9\n`);
}

const options = parseArgs();
calculate(options);
