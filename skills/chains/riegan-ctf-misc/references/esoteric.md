# Esoteric languages — identify, decode, occasionally run

Rule of thumb: an esolang challenge is usually **decode, not execute** — the
program's output or the program text *is* the flag material. Run things only
when the challenge demands behavior you cannot simulate in your head.

## Identify by look

| You see | Language | Notes |
|---|---|---|
| `++++[>++++>` `.` `,` `[` `]` `<` `>` | Brainfuck | `scripts/bf.py` runs it |
| only spaces/tabs/newlines (file "looks empty", `wc -c` big) | Whitespace | interpreter below; `xxd` first |
| `[](!+[])` `(+!![])` `($+[])` soup of brackets | JSFuck | JS, runs in node; sandbox it |
| brainfuck with extra noise chars between ops | *fuck variant (Nestedfuck, Flattenfuck…) | strip noise → brainfuck |
| `Ook. Ook? Ook!` | Ook! | brainfuck substitution: Ook *pairs* map to the 8 BF ops — recover the mapping from the Ook spec or by pair-frequency |
| grid of `v ^ < > : _ @` chars | Befunge | 2D; follow arrows manually for small programs |
| abstract colored rectangles image | Piet | `npiet` (npiet sourceforge; document install) |
| `HAI`, `KTHXBYE`, `VISIBLE`, `CAN HAS` | LOLCODE | readable-ish; glossary search |
| dramatis personae, `Speak thy mind`, acts/scenes | Shakespeare | decompile to stack ops |
| song lyrics, `Rockstar` keywords (`tommy`, `desire`) | Rockstar | transpile to JS via rockstar npm pkg or decode by hand |
| `/` `\` `+` `*` triangles | Malbolge | if actually required to run: reference interpreter; usually just a decoration |
| `[A-Z]` with `.` `-` runs, letters absent | Morse | table in `misc-grab-bag.md` |
| `!?` pauses, "coo"? Ook variant / Cow (`MoO`/`mOo`) | Cow | brainfuck-family substitution |

Strategy order: 1) match signature above; 2) search the exact syntax name;
3) decide decode-vs-run; 4) if run: prefer a local interpreter you write or
one already on this host; containerize anything else (`podman run --rm -i
docker.io/library/node:24-alpine node -` for JS; never run untrusted code on
the host directly).

## Brainfuck

```bash
skills/ctf-misc/scripts/bf.py prog.bf            # bounded tape, step limit
skills/ctf-misc/scripts/bf.py -c '++++++++[>++++[>++<-]<-]>.'
echo -n 'input' | skills/ctf-misc/scripts/bf.py prog.bf    # ',' reads stdin
```

Details: 30000-cell tape default (`--tape`), 10M-step cap (`--steps`), EOF
reads as 0. Verified: hello world, echo loop `,[.,]`, unbalanced-loop and
overflow errors.

Variant with cell values that must exceed 255? Some dialects use big cells —
that is a hint the challenge expects unicode codepoints; patch the script's
`& 0xFF` wraps or reimplement.

## Whitespace

`xxd file` first: whitespace programs are ` ` `\t` `\n` only. Instruction set
(standard): IMP `[Space]`=stack, `[Tab][Space]`=arith, `[Tab][Tab]`=heap,
`[LF]`=flow, `[Tab][LF]`=I/O; numbers are sign bit + binary, `[LF]`-terminated.
Stack ops: `[Space]n` push, `[LF][Space]` dup, `[LF][Tab]` swap, `[LF][LF]`
drop, `[Tab][Space]n` copy nth, `[Tab][LF]n` slide n. Arith: add/sub/mul/div/
mod pop b then a (`a op b`). Heap: push address then value, `store`; `load`
pushes. Flow: mark/call/jmp/jz/jneg/ret/end. I/O: putc/putn/readc/readn.

Verified interpreter (stdlib only; hello, arithmetic and heap-loop tested):

```python
S, T, L = " ", "\t", "\n"
R = lambda s: s.replace(S, "s").replace(T, "t").replace(L, "l")
IMP = {S: "stack", T + S: "arith", T + T: "heap", L: "flow", T + L: "io"}

def parse(src):
    src = "".join(c for c in src if c in " \t\n")
    pos = 0
    def take():
        nonlocal pos
        c = src[pos]; pos += 1; return c
    def number():
        c = take(); sign = -1 if c == T else 1; bits = ""
        while (c := take()) != L: bits += "1" if c == T else "0"
        return sign * int(bits or "0", 2)
    def lbl():
        s = ""
        while (c := take()) != L: s += "1" if c == T else "0"
        return s
    prog, labels = [], {}
    while pos < len(src):
        imp = take()
        if imp == T: imp += take()          # Tab IMPs are two chars
        kind = IMP[imp]; op, arg = take(), None
        if kind == "stack":
            if op == S: op, arg = "push", number()
            elif op == L: op = {"s": "dup", "t": "swap", "l": "drop"}[R(take())]
            else:
                op = {"s": "copy", "l": "slide"}[R(take())]; arg = number()
        elif kind == "arith":
            op = {"ss": "add", "st": "sub", "sl": "mul", "ts": "div", "tt": "mod"}[R(op + take())]
        elif kind == "heap":
            op = "store" if op == S else "load"
        elif kind == "flow":
            table = {"ss": ("mark", True), "st": ("call", True), "sl": ("jmp", True),
                     "ts": ("jz", True), "tt": ("jneg", True), "tl": ("ret", False),
                     "ll": ("end", False)}
            op, has_arg = table[R(op + take())]
            if has_arg: arg = lbl()
        else:
            op = {"ss": "putc", "st": "putn", "ts": "readc", "tt": "readn"}[R(op + take())]
        if op == "mark": labels[arg] = len(prog); continue
        prog.append((op, arg))
    return prog, labels

def run(prog, labels, inp=""):
    st, heap, calls, out = [], {}, [], []
    inp = iter(inp); ip = steps = 0
    while ip < len(prog):
        steps += 1
        if steps > 10_000_000: raise RuntimeError("step limit")
        op, arg = prog[ip]; ip += 1
        if op == "push": st.append(arg)
        elif op == "dup": st.append(st[-1])
        elif op == "swap": st[-1], st[-2] = st[-2], st[-1]
        elif op == "drop": st.pop()
        elif op == "copy": st.append(st[-arg - 1])
        elif op == "slide": del st[-arg - 1:-1]
        elif op == "add": b = st.pop(); st[-1] += b
        elif op == "sub": b = st.pop(); st[-1] -= b
        elif op == "mul": b = st.pop(); st[-1] *= b
        elif op == "div": b = st.pop(); st[-1] //= b
        elif op == "mod": b = st.pop(); st[-1] %= b
        elif op == "store": v = st.pop(); a = st.pop(); heap[a] = v
        elif op == "load": st.append(heap[st.pop()])
        elif op == "call": calls.append(ip); ip = labels[arg]
        elif op == "jmp": ip = labels[arg]
        elif op == "jz":
            if st.pop() == 0: ip = labels[arg]
        elif op == "jneg":
            if st.pop() < 0: ip = labels[arg]
        elif op == "ret": ip = calls.pop()
        elif op == "end": return "".join(out)
        elif op == "putc": out.append(chr(st.pop()))
        elif op == "putn": out.append(str(st.pop()))
    return "".join(out)

if __name__ == "__main__":
    import sys
    prog, labels = parse(open(sys.argv[1]).read())
    print(run(prog, labels, sys.stdin.read()), end="")
```

## JSFuck

`[]()!+` only. It is ordinary JS whose strings are assembled from
`(![]+[])[+[]]`-style indexing (`"false"[0]`), so evaluation needs nothing but
a JS engine. Verified primitives (node 24, podman-isolated):

```javascript
(![]+[])[+[]]                 // "f"
+[]+[] === "0"; +!+[] === 1   // numbers
([][[]]+[])                   // "undefined"
[]+{}                         // "[object Object]"
[]["fill"]["constructor"]     // Function — the escape hatch
[]["fill"]["constructor"]("return process")()   // works in node (verified)
```

An actual JSFuck blob from a challenge is untrusted code — decode by reading
or by generating your own via the standard encoder page (jsfuck.com) rather
than executing theirs. If you must execute:

```bash
podman run --rm -i docker.io/library/node:24-alpine node -
# paste the payload on stdin; process/require are reachable (verified)
```

Note: JSFuck uses exactly the six characters `[]()!+`. If a challenge hands you
JSFuck that ends in `()` it likely calls something; run it sandboxed and
observe, don't assume.

## Piet

Image of colored blocks (20 colors + black/white), program flow follows the
"codel" edges (DP left/right/up/down, CC toggle). Tool: `npiet`
(sourceforge project page; single-binary download) — `npiet file.png` prints
output. No local build here; document install, do not fetch while authoring.
Hand-decoding small Piet (a few codels) is feasible: stack ops map to exit
corner colors; keep a color→opcode chart from the Piet spec on hand.

## Substitution esolangs (Ook, Cow, Shortfuck, Emotion)

They are brainfuck with renamed symbols. Recover the mapping by symbol count
(8 distinct ops incl. `.` `,`) or by frequency (`+` most common usually), then
translate to brainfuck and use `scripts/bf.py`.

## Quiz/logic puzzles

Not a language but the other half of "misc": logic-grid puzzles, riddles,
knight/knave, number sequences. Approach: extract constraints literally into
`notes.md`, encode as a small python brute force or `sympy`/`z3` constraint
solve (`.venv` has sympy; `uv pip install --python .venv/bin/python z3-solver`
documented). Sequence puzzles: OEIS search first (agent web_search does this
well — give it the first terms verbatim).
