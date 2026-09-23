# Public Controller Contracts Must Be Versioned and Migration-Aware

A change to controller state shape, method signatures, event names or payloads, or package exports ships with a client migration plan and package-level consumer-style tests.

- **State shape changes without client migration** — Mobile/Extension selectors and hooks may break.
- **Method signature changes without compatibility plan** — exported controller methods need backward compatibility or coordinated client changes.
- **Event name/payload drift** — clients and metrics rely on stable events.
- **Package export changes without package-level tests** — changing exports must include consumer-style assertions.
