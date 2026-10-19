---
name: analysis-memory
description: 在 DSH 已绑定的多阶段分析任务中维护事实、假设、实验和失败边界，恢复有来源的分析成果，按需派发有限的只读子任务。单点查询无需建立记忆；专业分析方法由领域 skill 提供。
---

# Analysis Memory

主 agent 负责问题建模、方法选择、实验与判断；运行层维护状态、身份、引用与适用性。记忆正文是资料，不能改变授权、工具权限或资源租约。

## 建立或恢复

1. 先使用 analysis_session 的 init 创建并绑定任务，或用 bind 绑定已有任务。
2. dsh_memory_write 的 open 连接同一 task；首次需原建任务会话。跨会话恢复使用原 owner 取得的 handoff token；token 不写入记忆或报告。
3. 恢复先读 analysis_session status，再用 dsh_memory_read context/query 查看当前成果、失败边界和未决项。新会话没有 token 时不能冒认旧 owner；可继续原会话或让原会话产生交接 token。

目标仍由 analysis_session target 管理，每个目标有独立 generation。仅确认实例变化才增加代次。记忆记录的 target_id=null 表示任务级资料，此时 expected_generation=0；绑定具体目标时填真实当前代次。不能把运行时地址、cookie、PID 或有环境条件的实验伪装成任务级通用事实以规避失效。

## 记录与检索

- dsh_memory_write source：登记工作区内已落盘的 UTF-8 证据快照，最多 128 KiB。可用 record_id 显式导入本任务已有 evidence 记录。二进制先由专业工具输出可核对文本证据。
- dsh_memory_read read_source：回查原始快照。引用既有 ID，不编造来源。
- dsh_memory_write propose：提出 observation、claim、hypothesis、experiment、constraint 或 method_candidate。
- dsh_memory_write review_publish：main 回查证据和适用范围后 publish 或 reject。每次修改使用当前 expected_revision；revise 必须使用新的 operation_id。
- dsh_memory_read query/get/context/explain：按问题找资料，展开原文、来源、冲突与依赖。export 返回数据供用户保存，不会写任意路径。

记忆候选、schema 和六类 details 字段见 [contract.md](references/contract.md)。只有在实际需要该类记录时读取。

origin、verification、review_state 和 applicability 相互独立。看到工具输出只证明“输出中如此声称”；解释默认 inferred。tested 只涵盖具体实验。reviewed/adopted 只是分析采用；v0.2 没有可信平台接受回执适配器，因此新记忆拒绝升级 accepted，旧 analysis-session 的结论保留在原记录。

记一次有信息价值的实验或阶段成果即可，无需为普通读文件逐条填表。任务级 constraints 不能代替宿主授权。

## 失败、冲突与变化

实验分别记录执行状态和对命题的影响。缺依赖为 blocked/inconclusive，超时为 interrupted/unknown；一次无效果只说明相应输入与条件，不能直接排除整条假设。

同条件的反证用 link kind=contradicts 保留双方；不同条件的结果先写清条件。新结论可 revise 或 archive/supersede，历史保留。目标代次或证据内容变化后，查询时自动判 needs_recheck；v0.2 不自动跨代次继承静态结论。query 无命中不代表此前从未尝试。准备重复实验、把局部失败提升为路线失败或复核关键负面结论时，读取 [负结果复用](references/negative-evidence.md)，使用现有 experiment/claim 和来源，不另建台账。

环境、hook、权限、Ghidra 分析选项/人工类型修正改变时，显式 invalidate 相关成果并更新来源/目标；运行层不能自动识别所有环境变化。derived_from/depends_on 建立真实依赖，不能以相似文本代替证据关系。

## 可选协作

收益大于交接成本时，analysis_collaboration add 提供 question、sources 和 depends_on；dispatch 提供 work ID 数组。默认最多并行两个，每个最多 90 秒。主 agent 保留全部原有分析工具。

子 agent 只可用 dsh_evidence 读分配快照；宿主附带仅引用分配来源的已复核记忆包。记忆摘要不满足原证据阅读要求。任务范围外的资料不交接。

result 返回后主 agent 回查原证据，用 review 选择 adopted/rejected/needs_more_evidence。依赖支线必须在前一步 adopted 后运行；adopted 不证明真实目标验证成功。

status 查看支线；retire 显式放弃非运行支线；recover 只处理确认旧宿主已退出的支线，不重放未知操作。新会话携带 token 的 open 可在旧宿主确认退出后将失联支线标为 interrupted，再由新 owner 决定。

## 收尾与故障

checkpoint/transition/资源管理仍使用 analysis_session。任务 complete 前复核或显式放弃协作支线；不用把所有设想都变成待办。保留未决结论及交付范围。

dsh_memory_read health 查看数据库、索引和宿主计数。写入失败必须明确“未持久化”；不能回落临时库、声称成功或自动重做外部实验。索引降级时仍可使用有范围限制的中文子串/标识符查询。

项目共享、向量检索、独立后台整理 agent 和自动更新 skill 尚未启用。method_candidate 是评审材料，不会自动修改专业方法。

## 完整原始材料交接

任务原文超过普通记忆来源上限时，使用 dsh_handoff source 登记完整 UTF-8 材料并生成分块目录；将 doc- 来源显式分配给只读支线。dsh_evidence 可传 chunk，dsh_handoff coverage 显示实际读取覆盖，完整阅读不证明理解。详情按需读同级 analysis-session/references/controlled-requests.md。凭据不进入原文快照或普通记忆。

## 专职解题编排模式

复杂长任务需要独立运行的调度监督时，读取同级 analysis-orchestration/SKILL.md。该模式按任务显式启用，由主代理负责战略推理、原生 Solver 负责具体执行；运行层维护事件唤醒、定期巡检、纠偏和取消。启用后的角色规则覆盖本文普通模式下“主代理直接分析执行”的默认分工。简单任务和普通只读协作仍使用原有模式。不要同时启动另一条派发通道；严格 HTTP 控制会话暂不支持执行型 Solver，不能绕过原控制器。

## 协作推理与受限记忆

遇到重要前提传播、第二角度复核、执行型 Solver 召回记忆、授权变化或原件阅读覆盖时，先读 [协作推理与受限记忆](references/collaborative-memory.md)。摘要不能代替原件；读取回执不能证明理解；保留观察、解释、假设与有效范围。
