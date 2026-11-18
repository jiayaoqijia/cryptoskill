# 模型分工（2026-10-28 用户确认）

由 Research Bot 调度，通过 Codex CLI 前台阻塞执行并设超时；不放后台 nohup，否则跑完不会唤醒调度方。依据：Stone 提供的路由惯例，以及 runtime/experiments/model-ab-20261028 的 terra 与 sol 对比。

| 环节 | 模型 · effort |
|---|---|
| 脚本处理不了的采集、整理、测试 | gpt-6-luna · high |
| 身份核实、来源索引、复盘解释 | gpt-6.1-terra · medium |
| 证据可信度与跨源核验 | gpt-6.1-sol · medium |
| 独立复核与反证（不同于主判断的模型） | gpt-6.1-terra · high |
| 最终信号与高风险判断 | gpt-6.1-sol · high |

- gpt-6-astra 只在用户点名时使用。
- 不使用 Fast 或 Ultrafast 模式；不先用便宜模型、失败后再升级。
- 喂给模型的是精简证据包，不是全量上下文。模型只读写 runtime 下的任务目录。不传入密钥，也不对外发送任何内容。
- 每步记录实际模型、effort、耗时、token 和退出码。拿不到的写 unknown。
- 调用方式：`python3 "$SKILL_ROOT/scripts/codex_step.py" --task-dir <任务目录> --model <model> --effort <effort> --step <步骤名> --prompt-file <prompt.txt> --timeout <秒>`。它实际执行 `~/.local/bin/codex exec --skip-git-repo-check -C <任务目录> -s workspace-write -m <model> -c model_reasoning_effort=<effort> --json "<prompt>"`（stdin 置空），并把模型、effort、耗时、退出码和 token（从 `turn.completed.usage` 解析，拿不到写 unknown）追加到 `<任务目录>/steps.jsonl`。
- 不再使用绕过审批和沙箱的参数。workspace-write 沙箱下，模型只能写任务目录，默认不能联网；需要的数据先冻结进任务目录。
- Hermes、Gemini、Bridge Bot 均未实测，不作为主路线。
