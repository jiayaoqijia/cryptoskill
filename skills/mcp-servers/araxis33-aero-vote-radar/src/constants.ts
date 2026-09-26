// Verified against https://raw.githubusercontent.com/velodrome-finance/sugar/master/deployments/base.env
// and cross-checked on Basescan (contract names LpSugar / RewardsSugar match).
export const BASE_CHAIN_ID = 8453;

// Overridable via env var so users with their own Base RPC (Alchemy, Infura, etc.)
// get a much higher rate-limit ceiling than the shared public endpoints.
export const BASE_RPC_URL = process.env.BASE_RPC_URL ?? "https://base-rpc.publicnode.com";

export const VOTER_ADDRESS = "0x16613524e02ad97eDfeF371bC883F2F5d6C480A5" as const;
export const REWARDS_SUGAR_ADDRESS = "0x1b121EfDaF4ABb8785a315C51D29BCE0552A7678" as const;
// VotingEscrow (the veAERO NFT contract). Obtained by calling `Voter.ve()` on
// the address above rather than copied from docs, and re-verified 2026-08-08.
// Replaces VeSugar, whose `byAccount` reverts on a public RPC for accounts with
// many locks — see the comment on VOTING_ESCROW_ABI in abi.ts.
export const VOTING_ESCROW_ADDRESS = "0xeBf418Fe2512e7E6bd9b87a8F0f294aCDC67e6B4" as const;

// How many trailing weekly epochs to pull per pool for the trend estimate.
export const TREND_EPOCHS = 6;

// How many past epochs the `backtest` command replays by default. Each tested
// epoch needs its own full TREND_EPOCHS window of *older* history to form the
// estimate it would have had at the time, so the on-chain fetch depth is
// BACKTEST_EPOCHS + TREND_EPOCHS. RewardsSugar keeps plenty of history, but
// every extra epoch is more data per pool across hundreds of pools, so this
// stays modest by default and is overridable with `--epochs`.
export const BACKTEST_EPOCHS = 6;

// Upper bound on `--epochs`/`epochs` for the backtest command and MCP tool. The
// on-chain fetch depth (BACKTEST_EPOCHS + TREND_EPOCHS worth of epochs, per
// pool) scales directly with this, across every live-gauge pool — an unbounded
// value here means one mistyped flag (or an agent-supplied argument) turns
// into an enormous multi-hundred-pool fetch against a shared public RPC.
export const MAX_BACKTEST_EPOCHS = 20;

// Pools whose trailing-average epoch value is below this are excluded from
// rankings — at that size, one small one-off bribe swings the "predictive edge"
// percentage wildly without representing a meaningful voting opportunity.
export const MIN_TRAILING_USD = 10;

// Floor, in veAERO, below which a pool's vote weight is too small to form a
// ratio against. `refillRatio` divides a pool's typical settled weight by its
// current one, and both sides of that division need to be a real number of
// votes: measured on live data, an unfloored version topped the "will be
// refilled" list with a pool holding 1,364 votes against a history of zero,
// reporting a 2,577x refill that described nothing. Same reasoning as
// MIN_TRAILING_USD, applied to the denominator instead of the numerator.
export const MIN_VOTE_BASELINE = 1000;

// The veAERO budget around which the two measurements of the vote basis stop
// agreeing, and so the size above which the default basis is the one the
// evidence favours.
//
// Two honest measurements point opposite ways and both are kept:
//
//   predict-check scores each basis against the weight epochs actually settled
//   at, from real mid-week vantage points. "previous" wins there: 17% median
//   error and unbiased, against 26% and +4% high for "typical". That is why it
//   is the default.
//
//   backtest scores dollars instead of weights, replaying closed epochs. There
//   "typical" earned more at every small and mid budget, and the gap closes as
//   the budget grows. Measured 2026-08-29 over the last 5 epochs, typical
//   against the default: +114% at 5,000 veAERO, +99% at 25,000, +51% at
//   200,000, +6% at 750,000, then -4% at 1,000,000, -24% at 2,000,000 and -41%
//   at 5,000,000.
//
// They are not in conflict about the facts. A median accuracy figure weights
// every pool equally; an allocator does not — it deliberately picks the pools
// whose weight looks lowest relative to their incentives, which is exactly the
// tail where "previous" is wrong and "typical" (max of tally and usual weight)
// is protective. As the budget grows, dilution rather than pool-picking decides
// the outcome, the protection turns into over-estimated weight everywhere, and
// the default pulls ahead.
//
// The crossover moves week to week — a run the day before that one put the
// 1,000,000 figure at -30.7% rather than -4%.
//
// RE-MEASURED 2026-09-15, twice, and the second one is the one that counts.
//
// The first re-run that day found the advantage gone entirely: +4.2% at 2,000
// veAERO, -11.4% at 5,000, +4.0% at 25,000, -3.1% at 100,000, with the sign
// alternating. On that reading the small-budget warning was removed.
//
// It was measured on a pool universe that was missing most of Aerodrome.
// Concentrated-liquidity pools were being dropped in pool discovery, so the
// backtest was choosing from 107 pools where 359 exist and could not see the
// largest vote weights on the chain at all. With them restored, the same
// command over the same five epochs, filtered at --min-consistency 0.5:
//
//   veAERO     default      typical    difference   typical ahead in
//    2,000      $57.43       $87.64        +52.6%       5 of 5 epochs
//    5,000     $102.33      $180.70        +76.6%       5 of 5 epochs
//   10,000     $178.12      $287.42        +61.4%       5 of 5 epochs
//   25,000     $585.04      $559.32         -4.4%       4 of 5 epochs
//   50,000   $1,201.74      $991.38        -17.5%       4 of 5 epochs
//  100,000   $2,105.05    $1,606.93        -23.7%       4 of 5 epochs
//
// The crossover is real, it is not noise — below it "typical" wins every single
// epoch, not a majority — and it sits near 20,000 veAERO rather than the
// 1,000,000 recorded above. That old figure was never a measurement of
// Aerodrome; it was a measurement of the twentieth of it the tool could see.
//
// Which is the lesson worth keeping: a number re-measured on a broken universe
// is not a check on the number, it is the same mistake with a fresh date on it.
// The crossover still moves week to week, so this remains a threshold for a
// warning, never for silently switching the basis.
export const VOTE_BASIS_CROSSOVER_VEAERO = 20_000;

export const DEFILLAMA_PRICE_URL = "https://coins.llama.fi/prices/current";

// Bounds how long a single DefiLlama batch request can hang before it's treated
// as a failure. Without this, a stalled connection (no response, no error) never
// resolves or rejects, so a hung request would block a whole ranking run forever
// — and for mcp-server.ts, which holds one process open across many tool calls,
// that wedges every future call too, not just the one that hit it.
export const DEFILLAMA_TIMEOUT_MS = 8000;

// How many extra attempts a DefiLlama batch gets after an initial failure
// (network error, non-ok response, or timeout) before falling back to $0 —
// mirrors chain.ts's retry around the Base RPC client, which exists for the
// same reason: a public, unauthenticated endpoint drops occasional requests
// under load, and that shouldn't cost a whole batch its pricing. Kept lower
// than the RPC's retryCount (6) since a batch request is comma-joined and
// costs real latency to redo, and this runs inside mcp-server.ts's per-call
// budget rather than a single eth_call.
export const DEFILLAMA_RETRY_COUNT = 2;

// Delay between DefiLlama retry attempts. Short relative to DEFILLAMA_TIMEOUT_MS
// since most failures worth retrying (a dropped connection, a transient 5xx)
// clear within a second, not the RPC client's 1500ms (that backs off against
// rate-limiting; this backs off against a blip).
export const DEFILLAMA_RETRY_DELAY_MS = 400;

// Max token addresses per DefiLlama price request. A run can touch bribe/fee
// tokens across hundreds of live-gauge pools, and one comma-joined URL covering
// all of them at once risks tripping URL-length limits on DefiLlama's edge/CDN —
// which would silently zero out pricing for every token in the run, not just the
// ones that were actually the problem. Batching bounds the blast radius of a
// single failed/oversized request to just that batch.
export const PRICE_BATCH_SIZE = 50;

// How many DefiLlama batch requests run at once. Bounded rather than unbounded
// (a run can produce several batches) so a burst of simultaneous requests
// doesn't look like abuse to DefiLlama's edge/CDN — matches the concurrency
// cap already used for Base RPC calls in pools.ts/efficiency.ts/backtest.ts.
export const PRICE_BATCH_CONCURRENCY = 4;

// How long a successfully looked-up price stays valid before it's refetched.
// The CLI is a fresh process per invocation so this never matters there, but
// mcp-server.ts holds one process open for the life of a client connection —
// without a TTL, prices would be cached forever for that process and silently
// go stale.
export const PRICE_CACHE_TTL_MS = 5 * 60 * 1000;

// How long the $0 fallback stays valid — much shorter than a real price, and
// deliberately so. The two are not the same kind of fact: a real price is
// information that ages slowly, while a $0 fallback is the absence of one, and
// it is written both for tokens DefiLlama genuinely doesn't price and for a
// batch that merely failed to reach it. Caching those together for five minutes
// meant one timed-out request could value a token at $0 across a whole run of
// mcp-server.ts calls — enough to drop real pools below MIN_TRAILING_USD and
// reorder a ranking, with nothing in the output saying why. At 30s a transient
// failure costs one refetch; a genuinely unpriced token costs a cheap retry per
// batch, since it is looked up alongside the rest of its batch either way.
export const PRICE_FAILURE_CACHE_TTL_MS = 30 * 1000;

// Concentrated-liquidity factories whose pools Aerodrome is migrating to new
// MEV-resistant gauges ahead of the Aero launch. Its own app badges every pool
// they created "Migrating", tells liquidity providers to move to the new
// version, and leaves those pools out of the vote page's default "Most
// rewarded" list — so a recommendation into one points at a pool the voter
// cannot find where they vote, and whose fees are draining away.
//
// Read from Aerodrome's front end on 2026-09-16, after a voter could not find
// the radar's CL-cbBTC/EDGE pick: the first address is its
// VITE_OLD_SLIPSTREAM_FACTORY_ADDRESS_8453, and every pool listed from the
// second carried the same badge. Together they held 163 of the 360 ranked
// pools and 9 of the top 20 that day. The replacement factory,
// 0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef, is not migrating. Lower-case, as
// compared by `isMigratingFactory`.
export const MIGRATING_POOL_FACTORIES: ReadonlySet<string> = new Set([
  "0x5e7bb104d84c7cb9b682aac2f3d509f5f406809a",
  "0xade65c38cd4849adba595a4323a8c7ddfe89716a",
]);

// Floor, as a fraction of the previously published snapshot's pool count,
// below which `writeSnapshot` refuses to publish a new one. Per-pool epoch
// fetch failures are caught individually in `rankPoolsByEfficiency` (a public
// RPC dropping part of a burst under load is a recurring, observed failure
// mode here) so a degraded scan returns fewer pools rather than throwing —
// only an empty scan was ever refused. That let a scan hobbled by rate
// limiting silently overwrite a good, git-committed snapshot with a fraction
// of the real pool list, with nothing louder than a console.error to say so.
// The committed history has held 360-370 pools for months, so a drop below
// half that is a scan problem, not a sudden and genuine drop in live gauges.
export const SNAPSHOT_MIN_POOL_RATIO = 0.5;

// Default consistency floor for anything that *recommends* a vote (CLI
// `recommend`, MCP `recommend_allocation`) and for the backtests that score
// it, so they test the strategy they recommend. The hosted page has opened on
// 0.5 since it shipped; the CLI and MCP defaulted to no filter, and on the
// 2026-09-25 scan that put 100% of 10,000 veAERO into one pool whose weight had
// dropped to a twentieth of its usual for a week (consistency 0.49).
//
// Measured before changing it (backtest, 8 epochs, 2026-09-25), total USD:
//   10,000 veAERO:  no filter $208.73 -> 0.5 $299.27 (+43%)
//   25,000 veAERO:  no filter $662.50 -> 0.5 $790.99 (+19%)
//   100,000 veAERO: no filter $2,221.18 -> 0.5 $2,560.74 (+15%)
// Leaving out the newest epoch the gain is still +11% / +15% / +22%.
// `pools` keeps no filter: it lists, it does not recommend.
export const DEFAULT_MIN_CONSISTENCY = 0.5;
