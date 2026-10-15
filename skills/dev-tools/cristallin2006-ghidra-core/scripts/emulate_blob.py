#!/usr/bin/env python
"""emulate_blob.py - Unicorn harness for raw blobs (shellcode / peeled payloads).

Host-side tool (Python 3.8+, unicorn is the only non-stdlib dependency).
Emulates a bare blob (peeled shellcode / payload, e.g. a multi-MB
instruction-stream decoder) without hand-rolling a harness each time:
image + private stack mapping, register init, extra file mappings,
instruction cap, timeout, dirty-page tracking and page dumps.

Stop reasons reported: max-insns / ret-flyout (RIP left mapped memory,
usually a RET flying out) / invalid-fetch / unaligned / exception / timeout.

Usage:
  python emulate_blob.py blob.bin --base 0x140000000 --entry 0x0 \
      [--rsp 0x7ffffffde000] [--stack-size 0x100000] [--max-insns 50000000] \
      [--timeout 120] [--reg RAX=0x1 ...] [--map-file path@addr ...] \
      [--arch x64|x86|arm64] [--dump-dir out/] [--json out.json] \
      [--hook-rip-log N]

Exit codes: 0 emulation finished (any stop reason, read the report),
2 usage error, 3 unicorn not installed, 4 harness error (not the guest:
blob/map-file unreadable or empty, unknown --reg, mapping failed, or
entry-unmapped — 0 instructions fetched because entry is not mapped).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

try:
    from unicorn import (
        Uc, UcError,
        UC_ARCH_X86, UC_ARCH_ARM64,
        UC_MODE_32, UC_MODE_64, UC_MODE_ARM,
        UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_FETCH_UNMAPPED,
    )
    from unicorn import x86_const, arm64_const
except ImportError:
    print("[依赖缺失] 需要 unicorn：pip install unicorn（或进 re-tools-venv）",
          file=sys.stderr)
    sys.exit(3)

PAGE = 0x1000

ARCHES = {
    "x64": (UC_ARCH_X86, UC_MODE_64, x86_const.UC_X86_REG_RIP,
            x86_const.UC_X86_REG_RSP, "UC_X86_REG_", x86_const),
    "x86": (UC_ARCH_X86, UC_MODE_32, x86_const.UC_X86_REG_EIP,
            x86_const.UC_X86_REG_ESP, "UC_X86_REG_", x86_const),
    "arm64": (UC_ARCH_ARM64, UC_MODE_ARM, arm64_const.UC_ARM64_REG_PC,
              arm64_const.UC_ARM64_REG_SP, "UC_ARM64_REG_", arm64_const),
}


def align_down(v, a=PAGE):
    return v & ~(a - 1)


def align_up(v, a=PAGE):
    return (v + a - 1) & ~(a - 1)


def parse_int(s):
    return int(s, 0)


def parse_reg(s):
    if "=" not in s:
        raise argparse.ArgumentTypeError("--reg 需要 NAME=VALUE，如 RAX=0x1")
    name, val = s.split("=", 1)
    return name.strip().upper(), parse_int(val.strip())


def parse_map_file(s):
    if "@" not in s:
        raise argparse.ArgumentTypeError("--map-file 需要 path@addr，如 data.bin@0x2000000")
    path, addr = s.rsplit("@", 1)
    return path, parse_int(addr)


def main():
    ap = argparse.ArgumentParser(
        description="裸 blob 的 Unicorn 仿真 harness（固化手搭流程）")
    ap.add_argument("blob", help="待仿真 blob 文件")
    ap.add_argument("--base", type=parse_int, required=True, help="镜像加载基址")
    ap.add_argument("--entry", type=parse_int, default=0, help="入口偏移（相对 base，默认 0）")
    ap.add_argument("--rsp", type=parse_int, default=0x7ffffffde000, help="初始栈顶")
    ap.add_argument("--stack-size", type=parse_int, default=0x100000, help="栈区大小")
    ap.add_argument("--max-insns", type=parse_int, default=50000000, help="指令数上限")
    ap.add_argument("--timeout", type=float, default=120, help="超时秒数（墙钟+Unicorn）")
    ap.add_argument("--reg", type=parse_reg, action="append", default=[],
                    metavar="NAME=VALUE", help="入口寄存器初始化，可重复")
    ap.add_argument("--map-file", type=parse_map_file, action="append", default=[],
                    metavar="PATH@ADDR", help="额外映射文件到地址，可重复")
    ap.add_argument("--arch", choices=sorted(ARCHES), default="x64")
    ap.add_argument("--dump-dir", help="dirty 页 dump 目录（page_<addr>.bin）")
    ap.add_argument("--json", help="JSON 报告输出路径")
    ap.add_argument("--hook-rip-log", type=int, default=0, metavar="N",
                    help="每 N 条指令打印一次 RIP（调试卡死用，默认关）")
    a = ap.parse_args()

    uc_arch, uc_mode, reg_pc, reg_sp, reg_prefix, reg_consts = ARCHES[a.arch]
    pc_name = {UC_ARCH_X86: "RIP" if a.arch == "x64" else "EIP"}.get(uc_arch, "PC")

    # ---- harness 自身错误（文件/参数问题），与 guest 执行错误严格区分 ----
    try:
        blob = open(a.blob, "rb").read()
    except OSError as e:
        print("[harness 错误] 读取 blob 失败: %s" % e, file=sys.stderr)
        return 4
    if not blob:
        print("[harness 错误] blob 为空文件", file=sys.stderr)
        return 4

    base = align_down(a.base)
    if base != a.base:
        print("[提示] base 0x%x 非页对齐，已向下对齐到 0x%x" % (a.base, base))
    entry = a.base + a.entry

    state = {
        "insns": 0, "stop": None, "dirty": set(), "entry_unmapped": False,
        "regions": [], "t0": time.monotonic(),
    }

    uc = Uc(uc_arch, uc_mode)

    def map_region(addr, size, label):
        lo, hi = align_down(addr), align_up(addr + size)
        uc.mem_map(lo, hi - lo)
        state["regions"].append((lo, hi, label))
        return lo, hi

    try:
        map_region(base, len(blob), "image")
        uc.mem_write(base, blob)

        stack_lo = align_down(a.rsp - a.stack_size)
        stack_hi = align_up(a.rsp + 1)  # rsp 页对齐时含住栈顶所在页，RET 才能读 [rsp]
        map_region(stack_lo, stack_hi - stack_lo, "stack")
        uc.reg_write(reg_sp, a.rsp)

        for path, addr in a.map_file:
            try:
                payload = open(path, "rb").read()
            except OSError as e:
                print("[harness 错误] --map-file 读取失败: %s" % e, file=sys.stderr)
                return 4
            map_region(addr, max(len(payload), 1), os.path.basename(path))
            if payload:
                uc.mem_write(align_down(addr), payload)

        for name, val in a.reg:
            reg = getattr(reg_consts, reg_prefix + name, None)
            if reg is None:
                print("[harness 错误] 未知寄存器 %s（arch=%s）" % (name, a.arch),
                      file=sys.stderr)
                return 4
            uc.reg_write(reg, val)
    except UcError as e:
        print("[harness 错误] 内存映射/寄存器初始化失败（非 guest 错误）: %s" % e,
              file=sys.stderr)
        return 4

    def in_mapped(addr):
        return any(lo <= addr < hi for lo, hi, _ in state["regions"])

    def hook_code(uc_, address, size, _):
        state["insns"] += 1
        if state["insns"] > a.max_insns:
            state["stop"] = "max-insns"
            uc_.emu_stop()
        elif a.hook_rip_log and state["insns"] % a.hook_rip_log == 0:
            print("[rip-log] #%d %s=0x%x" % (state["insns"], pc_name, address))
        if time.monotonic() - state["t0"] > a.timeout:
            state["stop"] = "timeout"
            uc_.emu_stop()

    def hook_write(uc_, access, address, size, value, _):
        for off in range(0, size, PAGE):
            state["dirty"].add(align_down(address + off))
        state["dirty"].add(align_down(address + size - 1))  # 跨页写入的尾页

    def hook_fetch_unmapped(uc_, access, address, size, value, _):
        if state["insns"] == 0:
            # 第一条取指就失败 = 入口本身未映射，是 harness 配置错，不是 RET 飞出
            state["stop"] = ("entry-unmapped (入口 0x%x 未映射：0 条指令都未能取指，"
                             "这是 harness 配置错——检查 --base/--entry，"
                             "--entry 是相对 --base 的偏移)" % address)
            state["entry_unmapped"] = True
        elif in_mapped(uc_.reg_read(reg_pc)):
            state["stop"] = "invalid-fetch (0x%x 未映射)" % address
        else:
            state["stop"] = ("ret-flyout (%s=0x%x 已飞出映射区，疑似 RET 飞出)"
                             % (pc_name, address))
        uc_.emu_stop()
        return False

    uc.hook_add(UC_HOOK_CODE, hook_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, hook_write)
    uc.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, hook_fetch_unmapped)

    # ---- guest 执行：此处的 UcError 是 guest 炸了，不是 harness 炸了 ----
    err = None
    try:
        uc.emu_start(entry, 0, timeout=int(a.timeout * 1_000_000),
                     count=a.max_insns + 1)
    except UcError as e:
        err = e

    if state["stop"] is None:
        if err is None:
            state["stop"] = "finished (until 地址 0 处正常停住)"
        elif "FETCH_UNMAPPED" in str(err):
            state["stop"] = "invalid-fetch"
        elif "UNALIGNED" in str(err):
            state["stop"] = "unaligned"
        else:
            state["stop"] = "exception: %s" % err

    final_pc = None
    try:
        final_pc = uc.reg_read(reg_pc)
    except UcError:
        pass

    dirty = sorted(state["dirty"])
    if a.dump_dir and dirty:
        os.makedirs(a.dump_dir, exist_ok=True)
        for page in dirty:
            try:
                data = bytes(uc.mem_read(page, PAGE))
            except UcError:
                continue
            with open(os.path.join(a.dump_dir, "page_0x%x.bin" % page), "wb") as f:
                f.write(data)

    report = {
        "blob": a.blob, "arch": a.arch, "base": "0x%x" % base,
        "entry": "0x%x" % entry,
        "instructions": state["insns"],
        "stop_reason": state["stop"],
        "final_%s" % pc_name.lower(): ("0x%x" % final_pc) if final_pc is not None else None,
        "dirty_pages": ["0x%x" % p for p in dirty],
        "regions": [{"lo": "0x%x" % lo, "hi": "0x%x" % hi, "label": lb}
                    for lo, hi, lb in state["regions"]],
        "elapsed_sec": round(time.monotonic() - state["t0"], 3),
    }

    print("=== 仿真报告 ===")
    print("  blob        : %s (%d 字节, arch=%s)" % (a.blob, len(blob), a.arch))
    print("  base/entry  : 0x%x / 0x%x" % (base, entry))
    print("  执行指令数  : %d" % report["instructions"])
    print("  停止原因    : %s" % report["stop_reason"])
    print("  %s 终值   : %s" % (pc_name, report["final_%s" % pc_name.lower()]))
    print("  dirty 页    : %d" % len(dirty))
    for p in report["dirty_pages"][:32]:
        print("    %s" % p)
    if len(dirty) > 32:
        print("    ... 共 %d 页" % len(dirty))
    if a.dump_dir and dirty:
        print("  dirty dump  : %s (page_<addr>.bin)" % a.dump_dir)
    if err is not None:
        print("  [guest 异常] %s（guest 执行炸了，非 harness 问题）" % err)

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print("  JSON -> %s" % a.json)
    if state["entry_unmapped"]:
        print("  [harness 配置错] 入口未映射，本次仿真无效——修正 --base/--entry 后重跑")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
