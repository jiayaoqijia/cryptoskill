---
name: ssrf
domain: security-hardening/ssrf
trigger: Building any feature where the server fetches a user-supplied or user-influenced URL — link previews, webhooks, image proxies, imports — and needing to keep that fetch off internal systems.
anti_trigger: Validating generic input (subskills/input-output.md); controlling how much a fetch may consume (subskills/api-security.md).
scope: Outbound-fetch allow-lists, metadata endpoints, redirects
status: seedling
---

# Server-Side Request Forgery

## Standard

- OWASP Server Side Request Forgery Prevention Cheat Sheet: allow-list protocols, domains and ports; block private IP ranges (https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).
- OWASP ASVS 5.0 **V1.3.6 (L2)** for outbound-request restrictions.
- SSRF is folded into OWASP Top 10 A01:2025 and is API7 in the 2023 API Top 10.
- The canonical target is the cloud metadata service at `169.254.169.254`, which hands out the instance's IAM credentials.

## Decision rules

1. Every outbound fetch gets an explicit allow-list: scheme (https only), host, and port. No fetch outside it.
2. Resolve the hostname and check the resolved IP before connecting; re-check after every redirect hop.
3. Block private, loopback, link-local and reserved ranges — including IPv4-mapped IPv6 forms (`::ffff:169.254.169.254`), which naive filters miss.
4. Disable HTTP redirects, or cap the hops and validate each hop against the same allow-list.
5. Restrict egress at the network layer too: a compromised app should not reach the metadata service or arbitrary hosts.
6. Give the fetching workload its own minimal credential — never the instance's privileged role.

## Procedure

1. Centralise every outbound fetch in one module; ban direct `fetch`/`requests.get` on user-supplied URLs elsewhere.
2. In the module: parse the URL, check the scheme allow-list, resolve DNS, check the IP against the private/reserved list, then connect.
3. Pin or re-validate the IP on connect (DNS-rebinding defence); fail closed if the resolution changes.
4. Set a per-request timeout and a response size cap (subskills/api-security.md limits).
5. Handle redirects manually with the same checks per hop, or refuse redirects outright.
6. Test with the classic payloads: `http://169.254.169.254/`, `http://127.0.0.1:6379/`, `http://[::ffff:169.254.169.254]/`, a hostname resolving to `10.0.0.5`, and a redirect to a private address.

## Anti-patterns

- Passing a user-supplied URL to a fetch call with only a "no localhost" string check.
- Checking the hostname but connecting to a freshly-resolved, different IP (rebinding).
- Following redirects without re-validating each hop.
- Running the fetcher under the instance's privileged role.
- Filtering IPv4 only, while the resolver hands back IPv6.

## Done checklist

- [ ] One fetch module owns all outbound requests.
- [ ] Scheme, host and port allow-list enforced.
- [ ] DNS resolved and IP checked against private/reserved ranges, IPv6 included.
- [ ] Redirects re-validated per hop or disabled.
- [ ] Metadata endpoint unreachable from the workload (network egress rule).
- [ ] Rebinding test cases pass; fetcher runs under a minimal credential.

## Sources

- Primary: OWASP SSRF Prevention Cheat Sheet; OWASP Top 10 2025 A01; OWASP API Security Top 10 2023 API7; OWASP ASVS 5.0 V1.3.6.
- <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>
- <https://owasp.org/Top10/>
