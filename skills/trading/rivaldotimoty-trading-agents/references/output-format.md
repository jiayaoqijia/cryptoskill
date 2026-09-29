# Output formats

Two deliverables per analysis:
1. **Chat summary**: what the user reads first, in the chat.
2. **Full report**: every agent's output, saved as a markdown file when the
   environment allows files (otherwise offer to print it on request).

Write both in the user's language. The templates below are in English;
translate headings naturally (Indonesian example headings are given).

---

## 1. Chat summary

Keep it scannable: roughly 250 to 400 words plus the two tables.

```markdown
## {TICKER} · {Company name} · as of {analysis date}

**Final rating: {RATING}** · confidence {low/medium/high} · horizon {…}
Last price {price} {ccy} ({change}% d/d) · data up to {last bar date}

{2 to 3 sentence thesis in plain language: why this rating, what matters most.}

| | Level | Note |
|---|---|---|
| Entry | {zone or trigger} | {why here} |
| Stop | {price} ({-x%}) | {structure / ATR basis} |
| Target 1 / 2 | {p1} / {p2} | {R-multiples} |
| Size | {lots/units or risk %} | {risk basis} |

**If you don't own it:** … · **If you already own it:** …

| Desk | View | Key point |
|---|---|---|
| Technical | Bullish/Bearish/Neutral | … |
| Fundamentals | … | … |
| News & Macro | … | … |
| Sentiment | … (score) | … |
| Bull vs Bear | {winner} | {decisive argument} |
| Risk committee | {main adjustment} | … |

**Strongest bull point:** … · **Strongest bear point:** …
**Watch:** upgrade if … · downgrade if … · exit if …
**Data limits:** {missing data, stale sources, backtest caveats; omit line if none}

_Research output from a simulated multi-agent desk, not financial advice._
```

Indonesian heading suggestions: "Keputusan akhir", "Level", "Kalau belum
punya / Kalau sudah punya", "Meja analis", "Poin bull terkuat / Poin bear
terkuat", "Pantau", "Keterbatasan data", closing line "_Hasil riset simulasi
multi-agen, bukan saran investasi._"

Rules:
- No number appears here that is not in the full report.
- If a desk was skipped (user chose fewer analysts), write "not run".
- If the rating is Hold, the "Entry" row becomes the trigger that would make
  it actionable (e.g. "breakout above 10,250 on volume > 1.5× avg").

---

## 2. Full report file

File name: `{TICKER}_{YYYY-MM-DD}_trading-agents.md`

```markdown
# {TICKER}: multi-agent research report
Analysis date: … · Depth: quick/standard/deep · Mode: subagents / single-context
Data paths used: … · Benchmark: …

## 0. Summary
{the chat summary, verbatim}

## 1. Data snapshot
{technical.md content}
{fundamentals key table}
{sources.md list}
{fetch/data warnings}

## 2. Analyst reports
### 2.1 Technical · 2.2 Fundamentals · 2.3 News & Macro · 2.4 Sentiment

## 3. Bull vs Bear debate
{all turns in order}
### Research Manager: investment plan

## 4. Trader proposal
{including risk_tools.py output}

## 5. Risk committee
{all turns}

## 6. Portfolio Manager: final decision

## 7. Decision memory
{prior decisions on this ticker with outcomes; lessons applied; log entry saved}

## Appendix: method
Roles and flow follow TauricResearch/TradingAgents (arXiv 2412.20138),
re-implemented as a Claude skill. Numbers come from scripts/indicators.py,
scripts/risk_tools.py and the cited sources.
```

---

## 3. Multi-ticker comparison

When the user asks to compare several tickers, run each at quick depth,
then add:

```markdown
| Ticker | Rating | Confidence | Tech | Fund | News | Sent. | R:R to T1 | Key risk |
|---|---|---|---|---|---|---|---|---|
```
followed by a 3 to 5 sentence ranking with reasons. Warn up front that each
ticker is a full run and uses a meaningful share of the user's usage.
