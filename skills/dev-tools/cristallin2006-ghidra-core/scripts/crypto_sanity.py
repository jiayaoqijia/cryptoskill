#!/usr/bin/env python
r"""crypto_sanity.py - mechanical pre/post-inversion sanity gate (Iron Rule 9).

Host-side tool (any Python 3.8+, stdlib only). Pure local checks - no daemon
needed. This is the GATE between "I read a constant" and "I start inverting":
a constant whose length can never satisfy its own purpose (odd-length hex,
base64 not a multiple of 4, stream-cipher ciphertext longer than the claimed
plaintext) means the READING is wrong (cross-buffer misread / renderer
swallowed a leading zero), not that the program is broken. Entering the
inversion with a suspect reading is forbidden (Iron Rule 9).

Usage:
  # pre-inversion gate on a constant
  python crypto_sanity.py check --algo hex    --constant "ab01cd..."
  python crypto_sanity.py check --algo base64 --constant "QUJD...==" [--custom-table]
  python crypto_sanity.py check --algo xor|rc4 --constant "<hex ciphertext>" --plain-len 21

  # post-inversion gate on the recovered plaintext
  python crypto_sanity.py check-result --text "BJD{...}" [--expect-regex 'BJD\{[^}]*\}']
  python crypto_sanity.py check-result --hex "28 00 00 00" [--allow-binary]

Exit codes: 0 pass, 1 usage error, 2 GATE FIRED (read stdout, do not invert).
"""
from __future__ import annotations

import argparse
import json
import re
import string
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

PRINTABLE = set(string.printable) - set("\t\n\r\x0b\x0c")
B64_CHARSET = set(string.ascii_letters + string.digits + "+/")


def normalize_hex(text: str) -> str:
    """Accept 'ab cd', '0xAB,0xCD', '\\x41\\x42', 'AB:CD' -> 'abcd...'."""
    t = text.strip()
    t = t.replace("\\x", "").replace("0x", "").replace("0X", "")
    return re.sub(r"[\s:,\-]+", "", t)


def gate_fired(title: str, facts: list[str], diagnosis: str) -> int:
    print(f"[求逆闸门 · 铁律9] {title}")
    print("──── 事实 ────")
    for f in facts:
        print(f"  · {f}")
    print("──── 诊断 ────")
    print(f"  {diagnosis}")
    print("──── 强制动作 ────")
    print("  1. 用 read_views.py 重取常量：三视图 + --expect-len 对照变量声明长度")
    print("  2. 若重取后仍不合法 → 缓冲区归属错误：按 disp 区间重新归类 imm-store，")
    print("     相邻变量的写入不许拼进同一常量（铁律 9）")
    print("  3. 闸门未过，禁止进入求逆；更禁止据此宣布「校验不可满足」")
    return 2


def ok(report: dict) -> int:
    print(json.dumps({"ok": True, **report}, ensure_ascii=False))
    return 0


def cmd_check(args) -> int:
    algo = args.algo
    raw = args.constant

    if algo == "hex":
        norm = normalize_hex(raw)
        bad = [c for c in norm if c not in string.hexdigits]
        if bad:
            return gate_fired("hex 常量含非 hex 字符",
                              [f"常量（规范化后）: {norm!r}",
                               f"非法字符: {sorted(set(bad))}"],
                              "hex 文本里混入杂质 = 复制/渲染污染。常量必须来自 "
                              "read_views.py 的 fromhex-ready 视图，不是终端手工转录。")
        if len(norm) % 2:
            return gate_fired("hex 常量长度为奇数",
                              [f"hex 字符数: {len(norm)}（奇数）",
                               f"常量: {norm!r}"],
                              "奇数长度不可能是 hex dump——典型原因：渲染器吞了前导 0 "
                              "（0x01 显示成 '1'），或跨缓冲区误读。用 read_views.py "
                              "--expect-hex 对照渲染文本找第一个分叉字节。")
        return ok({"algo": "hex", "hex_chars": len(norm), "bytes": len(norm) // 2})

    if algo == "base64":
        t = raw.strip()
        facts = [f"长度: {len(t)}", f"常量: {t!r}"]
        if len(t) % 4:
            return gate_fired("base64 常量长度不是 4 的倍数", facts,
                              f"{len(t)} % 4 = {len(t) % 4}——base64 输出长度永远是 4 的倍数，"
                              "这个常量与它声称的用途永不相等。第一嫌疑人是读数"
                              "（跨缓冲区误读/吞前导 0），不是程序写坏了。")
        pad = len(t) - len(t.rstrip("="))
        if pad > 2 or "=" in t.rstrip("="):
            return gate_fired("base64 填充非法", facts + [f"'=' 数: {pad}"],
                              "'=' 只能出现在末尾且最多 2 个。")
        if not args.custom_table:
            bad = sorted(set(t) - B64_CHARSET - {"="})
            if bad:
                return gate_fired("base64 常量含表外字符", facts + [f"表外字符: {bad}"],
                                  "标准表装不下这些字符。若题目用换表 base64，确认换表后"
                                  "加 --custom-table 重查；否则 = 读数错误。")
        decoded = len(t) // 4 * 3 - pad
        return ok({"algo": "base64", "chars": len(t), "padding": pad,
                   "decoded_bytes": decoded})

    # xor / rc4: stream transforms preserve length exactly
    norm = normalize_hex(raw)
    if not norm or len(norm) % 2 or any(c not in string.hexdigits for c in norm):
        return gate_fired(f"{algo} 密文不是合法 hex",
                          [f"规范化后: {norm!r}"],
                          "流密码密文必须能按字节读出。先过 hex 检查（--algo hex）。")
    n = len(norm) // 2
    facts = [f"密文: {n} 字节"]
    if args.plain_len is not None:
        facts.append(f"声称明文长度: {args.plain_len}")
        if n != args.plain_len:
            return gate_fired(f"{algo} 密文长度 ≠ 明文长度", facts,
                              "XOR/RC4 是流变换，逐字节保长——密文与明文长度不等 = "
                              "常量读错了（多为跨缓冲区误读）。回 read_views.py 重取，"
                              "并按 disp 区间核对缓冲区归属（铁律 9）。")
    return ok({"algo": algo, "cipher_bytes": n,
               "plain_len_checked": args.plain_len is not None})


def cmd_check_result(args) -> int:
    if args.hex is not None:
        norm = normalize_hex(args.hex)
        try:
            data = bytes.fromhex(norm)
        except ValueError:
            print(json.dumps({"ok": False, "error": "--hex 不是合法 hex"},
                             ensure_ascii=False))
            return 1
        text = data.decode("utf-8", errors="replace")
    else:
        text = args.text

    if args.require_printable and not args.allow_binary:
        core = text.rstrip("\n")
        bad = [(i, c) for i, c in enumerate(core) if c not in PRINTABLE]
        if bad:
            preview = ", ".join(f"[{i}]={c!r}" for i, c in bad[:8])
            return gate_fired("反推结果违反显式 ASCII 输入契约",
                              [f"结果: {text!r}", f"不可打印位置: {preview}"],
                              "当前显式 ASCII 输入契约要求可打印；请检查编码、padding、模型或常量"
                              "错误的高置信信号（复盘 E4）。禁止宣布「校验不可满足」——"
                              "否定性结论的门槛是先用已知输入正向复现整条流水线"
                              "（ctf-patterns.md §8），做到了再谈求逆。")
    if args.expect_regex and not re.fullmatch(args.expect_regex, text.rstrip("\n")):
        return gate_fired("反推结果不匹配期望格式",
                          [f"结果: {text!r}", f"期望: /{args.expect_regex}/"],
                          "与显式输入契约不符；检查契约、编码、padding、模型与读数。")
    return ok({"result": text, "printable_checked": args.require_printable and not args.allow_binary,
               "regex_checked": bool(args.expect_regex)})


def main() -> int:
    ap = argparse.ArgumentParser(description="Iron Rule 9 pre/post-inversion sanity gate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="求逆前：常量合法性闸门")
    p.add_argument("--algo", required=True, choices=["hex", "base64", "xor", "rc4"])
    p.add_argument("--constant", required=True,
                   help="hex 文本（xor/rc4 传密文 hex；base64 传文本）")
    p.add_argument("--plain-len", type=int, default=None,
                   help="xor/rc4：声称的明文长度（流密码必须等长）")
    p.add_argument("--custom-table", action="store_true",
                   help="base64：题目用换表时跳过字符集检查")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("check-result", help="求逆后：结果合理性闸门")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--hex")
    p.add_argument("--expect-regex", help="结果必须 fullmatch 该正则")
    p.add_argument("--require-printable", action="store_true", help="explicit ASCII input contract")
    p.add_argument("--allow-binary", action="store_true",
                   help="结果是二进制格式时跳过可打印检查")
    p.set_defaults(fn=cmd_check_result)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
