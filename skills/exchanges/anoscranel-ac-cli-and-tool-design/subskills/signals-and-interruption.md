---
name: signals-and-interruption
domain: software-engineering/signals-and-interruption
trigger: "Handling an interrupted command without leaving broken state."
anti_trigger: "Not for process supervision, and not for service shutdown."
scope: "Ctrl-C, cleanup, and not leaving half a write."
status: seedling
---

# Signals and interruption

## Standard

An interrupted command is the normal case, not an exceptional one: a user presses Ctrl-C, a pipeline closes, a supervisor sends a termination signal. What distinguishes a well-behaved tool is that interruption leaves either the previous state or the completed state, never a partial one, and that the exit code reports the interruption rather than success.

The mechanics are a cleanup handler and an atomic write. The handler removes temporary artifacts and reports the interruption; the atomic write ensures that the file the tool was producing never appears half-finished. The harder case is a multi-step operation whose steps are not individually atomic, where the answer is a resumption marker rather than a cleanup.

Primary sources: <https://pubs.opengroup.org/> and <https://www.gnu.org/software/bash/>.

## Decision rules

- Record which signals the tool handles and which it lets terminate it.
- Record the cleanup performed on interruption and what it removes.
- Record the exit code associated with interruption, which should be conventional rather than zero.
- Record the temporary resources that must be cleaned: files, sockets, locks, and child processes.
- Record the multi-step operations and their resumption marker.
- Record the behaviour of children when the parent is interrupted.

## Procedure

1. Record the signals handled and the ones left to default behaviour.
2. Implement cleanup that removes temporary artifacts.
3. Write outputs atomically so a partial file never appears.
4. Record the resumption marker for multi-step work.
5. Ensure children are terminated with the parent.
6. Test interruption at several points in the run.

## Anti-patterns

- Swallowing the interrupt signal and continuing.
- Exiting zero after an interrupted run.
- Leaving temporary files behind on every interruption.
- Killing the parent and orphaning children.
- A multi-step operation with no way to tell how far it got.

## Done checklist

- [ ] Handled signals recorded.
- [ ] Cleanup recorded.
- [ ] Exit code recorded.
- [ ] Temporary resources enumerated.
- [ ] Resumption marker recorded.
- [ ] Child behaviour recorded.

The child process case is the one that leaves debris in practice: a parent that exits without terminating its children leaves orphaned work holding locks or ports, and the symptom appears on the next run as a failure that has nothing obviously to do with the interruption.


The exit code deserves the same care as the cleanup: a tool that is interrupted and returns zero tells the surrounding script that the work completed, and the script proceeds as if it had, which turns an interruption into a silent partial success that surfaces much later as missing data.

## Sources

- POSIX signals and utilities: <https://pubs.opengroup.org/>
- Shell process control: <https://www.gnu.org/software/bash/>
- CLI design guidance: <https://clig.dev/>
