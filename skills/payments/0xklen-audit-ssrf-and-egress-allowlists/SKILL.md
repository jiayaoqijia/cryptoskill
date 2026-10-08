---
name: audit-ssrf-and-egress-allowlists
description: Use when the server fetches a URL or host derived from user input. Finds the fetch sinks, tests metadata and internal endpoints, and moves from blocklists to an egress allowlist.
---

# Audit SSRF and egress allowlists

Server-side request forgery is any code path where the attacker chooses the destination the server
connects to, then reads the response or the side effect. Cloud metadata endpoints turn it into
credential theft; internal admin panels turn it into lateral movement.

## Procedure

1. Find every outbound request whose target can be influenced by input:

       rg -n "requests\.(get|post)|urllib|http\.Get|axios\.|fetch\(|curl |net/http|RestTemplate|WebClient" src/ \
         | rg -i "url|uri|host|endpoint|target|callback|webhook|redirect"

2. Note what the attacker controls: full URL, host, path, port, scheme, or an upstream redirect.

3. Classify the defence in place. A blocklist of `127.0.0.1` / `localhost` is weak; an allowlist of
   named hosts is strong. Check DNS resolution timing — validating a hostname then resolving it
   later is a TOCTOU window (DNS rebinding).

4. Test the classic targets against a staging instance and record status/latency:

       curl -s -m 3 "$APP/import?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
       curl -s -m 3 "$APP/import?url=http://127.0.0.1:6379/"          # redis
       curl -s -m 3 "$APP/import?url=file:///etc/passwd"
       curl -s -m 3 "$APP/import?url=gopher://127.0.0.1:6379/_INFO"

5. Check redirect handling: `curl -sL` follows redirects, and a server-side fetcher that follows
   them is trivially bounced to an internal host. Disable redirect-following or re-validate each
   hop.

6. Check IPv6 and decimal obfuscation bypasses: `[::1]`, `0x7f000001`, `2130706433`, `127.1`.

7. Replace the blocklist with an allowlist plus network egress control. Bind the fetcher to a
   dedicated egress proxy or a network namespace that can only reach the needed hosts.

## Pitfalls

- Decoding the URL once (`%2e%2e`) and validating before re-decoding lets a crafted value slip.
- Allowing only `https://` does not stop `https://169.254.169.254/`.
- Validating the hostname string but resolving it separately is the DNS-rebinding gap.
- Webhook and image-import features are the most common hidden SSRF sinks.
- A 200 with no body can still complete a blind side effect (a `DELETE` behind an internal API).
- Cloud metadata may require `Metadata-Flavor: Google` or IMDSv2 tokens; absence of a body does
  not mean absence of reachability.

## Verification

    printf '%s\n' \
      'http://169.254.169.254/latest/meta-data/' \
      'http://127.0.0.1:6379/' \
      'file:///etc/passwd' \
      | while read u; do \
          code=$(curl -s -m 3 -o /dev/null -w '%{http_code}' "$APP/import?url=$u"); \
          echo "$code $u"; \
        done

Pass: each probe returns a client error (400/403/422) or a fixed allowlist rejection, with no
internal body. Report the sinks found, which are user-controllable, and the allowlist now
enforced.
