# 目标架构、依赖与工作覆盖地图（实验性 v1）

多组件、多目标、反复续做或多个分支需要对齐结构时，可用 `dsh_target_map`。简单任务无需建图；不以“补全地图”为由扫描所有入口。先绑定任务并打开记忆；`schema` 返回准确字段，`health` 返回可用性。

地图只保存分类及版本引用，事实仍在原记忆，目标代次和工作状态仍由原运行层维护。`observed` 表示记录的观察来源，**不是独立验证**；`inferred` 是解释；无证据为 `unknown`；修订、原件改变、目标换代为 `stale`；冲突另有 `conflict_present`。过期优先于冲突展示，不得用新标签覆盖过期依据。`reviewed`、工作 `adopted`、绿色节点均不能证明用户目标完成。

## 建图与修改

先通过原件读取、记忆 propose/review_publish 保存和复核真实依据。每个节点、连线均绑定同任务**当前已复核且适用**的记忆版本；不能把未核对的 Solver 摘要直接升级为已观察事实。任务级记录只能描述真正不依赖实例的资料；跨目标连线须写明方向、两个实例和两侧条件，并引用相应原件，不能把实例实验伪装成通用资料。创建地图项用 expected_revision=0；修改和删除携带当前项版本；端点另带地图端点版本。

```json
{"action":"put_node","task":"TASK_ID","options":{"key":"service:portal","expected_revision":0,"kind":"service","record_id":"mem-PORTAL","record_revision":2}}
```

节点种类：host、service、component、artifact、identity、goal、unknown。标题、代次、观察/推断、验证等级及条件摘要由原记忆读取，不另填一份真相。identity 只引用脱敏身份/凭据来源，不保存或广播密钥值。

```json
{"action":"put_edge","task":"TASK_ID","options":{"key":"portal:data","expected_revision":0,"kind":"reads_from","from":"service:portal","from_revision":1,"to":"service:data","to_revision":1,"record_id":"mem-RELATION","record_revision":2}}
```

连线种类：hosts、connects_to、reads_from、authenticates_to、depends_on、produces、unknown。连线自身需要原记忆依据，两个端点也必须有效。**类型和方向是主代理的分析标注，运行层不验证语义。** 配置文件提到数据库只说明配置引用；没有实际连通证据时，关系记录用 inferred，并保留配置范围、网络视角、身份及未知项。不要把同版本软件、相似名称或一次失败当成漏洞等价、连通或全局故障。无法确定关系可用 unknown，不强迫补图。

depends_on 仅用于 goal 节点：`A → B` 表示 **A 依赖 B**，连线依据说明缺少什么条件。依赖环可能来自假设或建模错误，需人工核对；运行层不调度地图，不把依赖环当作已证明不可行。

## 绑定工作并决策

```json
{"action":"bind_goal","task":"TASK_ID","options":{"key":"goal:access:work","expected_revision":0,"node":"goal:access","node_revision":1,"objective_ref":"portal:access"}}
```

goal 节点绑定稳定 objective_ref；coverage 读取当前编排代次中该目标的原始 work 状态，未派单显示 unassigned，目标代次改变显示 stale_scope。没有复制工作进度、租约或验收状态。绑定可早于 add；建图后仍需用 dsh_orchestration 的 route/add/followup 显式决策，同目标优先复用原 work。

在新结构证据、重要前提变化、关键阻塞或派发相关工作之前按需查看局部图，比较未知依赖、已有尝试、缺少的证据和当前 work，再选择下一项可区分解释的实验。无需每一步重写地图，无需固定次数侦察，不以题目分值作为通用优先级规则。重要决策仍把实际记忆引用登记到 set_premises；**地图项不是完成证据**，原完成守卫继续生效。

```json
{"action":"view","task":"TASK_ID","options":{"focus":["service:portal"],"radius":1,"limit":20,"max_bytes":8192}}
```

focus 最多 8 个节点，radius=0 或 1；未指定 focus 时分页看全索引。输出有 total、snapshot、next_offset；续页传 offset 和原 expected_snapshot，状态变化会拒绝混页，重新从 0 获取。每页默认 8 KiB，上限 32 KiB，最多 50 项；累计索引键不再设 512 的硬上限，已删除键保留历史。Native 工具接口会把实际页预算收窄至约 12 KiB；为保持快照一致性仍流式核对所选范围的证据，优先使用局部图。条件摘要有 complete 标记且始终 requires_original，决策前用 dsh_memory_read get 读取完整条件、未排除项及冲突组。地图更新只记录引用变化；不会执行扫描、唤醒模型或自动派单。

## 共享与恢复边界

首版是**主会话工具**，Solver 无全局地图读写能力。向 Solver 交付相关原记录时，使用现有 memory_plan 的显式记录白名单，原件另授予；需要布局摘要时可在 handoff 中提供局部报告，并保留依据引用和不确定性。中性复核仍从原件和中性问题出发，不自动塞入地图推断。未提供自动 Solver 子图接口，避免另开一条旁路绕过记忆授权和冲突组检查。

地图索引与历史在原 SQLite 中独立附加表保存，重启保留；删除为留痕移除，不删除原记忆。旧记录、端点被修订或移除，相关边与绑定自动过期，主代理复核后显式更新引用。地图不会延长目标租约、扩大授权、放宽额度、共享凭据或恢复执行。升级先备份并排空工作；回退代码可保留附加表，不把旧数据库覆盖到新任务状态上。

目标绑定的首屏工作摘要有 next_offset/total；更多工作用 `coverage options={key:绑定键,offset,limit,max_bytes,expected_snapshot}`，不再隐藏第 65 项以后的工作。覆盖状态同时报告绑定依据是否失效。长任务与完成审查见 [long-tasks.md](long-tasks.md)。
