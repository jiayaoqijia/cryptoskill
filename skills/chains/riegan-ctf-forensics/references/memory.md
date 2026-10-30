# Memory forensics — volatility3

Install into the repo venv (do not use system python):

```bash
uv pip install --python .venv/bin/python volatility3
scripts/ctf vol -f dump.vmem windows.pslist     # entrypoint: vol
```

First run against a Windows image downloads symbol tables (ISF json files)
from Microsoft's symbol server — needs network, ~100 MB, cached afterwards
(`~/.cache/volatility3/`). Offline events: pre-copy the cache or expect the
first plugin call to fail with a symbol error.

## Identify the dump

| Extension / signature | Source | Notes |
|---|---|---|
| `.raw`, `.mem`, `.dd` | raw physical memory | works if it is really raw RAM |
| `.vmem` / `.vmemx` | VMware | usually works directly |
| `.vmss` (+ vmem) | VMware suspended VM | if vol refuses the vmem, run `vmss2core` (bundled with VMware Workstation) to convert the suspended state to a core dump |
| `.dmp` | Windows crash/minidump | full dump fine; kernel dumps may need conversion |
| `.lime` | LiME (Linux) | raw-equivalent, needs matching kernel ISF |
| `MDMP` magic | process minidump | not a full image — wrong tool; use `strings` or a minidump parser/debugger |

OS check before touching vol:

```bash
strings -n 8 d.raw | grep -aE 'Windows|Linux version' | sort -u | head
```

## Windows — plugin order that wins challenges

Run in this order; each stage feeds the next.

1. **Process tree** — anomalies first:
   ```bash
   scripts/ctf vol -f d.vmem windows.pslist
   scripts/ctf vol -f d.vmem windows.pstree
   scripts/ctf vol -f d.vmem windows.cmdline
   ```
   Look for: weird parent-child (cmd.exe under explorer.exe is normal, under
   winlogon.exe is not), doubled lsass/smss, blank cmdlines, base64 or
   powershell encoded-command strings, timestamps far from the rest.
2. **Flag files before deep dives** (cheapest win in memory CTFs):
   ```bash
   scripts/ctf vol -f d.vmem windows.filescan | grep -aiE 'flag|desktop|downloads|temp|secret'
   scripts/ctf vol -f d.vmem windows.dumpfiles --pid <pid> --dump-dir out/
   ```
   `dumpfiles` writes the executable/dll/handle-backed files; grep the output
   dir with the router flag regex.
3. **Network**: `windows.netscan` — connections + listeners; correlate ports
   to suspicious PIDs; note reverse shells (one PID, many connections).
4. **Interactive history**:
   ```bash
   scripts/ctf vol -f d.vmem windows.consoles    # typed console history
   scripts/ctf vol -f d.vmem windows.envars      # per-process environment
   ```
   Flags hide in env vars and console backscroll.
5. **Persistence / registry**:
   ```bash
   scripts/ctf vol -f d.vmem windows.registry.hivelist
   scripts/ctf vol -f d.vmem windows.registry.printkey --key "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
   scripts/ctf vol -f d.vmem windows.shimcache
   scripts/ctf vol -f d.vmem windows.amcache      # program execution history
   ```
   Other keys worth printing: `...\RunOnce`, `...\Image File Execution
   Options`, `SAM\Domains\Account\Users\Names` (local/hidden accounts).
   Offline hive parsing details: `disk-docs.md#registry`.
6. **Credentials**: `windows.hashdump` (works straight off the dump) →
   offline cracking is `ctf-crypto` territory (hashcat mode 1000).
7. **Injection**: `windows.malfind` — suspicious RWX regions; add
   `--dump --dump-dir out/` to carve them, then `strings`/`ctf-rev`.

Useful extras: `windows.handles --pid X` (what a process holds open),
`windows.dlllist --pid X` (weird DLL paths), `windows.pslist --pid X --dump`
(full process memory to a .dmp — then strings + flag regex on that file).

Plugins accept `--output json` for scripting; `-v` prints symbol-resolution
detail when something errors.

## Linux dumps

Symbols are the whole game: vol needs an ISF matching the exact kernel build.

```bash
scripts/ctf vol -f d.lime linux.banners       # kernel banner -> which ISF you need
scripts/ctf vol -f d.lime linux.pslist
scripts/ctf vol -f d.lime linux.pstree
scripts/ctf vol -f d.lime linux.bash          # per-user bash history
scripts/ctf vol -f d.lime linux.lsof          # open files per process
scripts/ctf vol -f d.lime linux.check_syscall # hijacked syscall table
```

No matching ISF: generate one from the kernel image + debug symbols with
dwarf2json (procedure in the volatility3 repo), or use the ISF the challenge
author ships — drop it under `~/.cache/volatility3/symbols/` and re-run
`linux.banners` to confirm detection.

Practical order: banners → pslist (find the interesting PID) → bash history
(often contains the flag literally) → lsof that PID →
`linux.pslist --pid X --dump`.

macOS: `mac.pslist`, `mac.bash` exist; same ISF battle; rare in CTFs — run
strings first.

## Universal fallbacks (any dump, zero setup)

```bash
strings -n 8 d.raw | grep -aiE 'flag|ctf\{|passw|secret' | head -50
grep -aoE '[a-zA-Z0-9_]{2,16}\{[^}]{4,}\}' d.raw | sort -u | head
strings -el d.raw | grep -i flag      # UTF-16LE — Windows string encoding
```

The UTF-16 pass catches most "volatility found nothing" moments. If the
challenge ships a `.vmem` with `.vmx`/`.nvram`, read the `.vmx` as text — it
names the guest OS.

## Failure modes

| Symptom | Cause / fix |
|---|---|
| unsatisfied symbol / symbol table errors | wrong or missing ISF; check `linux.banners`, allow the symbol download (network), or install the provided ISF into the symbols cache dir |
| plugins run but return nothing | wrong OS profile or truncated dump; verify with strings, try the other OS plugin family, convert (.vmss/.dmp) or fall back |
| first plugin call very slow | symbols downloading mid-run; the next run is cached |
| `windows.filescan` empty | dump truncated mid-acquisition; fall back to strings |
