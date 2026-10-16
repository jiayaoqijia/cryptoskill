# 原生后台任务：目标、期限与收尾

适用：普通会话已获准访问具体目标，并需要用原生后台 bash 执行。受控 HTTP 会话仍只用 dsh_control，不得通过本入口绕过其工具边界。

先 init/bind，登记由可信平台返回的当前 target 信息。目标 id 保持稳定，实例变化才更新代次；交接传目标 id/代次和来源引用，不重抄 IP 或明文凭据。随后：

```json
{"action":"job_scope","task":"实际TASK_ID","options":{"action":"set","target_id":"service","generation":1,"environment":"实际共享环境标识","ttl_seconds":60}}
```

60 秒仅为语法示例，按实际任务设置。既有策略的额度不会因设置或重设 scope 增加；可附 budget_ref 作为关联，但原生 bash 没有每请求额度保证。执行权限与审批仍由原工具决定。

作用域适用于该 owner 此后启动的原生后台 bash，包含在该 scope 中启动的计算；离线计算需要独立生命周期时先 clear 或使用普通未设 scope 的会话。不要用 nohup、双重后台或另起宿主脱离管理器。已启动的历史任务不追溯纳管。

宿主自动登记 job id、owner、task、target/generation、environment、期限；不复制命令、凭据或 job 输出。TTL 到期请求原生 job 取消，原生执行器负责其进程树。状态仍为 stopping 时不宣称停止；此机制不是操作系统隔离，主动脱离原生进程管理的进程不在保证内。

- 查询：`job_scope options={action:"status"}`；或 analysis_session status 的 readiness。job_output 保留原有输出查询。
- 清除：`job_scope options={action:"clear"}`，先取消并确认该 owner 已登记任务收尾，再移除 scope。
- 切换：通过 analysis_session target、transition 或 bind；入口先阻止该任务启动新的受管后台工作，再取消相应旧工作并等待。清理失败、超时或另一宿主的未确认任务会阻止切换。
- 外部槽位：本入口不直接调用平台 API。只有本地切换/清理成功后，调用方才释放或重建平台实例；绕过本入口的外部变化只能由后续代次/状态核对发现。
- 恢复：执行权威仍是原宿主的 job 注册表。持久化记录不自动恢复执行，旧宿主失联时显示未确认，需核对原执行器与环境，不能拿同名新 job id 代替。不会按全局进程名清理 Ghidra 等共享服务。

目标/task 的 CLI 入口会拒绝存在未确认原生任务的变更；正常收尾由拥有执行句柄的宿主完成。任意代码仍能修改本机状态，不将本插件宣传为对恶意宿主的安全隔离。
