#!/usr/bin/env python
r"""xor_scan.py - mechanical transform search over a blob (Iron Rule: fix the
ad-hoc XOR hunt into a tool).

Host-side tool (any Python 3.8+, stdlib only). Pure local byte crunching - no
daemon needed. Motivation (case-F retro): the analyst hand-wrote 4 throwaway
scripts on site (entropy profile, histogram, cosine similarity, single-byte
XOR sweep) to find that the payload at .data+0xc0 was XOR 0x77. That sweep is
a mandatory step for any multi-layer payload challenge and belongs in a tool.

What it does:
  1. Single-byte XOR sweep (0x01..0xFF). For each key: printable ratio,
     known-magic hits (MZ+PE\0\0 at start, \x7fELF, PK\x03\x04, UPX!, flag
     regex `[A-Za-z0-9_]+\{[^}]{4,}\}`, x86/x86-64 code prologues), entropy.
  2. --rolling N: repeating-key XOR with key length N. Per-lane frequency
     analysis picks each key byte independently (budget: 255 * len ops, no
     full-space brute force), then the assembled key is scored like any
     other candidate.
  3. --two-byte-add: optional single-byte ADD/SUB transform sweep.
  4. Candidates are ranked by a composite score (magic hit >> flag regex >>
     prologue >> printable-ratio gain). Top 10 printed with evidence.
  5. --dump <key> writes the decoded blob for one key to a file
     (--out picks the path). Key spec: `0x77` / `xor:0x77` / `add:0x20` /
     `sub:0x20` / `roll:0xAA,0xBB,0xCC`.

Usage:
  python xor_scan.py <blob> [--json out.json]
  python xor_scan.py payload.bin --rolling 8 --two-byte-add
  python xor_scan.py payload.bin --dump 0x77 --out payload.pe

Exit codes: 0 scan completed, 1 usage error (missing file / bad key spec).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

PRINTABLE = set(range(0x20, 0x7F)) | {0x09, 0x0A, 0x0D}
FLAG_RE = re.compile(rb"[A-Za-z0-9_]+\{[^}\r\n]{4,}\}")
PROLOGUES = [
    (b"\x55\x48\x89\xe5", "x86-64 序言 55 48 89 e5"),
    (b"\x55\x8b\xec", "x86 序言 55 8b ec"),
]
WEAK_SCORE = 40.0


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts if c)


def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    return sum(1 for b in data if b in PRINTABLE) / len(data)


def find_evidence(data: bytes, raw_ratio: float) -> tuple[float, list[str]]:
    """Score a decoded blob; return (score, evidence lines)."""
    score = 0.0
    ev = []

    if data[:2] == b"MZ":
        pe_off = data.find(b"PE\x00\x00", 0, 1024)
        if pe_off > 0:
            score += 80
            ev.append(f"PE 可执行文件头：MZ@0 + PE\\0\\0@0x{pe_off:x}（强命中）")
        else:
            score += 10
            ev.append("MZ@0（缺 PE\\0\\0，弱）")
    if data[:4] == b"\x7fELF":
        score += 70
        ev.append("ELF 魔数 @0（强命中）")
    if data[:4] == b"PK\x03\x04":
        score += 70
        ev.append("ZIP/PK 魔数 @0（强命中）")

    upx = data.find(b"UPX!")
    if 0 <= upx < 65536:
        score += 25
        ev.append(f"UPX! 魔数 @0x{upx:x}（UPX 壳线索）")
    if data[:2] != b"MZ":
        off = data.find(b"MZ")
        if 0 <= off < 4096 and data.find(b"PE\x00\x00", off, off + 1024) > 0:
            score += 25
            ev.append(f"内嵌 PE：MZ@0x{off:x}（非起点）")

    for sig, name in PROLOGUES:
        off = data.find(sig)
        if off >= 0:
            score += 15
            ev.append(f"{name} @0x{off:x}")
            break

    m = FLAG_RE.search(data)
    if m:
        raw = m.group(0)
        inner = raw[raw.index(b"{") + 1:-1]
        printable = all(b in PRINTABLE for b in raw)
        if printable and len(inner) <= 64:
            text = raw[:120].decode("ascii", errors="replace")
            score += 100
            ev.append(f"flag 正则命中 @0x{m.start():x}: {text}")
        else:
            # spec regex `[^}]{4,}` also matches binary runs; only count as noise
            score += 5
            ev.append(f"flag 正则弱命中 @0x{m.start():x}（内容不可打印/超长，按噪声处理）")

    ratio = printable_ratio(data)
    gain = max(0.0, ratio - raw_ratio)
    if gain > 0:
        score += 30 * gain
        ev.append(f"可打印率 {ratio:.1%}（原始 {raw_ratio:.1%}，+{gain:.1%}）")

    return score, ev


def xor_bytes(data: bytes, key: bytes) -> bytes:
    klen = len(key)
    if klen == 1:
        k = key[0]
        return bytes(b ^ k for b in data)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))


def add_bytes(data: bytes, delta: int, sign: int) -> bytes:
    return bytes((b + sign * delta) & 0xFF for b in data)


def lane_weight(b: int) -> float:
    if b == 0x20:
        return 6.0
    if 0x61 <= b <= 0x7A:   # a-z: English plaintext is mostly lowercase
        return 3.0
    if 0x41 <= b <= 0x5A:   # A-Z
        return 2.0
    if 0x30 <= b <= 0x39:   # digits
        return 1.0
    if b in b",.'\"!?{}_-\n\r\t":
        return 0.5
    if b in PRINTABLE:
        return 0.2
    return -8.0


def rolling_key_guess(data: bytes, klen: int) -> bytes:
    """Per-lane frequency analysis (cryptopals #6 style): pick each key byte
    maximizing an English-text weight over the decoded lane. Heuristic, tuned
    for text-ish payloads; binary payloads need the magic evidence instead."""
    key = bytearray()
    for lane in range(klen):
        segment = data[lane::klen]
        best_k, best_w = 1, None
        for k in range(1, 256):
            w = 0.0
            for b in segment:
                w += lane_weight(b ^ k)
            if best_w is None or w > best_w:
                best_w, best_k = w, k
        key.append(best_k)
    return bytes(key)


def parse_dump_key(spec: str) -> tuple[str, bytes]:
    s = spec.strip().lower()
    for prefix in ("xor:", "add:", "sub:"):
        if s.startswith(prefix):
            op = prefix[:-1]
            s = s[len(prefix):]
            break
    else:
        op = "xor"
    if op == "xor" and s.startswith("roll:"):
        op = "roll"
        s = s[len("roll:"):]
    if s.startswith("roll:"):
        op = "roll"
        s = s[len("roll:"):]
    if op == "roll":
        parts = [p for p in re.split(r"[,\s]+", s) if p]
        try:
            key = bytes(int(p, 16) if p.startswith("0x") else int(p) for p in parts)
        except ValueError:
            raise SystemExit(f"[错误] 无法解析滚动密钥: {spec!r}（示例 roll:0xAA,0xBB）")
        if not key:
            raise SystemExit(f"[错误] 滚动密钥为空: {spec!r}")
        return op, key
    try:
        v = int(s, 16) if s.startswith("0x") else int(s)
    except ValueError:
        raise SystemExit(f"[错误] 无法解析 key: {spec!r}（示例 0x77 / add:0x20 / sub:0x20 / roll:0xAA,0xBB）")
    if not 0 <= v <= 255:
        raise SystemExit(f"[错误] key 超出单字节范围: {spec!r}")
    return op, bytes([v])


def apply_transform(data: bytes, op: str, key: bytes) -> bytes:
    if op in ("xor", "roll"):
        return xor_bytes(data, key)
    if op == "add":
        return add_bytes(data, key[0], +1)
    if op == "sub":
        return add_bytes(data, key[0], -1)
    raise SystemExit(f"[错误] 未知变换: {op}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="对 blob 做机械变换搜索：单字节 XOR 全扫 + 可选滚动密钥/ADD/SUB，"
                    "按 magic/flag/可打印率评分排序")
    ap.add_argument("blob", help="待分析的载荷文件")
    ap.add_argument("--rolling", type=int, metavar="N", default=None,
                    help="滚动/重复密钥 XOR，key 长度 N（逐车道频率分析，不做全空间爆破）")
    ap.add_argument("--two-byte-add", action="store_true",
                    help="追加单字节 ADD/SUB 变换扫")
    ap.add_argument("--dump", metavar="KEY", default=None,
                    help="把指定 key 的解密结果写文件（0x77 / xor:0x77 / add:0x20 / sub:0x20 / roll:0xAA,0xBB）")
    ap.add_argument("--out", default=None, help="--dump 的输出路径（默认 <blob>.dump）")
    ap.add_argument("--json", dest="json_out", default=None, help="把完整报告写入 JSON 文件")
    ap.add_argument("--top", type=int, default=10, help="打印前 N 个候选（默认 10）")
    args = ap.parse_args()

    try:
        with open(args.blob, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"[错误] 无法读取 blob: {e}", file=sys.stderr)
        return 1
    if not data:
        print("[错误] blob 为空", file=sys.stderr)
        return 1

    if args.dump:
        op, key = parse_dump_key(args.dump)
        decoded = apply_transform(data, op, key)
        out_path = args.out or (args.blob + ".dump")
        with open(out_path, "wb") as f:
            f.write(decoded)
        score, ev = find_evidence(decoded, printable_ratio(data))
        print(f"[xor_scan] {op} {key.hex()} -> {out_path}（{len(decoded)} 字节，评分 {score:.1f}）")
        for line in ev:
            print(f"  · {line}")
        return 0

    raw_ratio = printable_ratio(data)
    raw_entropy = entropy(data)
    print(f"[xor_scan] blob: {args.blob}（{len(data)} 字节，熵 {raw_entropy:.2f} bits/byte，"
          f"可打印率 {raw_ratio:.1%}）")

    candidates = []

    for k in range(1, 256):
        decoded = xor_bytes(data, bytes([k]))
        score, ev = find_evidence(decoded, raw_ratio)
        if score > 0:
            candidates.append({
                "transform": "xor", "key": f"0x{k:02x}", "key_int": k,
                "score": round(score, 2), "entropy": round(entropy(decoded), 2),
                "printable": round(printable_ratio(decoded), 4), "evidence": ev,
            })

    if args.two_byte_add:
        for d in range(1, 256):
            for op, sign in (("add", +1), ("sub", -1)):
                decoded = add_bytes(data, d, sign)
                score, ev = find_evidence(decoded, raw_ratio)
                if score > 0:
                    candidates.append({
                        "transform": op, "key": f"0x{d:02x}", "key_int": d,
                        "score": round(score, 2), "entropy": round(entropy(decoded), 2),
                        "printable": round(printable_ratio(decoded), 4), "evidence": ev,
                    })

    if args.rolling:
        if args.rolling < 2:
            print("[错误] --rolling N 需要 N >= 2", file=sys.stderr)
            return 1
        key = rolling_key_guess(data, args.rolling)
        decoded = xor_bytes(data, key)
        score, ev = find_evidence(decoded, raw_ratio)
        candidates.append({
            "transform": "roll", "key": ",".join(f"0x{b:02x}" for b in key),
            "key_len": args.rolling, "score": round(score, 2),
            "entropy": round(entropy(decoded), 2),
            "printable": round(printable_ratio(decoded), 4),
            "evidence": ["逐车道频率分析猜测的滚动密钥"] + ev,
        })

    candidates.sort(key=lambda c: -c["score"])
    top = candidates[:args.top]

    print()
    if top:
        print(f"════ Top {len(top)} 候选 ════")
        for rank, c in enumerate(top, 1):
            print(f"  #{rank}  {c['transform']} key={c['key']}  评分 {c['score']:.1f}  "
                  f"熵 {c['entropy']:.2f}  可打印率 {c['printable']:.1%}")
            for line in c["evidence"]:
                print(f"      · {line}")
    else:
        print("════ 无任何候选得分 > 0 ════")

    print()
    best = top[0]["score"] if top else 0.0
    if best >= WEAK_SCORE:
        print(f"[结论] Top1 评分 {best:.1f} >= {WEAK_SCORE:.0f}，存在强候选——"
              f"用 --dump {top[0]['key'].split(',')[0] if top[0]['transform'] != 'roll' else 'roll:' + top[0]['key']} 解密落盘后人工复核。")
    else:
        print(f"[结论] Top1 评分仅 {best:.1f} < {WEAK_SCORE:.0f}，无强结论——"
              "载荷大概率不是单字节 XOR/ADD/SUB。考虑：多字节滚动密钥（--rolling N）、"
              "分段异或、先 Base 系解码再异或、或根本不是异或族变换。"
              "禁止在低分候选上宣布「解不出来」——先换变换族再谈（评分只是排序线索）。")

    report = {
        "blob": args.blob, "size": len(data),
        "raw_entropy": round(raw_entropy, 2), "raw_printable": round(raw_ratio, 4),
        "rolling": args.rolling, "two_byte_add": args.two_byte_add,
        "candidates": candidates,
    }
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[xor_scan] JSON 报告已写入: {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
