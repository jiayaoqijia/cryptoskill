# Custom VM reversing

Symptom: the decompile shows one enormous `switch` (or `switch`-like jump
table) inside a `while` loop, over a byte fetched from a big `.rodata` blob;
registers/state are held in a local array; opcodes don't match the host ISA.
That is an embedded interpreter — the "binary" is a VM and the real program
is bytecode.

## Recognizing dispatch

Two common shapes in decompiled C:

```c
while (1) {
    op = bytecode[pc++];
    switch (op) {                  // shape A: computed switch
      case 0: ...; break;
      case 1: ...; break;
      ...
    }
}
```

```c
while (1) {
    op = bytecode[pc++] ^ 0x37;    // shape B: decoded handler table
    handlers[op](vm);              // function pointer array
}
```

Hints that it's a VM:
- A big `const`/`.rodata` array (the bytecode) with high variety of bytes.
- A small array of ints used everywhere (`regs[16]`, `stack[256]`).
- A `pc`-like index variable incremented inside the loop.
- Arithmetic ops in many variants (add/sub/mul/xor on the same regs).

## Method — map opcodes by behavior, not by number

1. Extract the bytecode: `objdump -s -j .rodata binary` or read the address
   from the decompile and dump with gdb/xxd. Note the length (usually
   referenced nearby or ends at a marker).
2. For every switch case, write down WHAT it does in your own words:
   `case 0x1f: regs[a] = regs[b] ^ regs[c]` → opcode 0x1f = XOR.
   Ignore case numbering; two builds reorder case values freely.
3. Classify handlers: mov/const, binop, load/store, jump (writes pc),
   conditional jump (reads a flag/reg), call/ret (pc stack), in/out
   (reads stdin, prints). Flags: find where compares store results.
4. Identify the VM flavor:
   - Stack VM: one operand array + push/pop; opcodes have no operand
     registers (`add` pops two, pushes one). Most bytecode CTFs.
   - Register VM: `regs[]` indexed by operand bytes; three-operand form.
   - Accumulator: single implicit register (classic LMC/chip8 style).
5. Write a Python emulator skeleton (below), run the bytecode, log a trace
   (`pc, op, regs` each step), and read the trace — the validation loop and
   the flag transform become obvious as a log.

## Python emulator skeleton

```python
#!/usr/bin/env python3
# vm.py — trace the challenge bytecode. Fill handlers from your opcode map.
BC = open("bytecode.bin", "rb").read()

def run(inp: bytes):
    pc = 0
    regs = [0] * 16
    stack = []
    inp_i = 0
    steps = 0
    while pc < len(BC):
        op = BC[pc]; pc += 1
        steps += 1
        if steps > 1_000_000:
            raise SystemExit("step limit: infinite loop?")
        if op == 0x00:   # const rA, imm8
            a = BC[pc]; imm = BC[pc+1]; pc += 2; regs[a] = imm
        elif op == 0x01: # xor rA, rB, rC
            a,b,c = BC[pc:pc+3]; pc += 3; regs[a] = regs[b] ^ regs[c]
        elif op == 0x02: # jmp imm8
            tgt = BC[pc]; pc += 1; pc = tgt
        elif op == 0x03: # jz rA, imm8
            a = BC[pc]; tgt = BC[pc+1]; pc += 2
            if regs[a] == 0: pc = tgt
        elif op == 0x04: # read rA   (one input byte)
            a = BC[pc]; pc += 1
            regs[a] = inp[inp_i] if inp_i < len(inp) else 0; inp_i += 1
        elif op == 0x05: # print rA
            a = BC[pc]; pc += 1; print(chr(regs[a]), end="")
        else:
            raise SystemExit("unknown op 0x%02x at %d" % (op, pc))
        print("pc=%04x op=%02x regs=%s" % (pc, op, regs))  # trace line

run(b"A" * 32)
```

The trace line is the whole game: set input, watch which compares fail,
adjust input byte-by-byte (classic side-channel-free crackme VM loop).

## Common encodings

| Encoding | Recognize | Decode |
|---|---|---|
| Plain bytes | case values == raw bytes | none |
| XOR with fixed key | `op = bc[pc] ^ K` in the loop | xor back in your emulator |
| 7-bit varint operands | operands >127 continue with high bit | standard varint read |
| Nibble-packed | two 4-bit fields per byte | split byte hi/lo |
| Register file in order | first N locals of the dispatch function | mirror layout exactly (size matters: u8 vs u32) |
| Jump targets relative | pc updates as `pc += imm` | handle in jmp handlers only |

## Extracting the bytecode segment

```bash
# address + size from the decompile (e.g. bc at 0x402040, len 0x1a4):
objdump -s -j .rodata binary | less      # find the run of bytes
# or dump from the loaded image:
xxd -s 0x2040 -l 0x1a4 binary > bytecode.hex
```

Prefer the loaded/virtual address minus the segment file offset; if the
decompile references pointers into the blob (data tables, string pool inside
bytecode), keep the whole segment contiguous in your emulator memory.

## When the VM is the anti-analysis

Some challenges put a real check in the VM precisely so you can't patch a
branch. If the validator is `regs`-based, patch the emulator instead: force
compare results, or write a solver that inverts the opcode stream. If the VM
implements crypto-ish transforms over your input, capture the transform as a
function from your emulator (trace) and invert it offline.
