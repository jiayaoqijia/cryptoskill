// Heuristic spam/scam-token flags for token and pool rows returned by
// query_for_goal. Flags are advisory: rows are never removed. With the default
// handling, flagged rows are moved after unflagged rows and every move is
// reported, so a caller can always see (and undo) what happened.

// Small, conservative known-good list per network (lowercase addresses).
// Allowlisted tokens are never flagged. Callers can extend it per call with
// trusted_tokens. This is not an endorsement list, only "do not flag".
export const KNOWN_GOOD_TOKENS = {
  mainnet: {
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "WETH",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
    "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI",
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": "WBTC",
  },
  base: {
    "0x4200000000000000000000000000000000000006": "WETH",
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": "USDC",
  },
  "arbitrum-one": {
    "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": "WETH",
    "0xaf88d065e77c8cc2239327c5edb3a432268e5831": "USDC",
    "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": "USDT",
  },
  optimism: {
    "0x4200000000000000000000000000000000000006": "WETH",
    "0x0b2c639c533813f4aa9d7837caf62653d097ff85": "USDC",
  },
  matic: {
    "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270": "WMATIC",
    "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619": "WETH",
    "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359": "USDC",
  },
};

export const SPAM_HANDLING = ["flag_and_push_down", "flag_only", "off"];
export const THRESHOLDS = {
  // No single token's or pool's DEX TVL is plausibly above this (USD).
  implausible_tvl_usd: 1e11,
  // TVL claimed without matching trading: volume below this fraction of TVL.
  tvl_without_volume_ratio: 1e-5,
  tvl_without_volume_min_tvl_usd: 1e6,
  low_activity_tx_count: 25,
  low_activity_volume_usd: 1000,
  long_symbol: 15,
};

const URL_RE = /(https?:\/\/|www\.|t\.me\/|\.(com|io|net|org|xyz|app|finance|site|top|vip|cc|gg|info|link|club|live|pro|fun|online|website|claims?)\b)/i;
const LURE_RE = /\b(claim|claimable|visit|airdrops?|reward|rewards|bonus|giveaway|free|gift|voucher|redeem|eligible|whitelist)\b/i;
const ADDRESS_RE = /^0x[0-9a-f]{40}$/;

const num = (v) => {
  if (v === null || v === undefined || v === "") return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
};

function textReasons(prefix, tok) {
  const out = [];
  for (const key of ["symbol", "name"]) {
    const v = tok?.[key];
    if (typeof v !== "string" || !v) continue;
    if (URL_RE.test(v)) out.push(`${prefix}${key}_contains_url_or_domain`);
    if (LURE_RE.test(v)) out.push(`${prefix}${key}_contains_lure_word`);
    if (key === "symbol" && v.length > THRESHOLDS.long_symbol) out.push(`${prefix}symbol_unusually_long`);
  }
  return out;
}

function metricReasons(row) {
  const out = [];
  const tvl = num(row.totalValueLockedUSD ?? row.tvlUSD);
  const vol = num(row.volumeUSD ?? row.totalVolumeUSD);
  const tx = num(row.txCount);
  if (tvl !== null && tvl > THRESHOLDS.implausible_tvl_usd) out.push("implausible_tvl_usd");
  if (tvl !== null && vol !== null && tvl > THRESHOLDS.tvl_without_volume_min_tvl_usd && vol < tvl * THRESHOLDS.tvl_without_volume_ratio) {
    out.push("tvl_without_trading_volume");
  }
  if (tx !== null && tx < THRESHOLDS.low_activity_tx_count && (vol === null || vol < THRESHOLDS.low_activity_volume_usd)) out.push("low_activity");
  return out;
}

export function normalizeTrusted(list) {
  if (list === undefined) return { ok: true, set: new Set() };
  if (!Array.isArray(list) || list.length > 50 || !list.every((a) => typeof a === "string" && ADDRESS_RE.test(a.trim().toLowerCase()))) {
    return { ok: false, error: "trusted_tokens must be an array of at most 50 0x-prefixed 40-hex addresses" };
  }
  return { ok: true, set: new Set(list.map((a) => a.trim().toLowerCase())) };
}

// Which collections this applies to: rows that look like tokens or pools.
export function isTokenOrPoolRows(rows) {
  return Array.isArray(rows) && rows.some((r) => r && typeof r === "object" &&
    ("symbol" in r || "token0" in r || "totalValueLockedUSD" in r || "txCount" in r));
}

export function assessRows(rows, { network, trusted = new Set(), kind = "token" } = {}) {
  const allow = { ...(KNOWN_GOOD_TOKENS[network] || {}) };
  const isAllowed = (id) => typeof id === "string" && (Boolean(allow[id.toLowerCase()]) || trusted.has(id.toLowerCase()));
  return rows.map((row, index) => {
    if (!row || typeof row !== "object") return { index, id: null, flagged: false, reasons: [] };
    const id = typeof row.id === "string" ? row.id : null;
    const reasons = [];
    let allowlisted = false;
    if (kind === "token") {
      allowlisted = isAllowed(id);
      if (!allowlisted) reasons.push(...textReasons("", row), ...metricReasons(row));
    } else {
      const t0 = row.token0 && typeof row.token0 === "object" ? row.token0 : null;
      const t1 = row.token1 && typeof row.token1 === "object" ? row.token1 : null;
      const ok0 = t0 && isAllowed(t0.id), ok1 = t1 && isAllowed(t1.id);
      allowlisted = Boolean(ok0 && ok1);
      if (t0 && !ok0) reasons.push(...textReasons("token0_", t0));
      if (t1 && !ok1) reasons.push(...textReasons("token1_", t1));
      if (!allowlisted) reasons.push(...metricReasons(row));
    }
    const label = row.symbol ?? (row.token0?.symbol && row.token1?.symbol ? `${row.token0.symbol}/${row.token1.symbol}` : undefined);
    return { index, id, ...(label ? { label: String(label).slice(0, 40) } : {}), flagged: reasons.length > 0, reasons, ...(allowlisted ? { allowlisted: true } : {}) };
  });
}

// Returns { rows (possibly reordered), report }. Never removes a row.
export function applyTokenQuality(rows, { network, trusted, handling = "flag_and_push_down", kind = "token", collection }) {
  if (handling === "off" || !isTokenOrPoolRows(rows)) return { rows, report: null };
  const checks = assessRows(rows, { network, trusted, kind });
  const flagged = checks.filter((c) => c.flagged);
  let out = rows;
  let reordered = false;
  if (handling === "flag_and_push_down" && flagged.length && flagged.length < rows.length) {
    const good = checks.filter((c) => !c.flagged).map((c) => rows[c.index]);
    const bad = flagged.map((c) => rows[c.index]);
    out = [...good, ...bad];
    reordered = out.some((r, i) => r !== rows[i]);
  }
  return {
    rows: out,
    report: {
      collection, kind, handling, checked: rows.length, flagged_count: flagged.length,
      flagged: flagged.map(({ index, id, label, reasons }) => ({ original_index: index, id, ...(label ? { label } : {}), reasons })),
      allowlisted: checks.filter((c) => c.allowlisted).map((c) => c.id),
      reordered,
      ...(reordered ? { order_note: "Flagged rows were moved after unflagged rows (stable order within each group). Nothing was removed; use spam_handling:\"flag_only\" to keep the gateway order." } : {}),
      caveat: "Heuristic flags (URL/lure words in symbol or name, implausible TVL, TVL without trading volume, very low activity). They can be wrong in both directions; verify contract addresses independently. Known-good allowlist is small and per network; extend with trusted_tokens.",
      thresholds: THRESHOLDS,
    },
  };
}
