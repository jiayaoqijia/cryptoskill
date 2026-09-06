#!/usr/bin/env node
// 订单形状黄金矩阵 —— 用 ccxt createOrderRequest(只建请求体、不下单、不需 API key)断言每家交易所
// 把 coinos 传的参数映射成"正确的 native 订单",ccxt 版本/交易所行为一漂移立刻变红。
//
// 为什么需要它: 7 家交易所的条件单/algo/止盈止损/方向参数是动态长尾,ccxt 是 leaky abstraction。
// 这个矩阵把"人工审查 + 实测一次"固化成可重复的门禁 —— 升级 ccxt 或周期性跑,FAIL 即说明某家行为变了。
//
// 用法: node scripts/verify-order-matrix.mjs   (需要能连交易所; 走 HTTPS_PROXY/PROXY_URL 环境变量)
// 退出码: 0 = 全部符合黄金预期; 1 = 有漂移(请核对并更新 GOLDEN 或修 coinos)。
// 注意: 这验证的是"请求体形状"(下单前), 不验证服务器端真实成交 —— 后者靠每所小额实盘 smoke。

import ccxt from 'ccxt';

const PROXY = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy;

// 触发信号(由 7 家 createOrderRequest 实测归纳;与 exchange.mjs placeOrder 安全网同源)。
// 出现任一 = ccxt 把它当成了真条件单; 全无 = 触发价被静默丢弃(会变立即单, 危险)。
const TRIGGER_SIGNALS = ['trigger', 'stopprice', 'sltriggerpx', 'tptriggerpx', 'plantype', 'algotype', 'callback', 'trailing', 'conditional', 'move_order_stop', 'formula_price', 'stop_market', 'take_profit', 'activationprice'];
const hasTrigger = (req) => { const s = JSON.stringify(req).toLowerCase(); return TRIGGER_SIGNALS.some((x) => s.includes(x)); };

// 黄金预期: 每家 × 条件单类型 → 是否应被 ccxt 当成真条件单(true)还是统一参数下不出(false=coinos 安全网会拒)。
// 实测自 2026-06-09 ccxt 4.5.47。改这张表前先确认是 ccxt 真变好/变坏, 不是手滑。
// 实测自 2026-06-09 ccxt 4.5.47: 7 家都把 stopLossPrice/takeProfitPrice/triggerPrice 映射成各自的 native
// 条件单(binance STOP_MARKET / okx conditional / bybit trigger / bitget plan / gate trigger 对象 /
// htx sl_trigger_price)。trailing 各所参数名不同(callbackRate / trailingPercent / trailingTriggerPrice)。
const GOLDEN = {
  binance:     { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  okx:         { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  bybit:       { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  bitget:      { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  gate:        { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  htx:         { stopLoss: true, takeProfit: true, trigger: true, trailing: true },
  // Hyperliquid 不纳入严格矩阵: USDC 结算的边角所(多数流程路由到 aicoin-onchain),且其 ccxt
  // createOrderRequest 对这些参数形状会内部报错(非可靠信号)。HL 的条件单支持以实盘 smoke 为准。
};

// 方向断言(防 hedge 平仓变反向开仓的回归): 对会翻向的所(bitget/htx), 平多单经 hedge 参数必须出 close 信号。
const DIR_GOLDEN = {
  bitget: { params: { reduceOnly: true, hedged: true }, mustInclude: 'tradeside":"close', desc: 'hedge 平多 → tradeSide:Close(不是 Open)' },
  htx:    { params: { reduceOnly: true, hedged: true }, mustInclude: '"offset":"close', desc: 'hedge 平多 → offset:close' },
};

function pickSwapSymbol(ex) {
  // HL 用 USDC 结算(BTC/USDC:USDC), 其它多为 USDT。
  for (const s of ['DOGE/USDT:USDT', 'ETH/USDT:USDT', 'BTC/USDT:USDT', 'ETH/USDC:USDC', 'BTC/USDC:USDC', 'SOL/USDC:USDC']) if (ex.markets[s]) return s;
  return Object.keys(ex.markets).find((s) => typeof s === 'string' && ex.markets[s] && ex.markets[s].swap && (s.endsWith(':USDT') || s.endsWith(':USDC')));
}

function build(ex, sym, type, side, price, params) {
  const fn = typeof ex.createOrderRequest === 'function' ? 'createOrderRequest'
    : typeof ex.createContractOrderRequest === 'function' ? 'createContractOrderRequest' : null;
  if (!fn) return { _err: 'no request builder' };
  try { return ex[fn](sym, type, side, 100, price, params); } catch (e) { return { _err: `${e.constructor.name}: ${e.message.slice(0, 60)}` }; }
}

async function main() {
  let failed = 0;
  const rows = [];
  for (const id of Object.keys(GOLDEN)) {
    const g = GOLDEN[id];
    let ex, sym, last;
    try {
      ex = new ccxt[id]({ timeout: 25000, ...(PROXY ? { httpProxy: PROXY } : {}), options: { defaultType: 'swap' } });
      ex.has.fetchCurrencies = false;
      await ex.loadMarkets();
      sym = pickSwapSymbol(ex);
      last = (await ex.fetchTicker(sym)).last;
    } catch (e) {
      rows.push(`${id.padEnd(12)} ⏭  跳过(连不上/无市场): ${e.message.slice(0, 60)}`);
      continue;
    }
    const dn = last * 0.9, up = last * 1.1;
    // Hyperliquid 市价单需参考价(coinos placeOrder 已补; 矩阵也补,才能反映真实行为)。
    const mp = id === 'hyperliquid' ? last : undefined;
    const cases = [
      ['stopLoss', () => build(ex, sym, 'market', 'sell', mp, { stopLossPrice: dn })],
      ['takeProfit', () => build(ex, sym, 'market', 'sell', mp, { takeProfitPrice: up })],
      ['trigger', () => build(ex, sym, 'market', 'buy', mp, { triggerPrice: up, triggerDirection: 'ascending' })],
      ['trailing', () => build(ex, sym, 'market', 'sell', mp, { trailingPercent: 1, trailingTriggerPrice: last })],
    ];
    for (const [name, fn] of cases) {
      const req = fn();
      const got = req._err ? false : hasTrigger(req);
      const want = g[name];
      const ok = got === want;
      if (!ok) failed++;
      rows.push(`${id.padEnd(12)} ${name.padEnd(11)} ${ok ? '✅' : '❌'} 期望${want ? '支持' : '不支持'}/实际${got ? '支持' : '不支持'}${req._err ? ' (' + req._err + ')' : ''}`);
    }
    // 方向回归断言
    if (DIR_GOLDEN[id]) {
      const d = DIR_GOLDEN[id];
      const req = build(ex, sym, 'market', 'sell', undefined, d.params);
      const s = JSON.stringify(req).toLowerCase();
      const ok = !req._err && s.includes(d.mustInclude);
      if (!ok) failed++;
      rows.push(`${id.padEnd(12)} ${'dir-close'.padEnd(11)} ${ok ? '✅' : '❌'} ${d.desc}${req._err ? ' (' + req._err + ')' : ''}`);
    }
  }
  console.log('订单形状黄金矩阵(ccxt createOrderRequest, 仅请求体)');
  console.log('-'.repeat(72));
  for (const r of rows) console.log(r);
  console.log('-'.repeat(72));
  console.log('注: Hyperliquid 为 USDC 边角所(多走 aicoin-onchain),不纳入严格矩阵,条件单支持以实盘 smoke 为准。');
  if (failed) {
    console.log(`\n❌ ${failed} 项与黄金预期不符 —— ccxt 行为可能变了。核对后更新 GOLDEN 或修 exchange.mjs(尤其安全网/closeParamsFor)。`);
    process.exit(1);
  }
  console.log('\n✅ 全部符合黄金预期(6 家 CEX 的条件单映射 + bitget/htx hedge 平仓方向未漂移)。');
}

main().catch((e) => { console.error('matrix error:', e.message); process.exit(2); });
