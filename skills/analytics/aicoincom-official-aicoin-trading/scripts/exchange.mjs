#!/usr/bin/env node
// CCXT Exchange Trading CLI
// Requires: npm install ccxt
import { cli } from '../lib/cli.mjs';
import { loadEnv, writeEnvPath } from '../lib/env-loader.mjs';
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync, unlinkSync, mkdirSync, chmodSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dir = dirname(fileURLToPath(import.meta.url));

// .env auto-load (宿主可能不向子进程注入 env)。共享 loader,见 lib/env-loader.mjs。
loadEnv();

// pionex 在当前 ccxt 版本无实现 → 不列入可交易所(REFERRALS 仍保留作注册引流)。getExchange 另有兜底。
const SUPPORTED = ['binance','okx','bybit','bitget','gate','htx','hyperliquid'];

// AiCoin referral links — shown in exchanges list and missing-key errors
const REFERRALS = {
  okx:         { name: 'OKX',         code: 'aicoin20',  benefit: '永久返20%手续费', link: 'https://jump.do/zh-Hans/xlink-proxy?id=2' },
  binance:     { name: 'Binance',     code: 'aicoin668', benefit: '返10% + $500',   link: 'https://jump.do/zh-Hans/xlink-proxy?id=3' },
  bitget:      { name: 'Bitget',      code: 'hktb3191',  benefit: '返10%手续费',     link: 'https://jump.do/zh-Hans/xlink-proxy?id=6' },
  htx:         { name: 'HTX',         code: 'j2us6223',  benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=4' },
  gate:        { name: 'Gate.io',     code: 'AICOINGO',  benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=5' },
  bybit:       { name: 'Bybit',       code: '34429',     benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=15' },
  pionex:      { name: 'Pionex',      code: '4vgi0zUF',  benefit: '',               link: 'https://www.pionex.com/zh-CN/signUp?r=4vgi0zUF' },
  hyperliquid: { name: 'Hyperliquid', code: 'AICOIN88',  benefit: '返4%手续费',      link: 'https://app.hyperliquid.xyz/join/AICOIN88' },
};

const SECURITY_NOTICE = '⚠️ AiCoin API Key 与交易所 API Key 是完全独立的两套密钥：(1) AiCoin API Key 仅用于获取市场数据（行情、K线、资金费率等），无法进行任何交易操作，也无法读取你在交易所的任何信息。(2) 交易所 API Key 需要单独到各交易所后台申请和授权。(3) 所有密钥仅保存在本地设备 .env 文件中，不会上传到任何服务器。';

// AiCoin broker tags — ensures orders are attributed to AiCoin, not CCXT default
const BROKER_CONFIG = {
  binance: {
    options: { broker: { spot: 'x-MGFCMH4U', margin: 'x-MGFCMH4U', future: 'x-FaeSBrMa', swap: 'x-FaeSBrMa', delivery: 'x-FaeSBrMa' } },
  },
  okx: {
    options: { brokerId: 'c6851dd5f01e4aBC' },
  },
  bybit: {
    options: { brokerId: 'AiCoin' },
  },
  bitget: {
    options: { broker: 'tpequ' },
  },
  gate: {
    headers: { 'X-Gate-Channel-Id': 'AiCoin1' },
  },
  htx: {
    options: { broker: { id: 'AAf0e4f2ef' } },
  },
};

async function getExchange(id, marketType, skipAuth = false) {
  let ccxt;
  try {
    ccxt = await import('ccxt');
  } catch {
    // Auto-install ccxt if missing
    try {
      execSync('npm install --omit=dev', { cwd: resolve(__dir, '..'), stdio: 'pipe', timeout: 60000 });
      ccxt = await import('ccxt');
    } catch {
      throw new Error('ccxt not installed. Run: cd <skill-dir>/aicoin && npm install');
    }
  }
  const opts = {};
  if (!skipAuth) {
    if (id === 'hyperliquid') {
      // HL 用钱包签名,不是 api_key/secret: walletAddress=主钱包(查余额/持仓), privateKey=API钱包(agent)私钥(签单)。
      opts.walletAddress = process.env.HYPERLIQUID_WALLET_ADDRESS || process.env.HYPERLIQUID_MAIN_WALLET || '';
      opts.privateKey = process.env.HYPERLIQUID_PRIVATE_KEY || '';
      if (!opts.walletAddress || !opts.privateKey) {
        const ref = REFERRALS.hyperliquid || {};
        throw new Error(
          `未配置 Hyperliquid 钱包凭证。HL 用钱包签名(非 api key):需要主钱包地址 + API 钱包私钥。` +
          (ref.link ? `\n注册 HL(AiCoin 返佣):${ref.link} 邀请码 ${ref.code}` : '') +
          `\n配置:让 AI 用 save_key({"exchange":"hyperliquid","wallet_address":"0x主钱包","private_key":"0xAPI钱包私钥"}),写进 ~/.coinos/.env、chmod 600、不回显。` +
          `\n⚠️ 务必用 HL「API 钱包/agent wallet」私钥(可在 HL 后台单独授权与撤销),绝不要用主钱包私钥。\n${SECURITY_NOTICE}`
        );
      }
    } else {
      const pre = id.toUpperCase();
      opts.apiKey = process.env[`${pre}_API_KEY`];
      opts.secret = process.env[`${pre}_API_SECRET`] || process.env[`${pre}_SECRET`];
      if (process.env[`${pre}_PASSWORD`] || process.env[`${pre}_PASSPHRASE`]) {
        opts.password = process.env[`${pre}_PASSWORD`] || process.env[`${pre}_PASSPHRASE`];
      }
      if (!opts.apiKey) {
        const ref = REFERRALS[id] || {};
        throw new Error(
          `未配置 ${ref.name || id} 交易所 API Key。` +
          (ref.link ? `\n注册${ref.name}（AiCoin专属优惠）：${ref.link}\n邀请码：${ref.code}${ref.benefit ? '，' + ref.benefit : ''}` : '') +
          `\n配置方法：把 key 放进 ~/.coinos/.env（${pre}_API_KEY=xxx / ${pre}_API_SECRET=xxx），或让 AI 用 save_key 动作代写（自动 chmod 600、不回显）。` +
          `\n${SECURITY_NOTICE}`
        );
      }
    }
  }
  // Proxy support: PROXY_URL (MCP-compatible) or HTTPS_PROXY/HTTP_PROXY
  const proxyUrl = process.env.PROXY_URL
    || process.env.HTTPS_PROXY || process.env.https_proxy
    || process.env.HTTP_PROXY || process.env.http_proxy
    || process.env.ALL_PROXY || process.env.all_proxy;
  if (proxyUrl) {
    if (proxyUrl.startsWith('socks')) {
      let socksUrl = proxyUrl;
      if (socksUrl.startsWith('socks5://')) socksUrl = socksUrl.replace('socks5://', 'socks5h://');
      else if (socksUrl.startsWith('socks4://')) socksUrl = socksUrl.replace('socks4://', 'socks4a://');
      opts.socksProxy = socksUrl;
    } else if (proxyUrl.startsWith('https://')) {
      opts.httpsProxy = proxyUrl;
    } else {
      opts.httpProxy = proxyUrl;
    }
  }
  // Set market type
  if (marketType && marketType !== 'spot') {
    opts.options = { ...(opts.options || {}), defaultType: marketType };
  }
  // Apply AiCoin broker tags (overrides CCXT defaults)
  const brokerCfg = BROKER_CONFIG[id];
  if (brokerCfg) {
    if (brokerCfg.options) {
      opts.options = { ...(opts.options || {}), ...brokerCfg.options };
    }
    if (brokerCfg.headers) {
      opts.headers = { ...(opts.headers || {}), ...brokerCfg.headers };
    }
  }
  const Ex = ccxt.default?.[id] || ccxt[id];
  if (typeof Ex !== 'function') {
    // 防 `Ex is not a constructor` 裸崩 —— 交易所在当前 ccxt 版本无实现(如旧版没有的所、或拼写错)。
    const avail = (ccxt.exchanges || []).filter((e) => SUPPORTED.includes(e)).join(', ');
    throw new Error(`交易所 "${id}" 在当前 ccxt 版本中不可用。当前支持: ${avail || SUPPORTED.join(', ')}。`);
  }
  return new Ex(opts);
}

// createOrder 兜底各所"账户配置相关"的方向/参数差异(ccxt 只翻译不替你判断该传什么)。
// 处理: OKX 单向 posSide、币安/Bybit 双向(hedge)缺方向参数、Hyperliquid 市价需参考价。
async function placeOrder(ex, symbol, type, side, amount, price, params, exchange, marketType) {
  const p = { ...(params || {}) };
  const isSwap = marketType && marketType !== 'spot';
  const isOkxSwap = exchange === 'okx' && isSwap;
  const isBinanceSwap = exchange === 'binance' && isSwap;
  const isBybitSwap = exchange === 'bybit' && isSwap;

  // Hyperliquid 市价单需要参考价算滑点 —— ccxt 对 market + price 缺失直接 ArgumentsRequired,
  // 导致 HL 上 create_order/close_position/set_stop 全失败。用现价喂给 ccxt(它按默认滑点转 IOC 限价)。
  if (exchange === 'hyperliquid' && type === 'market' && (price == null || price === '')) {
    try { const t = await ex.fetchTicker(symbol); price = t.last ?? t.close ?? t.mark; } catch {}
    if (price == null) throw new Error(`Hyperliquid 市价单需要参考价(算滑点上限),但取不到 ${symbol} 现价,请稍后重试。`);
  }

  // 仅给"开/加仓"单(非 reduceOnly)自动补 posSide。OKX 双向平仓由 closeParamsFor 显式给 posSide;
  // OKX 单向(net)不该带 posSide(早先无条件猜会让 net 平仓单先必失败再 retry,无幂等键有重复挂单风险)。
  if (isOkxSwap && !p.posSide && !p.reduceOnly) {
    p.posSide = side === 'buy' ? 'long' : 'short';
  }
  // ── 条件单安全网(fail-safe)──
  // 调用方传了触发价意图(止盈止损/触发单/追踪),但该所 ccxt 没把它映射成真条件单时,拒绝下单。
  // 实测 Gate / HTX 的 stopLossPrice/takeProfitPrice 经 ccxt 映射成**空**(触发价被静默丢弃)→ 会被
  // 当成"立即市价单"下出去(止损瞬间变成立即成交)。这比"不支持"更危险,必须在下单前拦下。
  const TRIGGER_INTENT = ['stopLossPrice', 'takeProfitPrice', 'triggerPrice', 'stopPrice', 'trailingPercent', 'callbackRate', 'trailingTriggerPrice'];
  if (TRIGGER_INTENT.some((k) => p[k] != null) && typeof ex.createOrderRequest === 'function') {
    let req = null;
    try { req = ex.createOrderRequest(symbol, type, side, amount, price, p); } catch { /* 构建报错则放行,真调用会抛同样的错 */ }
    if (req) {
      const s = JSON.stringify(req).toLowerCase();
      // 各所 native 触发信号(由 7 家 createOrderRequest 实测归纳): binance type=STOP*/TAKE_PROFIT*/TRAILING*、
      // okx ordType=conditional/trigger/move_order_stop+slTriggerPx/tpTriggerPx、bybit triggerPrice、
      // bitget planType、htx trigger_type/formula_price、通用 stopPrice/callbackRate/trailing。
      const SIGNALS = ['trigger', 'stopprice', 'sltriggerpx', 'tptriggerpx', 'plantype', 'algotype', 'callback', 'trailing', 'conditional', 'move_order_stop', 'formula_price', 'stop_market', 'take_profit', 'activationprice'];
      if (!SIGNALS.some((sig) => s.includes(sig))) {
        throw new Error(`${exchange} 无法把这种条件单(止盈止损/触发/追踪)通过统一参数下出 —— 触发价会被静默丢弃、变成立即成交的市价单。已拒绝下单以防误成交。请改用支持的交易所(Binance/OKX/Bybit/Bitget),或到交易所端手动挂条件单。`);
      }
    }
  }
  try {
    return await ex.createOrder(symbol, type, side, amount, price, p);
  } catch (e) {
    const errMsg = String(e);
    // OKX net mode 不接受 posSide → 删掉重试(仅 OKX swap 且确是 posSide 报错;不在 spot retry)。
    if (isOkxSwap && p.posSide && errMsg.includes('posSide')) {
      delete p.posSide;
      return await ex.createOrder(symbol, type, side, amount, price, p);
    }
    // 币安双向(hedge): 缺 positionSide 报 -4061(下单前硬拒绝、订单未入场、retry 无重复成交风险)。
    //   开/加仓: buy→LONG / sell→SHORT。
    //   reduceOnly 平仓单(如 auto-trade 的裸 SL/TP): hedge 不接受 reduceOnly,删掉它并按"平的哪侧仓"补
    //   positionSide —— 平多(sell)挂 LONG、平空(buy)挂 SHORT(与开仓相反)。
    if (isBinanceSwap && !p.positionSide
        && (errMsg.includes('-4061') || errMsg.includes('position side does not match'))) {
      if (p.reduceOnly) { delete p.reduceOnly; p.positionSide = side === 'buy' ? 'SHORT' : 'LONG'; }
      else p.positionSide = side === 'buy' ? 'LONG' : 'SHORT';
      return await ex.createOrder(symbol, type, side, amount, price, p);
    }
    // Bybit 双向(hedge): 缺 positionIdx 报 10001 "position idx not match position mode"。
    //   开/加仓: buy→1(多)/ sell→2(空)。reduceOnly 平仓单按平的哪侧: 平多(sell)→1、平空(buy)→2。
    //   Bybit reduceOnly 可与 positionIdx 共存,保留 reduceOnly。同属下单前硬拒绝,retry 安全。
    if (isBybitSwap && p.positionIdx == null
        && (errMsg.includes('10001') || /position idx/i.test(errMsg) || /position mode/i.test(errMsg))) {
      p.positionIdx = p.reduceOnly ? (side === 'buy' ? 2 : 1) : (side === 'buy' ? 1 : 2);
      return await ex.createOrder(symbol, type, side, amount, price, p);
    }
    throw e;
  }
}

// 根据"真实持仓 + 交易所"推导平仓/减仓单该带的方向参数 —— 这是平仓/止损类操作防"反向单"和
// "hedge 模式 reduceOnly 被拒"的安全底线。方向只取自交易所返回的真实持仓 (pos.info),绝不靠
// agent 传的 side 猜。各所规则不同:
//   - 币安双向 (hedge): 必须带 positionSide=LONG/SHORT,且**不能**带 reduceOnly
//     (币安在 hedge 模式收到 reduceOnly 会直接拒单 → 这正是 close_position 早期"返回异常"的根因)。
//   - 币安单向 (positionSide=BOTH 或缺省) / 多数交易所: reduceOnly:true。
//   - OKX 双向: posSide=long/short + reduceOnly;单向 (net): 只给 reduceOnly,
//     posSide 交给 placeOrder 的 OKX 兜底逻辑 + 51000 重试处理。
//   - Bybit 双向: positionIdx 1=多/2=空 + reduceOnly;单向 (0): reduceOnly。
function closeParamsFor(exchange, marketType, pos) {
  const out = {};
  if (!marketType || marketType === 'spot') return out;
  const info = pos?.info || {};
  if (exchange === 'binance') {
    const ps = String(info.positionSide || '').toUpperCase();
    if (ps === 'LONG' || ps === 'SHORT') out.positionSide = ps; // hedge: 带 positionSide,不带 reduceOnly
    else out.reduceOnly = true;                                 // one-way
    return out;
  }
  if (exchange === 'okx') {
    out.reduceOnly = true;
    const ps = String(info.posSide || '').toLowerCase();
    if (ps === 'long' || ps === 'short') out.posSide = ps;
    return out;
  }
  if (exchange === 'bybit') {
    out.reduceOnly = true;
    const idx = info.positionIdx != null ? Number(info.positionIdx) : null;
    if (idx === 1 || idx === 2) out.positionIdx = idx;
    return out;
  }
  // Bitget 双向: reduceOnly 在 hedge 被忽略,裸 side 单=反向开仓(ccxt #17817 实锤)。必须 hedged:true,
  // ccxt 才翻 side + tradeSide:Close(实证: {reduceOnly:true,hedged:true}+sell → {side:buy,tradeSide:Close}=平多;
  // SL → holdSide:long 护多)。检测靠 pos.hedged(ccxt 据 posMode/holdMode 可靠填);模式完全测不出时**拒绝**,
  // 绝不退回裸 reduceOnly(那会让隐藏的 hedge 账户反向开仓)。
  if (exchange === 'bitget') {
    const pm = String(info.posMode || info.holdMode || '').toLowerCase();
    const isHedge = pos?.hedged === true || pm === 'hedge_mode';
    const isOneWay = pos?.hedged === false || pm === 'one_way_mode';
    if (isHedge) { out.hedged = true; out.reduceOnly = true; }
    else if (isOneWay) { out.reduceOnly = true; }
    else throw new Error('无法确定 Bitget 持仓模式(单向/双向)。为防双向账户被误当反向开仓,已中止 —— 请重试或在交易所核对持仓模式后再平。');
    return out;
  }
  // HTX 双向(dual_side): 平仓靠 offset 不靠 reduce_only;ccxt 仅在 hedged:true 时写 offset,offset 由
  // reduceOnly 决定(实证: {reduceOnly:true,hedged:true}+sell → offset:close=平多;漏 reduceOnly → offset:open=反向)。
  // pos.hedged 在 htx 永远 undefined,只能读 info.position_mode。测不出退 reduceOnly(若实为双向会缺 offset 被拒=fail-safe)。
  if (exchange === 'htx' || exchange === 'huobi' || exchange === 'huobipro') {
    out.reduceOnly = true;
    if (String(info.position_mode || '').toLowerCase() === 'dual_side') out.hedged = true;
    return out;
  }
  out.reduceOnly = true;
  return out;
}

// 查"条件/算法单"(止盈止损/触发/追踪),合并各 ordType 再去重 —— OKX 的止盈止损是 conditional 类,
// 与 trigger 类**分开存**,必须各类都查再合并,不能"第一次返回空就 return"(否则 OKX 的 set_stop
// 单会被漏掉:实测 stop_orders 旧逻辑先查 trigger 返回空就 return,读不到 conditional 类的 SL/TP)。
async function fetchConditionalOrders(ex, exchange, symbol) {
  const variants = [{ trigger: true }, { stop: true }];
  if (exchange === 'okx') variants.push({ ordType: 'conditional' }, { ordType: 'oco' }, { ordType: 'trigger' }, { ordType: 'move_order_stop' });
  const seen = new Map();
  let any = false, lastErr = null;
  for (const extra of variants) {
    try {
      const os = await ex.fetchOpenOrders(symbol, undefined, undefined, extra);
      any = true;
      for (const o of (os || [])) if (o && o.id != null) seen.set(o.id, o);
    } catch (e) { lastErr = e; }
  }
  if (!any) throw lastErr || new Error('无法查询条件单');
  return [...seen.values()];
}

cli({
  exchanges: async () => ({
    supported: SUPPORTED.map(id => {
      const ref = REFERRALS[id] || {};
      return { exchange: id, name: ref.name || id, register_link: ref.link || '', invite_code: ref.code || '', benefit: ref.benefit || '' };
    }),
    security_notice: SECURITY_NOTICE,
  }),
  register: async ({ exchange: exName }) => {
    if (!exName) return { exchanges: Object.keys(REFERRALS), usage: 'node exchange.mjs register \'{"exchange":"okx"}\'' };
    const key = exName.toLowerCase().replace(/[.\s]/g, '');
    const ALIASES = { 币安: 'binance', 火币: 'htx', 派网: 'pionex', hl: 'hyperliquid', gateio: 'gate' };
    const id = ALIASES[key] || key;
    const ref = REFERRALS[id];
    if (!ref) return { error: `不支持 ${exName}`, supported: Object.keys(REFERRALS) };
    return {
      exchange: ref.name, invite_code: ref.code, benefit: ref.benefit || '无额外优惠', register_link: ref.link,
      steps: ['打开注册链接', '选择手机或邮箱注册', '填入验证码、设置密码', '完成身份验证(KYC)', '如需API交易，到API管理创建key，配置到.env'],
      security_notice: SECURITY_NOTICE,
    };
  },
  // 本地 host 模式: 用户在 chat 里给了交易所 key 时, 把它写进规范位置 ~/.coinos/.env
  // (chmod 600), 绝不把 secret 回显。容器内有 web UI EnvSection, 不该走这个动作。
  save_key: async ({ exchange, api_key, api_secret, secret, password, passphrase, wallet_address, private_key }) => {
    if (!exchange) throw new Error('需要 exchange，例: {"exchange":"binance","api_key":"...","api_secret":"..."}');
    const id = exchange.toLowerCase().replace(/[.\s]/g, '');
    const pre = id.toUpperCase();
    const target = writeEnvPath();
    let lines = [];
    try { lines = readFileSync(target, 'utf-8').split('\n'); } catch { /* 文件还不存在 */ }
    const set = (key, val) => {
      const i = lines.findIndex(l => l.trim().startsWith(key + '='));
      if (i >= 0) lines[i] = `${key}=${val}`; else lines.push(`${key}=${val}`);
    };
    const flush = () => {
      try { mkdirSync(dirname(target), { recursive: true }); } catch {}
      writeFileSync(target, lines.join('\n').replace(/\n*$/, '\n'));
      try { chmodSync(target, 0o600); } catch {}
    };

    // Hyperliquid: 钱包签名模式(非 api key)。wallet_address=主钱包, private_key=API钱包(agent)私钥。
    if (id === 'hyperliquid') {
      const w = wallet_address || api_key;          // 容错: 误用 api_key 传地址
      const pk = private_key || api_secret || secret; // 容错: 误用 api_secret 传私钥
      if (!w || !pk) throw new Error('Hyperliquid 需要 wallet_address(主钱包地址) 和 private_key(API钱包/agent 私钥)');
      set('HYPERLIQUID_WALLET_ADDRESS', w);
      set('HYPERLIQUID_PRIVATE_KEY', pk);
      flush();
      return {
        saved: true, exchange: id, env_file: target, keys_written: ['HYPERLIQUID_WALLET_ADDRESS', 'HYPERLIQUID_PRIVATE_KEY'],
        _security: '私钥已写入并 chmod 600,未回显。⚠️ HL 私钥能签所有交易 —— 务必用 HL「API 钱包/agent wallet」私钥(可在 HL 后台单独授权与随时撤销),绝不要用主钱包私钥;明文已留在本次对话记录里,在意就去 HL 重新授权一个 agent。',
        next: `已就绪,可直接查: node scripts/exchange.mjs balance '{"exchange":"hyperliquid"}'`,
      };
    }

    const k = api_key;
    const s = api_secret || secret;
    const p = password || passphrase;
    if (!k || !s) throw new Error('需要 api_key 和 api_secret(OKX/Bitget 还需 password/passphrase;Hyperliquid 用 wallet_address + private_key)');
    set(`${pre}_API_KEY`, k);
    set(`${pre}_API_SECRET`, s);
    if (p) set(`${pre}_PASSWORD`, p);
    flush();
    const written = [`${pre}_API_KEY`, `${pre}_API_SECRET`].concat(p ? [`${pre}_PASSWORD`] : []);
    return {
      saved: true, exchange: id, env_file: target, keys_written: written,
      _security: 'secret 已写入并 chmod 600，未回显。注意：你刚在 chat 里发的明文 key 会留在对话记录里，在意可去交易所后台重新生成。强烈建议只勾「读取」权限、绑定 IP 白名单、不要开提现。',
      next: `已就绪，可直接查: node scripts/exchange.mjs balance '{"exchange":"${id}"}'`,
    };
  },
  markets: async ({ exchange, market_type, base, quote, limit = 100 }) => {
    const ex = await getExchange(exchange, market_type, true);
    await ex.loadMarkets();
    let m = Object.values(ex.markets).map(x => ({
      symbol: x.symbol, base: x.base, quote: x.quote, type: x.type, active: x.active,
      contractSize: x.contractSize || null,
      limits: x.limits || null,
      precision: x.precision || null,
    }));
    if (market_type) m = m.filter(x => x.type === market_type);
    if (base) m = m.filter(x => x.base === base.toUpperCase());
    if (quote) m = m.filter(x => x.quote === quote.toUpperCase());
    return m.slice(0, limit);
  },
  ticker: async ({ exchange, symbol, symbols, market_type }) => {
    const ex = await getExchange(exchange, market_type, true);
    if (symbol) return ex.fetchTicker(symbol);
    return ex.fetchTickers(symbols);
  },
  orderbook: async ({ exchange, symbol, market_type, limit }) => {
    const ex = await getExchange(exchange, market_type, true);
    return ex.fetchOrderBook(symbol, limit);
  },
  trades: async ({ exchange, symbol, market_type, limit }) => {
    const ex = await getExchange(exchange, market_type, true);
    return ex.fetchTrades(symbol, undefined, limit);
  },
  ohlcv: async ({ exchange, symbol, market_type, timeframe = '1h', limit }) => {
    const ex = await getExchange(exchange, market_type, true);
    return ex.fetchOHLCV(symbol, timeframe, undefined, limit);
  },
  balance: async ({ exchange, market_type, show_dust }) => {
    const ex = await getExchange(exchange, market_type);
    const bal = await ex.fetchBalance();
    // Return only non-zero balances for cleaner output
    const summary = {};
    for (const [ccy, amt] of Object.entries(bal.total || {})) {
      const total = Number(amt);
      if (total <= 0) continue;
      // Filter dust tokens (< $0.01 equivalent) unless show_dust is set
      // Stablecoins check: if < 0.01, it's dust
      const isStable = ['USDT','USDC','BUSD','DAI','TUSD','FDUSD'].includes(ccy);
      if (!show_dust && isStable && total < 0.01) continue;
      if (!show_dust && !isStable && total < 1e-7) continue;
      summary[ccy] = { free: bal.free[ccy], used: bal.used[ccy], total: bal.total[ccy] };
    }
    // OKX unified account note
    if (exchange === 'okx') {
      summary._note = 'OKX统一账户：现货和合约共用同一余额，无需划转。';
    }
    return summary;
  },
  positions: async ({ exchange, symbols, market_type }) => {
    const ex = await getExchange(exchange, market_type);
    const all = await ex.fetchPositions(symbols);
    // Filter out zero-size positions (Binance returns 100+ empty entries)
    return all.filter(p => Math.abs(Number(p.contracts || 0)) > 0);
  },
  open_orders: async ({ exchange, symbol, market_type }) => {
    const ex = await getExchange(exchange, market_type);
    if (symbol) return ex.fetchOpenOrders(symbol);
    try {
      return await ex.fetchOpenOrders();
    } catch (err) {
      if (err.message?.includes('symbol') || err.message?.includes('argument')) {
        throw new Error(`${exchange} 查询未成交订单需要指定交易对，例如: {"symbol":"BTC/USDT"}`);
      }
      throw err;
    }
  },
  closed_orders: async ({ exchange, symbol, market_type, since, limit = 50 }) => {
    const ex = await getExchange(exchange, market_type);
    const sinceTs = since ? new Date(since).getTime() : undefined;
    return ex.fetchClosedOrders(symbol, sinceTs, Number(limit));
  },
  my_trades: async ({ exchange, symbol, market_type, since, limit = 50 }) => {
    const ex = await getExchange(exchange, market_type);
    const sinceTs = since ? new Date(since).getTime() : undefined;
    return ex.fetchMyTrades(symbol, sinceTs, Number(limit));
  },
  fetch_order: async ({ exchange, symbol, order_id, market_type }) => {
    const ex = await getExchange(exchange, market_type);
    return ex.fetchOrder(order_id, symbol);
  },
  create_order: async ({ exchange, symbol, type, side, amount, amount_unit, cost, leverage, price, market_type, params, confirmed }) => {
    const pendingFile = resolve(__dir, '..', '.pending-order.json');

    // Internal calls (from auto-trade.mjs) bypass file-based confirmation
    const isInternal = process.env.AICOIN_INTERNAL_CALL === '1';

    // Step 2: Confirmation — only works if a pending order file exists from Step 1
    if (confirmed === 'true' || confirmed === true) {
      if (isInternal) {
        // Internal call: execute directly with provided params
        const ex = await getExchange(exchange, market_type);
        const order = await placeOrder(ex, symbol, type, side, amount, price, params, exchange, market_type);
        if (market_type && market_type !== 'spot') {
          try {
            await ex.loadMarkets();
            const mkt = ex.markets[symbol];
            if (mkt?.contractSize) {
              order._contractSize = mkt.contractSize;
              order._amountInBase = amount * mkt.contractSize;
              order._unit = `${amount} contracts × ${mkt.contractSize} ${mkt.base}/contract = ${amount * mkt.contractSize} ${mkt.base}`;
            }
          } catch {}
        }
        return order;
      }

      let pending;
      try { pending = JSON.parse(readFileSync(pendingFile, 'utf8')); }
      catch { throw new Error('没有待确认的订单。请先不带 confirmed 参数调用 create_order 来预览订单，等用户确认后再重新调用并带上 confirmed=true。'); }

      // Expire after 5 minutes
      if (Date.now() - pending.timestamp > 5 * 60 * 1000) {
        try { unlinkSync(pendingFile); } catch {}
        throw new Error('订单预览已过期（超过5分钟），请重新创建订单预览。');
      }

      // Execute with stored params (prevents model from tampering between preview and confirm)
      const ex = await getExchange(pending.exchange, pending.market_type);
      const order = await placeOrder(ex, pending.symbol, pending.type, pending.side, pending.amount, pending.price, pending.params, pending.exchange, pending.market_type);
      try { unlinkSync(pendingFile); } catch {}
      if (pending.market_type && pending.market_type !== 'spot') {
        try {
          await ex.loadMarkets();
          const mkt = ex.markets[pending.symbol];
          if (mkt?.contractSize) {
            order._contractSize = mkt.contractSize;
            order._amountInBase = pending.amount * mkt.contractSize;
            order._unit = `${pending.amount} contracts × ${mkt.contractSize} ${mkt.base}/contract = ${pending.amount * mkt.contractSize} ${mkt.base}`;
          }
        } catch {}
      }
      return order;
    }

    // Step 1: Preview — save pending order to file, return preview
    const ex = await getExchange(exchange, market_type);
    await ex.loadMarkets();
    const mkt = ex.markets[symbol];

    // Round contract amount to market precision/min (e.g. OKX BTC swap = 0.01 contract step)
    // Avoids the old `Math.max(1, Math.round(x))` floor that broke sub-1-contract orders.
    const roundContracts = (raw) => {
      const minStep = mkt.precision?.amount || mkt.limits?.amount?.min || 1;
      const minAmt = mkt.limits?.amount?.min || minStep;
      let v = Number(raw);
      if (!isFinite(v) || v <= 0) return minAmt;
      // Clamp to min first so amountToPrecision doesn't throw on values < precision step
      if (v < minAmt) v = minAmt;
      try { v = Number(ex.amountToPrecision(symbol, v)); } catch { v = Math.round(v / minStep) * minStep; }
      if (v < minAmt) v = minAmt;
      return v;
    };

    // cost param: user says "用XU做多" → calculate amount from USDT margin budget
    if (cost && mkt?.contractSize && market_type && market_type !== 'spot') {
      const tick = await ex.fetchTicker(symbol);
      const curP = tick.last;
      // 杠杆来源:入参 > 已有仓位 > 交易所账户杠杆配置(fetchLeverage)。
      // 都拿不到时**不要静默假设 1x** —— 按 1x 算出的张数会与实际杠杆差数量级(AGENTS.md 铁则二)。
      let lev = leverage ? Number(leverage) : null;
      if (!lev) {
        try {
          const positions = await ex.fetchPositions([symbol]);
          const pos = positions.find(p => p.symbol === symbol);
          if (pos?.leverage) lev = Number(pos.leverage);
        } catch {}
      }
      if (!lev && ex.has?.fetchLeverage) {
        try {
          const lv = await ex.fetchLeverage(symbol);
          const n = Number(lv?.longLeverage ?? lv?.leverage ?? lv?.info?.lever ?? lv?.shortLeverage);
          if (n > 0) lev = n;
        } catch {}
      }
      if (!(lev > 0)) {
        throw new Error(`无法确定 ${symbol} 的杠杆倍数(当前无持仓、交易所也未返回杠杆配置)。请显式传 leverage,例如 {"cost":${cost},"leverage":10,...},避免按 1x 误算张数。`);
      }
      amount = roundContracts(Number(cost) * lev / (mkt.contractSize * curP));
    }

    // 现货按金额买入(cost):反算 base 数量 amount = cost / 价格(通用,不依赖各所 cost 通道)。
    // 否则 cost 在现货被静默丢弃 → amount=undefined → 预览 NaN、下出无数量的废单。
    const isSpot = !market_type || market_type === 'spot';
    if (cost && isSpot && !mkt?.contractSize) {
      if (side !== 'buy') throw new Error('现货 cost(按金额下单)目前只支持买入;卖出请用 amount 指定币数量。');
      let px = Number(price);
      if (!(px > 0)) { try { px = (await ex.fetchTicker(symbol)).last; } catch {} }
      if (!(px > 0)) throw new Error(`无法获取 ${symbol} 价格以按金额反算数量,请改用 amount(币数量)。`);
      try { amount = Number(ex.amountToPrecision(symbol, Number(cost) / px)); } catch { amount = Number(cost) / px; }
    }

    // 非 cost 路径必须有有效 amount —— 这个校验要放在换算**之前**:roundContracts 会把 NaN/缺失
    // 兜成 minAmt,若放换算后再校验就被掩盖,变成静默下出一个最小单(废单)。
    if (!cost && (amount == null || !(Number(amount) > 0))) {
      throw new Error('数量无效: 请提供 amount(币数量;合约要传张数时加 amount_unit:"contracts"),或现货市价买入用 cost(USDT 金额)。');
    }

    // 合约: amount 默认按"币数量"理解,统一 /contractSize 换算成张数。整数也换 —— 旧版用 Number.isInteger
    // 猜单位(整数=张/小数=币),在 contractSize≠1 的所(OKX DOGE cs=1000、Gate BTC cs=0.0001 等)会把
    // 张数算错几个数量级。显式 amount_unit:"contracts" 才跳过换算(给已按张数传入的调用方)。
    if (!cost && mkt?.contractSize && market_type && market_type !== 'spot' && amount_unit !== 'contracts') {
      amount = roundContracts(Number(amount) / mkt.contractSize);
    }

    // 最终兜底: cost 路径若算出 0/NaN(金额过小、价格异常等)也拒绝,绝不落盘空 amount。
    if (amount == null || !(Number(amount) > 0)) {
      throw new Error('数量无效(经金额/张数换算后仍无效)。请检查 cost/amount 与当前价格、最小下单额。');
    }

    const pendingOrder = { exchange, symbol, type, side, amount, price, market_type, params, timestamp: Date.now() };
    writeFileSync(pendingFile, JSON.stringify(pendingOrder));

    // Build order details
    const sideLabel = side === 'buy' ? '买入/做多' : '卖出/做空';
    // 识别条件单(params 带触发价),避免对无 price 的 STOP_MARKET 显示"限价 undefined"。
    // 注:挂"保护已有仓位"的止盈止损请用 set_stop(自动算方向/reduceOnly),别在这里手搓。
    const trigPx = params && (params.stopLossPrice ?? params.takeProfitPrice ?? params.triggerPrice ?? params.stopPrice);
    const trailRate = params && (params.trailingPercent ?? params.callbackRate);
    const typeLabel = trailRate != null ? `追踪止损(回调 ${trailRate}%${params.activationPrice ? `,激活 ${params.activationPrice}` : ''})`
      : trigPx != null ? `条件单(触发价 ${trigPx})`
      : type === 'market' ? '市价' : `限价 ${price}`;
    const mktType = market_type || 'spot';

    const orderInfo = { 交易所: exchange, 交易对: symbol, 方向: sideLabel, 类型: typeLabel };

    // Fetch current price
    let curPrice = null;
    if (type === 'market' || !price) {
      try {
        const tick = await ex.fetchTicker(symbol);
        curPrice = tick.last;
        orderInfo['当前价格'] = `$${curPrice.toLocaleString()}`;
      } catch {}
    }

    // Contract details
    if (mkt?.contractSize) {
      orderInfo['合约数量'] = `${amount} 张`;
      orderInfo['换算'] = `${amount} × ${mkt.contractSize} ${mkt.base}/张 = ${amount * mkt.contractSize} ${mkt.base}`;
      if (curPrice) orderInfo['预估价值'] = `${(amount * mkt.contractSize * curPrice).toFixed(2)} USDT`;
    } else {
      orderInfo['数量'] = `${amount}`;
      if (curPrice) orderInfo['预估价值'] = `${(amount * curPrice).toFixed(2)} USDT`;
    }

    // Leverage & margin info for futures
    if (mktType !== 'spot') {
      let lev = leverage ? Number(leverage) : null;
      let mgnMode = null;
      try {
        const positions = await ex.fetchPositions([symbol]);
        const pos = positions.find(p => p.symbol === symbol);
        if (pos) {
          if (!lev && pos.leverage) lev = Number(pos.leverage);
          mgnMode = pos.marginMode || pos.marginType;
        }
      } catch {}
      if (lev) {
        orderInfo['杠杆'] = `${lev}x`;
        if (curPrice) {
          const notional = mkt?.contractSize ? amount * mkt.contractSize * curPrice : amount * curPrice;
          orderInfo['预估保证金'] = `${(notional / lev).toFixed(2)} USDT`;
        }
      }
      if (mgnMode) orderInfo['保证金模式'] = mgnMode;
    }

    return {
      _preview: true,
      status: '⚠️ 订单未下达',
      风险提示: '⚠️ 交易风险声明：加密货币交易具有高风险，可能导致本金全部损失。合约使用杠杆会放大收益和亏损。本工具仅提供交易执行功能，不构成投资建议。继续下单即表示你已知悉并接受以上风险。',
      用户须知: '下单前请确认：(1) 你已了解该交易的风险 (2) 投入的资金在可承受范围内 (3) 你已设置合适的止损',
      订单详情: orderInfo,
      操作指引: '请确认以上订单信息无误。回复「确认」或「yes」执行下单，回复「取消」放弃。',
    };
  },
  close_position: async ({ exchange, symbol, market_type, confirmed }) => {
    const mt = market_type || 'swap';
    const ex = await getExchange(exchange, mt);
    const positions = await ex.fetchPositions(symbol ? [symbol] : undefined);
    const open = positions.filter(p => Math.abs(Number(p.contracts || 0)) > 0);
    if (!open.length) return { message: '当前没有持仓需要平仓。', positions: [] };
    // Preview
    if (confirmed !== 'true' && confirmed !== true) {
      return {
        _preview: true,
        status: '⚠️ 平仓预览 — 订单未下达',
        待平仓位: open.map(p => ({
          交易对: p.symbol, 方向: p.side === 'long' ? '多' : '空',
          张数: Math.abs(Number(p.contracts)), 开仓价: p.entryPrice,
          未实现盈亏: p.unrealizedPnl, 杠杆: p.leverage,
        })),
        操作指引: '请确认平掉以上仓位。回复「确认」执行，回复「取消」放弃。',
      };
    }
    // Execute
    const results = [];
    for (const pos of open) {
      // 方向必须明确取自交易所;拿不到就跳过,绝不默认 buy(否则对多仓会变成加仓而非平仓)。
      if (pos.side !== 'long' && pos.side !== 'short') {
        results.push({ symbol: pos.symbol, status: '跳过', error: '交易所未返回持仓方向,拒绝盲目平仓' });
        continue;
      }
      const closeSide = pos.side === 'long' ? 'sell' : 'buy';
      const amount = Math.abs(Number(pos.contracts));
      try {
        // 方向参数从真实持仓推导(hedge/one-way 自适应)。放进 try: Bitget 模式测不出时 closeParamsFor
        // 会 throw(防反向开仓),应作为该仓的失败结果,不连累其它仓。
        const cp = closeParamsFor(exchange, mt, pos);
        const order = await placeOrder(ex, pos.symbol, 'market', closeSide, amount, undefined, cp, exchange, mt);
        results.push({ symbol: pos.symbol, side: pos.side, amount, status: '已平仓', orderId: order.id });
      } catch (e) {
        results.push({ symbol: pos.symbol, side: pos.side, amount, status: '失败', error: e.message });
      }
    }
    return { 平仓结果: results };
  },
  // 止盈止损 / 条件单 —— 给"已有仓位"挂服务器端保护单。两步确认。
  // 方向、reduceOnly/posSide 全部从真实持仓推导(防反向单、防 hedge 模式 reduceOnly 被拒),
  // 触发价做"在现价正确一侧"校验(防搞反/瞬间触发),用 ccxt 统一参数 stopLossPrice/
  // takeProfitPrice 下独立的 reduceOnly 条件单(跨 Binance/OKX/Bybit 等通用)。
  set_stop: async ({ exchange, symbol, market_type, stop_loss, take_profit, trigger_price, amount, side, force, confirmed }) => {
    const pendingFile = resolve(__dir, '..', '.pending-stop.json');

    // Step 2: 确认执行(读 step1 落盘的已解析订单,防 model 在两步之间篡改方向/数量/触发价)
    if (confirmed === 'true' || confirmed === true) {
      let pending;
      try { pending = JSON.parse(readFileSync(pendingFile, 'utf8')); }
      catch { throw new Error('没有待确认的止盈止损单。请先不带 confirmed 调用 set_stop 预览,等用户确认后再带 confirmed=true。'); }
      if (Date.now() - pending.timestamp > 5 * 60 * 1000) {
        try { unlinkSync(pendingFile); } catch {}
        throw new Error('止盈止损预览已过期(超过5分钟),请重新预览。');
      }
      const mt = pending.market_type || 'swap';
      const ex = await getExchange(pending.exchange, mt);
      // 防"两步窗口内持仓缩小/反手":再读一次盘,把数量 clamp 到当前同向持仓;持仓没了就不挂废单。
      // 这对币安双向(走 positionSide、不带 reduceOnly)尤其重要 —— 它没有 reduceOnly 兜底。best-effort:
      // 读盘失败则用原数量(OKX/Bybit/币安单向仍有 reduceOnly 兜住)。
      let execAmount = pending.amount;
      try {
        const curPos = (await ex.fetchPositions([pending.symbol]))
          .find(p => p.symbol === pending.symbol && p.side === pending.posSide && Math.abs(Number(p.contracts || 0)) > 0);
        if (!curPos) {
          try { unlinkSync(pendingFile); } catch {}
          return { 止盈止损结果: [], _warning: `${pending.symbol} 的 ${pending.posSide} 持仓已不存在(可能在确认期间被平掉/反手),未挂任何止盈止损单。请重新查持仓后再决定。` };
        }
        const curSize = Math.abs(Number(curPos.contracts));
        if (execAmount > curSize) execAmount = curSize;
      } catch { /* 读盘失败,沿用原数量 */ }
      const results = [];
      for (const o of pending.orders) {
        try {
          const order = await placeOrder(ex, pending.symbol, 'market', pending.closeSide, execAmount, undefined, o.params, pending.exchange, mt);
          results.push({ 类型: o.kind, 触发价: o.trigger, status: '已挂单', orderId: order.id });
        } catch (e) {
          results.push({ 类型: o.kind, 触发价: o.trigger, status: '失败', error: e.message });
        }
      }
      try { unlinkSync(pendingFile); } catch {}
      return {
        止盈止损结果: results,
        _note: '条件单在部分交易所(OKX 等)属算法/委托单,不出现在普通挂单列表 —— 用 stop_orders 动作或交易所 APP 的「条件委托」栏复核,别用 open_orders 误判没挂上。',
        验证建议: `node scripts/exchange.mjs stop_orders '{"exchange":"${pending.exchange}","symbol":"${pending.symbol}","market_type":"${mt}"}'`,
      };
    }

    // Step 1: 预览 —— 取真实持仓、推导方向、校验触发价、落盘待确认订单
    if (!symbol) throw new Error('需要 symbol(止盈止损是给已有仓位挂保护单),例: {"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap","stop_loss":63.5}');
    const mt = market_type || 'swap';
    if (mt === 'spot') throw new Error('set_stop 仅用于合约持仓的止盈止损。现货保护单请用 create_order 带 params。');
    if (stop_loss == null && take_profit == null && trigger_price == null) {
      throw new Error('至少给一个:stop_loss(止损触发价)/ take_profit(止盈触发价)/ trigger_price(单一触发价,按方向自动归类)。');
    }
    const ex = await getExchange(exchange, mt);
    await ex.loadMarkets();
    const mkt = ex.markets[symbol];
    const positions = await ex.fetchPositions([symbol]);
    const matching = positions.filter(p => p.symbol === symbol && Math.abs(Number(p.contracts || 0)) > 0);
    if (!matching.length) throw new Error(`${exchange} 上没有 ${symbol} 的持仓。止盈止损是给已有仓位挂保护单;若要挂"条件入场单",用 create_order 带 params。`);
    // 双向持仓(hedge)同一交易对可能同时有多/空两个仓 —— 选错边会把止损挂到反方向。必须指定 side。
    const wantSide = side ? String(side).toLowerCase().replace('多', 'long').replace('空', 'short') : null;
    let pos;
    if (matching.length > 1) {
      if (!wantSide) throw new Error(`${symbol} 同时持有多、空两个仓(双向持仓)。请指定 side("long"/"short")选择给哪个挂止盈止损。当前: ${matching.map(p => `${p.side} ${Math.abs(Number(p.contracts))}张`).join(' / ')}`);
      pos = matching.find(p => p.side === wantSide);
      if (!pos) throw new Error(`没找到 ${symbol} 的 ${wantSide} 持仓。当前持仓方向: ${matching.map(p => p.side).join(', ')}`);
    } else {
      pos = matching[0];
      if (wantSide && pos.side !== wantSide) throw new Error(`你指定 side=${wantSide},但 ${symbol} 当前持仓是 ${pos.side},方向不符,已中止以防挂错边。`);
    }

    if (pos.side !== 'long' && pos.side !== 'short') throw new Error(`无法确定 ${symbol} 持仓方向(交易所未返回 side),已中止以防止盈止损挂错边。`);
    const posSize = Math.abs(Number(pos.contracts));
    const isLong = pos.side === 'long';
    const closeSide = isLong ? 'sell' : 'buy';
    const cp = closeParamsFor(exchange, mt, pos); // reduceOnly/posSide/positionSide 从真实持仓推导

    // 数量:默认全仓;给了就取整到精度并 clamp 不超过持仓(reduceOnly 也会兜底,但提前 clamp 更直观)。
    let amt = posSize;
    let amtNote = `全仓 ${posSize}`;
    if (amount != null) {
      let v = Number(amount);
      try { v = Number(ex.amountToPrecision(symbol, v)); } catch {}
      if (!(v > 0)) throw new Error(`amount 非法: ${amount}`);
      if (v > posSize) { v = posSize; amtNote = `给的数量超过持仓,已 clamp 到全仓 ${posSize}`; }
      else amtNote = `部分 ${v} / 持仓 ${posSize}`;
      amt = v;
    }

    // 当前价(用于触发价方向校验)
    let cur = null;
    try { cur = (await ex.fetchTicker(symbol)).last; } catch {}
    // 拿不到现价就无法校验触发价方向(设反会瞬间触发或把止损当止盈)—— 默认中止,不靠 LLM 自觉。
    // 确需无校验挂单,显式传 force:true 自负风险。
    if (cur == null && !(force === true || force === 'true')) {
      throw new Error(`拿不到 ${symbol} 当前价,无法校验止盈止损触发价方向(设反会瞬间触发或方向颠倒)。请稍后重试;确需跳过校验挂单,显式传 "force":true 自负风险。`);
    }

    // 触发价方向校验:多单止损<现价、止盈>现价;空单反之。设反会瞬间触发或把止损当止盈 → 直接报错。
    const orders = [];
    const checks = [];
    const want = (px, kind) => {
      const v = Number(px);
      if (!isFinite(v) || v <= 0) throw new Error(`${kind}触发价非法: ${px}`);
      if (cur != null) {
        const okSide = kind === '止损' ? (isLong ? v < cur : v > cur) : (isLong ? v > cur : v < cur);
        const rel = kind === '止损' ? (isLong ? '应 < 现价' : '应 > 现价') : (isLong ? '应 > 现价' : '应 < 现价');
        if (!okSide) throw new Error(`${isLong ? '多' : '空'}单的${kind}触发价 ${v} 方向不对(${rel} ${cur})。设反了会瞬间触发或把止损当止盈,请核对。`);
        checks.push(`${kind} ${v} ${rel} ${cur} ✓`);
      }
      return v;
    };
    if (stop_loss != null) { const v = want(stop_loss, '止损'); orders.push({ kind: '止损', trigger: v, params: { stopLossPrice: v, ...cp } }); }
    if (take_profit != null) { const v = want(take_profit, '止盈'); orders.push({ kind: '止盈', trigger: v, params: { takeProfitPrice: v, ...cp } }); }
    if (trigger_price != null) {
      // 单一触发价:按它落在现价哪一侧 + 持仓方向,自动归类成止损或止盈。
      const v = Number(trigger_price);
      if (!isFinite(v) || v <= 0) throw new Error(`trigger_price 非法: ${trigger_price}`);
      if (cur == null) throw new Error('拿不到当前价,无法自动归类 trigger_price。请改用 stop_loss 或 take_profit 明确指定。');
      const kind = (isLong ? v < cur : v > cur) ? '止损' : '止盈';
      const key = kind === '止损' ? 'stopLossPrice' : 'takeProfitPrice';
      orders.push({ kind, trigger: v, params: { [key]: v, ...cp } });
      checks.push(`trigger_price ${v} 按方向归类为「${kind}」(现价 ${cur})`);
    }

    const modeDesc = cp.positionSide ? `hedge / positionSide=${cp.positionSide}(币安双向,不带 reduceOnly)`
      : cp.posSide ? `hedge / posSide=${cp.posSide} + reduceOnly`
      : cp.positionIdx ? `hedge / positionIdx=${cp.positionIdx} + reduceOnly`
      : cp.hedged ? `hedge / ${exchange}(ccxt 翻向 → tradeSide:Close / offset:close)`
      : 'one-way / reduceOnly';

    const pending = { exchange, symbol, market_type: mt, closeSide, posSide: pos.side, amount: amt, orders, timestamp: Date.now() };
    writeFileSync(pendingFile, JSON.stringify(pending));

    return {
      _preview: true,
      status: '⚠️ 止盈止损未挂单',
      持仓: { 交易对: symbol, 方向: isLong ? '多' : '空', 张数: posSize, 开仓价: pos.entryPrice, 当前价: cur, 杠杆: pos.leverage, 未实现盈亏: pos.unrealizedPnl },
      将挂条件单: orders.map(o => ({
        类型: o.kind, 触发价: o.trigger,
        触发后: `市价${closeSide === 'sell' ? '卖出平多' : '买入平空'}`,
        数量: mkt?.contractSize ? `${amt} 张` : `${amt}`,
        平仓模式: modeDesc,
      })),
      数量说明: amtNote,
      方向校验: checks.length ? checks : '(拿不到当前价,跳过触发价方向校验 —— 请你自己确认方向)',
      风险提示: '⚠️ 条件单是交易所服务器端触发的市价单,触发时按当时市价成交,极端行情可能滑点。ccxt 跨所行为有差异,挂单后务必用 stop_orders 或交易所 APP 复核确实挂上了。',
      操作指引: '确认无误回复「确认」执行挂单,回复「取消」放弃。',
    };
  },
  // 列出条件单/算法委托(止盈止损等)。OKX 等的算法单不在普通 open_orders 里,用这个查。
  stop_orders: async ({ exchange, symbol, market_type }) => {
    const ex = await getExchange(exchange, market_type || 'swap');
    try { return await fetchConditionalOrders(ex, exchange, symbol); }
    catch (e) { throw new Error(`查询条件单失败: ${e?.message || e}。部分交易所的算法/条件单需在交易所 APP 的「条件委托」栏查看。`); }
  },
  funding_rate: async ({ exchange, symbol, market_type }) => {
    const ex = await getExchange(exchange, market_type || 'swap', true);
    return ex.fetchFundingRate(symbol);
  },
  funding_rates: async ({ symbol, exchanges: exList, market_type }) => {
    const list = exList ? exList.split(',').map(s => s.trim()) : SUPPORTED;
    const sym = symbol || 'BTC/USDT:USDT';
    const results = await Promise.allSettled(
      list.map(async id => {
        try {
          const ex = await getExchange(id, market_type || 'swap', true);
          const r = await ex.fetchFundingRate(sym);
          return { exchange: id, symbol: sym, fundingRate: r.fundingRate, fundingDatetime: r.fundingDatetime, markPrice: r.markPrice };
        } catch (e) {
          return { exchange: id, symbol: sym, error: e.message };
        }
      })
    );
    const rates = results.map(r => r.status === 'fulfilled' ? r.value : { exchange: 'unknown', error: r.reason?.message });
    const valid = rates.filter(r => !r.error && r.fundingRate != null);
    if (valid.length >= 2) {
      valid.sort((a, b) => a.fundingRate - b.fundingRate);
      const spread = valid[valid.length - 1].fundingRate - valid[0].fundingRate;
      return { rates, arbitrage: { lowestRate: valid[0], highestRate: valid[valid.length - 1], spread, spreadPct: (spread * 100).toFixed(6) + '%', annualized: (spread * 3 * 365 * 100).toFixed(2) + '%' } };
    }
    return { rates, arbitrage: null, _note: 'Need at least 2 successful rate queries to calculate arbitrage spread' };
  },
  cancel_order: async ({ exchange, symbol, order_id, market_type }) => {
    const ex = await getExchange(exchange, market_type);
    if (order_id) {
      try { return await ex.cancelOrder(order_id, symbol); }
      catch (e) {
        // 普通订单端点找不到 → 多半是条件/算法单(币安 algoId、OKX/Bitget algo/plan 单走独立端点)。
        // 各所 not-found 信号都回退到 {stop:true}(条件单端点)再撤一次,别只认币安的 -2011。
        const m = String(e);
        if (/-2011|51400|51401|51402|51603|40109|43001|Unknown order|does not exist|order ?not ?found|订单不存在/i.test(m)) {
          return await ex.cancelOrder(order_id, symbol, { stop: true });
        }
        throw e;
      }
    }
    // 无 id = 全撤: 普通单 + 条件/算法单都要清(set_stop 挂的止盈止损就是条件单)。
    const out = {};
    // 不支持一键全撤的所(OKX / Hyperliquid 的 cancelAllOrders has===false)别把 NotSupported 吞成假成功 —— 那会留下没撤掉的单。改 fetchOpenOrders 拉出来逐个撤。
    const cancelByFetch = async (extra) => {
      const orders = await ex.fetchOpenOrders(symbol, undefined, undefined, extra || {});
      const res = [];
      for (const o of orders) {
        try { await ex.cancelOrder(o.id, symbol, extra || {}); res.push({ id: o.id, ok: true }); }
        catch (e) { res.push({ id: o.id, ok: false, error: String(e).slice(0, 100) }); }
      }
      return { canceled: res.filter(r => r.ok).length, total: res.length, detail: res };
    };
    if (ex.has?.cancelAllOrders) {
      try { out.regular = await ex.cancelAllOrders(symbol); } catch (e) { out.regular = { error: String(e).slice(0, 160) }; }
      try { out.conditional = await ex.cancelAllOrders(symbol, { stop: true }); } catch (e) { out.conditional = { skipped: String(e).slice(0, 120) }; }
    } else {
      try { out.regular = await cancelByFetch(); } catch (e) { out.regular = { error: String(e).slice(0, 160) }; }
      // 条件单: 用合并查询(覆盖 OKX conditional 类,不漏)再逐个撤
      try {
        const conds = await fetchConditionalOrders(ex, exchange, symbol);
        const res = [];
        for (const o of conds) {
          try { await ex.cancelOrder(o.id, symbol, { stop: true }); res.push({ id: o.id, ok: true }); }
          catch (e) { res.push({ id: o.id, ok: false, error: String(e).slice(0, 100) }); }
        }
        out.conditional = { canceled: res.filter((r) => r.ok).length, total: res.length, detail: res };
      } catch (e) { out.conditional = { skipped: String(e).slice(0, 120) }; }
    }
    return out;
  },
  set_leverage: async ({ exchange, symbol, leverage, market_type }) => {
    const ex = await getExchange(exchange, market_type);
    return ex.setLeverage(leverage, symbol);
  },
  set_margin_mode: async ({ exchange, symbol, margin_mode, market_type, leverage }) => {
    const ex = await getExchange(exchange, market_type);
    try {
      const modeParams = exchange === 'okx' && leverage ? { lever: String(leverage) } : {};

      // OKX isolated mode: try hedge mode first (with posSide), fallback to one-way mode (without posSide)
      if (exchange === 'okx' && margin_mode === 'isolated') {
        // First try with posSide (hedge mode)
        let hedgeModeSuccess = true;
        const results = [];
        for (const ps of ['long', 'short']) {
          try {
            results.push(await ex.setMarginMode(margin_mode, symbol, { ...modeParams, posSide: ps }));
          } catch (e) {
            const m = e.message || String(e);
            if (m.includes('already') || m.includes('No need') || m.includes('margin mode is not modified')) {
              results.push({ posSide: ps, unchanged: true });
            } else if (m.includes('posSide') || m.includes('51000')) {
              // posSide error = one-way position mode, try without posSide
              hedgeModeSuccess = false;
              break;
            } else throw e;
          }
        }
        if (hedgeModeSuccess) return { success: true, margin_mode, results };

        // Fallback: one-way position mode (no posSide)
        try {
          const res = await ex.setMarginMode(margin_mode, symbol, modeParams);
          return { success: true, margin_mode, response: res };
        } catch (e2) {
          const m2 = e2.message || String(e2);
          if (m2.includes('already') || m2.includes('No need') || m2.includes('margin mode is not modified')) {
            return { success: true, margin_mode, message: `已经是 ${margin_mode} 模式，无需切换。` };
          }
          throw e2;
        }
      }

      const res = await ex.setMarginMode(margin_mode, symbol, modeParams);
      if (res?.code === -4046 || res?.msg?.includes('No need to change') || res?.msg?.includes('margin mode is not modified')) {
        return { success: true, margin_mode, message: `已经是 ${margin_mode} 模式，无需切换。` };
      }
      return { success: true, margin_mode, response: res };
    } catch (err) {
      const msg = err.message || String(err);
      if (msg.includes('-4046') || msg.includes('No need to change') || msg.includes('already') || msg.includes('margin mode is not modified')) {
        return { success: true, margin_mode, message: `已经是 ${margin_mode} 模式，无需切换。` };
      }
      throw err;
    }
  },
  set_trading_params: async ({ exchange, symbol, leverage, margin_mode, market_type }) => {
    if (!symbol) throw new Error('symbol is required, e.g. BTC/USDT:USDT');
    if (!leverage && !margin_mode) throw new Error('At least one of leverage or margin_mode is required');
    const ex = await getExchange(exchange, market_type || 'swap');
    const results = { symbol, exchange };

    // Step 1: Set margin mode FIRST (must be done before leverage on some exchanges)
    if (margin_mode) {
      const mode = margin_mode.toLowerCase();
      if (!['cross', 'isolated'].includes(mode)) throw new Error('margin_mode must be "cross" or "isolated"');
      try {
        const modeParams = exchange === 'okx' && leverage ? { lever: String(leverage) } : {};

        // OKX isolated: try hedge mode first, fallback to one-way mode
        if (exchange === 'okx' && mode === 'isolated') {
          let hedgeModeSuccess = true;
          const modeResults = [];
          for (const ps of ['long', 'short']) {
            try {
              modeResults.push(await ex.setMarginMode(mode, symbol, { ...modeParams, posSide: ps }));
            } catch (e) {
              const m = e.message || String(e);
              if (m.includes('already') || m.includes('No need') || m.includes('margin mode is not modified')) {
                modeResults.push({ posSide: ps, unchanged: true });
              } else if (m.includes('posSide') || m.includes('51000')) {
                hedgeModeSuccess = false;
                break;
              } else {
                modeResults.push({ posSide: ps, error: m });
              }
            }
          }
          if (hedgeModeSuccess) {
            results.margin_mode = { success: true, mode, details: modeResults };
          } else {
            // Fallback: one-way position mode
            try {
              const res = await ex.setMarginMode(mode, symbol, modeParams);
              results.margin_mode = { success: true, mode, response: res };
            } catch (e2) {
              const m2 = e2.message || String(e2);
              if (m2.includes('already') || m2.includes('No need') || m2.includes('margin mode is not modified')) {
                results.margin_mode = { success: true, mode, message: `已经是 ${mode} 模式` };
              } else {
                results.margin_mode = { success: false, mode, error: m2 };
              }
            }
          }
        } else {
          try {
            const res = await ex.setMarginMode(mode, symbol, modeParams);
            if (res?.code === -4046 || res?.msg?.includes('No need to change')) {
              results.margin_mode = { success: true, mode, message: `已经是 ${mode} 模式` };
            } else {
              results.margin_mode = { success: true, mode, response: res };
            }
          } catch (e) {
            const m = e.message || String(e);
            if (m.includes('-4046') || m.includes('No need') || m.includes('already') || m.includes('margin mode is not modified')) {
              results.margin_mode = { success: true, mode, message: `已经是 ${mode} 模式` };
            } else {
              results.margin_mode = { success: false, mode, error: m };
            }
          }
        }
      } catch (e) {
        results.margin_mode = { success: false, error: e.message || String(e) };
      }
    }

    // Step 2: Set leverage
    if (leverage) {
      try {
        const res = await ex.setLeverage(Number(leverage), symbol);
        results.leverage = { success: true, leverage: Number(leverage), response: res };
      } catch (e) {
        const m = e.message || String(e);
        if (m.includes('already') || m.includes('No need') || m.includes('not modified')) {
          results.leverage = { success: true, leverage: Number(leverage), message: `已经是 ${leverage}x 杠杆` };
        } else {
          results.leverage = { success: false, leverage: Number(leverage), error: m };
        }
      }
    }

    results.success = (!results.margin_mode || results.margin_mode.success) && (!results.leverage || results.leverage.success);
    return results;
  },
  transfer: async ({ exchange, code, amount, from_account, to_account }) => {
    // OKX unified account: no transfer needed
    if (exchange === 'okx') {
      return {
        success: false,
        reason: 'OKX_UNIFIED_ACCOUNT',
        message: 'OKX 是统一账户，现货和合约共用同一个余额，不需要划转。直接下单即可。',
      };
    }
    if (!from_account || !to_account || !code || amount == null) {
      throw new Error('划转需要 code(币种)、amount(数量)、from_account、to_account。例: {"exchange":"binance","code":"USDT","amount":10,"from_account":"spot","to_account":"future"}');
    }
    const ex = await getExchange(exchange);
    // Normalize account names to CCXT-recognized keys
    // CCXT Binance only accepts: spot/main, future, delivery, margin/cross, linear, swap, inverse, funding, option
    // AI agents may say "futures", "usdm", "coinm" etc. which CCXT misinterprets as isolated margin symbols
    const ALIAS = { futures: 'future', usdm: 'future', coinm: 'delivery' };
    const fromRaw = from_account.toLowerCase();
    const toRaw = to_account.toLowerCase();
    const from = ALIAS[fromRaw] || fromRaw;
    const to = ALIAS[toRaw] || toRaw;
    try {
      return await ex.transfer(code, amount, from, to);
    } catch (err) {
      const msg = err.message || String(err);
      // Binance: API key lacks Universal Transfer permission
      if (exchange === 'binance' && (msg.includes('-1002') || msg.includes('not authorized'))) {
        throw new Error(`Binance 划转失败: API Key 没有万向划转(Universal Transfer)权限。请在 Binance API 管理后台开启「Permits Universal Transfer / 允许万向划转」权限。原始错误: ${msg}`);
      }
      throw err;
    }
  },
});
