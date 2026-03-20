# Sentiment Prompt Ideas for Trading

## 1. Stock Pre-Mortem + Sentiment Risk Analysis
- **Source:** https://techmitra.in/best-ai-prompts-for-stock-trading-business-finance/
- **Prompt:**
  "I am considering a long position in [Company Name] for a 3-year horizon. Conduct a pre-mortem analysis.
  Step 1: Assume the investment loses 50% in 18 months. List 5 plausible reasons why.
  Step 2: Search the web for employee reviews on Glassdoor/LinkedIn and customer complaints on Twitter for the last 6 months.
  Step 3: Correlate the financial risks from Step 1 with the sentiment in Step 2. Is management hiding operational stress? Provide a risk score out of 10."
- **Use Case:** Combine hypothetical downside analysis with live sentiment signals.

## 2. News Sentiment Labeling
- **Source:** https://www.pragmaticcoders.com/blog/top-ai-tools-for-traders
- **Prompt Template:** For each news article, assign one label: `Bullish`, `Neutral`, or `Bearish`.
- **Use Case:** Simple standardized classification for aggregated news impact scoring.

## 3. Twitter/X Sentiment for Specific Stocks
- **Example Context:** HistoricalOptionData examples (PLTR, MDB)
- **Prompt Template:** "Analyze X/Twitter sentiment for [Ticker] over the last [N] days and estimate bullish vs bearish percentages with key drivers."
- **Example Output Style:** "60% bullish on PLTR, driven by options flow and AI optimism."
- **Use Case:** Quick social-sentiment snapshot for entry/exit context.

## 4. Advanced Model Direction
- **Reference:** Nature paper on global Twitter sentiment modeling.
- **Approach:** Fine-tune a transformer model on market-specific local sentiment for equities/crypto.
- **Use Case:** Build a reusable sentiment signal layer for systematic strategies.
