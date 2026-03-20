# Recent Academic Research on Swing Trading Strategies

Swing trading is mostly a practitioner term. In academic literature, related work is usually framed as short-term momentum, mean reversion, or technical-analysis strategies with multi-day holding periods. This summary focuses on empirical studies with backtests that can inform algo-bot implementation.

## 1. A Hybrid AI-Driven Trading System Integrating Technical Analysis, Machine Learning and Financial Sentiment for Regime-Adaptive Equity Strategies
- **Authors:** Akshay Ajith et al.
- **Year:** 2026 (arXiv:2601.19504)
- **Key Findings:** Combines trend-following (EMA, MACD), mean-reversion (RSI, Bollinger Bands), sentiment (FinBERT), ML signal generation (XGBoost), and regime filtering (volatility/returns).
- **Strategies:** Multi-modal directional + normalization + sentiment + regime-aware risk adjustment.
- **Performance:** Backtested on 100 S&P 500 stocks over 6 years (4 train, 2 test) in Backtrader; 135% return over 24 months (`$100k` to `$235k`), stronger Sharpe and lower drawdown vs. major benchmarks.
- **Automation Adaptations:** Directly implementable in Python/Backtrader with structured + unstructured inputs.

## 2. A Comprehensive Analysis of Machine Learning Models for Algorithmic Trading of Bitcoin
- **Authors:** Syed Qaisar Jalil et al.
- **Year:** 2024 (arXiv:2407.18334)
- **Key Findings:** Evaluates 41 ML models (21 classifiers, 20 regressors) for BTC prediction; RF and SGD stand out on profit/risk tradeoff under volatility.
- **Strategies:** Direction/regression prediction feeding buy/sell decisions.
- **Performance:** Backtesting + forward + real-world testing; top models show positive PnL and stronger Sharpe.
- **Automation Adaptations:** Transferable to stock swing bots using similar TA feature engineering.

## 3. Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?
- **Authors:** Waylon Li et al.
- **Year:** 2025 (arXiv:2505.07078)
- **Key Findings:** LLM timing can outperform in short windows but underperform over long horizons (20+ years, 100+ symbols) due to bias behavior.
- **Strategies:** LLM-generated timing signals from unstructured data.
- **Performance:** Long-term results deteriorate vs. passive benchmarks; framework highlights bullish/bearish regime bias.
- **Automation Adaptations:** Use LLM signals only with strict regime filters and broad out-of-sample testing.

## 4. Predictive Modeling of Foreign Exchange Trading Signals Using Machine Learning Techniques
- **Authors:** ScienceDirect publication
- **Year:** 2025
- **Key Findings:** ML models (Ridge, KNN, RF, XGBoost, GBDT, ANN, LSTM, GRU) outperform MA crossover baselines for signal prediction.
- **Strategies:** ML-based signal generation for daily/intraday decisioning.
- **Performance:** Backtests from 2000-2023 on six major forex pairs show better return/risk profile vs. momentum baseline.
- **Automation Adaptations:** Strong fit for feature-rich swing pipelines.

## Additional Practitioner Empirical Source
- **QuantifiedStrategies.com Swing Trading Backtests (2026):** 10+ backtested swing strategies (mean reversion, breakouts, etc.) with settings/code ideas. Useful for prototyping despite non-academic methodology.

## Notes
- Source pool: recent arXiv and journal searches, with emphasis on empirical evaluation.
- For implementation, prioritize robust walk-forward validation and regime-aware risk controls.
