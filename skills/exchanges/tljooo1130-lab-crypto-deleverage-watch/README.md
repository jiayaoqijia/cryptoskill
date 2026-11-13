# crypto-deleverage-watch

Monitor whether a crypto perpetual-futures **leverage flush** looks complete, using only **public OKX and Binance APIs** (no keys). Four conditions, near/met thresholds, a state file, and alerts only when a status upgrades or falls from `met`.

用 OKX / 币安公开接口，判断永续合约的杠杆出清是否可能已经完成。四个条件、接近/满足阈值、状态文件；只在状态升级或从「满足」回落时提醒。

> 以上只是信息整理，不构成投资建议。
> This is information only, not investment advice.

## Quick start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/watch.py --state ./state.json --tz Asia/Bangkok
```

The script prints one JSON object with all four conditions, per-asset statuses, `notify` (only the changes that should alert), and a `possibly mostly flushed` / `可能已基本出清` flag when **three or more** conditions are `met` for the same asset.

可选：按小时汇总 OKX 已成交强平：

```bash
python3 scripts/okx_liquidations.py --start 2026-11-13 --tz Asia/Bangkok
```

可选：每日 BTC 杠杆快照与图（需要 `requirements-optional.txt`）：

```bash
python3 -m pip install -r requirements-optional.txt
python3 scripts/daily_leverage.py --data-dir ./data/leverage
```

## Default thresholds

| # | Condition | Near | Met |
|---|-----------|------|-----|
| 1 | Account long/short ratio (OKX primary, Binance too) | < 2.3 | < 2.0 |
| 2 | Coin-denominated OI drop from the running high since window start | ≥ 15% | ≥ 20% |
| 3 | OKX top-trader **position (notional)** long/short ratio | ≥ 0.95 | ≥ 1.0 |
| 4 | OKX filled liquidations, last 2h short USD vs long USD | shorts ≥ 50% of longs | shorts ≥ 100% of longs **and** last hour > prior hour |

Binance `topLongShortPositionRatio` is reference only; it is flagged when it falls below 1.5. Binance does not publish `allForceOrders`.

## Agent skill

See [SKILL.md](SKILL.md) for endpoints, state format, how to read the numbers, and a cron / routine example.

Suggested GitHub repo name: `crypto-deleverage-watch`.

## License

MIT License
