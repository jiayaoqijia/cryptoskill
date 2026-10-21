#!/usr/bin/env python
r"""Local representation/contract checks, not a universal inversion gate.

Host-side tool (any Python 3.8+, stdlib only). Pure local checks - no daemon
needed. A mismatch is scoped to the declared format, not proof of a bad read,
bad algorithm or an impossible target. Base64 defaults retain the legacy
standard alphabet/required-padding contract; specify other contracts explicitly.

Usage:
  # pre-inversion gate on a constant
  python crypto_sanity.py check --algo hex    --constant "ab01cd..."
  python crypto_sanity.py check --algo base64 --constant "QUJD...==" [--custom-table]
  python crypto_sanity.py check --algo xor|rc4 --constant "<hex ciphertext>" --plain-len 21

  # post-inversion gate on the recovered plaintext
  python crypto_sanity.py check-result --text "BJD{...}" [--expect-regex 'BJD\{[^}]*\}']
  python crypto_sanity.py check-result --hex "28 00 00 00" [--allow-binary]

Exit codes: 0 checked, 1 malformed result representation, 2 contract mismatch
(or argparse usage error), 3 inconclusive for explicitly unknown padding.
All diagnostics are JSON. Existing successful fields and options are retained.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
import string
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

B64_CHARSET = set(string.ascii_letters + string.digits + "+/")


def normalize_hex(text: str) -> str:
    """Accept 'ab cd', '0xAB,0xCD', '\\x41\\x42', 'AB:CD' -> 'abcd...'."""
    t = text.strip()
    t = t.replace("\\x", "").replace("0x", "").replace("0X", "")
    return re.sub(r"[\s:,\-]+", "", t)


def gate_fired(title: str, facts: list[str], diagnosis: str) -> int:
    print(json.dumps({'ok': False, 'status': 'invalid', 'error': title,
                      'facts': facts, 'diagnosis': diagnosis,
                      'authority': 'declared local condition only; root cause and target acceptance unknown'}, ensure_ascii=False))
    return 2


def ok(report: dict) -> int:
    print(json.dumps({"ok": True, 'status': 'checked',
                      'authority': 'local checks only; not target acceptance', **report}, ensure_ascii=False))
    return 0


def check_base64(raw: str, alphabet='standard', padding='required', custom_table=False) -> dict:
    """Check only the declared alphabet/padding. Unknown contracts stay unknown."""
    if alphabet not in ('standard', 'url') or padding not in ('required', 'omitted', 'unknown'):
        raise ValueError('Unsupported Base64 contract')
    t = raw.strip()  # Legacy constant-input normalization, not a packet-input decoder.
    pad = len(t) - len(t.rstrip('='))
    body = t.rstrip('=')
    report = {'algo': 'base64', 'chars': len(t), 'padding': pad,
              'alphabet': 'custom' if custom_table else alphabet, 'padding_contract': padding,
              'authority': 'local format only; root cause and target acceptance unknown'}
    def invalid(reason):
        return {**report, 'ok': False, 'status': 'invalid', 'error': reason}
    if pad > 2 or '=' in body or len(body) % 4 == 1:
        return invalid('Invalid Base64 payload/padding shape')
    if pad and (len(t) % 4 or pad != (-len(body)) % 4):
        return invalid('Padding does not match payload length')
    if padding == 'required' and len(t) % 4:
        return invalid('Required-padding contract needs complete groups of four')
    if padding == 'omitted' and pad:
        return invalid('Omitted-padding contract does not permit =')
    charset = (B64_CHARSET - set('+/') | set('-_')) if alphabet == 'url' else B64_CHARSET
    if not custom_table and set(body) - charset:
        return invalid('Character outside the declared Base64 alphabet')
    if padding == 'unknown':
        return {**report, 'ok': False, 'status': 'inconclusive',
                'reason': 'Payload shape is plausible; protocol padding contract not established'}
    if custom_table:
        return {**report, 'ok': True, 'status': 'checked', 'validation_scope': 'shape_only',
                'decoded_bytes': len(body) * 6 // 8,
                'unverified': ['custom alphabet mapping', 'decoded bytes', 'target acceptance']}
    try:
        data = base64.b64decode(t + ('=' * ((-len(t)) % 4)),
                                altchars=b'-_' if alphabet == 'url' else None, validate=True)
    except (ValueError, binascii.Error) as error:
        return invalid(str(error))
    return {**report, 'ok': True, 'status': 'checked', 'validation_scope': 'alphabet_and_padding',
            'decoded_bytes': len(data), 'decoded_hex': data.hex()}


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
                              "该输入不满足当前十六进制字节表示；核对输入契约与来源，原因未确定。")
        if len(norm) % 2:
            return gate_fired("hex 常量长度为奇数",
                              [f"hex 字符数: {len(norm)}（奇数）",
                               f"常量: {norm!r}"],
                              "完整十六进制字节串需要偶数字符；整数文本、截断或其他表示需先明确契约，不直接判读数错误。")
        return ok({"algo": "hex", "hex_chars": len(norm), "bytes": len(norm) // 2})

    if algo == "base64":
        report = check_base64(raw, args.alphabet, args.padding, args.custom_table)
        print(json.dumps(report, ensure_ascii=False))
        return {'checked': 0, 'invalid': 2, 'inconclusive': 3}[report['status']]

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
                              "纯 XOR/RC4 逐字节保长；当前长度不等。检查切片、头部、编码、所声明长度和读数，不能仅据此确定原因。")
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
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            text = None
    else:
        text = args.text
        data = text.encode('utf-8')

    checked = text
    if args.strip_final_newline and checked is not None:
        checked = checked[:-2] if checked.endswith('\r\n') else checked[:-1] if checked.endswith('\n') else checked

    if args.require_printable and not args.allow_binary:
        bad = [(i, byte) for i, byte in enumerate(checked.encode('utf-8') if checked is not None else data)
               if byte < 32 or byte > 126]
        if bad:
            preview = ", ".join(f"[{i}]={c!r}" for i, c in bad[:8])
            return gate_fired("反推结果违反显式 ASCII 输入契约",
                              [f"结果: {text!r}", f"不可打印位置: {preview}"],
                              "仅不满足已声明的 ASCII 契约；核对契约、编码、模型和数据，不能确定根因。")
    if args.expect_regex and checked is None:
        return gate_fired('结果不是可按 UTF-8 检查的文本', [], '保留原始字节；不能用替换字符冒充正则检查。')
    if args.expect_regex and not re.fullmatch(args.expect_regex, checked):
        return gate_fired("反推结果不匹配期望格式",
                          [f"结果: {text!r}", f"期望: /{args.expect_regex}/"],
                          "与显式输入契约不符；检查契约、编码、padding、模型与读数。")
    return ok({"result": text, 'result_hex': data.hex(), 'newline_stripped_for_check': args.strip_final_newline,
               "printable_checked": args.require_printable and not args.allow_binary,
               "regex_checked": bool(args.expect_regex)})


def main() -> int:
    ap = argparse.ArgumentParser(description="Local format checks scoped to declared contracts")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="常量表示与显式格式检查")
    p.add_argument("--algo", required=True, choices=["hex", "base64", "xor", "rc4"])
    p.add_argument("--constant", required=True,
                   help="hex 文本（xor/rc4 传密文 hex；base64 传文本）")
    p.add_argument("--plain-len", type=int, default=None,
                   help="xor/rc4：声称的明文长度（流密码必须等长）")
    p.add_argument("--custom-table", action="store_true",
                   help="base64：仅检查形状，不验证自定义字母表映射或解码字节")
    p.add_argument('--alphabet', choices=['standard', 'url'], default='standard', help='Base64 alphabet; legacy default: standard')
    p.add_argument('--padding', choices=['required', 'omitted', 'unknown'], default='required', help='Base64 padding contract; unknown exits 3')
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("check-result", help="结果表示与显式输入契约检查")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--hex")
    p.add_argument("--expect-regex", help="结果必须 fullmatch 该正则")
    p.add_argument("--require-printable", action="store_true", help="explicit ASCII input contract")
    p.add_argument("--allow-binary", action="store_true",
                   help="结果是二进制格式时跳过可打印检查")
    p.add_argument('--strip-final-newline', action='store_true', help='Explicitly remove one terminal LF/CRLF for text checks; raw bytes remain in result_hex')
    p.set_defaults(fn=cmd_check_result)

    args = ap.parse_args()
    if getattr(args, 'plain_len', None) is not None and args.plain_len < 0:
        ap.error('--plain-len must be nonnegative')
    if getattr(args, 'expect_regex', None):
        try:
            re.compile(args.expect_regex)
        except re.error as error:
            ap.error('Invalid --expect-regex: ' + str(error))
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
