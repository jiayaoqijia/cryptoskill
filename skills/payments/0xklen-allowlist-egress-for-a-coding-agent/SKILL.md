---
name: allowlist-egress-for-a-coding-agent
description: Use when a coding agent runs unattended with shell and network access. Put a default-deny egress allowlist in front of it, so only the package registries and APIs the task needs are reachable.
---

# Allowlist egress for a coding agent

An agent with open network is an exfiltration primitive waiting for a bad instruction. This skill puts egress behind an explicit allowlist and default-deny, so a compromise must defeat policy rather than just find a shortcut.

## Procedure

1. Enumerate the hosts the task legitimately needs: package registries, the repo remote, and any API the task calls. Write them as exact hostnames.

       printf '%s\n' registry.npmjs.org pypi.org files.pythonhosted.org github.com api.github.com > allowlist.txt

2. Default-deny the rest. On Linux with nftables, allow only the listed destinations and drop all other new outbound connections:

       nft add rule inet filter output tcp dport 443 ip daddr != @allow4 drop

3. On macOS use `pf` with a table: load the allowlist into an `egress_allow` table and pass only those, blocking the rest of outbound.

4. Route the agent through a proxy that enforces the list, so the policy lives in one auditable place rather than in the process:

       HTTPS_PROXY=http://127.0.0.1:8080 http_proxy=http://127.0.0.1:8080 no_proxy=localhost,127.0.0.1

5. Log denied attempts with the host and the process; a burst of denials is the signal an instruction tried to phone home.

       sudo tcpdump -n 'tcp[tcpflags] & tcp-syn != 0 and not host 127.0.0.1' -c 500

6. Re-review the allowlist when the task ends and shrink it; keep it per-task, not permanent.

7. Fail closed: if the proxy or firewall is down, the agent should lose network, not gain it.

## Pitfalls

- A wildcard or a whole cloud provider's CIDR in the allowlist reopens everything you closed.
- DNS is egress too; if resolution is open, data can leave in subdomain labels even with IP filtering.
- An agent that can edit its own firewall rules defeats the control; run the policy outside its reach.
- Package mirrors and CDNs share IPs; verify the enforcement keys on hostname, not a stale IP.

## Verification

    curl -sS --max-time 5 https://not-allowed.example ; echo "exit $?"   # non-zero = blocked = pass

Report: "allowlist n hosts; unauthorised connect blocked with exit <code>; denied attempts in log n to <hosts>."
