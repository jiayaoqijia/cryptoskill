#!/usr/bin/env node

/**
 * DeFi Yield Monitor - 平台对比工具
 * 
 * 使用方式:
 * node compare.mjs --token USDC --platforms aave,compound,curve
 * node compare.mjs --token DAI --chains ethereum,arbitrum
 */

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    token: 'USDT',
    platforms: null,
    chains: null,
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) {
      options.token = args[i + 1].toUpperCase();
      i++;
    } else if (args[i] === '--platforms' && args[i + 1]) {
      options.platforms = args[i + 1].toLowerCase().split(',');
      i++;
    } else if (args[i] === '--chains' && args[i + 1]) {
      options.chains = args[i + 1].toLowerCase().split(',');
      i++;
    }
  }
  
  return options;
}

function comparePlatforms(options) {
  console.log(`📊 ${options.token} 平台对比分析\n`);
  console.log('─'.repeat(80));
  
  // 模拟数据
  const comparison = [
    { platform: 'Aave', apy: 7.8, tvl: 5600, risk: 'A', audit: '✅ Multiple', insurance: '✅ Yes', gas: 18 },
    { platform: 'Compound', apy: 7.5, tvl: 890, risk: 'A+', audit: '✅ Multiple', insurance: '✅ Yes', gas: 3 },
    { platform: 'Curve', apy: 6.9, tvl: 2100, risk: 'A', audit: '✅ Multiple', insurance: '✅ Yes', gas: 1 },
    { platform: 'Spark', apy: 8.2, tvl: 1200, risk: 'A', audit: '✅ Yes', insurance: '✅ Yes', gas: 15 },
    { platform: 'Morpho', apy: 8.0, tvl: 380, risk: 'B+', audit: '✅ Yes', insurance: '❌ No', gas: 20 },
  ];
  
  console.log('\n核心指标对比:\n');
  console.log('平台        APY     TVL      风险   审计      保险    Gas');
  console.log('─'.repeat(70));
  
  comparison.forEach(p => {
    if (!options.platforms || options.platforms.includes(p.platform.toLowerCase())) {
      console.log(
        `${p.platform.padEnd(10)} ${p.apy.toFixed(1).padStart(5)}%  ` +
        `$${p.tvl.toString().padStart(5)}M  ${p.risk.padEnd(5)} ${p.audit.padEnd(10)} ${p.insurance.padEnd(6)} $${p.gas}`
      );
    }
  });
  
  console.log('\n' + '─'.repeat(80));
  console.log('\n💡 分析建议:\n');
  
  console.log('🏆 收益最高: Spark (8.2% APY)');
  console.log('   适合：大额存款 (>5000 USDT)');
  console.log('   年收益：$820 / 10000 USDT\n');
  
  console.log('🛡️ 最安全：Compound (A+ 风险评级)');
  console.log('   适合：保守型投资者');
  console.log('   Gas 最低：$3 (小额存款划算)\n');
  
  console.log('⚖️ 综合最佳：Aave');
  console.log('   收益：7.8% (排名第 2)');
  console.log('   安全：A 级，多重审计，有保险');
  console.log('   TVL: $5.6B (最大流动性)\n');
  
  console.log('─'.repeat(80));
  console.log('\n⚠️  风险提示：APY 会波动，投资前请再次确认实时数据');
  console.log('💰 赞助：0x33f943e71c7b7c4e88802a68e62cca91dab65ad9\n');
}

const options = parseArgs();
comparePlatforms(options);
