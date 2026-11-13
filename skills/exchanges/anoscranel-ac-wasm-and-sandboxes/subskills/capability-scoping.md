---
name: capability-scoping
domain: software-engineering/capability-scoping
trigger: "Granting capabilities per guest instead of ambient authority."
anti_trigger: "Not for authentication design, and not for OS access control."
scope: "Granting capabilities per guest rather than ambient authority."
status: seedling
---

# Capability scoping

## Standard

The safe default for sandboxed code is zero capability, and every grant is explicit, scoped, and revocable. That model — capabilities rather than ambient authority — replaces questions like "can the guest read the filesystem" with "which handle did the host give this guest, and for how long". A guest holding a scoped handle to one object cannot reach a sibling, because there is no path to it, only the handles it was given.

The discipline lives in the host's provisioning code. A single shared import given to all guests is ambient authority in disguise; a per-instantiation set of imports and handles, decided by the caller's identity and task, is the capability model actually enforced. The record of what was granted is then the audit artefact, and revocation — dropping a handle, refusing re-instantiation — is the response tool when a guest misbehaves.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## Decision rules

- Default new guest classes to zero imports; add capabilities on documented need.
- Provision imports and handles per instantiation, not per process.
- Tie grants to the caller's identity and the task, and record the tie.
- Prefer per-object handles over class-wide operations.
- Define revocation: what is dropped, and what happens to in-flight work.
- Audit the grant set on each change, as a set, not incrementally.

## Procedure

1. Enumerate the capability grants for each guest class.
2. Move any class-wide grants to per-instantiation provisioning.
3. Bind each grant to a caller identity and task justification.
4. Convert ambient operations to handle-scoped ones.
5. Implement and test revocation paths.
6. Record the grant set and its justification.

## Anti-patterns

- One import set for every guest, tuned for the most demanding one.
- Handles that outlive their task.
- Grants without a recorded justification.
- Debug imports surviving into production provisioning.
- No tested revocation path.

## Done checklist

- [ ] Grant set per guest class enumerated.
- [ ] Per-instantiation provisioning in place.
- [ ] Grants tied to identity and task.
- [ ] Handle-scoped operations used.
- [ ] Revocation implemented and tested.
- [ ] Grant set recorded with justifications.

A further consequence is that capability grants become testable: an acceptance test can instantiate a guest class and assert the exact import set it receives, so a grant added for a debugging session fails the suite when it survives into provisioning, and the capability posture is enforced by a build rather than by a reviewer's memory.

## Sources

- Import provisioning model: <https://webassembly.github.io/spec/>
- Toolchain binding interfaces: <https://llvm.org/docs/>
- Interface design for untrusted callers: <https://capnproto.org/encoding.html>
