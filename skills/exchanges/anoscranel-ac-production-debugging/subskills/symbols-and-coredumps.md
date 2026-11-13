---
name: symbols-and-coredumps
domain: software-engineering/symbols-and-coredumps
trigger: "Getting a crash dump that can actually be opened, and symbols that match it."
anti_trigger: "Not for reading the trace once opened (that is reading-stack-traces)."
scope: "Debug symbols, stripped binaries, and getting a core dump that can be opened."
status: seedling
---

# Symbols and core dumps

## Standard

A core dump is a snapshot of a process at its moment of death, and it is only usable if three things line up: the binary that produced it, the shared libraries it loaded, and the debug symbols that describe both. Production binaries are usually stripped — the symbol tables are removed to shrink them — so the dump and the symbols must come from the same build, and the symbol files are usually kept on a symbol server rather than shipped.

The other precondition is that the dump exists at all. Many production configurations disable core dumps because a core file can be as large as the process's memory and a crashing daemon that dumps cores repeatedly will fill a disk. The practical compromise is a limited dump, or a triggered capture on the next occurrence, or a diagnostic that preserves a thread list and a heap histogram instead of a full core.

## Decision rules

- Record the build identifier of the crashed binary before anything else; symbols are build-specific.
- Confirm whether core dumps are enabled and where they go; a full core of a large process fills disks.
- Confirm the debug symbols were archived for the production build; a stripped binary with no retained symbols is unreadable evidence.
- Prefer a limited capture — threads, registers, a heap histogram — when a full core is not affordable.
- Capture the loaded library list at crash time; the dump is meaningless without the matching builds of each library.
- Snapshot the machine state — memory pressure, disk, and ulimits — so the absence of a dump can itself be explained.

## Procedure

1. Note the binary's build identifier and the exact timestamp.
2. Check the dump location and size limits in the deployment configuration.
3. If a dump exists, verify the symbol files for that build are retrievable.
4. Open the dump with the tool matched to the runtime that produced it.
5. If no dump exists, configure a limited capture for the next occurrence.
6. Record what was captured and what the limits prevented.

## Anti-patterns

- Opening a dump with symbols from a different build.
- Assuming symbols from a local rebuild match the deployed binary.
- Copying a multi-gigabyte core to a laptop before checking what is needed from it.
- Leaving core dumps disabled without recording an alternative capture.
- Ignoring container settings; a container's core pattern may differ from the host's.

## Done checklist

- [ ] Build identifier recorded.
- [ ] Dump configuration checked in the deployment.
- [ ] Symbols for the build retrieved or their absence noted.
- [ ] Loaded libraries recorded.
- [ ] Alternative limited capture configured where needed.
- [ ] Capture limits and their consequences recorded.

## Sources

- ELF, build identifiers, and debug information: <https://refspecs.linuxfoundation.org/elf/elf.pdf>
- GNU debugger and core dump handling: <https://sourceware.org/gdb/documentation/>
- Symbol servers and minidumps on Windows: <https://learn.microsoft.com/en-us/windows/win32/debug/minidumps>
