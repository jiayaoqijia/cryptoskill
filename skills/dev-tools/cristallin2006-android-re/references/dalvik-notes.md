# Dalvik / smali 速查（校验点定位用）

供 apkanalyzer `dex code` 输出或 baksmali 风格文本的对照阅读。Java 与 smali 视图包含不同的重建/渲染假设。条件分支、位宽、异常路径或反编译结果影响结论且有疑点时，按当前问题核对相关原始字节码。

## 1. 常见 opcode 形态

| 形态 | 含义 | 定位价值 |
|---|---|---|
| `const-string vX, "..."` | 字符串常量入寄存器 | 锚点：Toast 文案、待比较的目标串 |
| `const/4 vX, 0xd` | 小常量（/4=4bit，/16=16bit） | 移位量、xor key、数组长度——**算法真相在这里，不在字段声明** |
| `invoke-virtual {vA, vB}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z` | 字符串比较 | **校验点核心**，调用点就是胜负手 |
| `move-result vX` | 接上一个 invoke 的返回值 | equals 的布尔结果在此，顺它找 `if-eqz/if-nez` |
| `if-eqz vX, :label` / `if-nez` | 零/非零条件跳 | 校验分支：跳向 wrong 还是 success |
| `if-lt/if-ge/if-gt/if-le vA, vB, :label` | 双寄存器比较跳 | 逐位比较循环的出口条件 |
| `xor-int/2addr`、`add-int/lit8`、`shl-int`、`ushr-int` | 算术/位运算 | 变换算法主体；`/lit8/lit16` 后缀 = 第二操作数是硬编码字面量 |
| `aget` / `aput` / `array-length` | 数组读写/长度 | 逐字节变换循环 |
| `new-instance` + `invoke-direct ...-><init>` | 构造对象 | `StringBuilder` 拼 flag 链的起点 |
| `sget`/`sput`/`iget`/`iput` | 静态/实例字段读写 | **判定字段是否真被读**（§4 误导识别） |
| `invoke-static ...->valueOf` / `->append` | StringBuilder/String 工具调用 | flag 拼接链 |

## 2. const-string / invoke 模式

典型校验片段（看到即认领）：

```smali
const-string v1, "wrong!!!"              # 失败文案 = 锚点
const-string v2, "success!!!"            # 成功文案 = 锚点
...
invoke-virtual {v3, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v0
if-eqz v0, :cond_wrong                   # equals 返回 0 → 跳 wrong
```

- 从 `"success!!!"`/`"wrong!!!"` 的 `const-string` 反向找：哪个 `:label` 指到它 → 哪个条件跳引用该 label → 条件跳的输入是哪个 `move-result` → 是哪个 `invoke` 的返回值。四步走完，校验点闭环。
- `invoke-virtual` 第一个寄存器是 this（`String.equals` 时即左侧串），第二个是参数——**用户输入 vs 目标串，谁左谁右决定哪边是变换算法的输出**。
- 非 equals 的比较也要查：`contentEquals`、`equalsIgnoreCase`、`compareTo`、`Arrays.equals`、`MessageDigest.isEqual`、`String.regionMatches`。

## 3. equals 比较点定位流程

1. jadx 全局搜成败文案（`success!!!`/`wrong!!!`/`正确`/`错误`）→ 得到校验方法名
2. apkanalyzer smali 里搜同一文案 → 拿到 smali 级条件跳结构（jadx 内联优化可能藏分支）
3. 两侧串的来源各追一条数据流：
   - 目标串是 `const-string` 直接给出的 → 答案可能就是明文，但仍需 oracle 验证
   - 目标串由变换产生（xor/add/shift 循环）→ 把循环抄成 Python/Java 复算；**复算用反编译代码原样编译执行**（本机有 JDK），别手抄逻辑
4. 循环出口是逐位 `if-ne` 类比较 → 可逐位 oracle/穷举；是整体 equals → 必须整体构造

## 4. 误导识别（R 类与命名陷阱）

以实际指令、输入和数据流为依据；名字、声明值和静态引用是线索，不独立证明运行时行为。

| 误导手法 | 形态 | 对策 |
|---|---|---|
| 类名误导 | 类叫 `ROT14`，实际是 ROT13 | 数 `add-int/lit8` 的字面量，不读类名 |
| 字段诱饵 | 字段声明 `shift = 13`，但算法用硬编码字面量，字段**从未被 iget/sget 读取** | 核对真实字段 descriptor 与读取点；所选静态范围未找到读取仍不排除反射、JNI、序列化或动态加载 |
| R 类混淆 | 资源 ID（`0x7f0e00xx`）查表得到字符串，静态视图只见数字 | jadx 已解 resources.arsc；smali 里查 `R$string` 对应常量再回表 |
| 字符串拆片 | `"fl"+"ag{"` 分散在多个 const-string | grep 全集模式（`flag\{` 扫不出时改扫 `\{`、`}`、单段 hex） |
| 假校验函数 | 存在多个 equals 调用点，真校验从不被 UI 路径调用 | Toast/UI 锚点只是一个入口；其他组件、回调、反射和未加载 DEX 仍可能调用，缺证据时保留未知 |
| 控制流平坦/字符串加密 | 全部字符串运行时解密 | 静态不硬刚 → frida hook `String.equals`/`String.<init>` 运行时收割（SKILL.md §3.3） |

遇到反编译异常或关键歧义时，可用合适的字节码视图/另一实现核对相关命题；不强制所有方法都跑两个工具。说明共享输入与解码假设，不把视图一致当作运行时接受。精确引用索引见 [DEX 静态索引](dex-static-index.md)。
