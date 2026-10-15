# List zero-reference data blocks (hidden permutation tables / S-boxes / key
# material in custom ciphers), with content classification and adjacent-block
# span-merge hints.
# @category DSH.Reverse
# @runtime PyGhidra
#
# Dual-mode script:
#   daemon (primary):
#     python rpc_driver.py exec-code <binary> <this file>
#     python rpc_driver.py "@<out.json>" exec-code <binary> <this file>
#     (rpc_driver's own @out writes the daemon JSON reply to disk; exec-code
#     cannot forward script args, so in daemon mode options come from the
#     DSH_UNREF_DATA_ARGS env var -- it must be exported BEFORE the daemon
#     starts, e.g. DSH_UNREF_DATA_ARGS='--min-size 32' python rpc_driver.py
#     ensure ...)
#   legacy (driver.py exec):
#     driver.py exec <binary> unreferenced_data.py ["@<out>"] [options]
#
# Options:
#   --min-size <n>         only report blocks of at least n bytes (default 16)
#   --include-referenced   also report referenced runs (default: zero-ref only)
#   --help                 print this usage as JSON
#
# Output: JSON with blocks[] {address, size, refs, class, preview_hex,
# merged_note?} where class is one of perm(n) (content is exactly the full
# permutation of 0..n-1, n in {16,32,64,128,256}), bijection (all bytes
# distinct but not 0..n-1), high-entropy-key (Shannon entropy > 4.5 bits/byte),
# const-run (single repeated byte), ascii (>=90% printable), other.
# merged_note flags a perm(16)/perm(32) block whose immediately following
# block (+0x20/+0x40/+0x80) combines into a larger permutation (64/128 items)
# or is its exact reverse -- two adjacent 32-byte tables are often the two
# halves of one 64-item permutation. Caveat: zero incoming xrefs only means
# no direct reference; tables reached via computed pointers (base+index)
# leave no xref -- verify before concluding dead data.

import sys as _sys

# dsh family convention: force UTF-8 on both streams (cp936 console mojibake
# lesson). Guarded: inside the rpc daemon the streams may not be reconfigurable.
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# --- DSH @out support (self-contained, no cross-script imports) ---
# If the first script argument starts with '@', it is popped and treated as an
# output file path: the full JSON payload is written there, and stdout only
# carries a short status summary between the markers.
_DSH_OUT_PATH = None

def _dsh_extract_out():
    global _DSH_OUT_PATH
    try:
        args = list(getScriptArgs())
    except NameError:
        return []
    if args and str(args[0]).startswith("@"):
        _DSH_OUT_PATH = str(args[0])[1:]
        args = args[1:]
    return args

_DSH_ARGS = _dsh_extract_out()
# --- end DSH @out support ---

import json
import math
import os
import shlex
import traceback

_USAGE = (
    "unreferenced_data.py [@out] [--min-size <n>] [--include-referenced] "
    "[--help]; daemon mode: options via DSH_UNREF_DATA_ARGS env (set before "
    "daemon start)"
)

_PERM_SIZES = (16, 32, 64, 128, 256)
_READ_CAP = 4096        # classification reads at most this many bytes per block
_SCAN_CAP = 1 << 20     # blocks larger than 1 MiB are skipped, not scanned


def _emit(data):
    """Daemon exec-code: hand the payload to the injected output_json (the last
    call wins). Legacy/direct: honor @out, else print between markers."""
    try:
        output_json  # noqa: F821 - injected by exec-code / exec_code.py
    except NameError:
        pass
    else:
        output_json(data)  # noqa: F821
        return
    if _DSH_OUT_PATH:
        try:
            f = open(_DSH_OUT_PATH, "w")
            try:
                f.write(json.dumps(data))
            finally:
                f.close()
            summary = {
                "status": data.get("status", "success"),
                "out": _DSH_OUT_PATH,
                "count": data.get("block_count", 0),
            }
            if data.get("status") == "error":
                summary["error"] = data.get("error")
            print("===JSON_START===")
            print(json.dumps(summary))
            print("===JSON_END===")
        except Exception as write_err:
            print("===JSON_START===")
            print(json.dumps({"status": "error",
                              "error": "failed to write out file: " + str(write_err)}))
            print("===JSON_END===")
    else:
        print("===JSON_START===")
        print(json.dumps(data))
        print("===JSON_END===")


def _parse_args(argv):
    """Manual parse (argparse would raise SystemExit inside exec'd code).
    Returns (opts, error)."""
    opts = {"min_size": 16, "include_referenced": False, "help": False}
    i = 0
    while i < len(argv):
        a = str(argv[i])
        if a in ("--help", "-h"):
            opts["help"] = True
        elif a == "--min-size":
            if i + 1 >= len(argv):
                return None, "--min-size needs an integer byte count"
            try:
                opts["min_size"] = int(str(argv[i + 1]), 0)
            except ValueError:
                return None, "--min-size not an integer: %s" % argv[i + 1]
            i += 1
        elif a == "--include-referenced":
            opts["include_referenced"] = True
        else:
            return None, "unknown argument: %s (usage: %s)" % (a, _USAGE)
        i += 1
    return opts, None


def _get_args():
    """Legacy mode: script args (after @out extraction). Daemon mode: exec-code
    forwards no script args, so fall back to the DSH_UNREF_DATA_ARGS env var."""
    if _DSH_ARGS:
        return _DSH_ARGS
    env = os.environ.get("DSH_UNREF_DATA_ARGS", "").strip()
    if env:
        try:
            return shlex.split(env)
        except ValueError:
            return env.split()
    return []


def _read_bytes(memory, addr, n):
    """Read n bytes as a Python bytes object; JArray fast path with a
    per-byte getByte fallback (works in both PyGhidra environments)."""
    try:
        from jpype import JArray, JByte
        buf = JArray(JByte)(n)
        memory.getBytes(addr, buf)
        return bytes(bytearray((int(b) & 0xFF) for b in buf))
    except Exception:
        out = bytearray()
        for i in range(n):
            out.append(memory.getByte(addr.add(i)) & 0xFF)
        return bytes(out)


def _entropy(data):
    """Shannon entropy in bits/byte."""
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    h = 0.0
    for c in counts:
        if c:
            p = c / float(n)
            h -= p * math.log(p, 2)
    return h


def _classify(data):
    """Classify a data block by interpreting its bytes."""
    n = len(data)
    if n == 0:
        return "other"
    if len(set(data)) == 1:
        return "const-run"
    if n in _PERM_SIZES and sorted(data) == list(range(n)):
        return "perm(%d)" % n
    if len(set(data)) == n:
        return "bijection"
    printable = sum(1 for b in data if 32 <= b < 127)
    if printable * 10 >= 9 * n:
        return "ascii"
    if _entropy(data) > 4.5:
        return "high-entropy-key"
    return "other"


def _scan(prog, min_size, include_referenced):
    """Segment each initialized memory block into runs of zero-ref vs
    referenced addresses; return (blocks, skipped)."""
    memory = prog.getMemory()
    refmgr = prog.getReferenceManager()
    blocks = []   # {address, size, refs, class, preview_hex} + _off/_data private
    skipped = []
    for block in memory.getBlocks():
        try:
            if not block.isInitialized():
                continue
        except Exception:
            continue
        start = block.getStart()
        size = int(block.getSize())
        if size <= 0:
            continue
        if size > _SCAN_CAP:
            skipped.append({"address": str(start), "size": size,
                            "reason": "block larger than 1 MiB scan cap"})
            continue
        runs = []
        rs = rrefs = 0
        rzero = None
        for off in range(size):
            try:
                rc = int(refmgr.getReferenceCountTo(start.add(off)))
            except Exception:
                rc = 0
            zero = (rc == 0)
            if rzero is None:
                rs, rrefs, rzero = off, rc, zero
            elif zero == rzero:
                rrefs += rc
            else:
                runs.append((rs, off - rs, rrefs, rzero))
                rs, rrefs, rzero = off, rc, zero
        if rzero is not None:
            runs.append((rs, size - rs, rrefs, rzero))
        for off, ln, refs, zero in runs:
            if ln < min_size:
                continue
            if not zero and not include_referenced:
                continue
            addr = start.add(off)
            data = _read_bytes(memory, addr, min(ln, _READ_CAP))
            rec = {"address": str(addr), "size": ln, "refs": refs,
                   "class": _classify(data),
                   "preview_hex": " ".join("%02x" % b for b in data[:32])}
            if ln > _READ_CAP:
                rec["class_sampled"] = True  # classified on first 4096 bytes
            rec["_off"] = int(addr.getOffset())
            rec["_data"] = data
            blocks.append(rec)
    return blocks, skipped


def _merge_hints(blocks):
    """For each perm(16)/perm(32) block, check the block immediately after it
    (+0x20/+0x40/+0x80): does the concatenation form a larger permutation
    (64/128 items), or is the next block its exact reverse?"""
    by_off = dict((b["_off"], b) for b in blocks)
    for b in blocks:
        if b["class"] not in ("perm(16)", "perm(32)"):
            continue
        nxt = by_off.get(b["_off"] + b["size"])
        if nxt is None:
            continue
        combined = b["_data"] + nxt["_data"]
        m = len(combined)
        if m in (64, 128) and sorted(combined) == list(range(m)):
            b["merged_note"] = ("与后继块 %s 合并构成 perm(%d)（同一置换的两半）"
                                % (nxt["address"], m))
        elif nxt["_data"] == b["_data"][::-1]:
            b["merged_note"] = ("后继块 %s 是本块的 reverse（倒序同表）"
                                % nxt["address"])


def run():
    try:
        opts, err = _parse_args(_get_args())
        if err:
            _emit({"status": "error", "error": err, "usage": _USAGE})
            return
        if opts["help"]:
            _emit({"status": "success", "usage": _USAGE, "doc": __doc__})
            return

        try:
            prog = program  # noqa: F821 - exec-code namespace
        except NameError:
            prog = currentProgram  # noqa: F821 - legacy GhidraScript global
        if prog is None:
            _emit({"status": "error", "error": "No program loaded"})
            return

        blocks, skipped = _scan(prog, opts["min_size"],
                                opts["include_referenced"])
        _merge_hints(blocks)
        blocks.sort(key=lambda b: b["_off"])
        for b in blocks:
            del b["_off"]
            del b["_data"]

        _emit({
            "status": "success",
            "program": prog.getName(),
            "min_size": opts["min_size"],
            "include_referenced": opts["include_referenced"],
            "block_count": len(blocks),
            "blocks": blocks,
            "skipped_blocks": skipped,
            "caveat": ("zero incoming refs only means no DIRECT xref; tables "
                       "reached via computed pointers (base+index) or from "
                       "uninitialized code paths leave no xref -- verify "
                       "before concluding dead data"),
        })

    except Exception as e:
        _emit({"status": "error", "error": str(e),
               "traceback": traceback.format_exc()})


run()
