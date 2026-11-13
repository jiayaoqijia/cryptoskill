---
name: provider-and-endpoint
domain: software-engineering/llm-api-integration
trigger: "Configuring base URLs, API versions, and authentication headers for a new LLM provider or local runtime"
anti_trigger: "Setting request body parameters or instructions (subskills/request-shape.md); handling rate limits and connection errors (subskills/error-and-resilience.md)"
scope: "Choosing the integration surface, base URLs, versioning paths, auth headers, and secret-manager key hygiene"
status: "seedling"
---

# Provider and Endpoint

## Standard

- **Twelve-Factor App Configuration**: configuration stored in environment variables, never hardcoded in source code or committed to version control. <https://12factor.net/config>
- **OWASP Secrets Management**: keys and credentials isolated from application code, rotated immediately upon exposure, and excluded from telemetry and logs. <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>

## Decision rules

- Choose hosted cloud APIs (such as Anthropic or OpenAI) for production workloads requiring high throughput and managed infrastructure, local runtimes (such as Ollama or vLLM) for offline development or strict data residency, and API gateways or multi-provider routers when fallback routing or unified billing is required.
- Configure base URLs using environment variables rather than hardcoded strings, supporting seamless switching between production endpoints, staging proxies, and local mocking servers.
- Transmit authentication credentials strictly via HTTP headers (`Authorization: Bearer $PROVIDER_API_KEY` or provider-specific headers such as `x-api-key`), never passing API keys in URL query parameters where they risk exposure in web server access logs and proxy caches.
- Scope API keys to minimum necessary permissions (such as read-only or restricted model endpoints) whenever the provider supports granular key generation.

## Procedure

1. Define configuration variables in the application environment using secure secret management tools or environment files excluded from version control.
2. Initialize the API client by reading the base URL and API key directly from environment variables at runtime initialization.
3. Construct request headers explicitly, attaching the required authentication header and content-type declarations (`application/json`).
4. Validate connectivity by dispatching a lightweight test request (such as listing available models or sending a minimal completion probe) before running batch or production workflows.
5. Implement key rotation procedures by updating environment secrets in the deployment manager without modifying application source code.

## Anti-patterns

- Hardcoding API keys directly into source code repositories or configuration files.
- Passing secret tokens as URL query string parameters in HTTP requests.
- Logging raw HTTP request headers or response payloads that contain active authorization credentials.
- Reusing a single administrator-level API key across multiple unrelated applications or environments.

## Done checklist

- [ ] Base URLs and endpoints are driven entirely by environment configuration.
- [ ] Authentication headers use secure bearer token patterns or provider headers.
- [ ] API keys are excluded from source code, logs, and telemetry output.
- [ ] Connection validation succeeds against the target provider endpoint.

## Sources

- The Twelve-Factor App, "Config", <https://12factor.net/config>
- OWASP Foundation, "Secrets Management Cheat Sheet", <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>

⚠️ Provider base URLs and versioning path conventions (such as `/v1/` prefixes) change periodically when APIs transition major versions; verify current provider documentation before deployment.
