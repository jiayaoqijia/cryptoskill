# 空闲决策、阶段结束与目标完成

适用于已启用过 dsh_orchestration 的任务。普通短任务不因此新增编排或完成表单。

## 查看与处置

status 的 decision_review 返回当前 signature、待办状态、投递情况和已有处置。全部工作空闲时，运行层保存一次待决策事件；通知最多尝试两次，领取消息不等于处置。通知失败保留待办，不自动接管、续做或不断调用模型。

根据实际用户目标、原证据、剩余依赖和成本选择 continue / waiting / blocked / deferred / complete。运行层校验结构、版本和引用，不能验证专业判断。resolve 不启动工作；continue 保留为 pending_action，继续时另行 followup/dispatch，空闲未执行时只作有界提醒，不能把记录意图当作执行成功。暂停任务仍需符合原 resume 条件。

```json
{"action":"resolve","task":"TASK_ID","options":{"expected_signature":"从最新 status.decision_review.signature 获取","resolution":{"decision":"blocked","goal_status":"unfulfilled","summary":"已完成局部检查，尚缺材料 B，不能据此宣称目标已完成。","unresolved":[{"work":"WORK_ID","issue":"缺少材料 B，无法区分解释 X/Y","disposition":"blocked","reason":"当前可读材料不含所需字段","next_step":"取得 B 后作一项区分实验"}]}}}
```

work 可省略；需要更多证据的分支必须以实际 work ID 保留在 unresolved 中。每项写 issue、disposition、reason，可附 next_step 和 evidence_refs。disposition 可为 continue / waiting / blocked / deferred / out_of_scope。无需把所有设想都登记为待办。

等待/阻塞/暂缓可以选填带时区的未来 recheck_at；这是一次软复查，不是 Solver 截止，也不自动恢复任务。没有复查时点或新相关证据时，处置后休眠。重复状态读取、同义汇报和心跳不制造新决策；目标、实质证据、结果或复核状态变化后按新签名重新判断。

## 完成总目标

已 review 只表示分支经过处理。needs_more_evidence 仍是不确定，不能从总任务里静默抹去。finish/disable/cancel 随时可按现有清理条件结束阶段或执行，不要求先证明任务成功。

要把 analysis_session 转为 complete：

1. 核对用户交付范围；所有在范围内的目标已经达成。
2. 使用最新签名 resolve：decision=complete、goal_status=fulfilled、summary、completion_scope、evidence_refs、unresolved。
3. finish 或 disable 结束编排并确认清理，再调用 analysis_session transition complete。共享 Python 状态层会再次核对，CLI 与原生入口使用同一检查。

完整交付可用以下结构，ID 与版本必须取实际返回值：

```json
{"decision":"complete","goal_status":"fulfilled","summary":"已按用户要求完成限定范围的分析报告。","completion_scope":"交付现有材料的证据审阅与未决项说明，不要求取得额外材料。","evidence_refs":["work:实际工作ID@实际result_revision"],"unresolved":[]}
```

证据引用仅接受本任务存在的 record:ID 或当前代次 work:ID@RESULT_REVISION。record 来自 analysis_session record 返回的 ID；已有文件证据可登记为 evidence，实验/结论按其真实类型登记。引用存在只证明来源可定位，不能代替阅读与判断。不得为过门写空证据或将自述升级 accepted。

用户只要求限定报告时，范围外研究项可以作为 unresolved 中 disposition=out_of_scope 保留，但必须说明 reason、完成范围和关联 work。范围内未解决的事项不能改标签冒充范围外。analysis_session 的 checkpoint.unresolved 仍表示未完成的实际任务目标；范围外后续研究写入处置或报告。

目标代次、结果修订、关键反馈证据、复核状态或任务目标/约束改变会使旧处置失效。签名过期时先重新读取状态，不盲目重试 resolve。重复相同请求幂等；更改处置需最新签名。暂停、取消、通知失败和宿主恢复均不自动获得执行授权。

## 关键失败结论复核

准备因“凭据未知/不存在路径/服务损坏”等判断放弃重要目标时，明确当前命题、输入/环境、可达材料覆盖、证据及尚不能排除的解释。只对影响大且证据薄弱的结论安排差异复核：尽量使用原始材料、不同实验或证据来源，允许复核者反驳初始解释。

零工具 Observer 可检查论证和交接缺口；文件核查或实验由具备最小必要工具的 Solver 执行。同模型一致、返回顺利、ack=applied 都不能单独证明结论正确。不要求所有目录全查、不规定固定尝试次数，也不为耗尽时间制造新路线。
