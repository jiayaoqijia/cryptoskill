> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 加密算法识别：指纹与语义核对

本文件提供算法候选；常量、API 与结构命中还需结合消费者和实际参数核对。crypto_sanity.py 仅检查已声明的局部格式，不能证明算法、密钥或完整模型正确。

## 1. 常量指纹（生成候选，结合使用点核对）

| 指纹 | 算法 |
|---|---|
| `63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76` | AES S-Box（前 16 字节） |
| 字符串 `"expand 32-byte k"` | ChaCha20 / Salsa20 |
| `30 82` 序列 + PEM marker | RSA（ASN.1 密钥结构） |
| `67 45 23 01 ef cd ab 89`（小端写入） | MD5 初始值 |
| `67 e6 09 6a 85 ae 67 bb`（大端 67452301...） | SHA-1 初始值 |
| `6a09e667 bb67ae85 3c6ef372 a54ff53a` | SHA-256 初始值 |
| 256 字节 0–255 排列的 S 盒 + 两重循环 | RC4（KSA+PRGA） |
| `A-Za-z0-9+/=` 查表 | Base64 |
| 巨大整数常量 + 模幂循环 | RSA/DH 手实现 |

Ghidra 侧：`find-bytes <bin> "63 7c 77 7b f2 6b 6f c5"` 一条命令定位；字符串指纹用 `search-strings`。

## 2. API → 语义对照（看到 import 就知道在干嘛）

| Windows CryptoAPI | CNG | OpenSSL | 语义 |
|---|---|---|---|
| CryptAcquireContext | BCryptOpenAlgorithmProvider | EVP_CIPHER_CTX_new | 初始化算法上下文 |
| CryptCreateHash | BCryptCreateHash | EVP_DigestInit_ex | 建 hash（常为密钥派生） |
| CryptDeriveKey | BCryptGenerateSymmetricKey | EVP_BytesToKey / PKCS5_PBKDF2 | 密钥派生 |
| CryptEncrypt / CryptDecrypt | BCryptEncrypt / BCryptDecrypt | EVP_EncryptUpdate / EVP_DecryptUpdate | 加解密主体 |
| CryptGenKey | BCryptGenerateKeyPair | EVP_PKEY_keygen | 生成密钥 |
| CryptImportKey | BCryptImportKey | EVP_PKEY_set1_RSA / d2i_* | 导入硬编码密钥 |
| CryptGenRandom | BCryptGenRandom | RAND_bytes | 随机源（看种子！） |

命中 `crypt*` import 时 triage 的 `suspicious_imports.crypto` 已自动报；本表用于认出后断语义。

## 3. 弱点清单（认出算法后找解密机会的决策点）

按命中率排序排查：

1. **硬编码密钥/IV**：xref 密钥缓冲区，常量直接可读 → 游戏结束
2. **弱 PRNG 种子**：`srand(time(NULL))` / `GetTickCount()` 做密钥种子 → 种子空间可爆破
3. **IV 复用 / 计数器复用**（CTR/CTR-like）：同一 keystream 异或两段已知明文即还原
4. **ECB 模式**：相同明文块 → 相同密文块，逐字节 oracle 可解
5. **密钥残留内存**：动态阶段 dump 进程内存搜密钥长度的高熵块
6. **自实现算法的结构缺陷**：自定义"加密"多为 XOR+移位+查表的组合，在变换关系和可逆条件成立时逐段求逆，按实际编码契约做局部检查

## 4. 混合加密结构（勒索软件典型，CTF 偶见）

per-file 对称密钥（AES/ChaCha20）加密数据 → RSA 公钥包裹对称密钥存文件头。
含义：**只逆出对称算法拿不到密钥**——密钥在文件头里被 RSA 包着；CTF 场景去找私钥是否硬编码在二进制里。

## 5. 识别完之后的交接

算法 + 密钥来源都清楚 → 求逆走 ghidra-static `references/ctf-patterns.md` §8 流水线（按可用证据独立检查模型与字节接口，不要求固定工具顺序）。认不出算法 → 用 oracle.py 喂已知明文观察中间态（`--break --dump`），从 I/O 形态反推（输出长度 = 输入长度 → 流密码；按 16 字节补齐 → 块密码）。
