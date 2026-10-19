# 必要技能材料交付（0.6.1）

解决已经选择必要方法但 Solver 忘记调用 skill 的问题。方法选择由编排代理负责；运行层保证已声明正文进入子代理当前上下文，不证明理解、正确应用或结果接受。

## 选择材料

新 Solver 的 add options 增加 skill_plan：

```json
{"required":[{"name":"ghidra-static","reason":"本分支需核对未知数据与程序语义","references":["references/data-driven-recovery.md"]}]}
```

按当前问题选必要入口。references 可以省略或补充深入卡；宿主仍会合并 skill 自身声明的必需参考卡。brief 中的打法摘要是派单上下文，不能代替方法原文，也不能作为“无需专业方法”的理由。不把整个知识库、全部链接或父代理已读内容复制给子代理。简单读取、格式转换或纯材料复核可明确：

```json
{"required":[],"none_reason":"仅汇总给定字段，不需要专业分析方法"}
```

缺少计划会明确拒绝，不自动猜测一套固定技能，也不要求所有任务至少加载某个通用 skill。Observer 仍是零工具的材料审查，不接受非空必要技能清单。

## Skill 自身的完整参考卡契约

本地目录 provider 的 skill 可在 SKILL.md 同目录维护 skill-materials.json：

```json
{"version":1,"required_references":["references/local.md"]}
```

这是知识包维护者对必要原文的声明，不由 brief 或模型自报覆盖。宿主将 required_references 与派单 references 取并集，去重后装入同一受验证区块。显式 references=[] 也不关闭 skill 声明的卡；不递归加载卡片中的所有链接。未提供声明的旧 skill 沿用主文加显式卡的行为，非本地 provider 不自动取得文件读取能力。

声明存在但 JSON 错误、版本/字段不支持、路径越界、文件缺失或材料过大时，该 Solver 在模型步骤前阻塞，不悄悄降级成只读 brief/主文。policy 本身最多 16KiB；每 skill 的必需卡与额外卡并集最多 8 张，完整区块仍限 64KiB。应维护小而相关的核心材料包；要改变必需包应修改并复核 skill 声明，而不是在派单中绕过。

## 宿主交付与可见性

每次原生上下文组装时，用该子代理的 scope/cwd/signal 查询原生技能注册表，检查 modelInvocable，使用原生正文渲染方式及资源位置；不继承主代理的技能权限，也不绕过禁用策略。

必要材料占独立的运行时上下文区块。原有 available_skills 目录和 skill 工具不被替换或过滤，其他方法与深入资料仍可按需调用。正文不会自动授权执行工具、安装、联网或再派发。

运行层在模型步骤进入前核对完整材料是否可见，覆盖直接文字作答的 Solver。上下文压缩采用原生替换/恢复机制；相同版本保持一份当前区块，不逐回合重复追加历史。续做和冷恢复重新解析当前版本，不永久相信 loaded 布尔值。材料内容或资源位置变化后更新摘要与交付记录。

当前最多选择 8 项 skill，每项必需与显式参考卡并集至多 8 张，完整区块最多 64 KiB；这些是材料边界，不是任务时限或推理步数。超限时收窄必要清单、将深入阅读留给 Solver，或按实际独立问题拆工作，不静默截断。正文占用模型上下文；宿主和模型原有输入限制仍适用。

参考卡只支持被选 skill 的本地目录 provider 下的 references/*.md，拒绝绝对路径、目录穿越和越界软链接；不联网取 URL，也不把任意路径包装成技能资料。资源没有本地目录或缺失时，报告具体材料阻塞。

## 状态与修复

status/result 的 skill_delivery：

- pending：已选择，尚未装载。
- prepared：宿主已完成组装，等待步骤可见性核对。
- delivered：完整区块在原生模型步骤入口可见，含 provider、来源、声明文件摘要、正文/参考卡摘要与组合摘要。references[].required_by 标明由 skill、assignment 或两者共同要求；coverage 显示技能数、参考卡数、声明要求的参考卡数。
- not_required：编排明确选择了无需专业方法，并保留理由。
- blocked：材料缺失、禁用、越界、过大或当前正文不可见；该 Solver 不进入模型推理。
- 旧记录的 undeclared 仅表示没有计划，不能解读为读过。

skill 调用次数为零不代表正文未交付，调用了一次 skill 也不证明 references 已读；看实际交付回执和当前原文可见性。status 为轻量摘要，完整路径和哈希在 result view=detail；不要常规反复拉取全量。

这些状态都不是“理解/应用已验证”。正文不存入编排状态表；实际材料随原生上下文保存，状态表仅保存选择和交付元数据。相同内容与交付状态不反复制造事件。

缺失材料只影响对应 Solver，不将整台宿主标为故障。按实际问题补安装/可读材料或调整工作；不为通过检查而写虚假 none_reason。取消、暂停与结束保持可用，不强迫继续无价值的路线。

旧 pending 工作没有计划时，先调用 set_skills options={work,skill_plan}，再 dispatch。已返回或失败的 Solver 可用 followup options={work,message,skill_plan} 更新选择并在同一 child 续做；在途工作不接受计划替换。必要时先正常暂停/取消，不能在工具运行中悄悄更换方法契约。

首次装载失败时，原任务材料可能尚未进入原生会话；修复后 followup 会补回当前任务交接。新结果仍按原 result_revision 和依赖规则复核；更改材料不能绕过已有采纳依赖的修订保护。

本功能不自动识别所有应读技能，也不强制全部 reference；它会交付被选 skill 声明的完整必需参考卡。遗漏“选择哪项方法”仍需分诊与证据复核；运行层负责的是已声明材料的可靠交付。
