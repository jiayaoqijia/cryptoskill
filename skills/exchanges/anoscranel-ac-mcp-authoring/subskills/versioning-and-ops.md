---
name: versioning-and-ops
domain: software-engineering/mcp-authoring
trigger: "Versioning MCP servers; managing breaking changes; capability negotiation; deprecating tools; publishing server packages"
anti_trigger: "Testing MCP servers (subskills/testing-and-debugging.md); designing tool schemas (subskills/tool-design.md)"
scope: "Operating MCP servers over time, semantic versioning, breaking change management, deprecation headers, and client contract documentation"
status: seedling
---

# Versioning and Ops

## Standard

- **Semantic Versioning Specification 2.0.0**: governing version numbers and breaking change rules for software libraries and servers. <https://semver.org>
- **Model Context Protocol Specification**: capability negotiation and protocol version compatibility standards. <https://modelcontextprotocol.io>
- ⚠️ Modifying existing tool parameter names or removing required fields is a breaking change requiring a major SemVer increment.

## Decision rules

1. If modifying tool parameters or removing capabilities, adhere to Semantic Versioning by incrementing major version numbers.
2. If deprecating an old tool version, maintain backward compatibility for at least one minor release cycle while issuing deprecation notices.
3. If negotiating protocol versions with clients, implement graceful fallback or clean rejection when versions are incompatible.
4. If publishing an MCP server package, maintain a comprehensive README documenting all tools, schemas, and environment configuration.
5. If releasing updates, automate release pipelines to verify schema contracts and lint documentation prior to publication.
6. ⚠️ Never introduce silent breaking changes to tool parameter types without updating the server version and notifying client operators.

## Procedure

1. Establish a Semantic Versioning release policy for the MCP server package.
2. Implement protocol capability negotiation handlers to inspect client version compatibility at startup.
3. Document all tools, resources, prompts, and environment variables clearly in the project README.
4. Set up deprecation notices and warning headers when phasing out legacy tool endpoints.
5. Configure automated CI release workflows to validate schemas and run contract tests before publishing.
6. Monitor server operational metrics and error rates following any production release update.

## Anti-patterns

- **Silent breaking changes.** Modifying tool parameter types or dropping fields without a major version bump. Fix: follow SemVer rigorously.
- **Abrupt removal of legacy tools.** Deleting old tool endpoints instantly without a deprecation warning period. Fix: use phased deprecation cycles.
- **Undocumented server deployments.** Publishing MCP packages without README instructions or schema references. Fix: maintain complete documentation.
- **Ignoring client version mismatches.** Allowing incompatible protocol versions to connect and fail unpredictably. Fix: enforce capability checks.

## Done checklist

- [ ] Semantic Versioning rules govern all server releases and updates.
- [ ] Protocol capability negotiation correctly handles version compatibility.
- [ ] The project README thoroughly documents all tools, schemas, and configs.
- [ ] Deprecation cycles provide adequate warning before tool removal.
- [ ] Automated CI pipelines validate contracts prior to publishing packages.

## Sources

- Semantic Versioning Specification 2.0.0: <https://semver.org>
- Model Context Protocol Specification: <https://modelcontextprotocol.io>
