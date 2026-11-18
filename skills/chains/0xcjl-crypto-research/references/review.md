# 30/90天自动复盘

## 调度

在专用Research Bot创建一个宿主例行任务：每天09:00，Asia/Bangkok。运行`due`读取已保存判断的到期项；不自动发现新币。空队列保持安静，有完成复盘、失败或需用户行动才通知。

每条判断as_of+30/90个24小时为目标时点；每天扫到期可能晚于目标，因此按原时间取历史数据，不能把任务执行当天价格冒充到期价格。同一decision_id+期限只有一个成功结果。pending_data下次继续；不要因通知超时重复创建整个任务。

## 对每个到期项

1. 读取旧报告、原始账本、当时来源和事前条件；不能修改原记录。辨认原信号有效期，短线与长期观察分开。
2. 批量采集对应时点价格、基准，以及足以验证原条件的链上/项目/X证据。价格优先使用目标时点之后第一个已收盘小时K线；无小时数据可用实际快照但必须在目标之后24h以内，并披露偏移。晚执行需找历史数据。
3. 模型核对资产、场所、计价/换算、时间和数据可比性，解释风险/催化/链上变化。场所/instrument必须匹配冻结基线。价格或预选基准暂缺时用pending_data；缺基准需benchmark_gap。永久无可靠数据才可complete，并写final_data_unavailable_reason和对应data_gap/benchmark_gap，不补造0。
4. 模型写review JSON，脚本计算方向收益和相对收益并追加账本；运行stats核对分母。报告同时评估原短线窗口是否失效；30/90收益不代表实际成交或盈利。

## 算术口径

- 标的收益：(P_horizon/P_reference - 1)*100；基准收益相同公式；相对收益为两者之差，单位百分点。
- BUY价格上涨方向命中，SELL价格下跌方向命中；持平不命中，WATCH/UNDETERMINED/NOT_APPLICABLE不进入方向命中分母。WATCH 仍按基线计算价格变化并检验事件，结果单列在 stats 的 WATCH_tracking（counts_toward_hit_rate=false）。BUY相对收益为正、SELL为负记相对方向命中，分别统计。
- 30/90天、BUY/SELL各列样本数、命中、方向命中率、相对样本与命中、不可评估数量及独立资产数。重复同一资产判断相关，不把快照样本当独立交易。
- 风险/事件主张分别用occurred/not_occurred/unknown，并附对应证据；无法观察不能记预测失败或成功。不给风险等级算未经定义的统一胜率。
- 基准端点需与标的端点相差不超过1h，基线与报告相差不超过15min。原信号的报价需报告前15min内；时间/来源无法保证时不计入准确率。

## review JSON字段

decision_id、horizon_days（30或90）、authored_by=model、execution_agent、model、reviewed_at、status（complete或pending_data）、assessment、quote、benchmark_quote、assertion_results。

quote结构同原判断的reference_quote（含venue和instrument）；无可靠报价为null，并填写data_gap。原记录有基准但没有可靠benchmark_quote时填写benchmark_gap，并保持pending_data；只有永久不可评估才填写final_data_unavailable_reason并关闭。相对不可评估数量单列。assertion_results每项id与原主张对应，status为occurred/not_occurred/unknown，已确定结果附evidence_refs；complete必须覆盖每个原主张，unknown也要保留。用新的证据包运行`review`，不要复制原证据当作到期新事实。

`audit`检查账本哈希链；它只检测一致性，不是第三方时间认证。若发现账本异常、锁文件遗留、原记录找不到或身份变更，停止该项并报告具体缺口，不删除/重建账本掩盖问题。

## 调度提示词

你是Research Bot。现在执行crypto-research的到期复盘。先读取已安装SKILL.md和references/review.md，运行doctor（不需要每次network探测）和due；runtime为安装验收记录的路径。无到期项保持安静。每个到期项先读原判断，脚本批量收集数据，模型解释/反证/复查条件，运行review追加记录并生成报告。只处理原账本，不生成新币名单；不交易/不发布/不改凭据。成功结果幂等，暂时缺数据记录pending_data并在下次继续。汇报新完成、实质失败或需用户行动；给出证据/报告位置和实际Agent/可核实模型。不要把配置成功声称为30/90天真实复盘已发生。
