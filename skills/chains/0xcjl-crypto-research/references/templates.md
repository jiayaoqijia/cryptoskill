# 报告与模型记录

## 报告骨架

标题：标的＋研究日期/时间（Asia/Bangkok，同时注明数据UTC时间）

- 执行：实际Agent、可核实模型或unknown、skill版本、模式/深度、研究问题。
- 身份：项目官网、链/合约或native_id；交易池另列；无币项目说明代币状态。
- 核心判断：先回答用户问题，每条结论带URL/evidence_id、数据时间；推断有依据与反证。
- 项目画像与发展：做什么、谁用、可验证进展/用户、团队/资金/商业机制、竞争。
- 适用的链上变化：指标、前值/后值、窗口/单位/范围、来源、潜在解释和反证；无前值建基线。
- 代币机会：流动性、注意力、筹码分别给证据和判断；注意力项目在此之前先给排雷结果。
- 风险与信号：风险等级及最弱环节；信号、适用周期、有效期、触发/失效、条件区间依据、退出限制；无币为NOT_APPLICABLE。
- 最强反方与缺口：哪些事实会改变结论，下一步复查什么。
- 来源表：ID、原文链接、来源/采样数据时间、取得时间、口径/限制、事实或自述/估计/推断。
- 复盘登记：decision_id、30/90到期时间、报告位置。只有record成功后才称已登记。

纯项目研究按适用性收缩，不机械填价格表；quick保留身份、结论、风险、来源与缺口。可使用表格，但每个关键判断仍有证据及时间。实测数据、模拟测试、分析判断、已调度任务分别说明状态。

## 模型判断JSON

以下是字段约定，不是真实信号；值由模型根据实际证据填写：

```json
{
  "decision_id": "unique-safe-id",
  "authored_by": "model",
  "execution_agent": "actual agent",
  "model": "actual model or unknown",
  "as_of": "ISO timestamp with timezone",
  "target_name": "verified project/token name",
  "asset": {"chain": "chain", "native_id": "native-asset-id"},
  "signal": "WATCH",
  "risk": "unknown",
  "signal_window": "research horizon",
  "valid_until": "ISO timestamp with timezone",
  "thesis": "model's evidence-based judgment",
  "invalidation_conditions": ["specific falsifying condition"],
  "recheck_conditions": ["specific measurable condition"],
  "evidence_refs": ["existing successful evidence IDs"],
  "reference_quote": {"asset": {}, "price": 0, "currency": "USD", "observed_at": "...", "venue": "...", "instrument": "...", "evidence_refs": ["source-id"]},
  "baseline_gap": "仅在确实拿不到可靠报价时填写原因，否则删除",
  "benchmark": null,
  "benchmark_gap": "reason for not using a benchmark, when applicable",
  "assertions": [{"id": "event-1", "condition": "event/metric, horizon, threshold and scope defined beforehand", "check_by": "ISO8601 截止时间", "evidence_refs": ["source-id"]}],
  "safety_checks": [
    {"item": "mint", "status": "checked_none_found", "method": "读了什么、怎么查的", "evidence_refs": ["source-id"]},
    {"item": "owner_privileges", "status": "confirmed_risk", "method": "...", "evidence_refs": ["source-id"]},
    {"item": "sell_simulation", "status": "unverified", "note": "为什么没验证"},
    {"item": "proxy_upgrade", "status": "unverified", "note": "..."},
    {"item": "pause_blacklist", "status": "unverified", "note": "..."},
    {"item": "tax", "status": "unverified", "note": "..."},
    {"item": "lp_lock", "status": "not_applicable", "note": "为什么不适用"},
    {"item": "source_verified", "status": "unverified", "note": "..."}
  ],
  "report_path": "saved report path",
  "data_cutoff": "ISO time: latest fetched_at of any cited source; no data after this",
  "analysis_completed_at": "ISO time the judgment was finished; data_cutoff <= as_of <= analysis_completed_at",
  "claims": [{"claim_id": "c1", "text": "one conclusion as written in the summary", "label": "fact|inference|self_reported|third_party_estimate|calculation|unknown|unverified",
              "sources": [{"evidence_ref": "existing ok evidence ID", "source_url": "https://full link",
                           "observed_at": "data's own time, or null + observed_at_unknown_reason",
                           "fetched_at": "must equal the evidence record retrieved_at when present",
                           "raw_path": "existing raw file"}]}],
  "review_objections": [{"id": "o1", "source": "path of terra/sol review output", "objection": "what the reviewer said",
                         "disposition": "adopted|retained",
                         "summary_change": "adopted: how the summary changed", "ledger_change": "adopted: how thesis/conditions changed",
                         "retention_reason": "retained: why the original stays"}],
  "review_objections_none_reason": "only when review_objections=[]: why no review step ran"
}
```

0.1.3起record是必过关卡：缺claims字段、任一来源缺source_url/observed_at/fetched_at/raw_path、raw_path文件不存在、来源取得晚于data_cutoff，或任一复核异议未二选一处理，都会拒绝登记。先改摘要和判断JSON，再record；不能先登记后补。

代币用asset.address替代native_id；不得同时填两个。无币项目asset=null、signal=NOT_APPLICABLE，reference_quote=null。对更新增加supersedes指向旧decision_id。

BUY/SELL必须填新鲜reference_quote：asset、price（正数USD）、currency=USD、observed_at、venue、instrument、evidence_refs。benchmark如适用为asset+reference_quote；默认非BTC资产用BTC衡量大盘背景，可另列事先确定且历史数据可靠的同类基准。BTC没有可靠外部基准时明确benchmark_gap，不用BTC自己作基准。不得事后换基准。

模型记录signaling窗口和valid_until；未触发条件的研究写WATCH，而不是先登记成BUY再事后挑选成功触发案例。assertions事先写可观察的事件/阈值/截止期（check_by 必填），不能事后补写原预测。

0.1.4 WATCH 默认留基线：WATCH 必须有 reference_quote（拿不到时写 baseline_gap 说明原因）、至少一条可验证 assertion（确实没有时写 no_assertion_reason）、signal_window 和 valid_until。复盘时照常算 return_pct 和事件结果（outcome.events / event_status），但 counts_toward_hit_rate=false，只出现在 stats 的 WATCH_tracking，不进 BUY/SELL 胜率。

0.1.4 安全检查四态：有 asset 的记录必须给 safety_checks，覆盖 mint、owner_privileges、proxy_upgrade、pause_blacklist、tax、sell_simulation、lp_lock、source_verified 八项，状态只能是 checked_none_found（已查未发现，需 method+evidence_refs）、confirmed_risk（已证实风险，需 method+evidence_refs）、unverified（未验证，需 note）、not_applicable（不适用，需 note）。不得写“安全”。本地文件证据可用 file:///绝对路径 作为 source_url（文件必须存在）。

## 勘误记录（errata）

已登记判断与报告原文不改。发现错误时另写 `runtime/reports/<decision_id>.errata-<n>.md`，再运行 `errata` 追加一条 record_type=erratum：erratum_id、target_decision_id（必须存在）、authored_by、execution_agent、model、errata_path、corrections[]。每条 correction 有 id、original_text、original_location、disposition=corrected（附corrected_text）或retained（附retention_reason），以及与 claims 相同字段的 sources[]。`due` 输出会列出该判断的 errata，复盘必须同时读勘误。勘误不改变 due 时间、信号或命中率分母；如需改变信号，用新 decision_id + supersedes。
