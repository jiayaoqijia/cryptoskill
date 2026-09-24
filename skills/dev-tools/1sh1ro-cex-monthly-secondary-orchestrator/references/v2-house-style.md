# V2 House Style (Current Approved Version)

Use this style after orchestration to match the latest accepted monthly-report output.

## Narrative rules

- Use month scope only (`YYYY-MM-01` to month end).
- Avoid figure-number wording in正文 (avoid `图1/图2/...`).
- Keep conclusions concise and evidence-driven (Coinbase-like tone).
- Write for an external reader by default, not for internal production review.
- Lead with thesis, then evidence. Do not lead with metadata.
- Each section should answer three things in order: `what changed`, `why it matters`, `what to watch next`.
- For exact paragraph responsibilities, follow `monthly-paragraph-contract.md`. This file is the paragraph-level source of truth.
- Prefer short narrative paragraphs over long checklist sections.
- Merge derivatives interpretation into the DVOL section in the gap-fill block.
- Remove the standalone NFT chart from正文 when the chart is not informative for the month.
- Stablecoin opportunity content, when included, must be concise:
  - one framing paragraph
  - at most one compact table
  - no large comparison dumps from daily reports
- Default voice should be institutional and restrained:
  - short declarative sentences
  - no promotional wording
  - avoid certainty words like "必然", "一定", "全面开启"
  - prefer probability framing: "更可能", "仍需确认", "倾向于"

## Exchange-style tone map

- `Coinbase style`: conclusion-first, neutral wording, explicit uncertainty.
- `Binance style`: chart-led flow, section compactness, broad-reader readability.
- `KuCoin style`: short-horizon tactical close and risk reminders.
- Apply all three in this order: structure (Coinbase), presentation rhythm (Binance), close (KuCoin).

## What must not appear in the public page

- `整月口径`
- `口径说明`
- `范围限定`
- `数据可用性说明`
- `参考样本与方法`
- `图表逐项解读`
- `月内图表索引`
- `数据源`
- `执行状态`
- raw pipeline wording such as `packages`, `manifest`, `run.log`

## Section design rules

- Section titles should sound like editorial headlines, not worksheet labels.
- Good examples:
  - `市场在修复，但没有进入全面进攻`
  - `主流币修复明显，长尾依旧偏弱`
  - `衍生品不拥挤，但情绪还是冷的`
- Avoid titles that sound like internal report scaffolding:
  - `市值与主导率分析`
  - `板块与资产分化`
  - `衍生品市场洞察`
- Preferred default section set:
  - `Key Takeaways`
  - `宏观代理与市场状态`
  - `交易所流量与资金活跃度`
  - `主流资产表现与市场广度`
  - `衍生品仓位温度`
  - `情绪与波动定价`
  - `下月交易框架（基准情景）`

## Interpretation rules

- Do not hardcode bearish language. Interpretation must follow the sign and shape of the data.
- If market cap rises but breadth stays weak, call it repair without broad risk expansion.
- If funding is near zero, describe it as neutral positioning, not crowded leverage.
- If F&G stays depressed while price repairs, call out sentiment lag explicitly.
- If a chart says little, cut the chart or compress it into one sentence.

## Chart rules

- Use light theme for all charts (white background, soft gray grid).
- `fig3_defi_tvl_share.png`: render as donut chart for single-month composition.
- `fig6_altcoin_outside_top10_share.png`: render as 100% stacked bar (`BTC / Top10 Alt / Outside Top10`).
- `chart_deribit_funding.png`: light-theme grouped bars (`Funding 8h` + `Current funding`, in bps).
- `chart_deribit_oi.png`: USD-normalized grouped bars; convert options OI from native units via `public/ticker` last price.

## Data-source annotation

Keep method notes available in internal artifacts when needed, but do not surface source/method boilerplate in the public page unless it materially changes interpretation.
