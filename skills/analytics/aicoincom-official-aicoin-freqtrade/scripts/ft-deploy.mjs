#!/usr/bin/env node
// ft-deploy.mjs — strategy lifecycle, backtest, hyperopt.
//
// 两套运行模式自动切换:
//   - CoinClaw 容器内 (OpenClaw / Hermes / Claude Code): freqtrade 已是
//     supervisord 管的常驻 daemon, 本脚本"部署策略" = 写策略文件 +
//     改 config.strategy + 重启 daemon. 不再 git clone freqtrade,
//     不再 nohup 后台进程, 不跟 daemon 抢 8080 端口.
//   - host 模式 (用户本地 macOS / Linux): 沿用老路径, 自己 clone freqtrade,
//     起后台进程, 写 PID file. 这条路在 coinclaw 之外仍然有效.
//
// coinclaw 模式下 strategy / backtest / 配置变更 都通过容器里预装的
// freqtrade CLI + freqtrade REST API 完成, 跟 dashboard 看到的状态保持一致.
import {
  readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync,
  readdirSync, renameSync, chmodSync,
} from 'node:fs';
import { resolve, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';

import {
  coinclawEnv, hostModeFreqtradePaths, envFileCandidates, supervisorSocket,
} from '../lib/coinclaw-env.mjs';
import { ftGet, ftPost } from '../lib/freqtrade-api.mjs';
import {
  buildStrategyCode, SAMPLE_STRATEGY,
  AVAILABLE_INDICATORS, AVAILABLE_AICOIN_DATA, PAID_DATA,
} from '../lib/strategy-builder.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));

// ─── 模式 / 路径解析 ─────────────────────────────────────────────
const ENV = coinclawEnv();
const HOST = hostModeFreqtradePaths();

// 三引擎下 STRAT_DIR / USER_DATA / CONFIG_PATH 直接来自 daemon 启动参数,
// 跟 dashboard / freqtrade /api/v1/show_config 保持完全一致 — 不会出现
// "agent 写到 ~/.freqtrade/user_data/strategies/ 但 daemon 不读" 这种坑.
const STRAT_DIR  = ENV ? ENV.strategyPath      : HOST.strategyPath;
const USER_DATA  = ENV ? ENV.freqtradeUserdir  : HOST.userdir;
const CONFIG_PATH = ENV ? ENV.configPath       : HOST.configPath;
const ENV_FILE   = ENV ? ENV.envFile           : envFileCandidates()[0]; // host: ~/.coinos/.env(规范位置, 与读路径最高优先级一致)

// FT_BIN 解析顺序:
//   1. coinclaw 容器: 'freqtrade' — image PATH 上已经有 (entrypoint
//      ENV PATH 包含 /home/node/.freqtrade/source/.venv/bin 或者
//      ftuser 的 ~/.local/bin), 直接用最干净.
//   2. host 模式优先 `command -v freqtrade` — 用户本地已经装过的
//      系统 freqtrade (brew / uv / 系统包) 直接复用. 老版本 ft-deploy
//      会 git clone freqtrade 重装一次 setup.sh, 多等几分钟 + 多占
//      ~500MB. 见 commit 50011b8.
//   3. host fallback: ~/.freqtrade/source/.venv/bin/freqtrade — 真
//      没有时才走 setup.sh 装到 venv.
const FT_BIN = ENV ? 'freqtrade' : (() => {
  try {
    const sys = execSync('command -v freqtrade', { encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    if (sys && existsSync(sys)) return sys;
  } catch {}
  return HOST.ftBin;
})();

// ─── 通用辅助 ─────────────────────────────────────────────────────
function run(cmd, opts = {}) {
  return execSync(cmd, { encoding: 'utf-8', timeout: 600000, ...opts }).trim();
}

function hasCommand(cmd) {
  try { run(`which ${cmd}`); return true; } catch { return false; }
}

// 轻量 env 读取 — freqtrade-api.mjs 已经 loadEnv() 一次, 这里是为了 host
// 模式下的 detectExchange / appendEnv 等动作能拿到最新值.
function loadEnv() {
  for (const file of envFileCandidates()) {
    if (!existsSync(file)) continue;
    try {
      for (const line of readFileSync(file, 'utf-8').split('\n')) {
        const t = line.trim();
        if (!t || t.startsWith('#')) continue;
        const eq = t.indexOf('=');
        if (eq < 1) continue;
        const key = t.slice(0, eq).trim();
        let val = t.slice(eq + 1).trim();
        if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) val = val.slice(1, -1);
        if (!process.env[key]) process.env[key] = val;
      }
    } catch {}
  }
}
loadEnv();

function appendEnv(key, val) {
  try { mkdirSync(dirname(ENV_FILE), { recursive: true }); } catch {} // ~/.coinos 可能还不存在
  if (!existsSync(ENV_FILE)) {
    writeFileSync(ENV_FILE, `${key}=${val}\n`);
    try { chmodSync(ENV_FILE, 0o600); } catch {}
    return;
  }
  const content = readFileSync(ENV_FILE, 'utf-8');
  const lines = content.split('\n');
  const idx = lines.findIndex((l) => l.trim().startsWith(`${key}=`));
  if (idx >= 0) {
    lines[idx] = `${key}=${val}`;
    writeFileSync(ENV_FILE, lines.join('\n'));
  } else {
    writeFileSync(ENV_FILE, content.trimEnd() + `\n${key}=${val}\n`);
  }
}

// 在三引擎容器里 .env 同时承载交易所 key + AiCoin key + DRY_RUN +
// SELECTED_EXCHANGE, agent 直接告诉用户去 EnvSection 改, 不在脚本里写.
// host 模式下沿用老的"自己 nohup freqtrade"流程, 才需要这个 detectExchange.
function detectExchange() {
  const exchanges = ['BINANCE', 'OKX', 'BYBIT', 'BITGET', 'GATE', 'HTX', 'KUCOIN', 'MEXC'];
  for (const ex of exchanges) {
    if (process.env[`${ex}_API_KEY`] && process.env[`${ex}_API_SECRET`]) {
      return {
        name: ex.toLowerCase(),
        key: process.env[`${ex}_API_KEY`],
        secret: process.env[`${ex}_API_SECRET`],
        password: process.env[`${ex}_PASSWORD`] || '',
      };
    }
  }
  return null;
}

// ─── coinclaw 模式: daemon 操作 ──────────────────────────────────
function readDaemonConfig() {
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

function writeDaemonConfig(cfg) {
  const bak = `${CONFIG_PATH}.bak`;
  copyFileSync(CONFIG_PATH, bak);
  try { chmodSync(bak, 0o600); } catch {}
  const tmp = `${CONFIG_PATH}.tmp.${process.pid}`;
  writeFileSync(tmp, JSON.stringify(cfg, null, 4) + '\n');
  try { chmodSync(tmp, 0o600); } catch {}
  renameSync(tmp, CONFIG_PATH);
  try { chmodSync(CONFIG_PATH, 0o600); } catch {}
}

function restartDaemon() {
  if (!ENV) throw new Error('restart daemon 仅在 coinclaw 容器内可用');
  const sock = supervisorSocket();
  try {
    execSync(`supervisorctl -s unix://${sock} restart freqtrade`, {
      stdio: 'pipe', timeout: 30000,
    });
    return { method: 'supervisorctl' };
  } catch (e) {
    try {
      const pid = run("pgrep -f 'freqtrade trade' | head -n1");
      if (pid) {
        process.kill(Number(pid), 'SIGTERM');
        return { method: 'kill+autorestart', pid: Number(pid) };
      }
    } catch {}
    throw new Error(`restart 失败: ${e.message}`);
  }
}

// 通过 dump+grep ps 拿 daemon 当前用的 strategy / pair_whitelist 等运行
// 时配置. /api/v1/show_config 是最稳的来源, 跟 freqtrade UI/dashboard 一致.
async function fetchDaemonState() {
  try {
    const cfg = await ftGet('show_config');
    return { online: true, ...cfg };
  } catch (e) {
    return { online: false, error: e.message };
  }
}

// ─── host 模式: 自己管 freqtrade 进程 ───────────────────────────
function getHostPid() {
  if (!HOST.pidFile || !existsSync(HOST.pidFile)) return null;
  const pid = readFileSync(HOST.pidFile, 'utf-8').trim();
  if (!pid) return null;
  try { process.kill(Number(pid), 0); return Number(pid); } catch { return null; }
}

function findPython() {
  const names = ['python3.13', 'python3.12', 'python3.11', 'python3'];
  const extraDirs = ['/opt/homebrew/bin', '/usr/local/bin', `${process.env.HOME}/.local/bin`];
  const candidates = [...names];
  for (const dir of extraDirs) {
    for (const n of names.slice(0, 3)) candidates.push(resolve(dir, n));
  }
  for (const bin of candidates) {
    try {
      const version = run(`${bin} --version`);
      const match = version.match(/(\d+)\.(\d+)/);
      if (match) {
        const major = Number(match[1]); const minor = Number(match[2]);
        if (major === 3 && minor >= 11) return { bin, major, minor, version };
      }
    } catch {}
  }
  return null;
}

function ensureModernPython() {
  let py = findPython();
  if (py) return py;

  if (process.platform === 'darwin') {
    try {
      const uvBin = resolve(process.env.HOME || '', '.local', 'bin', 'uv');
      if (!existsSync(uvBin)) {
        console.error('Installing uv (fast Python manager)...');
        run('curl -LsSf https://astral.sh/uv/install.sh | sh', { timeout: 60000 });
      }
      if (existsSync(uvBin)) {
        console.error('Installing Python 3.12 via uv...');
        run(`${uvBin} python install 3.12`, { timeout: 300000 });
        try {
          const pyPath = run(`${uvBin} python find 3.12`);
          if (pyPath) {
            const ver = run(`${pyPath} --version`);
            const m = ver.match(/(\d+)\.(\d+)/);
            if (m && Number(m[1]) === 3 && Number(m[2]) >= 11) {
              return { bin: pyPath, major: Number(m[1]), minor: Number(m[2]), version: ver };
            }
          }
        } catch {}
      }
    } catch (e) { console.error(`uv: ${e.message}`); }

    try {
      if (hasCommand('brew')) {
        console.error('Trying brew install python@3.12...');
        const brewEnv = { ...process.env, HOMEBREW_NO_AUTO_UPDATE: '1', HOMEBREW_NO_INSTALL_CLEANUP: '1' };
        run('brew install python@3.12', { timeout: 300000, env: brewEnv });
        py = findPython();
        if (py) return py;
      }
    } catch (e) { console.error(`brew: ${e.message}`); }
  }

  throw new Error('Python 3.11+ required. Install options:\n• curl -LsSf https://astral.sh/uv/install.sh | sh && uv python install 3.12\n• brew install python@3.12\n• https://www.python.org/downloads/');
}

function generateHostConfig(exchangeInfo, apiPassword, params = {}) {
  const config = {
    trading_mode: params.trading_mode || 'futures',
    margin_mode: params.margin_mode || 'isolated',
    max_open_trades: params.max_open_trades || 3,
    stake_currency: 'USDT',
    stake_amount: params.stake_amount || 'unlimited',
    tradable_balance_ratio: params.tradable_balance_ratio || 0.5,
    dry_run: params.dry_run !== false,
    dry_run_wallet: 1000,
    cancel_open_orders_on_exit: false,
    exchange: {
      name: exchangeInfo.name,
      key: exchangeInfo.key,
      secret: exchangeInfo.secret,
      ...(exchangeInfo.password ? { password: exchangeInfo.password } : {}),
      ccxt_config: {},
      ccxt_async_config: {},
      pair_whitelist: params.pairs || ['BTC/USDT:USDT', 'ETH/USDT:USDT'],
      pair_blacklist: [],
    },
    pairlists: [{ method: 'StaticPairList' }],
    entry_pricing: { price_side: 'same', use_order_book: true, order_book_top: 1 },
    exit_pricing: { price_side: 'same', use_order_book: true, order_book_top: 1 },
    api_server: {
      enabled: true,
      listen_ip_address: '127.0.0.1',
      listen_port: 8080,
      verbosity: 'error',
      enable_openapi: false,
      jwt_secret_key: randomBytes(16).toString('hex'),
      CORS_origins: [],
      // freqtrade 三引擎容器里 daemon user 都是 'freqtrade', host 模式跟齐 —
      // 老版本默认 'freqtrader' 跟容器不一致, 历史 bug.
      username: 'freqtrade',
      password: apiPassword,
    },
    bot_name: 'aicoin-freqtrade',
    initial_state: 'running',
    force_entry_enable: true,
    internals: { process_throttle_secs: 5 },
  };
  const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
  if (proxyUrl) {
    config.exchange.ccxt_config.proxies = { https: proxyUrl, http: proxyUrl };
    config.exchange.ccxt_async_config.aiohttp_proxy = proxyUrl;
    config.exchange.enable_ws = false;
  }
  return config;
}

// ─── 公共: 复制 AiCoin SDK + 模板策略到 strategy 目录 ────────────
// 三引擎容器 image 已经在 build time 把 aicoin_data.py 复制到了 strategy
// 目录(image-*/Dockerfile + image/Dockerfile), 所以 coinclaw 模式下这一步
// 是幂等的 no-op, 但留着保证 host 模式 + agent 第一次 create_strategy 时
// 能拿到 SDK.
function ensureSdkAndTemplates() {
  mkdirSync(STRAT_DIR, { recursive: true });
  const skillDir = resolve(__dir, '..');
  const sdkSrc = resolve(skillDir, 'lib', 'aicoin_data.py');
  const defaultsSrc = resolve(skillDir, 'lib', 'defaults.json');
  const strategiesSrc = resolve(skillDir, 'strategies');

  if (existsSync(sdkSrc)) {
    const sdkDest = resolve(STRAT_DIR, 'aicoin_data.py');
    if (!existsSync(sdkDest)) copyFileSync(sdkSrc, sdkDest);
  }
  if (existsSync(defaultsSrc)) {
    const dDest = resolve(STRAT_DIR, 'defaults.json');
    if (!existsSync(dDest)) copyFileSync(defaultsSrc, dDest);
  }
  if (existsSync(strategiesSrc)) {
    for (const f of readdirSync(strategiesSrc)) {
      if (f.endsWith('.py')) {
        const dest = resolve(STRAT_DIR, f);
        if (!existsSync(dest)) copyFileSync(resolve(strategiesSrc, f), dest);
      }
    }
  }
}

// ─── Actions ─────────────────────────────────────────────────────
const actions = {
  // ── check ──────────────────────────────────────────────────────
  // coinclaw 模式: ping daemon + show_config + balance.
  // host 模式: 检查 python / git / freqtrade installed / pid.
  check: async () => {
    if (ENV) {
      const checks = { mode: 'coinclaw', engine: ENV.engine, paths: {
        userdir: USER_DATA, strategy_path: STRAT_DIR, config: CONFIG_PATH,
      }};
      const state = await fetchDaemonState();
      checks.daemon_online = state.online;
      if (state.online) {
        checks.strategy = state.strategy;
        checks.exchange = state.exchange;
        checks.dry_run = state.dry_run;
        checks.timeframe = state.timeframe;
        checks.trading_mode = state.trading_mode;
        try {
          const bal = await ftGet('balance');
          checks.total = bal.total;
          checks.starting_capital = bal.starting_capital;
          checks.stake_currency = bal.stake;
        } catch (e) { checks.balance_error = e.message; }
      } else {
        checks.note = '在 coinclaw 容器里 daemon 由 supervisord 管理, 它没起来通常是 cold-start 卡住或 config 写错; 看 /workspace/logs/freqtrade-error.log 或 /home/node/.openclaw/workspace/.freqtrade/logs/';
      }
      return checks;
    }
    // host mode
    const checks = { mode: 'host' };
    const py = findPython();
    checks.python = py ? `${py.version} (${py.bin})` : false;
    if (!py) {
      try {
        const v = run('python3 --version');
        checks.python_warning = `${v} found but Freqtrade requires 3.11+. Deploy will auto-install 3.12.`;
      } catch {}
    }
    checks.git = hasCommand('git');
    checks.source_cloned = existsSync(resolve(HOST.sourceDir, 'setup.sh'));
    checks.freqtrade_installed = existsSync(FT_BIN);
    if (checks.freqtrade_installed) {
      try { checks.freqtrade_version = run(`${FT_BIN} --version`); } catch {}
    }
    const ex = detectExchange();
    checks.exchange = ex ? { name: ex.name, configured: true } : { configured: false };
    const pid = getHostPid();
    checks.running = !!pid;
    if (pid) checks.pid = pid;
    checks.ready = (!!py || process.platform === 'darwin') && checks.git && checks.exchange?.configured;
    if (!checks.ready) {
      checks.missing = [];
      if (!py && process.platform !== 'darwin') checks.missing.push('Python 3.11+ not found');
      if (!checks.git) checks.missing.push('git not found');
      if (!checks.exchange?.configured) checks.missing.push('No exchange API keys in .env');
    }
    return checks;
  },

  // ── deploy ─────────────────────────────────────────────────────
  // coinclaw 模式: 写策略 (如果 caller 已 create_strategy 就是 no-op) +
  //   改 config.strategy + 重启 daemon. 不再 git clone, 不再 nohup.
  // host 模式: 沿用老路径 (clone + setup.sh + nohup).
  deploy: async (params = {}) => {
    if (ENV) {
      const strategy = params.strategy;
      if (!strategy) throw new Error('strategy 必填, 例: {"strategy":"MyStrat"}');
      const stratFile = resolve(STRAT_DIR, `${strategy}.py`);
      if (!existsSync(stratFile)) {
        throw new Error(`策略文件不存在: ${stratFile}. 先用 ft-deploy.mjs create_strategy 或 Write 工具写文件到 ${STRAT_DIR}/`);
      }
      const cfg = readDaemonConfig();
      const before = { strategy: cfg.strategy, dry_run: cfg.dry_run, pairs: cfg.exchange?.pair_whitelist };
      cfg.strategy = strategy;
      // 允许在 deploy 里同时改 dry_run / pairs / max_open_trades, 一次完成.
      if (typeof params.dry_run === 'boolean') cfg.dry_run = params.dry_run;
      if (Array.isArray(params.pairs) && params.pairs.length) {
        if (!cfg.exchange) cfg.exchange = {};
        cfg.exchange.pair_whitelist = params.pairs;
      }
      if (params.max_open_trades) cfg.max_open_trades = params.max_open_trades;
      writeDaemonConfig(cfg);
      const restart = restartDaemon();
      return {
        success: true, mode: 'coinclaw', engine: ENV.engine,
        strategy, before, restart,
        config_path: CONFIG_PATH, strategy_file: stratFile,
        note: '策略生效需 daemon 重启完成 (10-30s); dashboard 会自动刷新到新策略名',
        warning: cfg.dry_run === false
          ? '⚠️ 已切到实盘 — 真实交易, 真实亏损. 确认 .env 里交易所 key 正确, 余额可控.'
          : null,
      };
    }
    // host mode (老逻辑, 保留不动)
    const py = ensureModernPython();
    console.error(`Using ${py.version} (${py.bin})`);
    if (!hasCommand('git')) throw new Error('git not found.');
    let exchangeInfo = detectExchange();
    if (!exchangeInfo) {
      if (params.dry_run !== false) {
        const exName = params.exchange || 'binance';
        exchangeInfo = { name: exName, key: 'dry-run', secret: 'dry-run' };
        console.error(`No exchange API keys found — using dummy keys for dry-run (${exName})`);
      } else {
        throw new Error('No exchange API keys found in .env (required for live trading)');
      }
    }
    mkdirSync(STRAT_DIR, { recursive: true });
    ensureSdkAndTemplates();
    if (!existsSync(FT_BIN)) {
      if (!existsSync(resolve(HOST.sourceDir, 'setup.sh'))) {
        console.error('Cloning Freqtrade repository...');
        run(`git clone https://github.com/freqtrade/freqtrade.git ${HOST.sourceDir}`, { timeout: 120000 });
        run(`cd ${HOST.sourceDir} && git checkout stable`, { timeout: 30000 });
      }
      console.error('Running Freqtrade setup.sh (this may take a few minutes)...');
      const pyDir = dirname(py.bin);
      const setupEnv = { ...process.env, PATH: `${pyDir}:${process.env.PATH}` };
      run(`cd ${HOST.sourceDir} && ./setup.sh -i`, { timeout: 600000, env: setupEnv });
      if (!existsSync(FT_BIN)) throw new Error('Freqtrade installation failed.');
    }
    const apiPassword = randomBytes(8).toString('hex');
    const config = generateHostConfig(exchangeInfo, apiPassword, params);
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
    try { chmodSync(CONFIG_PATH, 0o600); } catch {} // config.json 含明文交易所 key/secret, 收紧权限
    const samplePath = resolve(STRAT_DIR, 'SampleStrategy.py');
    if (!existsSync(samplePath)) writeFileSync(samplePath, SAMPLE_STRATEGY);
    const oldPid = getHostPid();
    if (oldPid) { try { process.kill(oldPid, 'SIGTERM'); } catch {} }
    const strategy = params.strategy || 'SampleStrategy';
    const stratFile = resolve(STRAT_DIR, `${strategy}.py`);
    if (strategy !== 'SampleStrategy' && !existsSync(stratFile)) {
      throw new Error(`Strategy "${strategy}" not found at ${stratFile}. Use create_strategy first.`);
    }
    const proxyEnv = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
    const proxyPrefix = proxyEnv ? `env HTTPS_PROXY=${proxyEnv} HTTP_PROXY=${proxyEnv} ` : '';
    run(`nohup ${proxyPrefix}${FT_BIN} trade --config ${CONFIG_PATH} --strategy ${strategy} --userdir ${USER_DATA} > ${HOST.logFile} 2>&1 & echo $! > ${HOST.pidFile}`);
    let ready = false;
    for (let i = 0; i < 15; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      const pid = getHostPid();
      if (pid) {
        try {
          const res = await fetch(`http://127.0.0.1:8080/api/v1/ping`, {
            headers: { Authorization: 'Basic ' + Buffer.from(`freqtrade:${apiPassword}`).toString('base64') },
            signal: AbortSignal.timeout(3000),
          });
          if (res.ok) { ready = true; break; }
        } catch {}
      }
    }
    appendEnv('FREQTRADE_URL', 'http://127.0.0.1:8080');
    appendEnv('FREQTRADE_USERNAME', 'freqtrade');
    appendEnv('FREQTRADE_PASSWORD', apiPassword);
    return {
      success: true, mode: 'host',
      exchange: exchangeInfo.name, strategy, dry_run: config.dry_run,
      pairs: config.exchange.pair_whitelist,
      api_url: 'http://127.0.0.1:8080', api_auth: 'stored in .env (FREQTRADE_PASSWORD)',
      pid: getHostPid(), ready, log_file: HOST.logFile, config_path: CONFIG_PATH,
      strategies_dir: STRAT_DIR,
      note: config.dry_run ? 'Running in DRY-RUN mode' : 'WARNING: Running in LIVE mode',
    };
  },

  // ── update ─────────────────────────────────────────────────────
  update: async () => {
    if (ENV) {
      return {
        skipped: true, mode: 'coinclaw',
        note: '在 coinclaw 容器里 freqtrade 由 image 预装, 升级请 helm upgrade 整个 instance (web 端有"升级"按钮), 不能在容器里 git pull',
      };
    }
    if (!existsSync(resolve(HOST.sourceDir, 'setup.sh'))) {
      return { error: 'Freqtrade not installed. Run deploy first.' };
    }
    const pid = getHostPid();
    if (pid) { try { process.kill(pid, 'SIGTERM'); } catch {} }
    console.error('Updating Freqtrade...');
    run(`cd ${HOST.sourceDir} && ./setup.sh -u`, { timeout: 600000 });
    return { updated: true, mode: 'host', note: 'Run start to restart Freqtrade.' };
  },

  // ── status ─────────────────────────────────────────────────────
  status: async () => {
    if (ENV) {
      const state = await fetchDaemonState();
      const result = { mode: 'coinclaw', engine: ENV.engine, ...state };
      // tail freqtrade 日志, 三引擎日志位置不同.
      const logCandidates = [
        '/workspace/logs/freqtrade.log',
        '/workspace/logs/freqtrade-error.log',
      ];
      for (const log of logCandidates) {
        if (existsSync(log)) {
          try { result.last_logs = run(`tail -10 ${log}`); break; } catch {}
        }
      }
      return result;
    }
    const pid = getHostPid();
    if (!pid) return { mode: 'host', running: false };
    let lastLogs = '';
    try { lastLogs = run(`tail -5 ${HOST.logFile} 2>/dev/null`); } catch {}
    return { mode: 'host', running: true, pid, log_file: HOST.logFile, last_logs: lastLogs };
  },

  // ── stop / start ───────────────────────────────────────────────
  // coinclaw 模式: supervisorctl. host 模式: SIGTERM pid.
  stop: async () => {
    if (ENV) {
      const sock = supervisorSocket();
      try {
        run(`supervisorctl -s unix://${sock} stop freqtrade`);
        return { stopped: true, mode: 'coinclaw', method: 'supervisorctl' };
      } catch (e) {
        return { stopped: false, error: e.message, note: 'supervisorctl 不可达, 试试 ft.mjs stop (REST)' };
      }
    }
    const pid = getHostPid();
    if (!pid) return { stopped: false, mode: 'host', reason: 'Not running' };
    try { process.kill(pid, 'SIGTERM'); } catch {}
    try { writeFileSync(HOST.pidFile, ''); } catch {}
    return { stopped: true, mode: 'host', pid };
  },

  start: async (params = {}) => {
    if (ENV) {
      const sock = supervisorSocket();
      try {
        run(`supervisorctl -s unix://${sock} start freqtrade`);
        return { started: true, mode: 'coinclaw', method: 'supervisorctl' };
      } catch (e) {
        return { started: false, error: e.message };
      }
    }
    if (getHostPid()) return { started: false, mode: 'host', reason: 'Already running' };
    if (!existsSync(FT_BIN)) throw new Error('Freqtrade not installed. Run deploy first.');
    if (!existsSync(CONFIG_PATH)) throw new Error('No config found. Run deploy first.');
    const strategy = params.strategy || 'SampleStrategy';
    const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
    const proxyPrefix = proxyUrl ? `env HTTPS_PROXY=${proxyUrl} HTTP_PROXY=${proxyUrl} ` : '';
    run(`nohup ${proxyPrefix}${FT_BIN} trade --config ${CONFIG_PATH} --strategy ${strategy} --userdir ${USER_DATA} > ${HOST.logFile} 2>&1 & echo $! > ${HOST.pidFile}`);
    await new Promise((r) => setTimeout(r, 3000));
    return { started: true, mode: 'host', pid: getHostPid() };
  },

  // ── logs ───────────────────────────────────────────────────────
  // coinclaw 模式: tail /workspace/logs/freqtrade.log (supervisord 写在那).
  // host 模式: tail freqtrade.log.
  logs: async ({ lines = 50 } = {}) => {
    if (ENV) {
      for (const log of ['/workspace/logs/freqtrade.log', '/workspace/logs/freqtrade-error.log']) {
        if (existsSync(log)) {
          try { return { mode: 'coinclaw', log_file: log, logs: run(`tail -${lines} ${log}`) }; } catch {}
        }
      }
      return { mode: 'coinclaw', logs: '(no log file found in /workspace/logs)' };
    }
    try { return { mode: 'host', logs: run(`tail -${lines} ${HOST.logFile} 2>/dev/null`) }; }
    catch { return { mode: 'host', logs: 'No log file found' }; }
  },

  // ── backtest ───────────────────────────────────────────────────
  // 两边都用 freqtrade backtesting CLI; 区别只在路径.
  // coinclaw 模式跑 backtest 不影响 daemon: backtesting 走自己的进程,
  // 跟 daemon 共用 user_data 但不共用 :8080.
  backtest: async (params = {}) => {
    if (!existsSync(FT_BIN) && !ENV) throw new Error('Freqtrade not installed. Run deploy first.');
    if (!existsSync(CONFIG_PATH)) {
      mkdirSync(dirname(CONFIG_PATH), { recursive: true });
      const exchange = params.exchange || 'binance';
      const cfg = generateHostConfig(
        { name: exchange, key: 'backtest-only', secret: 'backtest-only' },
        randomBytes(8).toString('hex'),
        { dry_run: true, pairs: params.pairs || ['BTC/USDT:USDT'] },
      );
      writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
      console.error(`Auto-created backtest config (exchange: ${exchange})`);
    }
    const strategy = params.strategy || 'SampleStrategy';
    const stratFile = resolve(STRAT_DIR, `${strategy}.py`);
    if (!existsSync(stratFile)) {
      throw new Error(`Strategy "${strategy}" not found at ${stratFile}. Use create_strategy or list with strategy_list.`);
    }
    const timeframe = params.timeframe || '1h';
    const timerange = params.timerange || '';
    const timerangeArg = timerange ? ` --timerange ${timerange}` : '';
    const pairs = params.pairs;
    const pairsArg = pairs ? ` -p ${(Array.isArray(pairs) ? pairs : [pairs]).join(' ')}` : '';

    const proxyEnv = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
    const proxyPrefix = proxyEnv ? `env HTTPS_PROXY=${proxyEnv} HTTP_PROXY=${proxyEnv} ` : '';

    console.error('Downloading historical data...');
    try {
      run(
        `${proxyPrefix}${FT_BIN} download-data --config ${CONFIG_PATH} --timeframe ${timeframe}${timerangeArg}${pairsArg} --userdir ${USER_DATA}`,
        { timeout: 300000 }
      );
    } catch (e) {
      console.error(`Data download warning: ${e.message}`);
    }

    console.error(`Running backtest: strategy=${strategy}, timeframe=${timeframe}${timerange ? `, timerange=${timerange}` : ''}...`);
    const rawOutput = run(
      `${proxyPrefix}${FT_BIN} backtesting --config ${CONFIG_PATH} --strategy ${strategy} --strategy-path ${STRAT_DIR} --timeframe ${timeframe}${timerangeArg}${pairsArg} --userdir ${USER_DATA}`,
      { timeout: 600000 }
    );
    const output = rawOutput
      .split('\n')
      .filter((l) => !l.includes('INFO') || l.includes('TOTAL') || l.includes('Result') || l.includes('trades') || l.includes('Profit') || l.includes('Drawdown') || l.includes('Win') || l.includes('Avg'))
      .join('\n')
      .replace(/\b127\.0\.0\.1:\d+\b/g, '[local]')
      .replace(/https?:\/\/\d+\.\d+\.\d+\.\d+:\d+/g, '[proxy]');
    return { mode: ENV ? 'coinclaw' : 'host', strategy, timeframe, timerange: timerange || 'all available', output };
  },

  // ── download_data ──────────────────────────────────────────────
  download_data: async (params = {}) => {
    if (!existsSync(FT_BIN) && !ENV) throw new Error('Freqtrade not installed. Run deploy first.');
    if (!existsSync(CONFIG_PATH)) {
      mkdirSync(dirname(CONFIG_PATH), { recursive: true });
      const exchange = params.exchange || 'binance';
      const cfg = generateHostConfig(
        { name: exchange, key: 'download-only', secret: 'download-only' },
        randomBytes(8).toString('hex'),
        { dry_run: true, pairs: params.pairs || ['BTC/USDT:USDT'] },
      );
      writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
    }
    const timeframe = params.timeframe || '1h';
    const timerange = params.timerange || '';
    const timerangeArg = timerange ? ` --timerange ${timerange}` : '';

    const proxyEnv = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
    const proxyPrefix = proxyEnv ? `env HTTPS_PROXY=${proxyEnv} HTTP_PROXY=${proxyEnv} ` : '';

    console.error(`Downloading data: timeframe=${timeframe}${timerange ? `, timerange=${timerange}` : ''}...`);
    const output = run(
      `${proxyPrefix}${FT_BIN} download-data --config ${CONFIG_PATH} --timeframe ${timeframe}${timerangeArg} --userdir ${USER_DATA}`,
      { timeout: 300000 }
    );
    return { mode: ENV ? 'coinclaw' : 'host', timeframe, timerange: timerange || 'all available', output };
  },

  // ── hyperopt ───────────────────────────────────────────────────
  hyperopt: async (params = {}) => {
    if (!existsSync(FT_BIN) && !ENV) throw new Error('Freqtrade not installed.');
    if (!existsSync(CONFIG_PATH)) {
      mkdirSync(dirname(CONFIG_PATH), { recursive: true });
      const exchange = params.exchange || 'binance';
      const cfg = generateHostConfig(
        { name: exchange, key: 'hyperopt-only', secret: 'hyperopt-only' },
        randomBytes(8).toString('hex'),
        { dry_run: true, pairs: params.pairs || ['BTC/USDT:USDT'] },
      );
      writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
    }

    const strategy = params.strategy || 'SampleStrategy';
    const stratFile = resolve(STRAT_DIR, `${strategy}.py`);
    if (!existsSync(stratFile)) throw new Error(`Strategy "${strategy}" not found at ${stratFile}.`);
    const timeframe = params.timeframe || '1h';
    const timerange = params.timerange || '';
    const epochs = Math.min(Number(params.epochs) || 100, 500);
    const spaces = params.spaces || 'roi stoploss trailing buy sell';
    const jobs = Math.min(Number(params.jobs) || 1, 4);
    const lossFunc = params.loss || 'SharpeHyperOptLoss';
    const minTrades = params.min_trades || 20;
    const timerangeArg = timerange ? ` --timerange ${timerange}` : '';

    const proxyEnv = process.env.PROXY_URL || process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
    const proxyPrefix = proxyEnv ? `env HTTPS_PROXY=${proxyEnv} HTTP_PROXY=${proxyEnv} ` : '';

    try {
      run(
        `${proxyPrefix}${FT_BIN} download-data --config ${CONFIG_PATH} --timeframe ${timeframe}${timerangeArg} --userdir ${USER_DATA}`,
        { timeout: 300000 }
      );
    } catch (e) { console.error(`Data download warning: ${e.message}`); }

    console.error(`Running hyperopt: strategy=${strategy}, epochs=${epochs}, jobs=${jobs}, spaces=${spaces}`);
    const output = run(
      `${proxyPrefix}${FT_BIN} hyperopt --config ${CONFIG_PATH} --strategy ${strategy} --strategy-path ${STRAT_DIR} --timeframe ${timeframe}${timerangeArg} --userdir ${USER_DATA} --hyperopt-loss ${lossFunc} --spaces ${spaces} --epochs ${epochs} -j ${jobs} --min-trades ${minTrades}`,
      { timeout: 1800000 }
    );

    return { mode: ENV ? 'coinclaw' : 'host', strategy, timeframe, epochs, spaces, jobs, loss_function: lossFunc, output };
  },

  // ── create_strategy ────────────────────────────────────────────
  // 写策略文件到 STRAT_DIR (三引擎下分别是 daemon 真读的路径).
  create_strategy: async (params = {}) => {
    let name = params.name;
    if (!name) throw new Error('name is required. Example: {"name":"MyStrategy","timeframe":"15m","indicators":["rsi","macd"],"aicoin_data":["funding_rate"]}');
    name = name.replace(/[^A-Za-z0-9_]/g, '');
    if (name && /^[a-z]/.test(name)) name = name[0].toUpperCase() + name.slice(1);
    if (!/^[A-Z][A-Za-z0-9_]+$/.test(name)) throw new Error('name must be a valid Python class name starting with uppercase (e.g. MyStrategy)');

    ensureSdkAndTemplates();
    const dest = resolve(STRAT_DIR, `${name}.py`);
    const tf = params.timeframe || '15m';
    const desc = params.description || 'Custom strategy';
    const ds = new Set(params.aicoin_data || []);
    const indicators = params.indicators || null;
    const entryLogic = params.entry_logic || null;
    const exitLogic = params.exit_logic || null;
    const direction = params.direction || 'long';

    if (!['long', 'short', 'both'].includes(direction)) {
      throw new Error(`direction must be "long", "short", or "both" (default: "long")`);
    }

    if (indicators) {
      const invalid = indicators.filter((i) => !AVAILABLE_INDICATORS.includes(i.toLowerCase()));
      if (invalid.length > 0) {
        throw new Error(`Unknown indicators: ${invalid.join(', ')}. Available: ${AVAILABLE_INDICATORS.join(', ')}`);
      }
    }

    const KEY = process.env.AICOIN_ACCESS_KEY_ID || '';
    const defaultKey = JSON.parse(readFileSync(resolve(__dir, '..', 'lib', 'defaults.json'), 'utf-8')).accessKeyId || '';
    const usingFreeKey = !KEY || KEY === defaultKey;
    const paidUsed = [...ds].filter((d) => d in PAID_DATA);

    const code = buildStrategyCode(name, tf, desc, ds, indicators, entryLogic, exitLogic, direction);
    writeFileSync(dest, code);

    const result = {
      success: true, strategy: name, file: dest,
      mode: ENV ? 'coinclaw' : 'host', engine: ENV ? ENV.engine : null,
      timeframe: tf, direction,
      indicators: indicators || ['rsi', 'bb', 'ema', 'volume_sma'],
      aicoin_data: [...ds],
      note: ds.size
        ? `Strategy uses AiCoin data (${[...ds].join(', ')}) in live/dry_run. Falls back to pure technical indicators in backtest.`
        : 'Pure technical indicator strategy. To add AiCoin data, pass aicoin_data array.',
      next: ENV
        ? `策略文件已写; 用 deploy {"strategy":"${name}"} 让常驻 daemon 切到这个策略 (会触发 ~30s 重启), 或先 backtest 验证`
        : `Use deploy {"strategy":"${name}"} to start in dry-run, or backtest first`,
      available_indicators: AVAILABLE_INDICATORS,
      available_aicoin_data: AVAILABLE_AICOIN_DATA,
    };

    if (usingFreeKey && paidUsed.length > 0) {
      result.warning = `PAID KEY REQUIRED — Strategy uses ${paidUsed.map((d) => `${d} (${PAID_DATA[d]})`).join(', ')} but no paid API key is configured. These data sources will silently fall back to defaults in live mode. Get key at https://www.aicoin.com/opendata → add AICOIN_ACCESS_KEY_ID & AICOIN_ACCESS_SECRET to .env.`;
    }

    return result;
  },

  // ── strategy_list ──────────────────────────────────────────────
  strategy_list: async () => {
    const files = [];
    if (existsSync(STRAT_DIR)) {
      for (const f of readdirSync(STRAT_DIR)) {
        if (f.endsWith('.py') && f !== '__init__.py' && f !== 'aicoin_data.py') {
          files.push(f.replace('.py', ''));
        }
      }
    }
    return { mode: ENV ? 'coinclaw' : 'host', strategies: files, path: STRAT_DIR };
  },

  // ── remove ─────────────────────────────────────────────────────
  remove: async () => {
    if (ENV) {
      return {
        skipped: true, mode: 'coinclaw',
        note: '在 coinclaw 容器里 freqtrade 是常驻 daemon, 不能 remove. 用 stop 停 daemon, 或 deploy {"strategy":"NoOpStrategy"} 切到空跑策略, 或在 web UI 删整个 instance',
      };
    }
    const pid = getHostPid();
    if (pid) { try { process.kill(pid, 'SIGTERM'); } catch {} }
    try { writeFileSync(HOST.pidFile, ''); } catch {}
    return { removed: true, mode: 'host', note: `Process stopped. Config preserved.` };
  },

  // ── backtest_results ───────────────────────────────────────────
  backtest_results: async () => {
    const resultsDir = resolve(USER_DATA, 'backtest_results');
    if (!existsSync(resultsDir)) return { mode: ENV ? 'coinclaw' : 'host', results: [], path: resultsDir };
    const files = readdirSync(resultsDir)
      .filter((f) => f.endsWith('.meta.json'))
      .map((f) => {
        try {
          const meta = JSON.parse(readFileSync(resolve(resultsDir, f), 'utf-8'));
          const strategy = Object.keys(meta)[0] || 'unknown';
          const info = meta[strategy] || {};
          return {
            file: f.replace('.meta.json', ''),
            strategy,
            timeframe: info.timeframe || '',
            start: info.backtest_start_ts ? new Date(info.backtest_start_ts * 1000).toISOString().slice(0, 10) : '',
            end: info.backtest_end_ts ? new Date(info.backtest_end_ts * 1000).toISOString().slice(0, 10) : '',
          };
        } catch { return null; }
      })
      .filter(Boolean)
      .sort((a, b) => b.file.localeCompare(a.file))
      .slice(0, 10);
    return { mode: ENV ? 'coinclaw' : 'host', results: files, path: resultsDir };
  },
};

// ─── CLI ─────────────────────────────────────────────────────────
const [action, ...rest] = process.argv.slice(2);
if (!action || !actions[action]) {
  console.log(`Usage: node ft-deploy.mjs <action> [json-params]\nActions: ${Object.keys(actions).join(', ')}`);
  process.exit(1);
}
let params = {};
if (rest.length) {
  try {
    params = JSON.parse(rest.join(' '));
  } catch {
    console.log(JSON.stringify({
      error: `参数不是合法 JSON: ${rest.join(' ')}`,
      hint: "参数要用 JSON 对象, 例: '{\"strategy\":\"MyStrat\"}'",
    }));
    process.exit(1);
  }
}
actions[action](params).then((r) => {
  // 提示 — 只在 host 模式 / 老用法时强调走脚本; coinclaw 模式 daemon 已经
  // 在 supervisord 管, 用户从 chat agent 调用脚本就是正确路径.
  if (!ENV) r._reminder = 'IMPORTANT: Always use ft-deploy.mjs for ALL Freqtrade operations. NEVER use Docker commands.';
  console.log(JSON.stringify(r, null, 2));
}).catch((e) => {
  console.error(e.message);
  process.exit(1);
});
