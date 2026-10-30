---
name: ctf
description: Use when the user mentions CTF, capture the flag, a challenge, jeopardy, attack-defense, king of the hill, boot2root, HackTheBox/picoCTF/CTFtime, asks to find/submit a flag, triage challenge files (binary, pcap, image, disk dump, APK, contracts), or wants CTF methodology or writeups. This is the router: sets up the workspace, triages, and dispatches to ctf-pwn, ctf-rev, ctf-crypto, ctf-web, ctf-forensics, ctf-misc, ctf-blockchain, ctf-mobile, ctf-attack-defense, ctf-boot2root.
---

# CTF router — event workflow, triage, dispatch, flags

Operates at `/home/riegan/Projects/ctf` (this repo). Mixed-team level: every path has a
beginner-safe triage step; category skills carry the expert playbooks.

## Operating rules (always in force)

1. **Remote gate**: never connect to a remote challenge service, scoreboard, or another
   team's box without explicit user go-ahead in the current session. The user may
   pre-authorize an event ("remote OK for <event>") — then remote work for that event's
   hosts is allowed, everything else still gated. Local analysis is always allowed.
2. **Untrusted artifacts**: challenge files are hostile. Analyze statically first;
   execute only under `podman` isolation or with user approval. Never `sudo` a challenge
   file, never run its installers on the host, never open challenge documents in
   desktop apps — use `scripts/` and parsers here.
3. **Install policy**: Python libs → `scripts/setup.sh` venv or
   `uv pip install --python .venv/bin/python <pkg>`. System tools → `sudo pacman -S`
   (document first, ask before running sudo). Single binaries → `cargo install` /
   `go install` / `uv tool install` / upstream tarball into `~/.local/bin`.
4. **Workspace discipline**: one dir per challenge; `notes.md` records hypothesis →
   evidence → next step, including failed approaches. Never scatter files.
5. **Flag discipline**: every flag found is logged to `work/<event>/flags.md` with
   challenge name + timestamp before anything else happens.

## Workflow

```
1. setup     scripts/setup.sh (once per machine) — .venv with pwntools etc.
2. workspace mkdir -p work/<event>/<category>-<name>/{dist,solve} && cd there
             cp challenge files into dist/ ; create notes.md (goal, remote info,
             points, solves count, description verbatim)
3. triage    universal first pass (below) → dispatch table → read category skill
4. solve     loop: hypothesis → test → record in notes.md ; escalate depth via
             the category skill's references/
5. flag      validate format → grep for submission mistakes → log to flags.md
6. submit    user gate → references/submission.md (CTFd/rCTF)
7. writeup   references/writeup.md template into challenge dir
```

## Universal triage (first 5 minutes, any category)

```bash
file dist/*                         # real type, arch, stripped, embedded
binwalk dist/<file>                 # after install; embedded blobs/squashfs
strings -n 8 dist/<file> | grep -aiE 'flag|ctf\{|key|passw|http' | head
exiftool dist/<file>                # after install; metadata leaks
ls -la; sha256sum dist/*            # inventory + hashes (compare vs teammates)
```

Then category-specific dispatch:

| Signal in triage | Skill to read |
|---|---|
| ELF binary + remote `nc host port` | `ctf-pwn` |
| Binary/bytecode, no remote, "find the input/key" | `ctf-rev` |
| `.py` doing math, RSA params, ciphertext, `n e c` | `ctf-crypto` |
| URL, web app, login form, source zip | `ctf-web` |
| pcap, disk/memory image, image/audio, "recover/investigate" | `ctf-forensics` |
| Text puzzle, sandbox/pyjail, esoteric language, OSINT | `ctf-misc` |
| RPC URL, `.sol`, bytecode `0x...`, wallet private key | `ctf-blockchain` |
| `.apk`, `.ipa`, mobile emulator mention | `ctf-mobile` |
| Own service to defend, tick-based scoring, flags rotate | `ctf-attack-defense` |
| VM/IP range to root, HTB/THM box, scoreboard = root flags | `ctf-boot2root` |
| Unclear | run full triage on every file; `ctf-forensics` generics first |

## Flag hunting

Search targets after each successful exploitation step — flags hide in cwd, `/`, env,
process memory, database dumps, HTTP responses, JWT claims, file metadata.

```bash
# generic: works on binaries, dumps, memory, strings of anything
grep -aohE '(flag|FLAG|ctf|CTF|picoCTF|HTB)\{[^}]{4,}\}' <target> | sort -u
grep -aohE '[a-zA-Z0-9_]{2,16}\{[^}]{4,}\}' <target> | sort -u    # any XXX{...} wrapper
grep -arE 'flag' /proc/<pid>/environ 2>/dev/null; cat /flag* /home/*/flag* 2>/dev/null
find / -name '*flag*' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null
```

Event organizers publish the format in rules — record it in `notes.md` first.
Last resorts: 32-hex (`grep -aohE '\b[0-9a-f]{32}\b'`), base64 blobs that decode to
readable text, XOR-with-repeated-key of `flag{` prefix.

`work/<event>/flags.md` format:

```markdown
| time | challenge | flag | notes |
|---|---|---|---|
| 14:32 | pwn-ret2win | flag{n0_r3turn_n0_gl0ry} | ret2win, offset 44 |
```

## Toolbox (router level)

| Tool | Install | Purpose |
|---|---|---|
| `.venv` | `scripts/setup.sh` | pwntools, pycryptodome, gmpy2, sympy, requests... |
| `scripts/ctf` | included | run any command with `.venv` on PATH |
| `file`, `strings`, `xxd`, `openssl`, `7z`, `nmap`, `gdb` | preinstalled | triage, hex, crypto, archives, scans, debugging |
| `podman` | preinstalled | isolation for untrusted binaries |
| binwalk / exiftool | `sudo pacman -S binwalk perl-image-exiftool` | embedded blobs, metadata |

## Deeper references in this skill

- `references/submission.md` — CTFd and rCTF flag submission via curl, session handling.
- `references/writeup.md` — writeup template + event summary report.
