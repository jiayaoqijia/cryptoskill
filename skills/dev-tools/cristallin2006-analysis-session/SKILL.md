---
name: analysis-session
description: 管理多阶段、多目标、需要中断恢复或协作的分析任务：任务身份、目标代次、关键证据、检查点、共享资源与交接。简单单点查询无需建立完整任务；专业分析方法由对应 skill 提供。
---

# Analysis Session

模型负责当前问题、假设、方法选择和下一步实验；运行库负责原子状态、事件关联与明确资源条件。默认一个主代理，能分离且收益大于交接成本时再委派，尊重用户顺序和资源约束。

## 受限会话的原生入口

优先使用 `analysis_session` 工具。`action=init` 配合 `options={"goal":"用户目标","data":{}}` 建任务并自动绑定当前会话；随后传 `task=任务ID` 调用 status、checkpoint、transition、target、record、lease 等。参数与旧 CLI 一一对应，结构化内容放 options.data，CLI 的 --file 不用于此入口。

不明参数用 `action=schema, options={"action":"checkpoint"}` 查询该动作的字段、必填项与例子；错误反馈也返回当前动作契约，不要反复猜参数。`checkpoint` 使用 `options={data:{summary,...}}`；`transition` 使用 `options={status:"complete",data:{summary:"完成情况",unresolved:[]}}`。init/bind/status/target 返回 readiness：实际绑定、目标代次、后台任务覆盖与 HTTP 策略状态。组件已加载不代表任务已创建，也不代表请求预算已生效。

`action=health` 返回 SQLite 实际完整性、已落库事件数和当前 host 的 hook 成功/失败计数。工具 decision=pass 只表示动作没有被阻断，不代表记录成功。hook 返回非阻断错误码 1 时，独立会话卡/建议与故障提示仍会注入；宿主健康文件同时保留生命周期点的结果。

原生入口与钩子仅获专用 analysis-state 目录的写能力，普通 shell、会话权限和审批不变。不能经该工具执行 guard/discover 的外部命令、选择解释器或更改沙箱；证据文件须位于当前工作区。

CLI 保留给自身已有目录写权限的维护/运行场景；受限会话不要反复裸调用 CLI 写 DSH_HOME，也不要回落临时库造成状态分叉。

## 创建与恢复

通用入口为 `${DSH_HOME:-$HOME/.dsh}/runtime/analysis-v1/session.py`，Python 标准库即可运行。

```bash
AS="${DSH_HOME:-$HOME/.dsh}/runtime/analysis-v1/session.py"
python3 "$AS" init --goal "当前用户目标" --session "会话卡中的 session_id"
python3 "$AS" status TASK_ID
python3 "$AS" target TASK_ID --id service --data '{"endpoint":"当前地址","fingerprint":"实例特征"}'
python3 "$AS" artifact TASK_ID --path ./sample
```

`target` 每次建立新代次；只在确认实例变化时调用。地址相同不能证明实例相同，地址变化也不自动证明实例变化。新代次保留历史，但 cookie、PID、运行时地址、实验结果需复核。相同文件哈希的静态发现可复用并说明范围。

恢复先读检查点、未决假设、目标代次与资源状态，再选择最有价值的实验。无需固定先清除某一假设。`bind TASK_ID --session ID` 显式绑定当前会话；工具事件只归属已绑定任务。

## 关键证据与结论

`record TASK_ID --kind experiment|evidence|claim|hypothesis|handoff|note --file UTF8_JSON` 批量记录一次实验的关键信息；无需为普通读文件逐条手填。证据需要真实文件路径，登记时保存 SHA-256。工具调用自动记录 ID、摘要哈希和耗时；桥接层不提供的退出状态保持 unknown，原始详情仍在 DSH 会话日志中。

结论字段相互独立：`origin=observed|inferred`，`verification=untested|tested|accepted`，`accept_scope`，`unresolved`。测试只支持具体命题，接受只支持对应程序/平台和实例。当前尚无可信平台接受回执适配器，新建 accepted 会拒绝；原有历史记录保留。字段检查不证明专业判断正确。

```json
{"text":"结论及范围","origin":"observed","verification":"tested","target":"service","generation":1,"evidence":["证据记录ID"],"unresolved":["未确认的适用条件"]}
```

同源模型往返测试有局部价值；与实际目标、不同输入及不同错误来源对照能增强证据。打桩或 hook 改变环境，要记录干预；缺少独立来源不阻止交付事实或明确限定的假设。

## 检查点、预算与收尾

`checkpoint TASK_ID --file checkpoint.json` 保存 summary、unresolved、next_experiment、resource_plan。状态为 running/waiting/paused/blocked/complete/cancelled；`transition TASK_ID --status paused --file checkpoint.json` 是显式转换。工具调用结束或回合结束不自动完成任务。尚未达到用户目标时保留未完成状态；报告可以先交付。

用户明确的请求、时间或并发上限为硬约束；自行估计的软预算用于复查。资源容量按实际环境决定，不设跨任务通用并发值。暂停/取消/结束时列明保留、终止、移交的资源和责任方，运行库不会擅自杀旧进程。

遇到连续无新增证据、模型反复修补或大量工具修复，盘点最不确定前提、可区分解释的实验、尚未利用的发现。可以继续原路线，说明新实验能增加什么信息。

## 共享资源与受控变更

`resource TASK_ID --id ID --data JSON` 登记后台任务或项目；Linux PID 同时绑定启动时刻和 boot ID，防止 PID 复用。`status` 检查进程身份；登记的活跃 PID 已失效时标记 inactive、结果待核对，不继续占用活跃资源预算，也不自动杀进程或宣布任务成功。

本机实测：DSH host 重载可停止关联的后台进程；不能只靠 detach 假定 daemon 会保留。维护前保存准确的 PID/启动身份、项目路径、加载程序与启动环境清单，结束活动回合；维护后逐项核对并按需恢复已有项目。Ghidra 用匹配的保存程序跳过分析重新打开，避免重新导入覆盖旧分析。项目缓存、用户计算任务和 host jobs 各自明确生命周期。

```bash
python3 "$AS" lease TASK_ID --action acquire --resource project:ABSOLUTE_PATH --owner SESSION_ID --ttl 300
# 从返回值取得 token。guard 选项放在 -- 前，命令放在 -- 后。
python3 "$AS" guard TASK_ID --resource project:ABSOLUTE_PATH --owner SESSION_ID --token TOKEN --timeout 300 -- python3 rpc_driver.py rename-function ./sample FUNC NAME
```

`renew`/`release` 需当前 token；过期重新认领产生新 token，旧持有者不能继续使用旧 token。实例变更操作还传 `--target ID --generation N`。guard 检查任务状态、租约、目标代次并记录结果；超时后结果可能未知，先核对外部实际状态，再考虑重试。

这一接口约束通过 guard 发起的操作，不能推断任意 shell 命令的资源语义。共同写同一项目时统一使用这个入口；已有 Ghidra handler 的串行锁继续生效。guard 不替代目标系统自己的事务机制。

长任务可用 DSH 原生 jobs 或 `guarded_run.py`，也可使用满足日志、心跳、超时、进程树终止和结果查询的等价工具。需长时共享变更时按预计时长设置 guard timeout；不要让裸进程脱离租约继续写。

### 访问具体目标的原生后台任务

在普通分析会话已有授权、需要后台访问目标时，用 `job_scope` 为未来原生后台 bash 设置当前目标代次、环境标识与期限；随后照常使用 bash(run_in_background=true)、job_output/job_kill。原生 job id、真实 owner 与执行句柄由宿主自动登记，不要求再手工注册 PID。示例和覆盖见 [native-jobs.md](references/native-jobs.md)。此接口不执行命令，不扩大权限，不给 SSH/FTP 提供请求计数。

目标更新、任务离开 running 或重新绑定前，入口取消其登记的旧任务并等待原生执行器确认收尾；未确认则拒绝切换并保留清理异常。更换目标后重新设置作用域。普通离线计算、未登记的既有任务和共享长期服务不自动认领或终止；外部平台的槽位释放仍需调用方在切换成功后操作。

## 交接

交接记录包含任务/目标代次、待回答问题、事实与证据ID、失败实验、资源/变更权限、预算、返回格式和清理责任。子代理返回结论适用范围与实际加载的 skill 文件版本；主代理复核后合并。父代理的加载历史不代表子代理已加载全文。

旧二进制台账仍可通过 `ghidra-core/scripts/ledger.py` 使用，接口见 [legacy-ledger.md](references/legacy-ledger.md)。纯 Web/数学任务使用 Task/Target，不创建空文件充当样本。环境探针 `discover` 提供路径和按需 import 测试，操作细节见 [runtime.md](references/runtime.md)。

## 结构化记忆与有限协作

需要恢复分析成果、比较假设/实验、保留失败边界或委派只读子任务时，读取同级 analysis-memory/SKILL.md。先使用本工具 init/bind 确定唯一任务，再用 dsh_memory_write 的 open 连接该任务；记忆与协作复用 analysis-state/state.sqlite3，不再创建另一套任务库。目标代次、资源租约、检查点与完成仍由本运行层维护。主 agent 保留核心分析，按需要使用 analysis_collaboration 派发只读原生子 agent。reviewed/adopted 不等于目标 accepted。完成任务前显式复核或放弃协作支线。

## 受控请求与完整交接

需要任务级请求预算、来源限制、凭据引用或完整长材料交接时，读取 [controlled-requests.md](references/controlled-requests.md)。先用 dsh_control status 确认覆盖；普通会话未全局拦网。宿主显式导入策略后，该会话仅可经受控 HTTP 发送器联网，不可用 shell/浏览器/MCP 绕过。主 agent 继续核心分析；方法提示不作为硬门。
