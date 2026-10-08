---
name: watch-egress-for-exfiltration
description: Use when a process, agent, or container you launched might leak data outbound. Baseline its network egress, then alarm on new destinations or unusual transfer volume.
---

# Watch egress for exfiltration

Exfiltration is not exotic: it is one outbound connection you did not expect. This skill establishes a baseline of legitimate egress and treats every new destination or outsized transfer as a breach until proven otherwise.

## Procedure

1. Snapshot established outbound connections before the task: `lsof -nP -iTCP -sTCP:ESTABLISHED | awk '{print $9}' | sort -u > egress_before.txt`.

2. Capture the DNS and connection setup for the run window on macOS:

       sudo tcpdump -n -i any 'port 53 or (tcp[tcpflags] & tcp-syn != 0)' -c 5000 -w egress.pcap

3. Extract destinations and query names: `tshark -r egress.pcap -T fields -e ip.dst -e dns.qry.name | sort | uniq -c | sort -rn | head -30`.

4. Diff live state against baseline every 30s:

       comm -13 egress_before.txt <(lsof -nP -iTCP -sTCP:ESTABLISHED | awk '{print $9}' | sort -u)

5. Set volume thresholds. A config task should move kilobytes, not megabytes; any single flow over, say, 5 MB to a non-allowlisted host is quarantine-worthy.

6. Alarm on the high-risk shapes: POST to raw IP addresses, uploads to paste-style hosts, DNS TXT query bursts (a covert channel), and connections to cloud metadata `169.254.169.254`.

7. On a hit, cut the path before you analyse: block with `pfctl` or stop the process, then preserve the pcap and the destination list.

## Pitfalls

- Baselines taken after the task starts already contain the leak; snapshot before.
- HTTPS hides the payload but not the destination; treat an unexpected host as guilty even without content.
- DNS is the quiet channel: a slow trickle of uniquely named subqueries leaks data with no large flow.
- Killing the process may destroy in-memory proof; capture first, then act.

## Verification

    comm -13 egress_before.txt egress_after.txt   # empty output = no new destinations

Report: "baseline N destinations; new destinations M (<list>); largest flow <bytes> to <host>; verdict clean/quarantined."
