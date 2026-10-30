#!/usr/bin/env python3
"""Brainfuck interpreter for CTF esoteric challenges.

Usage:
  bf.py FILE [--tape N] [--steps N]
  bf.py -c '++++[->++.<' [--tape N] [--steps N]

Stdlib only. Bounded tape (default 30000 cells, wrapping 8-bit cells, moving
right past the end is an error) and a step limit (default 10M) so hostile
programs cannot hang the box. Reads stdin when the program needs ','.
"""
import argparse
import sys

STEP_LIMIT_DEFAULT = 10_000_000
TAPE_DEFAULT = 30_000


class BFError(Exception):
    pass


def parse_jump_targets(code: str) -> dict[int, int]:
    stack, pairs = [], {}
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise BFError(f"unbalanced ']' at index {i}")
            j = stack.pop()
            pairs[j] = i
            pairs[i] = j
    if stack:
        raise BFError(f"unbalanced '[' at index {stack[0]}")
    return pairs


def run(code: str, tape_size: int = TAPE_DEFAULT, max_steps: int = STEP_LIMIT_DEFAULT,
        stdin=None, stdout=None) -> None:
    src = sys.stdin.buffer if stdin is None else stdin
    dst = sys.stdout.buffer if stdout is None else stdout
    jumps = parse_jump_targets(code)
    tape = bytearray(tape_size)
    ptr = ip = steps = 0
    while ip < len(code):
        steps += 1
        if steps > max_steps:
            raise BFError(f"step limit exceeded ({max_steps}); infinite loop?")
        op = code[ip]
        if op == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF
        elif op == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif op == ">":
            ptr += 1
            if ptr >= tape_size:
                raise BFError(f"tape overflow: pointer past {tape_size} cells; pass --tape")
        elif op == "<":
            ptr -= 1
            if ptr < 0:
                raise BFError("tape underflow: pointer before cell 0")
        elif op == ".":
            dst.write(bytes([tape[ptr]]))
        elif op == ",":
            ch = src.read(1)
            tape[ptr] = ch[0] if ch else 0  # EOF reads as 0 so ",[.,]"-style loops terminate
        elif op == "[":
            if tape[ptr] == 0:
                ip = jumps[ip]
        elif op == "]":
            if tape[ptr] != 0:
                ip = jumps[ip]
        ip += 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Brainfuck interpreter (bounded tape, step limit).")
    ap.add_argument("file", nargs="?", help="program file (omit with -c)")
    ap.add_argument("-c", "--code", help="inline program string")
    ap.add_argument("--tape", type=int, default=TAPE_DEFAULT, help=f"tape size in cells (default {TAPE_DEFAULT})")
    ap.add_argument("--steps", type=int, default=STEP_LIMIT_DEFAULT,
                    help=f"max executed instructions (default {STEP_LIMIT_DEFAULT})")
    args = ap.parse_args(argv)
    if not args.file and not args.code:
        ap.error("provide FILE or -c CODE")
    try:
        code = open(args.file).read() if args.file else args.code
    except OSError as e:
        print(f"bf.py: cannot read {args.file}: {e}", file=sys.stderr)
        return 2
    try:
        run(code, tape_size=args.tape, max_steps=args.steps)
    except BFError as e:
        print(f"bf.py: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
