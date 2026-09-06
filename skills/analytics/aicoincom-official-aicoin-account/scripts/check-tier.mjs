#!/usr/bin/env node
/**
 * check-tier.mjs — 探测当前 AiCoin API key 覆盖到哪个套餐档位
 *
 * 用法:
 *   node scripts/check-tier.mjs           # 检测当前档位
 *   node scripts/check-tier.mjs verify    # 升级后复测
 *
 * 原理: 串行打 5 个分档代表性 v3 接口，看哪些返回 200、哪些 403，据此推断
 * key 的实际档位。v3 是只读数据 API，没有「查 key 元数据」的接口，所以档位
 * 完全按实测权限推断（不显示到期时间 —— 到期时间请到 aicoin.com/opendata 查）。
 */
import { request } from '../lib/client.mjs';

const TIER_ORDER = ['免费版', '基础版', '标准版', '高级版', '专业版'];

const TIER_PRICES = {
  '免费版': '$0',
  '基础版': '$29/月',
  '标准版': '$79/月',
  '高级版': '$299/月',
  '专业版': '$699/月',
};

const TIER_FEATURES = {
  '基础版': '资金费率、多空比、新闻',
  '标准版': '大单数据、聚合成交、信号',
  '高级版': '清算地图、指标 K 线',
  '专业版': 'AI 分析、企业持仓、加密概念股等全部功能',
};

// 每档一个代表性 v3 接口，用它通不通判断 key 覆盖到哪一档。
const TIER_TESTS = [
  { tier: '免费版', endpoint: 'coins/tickers',                        params: { coin_key: 'bitcoin' }, label: '行情数据' },
  { tier: '基础版', endpoint: 'derivatives/long-short-ratio/summary', params: {}, label: '多空比' },
  { tier: '标准版', endpoint: 'market/big-orders',                    params: { coin_key: 'bitcoin', market: 'binance' }, label: '大单数据' },
  { tier: '高级版', endpoint: 'derivatives/liquidations/map',         params: { coin_key: 'bitcoin', market: 'binance', window: '24h' }, label: '清算地图' },
  { tier: '专业版', endpoint: 'treasuries/summary',                   params: { coin_key: 'bitcoin' }, label: '企业持仓' },
];

async function probe(test) {
  try {
    const { httpStatus, body } = await request('GET', test.endpoint, test.params);
    if (httpStatus === 200 && body && body.ok === true) return '✅ 可用';
    if (httpStatus === 401 || httpStatus === 403) return '❌ 需升级';
    if (httpStatus === 429) return '⚠️ 限流，稍后重测';
    // 鉴权/配额错误个别仍走旧格式塞在 HTTP 200 body 里
    if (body && (body.success === false || (body.error && /403|forbidden|权限|套餐|paywall/i.test(JSON.stringify(body.error))))) {
      return '❌ 需升级';
    }
    return `⚠️ 异常 (HTTP ${httpStatus})`;
  } catch {
    return '⚠️ 网络错误';
  }
}

async function checkTier() {
  const results = [];
  for (const test of TIER_TESTS) {
    results.push({ 套餐: test.tier, 功能: test.label, 状态: await probe(test) });
  }

  // 从低到高推断: 一路 ✅ 就升一档；碰到明确 ❌ 就停（网络错误跳过、继续往上探）
  let currentTier = '免费版';
  for (const test of TIER_TESTS) {
    const r = results.find((x) => x.套餐 === test.tier);
    if (r && r.状态 === '✅ 可用') currentTier = test.tier;
    else if (r && r.状态 === '❌ 需升级') break;
  }

  const idx = TIER_ORDER.indexOf(currentTier);
  const nextTier = idx < TIER_ORDER.length - 1 ? TIER_ORDER[idx + 1] : null;

  const output = { 当前套餐: currentTier, 功能检测: results };
  if (nextTier) {
    output.升级建议 = {
      下一级: `${nextTier} (${TIER_PRICES[nextTier]})`,
      新增功能: TIER_FEATURES[nextTier],
      升级链接: 'https://www.aicoin.com/opendata',
      操作步骤: [
        '1. 打开 https://www.aicoin.com/opendata',
        '2. 登录账号，选择目标套餐并付款',
        '3. 到「API 管理」页面查看 Key（升级后原 Key 自动生效，无需更换）',
        '4. 如果是新 Key，更新 .env 里的 AICOIN_ACCESS_KEY_ID 和 AICOIN_ACCESS_SECRET',
        '5. 运行 node scripts/check-tier.mjs verify 验证升级成功',
      ],
    };
  } else {
    output.状态 = '🎉 已是最高档专业版，全部功能可用。';
  }
  output.安全提示 = 'AiCoin API Key 仅用于获取市场数据，无法交易。密钥仅保存在本地。';
  return output;
}

const action = process.argv[2] || 'check';
const result = await checkTier();
if (action === 'verify') {
  result.验证模式 = true;
  result.说明 = '升级后请确认上方功能检测里对应功能显示 ✅';
}
console.log(JSON.stringify(result, null, 2));
