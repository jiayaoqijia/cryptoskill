---
name: analysis-orchestration
description: 为复杂、多阶段、有独立执行分支的分析任务启用专职战略编排与持续型 Solver；支持同一子会话续做、事件监督、证据复核和取消。简单查询及短串行任务无需启用。
---

# 解题编排

主代理理解目标、比较证据、安排资源、复核并综合结果；具体分析与执行委派给原生持续型 Solver，专业方法由 skill 提供。启用后主代理保留本地阅读、状态与记忆工具，具体执行和其他派发渠道受运行层限制。普通任务不必强行拆分。

## 启用与派发

先 analysis_session init/bind 建立唯一任务，再 dsh_memory_write action=open，随后调用 dsh_orchestration：

```json
{"action":"enable","task":"TASK_ID","options":{"max_parallel":2}}
```

默认 task_ms、timeout_ms、max_steps、max_wakeups 均为 null：不按任务时长、工作时长、累计步骤或提醒次数自动停止。不要自行增加“十分钟内解完”等要求；仅用户明确需要有限预算时传相应字段。插件不再固定 maxTokens=4096，模型自身的上下文、生成限制和单次工具超时仍存在。用户取消、权限变化和资源租约继续生效。

严格 HTTP 控制目前尚不支持执行型 Solver，enable 会拒绝；不能关闭控制或换会话绕过。持续型生命周期也没有使普通 shell 等路径自动获得全局网络预算保护。

```json
{"action":"add","task":"TASK_ID","options":{"key":"compare","question":"静态核对指定样本的两个解释，说明原文、假设、证据位置及失败边界。","success":"给出有根据的支持、否定、不确定或阻塞结果。","tools":["read"],"objective_ref":"sample:semantic-check","execution_plan":{"kind":"execution","requirements":[{"purpose":"读取样本原始材料","any_of":["read"]}]},"skill_plan":{"required":[{"name":"ghidra-static","reason":"本分支需要核对二进制语义与静态证据"}]}}}
```

新 Solver 同时声明 execution_plan，明确材料分析或执行工作及最小能力；缺所需工具不启动。复杂目标用稳定 objective_ref 路由到原 work，另开分支需明确来源与原因；字段、旧工作修复、资源/额度边界和分页查询见 [可靠工作与轻量监督](references/reliable-work.md)。

工具名须与当前会话一致。Solver 默认拥有 skill 与 dsh_solver_feedback，其他工具创建时明确授予；effective_tools 展示实际清单。加载知识不扩展权限。Observer 零工具。子代理不继承主代理完整对话或已加载技能正文，原文需交接可读位置。

每个新 Solver 的 add 须声明 skill_plan：选择与问题相关的必要 skill，或用 required=[]、none_reason 明确说明简单任务不需要专业方法。运行层按子代理原生作用域装载必要正文，并自动合并该 skill 的 skill-materials.json 中声明的必需完整参考卡；brief 摘要和 references=[] 不能替代或关闭这些原文。专业方法已写进 brief 不能作为 none_reason 的理由。status 的 skill_materials 数量和 result view=detail 的 skill_delivery 路径/摘要记录实际交付；不能以“我读过”代替。其他 skill 目录与工具保持可用，深入资料仍按需读取。字段、受限技能、参考卡、旧工作与续做处理见 [技能材料交付](references/skill-delivery.md)。

自动携带绑定任务的目标、约束和目标必要入口；可选 handoff 补输入引用、待核对结论、假设、失败边界与职责。区分用户限制和编排选择的阶段安排，注明来源和生效条件；初始只给 A 不等于用户永久禁止 B。指导只在原授权内补材料、澄清阶段，不让 Solver 猜测禁止事项已解除。详细契约见 [supervision.md](references/supervision.md)。

```json
{"action":"dispatch","task":"TASK_ID","options":{"work":["WORK_ID"]}}
```

立即返回实际启动或拒绝情况。默认任务并发 2，宿主最多 3，只有在途工作占执行槽位；累计工作数不设固定硬上限，历史通过摘要和分页读取。依赖先 review=adopted，不自动生成新方向。

## 长任务与完整材料

大量分支、长任务书、大文件引用、长结果或分批未决事项的处理见 [长任务与完整材料](references/long-tasks.md)。单页大小限制只控制传输；长说明保存全文并要求必要范围完整读取，关键约束与必需技能不静默裁剪。原文件按明确授权的工具读取，历史工作不为清额度而另开任务。

## 持续型子代理

Solver 在关键证据变化、阻塞和返回前用 progress 保存报告，再返回简短结果。缺材料时可以报告后空闲，不必循环调用模型保持存活，await_guidance 仅为可选有限等待。空闲实例可能释放，原生子会话和身份保留，后续消息可恢复同一上下文。

- status 默认轻量分页摘要，result options={work,view:"summary"} 查看单 work 状态；复核正文使用默认结果分页并携带 expected_revision。完整旧字段仅在显式 view=detail 时返回。
- events/wait 使用 after_seq 返回升序增量页；有 has_more 时继续同一 snapshot_seq。wait options={after_seq,timeout_ms:60000} 先返回积压事件，否则等待；不附整份 status，不把 wait 超时当成解题期限。
- decision 分页读取当前处置详情；event 按 seq 分页取回大事件。响应截断/分页与 trace 窗口均不等于完整证据。
- trace options={work} 按需查看近期实际工具反馈的有界预览与原生引用；仅尽力脱敏，不能代替完整证据。
- request_checkpoint options={work,reason} 请求保存进展，不强制改线。
- steer options={work,guidance:{observation,hypothesis,experiment,reconsider_if,evidence_refs}} 有据纠偏。运行中在可用步骤接收，返回后的工作也可继续。queued/seen 与 understood/applied/evaluated/disagreed/blocked 分开，回执不证明建议正确。

追加材料或继续未解决工作：

```json
{"action":"followup","task":"TASK_ID","options":{"work":"WORK_ID","message":"补充材料 B，请核对原假设并说明哪些结论应修订；原用户约束继续有效。"}}
```

同一目标先查 route 或复用原 work，避免换 key 丢上下文。重要排队或阻塞变化时比较边际收益、解锁依赖和切换成本，不强制按分数抢占。

同一工作续做保持 child ID、自身历史及工具边界，投递确认不是答案。续做清除旧采纳，新结果产生 result_revision 后重新复核。已有未取消依赖时，先退休依赖或创建新工作，避免静默修改已使用的输入。旧版一次性子会话不能伪装成持续型，应新建工作并交接证据。

无近期工具反馈、重复输入和经过较久只是复查线索；区分推理、在途工具、等待和空闲。不以耗时强迫换线。空闲工作不触发周期心跳，真实事件仍通知编排。

## 复核与结束

```json
{"action":"review","task":"TASK_ID","options":{"work":"WORK_ID","decision":"adopted","reason":"已核对原证据与适用范围，说明未验证部分。"}}
```

decision 也可为 rejected / needs_more_evidence。adopted 不等于 tested/accepted，不自动发布记忆；重要结论由主代理复核后写入原记忆。关键失败结论说明实际排除的命题、条件、原始证据和不排除范围；影响放弃整条路线而证据薄弱时，考虑不同材料或方法的复核。需要检查遗漏文件/运行实验时派具备必要工具的 Solver，零工具 Observer 仅审查所交接材料。可选 role=observer, observe_work=WORK_ID, tools=[] 审查所交接材料，不能假装独立访问了目标。

cancel options={work,reason} 停止指定工作并确认原生收尾；已返回工作也可明确取消。pause 取消在途执行，已返回结果保留；resume 仅在用户仍希望继续且原作用域有效时使用，不自动重放，需要续做时明确 followup。主回合取消、父会话退出、插件卸载、目标切换均要求收尾；cleanup_unknown 不算已停止。

pending/returned 工作先取消或复核，再 finish options={reason}，释放本任务保留的子代理。finish 只结束本编排阶段，不证明用户目标完成，也不阻止取消或合理止损。

全部工作空闲后，查看 status.decision_review 的摘要，必要时用 decision 分页核对完整处置；按当前签名 resolve 记录继续、等待、阻塞、暂缓或完成；这项记录不启动工作。准备结束总任务时，先读取 [目标处置与完成](references/resolution.md)：已有编排的任务须有最新 complete 处置、实际交付范围和证据，再 finish/disable 后调用 analysis_session complete。needs_more_evidence 分支仍须列明处置。无时限任务保持默认无时限，不为保持运行而制造新方向。已关闭或暂停的子代理不能通过原生消息接口绕开编排守卫。

recover 仅在原宿主身份已消失后恢复元数据，不重放、不证明外部资源已清理；核对后明确 resume/followup。共享项目仍需租约和 guard；脱离生命周期的后台进程和递归派发不开放。实现边界见 [design.md](references/design.md)。

## 协作推理与受限记忆

多组件、多目标或多个分支需要对齐结构时，可按需使用 [目标架构、依赖与工作覆盖地图](references/target-map.md)。地图只索引已复核记忆及真实工作状态；保留未知关系、条件、冲突和失效，不自动证明连通、授权或完成。关键证据或阻塞变化后按需查看局部图，再决定派单；简单任务无需建图。

遇到重要前提传播、第二角度复核、执行型 Solver 召回记忆、授权变化或原件阅读覆盖时，先读 [协作推理与受限记忆](references/collaborative-memory.md)。摘要不能代替原件；读取回执不能证明理解；保留观察、解释、假设与有效范围。
