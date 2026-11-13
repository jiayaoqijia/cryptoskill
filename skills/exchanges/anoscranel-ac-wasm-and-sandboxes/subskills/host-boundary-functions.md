---
name: host-boundary-functions
domain: software-engineering/host-boundary-functions
trigger: "Designing the host functions a guest may call."
anti_trigger: "Not for public API design, and not for RPC protocol design."
scope: "The explicit interface where guest code calls a host that chose to be reachable."
status: seedling
---

# Host boundary functions

## Standard

Every capability a guest has is a host function the host chose to provide. The boundary is import declarations in the guest matched against provisioning in the host, and the resulting surface is a policy decision: a host that exposes a generic file-write import has granted nothing beyond what it intended, while one that exposes scoped, object-handled operations has kept the policy where it belongs.

The design rules are familiar from API craft with a stricter cost model. Each import is a trust grant to code that may be hostile, so parameters must be validated at the boundary — lengths, indices, resource handles — and errors must return as values the guest can branch on, not as exceptions across a boundary the guest may not handle. The import set is also the audit unit: the sum of what a guest can do is exactly its import list, so the list is reviewed as a whole rather than function by function.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## Decision rules

- List every import provided to a guest class; that list is its total capability.
- Validate every boundary parameter: lengths, indices, handles, before use on the host side.
- Return errors as values with documented failure modes the guest can handle.
- Prefer handle-based, scoped operations over ambient ones like paths.
- Review the import set as a whole for each guest class, on change.
- Record each import's intended caller justification with the function's documentation.

## Procedure

1. Enumerate the imports each guest class receives.
2. For each import, write what it grants and to whom.
3. Validate all parameters at the host edge.
4. Define error returns the guest can branch on.
5. Scope operations through handles where possible.
6. Review the import list as a unit; record the review.

## Anti-patterns

- Providing a generic escape hatch import for debugging and shipping it.
- Trusting guest-supplied lengths or indices without validation.
- Exceptions crossing a boundary the guest cannot handle.
- Ambient path-style imports where handles would scope.
- Reviewing imports one at a time, missing the aggregate.

## Done checklist

- [ ] Import set enumerated per guest class.
- [ ] Each import grants a stated capability.
- [ ] Boundary validation implemented.
- [ ] Error values defined.
- [ ] Handles used where scoping matters.
- [ ] Import set reviewed as a whole.

## Sources

- Import mechanism: <https://webassembly.github.io/spec/>
- Toolchain binding conventions: <https://llvm.org/docs/>
- Structured interface pattern: <https://capnproto.org/encoding.html>
