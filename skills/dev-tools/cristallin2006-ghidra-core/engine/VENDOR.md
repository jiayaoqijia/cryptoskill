# VENDOR — ghidra-rpc

- **Upstream**: https://github.com/cellebrite-labs/ghidra-rpc (Cellebrite Labs)
- **Version**: 0.2.0 (pyproject.toml)
- **License**: MIT (per upstream README; upstream ships no LICENSE file)
- **Vendored**: 2026-09-15, from local clone `C:\Users\Lenovo\Desktop\ghidra-rpc-main\ghidra-rpc-main`
- **Install**: editable into `~/Desktop/src/ghidra-bridge/ghidra-rpc-venv`
  (`pip install -e engine/ghidra-rpc`) — patches below take effect live.

## dsh patches (each marked `# dsh-patch:` in source)

1. `ghidra_rpc/daemon.py` — create the endpoint directory before opening the
   daemon log file (upstream assumes `%LOCALAPPDATA%\ghidra-rpc` exists; with a
   redirected LOCALAPPDATA it does not).
2. `ghidra_rpc/session.py` / path handling — do NOT `Path.resolve()` the
   project path: resolving follows the `~/dsh-ghidra-workspace` junction back
   to `~/.dsh/...`, which Ghidra's ProjectLocator rejects ("Path element
   starting with '.'"). Use non-resolving absolutisation and derive the
   session/endpoint hash from the unresolved path so endpoints stay
   deterministic.
3. `ghidra_rpc/server/tools/memory.py` (`write_bytes`) — align with the skill's
   `patch_bytes.py`: temporarily grant write permission on the block, clear
   conflicting code units before writing, restore the flag afterwards, and
   report `instructions_cleared` in the result.
4. `ghidra_rpc/server/tools/disassembly.py` (`assemble`) — on
   AssemblySyntaxException retry once with the instruction text upper-cased
   (SLEIGH mnemonics are case-sensitive).

5. Custom dsh tools added under `ghidra_rpc/server/tools/dsh_tools.py`
   (exec_code, triage, export_binary, emulate_function) + CLI subcommands in
   `ghidra_rpc/cli.py`. These are additive, not patches to upstream logic.
   triage's packer detection is multi-signal by design (section names +
   `UPX!` magic scan of the raw file + structural heuristics, verdict in the
   `packer` block) — the old single section-name boolean misled agents when
   CTF authors renamed sections; `lang_hints.upx` is kept only as a compat
   field derived from the verdict.

When rebasing onto a newer upstream, re-apply the `# dsh-patch:` hunks and
re-check the tool registration in `server/tools/__init__.py`.
