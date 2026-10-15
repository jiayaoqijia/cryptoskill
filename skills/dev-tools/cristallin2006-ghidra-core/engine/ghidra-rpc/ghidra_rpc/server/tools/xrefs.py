"""Cross-reference tools: xrefs to and from addresses/functions."""

from __future__ import annotations

from ghidra_rpc.server.main import register_handler
from ghidra_rpc.server.tools.decompiler import _find_function


def _resolve_address(pi, target: str):
    """Resolve a target (function name or hex address) to a Ghidra Address."""
    prog = pi.program
    af = prog.getAddressFactory()

    # Try as address
    if target.startswith("0x") or target.startswith("0X"):
        addr_str = target[2:]
        try:
            addr = af.getAddress(addr_str)
            if addr:
                return addr
        except Exception:
            pass

    # Try as function
    try:
        func = _find_function(pi, target)
        return func.getEntryPoint()
    except ValueError:
        pass

    # Try as symbol — prefer non-external (e.g. PLT thunk) over EXTERNAL space symbols.
    # In ELF binaries an imported function like 'malloc' has both a PLT thunk at a real
    # code address AND an entry in the EXTERNAL address space.  Callers reference the PLT
    # thunk, so we must prefer that address for xref lookups.
    st = prog.getSymbolTable()
    external_fallback = None
    for sym in st.getAllSymbols(False):
        if str(sym.getName()).lower() == target.lower():
            addr = sym.getAddress()
            if not addr.getAddressSpace().isExternalSpace():
                return addr  # non-external (PLT thunk / IAT entry) — use immediately
            if external_fallback is None:
                external_fallback = addr

    if external_fallback is not None:
        return external_fallback

    raise ValueError(f"Cannot resolve target '{target}' to an address.")


def _collect_xrefs_at(pi, addr, limit: int) -> list[dict]:
    """Collect real references to ``addr`` within a single program.

    When ``addr`` falls in the EXTERNAL address space (e.g. an imported
    function's EXTERNAL symbol), callers don't reference that synthetic
    address directly — they call through thunk/PLT stubs — so this also walks
    every thunk function whose immediate target is ``addr`` and includes its
    callers too.
    """
    rm = pi.program.getReferenceManager()
    fm = pi.program.getFunctionManager()

    addrs_to_check = [addr]
    if addr.getAddressSpace().isExternalSpace():
        for func in fm.getFunctions(True):
            if func.isThunk():
                try:
                    thunked = func.getThunkedFunction(False)
                    if thunked is not None and str(thunked.getEntryPoint()) == str(addr):
                        addrs_to_check.append(func.getEntryPoint())
                except Exception:
                    pass

    xrefs = []
    for check_addr in addrs_to_check:
        for ref in rm.getReferencesTo(check_addr):
            if len(xrefs) >= limit:
                break
            from_func = fm.getFunctionContaining(ref.getFromAddress())
            xrefs.append({
                "from_address": str(ref.getFromAddress()),
                "from_function": str(from_func.getName()) if from_func else None,
                "type": str(ref.getReferenceType()),
            })
        if len(xrefs) >= limit:
            break
    return xrefs


def _program_key(ctx, pi) -> str:
    """Look up the ``ctx.programs`` key for an already-resolved ProgramInfo."""
    with ctx._programs_lock:
        for key, candidate in ctx.programs.items():
            if candidate is pi:
                return key
    return pi.name


def _is_data_ref_type(type_str: str) -> bool:
    """True for DATA-family reference type strings (DATA, DATA_IND, ...)."""
    return "DATA" in type_str.upper()


def _read_pointer_at(pi, addr) -> int | None:
    """Read the pointer-sized little/big-endian value stored at ``addr``.

    Returns None when the address has no initialised bytes or the read fails.
    """
    mem = pi.program.getMemory()
    ptr_size = pi.program.getDefaultPointerSize()
    try:
        if ptr_size == 8:
            return mem.getLong(addr) & 0xFFFFFFFFFFFFFFFF
        if ptr_size == 4:
            return mem.getInt(addr) & 0xFFFFFFFF
        if ptr_size == 2:
            return mem.getShort(addr) & 0xFFFF
    except Exception:
        return None
    return None


def _looks_like_fatptr_descriptor(pi, desc_addr, target_addr) -> bool:
    """True when ``desc_addr`` holds a pointer to (near) ``target_addr``.

    Rust/Go strings are {ptr, len} fat pointers: the first word of the
    descriptor points at the string body. Allow a ±16 byte tolerance so
    descriptors pointing at a small header before the payload still match.
    """
    value = _read_pointer_at(pi, desc_addr)
    if value is None:
        return False
    return abs(value - target_addr.getOffset()) <= 16


def _follow_fatptr_second_hop(pi, addr, first_hop: list[dict], limit: int) -> list[dict]:
    """For DATA-type first-hop xrefs that look like fat-pointer descriptors,
    collect the second-hop references to each descriptor address.

    Each returned entry carries ``hop: 2`` and ``via: <descriptor address>``.
    Descriptors are de-duplicated; the combined result respects ``limit``
    (first-hop entries keep priority). No third hop is ever followed.
    """
    second_hop: list[dict] = []
    seen_descriptors = set()
    remaining = limit - len(first_hop)
    if remaining <= 0:
        return second_hop

    for xref in first_hop:
        if remaining <= 0:
            break
        if not _is_data_ref_type(xref.get("type", "")):
            continue
        desc_str = xref["from_address"]
        if desc_str in seen_descriptors:
            continue
        try:
            desc_addr = pi.program.getAddressFactory().getAddress(desc_str)
        except Exception:
            continue
        if desc_addr is None:
            continue
        if not _looks_like_fatptr_descriptor(pi, desc_addr, addr):
            continue
        seen_descriptors.add(desc_str)
        for x in _collect_xrefs_at(pi, desc_addr, remaining):
            x["via"] = desc_str
            x["hop"] = 2
            second_hop.append(x)
            remaining -= 1
            if remaining <= 0:
                break

    return second_hop


def _handle_xrefs_to(ctx, args: dict) -> dict:
    """Find cross-references TO a target (who calls/references this?).

    With ``all_binaries``, also searches every other currently loaded program
    for a symbol with the same fully-qualified name and merges in real
    callers found there (each entry then carries a ``binary`` field). This is
    necessary because Ghidra's ReferenceManager is per-Program: a call whose
    caller and target live in two different loaded binaries is invisible to
    a single-program getReferencesTo() lookup. Most commonly hit on multidex
    Android projects (a method called from a different classesN.dex than the
    one that defines it), but the limitation isn't DEX-specific — it applies
    to any project with more than one binary loaded in the daemon.

    With ``follow_fatptr``, DATA-type first-hop references whose from-address
    holds a pointer back to (within ±16 bytes of) the target are treated as
    Rust/Go {ptr, len} fat-pointer descriptors: references TO the descriptor
    are collected as a second hop and merged in, each tagged with
    ``via: <descriptor address>`` and ``hop: 2``. First-hop entries are
    tagged ``hop: 1``. The combined result respects ``limit`` (first hop
    has priority); no third hop is followed.
    """
    binary = args.get("binary", "")
    target = args.get("target", "")
    limit = args.get("limit", 50)
    all_binaries = bool(args.get("all_binaries", False))
    follow_fatptr = bool(args.get("follow_fatptr", False))

    if not target:
        raise ValueError("Missing required argument: target")

    pi = ctx.get_program(binary)
    addr = _resolve_address(pi, target)
    xrefs = _collect_xrefs_at(pi, addr, limit)

    if follow_fatptr:
        for x in xrefs:
            x["hop"] = 1
        xrefs.extend(_follow_fatptr_second_hop(pi, addr, xrefs, limit))

    if not all_binaries:
        return {"xrefs": xrefs, "count": len(xrefs)}

    # Tag same-binary results so the shape is uniform once other binaries are mixed in.
    own_key = _program_key(ctx, pi)
    for x in xrefs:
        x["binary"] = own_key

    sym = pi.program.getSymbolTable().getPrimarySymbol(addr)
    if sym is None or len(xrefs) >= limit:
        return {"xrefs": xrefs, "count": len(xrefs)}

    qualified_name = str(sym.getName(True))
    leaf_name = str(sym.getName())

    with ctx._programs_lock:
        other_programs = [(key, p) for key, p in ctx.programs.items() if p is not pi]

    for other_key, other_pi in other_programs:
        if len(xrefs) >= limit:
            break
        try:
            candidates = list(other_pi.program.getSymbolTable().getSymbols(leaf_name))
        except Exception:
            continue
        for cand in candidates:
            if str(cand.getName(True)) != qualified_name:
                continue
            for x in _collect_xrefs_at(other_pi, cand.getAddress(), limit - len(xrefs)):
                x["binary"] = other_key
                xrefs.append(x)
            if len(xrefs) >= limit:
                break

    return {"xrefs": xrefs, "count": len(xrefs)}


def _is_stack_ref(ref) -> bool:
    """Return True if the reference target is in the stack address space."""
    try:
        return ref.getToAddress().getAddressSpace().isStackSpace()
    except Exception:
        # Fall back to string check for safety
        return str(ref.getToAddress()).startswith("Stack")


def _handle_xrefs_from(ctx, args: dict) -> dict:
    """Find cross-references FROM a target (what does this call/reference?).

    When target is a function, iterates all instructions in the function body
    to collect outgoing references. When target is a specific address, only
    checks that address.
    """
    binary = args.get("binary", "")
    target = args.get("target", "")
    limit = args.get("limit", 50)
    no_stack = bool(args.get("no_stack", False))

    if not target:
        raise ValueError("Missing required argument: target")

    pi = ctx.get_program(binary)
    rm = pi.program.getReferenceManager()
    fm = pi.program.getFunctionManager()

    # Try to resolve as a function first — if so, scan all instructions
    func = None
    try:
        func = _find_function(pi, target)
    except ValueError:
        pass

    xrefs = []
    if func is not None:
        # Iterate over all instructions in the function body
        listing = pi.program.getListing()
        body = func.getBody()
        for insn in listing.getInstructions(body, True):
            for ref in insn.getReferencesFrom():
                if no_stack and _is_stack_ref(ref):
                    continue
                if len(xrefs) >= limit:
                    break
                to_func = fm.getFunctionAt(ref.getToAddress())
                if to_func is None:
                    to_func = fm.getFunctionContaining(ref.getToAddress())
                xrefs.append({
                    "from_address": str(ref.getFromAddress()),
                    "to_address": str(ref.getToAddress()),
                    "to_function": str(to_func.getName()) if to_func else None,
                    "type": str(ref.getReferenceType()),
                })
            if len(xrefs) >= limit:
                break
    else:
        # Single address lookup
        addr = _resolve_address(pi, target)
        for ref in rm.getReferencesFrom(addr):
            if no_stack and _is_stack_ref(ref):
                continue
            if len(xrefs) >= limit:
                break
            to_func = fm.getFunctionContaining(ref.getToAddress())
            xrefs.append({
                "from_address": str(ref.getFromAddress()),
                "to_address": str(ref.getToAddress()),
                "to_function": str(to_func.getName()) if to_func else None,
                "type": str(ref.getReferenceType()),
            })

    return {"xrefs": xrefs, "count": len(xrefs)}


register_handler("xrefs_to", _handle_xrefs_to)
register_handler("xrefs_from", _handle_xrefs_from)
