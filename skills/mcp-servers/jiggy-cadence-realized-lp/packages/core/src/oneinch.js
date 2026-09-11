/**
 * oneinch.js — an INDEPENDENT price source, used to cross-check the one number this whole
 * project stands or falls on.
 *
 * WHY THIS EXISTS. Every realized-return figure we compute is a function of a price ratio:
 * IL is entirely determined by (exit price / entry price). That ratio comes from the Uniswap
 * subgraph's own `token0Price`. So the subgraph is BOTH the fee source and the price source,
 * and a tool whose entire thesis is "the advertised number is wrong" cannot also assume its
 * own single price feed is beyond question. That's the exact circularity we call out in other
 * people's numbers.
 *
 * 1inch's Spot Price API aggregates on-chain prices across DEXes independently of any single
 * pool. We use it as a SECOND opinion on the *current* price: if 1inch and the subgraph agree,
 * our price leg is corroborated; if they diverge past a threshold, we say so rather than
 * reporting a realized number built on a price only one source vouches for.
 *
 * It is deliberately NON-LOAD-BEARING. The product works without it (The Graph remains the
 * source of truth for the historical series RPC cannot provide). This is a confidence layer,
 * and it degrades honestly: no key -> { available:false, reason }, never a fabricated match.
 *
 * Key: process.env.ONEINCH_API_KEY, or ~/.config/cadence-secure/1inch.json {"api_key":"..."}.
 * Free from https://portal.1inch.dev.
 */

const SPOT_BASE = 'https://api.1inch.dev/price/v1.1';

// 1inch chain ids match EVM chain ids; we only map the chains our venues cover.
// optimism added 2026-09-11: venueList() covers it and 1inch gas-price returns 200 there,
// so omitting it was silently degrading one of our five chains to "unsupported".
const CHAIN_IDS = { mainnet: 1, arbitrum: 42161, polygon: 137, base: 8453, optimism: 10 };

const GAS_BASE = 'https://api.1inch.dev/gas-price/v1.5';

/**
 * Gas units for closing a Uniswap v3 position. Exiting is TWO transactions, not one:
 *   decreaseLiquidity  ~150k   (burn the liquidity back into token amounts)
 *   collect            ~120k   (sweep tokens + accrued fees to the owner)
 * Sources: typical mainnet execution for NonfungiblePositionManager calls. These are
 * ESTIMATES of gas UNITS -- the gas PRICE is live. We state the split so a caller can
 * substitute their own unit figures rather than trusting ours as exact.
 */
export const EXIT_GAS_UNITS = { decreaseLiquidity: 150_000, collect: 120_000, total: 270_000 };

/**
 * What it costs, in USD, to close a v3 position right now.
 *
 * Live gas price from 1inch, multiplied by estimated gas units, priced in the chain's native
 * token via 1inch spot price. Degrades honestly at every step: no key, unsupported chain, or
 * an upstream failure returns { available:false, reason }, never a fabricated dollar figure.
 *
 * NOTE ON PRECISION: the gas PRICE is measured live; the gas UNITS are estimates. We report
 * both separately and label the result an estimate, because pretending a +/-15% unit estimate
 * is an exact cost would be the same fabricated-precision defect this project exists to expose.
 */
export async function exitGasCost({
  chain = 'mainnet',
  apiKey = process.env.ONEINCH_API_KEY,
  gasUnits = EXIT_GAS_UNITS.total,
  speed = 'medium',
  timeoutMs = 8000,
} = {}) {
  if (!apiKey) return { available: false, reason: 'no ONEINCH_API_KEY set — gas estimate skipped' };
  const chainId = CHAIN_IDS[chain];
  if (!chainId) return { available: false, reason: `1inch gas price not wired for chain "${chain}"` };

  // Native token address is the same sentinel across EVM chains in 1inch's price API.
  const NATIVE = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee';
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const hdrs = { Authorization: `Bearer ${apiKey}`, Accept: 'application/json' };
    const gasRes = await fetch(`${GAS_BASE}/${chainId}`, { headers: hdrs, signal: ctrl.signal });
    if (!gasRes.ok) return { available: false, reason: `1inch gas-price HTTP ${gasRes.status}` };
    const gas = await gasRes.json();
    const tier = gas?.[speed] ?? gas?.medium;
    const maxFeeWei = Number(tier?.maxFeePerGas);
    if (!(maxFeeWei > 0)) return { available: false, reason: '1inch returned no usable gas price' };

    const priceRes = await fetch(`https://api.1inch.dev/price/v1.1/${chainId}/${NATIVE}?currency=USD`, { headers: hdrs, signal: ctrl.signal });
    if (!priceRes.ok) return { available: false, reason: `native-token price HTTP ${priceRes.status}` };
    const priceBody = await priceRes.json();
    const nativeUsd = Number(priceBody[NATIVE] ?? priceBody[NATIVE.toLowerCase()]);
    if (!(nativeUsd > 0)) return { available: false, reason: '1inch returned no usable native-token price' };

    const costNative = (maxFeeWei * gasUnits) / 1e18;
    const costUsd = costNative * nativeUsd;
    return {
      available: true,
      source: '1inch gas-price v1.5 + spot price v1.1',
      chain,
      speed,
      gasPriceGwei: Number((maxFeeWei / 1e9).toFixed(4)),
      gasUnits,
      gasUnitsBreakdown: EXIT_GAS_UNITS,
      nativeTokenUsd: Number(nativeUsd.toFixed(2)),
      costUsd: Number(costUsd.toFixed(2)),
      isEstimate: true,
      note: `Gas PRICE is live; gas UNITS (${gasUnits.toLocaleString()}) are an estimate for decreaseLiquidity + collect. Treat the dollar figure as approximate, not exact.`,
    };
  } catch (e) {
    return { available: false, reason: `1inch gas lookup failed: ${String(e.message || e).slice(0, 120)}` };
  } finally {
    clearTimeout(t);
  }
}

/**
 * Fetch the spot price of token0 denominated in token1 from 1inch, for comparison with the
 * subgraph's token0Price. Both token addresses are required (the subgraph carries them).
 *
 * Returns one of:
 *   { available:true,  oneInchPrice, subgraphPrice, divergencePct, agrees, threshold }
 *   { available:false, reason }              // no key, unsupported chain, or upstream error
 *
 * Never throws: a price cross-check that crashes the position endpoint would be worse than
 * no cross-check at all.
 */
export async function crossCheckPrice({
  token0,
  token1,
  subgraphPrice,
  chain = 'mainnet',
  apiKey = process.env.ONEINCH_API_KEY,
  thresholdPct = 2,
  timeoutMs = 8000,
} = {}) {
  if (!apiKey) {
    return { available: false, reason: 'no ONEINCH_API_KEY set — cross-check skipped (get a free key at portal.1inch.dev)' };
  }
  const chainId = CHAIN_IDS[chain];
  if (!chainId) return { available: false, reason: `1inch spot price not wired for chain "${chain}"` };
  if (!token0 || !token1) return { available: false, reason: 'token addresses missing from subgraph record' };

  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    // 1inch returns USD (or wei-denominated) prices per address; we request both tokens and
    // form the ratio ourselves so the comparison is apples-to-apples with token0Price.
    const url = `${SPOT_BASE}/${chainId}/${token0},${token1}?currency=USD`;
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${apiKey}`, Accept: 'application/json' },
      signal: ctrl.signal,
    });
    if (!res.ok) return { available: false, reason: `1inch HTTP ${res.status}` };
    const body = await res.json();
    const p0 = Number(body[token0.toLowerCase()] ?? body[token0]);
    const p1 = Number(body[token1.toLowerCase()] ?? body[token1]);
    if (!(p0 > 0) || !(p1 > 0)) return { available: false, reason: '1inch returned no usable price for this pair' };

    // CONVENTION, verified empirically 2026-09-10 against two pools with OPPOSITE token
    // ordering (USDC/WETH t0=USDC, and WETH/USDT t0=WETH):
    //
    //   subgraph token0Price = price of token0 expressed in token1
    //                        = (USD value of token1) / (USD value of token0)   <-- p1/p0
    //
    // The naive reading is p0/p1, and it is wrong: it returned 0.000405 against a subgraph
    // 2458.08 (exactly the reciprocal), which rendered as a -100% divergence warning on every
    // position. Both orderings agree with p1/p0 to within 0.33%, so this is one convention,
    // not a per-pool flip -- which is why the fix is NOT "detect and invert per pool".
    const oneInchPrice = p1 / p0;
    const sg = Number(subgraphPrice);
    if (!(sg > 0)) {
      return { available: true, oneInchPrice, subgraphPrice: null, divergencePct: null, agrees: null,
        note: 'subgraph price unavailable for comparison; 1inch spot price reported alone' };
    }
    const divergencePct = ((oneInchPrice - sg) / sg) * 100;
    const agrees = Math.abs(divergencePct) <= thresholdPct;
    return {
      available: true,
      source: '1inch Spot Price API v1.1',
      oneInchPrice,
      subgraphPrice: sg,
      divergencePct,
      agrees,
      threshold: thresholdPct,
      note: agrees
        ? `Independent 1inch spot price agrees with the subgraph within ${thresholdPct}% — the price leg of this realized figure is corroborated.`
        : `1inch spot price diverges from the subgraph by ${divergencePct.toFixed(2)}% — treat this realized figure's price leg as unconfirmed.`,
    };
  } catch (e) {
    return { available: false, reason: `1inch cross-check failed: ${String(e.message || e).slice(0, 120)}` };
  } finally {
    clearTimeout(t);
  }
}
