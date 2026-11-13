---
name: fds-and-ports
domain: software-engineering/fds-and-ports
trigger: "Diagnosing file descriptor exhaustion or ephemeral port exhaustion."
anti_trigger: "Not for connection pool sizing (that is connection-and-cursor-leaks)."
scope: "File descriptors, ephemeral ports, the TIME_WAIT pile, and their hard errors."
status: seedling
---

# File descriptors and ports

## Standard

Two hard-to-raise limits produce loud errors when hit. File descriptors: every socket, every open file, every pipe is one descriptor, and a process that opens without closing will hit its ulimit and see "too many open files" on the very next open — including opens the code makes for unrelated purposes, which is why the error appears in innocent places. Ephemeral ports: every outbound connection leases one from a finite range, and a client opening thousands of short connections to the same destination will see "address already in use" or silent connect failures.

The port case has a characteristic accumulation: connections closed by the client linger in TIME_WAIT, holding their port for a kernel-defined period. A workload that opens, closes, and reopens rapidly to one destination multiplies TIME_WAIT sockets until the range is consumed. The distinguishable signature is in the kernel counters — and the fix paths differ: reuse flags and connection pooling for ports, leak hunting or a raised limit for descriptors.

## Decision rules

- Check the process's descriptor count and its ulimit before theorising; both are one command.
- Group descriptors by type (sockets versus files) and by peer to find the leaker or the pile.
- For outbound storms, count TIME_WAIT sockets per destination before assuming a leak.
- Record the kernel's port range and reuse settings as they are actually configured.
- Watch the descriptor count over minutes; a sawtooth means churn, a staircase means leak.
- Verify after any limit change that the error class disappeared, not just the one error message.

## Procedure

1. Capture the error verbatim and the process's current descriptor count.
2. Compare count against ulimit.
3. Break down descriptors by type and peer.
4. Sample the count at intervals to read the curve.
5. For ports, count connections by state and destination.
6. Record the verdict: leak, churn pile, or limit set below need.

## Anti-patterns

- Raising the ulimit as the first move — it buys hours and destroys the evidence.
- Treating "too many open files" as a disk problem.
- Ignoring TIME_WAIT when the exhaustion is on outbound connections.
- Measuring once instead of over time.
- Changing the port range without reading the reuse flags available.

## Done checklist

- [ ] Descriptor count and ulimit recorded.
- [ ] Descriptor breakdown by type and peer.
- [ ] Curve sampled over minutes.
- [ ] Port states counted per destination.
- [ ] Kernel range and reuse settings recorded.
- [ ] Verdict recorded with the evidence.

## Sources

- Linux file descriptor limits: <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/>
- TCP state and TIME_WAIT: <https://www.rfc-editor.org/rfc/rfc9293>
- Socket options including reuse: <https://learn.microsoft.com/en-us/windows/win32/winsock/>
