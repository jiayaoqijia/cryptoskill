---
name: block-agent-egress-to-unlisted-hosts
description: Use when an agent's tool can reach the network. Allow only declared hosts and block the rest, so a poisoned prompt cannot exfiltrate data or fetch a payload.
---

# Block agent egress to unlisted hosts

An agent with open network access is an exfiltration channel waiting for a bad instruction. Allow egress only to hosts the task declared, and deny everything else by default.

## Procedure

1. From the brief, write the allowlist of hosts and ports: `api.internal:443`, `pypi.org:443`. Nothing else is permitted.
2. Enforce at the network layer, not in the prompt: a firewall rule, `--network` with a filtered proxy, or a DNS allowlist.
3. Deny by default; add a host only when a step fails for lack of it, and record why.
4. Resolve and pin: allow the resolved IP or a pinned hostname so DNS rebinding cannot redirect an approved name elsewhere.
5. Block raw IPs and link-local ranges unless explicitly listed; `169.254.169.254` (cloud metadata) is never allowed.
6. Log every outbound attempt with host, port, and decision: `egress=api.internal:443 allow` or `egress=evil.tld deny`.
7. Alert on denied attempts rather than dropping them silently — a blocked call is often the signal of prompt injection.
8. Treat a tool that "needs" a broad host list as a design smell; split it into narrower, single-purpose tools.

```bash
# nftables: drop all outbound except the allowlist, log the drops
nft add rule inet fw out tcp dport {443} ip daddr @allow4 accept
nft add rule inet fw out counter log prefix "egress-deny " drop
```

## Pitfalls

- Relying on a prompt instruction to "only visit approved sites", which injection can override.
- Allowlisting a hostname but not pinning its IP, so a fast DNS change redirects an approved name.
- Leaving the cloud metadata endpoint reachable, handing the agent the instance's credentials.
- Blocking silently, so an exfiltration attempt looks like a quiet success rather than an alarm.
- Allowing a package index for a build and never removing the rule when the build step ends.
- Granting a wildcard like `*.internal` that reaches far more hosts than the one step required.

## Verification

    nft list ruleset | grep -c 'egress-deny'; curl -sS --max-time 3 https://evil.tld/beacon; echo "exit=$? (nonzero = blocked)"

Report the allowlisted hosts, the enforcement layer, and any denied attempt observed during the run.
