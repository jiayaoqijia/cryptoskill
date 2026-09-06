#!/usr/bin/env node
// AiCoin API Key status check — ALWAYS outputs security notice
// Usage: node scripts/api-key-info.mjs [check]
// When user asks about configuring/checking AiCoin API key, run this script.

import { loadEnv, writeEnvPath, envCandidates } from '../lib/env-loader.mjs';
import { readFileSync } from 'node:fs';

// .env auto-load (宿主可能不向子进程注入 env)。共享 loader,见 lib/env-loader.mjs。
loadEnv();

function findKey() {
  const val = process.env.AICOIN_ACCESS_KEY_ID?.trim();
  if (!val) return { found: false };
  // 找出这把 key 真正来自哪个候选文件(扫描顺序与 loadEnv 一致,首个命中即来源);
  // 都没命中 = 来自注入的环境变量。汇报真实位置,而不是"建议写入位置"。
  let source = null;
  for (const f of envCandidates()) {
    try {
      if (readFileSync(f, 'utf-8').split('\n').some((l) => l.trim().startsWith('AICOIN_ACCESS_KEY_ID='))) { source = f; break; }
    } catch { /* 文件不存在或不可读,跳过 */ }
  }
  return { found: true, key_id: val.slice(0, 8) + '...', source: source || '环境变量(已注入,非文件)' };
}

const status = findKey();
const envPath = writeEnvPath();

const result = {
  aicoin_key_status: status.found
    ? { configured: true, key_preview: status.key_id, env_file: status.source }
    : {
        configured: false,
        setup_steps: [
          '访问 https://www.aicoin.com/opendata 注册并创建 API Key',
          '在 .env 文件中添加：AICOIN_ACCESS_KEY_ID=your-key-id',
          '在 .env 文件中添加：AICOIN_ACCESS_SECRET=your-secret',
          `.env 文件位置：${envPath}（CoinClaw 容器内请在 web UI EnvSection 配置）`,
        ],
        tier_options: [
          { tier: '免费版',     price: '$0',     highlights: '价格、K线、热门币' },
          { tier: '基础版',     price: '$29/mo',  highlights: '+ 资金费率、多空比、新闻' },
          { tier: '标准版',     price: '$79/mo',  highlights: '+ 鲸鱼单、信号、灰度' },
          { tier: '高级版',     price: '$299/mo', highlights: '+ 爆仓热力图、指标K线' },
          { tier: '专业版',     price: '$699/mo', highlights: '全部接口：AI分析、OI、美股' },
        ],
      },
  security_notice: {
    message: 'AiCoin API Key 与交易所 API Key 是完全独立的两套密钥',
    details: [
      'AiCoin API Key 仅用于获取市场数据（行情、K线、资金费率等），无法进行任何交易操作，也无法读取你在交易所的任何信息',
      '如需在交易所下单交易，需要单独到各交易所后台申请交易 API Key',
      '所有密钥（AiCoin key 和交易所 key）仅保存在你的本地设备 .env 文件中，不会上传到任何服务器',
    ],
  },
};

console.log(JSON.stringify(result, null, 2));
