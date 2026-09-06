// Shared .env auto-loader for coinos-skills.
// 各 skill 自包含 → 本文件在每个 skill 的 lib/ 下保留一份**字节相同**的副本,
// 由 scripts/validate-skills.mjs 的 drift guard 强制一致(改一处必须同步全部)。
//
// key 的规范存放位置(coinos 文件夹),不再靠"向上爬目录找 .env"的启发式:
//   - macOS / Linux: ~/.coinos/.env
//   - Windows:       %USERPROFILE%\.coinos\.env
//   - CoinClaw 容器: /workspace/.env (产品 web UI EnvSection → entrypoint 注入, 保留)
// 另外也读: 当前目录 .env(临时/项目本地)+ 旧引擎位置(~/.openclaw 等, 向后兼容, 最低优先级)。
//
// 规则: 候选按下面顺序, 同一个 key 先命中者生效; 已注入的 env(process.env)永远优先
// (if (!process.env[k]) 守卫)。所以把 key 放进 ~/.coinos/.env 后, 旧的 ~/.openclaw
// 免费 key 不会再抢 —— 它排在后面, 对应的 key 已经先被填上了。
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

const HOME = process.env.HOME || process.env.USERPROFILE || '';

// CoinClaw 容器 sentinel → 产品注入的 /workspace/.env。
function containerEnvFile() {
  if (existsSync('/workspace/.hermes') || existsSync('/workspace/.claude')) return '/workspace/.env';
  if (existsSync('/home/node/.openclaw')) return '/home/node/.openclaw/workspace/.env';
  return null;
}

// coinos 规范配置文件 —— 跨平台 ~/.coinos/.env(Windows: %USERPROFILE%\.coinos\.env)。
export function coinosEnvFile() {
  return HOME ? join(HOME, '.coinos', '.env') : null;
}

// 候选 .env 路径(有序;同一个 key 先命中者生效,且注入 env 永远优先)。
export function envCandidates() {
  const list = [];
  const container = containerEnvFile();
  if (container) list.push(container);               // 1. 容器: 产品注入位置
  const coinos = coinosEnvFile();
  if (coinos) list.push(coinos);                     // 2. ~/.coinos/.env —— 规范位置
  list.push(resolve(process.cwd(), '.env'));         // 3. 当前目录(临时/项目本地)
  if (HOME) {                                        // 4. 旧引擎位置, 向后兼容(最低优先级)
    list.push(resolve(HOME, '.openclaw', 'workspace', '.env'));
    list.push(resolve(HOME, '.openclaw', '.env'));
    list.push(resolve(HOME, '.hermes', '.env'));
  }
  return [...new Set(list)];
}

// 把候选 .env 载入 process.env,不覆盖已注入的变量。
export function loadEnv() {
  for (const envFile of envCandidates()) {
    try {
      for (const line of readFileSync(envFile, 'utf-8').split('\n')) {
        const t = line.trim();
        if (!t || t.startsWith('#')) continue;
        const eq = t.indexOf('=');
        if (eq < 1) continue;
        const k = t.slice(0, eq).trim();
        let v = t.slice(eq + 1).trim();
        if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
        if (!process.env[k]) process.env[k] = v;
      }
    } catch { /* 文件不存在或不可读,跳过 */ }
  }
}

// saveKey 应写入的 .env 路径 —— 规范位置 ~/.coinos/.env(容器内写 /workspace/.env)。
// 调用方写入前需 mkdir -p 父目录(~/.coinos 可能还不存在)。
export function writeEnvPath() {
  const container = containerEnvFile();
  if (container) return container;
  const coinos = coinosEnvFile();
  if (coinos) return coinos;
  return resolve(process.cwd(), '.env');
}
