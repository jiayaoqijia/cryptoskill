# Glossary — the terms a literal translation gets wrong

Almost every name in the JSON is an ordinary English concept and should simply be translated:
peak, drawdown, survival rate, graduation rate, holders, market cap, liquidity, pool, launch.
Those are **not** listed here.

What is listed is the small set of Chinese trading slang that a word-by-word translation renders
either meaningless or misleading. When you write in Chinese, use the rendering in this column and
nothing else — these are the words traders actually use, and an invented synonym reads as a
mistranslation of a score they are being asked to act on.

| JSON / concept | Chinese | Note |
|---|---|---|
| CONDUCT (the axis) | 信誉 | not 品行/行为 — 信誉 is what a trader checks before buying |
| POWER (the axis) | 实力 | not 力量 |
| TOTAL | 综合 | the headline number |
| dump (`dump_gate`) | 割 | literally "to cut". Selling into buyers' bids at the open. Not 倾销, not 抛售 — those describe size, 割 describes who pays for it |
| open-dump | 开盘收割 | the tier line: dumping *at* the open specifically |
| dump rate | 割率 | over coins that carry his own trades, not over launches |
| severity | 狠度 | how hard he cut, 0–1 per coin. Not 严重性 |
| pull / pull multiple | 抽水 / 抽水倍数 | cash out ÷ cash in, per coin. 抽水 is "siphoning", not 提取 |
| 1st sell | 首卖 | seconds from open to his first sell |
| the curve (`on_curve`) | 内盘 | the bonding curve. A coin that never graduated is stuck 在内盘 — never 曲线 |
| graduated (`graduated`) | 外盘 / 毕业 | reached an open market off the curve |
| flagship | 代表作 | his highest-peaking coin. Not 旗舰 |
| walk-away / CTO (`walkaway_rate`) | 撒手 / CTO | he abandoned the coin to the community |
| self-snipe (`self_snipe_rate`) | 自狙 | he buys his own open. Disclosed, never scored |
| bundled buying (`bundler`) | 打包买入 | bought in the creation block. Could be his alts, a paid service, or someone else's bot |
| untradeable | 卖不出去 | nobody can sell it — stuck on the curve or a dead pool. Not 不可交易 |
| unaccounted exit (`exit_unrecorded`) | 出货路径查不到 | the position is gone and no row explains how |
| sniping a launch | 打新 | buying at the open — the action the whole score is about |

The five dump tiers (`dump_gate.tier`), in order of severity:

| `tier` | Chinese | Meaning |
|---|---|---|
| `sys` | 系统性 | pool drained, or he dumps most opens — hard cap 45 / 49 |
| `often` | 经常 | dump rate above 30% — CONDUCT − 20, TOTAL capped 74 |
| `rare` | 偶发 | dump rate ≤ 30% — not capped at all |
| `often_unproven` | 无法证明他不割 | fewer than 5 coins carry his own trades — ceiling only, no deduction |
| `none` | 一次都没割 | ≥ 5 traded coins and not one dump among them — measured clean, **not** "no data" |

`none` is the one tier that is routinely said backwards. It means there IS a sample and the sample is
clean. Never render it as 查不到 / no record found.

The four verdict bands (`score.band`): `buyable` 可以打 · `mixed` 一般 · `avoid` 别碰 · `stay_away` 远离.
