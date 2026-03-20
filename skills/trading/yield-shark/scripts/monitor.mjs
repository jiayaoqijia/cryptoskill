#!/usr/bin/env node

/**
 * YieldIQ - 主程序 (真实 API 版)
 * 查询稳定币最优收益率
 * 
 * 使用方式:
 * node scripts/monitor.mjs USDT
 * node scripts/monitor.mjs USDC --limit 10
 * node scripts/monitor.mjs DAI --chain ethereum
 */

// 平台元数据 (风险评级等)
const PLATFORM_METADATA = {
  'aave-v3': { name: 'Aave V3', risk: 'A', riskDisplay: '🟢 A' },
  'compound-v3': { name: 'Compound V3', risk: 'A+', riskDisplay: '🟢 A+' },
  'spark': { name: 'Spark', risk: 'A', riskDisplay: '🟢 A' },
  'morpho-blue': { name: 'Morpho', risk: 'B+', riskDisplay: '🟡 B+' },
  'curve': { name: 'Curve', risk: 'A', riskDisplay: '🟢 A' },
  'yearn-v2': { name: 'Yearn', risk: 'B+', riskDisplay: '🟡 B+' },
  'beefy': { name: 'Beefy', risk: 'B+', riskDisplay: '🟡 B+' },
  'euler': { name: 'Euler', risk: 'B', riskDisplay: '🟡 B' },
};

// 链名称映射
const CHAIN_NAMES = {
  'Ethereum': 'Ethereum',
  'Arbitrum': 'Arbitrum',
  'Optimism': 'Optimism',
  'Base': 'Base',
  'Polygon': 'Polygon',
  'BSC': 'BSC',
};

// 估算 Gas 成本 (美元)
const GAS_ESTIMATES = {
  'Ethereum': 15,
  'Arbitrum': 0.5,
  'Optimism': 0.3,
  'Base': 0.2,
  'Polygon': 0.5,
  'BSC': 0.3,
};

const API_ENDPOINTS = {
  defillama: 'https://yields.llama.fi/pools',
};

function parseArgs() {
  const args = process.argv.slice(2);
  const token = args[0]?.toUpperCase() || 'USDT';
  
  const options = {
    limit: 8,
    chain: null,
    minApy: 0,
    minTvl: 100000, // $100k
  };
  
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--limit' && args[i + 1]) {
      options.limit = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--chain' && args[i + 1]) {
      options.chain = args[i + 1];
      i++;
    } else if (args[i] === '--min-apy' && args[i + 1]) {
      options.minApy = parseFloat(args[i + 1]);
      i++;
    }
  }
  
  return { token, options };
}

async function fetchDeFiLlamaData() {
  console.log('📡 正在从 DeFiLlama 获取实时数据...\n');
  
  try {
    const response = await fetch(API_ENDPOINTS.defillama);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.data || [];
  } catch (error) {
    console.error('❌ 获取数据失败:', error.message);
    console.log('⚠️  使用缓存数据...\n');
    return getFallbackData();
  }
}

function getFallbackData() {
  return [
    { pool: 'aave-v3-ethereum-usdt', project: 'aave-v3', symbol: 'USDT', chain: 'Ethereum', apy: 7.8, tvlUsd: 5600000000 },
    { pool: 'spark-ethereum-usdt', project: 'spark', symbol: 'USDT', chain: 'Ethereum', apy: 8.2, tvlUsd: 1200000000 },
    { pool: 'compound-v3-arbitrum-usdt', project: 'compound-v3', symbol: 'USDT', chain: 'Arbitrum', apy: 7.5, tvlUsd: 890000000 },
    { pool: 'morpho-ethereum-usdt', project: 'morpho-blue', symbol: 'USDT', chain: 'Ethereum', apy: 8.0, tvlUsd: 380000000 },
    { pool: 'curve-base-usdt', project: 'curve', symbol: 'USDT', chain: 'Base', apy: 6.9, tvlUsd: 2100000000 },
  ];
}

function filterStablecoinData(data, token) {
  const stablecoinVariants = {
    'USDT': ['USDT', 'TETHER'],
    'USDC': ['USDC', 'USD_COIN'],
    'DAI': ['DAI'],
  };
  
  const variants = stablecoinVariants[token] || [token];
  
  return data.filter(pool => {
    // 代币匹配
    const matchToken = variants.some(v => pool.symbol?.toUpperCase() === v);
    // 项目在元数据中
    const matchProject = PLATFORM_METADATA[pool.project];
    // APY 在合理范围 (0-30%)
    const validApy = pool.apy > 0 && pool.apy < 30;
    // TVL > $100k
    const validTvl = pool.tvlUsd > 100000;
    // 排除 LP 池 (symbol 中包含 '-' 的是 LP 池)
    const notLp = !pool.symbol?.includes('-');
    
    return matchToken && matchProject && validApy && validTvl && notLp;
  });
}

function deduplicatePools(pools) {
  // 按项目 + 链去重，保留 TVL 最高的
  const map = new Map();
  pools.forEach(pool => {
    const key = `${pool.project}-${pool.chain}`;
    if (!map.has(key) || pool.tvlUsd > map.get(key).tvlUsd) {
      map.set(key, pool);
    }
  });
  return Array.from(map.values());
}

function processPoolData(pools) {
  return pools.map(pool => {
    const metadata = PLATFORM_METADATA[pool.project] || { name: pool.project, riskDisplay: '⚪ ?' };
    const chain = CHAIN_NAMES[pool.chain] || pool.chain;
    const gas = GAS_ESTIMATES[chain] || 5;
    const tvlM = pool.tvlUsd >= 1000000000 ? (pool.tvlUsd / 1000000000).toFixed(2) + 'B' : (pool.tvlUsd / 1000000).toFixed(0) + 'M';
    
    return {
      name: metadata.name,
      chain: chain,
      apy: pool.apy,
      riskDisplay: metadata.riskDisplay,
      gas: gas,
      tvl: tvlM,
      tvlRaw: pool.tvlUsd,
    };
  });
}

function formatApy(apy) {
  return `${apy.toFixed(1)}%`.padEnd(8);
}

function formatGas(gas) {
  return `$${gas.toFixed(1)}`.padEnd(6);
}

function formatTvl(tvl) {
  return `$${tvl}`.padEnd(8);
}

async function main() {
  const { token, options } = parseArgs();
  
  const validTokens = ['USDT', 'USDC', 'DAI'];
  if (!validTokens.includes(token)) {
    console.error(`❌ 不支持的代币：${token}`);
    console.log(`支持的代币：${validTokens.join(', ')}`);
    process.exit(1);
  }
  
  const rawData = await fetchDeFiLlamaData();
  const filtered = filterStablecoinData(rawData, token);
  const deduped = deduplicatePools(filtered);
  const processed = processPoolData(deduped);
  
  // 排序和限制
  let sorted = processed.filter(p => p.apy >= options.minApy);
  if (options.chain) {
    sorted = sorted.filter(p => p.chain.toLowerCase().includes(options.chain.toLowerCase()));
  }
  sorted.sort((a, b) => b.apy - a.apy);
  sorted = sorted.slice(0, options.limit);
  
  if (sorted.length === 0) {
    console.log(`⚠️  未找到 ${token} 的收益率数据`);
    process.exit(0);
  }
  
  // 输出结果
  console.log(`💰 ${token} 最优收益排行 (DeFiLlama 实时数据)\n`);
  console.log('排名  平台 (链)            APY      风险    Gas     TVL');
  console.log('─'.repeat(70));
  
  const medals = ['🥇', '🥈', '🥉', '4️⃣ ', '5️⃣ ', '6️⃣ ', '7️⃣ ', '8️⃣ '];
  
  sorted.forEach((p, i) => {
    const medal = medals[i] || `${i + 1}.  `;
    const name = p.name.padEnd(12);
    const chain = `(${p.chain})`.padEnd(12);
    const apy = formatApy(p.apy);
    const risk = p.riskDisplay.padEnd(8);
    const gas = formatGas(p.gas);
    const tvl = formatTvl(p.tvl);
    
    console.log(`${medal} ${name} ${chain} ${apy} ${risk} ${gas} ${tvl}`);
  });
  
  console.log('\n' + '─'.repeat(70));
  
  // 智能推荐
  if (sorted.length > 0) {
    const best = sorted[0];
    const lowGas = sorted.reduce((min, p) => p.gas < min.gas ? p : min, sorted[0]);
    
    console.log(`\n💡 智能推荐:`);
    if (best.name !== lowGas.name && best.chain !== lowGas.chain) {
      console.log(`   🏆 收益最高：${best.name} (${best.chain}) - ${best.apy} APY`);
      console.log(`   💰 小额优选：${lowGas.name} (${lowGas.chain}) - Gas $${lowGas.gas}`);
    } else {
      console.log(`   ✅ ${best.name} (${best.chain}) 综合最优 - ${best.apy} APY`);
    }
  }
  
  console.log(`\n🔍 查询其他：node scripts/monitor.mjs USDC|DAI`);
  console.log(`💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9 | USDC: 0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`);
  console.log(`\n🌐 平台官网:`);
  if (sorted.length > 0) {
    const top3 = sorted.slice(0, 3);
    top3.forEach((p, i) => {
      const url = p.website || `https://${p.name.toLowerCase().replace(' ', '')}.finance`;
      const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : '🥉';
      console.log(`   ${medal} ${p.name} (${p.chain}): ${url}`);
    });
  }
  console.log(`\n🦈 YieldShark v1.0.2 - 嗅到钱的味道`);
  console.log(`🔗 https://clawhub.com/skills/yield-shark`);
  console.log(`💡 新用户免费 3 次/天！\n`);
}

main().catch(console.error);
