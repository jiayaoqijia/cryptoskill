# Monthly Paragraph Contract

Use this contract when writing or rewriting the public monthly secondary-market report. It defines what each paragraph must do. The report should feel like an exchange research publication: conclusion first, data second, implication third.

## Global Rules

- Every paragraph must answer one of three jobs: `what changed`, `why it matters`, or `what to watch next`.
- Do not publish method notes, task status, package paths, data-source boilerplate, or chart indexes in the public report.
- Do not write filler captions. If a chart is included, the nearby paragraph must interpret it.
- Use month scope only. Do not mix daily-report wording into the monthly report.
- If data is missing, write a compact limitation sentence and avoid unsupported ranking or directional claims.
- Keep each paragraph to 1-3 sentences.

## Required Structure

### 1. Title

Format:

`# YYYY 年 M 月二级市场月报`

Purpose:

- State report month only.
- Do not add slogans or subtitles.

### 2. Opening Thesis

One paragraph.

Must write:

- The month's market regime in one sentence: repair, risk expansion, defensive rotation, deleveraging, or range-bound divergence.
- The main contradiction in one sentence: for example `price repaired but breadth lagged`, `volume rose but leverage crowded`, or `majors led while long tail stayed weak`.

Must use:

- Market cap monthly change.
- BTC dominance change or breadth proxy.
- One confirming or contradicting risk indicator such as funding, DVOL, F&G, or CEX volume.

Do not:

- List numbers mechanically.
- Mention data sources.

### 3. Key Takeaways

4-6 bullets. Each bullet is one conclusion, not one raw metric.

Bullet 1, market regime:

- Write whether the month moved from defense to repair, repair to trend, trend to distribution, or remained fragmented.
- Include market cap start/end or monthly change.

Bullet 2, leadership:

- Write whether BTC/majors led or risk broadened.
- Include BTC dominance change and/or outside-Top10 share.

Bullet 3, asset dispersion:

- Write whether top assets were broadly positive, mixed, or weak.
- Include top performer, bottom performer, and median or winners/losers count.

Bullet 4, leverage:

- Write whether leverage was neutral, crowded long, crowded short, or mixed.
- Include funding and optionally OI/DVOL.

Bullet 5, sentiment:

- Write whether sentiment confirmed or lagged price.
- Include F&G ending regime or monthly average.

Optional bullet 6, chain/sector:

- Write whether DeFi/NFT/stablecoin data supports risk expansion.
- Include TVL, NFT volume, or stablecoin liquidity signal.

### 4. Macro Proxy And Market State

Two paragraphs plus 1-2 charts.

Paragraph 1, what changed:

- Interpret total market cap and BTC dominance together.
- State the regime: core-asset repair, broad beta expansion, defensive concentration, or liquidity withdrawal.

Paragraph 2, why it matters / next watch:

- Explain what would confirm continuation next month.
- Use volume, breadth, or volatility as the confirmation gate.

Charts:

- Market cap chart.
- BTC dominance chart.

### 5. Exchange Flow And Activity

One to two paragraphs plus chart if available.

Paragraph 1, what changed:

- If CEX rows are available, write total sample 30d volume, estimated month-over-month change, strongest venue, weakest venue.
- If CEX rows are missing, write a limitation sentence and fall back to total market volume only.

Paragraph 2, why it matters:

- Interpret whether activity confirms price repair.
- Mention execution quality, liquidity concentration, or venue rotation only if the data supports it.

Chart:

- CEX 30d volume change chart only when generated.

### 6. Major Assets And Breadth

Two paragraphs plus 2 charts.

Paragraph 1, asset performance:

- Write strongest and weakest top assets.
- Include winners/losers count and median return when available.
- Explain whether the month was single-name driven, majors-led, or broad.

Paragraph 2, breadth:

- Describe outside-Top10 market-cap share as concentration only.
- State whether long-tail risk appetite is expanding only when a broader asset-return sample confirms it; otherwise disclose the evidence gap.

Charts:

- Top10 monthly performance chart.
- Outside-Top10 share chart.

### 7. On-Chain Risk Appetite

One to two paragraphs plus charts as available.

Paragraph 1, DeFi:

- Write total DeFi TVL and leading-chain share.
- Interpret whether chain-level capital is concentrated or rotating.

Paragraph 2, NFT / non-fungible risk:

- Write NFT volume only when fig4 data succeeds.
- If NFT data is missing, write that NFT is not used as a core conclusion for the month.
- Interpret whether NFT risk appetite confirms or lags liquid-token risk appetite.

Charts:

- DeFi TVL share chart.
- NFT volume chart only when available.

### 8. Derivatives Positioning

Two paragraphs plus 3 charts.

Paragraph 1, leverage bias:

- Interpret BTC and ETH calendar-month funding history together; a run-time ticker snapshot is not monthly evidence.
- Classify as neutral, crowded long, crowded short, or divergent.

Paragraph 2, volatility and positioning:

- Interpret DVOL range and month-end level.
- Use OI only when its snapshot time is within 48 hours of target month-end; otherwise omit it and disclose the gap.
- State what derivatives imply for next-month risk: squeeze risk, low-vol carry, or repricing risk.

Charts:

- Funding chart.
- OI chart only when the month-end timing gate passes.
- DVOL chart.

### 9. Sentiment And Volatility Pricing

One to two paragraphs plus charts.

Paragraph 1, sentiment confirmation:

- Write F&G ending value and Chinese regime label.
- Compare sentiment with price action: confirming, lagging, overheated, or divergent.

Paragraph 2, volatility context:

- Use realized volatility or DVOL context.
- Explain whether market risk is being priced cheaply, fairly, or expensively.

Charts:

- F&G chart.
- Realized volatility chart.

### 10. Next-Month Trading Framework

Three numbered paragraphs.

Paragraph 1, base case:

- State preferred exposure bucket: core assets, selective top alts, defensive/stable carry, or low exposure.
- Include the condition that keeps this base case valid.

Paragraph 2, upside case:

- State what must improve before increasing beta exposure.
- Use at least two triggers from: breadth, volume, F&G, funding, DVOL, smart-money position, stablecoin liquidity.

Paragraph 3, risk case:

- State what invalidates the constructive view.
- Include concrete de-risking action: reduce chase exposure, raise margin buffer, tighten liquidity threshold, or take profit.

## Missing Data Rules

- Missing CEX flow: do not rank venues; use market-wide volume and state the limitation in one sentence.
- Missing NFT data: do not include the NFT chart; write that NFT is excluded from core conclusions.
- Missing F&G: use volume, funding, and DVOL to discuss sentiment indirectly.
- Missing Deribit: do not infer leverage crowding; state that derivatives confirmation is unavailable.
- Missing breadth: avoid altseason or long-tail claims.

## Quality Bar

Before publishing, check:

- Each section has interpretation, not just data.
- No section contains only one weak sentence unless data is missing.
- Charts are not broken or referenced when files are absent.
- The conclusion direction matches the signs of the data.
- Language is restrained: avoid `全面开启`, `必然`, `确定性`, `史诗级`, and promotional wording.
