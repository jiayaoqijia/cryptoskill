---
name: config-bindings-generation
domain: software-engineering/config-bindings-generation
trigger: "Turning configuration from strings into typed values."
anti_trigger: "Not for choosing configuration values, and not for secrets management."
scope: "Typed configuration from schema to binding."
status: seedling
---

# Config bindings generation

## Standard

Configuration is data that crosses the same boundary as any other input, and a bindings generator treats it as such: a schema declares the fields, types, and defaults; the generator emits typed bindings that parse the raw configuration into checked values. The alternative — string lookups scattered through the code — validates each access by nothing, and the failure appears in production where a typo, a missing key, or a string where a number was meant first meets the code path.

The generation boundary is where the craft sits. Parse once at startup, fail fast at the boundary, and let the rest of the application consume typed values; or parse lazily per access and pay the failure at an arbitrary later time. Generated bindings push toward the first by construction, and the wiring decision is what the failure looks like at startup — a process that refuses to start with a message naming the key, versus one that starts and cannot serve.

Primary source: <https://12factor.net/>.

## Decision rules

- Record which configuration source the bindings parse: file, environment, or both, and precedence order.
- Generate from a checked-in schema, not from the live environment's current keys.
- Parse at the boundary and fail fast: an invalid value prevents startup with the key named.
- Record default values and require explicit action to change a default.
- Validate values at parse time that only runtime can use — ranges, enumerations, cross-field rules.
- Bind secrets by reference, never by embedding them in generated files or in the schema artifact.

## Procedure

1. Author the configuration schema with types, defaults, and validation constraints.
2. Generate bindings and wire parsing at startup with fail-fast semantics.
3. Record precedence between file and environment when both are supported.
4. Test the failure path: an invalid key stops startup naming the key.
5. Add cross-field validation to the schema where it is implementable at parse time.
6. Record the schema location, the generator, and the parse boundary.

## Anti-patterns

- String-typed lookups of typed configuration scattered through the code.
- Lazy parse per access, deferring failure to the code path that reads it.
- A schema coupled to a particular environment's current keys rather than to declared intent.
- Changing a default by editing the deployed environment instead of the schema.
- Secrets placed inside the generated binding artifacts.

## Done checklist

- [ ] Schema authored with types, defaults, constraints.
- [ ] Bindings generated and wired at startup.
- [ ] Precedence order recorded.
- [ ] Invalid key fails startup naming the key.
- [ ] Cross-field validation present where possible.
- [ ] Secrets referenced, not embedded.

## Sources

- Configuration in the environment: <https://12factor.net/>
- JSON Schema for configuration validation: <https://json-schema.org/>
- Fail-fast startup practice: <https://sre.google/sre-book/>
