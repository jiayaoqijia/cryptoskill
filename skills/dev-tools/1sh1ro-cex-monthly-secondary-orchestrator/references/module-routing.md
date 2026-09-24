# 月报模块路由

| 模块别名 | 内部模块 | 脚本与数据源 |
|---|---|---|
| `top-assets` | `fig2` | CoinGecko 当前成分 + 严格自然月 `market_chart/range` |
| `defi` | `fig3` | DefiLlama 历史链 TVL |
| `nft` | `fig4` | CryptoSlam 日度 global sales；缺月失败，不填零 |
| `concentration` | `fig6` | CMC 全市场历史 + CoinGecko 市值历史 |
| `derivatives` | `deribit` | Deribit 历史 funding、DVOL；OI 使用月末 48h 门禁 |
| `core` | `core_report` | CMC、Alternative.me、CoinGecko 历史序列 |

查看来源注册表：

```bash
python3 scripts/run_monthly_module.py --describe
```

运行单模块：

```bash
python3 scripts/run_monthly_module.py \
  --module derivatives \
  --month 2026-06 \
  --outdir /tmp/monthly-modules/deribit
```

单模块输出包含原始产物、`run.log` 和 `module_manifest.json`。完整月报仍调用 `run_cex_monthly_orchestrator.py`；两种入口复用 `monthly_module_registry.py`，避免命令和日期口径漂移。
