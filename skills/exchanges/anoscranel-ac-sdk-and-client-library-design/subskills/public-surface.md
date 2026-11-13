---
name: public-surface
domain: software-engineering/public-surface
trigger: "Deciding what a client library exposes."
anti_trigger: "Not for HTTP endpoint design, and not for internal module boundaries."
scope: "What to expose, what to hide, and the cost of every public name."
status: seedling
---

# Public surface

## Standard

Every public name is a commitment: someone will call it, and removing it becomes a breaking change. The surface therefore grows monotonically unless the library treats publication as a decision rather than a default, and most libraries in the wild expose ten times what their callers use because exposing was easier than deciding.

The useful discipline is to publish a small set of types that compose, and to keep everything else internal by default. A client whose primary object exposes a request method, a few configuration options, and a typed error hierarchy is easier to keep stable than one that exposes its HTTP transport, its retry policy, and its serialiser, because the latter leaks mechanisms that must then be supported.

Primary sources: <https://semver.org/> and <https://www.rfc-editor.org/rfc/rfc9110>.

## Decision rules

- Record the public types and the reason each is public.
- Record what is deliberately internal and how that is enforced, since a convention is not enforcement.
- Record the primary entry point and whether there is exactly one.
- Record any escape hatch for advanced use, and mark it as unsupported if it is.
- Record the deprecated names and their replacements.
- Record the review that decides publication, since a default of public is a decision to grow the surface.

## Procedure

1. List the public types and record the justification for each.
2. Identify mechanisms that leaked into the surface and record a plan to hide them.
3. Confirm a single entry point.
4. Record the escape hatch and its support status.
5. Record deprecations.
6. Write the surface inventory.

## Anti-patterns

- Exposing everything because hiding requires effort.
- An escape hatch that is used by most callers, which means the main surface is wrong.
- Multiple entry points that behave slightly differently.
- Internal conventions that are not enforced by the language's visibility rules.
- Deprecated names left indefinitely with no removal date.

## Done checklist

- [ ] Public types listed with reasons.
- [ ] Internal mechanisms recorded with enforcement.
- [ ] Entry point recorded.
- [ ] Escape hatch and support status recorded.
- [ ] Deprecations recorded.
- [ ] Publication review recorded.

The escape hatch also needs a support statement: an advanced option that the library's own team uses in production is supported whether or not it is documented as such, and a caller who discovers it through reading source has found an undocumented commitment rather than an undocumented feature.


## Sources

- Semantic versioning for libraries: <https://semver.org/>
- HTTP client behaviour: <https://www.rfc-editor.org/rfc/rfc9110>
- API evolution context: <https://www.w3.org/>
