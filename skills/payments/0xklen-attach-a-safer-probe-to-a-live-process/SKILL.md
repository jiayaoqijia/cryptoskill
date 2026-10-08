---
name: attach-a-safer-probe-to-a-live-process
description: Use when a running process is misbehaving and restarting it would lose the state. Inspects it in place with non-destructive tools, capturing evidence before any intervention.
---

# Attach a Safer Probe to a Live Process

A hung or slow process holds the only evidence you need. Inspect its threads, stacks, and file descriptors from outside; kill nothing until you have captured and copied that evidence.

## Procedure

1. Identify the target precisely: `pgrep -af myservice` and confirm the pid, user, and start time so you never attach to the wrong one.
2. Check liveness cheaply first: `top -b -n1 -p <pid>` and `cat /proc/<pid>/status | grep -E 'State|Threads|VmRSS'`. A state of `D` points at I/O, `R` at CPU spin, `S` at a wait.
3. Take thread stacks non-invasively: `py-spy dump --pid <pid>` (Python), `jstack <pid>` (JVM), `gdb -p <pid> -batch -ex 'thread apply all bt'` (native), `pstack <pid>`. Do this twice, seconds apart.
4. Diff the two stack samples. A line that stays in the same frame is the stuck work; a line that moves is just activity.
5. Inspect open resources: `lsof -p <pid>` for leaked handles and `ss -tnp | grep <pid>` for connections in `CLOSE_WAIT` or `SYN_SENT`.
6. Snapshot heap or metrics if the runtime supports it without pausing long: `jcmd <pid> GC.heap_info`, `curl localhost:<port>/metrics`, or a `SIGQUIT` that triggers a graceful dump.
7. Copy every artefact out before acting: save stacks and outputs under `evidence/pid-<pid>-<time>/`.
8. Only then choose an intervention; prefer a graceful `SIGTERM` and a restart over `kill -9`, and never attach a write-capable debugger in production without a rollback.

## Pitfalls

- `gdb` with a breakpoint that halts all threads in production, turning a slowdown into an outage.
- Attaching with a thread-heavy sampler that itself adds latency; sample from outside the process.
- Killing with `kill -9` first, which discards the core and the answer.
- Assuming the newest pid is the one; supervisors restart children, so match start time.
- Reading a single stack sample and concluding "stuck in X" — one sample cannot distinguish wait from valid work.
- Leaving the process in an attached state (gdb stopped) while stepping away.

## Verification

    py-spy dump --pid "$(pgrep -f myservice | head -1)" > evidence/stack1.txt
    sleep 3
    py-spy dump --pid "$(pgrep -f myservice | head -1)" > evidence/stack2.txt
    diff evidence/stack1.txt evidence/stack2.txt
    # the unchanged frame across both dumps is the suspect; log the pid and timestamp with the capture

Report to the user: the pid and its state, the frame frozen across both samples, and the resource anomaly (fd or connection) if one exists.
