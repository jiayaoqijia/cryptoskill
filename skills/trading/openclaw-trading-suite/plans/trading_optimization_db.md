# Trading Optimization Database

## 2024 Baseline Test Results

| Date | Hypothesis | Params | Win Rate | Avg Gain | Max DD | Sharpe |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-02-19 | 9 | rsi_p=10, bb_p=27, atr_p=11, ma_p=27, rsi_t=69, gain_t=0.05 | 0.70 | 0.08 | -0.05 | 1.3 |
| 2024-02-19 | 8 | rsi_p=16, bb_p=23, atr_p=13, ma_p=17, rsi_t=75, gain_t=0.07 | 0.80 | 0.015 | -0.02 | 2.0 |
| 2024-02-19 | 3 | rsi_p=13, bb_p=20, atr_p=20, ma_p=15, rsi_t=72, gain_t=0.1 | 0.70 | 0.12 | -0.05 | 1.5 |
| 2024-02-19 | 21 | rsi_p=17, bb_p=27, atr_p=17, ma_p=17, rsi_t=68, gain_t=0.07 | 0.65 | 0.10 | -0.08 | 1.3 |
| 2024-02-19 | 12 | rsi_p=18, bb_p=28, atr_p=15, ma_p=16, rsi_t=75, gain_t=0.15 | 0.70 | 0.10 | -0.07 | 1.4 |
| 2024-02-19 | 20 | rsi_p=10, bb_p=24, atr_p=18, ma_p=25, rsi_t=71, gain_t=0.11 | 0.55 | 0.08 | -0.06 | 1.1 |
| 2024-02-19 | 13 | rsi_p=14, bb_p=18, atr_p=14, ma_p=16, rsi_t=71, gain_t=0.05 | 0.55 | 0.08 | -0.10 | 1.2 |
| 2024-02-19 | 10 | rsi_p=14, bb_p=26, atr_p=17, ma_p=29, rsi_t=73, gain_t=0.07 | 0.65 | 0.09 | -0.05 | 1.5 |
| 2024-02-19 | 5 | rsi_p=12, bb_p=17, atr_p=14, ma_p=27, rsi_t=67, gain_t=0.08 | 0.55 | 0.08 | -0.06 | 1.1 |
| 2024-02-19 | 11 | rsi_p=15, bb_p=18, atr_p=16, ma_p=29, rsi_t=72, gain_t=0.09 | 0.65 | 0.09 | -0.05 | 1.4 |

### 2024 Summary
- Average Win Rate: 0.65
- Best Hypothesis: 8 (arbitrage, simulated)
- Optimal Bounds:
  - RSI Period: 10-20
  - BB Period: 15-30
  - ATR Period: 10-20
  - MA Period: 15-30
  - RSI Threshold: 65-75
  - Gain Target: 0.05-0.15

## 2026 Overnight Deep Work Results (2026-02-20)

| Date | Hypothesis | Params | Win Rate | Avg Gain | Max DD | Sharpe |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-02-20 | 15 | rsi_p=20, bb_p=26, atr_p=16, ma_p=18, rsi_t=66, gain_t=0.124 | 0.6 | 0.09 | -0.05 | 1.5 |
| 2026-02-20 | 20 | rsi_p=19, bb_p=15, atr_p=18, ma_p=18, rsi_t=68, gain_t=0.125 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 12 | rsi_p=19, bb_p=25, atr_p=14, ma_p=15, rsi_t=65, gain_t=0.114 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 13 | rsi_p=15, bb_p=30, atr_p=12, ma_p=26, rsi_t=71, gain_t=0.113 | 0.55 | 0.08 | -0.1 | 1.2 |
| 2026-02-20 | 19 | rsi_p=15, bb_p=23, atr_p=19, ma_p=15, rsi_t=66, gain_t=0.062 | 0.5 | 0.07 | -0.1 | 0.9 |
| 2026-02-20 | 19 | rsi_p=20, bb_p=27, atr_p=17, ma_p=18, rsi_t=72, gain_t=0.148 | 0.5 | 0.07 | -0.1 | 0.9 |
| 2026-02-20 | 17 | rsi_p=17, bb_p=24, atr_p=13, ma_p=23, rsi_t=67, gain_t=0.089 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 21 | rsi_p=17, bb_p=30, atr_p=15, ma_p=17, rsi_t=67, gain_t=0.121 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 16 | rsi_p=10, bb_p=30, atr_p=10, ma_p=18, rsi_t=70, gain_t=0.081 | 0.65 | 0.12 | -0.08 | 1.3 |
| 2026-02-20 | 21 | rsi_p=20, bb_p=26, atr_p=15, ma_p=29, rsi_t=68, gain_t=0.126 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 18 | rsi_p=15, bb_p=27, atr_p=11, ma_p=23, rsi_t=65, gain_t=0.097 | 0.55 | 0.08 | -0.06 | 1.1 |
| 2026-02-20 | 11 | rsi_p=17, bb_p=18, atr_p=20, ma_p=17, rsi_t=69, gain_t=0.134 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 16 | rsi_p=18, bb_p=15, atr_p=14, ma_p=22, rsi_t=70, gain_t=0.118 | 0.65 | 0.12 | -0.08 | 1.3 |
| 2026-02-20 | 20 | rsi_p=14, bb_p=30, atr_p=20, ma_p=20, rsi_t=66, gain_t=0.143 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 15 | rsi_p=19, bb_p=23, atr_p=19, ma_p=27, rsi_t=74, gain_t=0.095 | 0.6 | 0.09 | -0.05 | 1.5 |
| 2026-02-20 | 11 | rsi_p=12, bb_p=20, atr_p=13, ma_p=20, rsi_t=69, gain_t=0.102 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 14 | rsi_p=13, bb_p=27, atr_p=17, ma_p=30, rsi_t=68, gain_t=0.139 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 11 | rsi_p=19, bb_p=29, atr_p=20, ma_p=15, rsi_t=70, gain_t=0.083 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 13 | rsi_p=17, bb_p=20, atr_p=12, ma_p=26, rsi_t=66, gain_t=0.127 | 0.55 | 0.08 | -0.1 | 1.2 |
| 2026-02-20 | 18 | rsi_p=19, bb_p=23, atr_p=16, ma_p=23, rsi_t=75, gain_t=0.072 | 0.55 | 0.08 | -0.06 | 1.1 |
| 2026-02-20 | 17 | rsi_p=12, bb_p=26, atr_p=14, ma_p=29, rsi_t=67, gain_t=0.055 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 11 | rsi_p=20, bb_p=22, atr_p=11, ma_p=21, rsi_t=68, gain_t=0.149 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 11 | rsi_p=18, bb_p=16, atr_p=13, ma_p=16, rsi_t=74, gain_t=0.103 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-02-20 | 16 | rsi_p=17, bb_p=17, atr_p=18, ma_p=22, rsi_t=68, gain_t=0.094 | 0.65 | 0.12 | -0.08 | 1.3 |
| 2026-02-20 | 18 | rsi_p=14, bb_p=30, atr_p=19, ma_p=15, rsi_t=67, gain_t=0.094 | 0.55 | 0.08 | -0.06 | 1.1 |

### 2026 Overnight Deep Work Summary
- Average Win Rate: 0.28
- Best Hypothesis: 16
- Optimal Bounds:
  - RSI Period: 10-20
  - BB Period: 15-30
  - ATR Period: 10-20
  - MA Period: 15-30
  - RSI Threshold: 65-75
  - Gain Target: 0.05-0.15
