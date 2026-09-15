/**
 * Telling a pool's earnings apart from its reward tokens' price moves.
 *
 * Every dollar figure in a snapshot is priced at the instant that scan ran, so
 * subtracting one scan's `latestEpochUsd` from the next measures two things
 * added together: rewards that accrued in between, and the repricing of the
 * rewards that were already sitting there. The README has always said so, and
 * has always said the fix is data rather than modelling — since 2026-08-28 each
 * snapshot publishes the raw token amounts behind that dollar figure, plus the
 * decimals and price the scan used, at `latestEpochBribes` / `latestEpochFees`
 * and `rewardTokens`.
 *
 * This module is the reader those amounts were published for. Amounts do not
 * reprice: value the earlier and the later scan's amounts at **one** price
 * vector and the difference is accrual alone, with the price move removed by
 * construction rather than estimated. Run the same pair through each scan's own
 * prices and you get the naive figure. The gap between the two is what the
 * price move was worth, and it is reported rather than quietly applied.
 *
 * Nothing here fetches. It reads scans the caller already loaded — from git or
 * from a directory — which keeps the whole measurement unit-testable and means
 * the report can never disagree with the committed history it claims to
 * describe.
 */

/** One reward token as some scan valued it. */
export interface TokenPrice {
  decimals: number;
  priceUsd: number;
}

/** What one scan knew about one pool's current-epoch rewards. */
export interface AccrualPool {
  symbol: string;
  /** Lowercased pool address. */
  pool: string;
  /** Unix seconds of the epoch these amounts belong to. Amounts reset when it changes. */
  epochTs: number;
  /** `[token address (lowercase), raw amount]`, bribes and fees already merged — the split matters for where rewards come from, not for what they are worth. */
  amounts: [string, bigint][];
  /** The scan's own USD figure for those amounts, kept so the naive difference can be reproduced exactly rather than recomputed. */
  usd: number;
}

/** One committed scan, reduced to what this measurement needs. */
export interface AccrualScan {
  /** Unix seconds of when the scan ran. */
  at: number;
  prices: Map<string, TokenPrice>;
  /** Keyed by lowercased pool address. */
  pools: Map<string, AccrualPool>;
}

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null;

/**
 * Raw `[address, amount]` pairs as the snapshot writes them: the amount is a
 * decimal string because it is a `uint256` and would lose precision as a
 * number. A pair that does not parse is dropped rather than counted as zero —
 * an unreadable amount is missing data, and calling it zero would invent a
 * reward that fell to nothing.
 */
function toAmounts(v: unknown): [string, bigint][] {
  if (!Array.isArray(v)) return [];
  const out: [string, bigint][] = [];
  for (const pair of v) {
    if (!Array.isArray(pair) || pair.length < 2) continue;
    const [addr, amount] = pair;
    if (typeof addr !== "string" || typeof amount !== "string") continue;
    try {
      out.push([addr.toLowerCase(), BigInt(amount)]);
    } catch {
      // Not an integer string. Skip the pair, keep the pool.
    }
  }
  return out;
}

/**
 * Pulls one committed snapshot into the shape this measurement works in, or
 * null if it predates the raw amounts and so cannot be part of it.
 *
 * A scan whose pools carry no `rewardTokens` at the root is from before
 * 2026-08-28. It is not broken and it is still used by every other measurement
 * in the repo — it simply cannot answer this question, and silently treating
 * its missing amounts as zero would read as every pool earning nothing.
 */
export function scanFromSnapshot(raw: unknown): AccrualScan | null {
  if (!isRecord(raw)) return null;
  const at = Date.parse(String(raw.generatedAt ?? ""));
  if (Number.isNaN(at)) return null;
  if (!Array.isArray(raw.rewardTokens) || raw.rewardTokens.length === 0) return null;
  if (!Array.isArray(raw.pools)) return null;

  const prices = new Map<string, TokenPrice>();
  for (const t of raw.rewardTokens) {
    if (!isRecord(t) || typeof t.address !== "string") continue;
    prices.set(t.address.toLowerCase(), {
      decimals: Number(t.decimals) || 0,
      priceUsd: Number(t.priceUsd) || 0,
    });
  }

  const pools = new Map<string, AccrualPool>();
  for (const p of raw.pools) {
    if (!isRecord(p) || typeof p.pool !== "string") continue;
    const epochTs = Number(p.latestEpochTs);
    if (!Number.isFinite(epochTs) || epochTs <= 0) continue;
    const amounts = [...toAmounts(p.latestEpochBribes), ...toAmounts(p.latestEpochFees)];
    if (amounts.length === 0) continue;
    pools.set(p.pool.toLowerCase(), {
      symbol: typeof p.symbol === "string" ? p.symbol : p.pool,
      pool: p.pool.toLowerCase(),
      epochTs,
      amounts,
      usd: Number(p.latestEpochUsd) || 0,
    });
  }

  if (pools.size === 0) return null;
  return { at: Math.floor(at / 1000), prices, pools };
}

/**
 * What a set of raw amounts is worth under one price vector.
 *
 * A token the vector has no entry for contributes nothing, which is the same
 * thing the scan itself did with an unpriced token — see `priceUsd: 0` in
 * `SnapshotRewardToken`. Keeping that behaviour is what makes the revalued
 * figure comparable to the scan's own; `unpricedTokens` below is how the
 * measurement stays honest about it instead of hiding it.
 */
export function valueAt(amounts: [string, bigint][], prices: Map<string, TokenPrice>): number {
  let total = 0;
  for (const [addr, amount] of amounts) {
    const p = prices.get(addr);
    if (!p || p.priceUsd === 0) continue;
    total += (Number(amount) / 10 ** p.decimals) * p.priceUsd;
  }
  return total;
}

/** Raw amounts summed per token across both scans of a pair, for differencing. */
function sumByToken(amounts: [string, bigint][]): Map<string, bigint> {
  const out = new Map<string, bigint>();
  for (const [addr, amount] of amounts) out.set(addr, (out.get(addr) ?? 0n) + amount);
  return out;
}

/** One pool observed at two moments inside the same epoch. */
export interface AccrualWindow {
  symbol: string;
  pool: string;
  epochTs: number;
  fromAt: number;
  toAt: number;
  /** Hours actually between the two scans, which is near but not exactly the requested window. */
  hours: number;
  /** Later scan's USD minus earlier scan's USD, each priced by its own scan — accrual and repricing together. */
  naiveUsd: number;
  /** The same two sets of amounts, both valued at the later scan's prices — accrual with the price move removed. */
  accrualUsd: number;
  /** `naiveUsd - accrualUsd`: what the reward tokens' price move was worth over the window. */
  repricingUsd: number;
  /** True if any token's raw amount fell between the two scans, which rewards inside one epoch should not do. */
  amountFell: boolean;
  /**
   * True if any token's raw amount moved at all. This turns out to be the
   * measurement's most important field rather than a detail: on the committed
   * history almost no pool's amounts move once a scan can see them, so a window
   * where this is false has no accrual to find and its entire dollar movement
   * is price.
   */
  amountMoved: boolean;
  /** Tokens present in the amounts but carrying no price in the later scan, so contributing $0 to both sides. */
  unpricedTokens: number;
}

/**
 * Pairs each scan with the nearest later scan about `hours` apart, and measures
 * every pool the two have in common.
 *
 * Two rules decide what is comparable, and both are about not inventing a
 * number:
 *
 * - **Same epoch, same pool.** Amounts are cumulative within an epoch and reset
 *   at its boundary, so a pair that straddles one would read as the pool losing
 *   everything it had earned. Pairs where `epochTs` differs are skipped, not
 *   clamped.
 * - **The later scan's prices for both sides.** Any single vector removes the
 *   price move; the later one is chosen because it is the one a reader holding
 *   the newest snapshot already has, so the figure can be reproduced from the
 *   file in front of them rather than from a scan they would have to go and dig
 *   out of git.
 *
 * `tolerance` is a fraction of the requested window, because scans land every
 * six hours or so and demanding an exact 48.000 hours would match nothing.
 */
export function buildWindows(scans: AccrualScan[], hours: number, tolerance = 0.25): AccrualWindow[] {
  const ordered = [...scans].sort((a, b) => a.at - b.at);
  const target = hours * 3600;
  const slack = target * tolerance;
  const out: AccrualWindow[] = [];

  for (let i = 0; i < ordered.length; i++) {
    const from = ordered[i];
    // The closest later scan to the requested distance. Scanning forward and
    // keeping the best rather than taking the first inside the window stops a
    // dense patch of scans from filling the results with 36-hour pairs when 48
    // was asked for.
    let best: AccrualScan | null = null;
    let bestMiss = Infinity;
    for (let j = i + 1; j < ordered.length; j++) {
      const gap = ordered[j].at - from.at;
      if (gap > target + slack) break;
      if (gap < target - slack) continue;
      const miss = Math.abs(gap - target);
      if (miss < bestMiss) {
        bestMiss = miss;
        best = ordered[j];
      }
    }
    if (!best) continue;

    for (const [address, later] of best.pools) {
      const earlier = from.pools.get(address);
      if (!earlier) continue;
      if (earlier.epochTs !== later.epochTs) continue;

      const earlierAt = valueAt(earlier.amounts, best.prices);
      const laterAt = valueAt(later.amounts, best.prices);

      const before = sumByToken(earlier.amounts);
      const after = sumByToken(later.amounts);
      let amountFell = false;
      let amountMoved = false;
      for (const addr of new Set([...before.keys(), ...after.keys()])) {
        const was = before.get(addr) ?? 0n;
        const now = after.get(addr) ?? 0n;
        if (now !== was) amountMoved = true;
        if (now < was) amountFell = true;
      }

      let unpriced = 0;
      for (const addr of after.keys()) {
        const p = best.prices.get(addr);
        if (!p || p.priceUsd === 0) unpriced++;
      }

      const naiveUsd = later.usd - earlier.usd;
      const accrualUsd = laterAt - earlierAt;
      out.push({
        symbol: later.symbol,
        pool: address,
        epochTs: later.epochTs,
        fromAt: from.at,
        toAt: best.at,
        hours: (best.at - from.at) / 3600,
        naiveUsd,
        accrualUsd,
        repricingUsd: naiveUsd - accrualUsd,
        amountFell,
        amountMoved,
        unpricedTokens: unpriced,
      });
    }
  }

  return out;
}

const median = (xs: number[]): number => {
  if (xs.length === 0) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  const mid = s.length >> 1;
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
};

/** The headline for one window length. */
export interface WindowSummary {
  hours: number;
  observations: number;
  /**
   * Share of pool-windows where the naive difference came out below zero. This
   * is the figure the README quotes (43% at 48 hours) as the reason the dollar
   * series cannot answer "what did this pool earn between Tuesday and
   * Thursday".
   */
  negativeNaive: number;
  /** The same share once the price move is removed. A pool cannot un-earn a reward, so whatever is left here is data trouble, not economics. */
  negativeAccrual: number;
  /**
   * Share of pool-windows where any raw amount moved at all — the measurement's
   * headline. Where this is near zero, the epoch's incentives were already
   * fixed when the scan first saw them, and the dollar series is reporting the
   * reward tokens' price and nothing else.
   */
  withAccrual: number;
  medianNaiveUsd: number;
  medianAccrualUsd: number;
  /** Median accrual over only the windows where amounts actually moved, so the few real ones are not averaged into invisibility by the many that could not move. */
  medianAccrualWhenMoved: number;
  /** Median of `|repricing| / (|repricing| + |accrual|)` — how much of a typical window's dollar movement was the price rather than the pool. */
  medianRepricingShare: number;
  /** Pool-windows where a raw amount fell inside an epoch. */
  amountFell: number;
  /** Pool-windows carrying at least one token with no price, which therefore counts as $0 on both sides. */
  withUnpriced: number;
}

function summarise(hours: number, windows: AccrualWindow[]): WindowSummary {
  const n = windows.length;
  const share = (k: number) => (n === 0 ? NaN : k / n);
  return {
    hours,
    observations: n,
    negativeNaive: share(windows.filter((w) => w.naiveUsd < 0).length),
    negativeAccrual: share(windows.filter((w) => w.accrualUsd < 0).length),
    withAccrual: share(windows.filter((w) => w.amountMoved).length),
    medianNaiveUsd: median(windows.map((w) => w.naiveUsd)),
    medianAccrualUsd: median(windows.map((w) => w.accrualUsd)),
    medianAccrualWhenMoved: median(windows.filter((w) => w.amountMoved).map((w) => w.accrualUsd)),
    medianRepricingShare: median(
      windows
        .map((w) => {
          const denom = Math.abs(w.repricingUsd) + Math.abs(w.accrualUsd);
          return denom === 0 ? NaN : Math.abs(w.repricingUsd) / denom;
        })
        .filter((x) => !Number.isNaN(x)),
    ),
    amountFell: windows.filter((w) => w.amountFell).length,
    withUnpriced: windows.filter((w) => w.unpricedTokens > 0).length,
  };
}

export interface AccrualReport {
  generatedAt: string;
  /** Scans carrying raw amounts, which is not the same as scans in the history. */
  scans: number;
  /** ISO dates of the oldest and newest such scan, so a reader can see the measurement's reach without opening git. */
  from: string;
  to: string;
  windows: WindowSummary[];
  /**
   * The largest dollar swings, over the longest window measured, that were
   * entirely price: the pool's raw amounts never moved, so every cent of the
   * change a dollar-series reader would have seen came from the reward tokens
   * repricing.
   */
  pureRepricing: { symbol: string; pool: string; repricingUsd: number }[];
  /**
   * The pools whose amounts did move, with what that movement was worth at one
   * price. On the current history this list is short, and that is the finding
   * rather than a shortcoming of the measurement.
   */
  didAccrue: { symbol: string; pool: string; accrualUsd: number; repricingUsd: number }[];
}

/** The window lengths the README already reports the naive negative-rate for, so the two can be read side by side. */
export const DEFAULT_WINDOW_HOURS = [48, 72, 96, 120];

export function buildAccrualReport(
  scans: AccrualScan[],
  windowHours: number[] = DEFAULT_WINDOW_HOURS,
  generatedAt: Date = new Date(),
): AccrualReport {
  const ordered = [...scans].sort((a, b) => a.at - b.at);
  const iso = (t: number) => new Date(t * 1000).toISOString();

  const longest = Math.max(...windowHours);
  const longestWindows = buildWindows(ordered, longest);

  // Both lists are taken over the longest window because that is where accrual
  // has had the best chance to show up: a pool whose amounts have not moved in
  // five days has not moved in two either.
  //
  // One row per pool, keeping its largest window, so a single busy pool cannot
  // occupy the whole list with near-identical overlapping pairs.
  const keepLargest = <T extends { pool: string }>(rows: T[], by: (row: T) => number): T[] => {
    const best = new Map<string, T>();
    for (const row of rows) {
      const seen = best.get(row.pool);
      if (!seen || by(row) > by(seen)) best.set(row.pool, row);
    }
    return [...best.values()].sort((a, b) => by(b) - by(a));
  };

  const pureRepricing = keepLargest(
    longestWindows.filter((w) => !w.amountMoved).map((w) => ({ symbol: w.symbol, pool: w.pool, repricingUsd: w.repricingUsd })),
    (r) => Math.abs(r.repricingUsd),
  ).slice(0, 10);

  const didAccrue = keepLargest(
    longestWindows
      .filter((w) => w.amountMoved)
      .map((w) => ({ symbol: w.symbol, pool: w.pool, accrualUsd: w.accrualUsd, repricingUsd: w.repricingUsd })),
    (r) => Math.abs(r.accrualUsd),
  ).slice(0, 10);

  return {
    generatedAt: generatedAt.toISOString(),
    scans: ordered.length,
    from: ordered.length > 0 ? iso(ordered[0].at) : "",
    to: ordered.length > 0 ? iso(ordered[ordered.length - 1].at) : "",
    windows: windowHours.map((h) => summarise(h, h === longest ? longestWindows : buildWindows(ordered, h))),
    pureRepricing,
    didAccrue,
  };
}
