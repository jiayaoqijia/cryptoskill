# Research on Technical Indicators for Stock Swing Trading

Recent academic papers (2025-2026), especially on arXiv, emphasize empirical backtests of technical indicators like RSI, MACD, and Bollinger Bands for short-term (days to weeks) trading. This aligns well with swing strategies. A common result is that nonlinear ML/DL models outperform simple baselines.

## 1. Deep Learning for Short-Term Equity Trend Forecasting: A Behavior-Driven Multi-Factor Approach
- **Authors:** Yuqi Luan et al.
- **Year:** 2025 (arXiv:2508.14656)
- **Key Findings:** A dual-task MLP on 40 behavioral alpha factors (including MACD, RSI, Bollinger Bands from price/volume) predicts 5-day returns and direction, capturing momentum herding, reversals, and divergences. It outperforms CNN/SVM in IC, ICIR, and Sharpe via long-short portfolios.
- **Indicators/Patterns:** RSI rebounds, MACD crosses, Bollinger Band deviations with volume.
- **Performance:** Superior information ratio; top-K backtests show stable alpha.
- **Implementation Notes:** Input z-scored factors -> MLP (64-32 ReLU neurons, dropout 0.1) -> dual heads (MSE + 0.5 BCE loss, Adam `lr=5e-4`).
- **Link:** https://arxiv.org/abs/2508.14656

## 2. Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy
- **Authors:** Hongyang Yang et al.
- **Year:** 2025 (arXiv:2511.12120)
- **Key Findings:** Ensemble PPO/A2C/DDPG agents on 30 DJIA stocks, with state including MACD and RSI, show robustness across regimes using a turbulence index.
- **Indicators/Patterns:** RSI overbought/oversold, MACD momentum.
- **Performance:** Highest Sharpe vs. DJIA and min-variance baselines.
- **Implementation Notes:** Continuous actions (buy/sell/hold shares); reward = portfolio delta - 0.1% transaction cost; GitHub code available.
- **Link:** https://arxiv.org/abs/2511.12120

## 3. Evolving Financial Trading Strategies with Vectorial Genetic Programming
- **Authors:** Sara Silva et al.
- **Year:** 2025 (arXiv:2504.05418)
- **Key Findings:** Vectorial GP variants (complex numbers, strongly typed) evolve profitable rules using technical indicators across 7+ years and 3 instruments, outperforming standard GP.
- **Indicators/Patterns:** RSI, Bollinger Bands, oscillators, band systems.
- **Performance:** Profitable despite EMH-related challenges.
- **Implementation Notes:** GP on vectors of past prices plus indicators (SMA/EMA/RSI/BB).
- **Link:** https://arxiv.org/abs/2504.05418

## 4. Trading on Uncertainty: FutureQuant Transformer’s Distribution-Based Strategy for Futures Markets
- **Authors:** Wenhao Guo et al.
- **Year:** 2025 (arXiv:2505.05595)
- **Key Findings:** A Transformer predicts price quantiles/distributions; a simple strategy using RSI/ATR/BB thresholds produces gains.
- **Indicators/Patterns:** RSI, Bollinger Bands, ATR thresholds.
- **Performance:** 0.1193% average return per 30-minute trade, above SOTA baselines.
- **Implementation Notes:** Quantile loss with attention over LOB/high-frequency data.
- **Link:** https://arxiv.org/abs/2505.05595

## 5. A Robust Objective Function for Reducing Overfitting in Data-Driven Trading Strategies (GT-Score)
- **Authors:** Alexander Sheppert
- **Year:** 2026 (arXiv:2602.00080)
- **Key Findings:** GT-Score optimization for RSI/MACD/BB strategies on 50 S&P 500 names (2010-2024) yields 98% better generalization (validation/train ratio).
- **Indicators/Patterns:** RSI thresholds, MACD periods, BB window/width.
- **Performance:** Higher generalization ratio (0.183) vs. Sharpe/Sortino/simple objectives; statistically significant (`p < 0.01`).
- **Implementation Notes:** GT = `mu ln(z) r^2 / sigma_down`; `z = (mu - mu_BH) / SE`; walk-forward + Monte Carlo (15 seeds).
- **Link:** https://arxiv.org/abs/2602.00080

## Notes
- Short-term focus (5-day and above) is suitable for swing systems.
- Empirical backtests often favor ML ensembles/GP over static rule systems.
- No direct code snippets are included in these summaries; implementation is typically via PyTorch/TF (DL) or DEAP (GP).
- Practical priority: combine RSI + MACD + BB with robust validation to avoid overfitting.
