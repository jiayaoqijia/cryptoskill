---
name: verify-mtls-client-certificate
description: Use when configuring or debugging mutual TLS between services where the client must present a certificate. Verify the server validates the chain, checks the client identity, and rejects expired or unauthorized client certs rather than accepting any well-formed one.
---

# Verify mTLS client certificate

mTLS only adds security if the server actually validates the presented client cert against a trusted
CA and maps its identity. A server that reads "some cert is present" and moves on is doing nothing.

## Procedure

1. Generate/obtain a client cert signed by the internal CA and confirm its subject:
   ```bash
   openssl x509 -in client.crt -noout -subject -issuer -ext subjectAltName
   ```
2. Configure the server to require and verify client certs (Nginx example):
   ```nginx
   ssl_client_certificate /etc/ssl/internal-ca.crt;
   ssl_verify_client on;          # "optional" lets unauthenticated clients through
   ssl_verify_depth 2;
   ```
   `on` rejects clients with no cert; `optional` accepts them, which is the usual config mistake.
3. Prove a valid client cert is accepted:
   ```bash
   openssl s_client -connect api.internal:443 -servername api.internal \
     -cert client.crt -key client.key -CAfile internal-ca.crt </dev/null 2>&1 | grep -i 'Verify return'
   ```
4. Prove a *missing* cert is rejected:
   ```bash
   openssl s_client -connect api.internal:443 -servername api.internal </dev/null 2>&1 \
     | grep -iE 'alert|handshake'
   ```
   Expect a handshake failure / `certificate required` alert.
5. Prove a cert from the wrong CA (a public cert) is rejected, not just a missing one:
   ```bash
   openssl s_client -connect api.internal:443 -servername api.internal \
     -cert /etc/ssl/certs/public.crt -key public.key </dev/null 2>&1 | grep -i alert
   ```
6. Map the identity in the app: read `$ssl_client_s_dn` / `$ssl_client_verify` in Nginx, or the
   peer-cert subject in your gateway, and assert the CN/SAN equals the service identity before allowing
   the request:
   ```nginx
   if ($ssl_client_verify != SUCCESS) { return 496; }
   ```
7. Confirm expiry handling — a client cert that has expired should fail, tested with `-attime`:
   ```bash
   openssl verify -attime 2000000000 -CAfile internal-ca.crt client.crt   # simulate far future
   ```

## Pitfalls

- `ssl_verify_client optional` (or its gateway equivalent) accepts clients with no certificate at all.
- Verifying the chain but never checking the CN/SAN lets *any* cert from the internal CA act as any service.
- `ssl_verify_depth` too low rejects valid chains that include an intermediate.
- Revoking a compromised client cert needs CRL/OCSP configured; without it the cert works until expiry.
- Testing only the happy path (valid cert passes) misses the two failure cases that matter.
- Rotating the CA without reissuing client certs breaks every service at once on renewal day.
- Behind a load balancer that terminates TLS, the app never sees the client cert unless the LB forwards it — and then it is a header you must not trust blindly.

## Verification

    openssl s_client -connect api.internal:443 -servername api.internal \
      -cert client.crt -key client.key -CAfile internal-ca.crt </dev/null 2>&1 \
      | grep -E 'Verify return code|subject='

Pass means the valid client cert verifies (`Verify return code: 0`) and steps 4–5 fail with an alert.
Report: "mTLS required; valid client accepted, no-cert and wrong-CA rejected with handshake alerts,
CN mapped to service identity."
