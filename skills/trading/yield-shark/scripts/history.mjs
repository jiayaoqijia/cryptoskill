#!/usr/bin/env node
/**
 * 🦈 YieldShark - 收益率历史记录
 * 将查询结果保存到本地，生成历史趋势
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, '..', 'data');
const HISTORY_FILE = path.join(DATA_DIR, 'yield-history.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 加载历史记录
function loadHistory() {
    try {
        if (fs.existsSync(HISTORY_FILE)) {
            return JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('⚠️  加载历史记录失败:', e.message);
    }
    return { records: [] };
}

// 保存记录
function saveRecord(token, platform, chain, apy, tvl) {
    const history = loadHistory();
    const record = {
        timestamp: Date.now(),
        date: new Date().toISOString(),
        token,
        platform,
        chain,
        apy,
        tvl
    };
    
    history.records.push(record);
    
    // 保留最近 1000 条记录
    if (history.records.length > 1000) {
        history.records = history.records.slice(-1000);
    }
    
    fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
    return record;
}

// 显示历史趋势
function showHistory(token = null, limit = 10) {
    const history = loadHistory();
    
    if (history.records.length === 0) {
        console.log('📊 暂无历史记录');
        return;
    }
    
    let records = history.records;
    
    // 过滤代币
    if (token) {
        records = records.filter(r => r.token.toLowerCase() === token.toLowerCase());
    }
    
    // 按时间倒序
    records = records.sort((a, b) => b.timestamp - a.timestamp).slice(0, limit);
    
    console.log(`\n📊 收益率历史记录 ${token ? `(${token})` : ''}\n`);
    console.log(`时间                     代币  平台 (链)              APY      TVL`);
    console.log(`──────────────────────────────────────────────────────────────────────`);
    
    records.forEach(r => {
        const time = new Date(r.timestamp).toLocaleString('zh-CN', { 
            month: '2-digit', day: '2-digit', 
            hour: '2-digit', minute: '2-digit' 
        });
        const apyColor = r.apy > 20 ? '🟢' : r.apy > 10 ? '🟡' : '🔴';
        console.log(`${time}  ${r.token.padEnd(5)} ${r.platform.padEnd(10)} (${r.chain.padEnd(10)})  ${apyColor} ${r.apy.toFixed(2)}%   $${r.tvl >= 1000000 ? (r.tvl/1000000).toFixed(1) + 'M' : (r.tvl/1000).toFixed(0) + 'K'}`);
    });
    
    console.log(`\n💡 提示: node scripts/history.mjs USDT --limit 20`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🦈 YieldShark - 历史记录工具

用法:
  node scripts/history.mjs              # 查看所有历史
  node scripts/history.mjs USDT         # 查看 USDT 历史
  node scripts/history.mjs --limit 20   # 查看最近 20 条
  node scripts/history.mjs --clear      # 清空历史记录

选项:
  --help, -h     显示帮助
  --limit N      限制显示条数 (默认 10)
  --clear        清空历史记录
`);
    process.exit(0);
}

if (args.includes('--clear')) {
    if (fs.existsSync(HISTORY_FILE)) {
        fs.unlinkSync(HISTORY_FILE);
        console.log('✅ 历史记录已清空');
    } else {
        console.log('ℹ️  暂无历史记录');
    }
    process.exit(0);
}

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 10;
const token = args.find(a => !a.startsWith('--'));

showHistory(token, limit);
