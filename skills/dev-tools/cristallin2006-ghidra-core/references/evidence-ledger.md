# 旧二进制台账兼容接口

`ghidra-core/scripts/ledger.py` 为 runtime/analysis-v1/legacy_ledger.py 的薄包装。存储仍是样本 hash 关联的 JSONL，历史条目不重写，完整 CLI 操作统一加锁。纯服务与数学问题使用 analysis-session 的 Task/Target。

query/observe/conclude/anomaly/resolve/hypothesis/plan/brute/stuck/status/render/validate 名称保留。observe 的 delta 可选，区域重试和相似 stuck 不再拒收。model/negative 不要求固定 anchor/proof 前缀；结论仍要求内容与证据，既有 ID 更新用 --overturn 追加新版本。

conclude 新增 origin、verification、scope、unresolved。无程序接受证据的 kind=flag 记录为 untested 候选；verification=accepted 必须提供 program-accept，但字段存在不证明真实性。测试范围由模型说明。independent=yes 只是来源声明。已有平台参数只为旧调用兼容保留，不提供平台特定提交行为。

```bash
python3 "$L" observe ./sample --region check --tool gdb --note "关键观察"
python3 "$L" conclude ./sample --conclusion "候选输入" --evidence "日志路径/命令及输出" --kind flag --verification untested
python3 "$L" stuck ./sample --at check --tried "已做实验" --escalate "下一步实验"
```

假设可以保持 open；只有标 confirmed/killed 时仍要求实际证据，无法确认时保持未决或说明豁免。交付可以保留未决项。损坏 JSONL 不静默忽略，需保存原件并核验截断。建议型信息可忽略并按实际范围解释。


新任务接口见 analysis-session。
