---
name: inspect-tcp-connection-states
description: Use when a service stops accepting connections, sockets pile up, or a process is stuck after a deploy. Read the socket table with ss to see which TCP states dominate, since CLOSE_WAIT, SYN_SENT, and TIME_WAIT point at three different bugs.
---

# Inspect TCP connection states

The socket table tells you who is stuck and how. A backlog of `CLOSE_WAIT` means your code is not
closing sockets; `SYN_SENT` means a peer is unreachable; `TIME_WAIT` in the thousands means churn.
Read the states before touching the app.

## Procedure

1. Summarise all sockets by state:
   ```bash
   ss -s
   ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn
   ```
2. List established connections to your service port with the owning process:
   ```bash
   sudo ss -tanp 'sport = :8080'
   sudo ss -tanp state established '( sport = :8080 )'
   ```
3. Interpret the dominant state:
   - `CLOSE_WAIT` — the peer closed, and **your** process has not called close(). A connection-leak in application code.
   - `SYN_SENT` — you sent a SYN and got no reply: firewall drop, wrong address, or a dead peer (see `capture-network-traffic-with-tcpdump`).
   - `TIME_WAIT` — normal after close; thousands to one destination means connection churn, fixed by pooling (see `tune-http-keep-alive-and-connection-pools`).
   - `LISTEN` with `Recv-Q` full — the accept backlog is saturated; the app is not accepting fast enough.
4. Check the listen backlog explicitly:
   ```bash
   ss -lnt | grep :8080    # Recv-Q / Send-Q columns
   ```
   A `Recv-Q` close to the configured `backlog` means connections are being dropped before `accept()`.
5. Count CLOSE_WAIT per process to find the leaking service:
   ```bash
   sudo ss -tanp state close-wait | grep -oP 'users:\(\("\K[^"]+' | sort | uniq -c | sort -rn
   ```
6. Check the send/receive queues on established sockets for a stuck consumer:
   ```bash
   ss -tanm 'sport = :8080' | grep -A1 ESTAB | head
   ```
7. On Linux, confirm conntrack is not full if `SYN_SENT`/drops appear with plenty of capacity:
   ```bash
   cat /proc/sys/net/netfilter/nf_conntrack_count
   cat /proc/sys/net/netfilter/nf_conntrack_max
   ```

## Pitfalls

- `CLOSE_WAIT` is an application bug (missing close), not a kernel or firewall problem; raising limits will not fix it.
- Retrying at the client while sockets sit in `SYN_SENT` multiplies half-open connections.
- `TIME_WAIT` to a *single* destination is churn; across many destinations it is just normal traffic.
- A full accept backlog drops SYNs silently — from the client it looks like a timeout, not a refusal.
- `netstat` is deprecated and slow on large hosts; use `ss`.
- Tightening `tcp_tw_reuse`/`tcp_tw_recycle` to "fix" TIME_WAIT can break NAT'd clients.
- Conntrack exhaustion shows as random drops across all traffic, not just one service.

## Verification

    ss -s
    ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn
    sudo ss -tanp state close-wait | wc -l

Pass means no dominant `CLOSE_WAIT`/`SYN_SENT` pile-up and `Recv-Q` on the listener is near 0. Report:
"12,400 CLOSE_WAIT held by pid 4412 (worker leak); TIME_WAIT stable; fixed by closing response bodies."
