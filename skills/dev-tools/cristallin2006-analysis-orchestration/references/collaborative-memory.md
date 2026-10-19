# 协作推理与受限记忆（0.7.0）

运行层核对版本、权限和实际交付；主代理判断结论和实验价值；skill 提供方法。观察、解释、假设、复核、采纳、外部接受分别保留，不能因为多位 Solver 同意就升级为事实。

## 重要前提与完成判断

主代理按需调用 `dsh_orchestration set_premises`，options 为 `{"expected_revision":0,"decision_premises":[{"record_id":"实际记录ID","revision":2}]}`。初始版本为 0；清空使用空数组及当前版本。仅登记会影响路线放弃、跨分支复用或总目标完成的重要判断，不为普通工具操作建立前提表。

登记时必须是本任务已复核、当前适用或明确争议中的真实修订。状态中 `decision_review` 提示需重新核对的数量；`decision` 分页返回完整依据和前提闭包，主代理当前上下文投影所用/当前修订及有效适用性。记录修订、撤销、争议、依赖、来源有效性、有效期和目标代次改变会使相关处置签名变化；无关记忆变化不会改变签名。任务完成入口与 JS 插件使用相同依据投影，不允许旧完成处置继续通行。

依据变化不是原命题为假的证明。不能删除模型历史中的旧解释，也不能自动撤销已执行的外部操作。重新核对后用当前签名 resolve，必要时更新/移除登记前提；暂停、取消、暂缓和限定交付范围的报告仍可使用。局部 500/连接失败不能未经论证扩大为整条路线不可行，也不能反向断言一定是操作错误。

## 显式预留 Solver 记忆能力

在首次 `add` 中提供可选 `memory_plan`，才会把 `dsh_solver_memory` 加入该 Solver 的原生工具白名单。可以提供空对象预留能力。没有预留的旧 child 不热扩工具、不强制重开，继续使用原有交接。Observer 始终零工具；不能直接在 tools 数组添加此工具。

```json
{
  "bindings": [{"record_id":"实际记录ID","revision":2,"use":"premise"}],
  "sources": [{"source_id":"实际src-ID","sha256":"实际SHA256","access":"full"}]
}
```

bindings.use 为 context/premise/challenge；挑战对象不是要求接受的结论。工作内 premise 标签不会自动登记总目标的 decision_premises，后者由主代理单独明确选择。记录授权不会自动授权来源、上游依赖或整个任务。

主代理调用 `memory_grant`，options 为 `{"work":"实际work-ID","expected_grant_revision":1,"memory_plan":{...}}`。传入完整替换计划，省略项即撤销。正常 add 后初始授权版本为 1，详细结果 memory_coverage 返回实际版本；初次授权未成功时可用版本 0 修复。撤销立即生效，新增在当前子会话下一原生步骤边界发布。相同内容的重试去重。授权更新不会唤醒空闲/暂停工作，也不会自动续做、创建新 child 或授予执行工具。memory_grant 修订不重写原始派单指纹，同 key 重试仍按最初任务书核对。

普通 dsh_memory_read/write 仍只允许主会话。新工具接受 status/query/get/read_source/changes，不接受 task、actor、owner、work、路径、URL、SQL 或写操作。身份来自当前原生血缘、宿主、任务代次、work、child、turn 与生命周期；主代理、兄弟 child、Observer、暂停、结束和未授权冷恢复均不能冒用。

status 索引默认最多 8 项，可用 offset/limit/max_bytes/snapshot 续页；index_truncated/next_offset 明确截断。query 只匹配已授记录，单页最多 20 条；get 必填 record_id/expected_revision，返回固定投影的 JSON 文本页，拼接 text 后解析，正文不是原件。read_source 必填 source_id/expected_hash；后续页携带 snapshot 与 offset。offset 是 Unicode 码点，默认响应预算 8KiB，max_bytes 最大 16KiB。原件只支持已登记 src-* UTF-8 快照；doc-* 明确不支持，不退回读取任意文件。范围授权使用 `access:"ranges",ranges:[[start,end]]`，以完整来源 SHA256 固定，码点范围左闭右开；read_source 可选 range_index，不能通过 locator 扩权。

query 不暴露未授权计数、标题或关系。冲突组/必要依赖缺少授权时 get 返回范围不足、query 省略该组；主代理应补足合法材料，不能把查无结果当作不存在历史。未经复核候选不共享；争议双方完整授权后保留 disputed 标记，不单独输出一侧为确定事实。

changes 使用 after_seq/limit/max_bytes 按升序读取当前授权范围的持久变化；只推进到实际返回的 next_seq，more 为真时继续。重复查询和心跳不制造相同变化。下一步骤的短索引仅提示授权与当前版本/适用性，不注入全部正文。原件来源变化同样记录，读取时重新校验，不依赖通知是否及时。

读取回执按 work、child、授权修订及记录/来源版本记录，合并实际返回范围；重复页不增加覆盖。review 的 memory_coverage 区分当前来源是否有效、历史快照是否读全与当前完整覆盖。索引/正文/brief 都不等于原件已读，读过也不等于理解。源快照登记沿用现有敏感识别，授权不是 DLP；主代理必须先脱敏复核，普通记忆不放凭据、访问 token 或 resume token。

## 第二角度工作

independent_branch/review 可选 contrast_plan，沿用 source_work/branch_reason，不强制每个目标双代理。包括 basis、具体 question、challenged_premise.statement、difference_axes、approach、discriminating_outcomes、required_sources。basis 至少提供真实的 source_result_revision / source_checkpoint_revision / source_assignment_fingerprint 之一；引用派单指纹可在首位 Solver 未返回时并行，不冒充其已作出的结论。required_sources 必须有对应明确来源授权，首次模型调用前不要求已读；返回 blocked/inconclusive 是合理结果。

mode=informed 提供常规交接；mode=independent 使用调用者专门撰写的中性问题、方法与区分结果，宿主不复制原 work 的问题、成功标准、被挑战 statement、依赖报告、checkpoint 或结论记忆。独立模式拒绝 handoff、depends_on、记忆 bindings 和 Observer；仅授原件，保留记录的用户目标/约束、工具、专业 skill。调用者仍须确保 question/approach/discriminating_outcomes、key、技能选择本身没有夹带第一位 Solver 的结论；运行层不能证明自然语言真正中性或心理独立。原件中的观点不篡改。

独立模式不接受技术 steer 或自由文本 followup，以免在中途泄入待复核结论；可请求中性 checkpoint、查看结果、取消或复核。补足原件后可用 followup options={work,neutral:true} 续做同一 child；不携带 message/skill_plan，由宿主生成中性续做说明，保留原问题与方法。若需要引入第一位 Solver 结论进行知情指导，先复核结果，再明确建立 informed review 分支，不伪装为继续盲检。普通工作仍优先复用同 child followup。原 work 的 basis 更新仅标记 basis_current=false，不自动取消第二角度工作。

progress 可选 premise_relation=supports/challenges/inconclusive/not_applicable，保留原 supported/not_supported/inconclusive/blocked。支持原解释可以正常采纳，不能要求为了成功制造反证；adopted 不等于 tested/accepted。主代理决定 revise/link/invalidate，Solver 无共享记忆写权限。

## 生命周期与兼容

Broker 由 analysis-memory 使用已核对的 Cordis provide/get 提供内部窄接口；不导出数据库或父工具，不伪造父 actor。服务卸载时先拒绝并收尾读取、撤销服务，再关闭库。服务不可用时明确提示，不用父代理权限或临时数据库兜底；仍可分析已合法交付的原件并安全收尾。

暂停/结束使当前执行授权失活；同 child 明确续做时重新核对；重启/recover 只恢复元数据，不自动激活或重放动作。新元数据仍在同一 state.sqlite3 的 mem_solver_* 表，组件版本 1，候选 schema 0.2 不变。0.6.1 必需 skill/参考卡完整交付和其他 skill 可发现性保持。

验收仅采用虚构文件、隔离数据库和确定性本地适配器，不调用真实模型或访问真实目标。机制验收不证明提分、推理质量或不同角度必然更有效。
