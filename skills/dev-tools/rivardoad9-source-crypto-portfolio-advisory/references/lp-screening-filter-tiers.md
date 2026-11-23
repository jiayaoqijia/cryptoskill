# LP screening: filter tiers + measured funnel (1 Oct 2026)

Companion to `references/meteora-dlmm-lp-screening.md` (pool criteria, cost model, data pull) and
`references/dlmm-position-setup.md` (ticket placement). This file is about **how to hand filter settings
to the user** — which fields to set, which to leave alone, and what to say about the result count.

## Lesson that produced this file

The user filled the whole conservative filter stack the way it was handed over and got **zero pools** —
"malah kosong nih terlalu ketat ya". Nothing was broken: the engine core alone leaves 122 of 2.000 pools,
and Fee/TVL ≥5% cuts that to 4. Stacking judgment filters on top took it to 0. The failure was in the
handover, not the filters.

**Rule: never hand over a filter list without the expected survivor count, and split it into two tiers.**

## Measured funnel (2.000 DLMM pools scanned, datapi, 1 Oct 2026)

| Filter added | Survivors |
|---|---|
| scan total | 2.000 |
| TVL $50–500k | 205 |
| + pool age ≥48h | 201 |
| + volume 24h ≥$10k | 150 |
| + both tokens verified (**engine core complete**) | **122** |
| + Fee/TVL ≥5% | **4** |
| + Fee/TVL ≥3% | 10 |
| + Fee/TVL ≥2,31% (1× break-even) | 12 |

Fee/TVL is the single cliff (122 → 4) and it is arithmetic, not a bug. Of the 4 at the 5% bar, 3 failed
security (top10 28–48%, mint/freeze still live, 0,2–3% tax) — so a full-stack day legitimately ends with
**one** candidate, sometimes zero. Say that out loud instead of loosening silently.

Reject histogram worth showing back as evidence: 1.740 TVL <$50k · 91 fee/TVL <0,8% · 53 TVL >$500k ·
51 volume <$10k · 21 token unverified · 2 fee/TVL >25%.

## Filter panel fields (meteora.ag and the third-party screener with presets Default / Hermes / Meteora)

Token Details (Verified, JupShield Safeguard, Jupiter Organic Score, New Listing, No High Supply
Concentration, No High Single Ownership) · Market Cap · Token Age (Hours) · Holders · Top 10 Holders % ·
Dev Balance % · Launchpads · Pool Details (DLMM, DAMM V2, Has Farm) · Pool Age (Hours) · Volume · Fees ·
Fee/TVL % · TVL · Base Fee · Active TVL · Volume/Active TVL · Fee/Active TVL · DLMM Bin Step + Fee
Collection Mode · DAMM V2 (Concentrated Liquidity, Dynamic Fee, Permanently Locked Liquidity,
Fee Scheduler).

### Tier 1 — engine-validated core (always set)

| Field | Set to | Why |
|---|---|---|
| Verified | ✅ | engine `bothTokensVerified` |
| Fee/TVL % min–max | **5 – 25** strict · **2,3 – 25** relaxed | 25% = `MAX_FEE_TVL_RATIO`; real $300 floor is 5,79%; 2,3% = 1× break-even |
| TVL min–max | 50.000 – 500.000 | `MIN/MAX_TVL_USD` |
| Pool Age (Hours) min | 48 | `MIN_POOL_AGE_HOURS` |
| Volume min | 10.000 | `MIN_24H_VOLUME_USD` |
| Launchpads / Pool Details | DLMM ✅ · DAMM V2 ❌ | engine is DLMM-only; Fee Scheduler pools have time-decaying fees that invalidate fee/TVL |
| Holders min | 3.000 | entry filter |
| Top 10 Holders max % | 25 | entry filter |
| Bin Step (screening) | leave blank | bin step sets fee-per-swap vs grid width, not profitability — in the *position form* it matters (`dlmm-position-setup.md`) |

### Tier 2 — judgment (my additions; each one costs candidates)

JupShield Safeguard ✅ · No High Supply Concentration ✅ · No High Single Ownership ✅ · Jupiter Organic
Score min 60 · Market Cap min $500k · Token Age min 168 h · Dev Balance max 5% · Fees min $2.000 ·
Base Fee min 0,2% · Active TVL min $5.000 · Volume/Active TVL min 2 · Fee/Active TVL min 2,4% ·
Has Farm blank. Announce these as judgment, not as engine rules — the engine validates none of them.
**Token Age (token ≥7 days) and Pool Age (pool ≥48h) are separate fields, both in hours.**

## Micro-pool trap to name outright

**630 of 2.000 pools had fee/TVL ≥1% with TVL <$50k.** Without a TVL minimum the list fills with
$3–5k-TVL pools advertising 25–38% fee/TVL — that is arb-bot churn against the main pool, not yield, and a
$300 ticket would be 5,6% of the pool (rule: ≤1–2%). The user opened exactly one of these (e/acc-USDC,
$5,3k TVL) straight from the "Top Performers" tab; the correct venue for the same token was the SOL pool
at $291k TVL / 7,00% fee/TVL.

Also: the **"Top Performers" tab surfaces exactly these micro pools** (performance-sorted). Screen from
the `All` tab with filters, then sort by Fee/TVL × volume 24h.

## Deliverable shape

Tier-1 values → expected survivor count → Tier-2 optional list with the warning that each shrinks it →
the reject histogram → the one or two candidates that survived, with the number that disqualified the
rest. If nothing survives, say "no trade today" and keep the bar where it is.
