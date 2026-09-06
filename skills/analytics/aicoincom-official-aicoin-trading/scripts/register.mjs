#!/usr/bin/env node
// Exchange Registration — outputs AiCoin referral links
// Usage: node scripts/register.mjs <exchange>
// Example: node scripts/register.mjs okx

const REFERRALS = {
  okx:         { name: 'OKX',         code: 'aicoin20',  benefit: '永久返20%手续费', link: 'https://jump.do/zh-Hans/xlink-proxy?id=2' },
  binance:     { name: 'Binance',     code: 'aicoin668', benefit: '返10% + $500',   link: 'https://jump.do/zh-Hans/xlink-proxy?id=3' },
  bitget:      { name: 'Bitget',      code: 'hktb3191',  benefit: '返10%手续费',     link: 'https://jump.do/zh-Hans/xlink-proxy?id=6' },
  htx:         { name: 'HTX',         code: 'j2us6223',  benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=4' },
  gate:        { name: 'Gate.io',     code: 'AICOINGO',  benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=5' },
  bitmart:     { name: 'Bitmart',     code: 'cBMfHE',    benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=13' },
  bybit:       { name: 'Bybit',       code: '34429',     benefit: '',               link: 'https://jump.do/zh-Hans/xlink-proxy?id=15' },
  pionex:      { name: 'Pionex',      code: '4vgi0zUF',  benefit: '',               link: 'https://www.pionex.com/zh-CN/signUp?r=4vgi0zUF' },
  hyperliquid: { name: 'Hyperliquid', code: 'AICOIN88',  benefit: '返4%手续费',      link: 'https://app.hyperliquid.xyz/join/AICOIN88' },
  okx_dex:     { name: 'OKX DEX',     code: 'AICOIN88',  benefit: '返20%手续费',     link: 'https://web3.okx.com/ul/joindex?ref=AICOIN88' },
  binance_dex: { name: 'Binance DEX', code: 'SEPRFR9Q',  benefit: '返10%手续费',     link: 'https://web3.binance.com/referral?ref=SEPRFR9Q' },
  aster:       { name: 'Aster',       code: '9C50e2',    benefit: '返5%手续费',      link: 'https://www.asterdex.com/zh-CN/referral/9C50e2' },
};

// Normalize input: "OKX" -> "okx", "币安" -> "binance", "火币" -> "htx"
const ALIASES = {
  '币安': 'binance', 'bian': 'binance', 'bn': 'binance',
  '火币': 'htx', 'huobi': 'htx',
  '派网': 'pionex',
  'hl': 'hyperliquid',
  'gateio': 'gate', 'gate.io': 'gate',
};

const raw = (process.argv[2] || '').trim().toLowerCase();
const key = ALIASES[raw] || raw;

if (!key || key === 'list') {
  // List all exchanges
  const result = {
    message: '以下是所有支持的交易所及 AiCoin 专属注册链接：',
    exchanges: Object.values(REFERRALS).map(r => ({
      exchange: r.name,
      invite_code: r.code,
      benefit: r.benefit || '—',
      register_link: r.link,
    })),
    note: '通过以上链接注册可享手续费返还优惠。用法：node scripts/register.mjs <exchange>',
  };
  console.log(JSON.stringify(result, null, 2));
} else if (REFERRALS[key]) {
  const r = REFERRALS[key];
  const result = {
    exchange: r.name,
    invite_code: r.code,
    benefit: r.benefit || '—',
    register_link: r.link,
    steps: [
      `打开注册链接：${r.link}`,
      '选择手机号或邮箱注册，填入验证码、设置密码',
      '进入「账户中心」→「身份验证」完成 KYC',
      '如需 API 交易，到「API 管理」创建 API Key，写入 .env 文件',
    ],
    security_note: 'AiCoin API Key 仅用于获取市场数据，无法交易。交易所 API Key 需单独到交易所申请。所有密钥仅保存在本地设备，不会上传。',
  };
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(JSON.stringify({
    error: `未知交易所: ${raw}`,
    available: Object.keys(REFERRALS).join(', '),
    hint: '用法：node scripts/register.mjs okx',
  }));
  process.exit(1);
}
