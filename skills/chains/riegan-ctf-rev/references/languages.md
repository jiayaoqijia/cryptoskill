# Language-specific recovery

Triage target: `file`, `strings -n 6`, `readelf -d/-s`, section names. Match
row → follow its column. All "install" commands are to document/run on demand,
never during authoring.

| Runtime | Recognize by | Recover with | Install |
|---|---|---|---|
| C (stripped) | libc imports only | Ghidra + calling convention table below | preinstalled |
| C++ | `_Z` mangled, `_Unwind`, vtables | Ghidra demangler; manual vtable walk | preinstalled (`c++filt` in gcc) |
| Rust | `core::panicking`, `src/main.rs:` panic strings, `rust_begin_unwind` | Ghidra; panic locations as map | preinstalled |
| Go | `go:buildid`, `runtime.main`, pclntab | GolangAnalyzerExtension / `go tool objdump` | below |
| .NET | `_CorExeMain`, `mscoree.dll` import | ilspycmd | `dotnet tool install -g ilspycmd` |
| Java | `.jar`, `META-INF/MANIFEST.MF` | jadx; `javap -c` fallback | jadx release tarball |
| Python | `MEI` / `pyi-` strings, `python3xx.dll` | pyinstxtractor-ng + pycdc | below |
| Electron/Node | `app.asar`, `pkg-prelude` / `snapshot.bin` | `npx asar extract`; pkg unpackers | node/npm preinstalled |
| UPX (any) | `UPX!` magic, `UPX0..2` sections | `upx -d` | `sudo pacman -S upx` |
| .NET single-file | .NET bundle footer | `dotnet bundle-extract`-style tooling or single-file extract in ilspy; often just strings first | — |
| AutoIt | `AU3!EA06` / `>>>AUTOIT SCRIPT<<<` | Exe2Aut-style extractors (untrusted-binary caution) | upstream tools |
| AutoHotkey | `AutoHotkey` strings, `>-<` resource | resource dump + AHK decompilers | upstream tools |
| Flash/SWF | `FWS`/`CWS`/`ZWS` magic | Ruffle runs it (modern player, `pacman -S ruffle` or release); FFDec (JPEXS) for FLA/actionscript | below |
| GameMaker | `data.win`, `FORM` chunk | UndertaleModTool (GameMaker) | upstream release |
| Godot | `.pck` magic `GDPC` | gdsdecomp (Godot RE Tools) | upstream release |

## C — calling conventions (x86_64 SysV)

| Arg | Register | Callee-saved set |
|---|---|---|
| 1st | `rdi` | `rbx, rbp, r12–r15, rsp` |
| 2nd | `rsi` | everything else is caller-saved |
| 3rd | `rdi→rsi→` `rdx` | |
| 4th | `rcx` | return: `rax` (`rdx:rax` for 128-bit) |
| 5th | `r8` | struct>16B passed by pointer |
| 6th | `r9` | varargs: `al` = # of vector regs used |
| 7th+ | stack (`[rsp+8]` at entry, after return addr) | |

32-bit x86 (cdecl): all args on the stack, `[ebp+8]`, `[ebp+0xc]`, ...
Windows x64: `rcx, rdx, r8, r9` then stack; callee-saved `rbx, rdi, rsi, r12-r15` (different!).

In gdb at a call: `x/s $rdi`, `x/s $rsi` shows the first two pointer args.

## C++ specifics

- Demangle: `echo _ZN5Table6insertERK7Element | c++filt` (or `c++filt < file`).
- Vtable layout: object → `[0]=vptr` → vptr points at array of method pointers
  (after RTTI/offset-to-top header at vptr-8 in Itanium ABI). In Ghidra,
  apply a Structure to the vtable to name virtual calls.
- RTTI: `typeinfo` symbols (`_ZTI...`) reveal class names even semi-stripped.
- Constructors: the function writing the vtable pointer into `this` (`rdi`).

## Rust specifics

- Panic strings embed source paths: `panicked at src/check.rs:42:9` — that is
  a line-numbered map into the challenge source. Xref the string, read the
  surrounding logic.
- `core::panicking::panic`, `slice_index_len_fail` etc. mark bounds/assert
  checks; the code near them is validation logic.
- Common types: `&str` is (ptr,len) pair; `Vec<T>` is (cap, len, ptr) triple
  — read two/three registers, not one.
- Release builds are usually just C-like once demangled; `rustc-demangle`
  (`cargo install rustc-demangle` or the python `rustc_demangle` pkg) helps.

## Go specifics

- Almost never truly stripped: pclntab keeps function names. In Ghidra, use
  the GolangAnalyzerExtension (Ghidra 11.x ships Go support; older: install
  the extension release matching your Ghidra version) — it recovers names,
  strings (`go:string`), and types.
- Quick check without Ghidra: `go tool objdump -s 'main\.' binary` lists
  main-package symbols (needs go, preinstalled on this host).
- Plain `strings` on a Go binary contains function names and file paths —
  grep `main\.` to see the challenge's own functions.
- `runtime.main` calls `main.main`; goroutines start via `runtime.newproc`
  with the target fn as arg — xref it.
- Go calling convention (1.17+): args in registers `rax, rbx, rcx, rdi, rsi,
  r8, r9, r10, r11` then stack — NOT SysV.

## Java (.jar)

```bash
# jadx (release tarball from github.com/skylot/jadx releases → ~/.local/bin)
jadx -d out/ challenge.jar          # decompiled .java sources
jadx-gui challenge.jar              # interactive
# fallback, always available with JDK:
unzip -o challenge.jar -d jarx/
javap -c -p -classpath jarx com.example.Main   # bytecode listing
```

Obfuscated names: follow `main(String[])` from the manifest's `Main-Class`.

## .NET

```bash
dotnet tool install -g ilspycmd     # .NET SDK present via dotnet on host
ilspycmd challenge.exe -p -o out/  # project sources
ilspycmd challenge.exe > all.cs    # single dump
# GUI alternative: dnSpy/ILSpy on another box or via podman+wine; CLI is enough for CTFs
```

Look for `Main`, string decryption in static ctors, and
`ObfuscatorAttribute` (confuser/dnguard → dedicated de4dot: `dotnet tool` or
release).

## Python packaged (PyInstaller)

```bash
# 1. unpack
uv pip install --python .venv/bin/python pyinstxtractor-ng
.venv/bin/pyinstxtractor-ng challenge.exe     # → challenge.exe_extracted/
# 2. main script appears as compiled .pyc (often name-only, header stripped);
#    prepend pyc magic if needed, then decompile:
#    pycdc (decompyle++): build from source github.com/zrax/pycdc (cmake),
#    or try `uv pip install --python .venv/bin/python pycdc` wrappers.
pycdc extracted/main.pyc > main.py
# pip also has 'uncompyle6/decompyle3' for older pythons; pycdc covers newest.
```

Version hint: `python3xx.dll` inside the archive tells you the magic bytes.

## Node: pkg / Electron

```bash
# Electron asar:
npx asar extract app.asar out/          # then read the JS sources
# pkg single executable: look for the payload between markers
# (pkg stores a JSON index at the end / 'pkg-prelude' in strings);
# practical route: run it, find the extracted cache (pkg caches to tmp), or
# use upstream unpackers (pkg-unpacker / pkg-extract on github).
```

## UPX

```bash
sudo pacman -S upx
upx -d challenge -o challenge.unpacked
upx -t challenge           # integrity check first
```

If `-d` fails ("file is modified/hacked"), the author corrupted the UPX
header to break unpacking: fix l_info/p_info fields (compare against a fresh
`upx` pack of a similar ELF) or dump from memory after the stub runs
(`references/antidebug.md`).
