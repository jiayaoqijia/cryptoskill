---
name: debug-tls-handshake-with-openssl
description: Use when an HTTPS call fails with a certificate, SNI, chain, or protocol error. Drive openssl s_client by hand to see the offered protocol, the served chain, and the exact verification error instead of reading a wrapped HTTP client error.
---

# Debug TLS handshake with openssl s_client

Application clients hide the handshake. `ssl_error_handshake_failure` could be a wrong SNI, a missing
intermediate, an expired cert, or a protocol mismatch. Talk TLS directly and read the wire.

## Procedure

1. Connect and force the SNI the client would send — without it a shared IP serves the wrong cert:
   ```bash
   openssl s_client -connect example.com:443 -servername example.com </dev/null
   ```
   Read `Verify return code`. `0 (ok)` is success; anything else is the real error.
2. Print only the served cert and its validity window:
   ```bash
   echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
     | openssl x509 -noout -subject -issuer -dates
   ```
3. Show the full chain the server sends, which reveals a missing intermediate:
   ```bash
   echo | openssl s_client -connect example.com:443 -servername example.com -showcerts 2>&1 \
     | grep -E 'subject=|issuer='
   ```
   If the leaf's `issuer` never appears as a `subject` in the chain, the intermediate is missing and
   some clients (not browsers that cache it) will fail.
4. Test the protocol/cipher combination the failing client uses:
   ```bash
   openssl s_client -connect example.com:443 -servername example.com -tls1_2 </dev/null 2>&1 | head -1
   openssl s_client -connect example.com:443 -servername example.com -tls1_3 </dev/null 2>&1 | head -1
   ```
5. Verify the leaf against the system trust store from the *failing host*:
   ```bash
   openssl s_client -connect example.com:443 -servername example.com -CAfile /etc/ssl/certs/ca-certificates.crt </dev/null
   ```
   A `unable to get local issuer certificate` here means the client's trust store is stale.
6. For mTLS failures, add the client cert and read the alert:
   ```bash
   openssl s_client -connect api.example.com:443 -servername api.example.com \
     -cert client.crt -key client.key 2>&1 | grep -i alert
   ```

## Pitfalls

- Omitting `-servername` gets the default vhost's cert; the failure then looks unrelated to your hostname.
- A browser succeeding proves nothing — it caches intermediates and has a different trust store.
- `Verify return code: 0` still prints when no `-CAfile` was given on some builds; check the return code line, not the presence of a key exchange.
- Testing from your laptop but failing in a container usually means a different CA bundle or a missing `ca-certificates` package.
- An expired intermediate breaks clients even when the leaf is valid.
- `openssl s_client` does not send SNI by default on older builds; set it explicitly every time.

## Verification

    echo | openssl s_client -connect example.com:443 -servername example.com 2>&1 \
      | grep -E 'Verify return code|Protocol'

Pass means `Verify return code: 0 (ok)` and the expected TLS version. Report: "leaf valid to
2026-11-01, chain complete, TLS 1.3 negotiated; failure was a missing intermediate on the shared
vhost."
