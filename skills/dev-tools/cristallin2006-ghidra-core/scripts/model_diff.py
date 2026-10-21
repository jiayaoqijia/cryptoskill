#!/usr/bin/env python
"""Compare a local model command and oracle on a declared sampled input distribution.

--model and --oracle receive stdin; --input-gen hex:N / dec / ascii:N,
--n, --seed and --json control sampling and output. Commands execute only when
explicitly supplied. Fingerprints are descriptive heuristics, not root-cause
proof: interface, model, algorithm and environment errors can share a pattern.
Exit 0: sampled outputs match; 2: divergence; 3: command/setup failure.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from collections import Counter

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

TIMEOUT = 10  # 每组输入的子进程超时（秒）

VERDICT_INTERFACE = ("该结构提示核对接口、搬运或位宽；也可能来自算法、模型或组合错误。"
                     "用输入输出解析、半字和偏移对照区分解释，指纹本身不确定根因。")
VERDICT_LENGTH = ("疑似接口错（framing）：先核对编码（hex vs raw）、换行、padding、"
                  "长度前缀；算法、模型和初始状态错误也可能改变长度，不能排除。")
VERDICT_ALGORITHM = ("疑似算法错/模型整体错误：差异无搬运规律，回到算法层面对照"
                     "；也保留未被当前启发式识别的接口或环境差异，根因未确定。")


def gen_input(spec: str, rng: random.Random) -> bytes:
    parts = spec.split(":")
    kind = parts[0].lower()
    try:
        if kind == "hex":
            n = int(parts[1]) if len(parts) > 1 else 32
            return bytes(rng.randrange(256) for _ in range(n))
        if kind == "dec":
            lo = int(parts[1]) if len(parts) > 2 else 0
            hi = int(parts[2]) if len(parts) > 2 else 2**31 - 1
            return (str(rng.randint(lo, hi)) + "\n").encode()
        if kind == "ascii":
            n = int(parts[1]) if len(parts) > 1 else 16
            return bytes(rng.randrange(0x20, 0x7F) for _ in range(n))
    except (ValueError, IndexError):
        pass
    raise ValueError(f"未知 --input-gen 规格: {spec!r}"
                     "（支持 hex:N / dec[:min:max] / ascii:N）")


def run_cmd(cmd: str, data: bytes) -> tuple[str, bytes, bytes]:
    """-> (status, stdout, stderr); status: ok|timeout|spawn-error|nonzero-exit"""
    try:
        p = subprocess.run(cmd, input=data, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return ("timeout", b"", b"")
    except OSError as ex:
        return ("spawn-error", b"", str(ex).encode())
    if p.returncode != 0:
        return ("nonzero-exit", p.stdout, p.stderr)
    return ("ok", p.stdout, p.stderr)


def _swap_nib(b: int) -> int:
    return ((b & 0x0F) << 4) | (b >> 4)


def _word_fp(mo: bytes, om: bytes, size: int) -> tuple[str, str] | None:
    """按 size 字节块检查宽度级指纹（16/32 位半字级规律）；命中返回
    (指纹名, 细节)，否则 None。判词一律 VERDICT_INTERFACE——宽度级规律
    模式只描述观测到的形状，不能排除算法或其他根因。"""
    n = len(mo)
    if size < 2 or n % size != 0:
        return None
    h = size // 2
    words_m = [mo[i:i + size] for i in range(0, n, size)]
    words_o = [om[i:i + size] for i in range(0, n, size)]
    pairs = list(zip(words_m, words_o))
    # ① 整块高低半互换（真·半字交换，如 4 字节块 d[2:4]+d[0:2]）
    if all(mw == ow[h:] + ow[:h] for mw, ow in pairs):
        return (f"高低半块交换（按 {size} 字节块）",
                f"model 输出 = oracle 输出按 {size} 字节块高低 {h} 字节互换，"
                f"典型的 {size * 4} 位半字拼装写反（移位方向/字段顺序错）")
    # ② 低半块全对 + 高半块差异恒定（历史样本中的一种形状）
    if all(mw[:h] == ow[:h] for mw, ow in pairs):
        per_pos_xor = [{(mw[h + p] ^ ow[h + p]) for mw, ow in pairs}
                       for p in range(h)]
        per_pos_add = [{(mw[h + p] - ow[h + p]) % 256 for mw, ow in pairs}
                       for p in range(h)]
        if all(len(s) == 1 for s in per_pos_xor):
            ds = [s.pop() for s in per_pos_xor]
            if any(ds):
                return (f"低半块全对+高半块 XOR 恒定（按 {size} 字节块）",
                        f"低 {h} 字节全部一致，高 {h} 字节逐位 XOR 差恒定为 "
                        f"{' '.join('0x%02x' % d for d in ds)}——接口/搬运写错的"
                        "形状线索，查移位/掩码/字段位宽，"
                        "第一嫌疑人是 harness/连线")
        if all(len(s) == 1 for s in per_pos_add):
            ds = [s.pop() for s in per_pos_add]
            if any(ds):
                return (f"低半块全对+高半块加法恒定（按 {size} 字节块）",
                        f"低 {h} 字节全部一致，高 {h} 字节逐字节差恒定为 "
                        f"{' '.join('+0x%02x' % d for d in ds)}（mod 256）——"
                        "可能的接口/搬运线索，查常量/基址/位宽")
    # ③ 单侧半块恒为常量（需 ≥2 个块，单块时"恒为常量"无意义）
    if len(pairs) >= 2:
        for side, sl in (("低", slice(0, h)), ("高", slice(h, size))):
            vals = {mw[sl] for mw in words_m}
            if len(vals) == 1 and any(mw[sl] != ow[sl] for mw, ow in pairs):
                c = vals.pop()
                return (f"{side}半块恒为常量（按 {size} 字节块）",
                        f"model 每 {size} 字节块的{side} {h} 字节恒为 "
                        f"{c.hex(' ')}，疑似常量写死/掩码错——接口/搬运问题")
    return None


def fingerprint(model_out: bytes, oracle_out: bytes) -> tuple[str, str, str]:
    """-> (指纹名, 细节, 判词)。判词优先级：宽度级规律 > 字节级搬运 > 无规律。"""
    if len(model_out) != len(oracle_out):
        return ("长度不一致",
                f"model={len(model_out)}B vs oracle={len(oracle_out)}B",
                VERDICT_LENGTH)
    n = len(model_out)
    diffs = [i for i in range(n) if model_out[i] != oracle_out[i]]
    # 按既有形状优先级分类；分类不构成根因排除。
    for size in (4, 2):
        hit = _word_fp(model_out, oracle_out, size)
        if hit is not None:
            return (hit[0], hit[1], VERDICT_INTERFACE)
    # 字节级（nibble 粒度）
    if all((model_out[i] & 0x0F) == (oracle_out[i] & 0x0F) for i in range(n)):
        bad = next(i for i in range(n) if model_out[i] != oracle_out[i])
        return ("低半字节全对（低 nibble）",
                f"{len(diffs)}/{n} 字节高 nibble 不同，低 nibble 全部一致"
                f"（首个 offset {bad}: model=0x{model_out[bad]:02x} "
                f"oracle=0x{oracle_out[bad]:02x}）",
                VERDICT_INTERFACE)
    if all(model_out[i] == _swap_nib(oracle_out[i]) for i in range(n)):
        return ("高低半字节交换（nibble swap）",
                f"model 输出 = oracle 输出逐字节 nibble 交换（{len(diffs)}/{n} 字节），"
                "典型的 hex 解码/位拼接写反",
                VERDICT_INTERFACE)
    if len(diffs) == 1:
        i = diffs[0]
        return ("单常量差",
                f"仅 offset {i} 不同: model=0x{model_out[i]:02x} "
                f"oracle=0x{oracle_out[i]:02x}",
                VERDICT_INTERFACE)
    deltas = {(model_out[i] - oracle_out[i]) % 256 for i in range(n)}
    if len(deltas) == 1:
        d = deltas.pop()
        return ("全体偏移固定值",
                f"所有字节 model = oracle + 0x{d:02x}（mod 256）",
                VERDICT_INTERFACE)
    return ("完全无关",
            f"{len(diffs)}/{n} 字节不同且无搬运规律",
            VERDICT_ALGORITHM)


def hexs(b: bytes, limit: int = 64) -> str:
    s = b[:limit].hex(" ")
    return s + (f" …(+{len(b) - limit}B)" if len(b) > limit else "")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="模型 vs oracle 对拍；分歧指纹只提供排查线索，不确定根因")
    ap.add_argument("--model", required=True,
                    help="我方模型实现命令（stdin 喂输入/stdout 出结果）")
    ap.add_argument("--oracle", required=True, help="真实 oracle 命令（同约定）")
    ap.add_argument("--input-gen", required=True,
                    help="hex:N（N 随机字节）| dec[:min:max]（随机整数行）| "
                         "ascii:N（N 随机可打印字符）")
    ap.add_argument("--n", type=int, default=200, help="投喂组数（默认 200）")
    ap.add_argument("--seed", type=int, default=1, help="确定性 seed（默认 1）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    mismatches = []
    errors = []
    for i in range(args.n):
        data = gen_input(args.input_gen, rng)
        om_status, om_out, om_err = run_cmd(args.oracle, data)
        mo_status, mo_out, mo_err = run_cmd(args.model, data)
        if om_status != "ok" or mo_status != "ok":
            errors.append({"index": i, "input_hex": data.hex(),
                           "oracle_status": om_status,
                           "model_status": mo_status,
                           "oracle_stderr": om_err[:200].decode("utf-8", "replace"),
                           "model_stderr": mo_err[:200].decode("utf-8", "replace")})
            continue
        if mo_out != om_out:
            fp, detail, verdict = fingerprint(mo_out, om_out)
            mismatches.append({"index": i, "input_hex": data.hex(),
                               "oracle_hex": om_out.hex(),
                               "model_hex": mo_out.hex(),
                               "fingerprint": fp, "detail": detail,
                               "verdict": verdict})

    if errors:
        result = {"ok": False, "error": "子进程运行错误（命令本身有问题，先修命令）",
                  "runs": args.n, "run_errors": len(errors),
                  "first_error": errors[0]}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"[model_diff] 命令错误：{len(errors)}/{args.n} 组输入子进程非正常结束")
            e = errors[0]
            print(f"  首例 #{e['index']}: oracle={e['oracle_status']} "
                  f"model={e['model_status']}")
            print(f"  oracle stderr: {e['oracle_stderr']!r}")
            print(f"  model  stderr: {e['model_stderr']!r}")
            print("先让两条命令单独跑通再对拍。")
        return 3

    fp_counter = Counter(m["fingerprint"] for m in mismatches)
    result = {
        "ok": not mismatches, "runs": args.n, "seed": args.seed,
        "input_gen": args.input_gen,
        "mismatches": len(mismatches),
        "mismatch_rate": len(mismatches) / max(args.n, 1),
        "fingerprint_histogram": dict(fp_counter),
        "first_divergence": mismatches[0] if mismatches else None,
        "diagnostic_scope": "sampled output patterns only; root cause undetermined",
        "root_cause": "undetermined" if mismatches else None,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[model_diff] n={args.n} seed={args.seed} gen={args.input_gen}")
        print(f"  oracle: {args.oracle}")
        print(f"  model : {args.model}")
        if not mismatches:
            print(f"结果: {args.n}/{args.n} 全部一致——模型与 oracle 在该输入分布下逐字节相同")
        else:
            m = mismatches[0]
            print(f"首个分歧（第 {m['index']} 组）:")
            print(f"  input : {hexs(bytes.fromhex(m['input_hex']))}")
            print(f"  oracle: {hexs(bytes.fromhex(m['oracle_hex']))}")
            print(f"  model : {hexs(bytes.fromhex(m['model_hex']))}")
            print(f"  指纹: {m['fingerprint']} —— {m['detail']}")
            print(f"  判词: {m['verdict']}")
            rate = result["mismatch_rate"] * 100
            print(f"统计: mismatch {len(mismatches)}/{args.n}（{rate:.1f}%）")
            for fp, cnt in fp_counter.most_common():
                print(f"  {fp} × {cnt}")
    return 2 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
