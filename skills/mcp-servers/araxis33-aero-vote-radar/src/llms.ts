import type { PoolEfficiency } from "./efficiency.js";
import {
  expectedUsdForWholePercentVote,
  recommendAllocation,
  toWholePercentWeights,
} from "./allocator.js";
import { withoutMigrating } from "./pools.js";

/**
 * The budget the plain-text summary is priced for — the hosted page's own
 * default, so a reader who follows the link lands on the same figure.
 */
export const LLMS_EXAMPLE_VEAERO = 10_000;

/**
 * The hosted page's other defaults — `#mincons` 0.5 and `#votebasis` "typical"
 * in docs/index.html. Mirrored so the text an assistant quotes is the answer a
 * reader gets on the page. The CLI's defaults differ (no filter, "previous"),
 * and on a spiky pool they disagree outright: on 2026-09-25 they put 100% into
 * one pool whose weight had dropped to a twentieth of its usual for a week.
 */
export const LLMS_MIN_CONSISTENCY = 0.5;
export const LLMS_VOTE_BASIS = "typical" as const;

const SITE = "https://aero.deftools.xyz";

/** Announced by Aero on 2026-09-25; the page carries the same notice (#aeroLaunchNote). */
const AERO_LAUNCH_UTC = "2026-10-22 00:00 UTC";
const AERO_LAUNCH_URL = "https://aero.xyz/articles/aero-launch-update-all-systems-go/";
const REPO = "https://github.com/araxis33/aero-vote-radar";

function usd(n: number): string {
  return `$${n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function utc(unixSeconds: number): string {
  return new Date(unixSeconds * 1000).toISOString().replace(/:\d\d\.\d{3}Z$/, " UTC").replace("T", " ");
}

/**
 * Renders `llms.txt`: the site as plain text for AI assistants and crawlers.
 *
 * The hosted page builds its answer in the browser, so anything that reads the
 * HTML without running it — which is how assistants fetch a page — sees a form
 * and no numbers. Most of the repo's visitors arrive from chatgpt.com, so this
 * file carries this week's actual suggestion, computed by the same
 * `recommendAllocation` the CLI's `recommend` uses, on the hosted page's
 * default settings (migrating pools left out), and says when it expires.
 *
 * Pure: the scan result and both timestamps come in as arguments.
 */
export function renderLlmsTxt(
  ranked: PoolEfficiency[],
  generatedAt: Date,
  epochEndsAt: number,
): string {
  const asOf = Math.floor(generatedAt.getTime() / 1000);
  const notMigrating = withoutMigrating(ranked);
  const migrating = ranked.length - notMigrating.length;
  const eligible = notMigrating.filter((p) => p.consistency >= LLMS_MIN_CONSISTENCY);
  const allocation = recommendAllocation(eligible, LLMS_EXAMPLE_VEAERO, undefined, undefined, 1, LLMS_VOTE_BASIS, asOf);
  const weights = toWholePercentWeights(allocation);
  const weekly = expectedUsdForWholePercentVote(allocation, LLMS_EXAMPLE_VEAERO);

  const lines = [
    "# Aero Vote Radar",
    "",
    "> Where to vote veAERO on Aerodrome (Base) this week to earn the most. Enter how much veAERO you hold and get whole percentages to paste into Aerodrome's voting page, ranked by what each pool pays per vote after your own vote dilutes it. Free, open source (MIT), read-only: no wallet connection, no signatures.",
    "",
    `Scanned from Base mainnet: ${generatedAt.toISOString()}. The scan re-runs every 6 hours.`,
    `Current epoch closes: ${utc(epochEndsAt)}. A vote only counts for the epoch it is cast in, so the suggestion below expires then.`,
    "",
    `Coming change: Aerodrome becomes Aero on ${AERO_LAUNCH_UTC}, with a new rewards system (sAERO and Predictive Allocation). How veAERO carries over has not been published yet; this file covers the current weekly veAERO vote. Source: ${AERO_LAUNCH_URL}`,
    "",
    `## This week's suggestion for ${LLMS_EXAMPLE_VEAERO.toLocaleString("en-US")} veAERO`,
    "",
  ];

  if (weights.length === 0) {
    lines.push("No pool qualified in this scan. Open the page for the live view.");
  } else {
    for (const w of weights) lines.push(`- ${w.percent}% ${w.symbol} (pool ${w.pool})`);
    lines.push(
      "",
      `Expected reward for that vote: about ${usd(weekly)} for the epoch, estimated from each pool's recent epochs and the vote weight it usually settles at. Pools whose rewards swing too much week to week (consistency below ${LLMS_MIN_CONSISTENCY}) are left out, as on the page. An estimate, not a promise: other voters move during the week.`,
    );
  }

  lines.push(
    "",
    `Pools scanned: ${ranked.length}.` +
      (migrating > 0
        ? ` Left out: ${migrating} pool(s) Aerodrome marks "Migrating" to new gauges; its vote page hides them by default.`
        : ""),
    "Different amounts split differently because your own vote dilutes each pool. For your balance, use the page.",
    "",
    "## How to use it",
    "",
    `- Web: ${SITE} — type your veAERO balance, copy the percentages, paste them into Aerodrome's vote page.`,
    "- CLI: `npx aero-vote-radar recommend --veaero 10000 --vote-ready`",
    "- MCP server for AI agents: `npx aero-vote-radar-mcp` (tools: recommend_allocation, list_pool_efficiency, backtest_strategy, get_my_veaero, prepare_vote_calldata)",
    "",
    "## Links",
    "",
    `- [Live page](${SITE})`,
    `- [Source and method](${REPO})`,
    `- [Raw pool data, JSON](${SITE}/data/snapshot.json)`,
    "- [npm package](https://www.npmjs.com/package/aero-vote-radar)",
    "",
    "Not financial advice. The tool prints numbers; the user casts the vote.",
    "",
  );

  return lines.join("\n");
}
