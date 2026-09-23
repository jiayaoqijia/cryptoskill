# Embedded Signer Boundaries

An embedded signer receives sensitive key material only after its communication boundary is established.

- **Navigation policy mistaken for network isolation**: An origin allowlist does not block fetch, XHR, WebSocket or subresource requests. Enforce and test outbound denial before handing key material to embedded code.
- **Bridge messages trusted by assertion**: Parse messages as unknown and validate message-specific inputs/results. Missing transport and unmount must reject pending work promptly. Bound recovery retries and use one deadline across readiness and execution.
