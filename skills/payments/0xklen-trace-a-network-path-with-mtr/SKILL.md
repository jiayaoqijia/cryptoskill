---
name: trace-a-network-path-with-mtr
description: Use when latency or loss to a host is intermittent, or a connection is slow from one region and fine from another. Run mtr to see per-hop loss and latency over time and separate a real problem hop from ICMP deprioritisation noise.
---

# Trace a network path with mtr

A single traceroute shows one instant; a bad path is about sustained loss and added latency at a
specific hop. mtr samples continuously, so you can tell a genuine problem hop from a router that
merely deprioritises ICMP replies.

## Procedure

1. Run mtr in report mode with enough cycles to be meaningful:
   ```bash
   mtr -rwzbc 50 api.example.com
   ```
   `-r` report, `-w` wide, `-z` ASN names, `-b` both IP and name, `-c 50` fifty probes.
2. Read the loss column carefully:
   - Loss at a hop *and every hop after it* down to the destination is a real problem at that hop.
   - Loss at one hop that does **not** continue to the destination is ICMP rate-limiting noise, not loss.
3. Compare the `Avg` and `Stdev` columns; high stdev means jitter, which breaks real-time traffic even
   without packet loss.
4. For a specific hop, query it directly to confirm responsiveness:
   ```bash
   ping -c 20 10.20.0.1
   ```
5. Run TCP-mode traces to bypass ICMP deprioritisation and mirror real application traffic:
   ```bash
   mtr -T -P 443 -rwc 50 api.example.com
   ```
6. Compare from a second vantage point (another region or a public looking-glass) to localise the
   bad hop to one side of the network:
   ```bash
   mtr -rwc 50 10.20.0.1
   ```
7. Record the hop where the latency first steps up — that is the boundary between two networks and
   usually the place to raise a ticket.

## Pitfalls

- Treating a mid-path loss figure as real when the final hop shows no loss: routers rate-limit ICMP.
- A single traceroute with default 3 probes is statistically meaningless; use `-c 50`.
- ICMP traces can be filtered entirely while TCP to port 443 works fine — always confirm in TCP mode.
- mtr measures one direction; a problem on the return path will not appear.
- DNS resolution per hop (`-z` without `-n`) can slow a long trace; use `-n` when you only need IPs.
- A satellite or mobile link shows uniformly high latency with no single bad hop — that is physics, not a fault.
- Running mtr in the foreground of a stuck terminal floods output; always use report mode.

## Verification

    mtr -rwzbc 50 api.example.com
    mtr -T -P 443 -rwc 50 api.example.com

Pass means the destination shows no loss and the latency profile is flat, or you can name the exact
hop where loss begins and continues. Report: "loss starts at AS64500 hop 10.20.0.1 and persists to
destination; TCP-mode matches, ticket raised with that hop."
