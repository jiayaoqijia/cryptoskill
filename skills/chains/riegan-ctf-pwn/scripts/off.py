#!/usr/bin/env python3
"""Find the offset from input start to the crash point (saved RIP) with a
cyclic (de Bruijn) pattern.

Modes:
  off.py ./dist/chal                 local crash, solve offset from core dump
  off.py ./dist/chal --prompt ': '   wait for a prompt before sending pattern
  off.py --remote host 1337          send pattern to a service (no core file);
                                     convert the fault address it reports:
  off.py 0x61616164                  translate a pattern value to an offset

Requires pwntools (scripts/setup.sh); --help works without it.
"""
import argparse
import sys

EXAMPLES = """examples:
  %(prog)s ./dist/chal
  %(prog)s ./dist/chal --length 1024 --prompt 'name: '
  %(prog)s --remote chal.ctf.example 1337
  %(prog)s 0x61616168
"""


def build_parser():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES,
    )
    ap.add_argument("binary", nargs="?",
                    help="local ELF to crash (omit for pure value lookup)")
    ap.add_argument("fault", nargs="?",
                    help="fault/pattern value, e.g. 0x61616164 "
                         "(0x-prefixed or decimal)")
    ap.add_argument("--remote", nargs=2, metavar=("HOST", "PORT"),
                    help="send the pattern to a remote service instead")
    ap.add_argument("--length", type=int, default=512,
                    help="cyclic pattern length (default 512)")
    ap.add_argument("--prompt",
                    help="recvuntil this string before sending the pattern")
    ap.add_argument("--raw", action="store_true",
                    help="send() without trailing newline (default sendline)")
    return ap


def report(name, value, offset):
    print(f"[+] {name} = {value:#x} -> offset {offset}")


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)

    # A lone argument that parses as a number is a fault value, not a path.
    if args.fault is None and args.binary is not None:
        try:
            args.fault = int(args.binary, 0)
            args.binary = None
        except ValueError:
            pass

    try:
        from pwn import context, cyclic, cyclic_find, process, remote
    except ImportError:
        sys.exit("pwntools not installed: run scripts/setup.sh "
                 "(or execute via: scripts/ctf python <script>)")

    context.log_level = "warn"

    if args.fault is not None:
        offset = cyclic_find(args.fault)
        if isinstance(offset, int) and offset >= 0:
            report("value", args.fault, offset)
            return 0
        print(f"[-] {args.fault:#x} is not a cyclic pattern value "
              "(wrong value, or pattern length too small)")
        return 2

    if args.binary is None and not args.remote:
        ap.error("need a binary path (local crash) or --remote HOST PORT")

    pattern = cyclic(args.length)
    if args.remote:
        io = remote(args.remote[0], int(args.remote[1]))
    else:
        io = process(args.binary)
    if args.prompt:
        io.recvuntil(args.prompt.encode())
    (io.send if args.raw else io.sendline)(pattern)

    if args.remote:
        try:
            tail = io.recvall(timeout=3)
            if tail:
                print(f"[*] service said: {tail.decode('latin-1')!r}")
        except EOFError:
            pass
        print("[+] pattern sent; when the service reports its fault address, "
              f"run: {sys.argv[0]} 0x<value>")
        return 0

    status = io.wait()
    print(f"[*] exit status: {status} (negative = killed by signal; "
          "-11 SIGSEGV, -6 SIGABRT)")

    try:
        core = io.corefile
    except Exception as exc:  # no readable core dump
        print(f"[-] no core dump ({exc})")
        print("    cat /proc/sys/kernel/core_pattern   # must be a file like 'core'")
        print("    sudo sysctl -w kernel.core_pattern=core   then re-run")
        print(f"    manual: gdb ./{args.binary}, feed it the pattern, "
              "x/gx $rsp, then")
        print(f"            {sys.argv[0]} 0x<value>")
        return 2

    candidates = []
    for attr in ("fault_addr", "pc"):
        value = getattr(core, attr, None)
        if value:
            candidates.append((f"core.{attr}", int(value)))
    rsp = getattr(core, "rsp", None)
    if rsp:
        for width in (8, 4):  # amd64 qword / i386 dword at the stack top
            try:
                raw = core.read(rsp, width)
                candidates.append(
                    (f"*core.rsp ({width}-byte)",
                     int.from_bytes(raw, "little")))
            except Exception:
                pass

    found = False
    for name, value in candidates:
        try:
            offset = cyclic_find(value)
        except Exception:
            continue
        if isinstance(offset, int) and offset >= 0:
            report(name, value, offset)
            found = True
    if not found:
        if candidates:
            print("[-] no cyclic value recognized; check these by hand:")
            for name, value in candidates:
                print(f"    {name} = {value:#x}")
        else:
            print("[-] core file yielded no candidate registers")
    return 0 if found else 2


if __name__ == "__main__":
    sys.exit(main())
