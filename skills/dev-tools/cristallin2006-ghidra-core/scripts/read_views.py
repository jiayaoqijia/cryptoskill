#!/usr/bin/env python
"""read_views.py - authoritative multi-view byte reader (Iron Rule 8).

Host-side tool (any Python 3, stdlib only). Fetches raw bytes through the
rpc daemon (`read-bytes`) and renders every view you might need, so that
the authoritative reading of a key constant NEVER comes from hand-copied
terminal hex or a decompiler's string rendering.

Usage:
  python read_views.py <binary> <addr> <len> [--expect-len N] [--expect-hex HEX] [--json]

Views rendered:
  hexdump   canonical offset/hex/ascii dump (16 B/line)
  hex       fromhex-ready lowercase hex WITH EXPLICIT BYTE COUNT
  ascii     printable-substitution view
  cstr      NUL-terminated interpretation from <addr>, with its length

Consistency checks (exit 2 on failure - treat like the ledger breaker):
  --expect-len N     declared/pseudocode length vs bytes actually read
                     vs cstr length - any disagreement = MISMATCH
  --expect-hex HEX   hex text copied from a decompiler rendering vs the
                     real bytes - catches the classic "renderer swallows
                     leading zeros" (IDA shows 0x01 as '1') with a
                     byte-exact first-diff offset

When a check fails the FIRST suspect is the reading, not the program
(Iron Rule 8). Conclusion "this logic is broken/inverted" is forbidden
until the reading itself is verified with this tool.
"""
from __future__ import annotations

import json
import string
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
RPC_DRIVER = HERE / "rpc_driver.py"

PRINTABLE = set(string.printable) - set("\t\n\r\x0b\x0c")


def fetch(binary: str, addr: str, length: int) -> bytes:
    cmd = [sys.executable, str(RPC_DRIVER), "read-bytes", binary, addr, str(length)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(json.dumps({"ok": False, "error": "rpc_driver output not JSON",
                          "stdout": proc.stdout[-500:], "stderr": proc.stderr[-500:]},
                         ensure_ascii=False))
        sys.exit(1)
    if not data.get("ok"):
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)
    result = data.get("result") or data
    return bytes.fromhex(result["hex"])


def ascii_view(data: bytes) -> str:
    return "".join(chr(b) if chr(b) in PRINTABLE else "." for b in data)


def hexdump(base: int, data: bytes) -> list[str]:
    lines = []
    for off in range(0, len(data), 16):
        chunk = data[off:off + 16]
        hexpart = " ".join(f"{b:02X}" for b in chunk)
        hexpart = hexpart.ljust(16 * 3 - 1)
        lines.append(f"{base + off:08X}  {hexpart}  |{ascii_view(chunk)}|")
    return lines


def cstr_view(data: bytes) -> tuple[str, int]:
    end = data.find(b"\x00")
    raw = data if end == -1 else data[:end]
    return ascii_view(raw), len(raw)


def normalize_hex(text: str) -> str:
    t = text.strip().lower()
    if t.startswith("0x"):
        t = t[2:]
    return "".join(t.split())


def main(argv: list[str]) -> int:
    args = list(argv)
    as_json = "--json" in args
    if as_json:
        args.remove("--json")
    expect_len = None
    if "--expect-len" in args:
        i = args.index("--expect-len")
        expect_len = int(args[i + 1], 0)
        del args[i:i + 2]
    expect_hex = None
    if "--expect-hex" in args:
        i = args.index("--expect-hex")
        expect_hex = normalize_hex(args[i + 1])
        del args[i:i + 2]
    if len(args) < 3:
        print(__doc__)
        return 2

    binary, addr_text = args[0], args[1]
    base = int(addr_text, 0) if addr_text.lower().startswith("0x") \
        else int(addr_text, 16)
    length = int(args[2], 0)
    data = fetch(binary, addr_text, length)
    actual_hex = data.hex()
    cstr, cstr_len = cstr_view(data)
    non_printable = sum(1 for b in data if chr(b) not in PRINTABLE)

    checks = []
    failed = False

    if expect_len is not None:
        ok = expect_len == len(data) and expect_len == cstr_len
        checks.append({
            "check": "expect-len", "ok": ok,
            "declared": expect_len, "bytes_read": len(data), "cstr_len": cstr_len,
            "verdict": "一致" if ok else
            "MISMATCH：声明长度/实读长度/cstr 长度不一致 —— 先怀疑读数（铁律 8），"
            "禁止据此推断程序逻辑有 bug",
        })
        failed |= not ok

    if expect_hex is not None:
        if expect_hex == actual_hex:
            checks.append({"check": "expect-hex", "ok": True,
                           "verdict": "渲染文本与真实字节一致"})
        else:
            diff = next((i for i, (a, b) in enumerate(zip(expect_hex, actual_hex))
                         if a != b), min(len(expect_hex), len(actual_hex)))
            byte_off, nibble = diff // 2, diff % 2
            detail = {
                "check": "expect-hex", "ok": False,
                "expect_chars": len(expect_hex), "actual_chars": len(actual_hex),
                "first_diff_at_hex_char": diff,
                "first_diff_byte_offset": byte_off,
                "expect_around": expect_hex[max(0, diff - 8):diff + 8],
                "actual_around": actual_hex[max(0, diff - 8):diff + 8],
            }
            hint = ""
            if len(expect_hex) != len(actual_hex):
                hint = ("长度不一致 —— 典型原因：反编译器/IDA 的 hex 渲染吞掉了 "
                        "0x01->'1'、0x0E->'E' 之类的前导 0。以真实字节为准，"
                        "把渲染文本整体作废（铁律 8）")
            else:
                hint = (f"第 {byte_off} 字节（第 {nibble + 1} 个半字节）起不一致 "
                        "—— 以真实字节为准，渲染文本作废（铁律 8）")
            detail["verdict"] = hint
            checks.append(detail)
            failed = True

    notes = []
    if len(data) > 0 and non_printable / len(data) > 0.2:
        notes.append(f"{non_printable}/{len(data)} 字节不可打印 —— 这不是文本；"
                     "任何工具的字符串/hex 渲染都只是视图，唯一权威读数是本 dump")

    report = {
        "ok": not failed,
        "address": hex(base), "bytes_read": len(data),
        "hex": actual_hex, "hex_byte_count": len(data),
        "cstr": cstr, "cstr_len": cstr_len,
        "checks": checks, "notes": notes,
    }

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"== read_views @ {hex(base)}  ({len(data)} bytes) ==")
        print("\n".join(hexdump(base, data)))
        print(f"hex ({len(data)} bytes, fromhex-ready): {actual_hex}")
        print(f"ascii: {ascii_view(data)}")
        print(f"cstr ({cstr_len} chars): {cstr}")
        for n in notes:
            print(f"NOTE: {n}")
        for c in checks:
            mark = "PASS" if c["ok"] else "FAIL"
            print(f"[{mark}] {c['check']}: {c['verdict']}")
            if not c["ok"] and c["check"] == "expect-hex":
                print(f"       expect[{c['expect_chars']}]: ...{c['expect_around']}...")
                print(f"       actual[{c['actual_chars']}]: ...{c['actual_around']}...")
        if failed:
            print("exit 2：一致性检查失败 —— 第一嫌疑人是读数，不是程序。"
                  "结论必须先以本工具的真实字节重建。")
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
