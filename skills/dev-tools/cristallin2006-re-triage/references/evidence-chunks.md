# 已保存分块的完整性与恢复

用于本地已经取得的多段文件、短读、重试或跨阶段恢复；不固化 SQL 下载器，不自动连接、重试或执行目标代码。传输仍走已有授权、请求预算与资源生命周期。完整性未知不等于内容不可用，但不能以零填充产物假装完整原件。

## 明确同一来源

记录来源 identity、generation、version（未知可为 null）、预期 size、可选 source_sha256，以及每块 offset、实际 length、requested_length、path、sha256 和对应 source。版本是调用者声明，不是工具对远端当前状态的独立认证。

本地 SHA-256 标识实际取得的字节。只有与已声明的可信源摘要相等，才有该比较结论；缺源摘要/快照保障时，即使字节范围齐全也保留远端一致性未知。相同大小或文件名不足以认定跨代次恢复安全。

## 本地组装器

```bash
python3 scripts/evidence_chunks.py saved/manifest.json
python3 scripts/evidence_chunks.py saved/manifest.json --out recovered.bin
```

manifest 顶层为 `{version:1,source:{identity,generation,version},size,source_sha256,chunks}`；source_sha256 可为 null。每块为 `{offset,path,sha256,source,length,requested_length}`，path 相对于清单目录。使用实际已保存块的 SHA-256；source 与顶层一致，generation 为非负整数。

- 允许乱序、相同字节的重复/重叠和短读记录；重新运行时重新核对文件与 hash，不发起传输。
- 缺口、冲突、长度/hash 改变、来源/版本不同、路径逃逸或特殊文件不会被当成有效完整原件。
- 返回 missing_bytes、gap_ranges、冲突位置、每块短读回执；位置列表过长时有显式 omitted 标记，完整性结论仍按全部已读字节检查。
- 只在完整且未违背声明摘要时允许 `--out`；创建新的 0600 文件，临时文件写好后发布，不覆盖现有文件或符号链接。缺口不产生零填充文件。输出/输入目录需由调用者保证在授权范围内；该工具不是 OS 文件系统隔离边界。
- `snapshot=unknown/caller_declared_version` 与 `matches_declared_source_digest=null/true/false` 分别表达已知范围；不自动宣称远端已验证。

`--max-size/--max-chunks/--max-read/--max-manifest` 限制单次内存、输入与工作规模，可按实际材料配置，不限制任务累计材料数量。超限明确拒绝，不能为绕限静默删块。清单和块包含原始数据引用，应留在项目私有证据中，不自动发布为跨任务方法卡。
