---
name: tls-termination
domain: software-engineering/tls-termination
trigger: "Deciding where TLS ends and how certificates are kept alive."
anti_trigger: "Not for protocol-level security analysis, and not for internal service mesh mTLS."
scope: "Where TLS ends and what the certificate lifecycle costs."
status: seedling
---

# TLS termination

## Standard

TLS terminates where encrypted traffic becomes plaintext, and that point is a placement decision with consequences. Terminating at the edge load balancer is common and operationally simple — certificates live in one place, and the internal path is a network the operator controls — but the plaintext then traverses that internal network, which is a boundary decision, not an inconvenience. Terminating at each instance moves the key material outward and the certificate management burden with it.

The certificate lifecycle is the part that fails in production. A certificate has a validity window and expires without ceremony; the expiry that takes a service down is the one nobody was watching, because the person who installed it moved on and the renewal reminder went to a list that no longer exists. Automated renewal with an alert on renewal failure is the control; the alert is the part that matters, because the automation that renews ninety-nine times fails on the hundredth.

Primary source: <https://www.rfc-editor.org/>.

## Decision rules

- Record where TLS terminates for each public route and what network plaintext traverses.
- Record every certificate's issuer, scope, expiry, and renewal method.
- Alert on renewal failure, not on expiry; expiry alerts arrive too late to act on.
- Record the minimum protocol versions and cipher policy the edge enforces.
- Verify the full chain serves correctly after any certificate change.
- Record the client-side impact of any version policy change before enforcing it.

## Procedure

1. Document termination points and plaintext paths.
2. Inventory certificates with expiries and renewal methods.
3. Confirm renewal automation and alerting on its failure.
4. Test a renewal end to end before relying on it.
5. Verify the served chain and protocol versions from outside.
6. Record the policy and the verified behaviour.

## Anti-patterns

- Expiry monitoring without renewal-failure monitoring.
- Termination placement decided by convenience without recording the boundary.
- A certificate change that was never verified from outside the network.
- Protocol version policy raised without checking the client population.
- Renewal automation that was configured once and never tested again.

## Done checklist

- [ ] Termination points and plaintext paths recorded.
- [ ] Certificate inventory recorded.
- [ ] Renewal automation and failure alerting confirmed.
- [ ] Renewal tested end to end.
- [ ] Chain and versions verified externally.
- [ ] Policy recorded.

## Sources

- TLS 1.3 specification: <https://www.rfc-editor.org/rfc/rfc8446>
- Certificate lifecycle and ACME automation: <https://www.rfc-editor.org/rfc/rfc8555>
- HTTP over TLS conventions: <https://www.rfc-editor.org/rfc/rfc9110>
