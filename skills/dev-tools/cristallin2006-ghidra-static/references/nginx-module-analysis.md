# nginx 模块：注册、回调与生命周期

nginx 模块、配置指令或跨请求对象影响当前分析时按需读。模块注册、配置 set 回调与最终请求 handler 是不同入口，命令名不代表已找到请求处理函数。

恢复 ngx_module_t、ngx_command_t、ctx 与 handler 时，用实际版本/架构/构建的定义、重定位、节映射、字符串和消费指令相互约束。NGX_MODULE_V1 的 name 可为 NULL，index/ctx_index 可为 unset；名字可由 ngx_module_names 提供。磁盘占位/未重定位值不是运行态指针。

某 AMD64 profile 的记录长 0xc8 不代表 0xc8 对齐或所有版本固定结构。无符号时从相关字符串、回调、表关系提出候选；不按步长扫全文件自动认定。不支持的 relocation/布局保持 unknown，不套旧偏移。

main/server/location、ctx_index 与实际 loc_conf 分别核对。set 回调可能仅写配置，实际请求路径还受 location 匹配、阶段 handler、过滤器与模块状态影响。单样本任意前缀响应不证明新实例所有路径同样可达。

master、worker、connection、request、pool 是不同寿命域。模块全局通常属于进程，跨请求全局不等于跨 worker 共享；keep-alive 不证明对象/计数器/后端状态恒定。request pool cleanup 后全局仍留指针是 UAF 线索，仍核对释放与后续访问。

worker 替换、exec、后端重连或库改变后，关联当前进程身份/映像/连接与对象代次；旧地址/公式不因模块同名继续有效。argv 可改写，pidfile 不证明稳定身份/清理权。只读识别、attach、重启与清理是不同动作。

fork 可共享 fd/socket inode，不能单独认定当前请求所有者。模块 load bias 需 PT_LOAD/maps/映像身份，不取首个 offset=0；参见 re-dynamic/references/process-observation.md。需要时复用目标地图与记忆；简单查询不必建全图，不为找隐藏 relay 全量扫描或自动调用。

依据：nginx [ngx_module.h, release-1.28.0](https://github.com/nginx/nginx/blob/release-1.28.0/src/core/ngx_module.h)。独立归纳，不分发 nginx 头文件或题目模块。
