#!/usr/bin/env python
"""upx_repair.py - repair tampered UPX headers so `upx -d` accepts the file.

Tampering handled:
  1. Section names renamed (UPX0/UPX1 -> random)  -> renamed back
  2. "UPX!" magic zeroed/overwritten              -> rewritten at the
     structural PackHeader offset (first raw section start - 32),
     validated by running `upx -t` as the oracle

Usage (run with the unpacker venv python, needs pefile):
  python upx_repair.py <packed.exe> [--write] [--out <fixed.exe>] [--upx <path>]

Without --write it only reports (dry-run). Successful repair is proven by
`upx -t`, then unpack with:  upx -d <fixed.exe> -o <unpacked.exe>
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pefile

UPX_MAGIC = b"UPX!"
DEFAULT_UPX = (os.path.expanduser("~/Desktop/src/tools/upx/upx.exe") if os.name == "nt"
               else (shutil.which("upx") or "/usr/bin/upx"))


def section_header_base(pe: pefile.PE) -> int:
    return pe.DOS_HEADER.e_lfanew + 4 + 20 + pe.FILE_HEADER.SizeOfOptionalHeader


def upx_test(upx: str, path: Path) -> bool:
    try:
        p = subprocess.run([upx, "-t", str(path)], capture_output=True,
                           text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return p.returncode == 0 and "OK" in (p.stdout + p.stderr)


def repair(path: Path, write: bool, out: Path | None, upx: str) -> dict:
    buf = bytearray(path.read_bytes())
    pe = pefile.PE(data=bytes(buf), fast_load=True)
    rep: dict = {"file": str(path), "sections_fixed": [],
                 "magic_found_at": [], "magic_restored_at": None,
                 "upx_test": None, "notes": []}

    # 1) section names
    names = [s.Name.rstrip(b"\x00") for s in pe.sections]
    if not any(n in (b"UPX0", b"UPX1") for n in names):
        non_dot = [s for s in pe.sections
                   if not s.Name.rstrip(b"\x00").startswith((b".", b"/"))]
        if len(non_dot) >= 2:
            base = section_header_base(pe)
            for sec, want in zip(non_dot[:2], (b"UPX0", b"UPX1")):
                hdr_off = base + pe.sections.index(sec) * 0x28
                rep["sections_fixed"].append(
                    {"from": sec.Name.rstrip(b"\x00").decode("latin1"),
                     "to": want.decode(), "offset": hdr_off})
                buf[hdr_off:hdr_off + 8] = want.ljust(8, b"\x00")

    # 2) magic
    if UPX_MAGIC in bytes(buf):
        off = bytes(buf).find(UPX_MAGIC)
        rep["magic_found_at"] = [off]
    else:
        # PackHeader = magic(4) + l_info(28), located 32 bytes before the
        # first section that has raw data. Try each candidate and let
        # `upx -t` be the oracle.
        cands = [s.PointerToRawData - 32 for s in pe.sections
                 if s.PointerToRawData > 32]
        for off in cands:
            trial = bytearray(buf)
            trial[off:off + 4] = UPX_MAGIC
            with tempfile.NamedTemporaryFile(
                    suffix=".exe", delete=False) as tf:
                tf.write(bytes(trial))
                tpath = Path(tf.name)
            try:
                if upx_test(upx, tpath):
                    buf = trial
                    rep["magic_restored_at"] = off
                    rep["upx_test"] = "OK"
                    break
            finally:
                tpath.unlink(missing_ok=True)
        if rep["magic_restored_at"] is None:
            rep["notes"].append(
                "structural magic candidates all failed upx -t; tampering "
                "goes beyond the magic (l_info/p_info fields) — fall back "
                "to manual repair (references/unpack-playbook.md)")

    if rep["magic_found_at"] or rep["magic_restored_at"] is not None:
        if rep["upx_test"] is None:
            target = out or path
            if write:
                target.write_bytes(bytes(buf))
            rep["upx_test"] = "OK" if upx_test(
                upx, target if write else path) else "FAIL"

    changed = bool(rep["sections_fixed"]) or rep["magic_restored_at"] is not None
    if write and changed:
        target = out or path
        if not rep.get("_written"):
            target.write_bytes(bytes(buf))
        rep["written"] = str(target)
    elif write:
        rep["notes"].append("nothing to write")
    rep["ok"] = True
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("--write", action="store_true", help="apply repairs")
    ap.add_argument("--out", type=Path, help="write repaired copy here")
    ap.add_argument("--upx", default=os.environ.get("UPX_BIN", DEFAULT_UPX))
    args = ap.parse_args()
    rep = repair(args.file, args.write, args.out, args.upx)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
