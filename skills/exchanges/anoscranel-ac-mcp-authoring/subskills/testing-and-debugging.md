---
name: testing-and-debugging
domain: software-engineering/mcp-authoring
trigger: "Testing MCP servers; validating tool schemas; using the MCP inspector for interactive debugging; writing contract tests"
anti_trigger: "Auditing server security (subskills/security-model.md); versioning and publishing (subskills/versioning-and-ops.md)"
scope: "Systematic validation of tool schemas, transport smoke tests, contract testing, interactive debugging with the MCP inspector, and clean logging"
status: seedling
---

# Testing and Debugging

## Standard

- **Model Context Protocol Inspector Documentation**: interactive debugging and schema validation tooling for MCP servers. <https://modelcontextprotocol.io>
- **Contract Testing Best Practices**: verifying protocol compliance and message payload integrity across client-server boundaries. <https://martinfowler.com/bliki/ContractTest.html>
- ⚠️ Automated test suites must validate JSON-RPC message framing and schema compliance under simulated transport interruptions.

## Decision rules

1. If developing a new tool, write automated contract tests that validate input schema compliance and expected output structures.
2. If troubleshooting connection or message framing issues, use the official MCP inspector for interactive protocol inspection.
3. If testing server transport resilience, simulate abrupt client disconnections and verify graceful server cleanup.
4. If logging debugging information during test execution, ensure structured log levels prevent test runner pollution.
5. If mocking external API dependencies in tool tests, use deterministic fixtures to ensure repeatable test outcomes.
6. ⚠️ Never rely solely on manual end-to-end agent testing; automated schema contract tests are mandatory for regression safety.

## Procedure

1. Set up an automated testing framework configured for JSON-RPC message exchange.
2. Write unit tests for each tool verifying input validation against compiled JSON Schemas.
3. Implement contract tests covering resource URI resolution and prompt template rendering.
4. Launch the MCP inspector tool interactively to inspect capability negotiation and message payloads.
5. Execute transport smoke tests simulating local stdio and remote HTTP message streams.
6. Review server log output to confirm debugging records are clean, informative, and free of leaked secrets.

## Anti-patterns

- **Manual-only testing.** Testing MCP servers exclusively by chatting with an agent without automated validation. Fix: add contract test suites.
- **Ignoring schema drift.** Failing to update automated tests when tool parameter schemas evolve. Fix: tie tests to schema definitions.
- **Polluting test output.** Printing verbose raw byte streams during test runs without formatting. Fix: use structured test loggers.
- **Flaky external mocks.** Relying on live third-party network APIs during unit testing. Fix: use isolated deterministic fixtures.

## Done checklist

- [ ] Automated contract tests cover all tools, resources, and prompt endpoints.
- [ ] JSON-RPC message framing and schema compliance are verified in CI.
- [ ] The MCP inspector is utilized for interactive protocol debugging.
- [ ] Transport smoke tests validate stability under simulated disconnections.
- [ ] Logging output remains clean, structured, and secret-free.

## Sources

- Model Context Protocol Inspector Documentation: <https://modelcontextprotocol.io>
- Contract Testing Best Practices: <https://martinfowler.com/bliki/ContractTest.html>
