#!/usr/bin/env python3
"""pwntools exploit skeleton for ELF pwn challenges.

Copy into work/<event>/<chal>/solve/exploit.py and fill the TODO block.
The pwn import is deferred so --help works before scripts/setup.sh has run.

Usage:
  ./solve-template.py ./dist/chal                          # local process
  ./solve-template.py ./dist/chal --remote ctf.example 1337
  ./solve-template.py ./dist/chal --libc ./dist/libc.so.6
  ./solve-template.py ./dist/chal --gdb                    # gdb.debug via tmux

Always run inside the repo venv:
  scripts/ctf python exploit.py ./dist/chal --remote host 1337
Remote connections are gated by the router skill (skills/ctf/SKILL.md).
"""
import argparse
import re
import sys

# Router flag regex (keep in sync with skills/ctf/SKILL.md "Flag hunting").
FLAG_RE = re.compile(r"(?:flag|FLAG|ctf|CTF|picoCTF|HTB)\{[^}]{4,}\}")

GDB_SCRIPT = """b main
continue
"""

EXAMPLES = """examples:
  %(prog)s ./dist/chal
  %(prog)s ./dist/chal --remote chal.ctf.example 1337 --libc ./dist/libc.so.6
  %(prog)s ./dist/chal --gdb
"""


def build_parser():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES,
    )
    ap.add_argument("binary", help="path to the challenge ELF")
    ap.add_argument("--remote", nargs=2, metavar=("HOST", "PORT"),
                    help="connect to HOST PORT instead of spawning locally")
    ap.add_argument("--libc", metavar="PATH",
                    help="libc.so.6 shipped with the challenge "
                         "(set libc.address after leaking)")
    ap.add_argument("--gdb", action="store_true",
                    help="local only: run under gdb.debug "
                         "(set context.terminal, e.g. tmux)")
    ap.add_argument("--debug", action="store_true",
                    help="context.log_level = 'debug'")
    return ap


def hunt_flag(io):
    """Drain the tube and grep the router's flag regex out of everything."""
    data = b""
    try:
        data = io.recvall(timeout=5)
    except EOFError:
        pass
    match = FLAG_RE.search(data.decode("latin-1"))
    if match:
        print(f"[+] flag: {match.group(0)}")
        return 0
    print("[-] no flag in output -- fill in the TODO block; end with "
          "io.interactive() once you have a shell")
    return 1


def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        from pwn import ELF, ROP, context, flat, gdb, process, remote
    except ImportError:
        sys.exit("pwntools not installed: run scripts/setup.sh "
                 "(or execute via: scripts/ctf python <script>)")

    context.log_level = "debug" if args.debug else "info"

    elf = ELF(args.binary, checksec=True)
    if args.libc:
        libc = ELF(args.libc, checksec=False)
    else:
        libc = None
        print("[i] no --libc given; add the handout libc for anything "
              "ret2libc (references/toolchain.md, pwninit)")

    if args.remote:
        io = remote(args.remote[0], int(args.remote[1]))
    elif args.gdb:
        # context.terminal = ["tmux", "new-window"]   # required for the window
        io = gdb.debug(args.binary, gdbscript=GDB_SCRIPT)
    else:
        io = process(args.binary)

    # ---- TODO: exploit steps -----------------------------------------------
    # 1. reach the vulnerable input
    #    io.sendlineafter(b"choice: ", b"1")
    # 2. leak / build the payload
    #    rop = ROP([elf, libc])                    # after libc.address is set
    #    rop.call(libc.sym["system"], [next(libc.search(b"/bin/sh\x00"))])
    #    print(rop.dump())
    #    payload = flat({OFFSET: rop.chain()})     # OFFSET from scripts/off.py
    # 3. deliver
    #    io.sendline(payload)
    # 4. cash out
    #    io.interactive()                          # shell; or ORW + flag grep
    # -------------------------------------------------------------------------

    return hunt_flag(io)


if __name__ == "__main__":
    sys.exit(main())
