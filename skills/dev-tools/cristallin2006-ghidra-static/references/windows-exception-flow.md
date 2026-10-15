# Windows PE 异常控制流

只在 PE 存在 SEH/VEH 注册、显式异常、INT3/非法指令、异常过滤器或调试器已观测到 handler 时启用。Linux 信号样本继续读 `exception-control-flow.md`。

1. 检查导入、TLS/初始化、`AddVectoredExceptionHandler`、`SetUnhandledExceptionFilter` 和 x86 FS:[0] 链；x64 检查 `.pdata/.xdata` 与 unwind 信息。记录 handler 地址、注册时刻、触发点和异常类型。导入缺失不排除动态解析。
2. 在调试器对异常触发点与 handler 下断，记录 first/second chance、异常码、上下文变动及 handler 返回后的 RIP/EIP。把“正常边”和“异常边”分别画到校验/输出函数；反编译器无 xref 仅表示其 CFG 缺边。
3. 只对目标 handler 和后继函数做局部反编译、常量提取与求解。`angr call_state` 需要已确认入口、调用约定及异常后的状态；整程序 `explore` 路径爆炸时立即停机并记状态/时间上限。
4. patch 异常或反调试仅供定位；候选必须在未修改 PE 的目标环境复验。若 Wine 与 Windows 结果不同，Windows 原生运行的异常链为此类样本的优先证据，记录最小差分。

不得从“正常路径只打印某句话”推断异常路径不可达。可达性否定仍遵循 ledger 的 `--kind negative --proof` 规则。
