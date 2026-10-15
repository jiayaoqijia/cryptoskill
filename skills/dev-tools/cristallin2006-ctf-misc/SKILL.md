---
name: ctf-misc
description: 处理编码与语言沙箱能力隔离、受限解释器、二维码/音频/RF、特定游戏/VM 杂项问题。按明确能力使用；不作为所有未分类任务的兜底或通用调度入口。
---

# ctf-misc

## 输入与输出

输入为材料、解释器/沙箱条件与具体问题；输出为可复现变换、能力边界、输入/输出及验证范围。

编码先识别候选变换并用已知输入检验，多层变换记录顺序和中间产物，重复工作可用脚本或 CyberChef。语言沙箱先明确版本、对象可达性、过滤器、宿主桥接和执行条件；HTTP 会话与运输由 ctf-web 处理。已有 Web 资料 node-and-prototype.md 可按 vm2/原型链线索读取，不要求加载整个 Web 正文。

游戏/VM、DNS 协议、音频/RF 按下面专题选择。pcap 取证交 traffic-analysis，数学结构交 crypto，二进制语义与内存利用分别交 static/pwn。CTFd 导航资料仅在用户明确需要平台操作时读取，不触发本 skill 的通用分析路由。设备/系统操作遵守任务范围。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。


## 决策表(症状 → 读哪个文件)

| 症状/线索 | 读 |
|---|---|
| pyjail:eval/exec 过滤、builtins 裁剪、audit hook | `pyjails.md` |
| bash jail / 受限 shell(rbash、命令白名单) | `bashjails.md` |
| 编码识别、多层解码链、二维码、DTMF、SMS PDU | `encodings.md`、`encodings-advanced.md`;确定性变换直接用 `cyberchef` CLI(见 `cyberchef-cheatsheet.md`) |
| RF/SDR/IQ 信号(QAM、载波恢复) | `rf-sdr.md` |
| DNS 利用(ECS 欺骗、NSEC 走链、IXFR) | `dns.md`;**pcap 里的 DNS 隧道 → traffic-analysis** |
| 游戏题/WASM/K8s/浮点/汇编沙箱/Docker 逃逸 | `games-and-vms.md`、`games-and-vms-2.md`、`games-and-vms-3.md`、`games-and-vms-4.md` |
| Linux 提权(sudo/SUID/cron/docker 组) | `linux-privesc.md` |
| CTFd 平台 API(列题/下载/交 flag) | `ctfd-navigation.md` |
| Unicode 隐写/浮点藏字节/杂项一句话技巧 | `quick-reference.md` |

`quick-reference.md` 用于专题不明时的速查；只读取当前相关资料。

## 平台成本决策

需要评估 hint 或有限容器槽位时，按需读取 [platform-decisions.md](references/platform-decisions.md)，结合原材料、成本和信息价值；不以请求数充当分析进展。
