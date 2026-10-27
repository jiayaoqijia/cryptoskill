# BEAM 制品：静态观察与运行边界

用于 FOR1/BEAM、.beam、ebin 或 Erlang/Elixir release。Web 请求/认证由 `ctf-web/references/elixir-beam-web.md` 承接，校验数学由 `ctf-crypto/references/crc-oracle-contracts.md` 承接；无需按专业固定增加代理。

## 先确认实际可读材料

元数据、源码、BEAM 制品和完整 release 不等价。记录文件 hash、来源、完整性和对应版本；缺少附件就保留假设，不凭产品名构造确定链。已可读代码/字面量可减少无区分力的猜测，不强制一律先逆向或下载全部运行时。

BEAM 是 IFF 类容器：FOR1 长度、BEAM 标识、chunk 长度及四字节对齐都需核对。OTP 27 的 LitT 先声明未压缩大小，再存 zlib 数据；解压后包含数量与带长度的 ETF 项。原子、指令、类型和调试格式有版本差异，不能将一个版本的编码规则当通用反汇编器。

## 只读清点器

```bash
python3 scripts/beam_inventory.py /explicit/module.beam
python3 scripts/beam_inventory.py /explicit/module.beam --max-preview 4096
```

从本 skill 目录调用，或使用工具实际绝对路径。工具读取一个显式本地普通文件，清点 chunk、OTP 27 风格 Atom/AtU8、导入/导出/本地函数表和安全支持的 ETF 子集，不执行模块、release boot、调试后端或 on_load，也不反汇编 Code 指令。

- ETF 支持整数、有限浮点、原子、nil、tuple/list、map 与 binary/字节列表；map 保留键值对，不覆盖重复键。函数、引用、进程等其他标签保留为 unsupported 的整项 hash 与定位，不猜长度继续解释该项。
- `container_valid` 只指容器结构。`literal_coverage` 分开列 decoded/unsupported；未知 chunk 仍在清单里，不据此声称完成语言语义恢复。
- binary/字节列表预览带 length、hash、preview_truncated；需要更多时显式提高 `--max-preview` 并回查原件，不把预览当完整源码。
- 字面量给出 compressed_chunk_file_offset 与 decompressed_entry_offset；后者不是直接文件偏移。原子/表项使用实际文件位置。
- Dbgi 只报告存在性；有调试信息也可能需语言后端或解密，缺失则不能声称恢复源码。

输入、解压输出、项数、节点、深度和预览边界可通过 `--max-*` 配置，超限明确失败，不限制任务总时长或解题次数。特殊文件、损坏长度、压缩尾随数据和重复 chunk 不当成正常制品。

## 若确实需要运行时观察

先探测已安装的可信工具和匹配 OTP；使用 `beam_lib` / `beam_disasm` 时区分解析和加载模块。启动从目标取得的运行时或 release 是执行不可信代码，应走原有隔离与资源审批路径；缺 OTP 不是默认自动从目标取回并运行的理由。

字符串、导入和导出只是候选。结合调用方、路由匹配、权限与原目标反馈核对；本地模型、同源 mock 自洽、调试后输出和原目标接受分别报告。分块制品的完整性见 [分块证据](evidence-chunks.md)。提取结果可能含实例秘密，原始输出留在授权项目证据中，不自动发布到方法库。

格式依据：[OTP 27 beam_asm](https://github.com/erlang/otp/blob/OTP-27.3.4.4/lib/compiler/src/beam_asm.erl)、[ETF](https://www.erlang.org/docs/27/apps/erts/erl_ext_dist.html)、[beam_lib](https://www.erlang.org/docs/27/apps/stdlib/beam_lib.html)。工具为独立实现的受限观察器，不是完整 OTP 兼容层。
