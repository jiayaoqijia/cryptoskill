# APK 分诊细则（结构 / AXML / 签名 / 多 dex / flag 全扫）

路径变量沿用 SKILL.md 路径约定（`$CT` `$BT` `$AGPY`）。

## 1. zip 结构（APK 就是 zip）

```bash
unzip -l app.apk                                   # 快速看条目
"$CT/apkanalyzer.bat" files list app.apk           # 官方口径，含大小
"$CT/apkanalyzer.bat" files download app.apk out/  # 按需取条目，不全量解压
```

关键条目速查：

| 条目 | 看点 |
|---|---|
| `classes.dex`, `classes2.dex`… | 全部逻辑所在；**逐个统计，别只看第一个**（§4） |
| `lib/<abi>/*.so` | 有则部分逻辑可能在 native → ghidra-static；ABI 优先 x86_64 |
| `AndroidManifest.xml` | 二进制 AXML，直接读是乱码 → §2 |
| `resources.arsc` | 字符串/资源索引表；flag 文案可能藏在 strings.xml 编译产物里 |
| `res/`, `assets/` | 附件、加密资源、第二级载荷常藏 assets |
| `META-INF/` | 签名分诊 → §3 |
| `kotlin/`、`META-INF/*.kotlin_module` | Kotlin 痕迹，自有类过滤时别误伤 |

## 2. AXML / Manifest 要点

**不要手写 AXML 解析器**（偏移坑实测踩过两个）——两条免解析途径：

```bash
"$CT/apkanalyzer.bat" manifest print app.apk       # 直接出文本 Manifest
"$JADX" -d jadx-out app.apk                        # jadx 顺带还原 Manifest + resources.arsc
```

需要资源表内容时：`"$BT/aapt2" dump badging app.apk`、`"$BT/aapt2" dump xmltree app.apk --file AndroidManifest.xml`。

字段 → 行动对照：

| 字段 | 判定 | 行动 |
|---|---|---|
| `android:debuggable="true"` | 可调试 | `adb shell run-as <pkg>` 读私有目录；jdwp 附加调试；动态优先 |
| `android:usesCleartextTraffic="true"` | 允许明文 HTTP | 有网络行为时抓包可得明文 → traffic-analysis |
| `android:extractNativeLibs="false"` | so 不落地解压 | 与"无 so / so 未压缩直接 mmap"互相印证；统计 lib/ 时别漏 |
| `application` 的 `name` 属性 | 自定义 Application 类 | 校验逻辑可能在 `onCreate`/`attachBaseContext` 提前跑，jadx 里优先看 |
| `activity exported="true"` | 可直接 `am start -n` 拉起 | 动态驱动入口清单 |
| `provider exported` / `deeplink` | 外部可达攻击面 | CTF 里常是绕过 UI 直接喂校验的捷径 |

## 3. 签名版本判定

```bash
unzip -l app.apk | grep -E 'META-INF/(CERT\.RSA|MANIFEST\.MF)'
"$BT/apksigner.bat" verify --verbose --print-certs app.apk   # 有签名时看 v1/v2/v3 各档 true/false
```

| 证据 | 判定 | 后果 |
|---|---|---|
| `META-INF` 无 `CERT.RSA`/`MANIFEST.MF`，apksigner 报 does not verify | **v1 未签名** | 可自由改写 zip 内容后 `apksigner sign` 重签（SKILL.md §4） |
| 仅 v2/v3 signing block 有效 | v2+ 签名 | 任何字节改动破签名；改逻辑走 frida 动态 patch，别重签 |
| v1+v2 均有 | 双签名 | 改动后 v2 必破，重签也无法还原原证书；同上行 |

CTF 题多为第一种；判定记录进 ledger（`observe`，key 用 apk 文件名）。

## 4. 多 dex 自有类统计法

**启发式**：dexJEA/multidex 分包时，体积最大的 dex 几乎总是 androidx/material/kotlin 库代码，应用自有逻辑常集中在一个**极小 dex**。实测基准：`classes.dex` 5.1MB / 3346 类 / 自有类 0；全部逻辑在 `classes3.dex` 3172 字节 / 3 类 / 23 方法。

一条命令出逐 dex 统计（androguard 4.1.4，API 已验证）：

```bash
"$AGPY" - <<'EOF'
import re
from androguard.core.apk import APK
from androguard.core.dex import DEX
LIB = re.compile(r'^L(android|androidx|kotlin|kotlinx|com/google|org/apache|com/squareup)/')
a = APK("app.apk")
for i, blob in enumerate(a.get_all_dex()):
    d = DEX(blob)
    names = [c.get_name() for c in d.get_classes()]
    own = [n for n in names if not LIB.match(n)]
    print(f"dex#{i}: {len(blob)} 字节, {len(names)} 类, 自有 {len(own)} 类")
    for n in own[:15]:
        print("   ", n)
EOF
```

- 库前缀过滤表按需扩（`Lcom/bumptech/`、`Lio/reactivex/` 等常见库同理）
- **自有类为 0 的大 dex 直接跳过**；自有类 <20 个的 dex 优先人肉通读
- 与 flag 全扫（§5）交叉：命中的字面量落在哪个 dex，就坐实了哪个 dex 是主战场

## 5. flag 全扫（APK 扫描面）

flag 形态 regex 集的权威源在 **re-triage `references/triage.md` §4**（标准/赛事前缀/裸 hex/MD5 形态），此处只记 APK 特有的**扫描面**：**所有 dex + resources.arsc + assets 全扫**，不只扫 classes.dex。dex 字符串是长度前缀 UTF-8，`grep -a` 可直接扫二进制：

```bash
mkdir -p /tmp/apkx && unzip -o -q app.apk -d /tmp/apkx
grep -aoE 'flag\{[^}]*\}|BJD\{[^}]*\}|CTF\{[^}]*\}|\{[0-9a-fA-F]{16,}\}' \
  /tmp/apkx/classes*.dex /tmp/apkx/resources.arsc 2>/dev/null | sort -u
```

扫不出 → flag 是**逐段拼接/变换**出来的，转 SKILL.md §2 校验点定位套路（找 `StringBuilder` append 链、xor/add 循环）。扫出多个 → 逐个过真机 oracle 正负对照。
