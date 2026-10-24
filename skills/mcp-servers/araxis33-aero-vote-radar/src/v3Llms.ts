import type { V3ScanFile, V3ScanGauge } from "./v3.js";
import { isSteady, per10kNow } from "./v3History.js";

/**
 * Renders `llms.txt` from the hourly Aero scan: the page as plain text for AI
 * assistants and crawlers, which fetch the HTML without running it and so see
 * no numbers. Same ranking as the page's table (fees over the scan window plus
 * incentives now, for 10,000 sAERO after it dilutes the pool), the steadiest
 * pools on the hourly history, and how allocation works.
 *
 * Pure: the scan comes in as an argument.
 */

const SITE = "https://aero.deftools.xyz";
const REPO = "https://github.com/araxis33/aero-vote-radar";
const PER = 10_000;
/** Pools below this weight are left out, as on the page. */
const MIN_WEIGHT = 100_000;
const TOP = 10;
const STEADY_TOP = 5;

const CHAIN_NAMES: Record<string, string> = {
  base: "Base", ethereum: "Ethereum", optimism: "OP Mainnet", arbitrum: "Arbitrum", ink: "Ink", robinhood: "Robinhood Chain", arc: "Arc",
};

const usd = (n: number) => (n >= 1000 ? "$" + Math.round(n).toLocaleString("en-US") : "$" + n.toFixed(2));
const name = (g: V3ScanGauge) =>
  `${g.symbol0 && g.symbol1 ? `${g.symbol0}/${g.symbol1}` : g.pool} (${g.kind?.replace(/^CL\d+$/, "CL") ?? "?"}, ${CHAIN_NAMES[g.chain] ?? g.chain})`;
const perDay = (g: V3ScanGauge) => g.feesUsdPerDay + g.incentivesUsdPerDay;
const per10k = (g: V3ScanGauge) => (perDay(g) * PER) / (g.weight + PER);

export function renderV3LlmsTxt(scan: V3ScanFile): string {
  const pools = scan.gauges.filter((g) => g.weight >= MIN_WEIGHT && perDay(g) > 0);
  const best = [...pools].sort((a, b) => per10k(b) - per10k(a)).slice(0, TOP);
  const steady = pools
    .filter((g) => isSteady(g.steady))
    .sort((a, b) => per10kNow(b) - per10kNow(a))
    .slice(0, STEADY_TOP);
  const networks = Object.values(scan.chains ?? {}).filter((c) => c.status === "live").length || 1;
  const allocated = scan.gauges.reduce((a, g) => a + g.weight, 0);

  const lines = [
    "# Aero Vote Radar",
    "",
    "> Where sAERO earns the most on Aero (formerly Aerodrome), across its networks. Enter how much sAERO you hold and see what every pool pays you per day after your own stake dilutes it, plus the 47 h timer of your stakes on each network. Free, open source (MIT), read-only: no wallet connection, no signatures.",
    "",
    `Scanned from Aero's contracts on ${networks} network${networks === 1 ? "" : "s"}: ${scan.checkedAt}. The scan re-runs every hour.`,
    `Fees are what each pool swept to its allocators over the last ${Math.round(scan.windowHours)} h; incentives are what projects stream right now. ${Math.round(allocated).toLocaleString("en-US")} sAERO is allocated across ${scan.gauges.length} pools.`,
    "",
    `## Best pools for ${PER.toLocaleString("en-US")} sAERO right now`,
    "",
  ];
  if (best.length === 0) lines.push("No pool with at least 100,000 sAERO paid anything in this scan. Open the page for the live view.");
  for (const g of best)
    lines.push(
      `- ${name(g)}: about ${usd(per10k(g))} a day for ${PER.toLocaleString("en-US")} sAERO — fees ${usd(g.feesUsdPerDay)}/day, incentives ${usd(g.incentivesUsdPerDay)}/day, ${Math.round(g.weight).toLocaleString("en-US")} sAERO in the pool`,
    );
  lines.push(
    "",
    "Pools with at least 100,000 sAERO. A larger amount dilutes each pool more and is better split across a few; the page splits any amount.",
    "",
    "## Steadiest pools",
    "",
  );
  if (steady.length === 0) {
    lines.push("Not enough hourly history yet (needs a day of scans).");
  } else {
    lines.push("Pools that paid at least half their own average in 75% of the hourly scans or more, best current pay first (last 24 h of fees plus incentives, for 10,000 sAERO):", "");
    for (const g of steady) {
      const s = g.steady!;
      lines.push(`- ${name(g)}: ${usd(per10kNow(g))} a day now, average ${usd(s.avgPer10k)}, lowest hour ${usd(s.minPer10k)}, held up ${s.held} of ${s.of} hours`);
    }
  }
  lines.push(
    "",
    "## How allocation works on Aero",
    "",
    "- Each sAERO stake can change its allocation once every 47 hours, separately on each network; a new stake's first allocation has no wait.",
    "- Your own stake dilutes a pool: per day ≈ the pool's daily rewards × your sAERO / (sAERO already in the pool + yours).",
    "- Top pools cool off fast; moving every 47 h earned about 1.7× moving weekly in a 3-week backtest on pre-launch Aerodrome fees.",
    `- Allocate at https://app.aero.xyz/markets/allocate in your own wallet. The radar never holds funds.`,
    "",
    "## Links",
    "",
    `- [Live page](${SITE})`,
    `- [How to use it](${SITE}/#guide)`,
    `- [Raw scan, JSON](${SITE}/data/v3.json)`,
    `- [Source and method](${REPO})`,
    "",
    "Not financial advice. The tool prints numbers; the user allocates.",
    "",
  );
  return lines.join("\n");
}
