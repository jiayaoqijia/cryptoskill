import fetch from 'node-fetch';

const DEFI_LLAMA_API = 'https://yields.llama.fi/pools';
const CACHE_TTL = 300000; // 5 minutes

// 支持的代币
const SUPPORTED_TOKENS = ['USDT', 'USDC', 'DAI'];

// 平台配置
const PLATFORMS = {
  'aave-v3': { name: 'Aave V3', risk: 'A', chain: 'multi' },
  'compound-v3': { name: 'Compound V3', risk: 'A+', chain: 'multi' },
  'beefy': { name: 'Beefy', risk: 'B+', chain: 'multi' },
  'curve': { name: 'Curve', risk: 'A', chain: 'multi' },
  'yearn': { name: 'Yearn', risk: 'B+', chain: 'multi' },
};

// 格式化 APY
function formatApy(apy) {
  return apy.toFixed(2) + '%';
}

// 格式化 TVL
function formatTvl(tvl) {
  if (tvl >= 1e9) return '$' + (tvl / 1e9).toFixed(1) + 'B';
  if (tvl >= 1e6) return '$' + (tvl / 1e6).toFixed(0) + 'M';
  if (tvl >= 1e3) return '$' + (tvl / 1e3).toFixed(0) + 'K';
  return '$' + tvl.toFixed(0);
}

// 获取数据
async function fetchData(tokens) {
  console.log('📡 正在从 DeFiLlama 获取实时数据...\n');
  
  const response = await fetch(DEFI_LLAMA_API);
  const result = await response.json();
  const data = result.data || result || [];
  
  return data.filter(pool => {
    const symbol = pool.symbol?.toUpperCase() || '';
    return tokens.some(token => symbol.includes(token));
  }).map(pool => {
    const symbol = pool.symbol?.toUpperCase() || 'UNKNOWN';
    return {
      pool: pool.pool,
      project: pool.project,
      chain: pool.chain,
      symbol: symbol,
      apy: pool.apy || 0,
      tvlUsd: pool.tvlUsd || 0,
      apyBase: pool.apyBase || 0,
      apyReward: pool.apyReward || 0,
    };
  });
}

// 处理数据
function processData(data) {
  return data
    .filter(item => {
      // 过滤掉 LP 池
      if (item.symbol.includes('-') || item.symbol.includes('/')) return false;
      // 过滤掉 TVL 太小的
      if (item.tvlUsd < 100000) return false;
      // 过滤掉 APY 异常的
      if (item.apy > 100 || item.apy < 0) return false;
      return true;
    })
    .map(item => ({
      ...item,
      displayName: PLATFORMS[item.project]?.name || item.project,
      risk: PLATFORMS[item.project]?.risk || 'B',
    }))
    .sort((a, b) => b.apy - a.apy);
}

// 显示对比
function displayComparison(data, limit = 10) {
  if (!data || data.length === 0) {
    console.log('❌ 未找到符合条件的数据\n');
    return;
  }
  
  console.log('💰 多代币收益对比 (DeFiLlama 实时数据)\n');
  console.log('代币  平台 (链)            APY      风险    TVL');
  console.log('─'.repeat(70));
  
  data.slice(0, limit).forEach((item, i) => {
    const token = (item.symbol || 'UNK').padEnd(6);
    const name = (item.displayName || item.project || 'Unknown').toString().padEnd(12);
    const chain = `(${item.chain || 'Unknown'})`.padEnd(12);
    const apy = formatApy(item.apy || 0);
    const risk = (item.risk || 'B').padEnd(5);
    const tvl = formatTvl(item.tvlUsd || 0);
    
    console.log(`${token} ${name} ${chain} ${apy} ${risk} ${tvl}`);
  });
  
  console.log('─'.repeat(70) + '\n');
  
  // 按代币分组显示最优
  console.log('🏆 各代币最优收益:\n');
  
  const tokens = [...new Set(data.map(item => item.symbol).filter(Boolean))];
  tokens.forEach(token => {
    const best = data.find(item => item.symbol === token);
    if (best) {
      console.log(`   ${token}: ${best.displayName || best.project} (${best.chain}) - ${formatApy(best.apy)} 🟢 ${best.risk}`);
    }
  });
  
  console.log('\n🔍 查询单个代币：node scripts/compare.mjs --token USDT');
  console.log('💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9 | USDC: 0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44');
  console.log('\n🦈 YieldShark v1.0.3 - 嗅到钱的味道');
  console.log('🔗 https://clawhub.com/skills/yield-shark');
  console.log('💡 新用户免费 3 次/天！\n');
}

async function main() {
  const args = process.argv.slice(2);
  let tokens = SUPPORTED_TOKENS;
  
  // 支持自定义代币
  const tokenIndex = args.indexOf('--tokens');
  if (tokenIndex !== -1 && args[tokenIndex + 1]) {
    tokens = args[tokenIndex + 1].toUpperCase().split(',');
  }
  
  const limitIndex = args.indexOf('--limit');
  const limit = limitIndex !== -1 ? parseInt(args[limitIndex + 1]) : 10;
  
  const data = await fetchData(tokens);
  const processed = processData(data);
  displayComparison(processed, limit);
}

main().catch(console.error);
