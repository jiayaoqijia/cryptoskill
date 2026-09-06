// CoinClaw 三引擎(OpenClaw / Hermes / Claude Code)自动识别 helper.
//
// CoinClaw 把 freqtrade 起为 supervisord 管理的常驻 daemon, 端口 8080,
// Basic auth 用户名 'freqtrade', 密码写在容器内的 .ft_api_pass 文件.
// 三引擎的 workspace / userdir / strategy-path / config.json / .env 都
// 在不同位置, 但本 helper 屏蔽差异 — skill 脚本只关心 coinclawEnv() 返回值.
//
// 不在 CoinClaw 容器里运行(用户本地 macOS / Linux)时, coinclawEnv() 返回
// null, ft-deploy.mjs 会走 host 模式 (自己 git clone freqtrade + setup.sh).
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// 三引擎的真实 daemon 路径(--strategy-path / --userdir / --config 等都来自
// image-*/freqtrade-launch.sh 或 image/freqtrade-wait.sh 的 exec 行).
const ENGINES = [
  {
    engine: 'hermes',
    workspaceRoot: '/workspace',
    skillsRoot: '/workspace/.hermes/skills',
    freqtradeUserdir: '/workspace/freqtrade',
    strategyPath: '/workspace/strategies',
    configPath: '/workspace/freqtrade/config.json',
    envFile: '/workspace/.env',
    ftPassFile: '/workspace/.ft_api_pass',
    sentinelFile: '/workspace/.hermes',
  },
  {
    engine: 'claude-code',
    workspaceRoot: '/workspace',
    skillsRoot: '/workspace/.claude/skills',
    freqtradeUserdir: '/workspace/freqtrade',
    strategyPath: '/workspace/strategies',
    configPath: '/workspace/freqtrade/config.json',
    envFile: '/workspace/.env',
    ftPassFile: '/workspace/.ft_api_pass',
    sentinelFile: '/workspace/.claude',
  },
  {
    engine: 'openclaw',
    workspaceRoot: '/home/node/.openclaw/workspace',
    skillsRoot: '/home/node/.openclaw/workspace/skills',
    freqtradeUserdir: '/home/node/.openclaw/workspace/freqtrade',
    strategyPath: '/home/node/.openclaw/workspace/strategies',
    configPath: '/home/node/.openclaw/workspace/freqtrade/config.json',
    envFile: '/home/node/.openclaw/workspace/.env',
    ftPassFile: '/home/node/.openclaw/workspace/.ft_api_pass',
    sentinelFile: '/home/node/.openclaw',
  },
];

let _cached;

export function coinclawEnv() {
  if (_cached !== undefined) return _cached;
  // Hermes 和 CC 共用 /workspace, 但 sentinelFile 区分: .hermes vs .claude.
  // 顺序很重要: 先匹配 .hermes (Hermes 启动时一定有 /workspace/.hermes/),
  // 再匹配 .claude (CC), 最后兜底到 OpenClaw.
  for (const env of ENGINES) {
    if (existsSync(env.sentinelFile) && existsSync(env.configPath)) {
      _cached = { ...env, ftApiUser: 'freqtrade', ftApiUrl: 'http://127.0.0.1:8080' };
      return _cached;
    }
  }
  // Hermes/CC 把 /workspace/.openclaw/workspace/.env 软链到 /workspace/.env,
  // 但 sentinel 是 .hermes/.claude 而不是 .openclaw — 不会误识别成 OpenClaw.
  _cached = null;
  return null;
}

// 读 ft_api_pass 文件. 三引擎的 entrypoint.sh 都在第一次启动写一次,
// PVC 持久化, 之后只读不写. 文件不存在 / 读失败都返回 null, 让 caller
// 退到 .env 里的 FREQTRADE_PASSWORD (或 host 模式生成的随机密码).
export function readFtApiPass(env = coinclawEnv()) {
  if (!env || !existsSync(env.ftPassFile)) return null;
  try {
    return readFileSync(env.ftPassFile, 'utf-8').trim() || null;
  } catch {
    return null;
  }
}

// 用户在 chat 里填的交易所 / AiCoin / DRY_RUN 等都写到 .env,
// 三引擎共用. Host 模式下回退到 cwd / ~/.openclaw/workspace/.env.
export function envFileCandidates() {
  const env = coinclawEnv();
  if (env) return [env.envFile];
  return [
    resolve(process.env.HOME || '', '.coinos', '.env'),   // 规范位置(coinos 文件夹)
    resolve(process.cwd(), '.env'),
    resolve(process.env.HOME || '', '.openclaw', 'workspace', '.env'),
    resolve(process.env.HOME || '', '.openclaw', '.env'),
    resolve(process.env.HOME || '', '.hermes', '.env'),
  ];
}

// 给 host 模式用. 在 CoinClaw 容器外, ft-deploy.mjs 自己 clone freqtrade
// 到 ~/.freqtrade, 写策略到 ~/.freqtrade/user_data/strategies — 老路径,
// 不动. 只在 coinclawEnv() === null 时调用.
export function hostModeFreqtradePaths() {
  const home = process.env.HOME || '';
  const ftDir = resolve(home, '.freqtrade');
  const userData = resolve(ftDir, 'user_data');
  return {
    ftDir,
    sourceDir: resolve(ftDir, 'source'),
    venvDir: resolve(ftDir, 'source', '.venv'),
    userdir: userData,
    strategyPath: resolve(userData, 'strategies'),
    configPath: resolve(userData, 'config.json'),
    pidFile: resolve(ftDir, 'freqtrade.pid'),
    logFile: resolve(ftDir, 'freqtrade.log'),
    ftBin: resolve(ftDir, 'source', '.venv', 'bin', 'freqtrade'),
  };
}

// 判断是否能 supervisorctl(只有在 coinclaw 容器里有). 用于 ft.mjs 的
// restart_daemon action — supervisorctl 走 unix socket, 路径见
// image-*/supervisord.conf. 三引擎的 socket 位置略不同, 这里用 socket
// 实际路径而不是 supervisorctl 的默认 search.
export function supervisorSocket() {
  const env = coinclawEnv();
  if (!env) return null;
  if (env.engine === 'openclaw') return '/tmp/supervisor.sock';
  // Hermes/CC: file=/workspace/supervisor.sock
  return '/workspace/supervisor.sock';
}

// 仅供测试: 强制清缓存. 生产代码不要调用.
export function _resetCacheForTesting() {
  _cached = undefined;
}
