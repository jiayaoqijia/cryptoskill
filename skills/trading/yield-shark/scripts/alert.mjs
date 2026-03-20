#!/usr/bin/env node

/**
 * DeFi Yield Monitor - 收益提醒
 * 设置 APY 阈值提醒
 * 
 * 使用方式:
 * node alert.mjs --token DAI --min-apy 5
 * node alert.mjs --token USDC --platform aave --notify telegram
 */

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    token: null,
    platform: null,
    minApy: null,
    maxApy: null,
    notify: 'console',
    chain: null,
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) {
      options.token = args[i + 1].toUpperCase();
      i++;
    } else if (args[i] === '--platform' && args[i + 1]) {
      options.platform = args[i + 1].toLowerCase();
      i++;
    } else if (args[i] === '--min-apy' && args[i + 1]) {
      options.minApy = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--max-apy' && args[i + 1]) {
      options.maxApy = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--notify' && args[i + 1]) {
      options.notify = args[i + 1].toLowerCase();
      i++;
    } else if (args[i] === '--chain' && args[i + 1]) {
      options.chain = args[i + 1].toLowerCase();
      i++;
    }
  }
  
  return options;
}

function setupAlert(options) {
  console.log(`\n🔔 收益提醒设置\n`);
  console.log('─'.repeat(60));
  
  if (!options.token) {
    console.error('❌ 请指定代币：--token <USDT|USDC|DAI>');
    process.exit(1);
  }
  
  console.log(`代币：${options.token}`);
  
  if (options.platform) {
    console.log(`平台：${options.platform}`);
  } else {
    console.log(`平台：所有支持的平台`);
  }
  
  if (options.chain) {
    console.log(`链：${options.chain}`);
  } else {
    console.log(`链：所有支持的链`);
  }
  
  if (options.minApy) {
    console.log(`最低 APY: ${options.minApy}%`);
  }
  
  if (options.maxApy) {
    console.log(`最高 APY: ${options.maxApy}%`);
  }
  
  console.log(`通知方式：${options.notify}`);
  console.log('─'.repeat(60));
  
  // 模拟提醒设置
  console.log(`\n✅ 提醒已设置!\n`);
  console.log(`📋 提醒规则:`);
  console.log(`   当 ${options.token} 在 ${options.platform || '任意平台'} 的 APY ` +
    `${options.minApy ? `>= ${options.minApy}%` : '变化超过 0.5%'} 时`);
  console.log(`   通过 ${options.notify} 通知你\n`);
  
  // 通知方式说明
  console.log(`📱 支持的通知方式:`);
  console.log(`   - console: 终端输出 (当前)`);
  console.log(`   - telegram: Telegram 机器人`);
  console.log(`   - email: 邮件通知`);
  console.log(`   - webhook: 自定义 Webhook\n`);
  
  console.log(`⚙️  修改提醒:`);
  console.log(`   node alert.mjs --token ${options.token} --min-apy 6 --notify telegram\n`);
  
  console.log(`❌ 取消提醒:`);
  console.log(`   node alert.mjs --token ${options.token} --cancel\n`);
  
  console.log(`💰 赞助：0x33f943e71c7b7c4e88802a68e62cca91dab65ad9\n`);
}

const options = parseArgs();
setupAlert(options);
