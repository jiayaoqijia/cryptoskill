---
name: trading-agents
description: Multi-agent stock and crypto research desk modelled on TauricResearch/TradingAgents. Four analysts (technical, fundamentals, news/macro, sentiment) write independent reports, bull and bear researchers debate, a research manager judges, a trader builds an exchange-valid plan (entry, stop, targets, size), a risk committee challenges it, and a portfolio manager issues a five-tier rating (Buy/Overweight/Hold/Underweight/Sell) backed by computed indicators and cited sources. Use whenever the user asks to analyse or rate a stock, index or crypto, asks whether to buy/sell/hold, wants entry/stop/target levels or a bull vs bear view, or mentions TradingAgents, including Indonesian phrasings like "analisis saham BBCA", "BBRI layak beli?", "prospek TLKM", "analisa teknikal/fundamental", .JK tickers, US tickers, and BTC/ETH. Also for comparing tickers or re-checking an earlier call. Research, not financial advice.
---

# Trading Agents

A simulated trading desk. Separate roles, separate evidence, a real debate,
and a decision that has to survive a risk committee. The value comes from
three disciplines, so protect them throughout:

1. **Independence**: each role sees only its own inputs, so the analysts
   aren't writing toward a verdict they already know.
2. **Verified numbers**: every price, indicator and ratio comes from a
   script output or a cited source. The desk never estimates numbers.
3. **Time discipline**: nothing after the analysis date is used.

Files in this skill (paths are relative to this SKILL.md's directory):
- `references/agents.md`: role cards for all 12 agents. **Read before step 3.**
- `references/data-sources.md`: data paths, fallbacks, search recipes,
  market rules (IDX, US, crypto). **Read at step 2.**
- `references/output-format.md`: chat summary and full report templates.
  **Read before step 9.**
- `scripts/fetch_data.py`: yfinance fetch → prices, fundamentals, news, technical snapshot.
- `scripts/indicators.py`: technical snapshot from any OHLCV CSV.
- `scripts/risk_tools.py`: tick-valid stop/targets, R:R, position size (IDX lots).
- `scripts/decision_log.py`: memory of past calls, outcome review, lessons.

---

## Step 0. Understand the request

Extract, without interrogating the user (state assumptions instead):

- **Ticker**, normalised to Yahoo format. Indonesian context or a bare
  4-letter IDX code → add `.JK` (BBCA → BBCA.JK). "bitcoin"/"BTC" → `BTC-USD`.
  Ambiguous (e.g. a code that is both a US and IDX listing) → pick the one
  the conversation implies and say so.
- **Analysis date**: default today. A past date means **backtest mode**
  (see data-sources.md §9).
- **Depth**: `quick`, `standard` (default) or `deep`; the user may also pick
  a subset of analysts.
- **User context** if given: already holding? average price? capital, risk
  tolerance, horizon. Feed it to the Trader and Portfolio Manager only.
- **Language**: respond in the user's language.

| Depth | Report length | Bull/Bear rounds | Risk rounds | When |
|---|---|---|---|---|
| quick | ~150 to 250 words | 1 | 1 | "cepat", multi-ticker comparisons, quick checks |
| standard | ~300 to 450 words | 2 | 1 | default |
| deep | ~450 to 700 words | 3 | 2 | user asks for thorough / deep / serious decision |

A round is one Bull turn plus one Bear turn. In rounds 2+, alternate who
opens so neither side always gets the last word.

## Step 1. Choose the orchestration mode and set up the run

**Mode A: real subagents.** If you can spawn subagents (for example a
Task/Agent tool in Claude Code or Cowork), each role runs as its own agent
with its own context. Use this whenever it is available; it is the closest
match to the original framework.

**Mode B: single context.** In a regular chat (claude.ai) you play every
role yourself. Independence then depends on the firewall protocol in step 3.

Create a run directory, e.g. `ta_runs/{TICKER}_{DATE}/` (in claude.ai use
`/home/claude/ta_runs/...`). Every artefact is written there as a file:
`sources.md`, `technical.md`, `01_technical.md`, `02_fundamentals.md`,
`03_news.md`, `04_sentiment.md`, `10_debate.md`, `11_plan.md`,
`20_trader.md`, `30_risk.md`, `40_decision.md`. Files are what enforce
separation: each role reads its inputs from disk, not from memory of other
roles.

## Step 2. Build the data snapshot

Read `references/data-sources.md`, then:

1. Try `python scripts/fetch_data.py {TICKER} --date {DATE} --outdir {RUN}`.
2. If it exits 2 (network blocked; normal on claude.ai) or 3, use the
   fallback paths: a user-uploaded CSV via `scripts/indicators.py`, a
   history page fetched and transcribed to CSV, or web search only.
   Don't stop to ask for data; proceed and flag limits.
3. Run web searches for fundamentals, news/macro and sentiment regardless;
   Yahoo's coverage is thin for many names, especially IDX. Log every source
   in `sources.md` with date, URL, analyst tag and the exact figures used.
   Scale searches to depth: quick ≈ 4 to 6, standard ≈ 8 to 12, deep ≈ 12 to 20.
4. If a decision log exists (the user uploaded `trading_agents_log.jsonl`,
   or one exists locally), run
   `python scripts/decision_log.py --log {LOG} review --ticker {TICKER} --price {last} --date {DATE}`
   and save the result for the Portfolio Manager.

Sanity-check the snapshot before any agent uses it: last bar date near the
analysis date, price in the right order of magnitude and currency, and
the correct company behind the ticker.

## Step 3. Analyst team

Read `references/agents.md` sections 1 to 2. Run the four analysts (or the
subset the user chose). Each writes its report file.

**Mode A.** Launch the analysts in parallel. Give each a self-contained
prompt:
```
You are the {ROLE} on a trading research desk analysing {TICKER} as of {DATE}.
Follow these rules and this role card exactly:
<paste "Shared rules" + the role's card from references/agents.md>
Depth: {depth} (length budget {…}). Language: {lang}.
Read ONLY these inputs: {file list}. Do not open other files in {RUN}.
You may run web searches only for your own topic; append each source to
{RUN}/sources.md tagged "{tag}". Write your report to {RUN}/{NN}_{role}.md
and return it.
```

**Mode B: firewall protocol.**
- Write each analyst report using only that analyst's inputs (re-read them
  from disk right before writing), then save it to its file.
- Reports are **final once written**. Do not go back and soften an earlier
  report after later ones point the other way; the disagreement is
  information the debate needs.
- Do not form or mention an overall view until the Research Manager step.
- Keep each report within its length budget so later steps have room.

## Step 4. Bull vs Bear debate

Follow the debate rules in `agents.md` §3. Inputs for both sides: the four
reports, the opponent's previous turns, and lessons from the decision log.
Each turn must rebut the opponent's strongest point first. Write all turns to
`10_debate.md`.

Mode A: run each turn as a fresh subagent call given the reports plus the
debate so far. Mode B: write each turn as that side only; the Bear should
be as good a lawyer as the Bull.

## Step 5. Research Manager

Judge the debate on evidence quality and write the investment plan
(`11_plan.md`) with a five-tier rating. Hold must be justified by a small
edge or thin evidence, never used as a compromise.

## Step 6. Trader

Translate the plan into a concrete proposal (`20_trader.md`). Compute
levels with `scripts/risk_tools.py` using ATR and pivots from
`technical.json`; add `--equity/--risk-pct` if the user gave capital. Quote
the script's numbers exactly.

## Step 7. Risk committee

Aggressive, Conservative and Neutral members (agents.md §5) debate the
proposal for the configured number of rounds. Each ends with a concrete
adjustment. Write to `30_risk.md`.

## Step 8. Portfolio Manager

Make the final call (`40_decision.md`): adopt or reject each risk
adjustment with reasons, apply lessons from the decision log explicitly,
re-run `risk_tools.py` if parameters changed, and set upgrade, downgrade and
exit triggers.

Then record the decision:
`python scripts/decision_log.py --log {LOG} add --ticker … --date … --rating … --price … --stop … --target … --confidence … --horizon … --thesis "…"`
Use `./trading_agents_log.jsonl` locally; on claude.ai use the uploaded log
if there is one, else a new file in the run directory.

## Step 9. Deliver

Read `references/output-format.md`.
1. Post the **chat summary** in the conversation.
2. Assemble the **full report** from the run files. If you can create
   files for the user (on claude.ai: write to `/mnt/user-data/outputs/` and
   share it with the file-presenting tool), save it as
   `{TICKER}_{DATE}_trading-agents.md`. Also share the updated
   `trading_agents_log.jsonl` so the user can upload it next time to give the
   desk memory; mention this once, briefly.
3. If data was limited, close with one line on how to unlock more (upload a
   1 to 2 year daily CSV, or allow the Yahoo hosts in network settings).

---

## Quality bar (check before delivering)

- Every number in the summary appears in a script output or `sources.md`.
- Company name matches the ticker; currency and price scale are right.
- No source is dated after the analysis date.
- Analyst stances are allowed to disagree, and the summary shows it.
- The Bear's best argument appears in the summary, even for a Buy.
- IDX plans use valid ticks and whole lots; stops sit outside daily noise
  (≥ ~1 ATR) and the first target offers ≥ ~1.5R, or the plan says why not.
- The final rating follows from the plan, the trader proposal and the risk
  adjustments; if it differs from the Research Manager's rating, explain why.
- One short "research, not financial advice" line, without further
  disclaimers.

## Handling special requests

- **"Quick answer only"**: run quick depth but keep all roles, and give just
  the chat summary. Offer the full report.
- **Multiple tickers**: quick depth each, then the comparison table from
  output-format.md §3. Warn up front that each ticker is a full run.
- **Follow-up questions** ("why did the bear lose?", "what if I hold at
  9,000?"): answer from the run files; re-run only the affected roles
  (e.g. Trader + Risk + PM for a new entry price).
- **Re-checking an old call**: run `decision_log.py review`, then a fresh
  analysis whose Portfolio Manager explicitly compares with the prior call.
- **User's personal stakes** (e.g. "all my savings"): the Conservative
  analyst and PM must address concentration and suitability plainly; the
  desk still gives its research view.
