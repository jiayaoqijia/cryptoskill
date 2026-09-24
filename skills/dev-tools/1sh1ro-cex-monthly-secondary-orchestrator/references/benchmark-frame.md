# Benchmark Frame (Coinbase / Binance / KuCoin)

This reference exists to keep monthly reports close to how large exchanges and brokers actually publish.
It is not a request to imitate wording. It is a request to imitate structure, pacing, and editorial judgment.

## Coinbase

Observed from official "Crypto Market Positioning" pages:

- Lead with `Key takeaways`, not with methodology.
- Organize the body by market lenses such as `Technicals`, `Flows`, `Market Depth`, `Volumes`, `Open Interest`.
- Keep each section short: one judgment paragraph, then a chart, then one follow-up sentence.
- Use neutral institutional language. Do not overclaim. Prefer "mixed", "neutral", "slightly defensive", "wait-and-see" over dramatic labels.
- Let structure do the work. Coinbase does not expose production notes like source manifests, execution status, or appendix-style chart indexes to readers.

Implication for our reports:

- Start with a short thesis paragraph and 4 to 6 takeaways.
- Group charts by topic, not by chart number.
- Every chart must answer one question: what changed, why it matters, what it implies next.

## Binance

Observed from official "Monthly Market Insights" pages:

- Open with a clear monthly title and concise takeaways.
- Make the page chart-led. A chart should be followed by a compact explanation block, not by a mechanical caption.
- Use themed sections such as market performance, breadth, DeFi, NFT, derivatives, calendar/risk.
- Keep the tone analytical but readable for a broad crypto audience.
- Avoid long methodological detours inside the public page.

Implication for our reports:

- One section should carry one market idea.
- Put the most decision-useful charts early.
- Remove weak or repetitive charts rather than force-completing a template.

## KuCoin

Observed from official market reports:

- Lead with market pulse first.
- Use short, event-aware commentary.
- Sections often flow as `Market`, `Major Asset Changes`, `Outlook`, `Macro`, `Policy`, `Industry Highlights`.
- Writing is tighter and more audience-facing than institutional research.

Implication for our reports:

- Use KuCoin-style short horizon phrasing for the final outlook or tactical risk section.
- Keep bullet lists short and event-linked.
- Do not let the page become a data dump.

## Editorial Rules Derived From These Samples

- Public reports are for readers, not for the production pipeline.
- Never expose sections like `数据可用性说明`, `参考样本与方法`, `口径说明`, `范围限定`, `图表索引`, `执行状态` in the public-facing body.
- Never write `图1/图2/...` headings.
- Never leave obvious template residue such as wrong month references or generic "系统性回撤" language when the data shows repair.
- Avoid appendix behavior in正文. If a table does not help the reader make a decision, cut it.

## Monthly Content Blueprint (What to write, what to measure)

Use this as the default public monthly skeleton:

For paragraph-level instructions, use `monthly-paragraph-contract.md`. The outline below defines sections; the paragraph contract defines what each paragraph must write.

1. `Key Takeaways`
- Write: 4-6 one-line conclusions with direction and confidence.
- Measure: market cap change, BTC dominance change, top/bottom major-asset returns, breadth proxy.

2. `Macro Proxy and Market Regime`
- Write: risk-on/risk-off state and whether crypto is in repair, trend, or distribution.
- Measure: market cap path, BTC dominance path, realized volatility regime (use in-report proxies when external macro is unavailable).

3. `Flow and Activity`
- Write: where trading activity concentrated and whether participation broadened.
- Measure: major CEX 30d volume change, leaders/laggards in exchange activity.

4. `Leaders vs. Breadth`
- Write: whether gains are concentrated in majors or diffusing into long tail.
- Measure: top-coin monthly returns, winners/losers count, outside-top10 share.

5. `Derivatives Risk Temperature`
- Write: leverage crowding, positioning bias, and liquidation sensitivity.
- Measure: funding, futures/options OI mix, DVOL range and month-end level.

6. `Sentiment and Narrative Confirmation`
- Write: whether sentiment confirms price or lags price.
- Measure: F&G regime and path, realized-vol path, narrative concentration signal when available.

7. `Next-Month Trading Framework`
- Write: base case with explicit trigger conditions and risk controls.
- Measure: trigger thresholds tied to funding, DVOL, breadth, and activity expansion.

## How to combine

- Use Coinbase for section logic and tone discipline.
- Use Binance for chart-led page flow.
- Use KuCoin for the closing tactical voice.
- Default to a reader-facing report, not an analyst worklog.
