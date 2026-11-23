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

// Major tokens by symbol per network (lowercase addresses), used to resolve
// "pools containing WETH" to an address filter. Also never flagged as spam.
export const COMMON_TOKENS = {
  mainnet: {
    WETH: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", USDC: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    USDT: "0xdac17f958d2ee523a2206206994597c13d831ec7", DAI: "0x6b175474e89094c44da98b954eedeac495271d0f",
    WBTC: "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
  },
  base: {
    WETH: "0x4200000000000000000000000000000000000006", USDC: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    DAI: "0x50c5725949a6f0c72e6c4a641f24049a917db0cb", CBBTC: "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf",
  },
  "arbitrum-one": {
    WETH: "0x82af49447d8a07e3bd95bd0d56f35241523fbab1", USDC: "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
    USDT: "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", DAI: "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
    WBTC: "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
  },
  optimism: {
    WETH: "0x4200000000000000000000000000000000000006", USDC: "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
    USDT: "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58", DAI: "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
    WBTC: "0x68f180fcce6836688e9084f035309e29bf0a2095",
  },
  matic: {
    WMATIC: "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270", WETH: "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
    USDC: "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359", USDT: "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
    DAI: "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063", WBTC: "0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6",
  },
};
for (const [net, map] of Object.entries(COMMON_TOKENS)) {
  KNOWN_GOOD_TOKENS[net] ||= {};
  for (const [sym, addr] of Object.entries(map)) KNOWN_GOOD_TOKENS[net][addr] ||= sym;
}

// Symbols a goal may name. ETH means the chain's wrapped ether (pools hold WETH).
const SYMBOL_ALIASES = { ETH: "WETH", ETHER: "WETH", BITCOIN: "WBTC", BTC: "WBTC" };
export const RESOLVABLE_SYMBOLS = new Set([...Object.values(COMMON_TOKENS).flatMap((m) => Object.keys(m)), ...Object.keys(SYMBOL_ALIASES)]);
export function canonicalSymbol(word) {
  const u = String(word || "").toUpperCase();
  return SYMBOL_ALIASES[u] || u;
}
// -> { address } | { error }
export function resolveTokenSymbol(symbol, network) {
  const sym = canonicalSymbol(symbol);
  const map = COMMON_TOKENS[network];
  if (!map) return { error: `no built-in token addresses for network ${network || "unknown"}` };
  // MATIC/POL only exist as wrapped native on matic; ETH on matic is the bridged WETH.
  const address = map[sym];
  return address ? { symbol: sym, address } : { error: `${sym} has no built-in address on ${network}` };
}

export const SPAM_HANDLING = ["flag_and_push_down", "flag_only", "off"];
export const THRESHOLDS = {
  // No single token's or pool's DEX TVL is plausibly above this (USD).
  // The largest real Uniswap pool or token holds a few $B, so $10B per row is
  // already far outside anything real.
  implausible_tvl_usd: 1e10,
  // TVL claimed without matching trading: volume below this fraction of TVL.
  tvl_without_volume_ratio: 1e-4,
  tvl_without_volume_min_tvl_usd: 1e5,
  // TVL per transaction: a large TVL built from a handful of transactions.
  tvl_per_tx_usd: 1e8,
  tvl_per_tx_min_tvl_usd: 1e6,
  // A pool holding this much TVL while one side is not a known major token.
  // Real pools beyond $1B do not exist on a long-tail pair.
  extreme_tvl_unlisted_pair_usd: 1e9,
  // Cumulative lifetime volume below 5% of claimed TVL on a $1M+ pool/token
  // involving an unlisted token is a strong indicator of spoofed/manipulated TVL.
  unlisted_high_tvl_min_usd: 1e6,
  unlisted_high_tvl_volume_ratio: 0.05,
  // totalSupply / 10^decimals above this many whole tokens (SHIB ~ 6e14).
  implausible_supply_tokens: 1e15,
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

// Whole-token supply from raw totalSupply and decimals (BigInt-safe strings).
function supplyTokens(row) {
  const raw = row?.totalSupply;
  if (raw === null || raw === undefined || raw === "") return null;
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return null;
  const dec = num(row.decimals);
  const d = dec !== null && dec >= 0 && dec <= 36 ? dec : 18;
  return n / 10 ** d;
}

function metricReasons(row, { allowlisted = false } = {}) {
  const out = [];
  const tvl = num(row.totalValueLockedUSD ?? row.tvlUSD);
  const vol = num(row.volumeUSD ?? row.totalVolumeUSD);
  const tx = num(row.txCount);
  if (tvl !== null && tvl > THRESHOLDS.implausible_tvl_usd) out.push("implausible_tvl_usd");
  if (tvl !== null && vol !== null && tvl > THRESHOLDS.tvl_without_volume_min_tvl_usd && vol < tvl * THRESHOLDS.tvl_without_volume_ratio) {
    out.push("tvl_without_trading_volume");
  }
  if (!allowlisted && tvl !== null && vol !== null && tvl >= THRESHOLDS.unlisted_high_tvl_min_usd && vol < tvl * THRESHOLDS.unlisted_high_tvl_volume_ratio && !out.includes("tvl_without_trading_volume")) {
    out.push("unlisted_token_low_volume_for_tvl");
  }
  if (tvl !== null && tx !== null && tx > 0 && tvl > THRESHOLDS.tvl_per_tx_min_tvl_usd && tvl / tx > THRESHOLDS.tvl_per_tx_usd) out.push("tvl_per_transaction_implausible");
  const supply = supplyTokens(row);
  if (supply !== null && supply > THRESHOLDS.implausible_supply_tokens) out.push("implausible_total_supply");
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
      if (!allowlisted) reasons.push(...textReasons("", row), ...metricReasons(row, { allowlisted }));
    } else {
      const t0 = row.token0 && typeof row.token0 === "object" ? row.token0 : null;
      const t1 = row.token1 && typeof row.token1 === "object" ? row.token1 : null;
      const ok0 = t0 && isAllowed(t0.id), ok1 = t1 && isAllowed(t1.id);
      allowlisted = Boolean(ok0 && ok1);
      if (t0 && !ok0) reasons.push(...textReasons("token0_", t0));
      if (t1 && !ok1) reasons.push(...textReasons("token1_", t1));
      if (!allowlisted) reasons.push(...metricReasons(row, { allowlisted }));
      const poolTvl = num(row.totalValueLockedUSD ?? row.tvlUSD);
      if (!allowlisted && (ok0 || ok1) && poolTvl !== null && poolTvl > THRESHOLDS.extreme_tvl_unlisted_pair_usd && !reasons.includes("implausible_tvl_usd")) {
        reasons.push("extreme_tvl_with_unlisted_token");
      }
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
  let reorderedBy = null;
  const allFlagged = rows.length > 1 && flagged.length === rows.length;
  if (handling === "flag_and_push_down" && allFlagged && rows.every((r) => num(r?.volumeUSD ?? r?.totalVolumeUSD) !== null)) {
    // Nothing trustworthy to rank first: order by traded volume, which is
    // harder to fake than TVL. Rows are still all returned.
    const vol = (r) => num(r.volumeUSD ?? r.totalVolumeUSD);
    out = [...rows].sort((a, b) => vol(b) - vol(a));
    reordered = out.some((r, i) => r !== rows[i]);
    reorderedBy = "volumeUSD";
  } else if (handling === "flag_and_push_down" && flagged.length && flagged.length < rows.length) {
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
      reordered, all_flagged: allFlagged,
      ...(reorderedBy ? { reordered_by: reorderedBy, order_note: "Every row was flagged, so rows were ordered by volumeUSD (harder to fake than TVL). Nothing was removed; this deployment's data looks unreliable, consider another deployment." } : {}),
      ...(reordered && !reorderedBy ? { order_note: "Flagged rows were moved after unflagged rows (stable order within each group). Nothing was removed; use spam_handling:\"flag_only\" to keep the gateway order." } : {}),
      caveat: "Heuristic flags (URL/lure words in symbol or name, implausible TVL, TVL without trading volume, very low activity). They can be wrong in both directions; verify contract addresses independently. Known-good allowlist is small and per network; extend with trusted_tokens.",
      thresholds: THRESHOLDS,
    },
  };
}
