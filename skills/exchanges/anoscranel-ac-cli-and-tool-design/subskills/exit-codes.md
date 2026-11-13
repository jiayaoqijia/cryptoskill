---
name: exit-codes
domain: software-engineering/exit-codes
trigger: "Choosing what a command returns to the shell."
anti_trigger: "Not for HTTP status codes, and not for error message wording."
scope: "What each code means, and the script that consumes it."
status: seedling
---

# Exit codes

## Standard

An exit code is a boolean with room for detail, and most of that detail is wasted because scripts only test for zero. The convention that matters is simple: zero means success, non-zero means failure, and a small set of distinct values lets a caller distinguish the kinds of failure it might handle differently.

The design question is which distinctions are worth a code. A caller that can retry a transient failure benefits from distinguishing it from a permanent one; a caller that checks whether a resource exists benefits from a distinct code for absence. Beyond a handful, the codes are documentation rather than interface, and a documented enumeration that a caller must read is often worse than a clear error message on stderr.

Primary sources: <https://pubs.opengroup.org/> and <https://www.gnu.org/software/bash/>.

## Decision rules

- Record the meaning of each exit code the tool can return.
- Record which codes a caller is expected to branch on, and keep that set small.
- Record the code used for usage errors, distinct from runtime failures.
- Record the code used when the requested result is absent, if that is not an error.
- Record that signals produce their own conventional codes rather than a generic failure.
- Record the codes the tool must not return because they collide with a shell's special meanings.

## Procedure

1. Enumerate the failure classes the tool can produce.
2. Assign codes to the classes a caller might handle.
3. Reserve a code for usage errors.
4. Record the absence case explicitly, since it is often not a failure.
5. Verify signal termination produces the conventional value.
6. Record the enumeration in the help output.

## Anti-patterns

- Returning a generic failure for every error.
- Using a code that a shell reserves for its own purposes.
- Treating a normal absence as an error.
- An enumeration so long that no caller branches on it.
- Returning success after a partial write.

## Done checklist

- [ ] Codes enumerated with meanings.
- [ ] Branchable set kept small and recorded.
- [ ] Usage error code reserved.
- [ ] Absence case recorded.
- [ ] Signal codes verified.
- [ ] Enumeration in help output.

The distinction that earns its own code most often is absence: a tool asked for a resource that does not exist has not failed, and a script that cannot tell absence from failure either treats a normal case as an error or swallows a real one. One code, documented, removes the ambiguity.


## Sources

- POSIX utility conventions: <https://pubs.opengroup.org/>
- Shell behaviour reference: <https://www.gnu.org/software/bash/>
- Command-line interface guidelines: <https://clig.dev/>
