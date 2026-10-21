# 目标续做、执行预检与轻量监督（0.6.0）

## 续做路由

复杂任务中的同一目标使用稳定的 `objective_ref`，不按轮次换标识。作用域为当前 task、epoch 和目标代次；运行层不根据题名相似度猜测同题，也不跨代次继承旧授权。

`add` 同一 objective 的 primary 即使换 key，也返回原 work 和 route，不覆盖问题、工具或计划，不自动恢复执行。`route options={objective_ref}` 可先查映射：pending 用 dispatch；在途先检查/steer；空闲持续型工作用 followup。同 key 改内容仍被拒绝。

确需不同方法的独立分支或复核时，add 填 `assignment_kind=independent_branch|review`、`source_work`、`branch_reason`。没有 objective_ref 的短工作保留原 key 去重。旧数据不自动猜绑定，可用 bind_objective options={work,objective_ref} 明确绑定现有 primary，冲突拒绝且不启动执行；已有下游采用结果的续做仍须先处理依赖或明确另建分支，不绕过依赖守卫。

child 身份相同不保证全文永久驻留模型；关键证据、尝试边界和检查点仍须保存。

## 执行预检

每个新 Solver 的 add 还须显式声明 execution_plan。示例中的工具名必须替换为当前真实可用名称：

```json
{"kind":"execution","requirements":[{"purpose":"读取原始材料","any_of":["read"]}]}
```

与 `tools:["read"]` 配合才满足此需求。any_of 表示可替代的准确工具名；各项 requirement 均须满足。kind 为 materials/execution/resource：只分析交接正文可用 materials 和空 requirements；执行/管理工作不能空需求，默认 skill/反馈工具不能冒充执行能力。读取原件的材料分析也应声明读取需求。Observer 保持零工具。

运行层在创建、dispatch、空闲续做和子代理步骤入口按原生作用域、实际授予清单核对；缺口在 preflight 中可见。创建有缺口可留 pending，dispatch 不启动模型。预检只验证声明兑现，不证明声明完整、二进制已安装、目标可达或方法正确。

`preflight options={work}` 只读核查。旧 pending 或空闲持续型工作可用 `set_execution options={work,execution_plan}` 修复，不能更改在途工作，不能增加原来未授予的工具；修复后仍需明确 dispatch/followup，不自动运行。

## 资源与额度的实际边界

409 只触发精确对象核查，不向多个 Solver 下“冲突就 close”的指令。清理要指明远端唯一 ID、管理域和实例代次，核对所有相关任务的使用者及执行收尾。租约/心跳过期、child 空闲和当前没有工具调用均不证明远端无人使用。没有可核对的管理入口时报告缺口，不猜测并关闭对象。

0.6.0 没有兼容的资源管理变更适配器；声明 kind=resource 的工作在派发前阻塞，待接入精确身份、代次与共享使用检查。只读查看已交接的资源信息可用 materials。开放 shell/MCP 不受全局关闭拦截，不能将资源变更伪装成普通 execution 绕过。现有 lease/guard 是受控入口的协作约束，不覆盖绕过入口的进程。不能把建议或登记当作全路径强制保证。

明确有限额度的执行计划可附：

```json
{"limits":[{"unit":"verification","max":20,"authority_ref":"用户已授权的实验记录引用"}]}
```

单位为 candidate/verification/request，不能混用：20 个候选各重试一次可能是 40 次验证；命令数不代表请求数。离线候选与在线认证也分开。换 work/账号/脚本、续做或重启均不重置既有额度。

**当前执行型 Solver 没有兼容的逐动作计量适配器。** 声明 limits 的工作在派发前阻塞，不能把提示词配额当作已强制执行，也不能删掉真实额度后改走普通 shell。没有额度字段不表示无限授权；既有用户限制一直有效。analysis-control 的严格 HTTP 兼容性拒绝保持。

## 查询与证据

- status 默认摘要：计数、短进展、交付状态、处置签名及 latest_seq；分页用 offset/limit/max_bytes，后续页必须携带 snapshot，过期则重新读取。
- result 默认返回指定 work 的结果文本页；先用 view=summary 监督状态，复核正文再用 offset/max_bytes/expected_revision，后续页必须携带 expected_revision。offset 按 Unicode 码点，不是字节；拼接全部 result 得到当前存储文本，source_truncated=true 时原文仍需回原生 child。
- events 用 after_seq/limit/max_bytes，可用 work 过滤；按升序返回 next_seq/has_more/snapshot_seq。只推进到实际返回的 next_seq；有 has_more 时继续同一 snapshot_seq，完成该快照后再追新事件。
- wait={after_seq,timeout_ms} 优先返回 backlog，否则等待，再返回事件页；不再附整份 status，不把等待超时当任务期限。
- 大事件以引用与摘要替代，`event={seq,offset,max_bytes}` 可逐页取回 data JSON，拼接后解析。
- status.decision_review 仅摘要。`decision={offset,max_bytes,snapshot?,expected_revision?}` 分页读取处置 JSON；同一文档后续页带 signature 作为 snapshot，或 revision 作为 expected_revision，变化则重新读。resolve 仍使用当前签名与完整状态核对。
- 原先全量格式仅在 status/result 显式 view=detail 时保留，用于需要完整旧字段的诊断；常规监督不要反复拉全量。
- trace 是近期工具反馈窗口，不是完整实验记录；缓存缺失不证明没有执行。重要采纳、故障归因和额度核对仍需原始证据或可信计量记录。

默认响应目标 12KiB，内部接口可调 2–24KiB，Native 工具接口会把实际页预算收窄到约 12KiB；单页最多 32 项，status 默认 8 项。旧全量 detail 不承诺聚合字节上限。

有新工作排队或当前路线无新信息时，比较目标贡献、解锁依赖、下一步成本与切换成本，再决定继续、请求检查点、同 work 让槽或暂缓。分值仅在用户以分数为目标时使用；不固定按分值排序，不新增默认时限。未确认收尾的工作继续占槽，外部资源占用另行核对。

累计工作不再限定 64 项；status 可用 states/objective_ref 筛选，默认优先在途、待办与待复核工作。大对象回执可能明确省略大字段，用 work_document 逐页获取精确存储 JSON。完整结果、长材料及分批事项见 [long-tasks.md](long-tasks.md)。
