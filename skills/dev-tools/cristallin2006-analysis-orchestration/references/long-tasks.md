# 长任务、完整材料与分页（0.8）

多轮续做、大量分支、长任务书、长结果或地图持续增长时阅读本说明。普通短任务维持原接口，无需另建任务或手动分片。

## 累计容量与历史

当前运行层不再以累计 64 项 work 或 512 个地图键阻止新增；删除的地图键也不会耗尽一份固定额度。已完成工作、原子会话身份、目标绑定、证据与地图历史保留。没有新增默认任务时限、推理步数或累计材料字数上限；磁盘容量、模型上下文、原生单次工具限制依然适用。

status 默认有界摘要，优先列出在途工作、pending 和待复核工作；历史工作在后续页。可用 `states` 筛选状态或 `objective_ref` 筛选目标，counts 仍统计全代次状态，total 是筛选结果数。同目标仍先 route/followup，不能为了清额度另开主工作、重置目标或丢掉旧上下文。

```json
{"action":"status","task":"TASK_ID","options":{"states":["running","returned","needs_more_evidence"],"limit":8}}
```

常规查询在 SQLite 按页取正文，心跳只读取在途工作。完成依据以全部工作元数据的版本摘要核对；工作、复核、结果版本、重要反馈、目标或约束变化仍会使旧判断失效。摘要不是正确性证明，也没有排除历史分支的权限。

地图 view 也按页提取局部图；为保证一致性仍需流式核对所选范围的证据，查询成本随范围增长。优先 focus 到相关节点，避免每轮遍历全图。goal 绑定的工作摘要最多显示一小页，更多工作使用 `dsh_target_map action=coverage`，不再隐藏第 65 项以后的工作：

```json
{"action":"coverage","task":"TASK_ID","options":{"key":"GOAL_BINDING_KEY","offset":0,"limit":8}}
```

## 长任务说明的交付

长 question、记录目标、非关键约束部分的 handoff、目标上下文与长 followup 自动保存为不可变的全文材料包；初始消息携带哈希和读取入口。用户关键约束在交接和续做时完整附带，超过可容纳边界时明确拒绝，不能删减、藏进摘要或要求 Solver 猜测。

Solver 用已有默认工具读取自己工作获授的材料，无需另授 shell 或全局记忆权限：

```json
{"action":"read_material","packet_id":"packet-...","expected_hash":"SHA256","offset":0,"max_bytes":8192}
```

这是 `dsh_solver_feedback` 的参数，**不传 task/work/owner/path**。正文在 `result`；按 next_offset 续读，携带 snapshot，offset 是 Unicode 码点。`read_coverage.full` 表示该材料文本范围已读完，`all_required_read` 表示本次所有必要任务材料已读完；均不证明理解或内容持续驻留在压缩后的模型上下文。

必要说明未读完时，运行层仅允许材料读取、上下文及 working/blocked 反馈；执行工具和成功结论被拒绝。直接结束会标记交付失败，仍可同子会话 followup 补读。不得以“已经看到 brief”为由绕过全文读取。需要重查历史续做原文时，`dsh_solver_feedback action=materials` 分页列出本工作过去交付的材料；read_material 继续按原哈希读取。其他工作、Observer、暂停或结束的 Solver 不能借此取得材料。

必要 skill 与强制参考卡继续通过原宿主全文装载和可见性检查；64 KiB 的必需知识块超限仍明确阻止启动，不用摘要替换。大任务书的分页机制不绕过专业知识交付规则。零工具 Observer 无法自行翻页；超大审查输入会明确失败，应交接与问题相关的原件范围，或使用具有明确只读工具的 Solver。

## 大文件与授权

大文件保留原文件，通过 handoff.inputs 交接明确路径/产物引用、用途、必要时的哈希与范围，并在 execution_plan 中声明真实读取/分析工具。执行型 Solver 使用已有授权工具按范围读取或在本地分析；不要为交接而把二进制、数据集或整份源码塞进 question。

普通记忆来源 128 KiB、dsh_handoff 的 2 MiB 上限是相应证据快照/只读协作通道的边界，**不是所有任务文件的大小上限**。大文件不要求导入这些快照通道。任务材料包只保存交接文本，不因路径字符串自动打开文件，也不扩大文件、网络、资源或凭据权限。原生工具自身可能分页或截断，必须检查实际结果与读取范围；索引、摘要和哈希不能代替需要核对的正文，也不强迫不相关的全文件扫描。

## 主代理的全文入口与完整结果

原生工具宿主也会限制超大工具输出。因此 add/review/result detail 等过大回执返回明确标注的有界摘要，而不是回传一整份巨大 JSON。`large_fields_omitted=true` 时用 work_document 读取精确存储数据：

```json
{"action":"work_document","task":"TASK_ID","options":{"work":"WORK_ID","offset":0,"max_bytes":8192}}
```

拼接每页 result 后解析 JSON；后续页带 snapshot。工作变化会拒绝混页。该文档中 result_external=true 时，result 字段是有明确标记的预览，完整结果通过原 `result` action 逐页读取，携带 expected_revision。

新 Solver 返回的**实际接收文本**完整保存为结果版本，不再因超过 32,768 字符丢掉尾部；数据库行只保留有标记的预览，完整副本按版本和哈希校验。模型自身生成上限、原生工具之前就截断的输出，无法由本层补出。旧版本已截断的存储副本也不会自动恢复，应回到原生子会话核对，不能清除旧 source_truncated 标记冒充完整。

Native 工具接口将页预算收窄到最多约 12 KiB，材料读取默认 8 KiB；响应可以比请求的 max_bytes 更小。只要 next_offset 非 null 就还有后续，不能把当前页结束当成原文结束。页数没有累计配额。

## 分批登记未决事项

少量未决事项仍用 resolve.resolution.unresolved（单次最多 32 条）。更多事项分批登记到独立集合，每批最多 32 个键且约 24 KiB；这是传输边界，集合累计数量不设硬上限：

```json
{"action":"issues","task":"TASK_ID","options":{"expected_signature":"CURRENT_SIGNATURE","expected_revision":0,"upsert":[{"key":"branch-a","work":"WORK_ID","issue":"仍缺少哪份证据","disposition":"continue","reason":"为什么需要继续","next_step":"下一项有区分力的核对"}]}}
```

返回 issue_set_revision 和新的 signature。下一批带当前 signature 与集合版本；remove 显式删除指定键。只读 issues 可分页查看当前集合；已冻结集合用 issue_set_id 查看。任务依据变化后，旧集合不自动套到新判断上，须复核后重新登记。

最终 resolve 增加 `resolution.issue_set_revision`，可与少量 inline unresolved 合用。运行层核对全部事项，冻结不可变集合及哈希，JS/Python 完成守卫读取同一份数据。每个 needs_more_evidence 工作仍须有明确处置；存在任何范围内未决事项时不能 complete。登记为 out_of_scope 必须有真实范围依据，不能为了通过检查批量标成范围外。issues 不派发任务、不授予权限、不证明目标完成。

升级采用附加表和索引，不清历史、不自动恢复执行；部署前备份并确认收尾。回退代码可保留附加表，但含新式全文结果或事项集合的任务不能交给不识别该格式的旧完成守卫。
