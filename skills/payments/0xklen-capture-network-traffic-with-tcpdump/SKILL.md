---
name: capture-network-traffic-with-tcpdump
description: Use when a connection fails or misbehaves and the application logs are silent — packets that never left, a reset, retransmits, or a wrong destination. Capture a bounded slice on both ends with tcpdump and read the TCP flags and sequence behaviour.
---

# Capture network traffic with tcpdump

When logs say "connection error" and nothing more, the answer is on the wire: a SYN with no SYN-ACK
(bad route/firewall), an RST (rejected), or repeated retransmits (loss/MTU). Capture deliberately.

## Procedure

1. Capture a bounded slice to a file — never stream unbounded to the terminal in production:
   ```bash
   sudo tcpdump -i any -s 0 -w /tmp/cap.pcap -c 200 'host 10.0.2.7 and port 5432'
   ```
   `-s 0` captures full packets; `-c 200` stops after 200 so you cannot fill the disk.
2. Reproduce the failure while the capture runs, then stop it.
3. Read the header lines with timestamps and flags; look for the handshake pattern:
   ```bash
   tcpdump -nn -r /tmp/cap.pcap 'tcp[tcpflags] & (tcp-syn|tcp-rst|tcp-fin) != 0'
   ```
   `S` then nothing back → dropped SYN. `S` then `R` → a closed port or a rejecting firewall.
4. Check for retransmission storms (loss or asymmetric MTU):
   ```bash
   tcpdump -nn -r /tmp/cap.pcap | grep -c '\[TCP Retransmission\]' 2>/dev/null
   # or count duplicate ACKs by sequence number in your analysis tool
   ```
5. Confirm the destination MAC/IP — a wrong next-hop (misconfigured route or VIP) shows here:
   ```bash
   tcpdump -nn -e -r /tmp/cap.pcap | head -5
   ```
6. Capture on *both* ends when you suspect a middlebox. SYN present on the client capture but absent
   on the server capture means something in between dropped it.
7. Correlate an RST with the port owner at that instant (see `inspect-tcp-connection-states`).

## Pitfalls

- `-i any` on Linux uses a synthesized interface that can drop packets under load; capture on the
  specific interface for high-rate traffic.
- Without `-nn`, tcpdump resolves names/ports, adding latency and confusing the timeline — always use it.
- Capturing on a host that is behind a load balancer sees the LB IP, not the client (see `forward-client-ip-through-a-proxy`).
- An unbounded capture to disk can fill the volume and take the host down; always bound with `-c`/`-w`+rotation.
- TLS payload is encrypted — you see the handshake and sizes, not the content. Look at timing and flags, not body.
- `tcpdump` needs CAP_NET_RAW; in a container, the host namespace may be required to see the traffic.
- Reading only the summary lines misses the flags; always inspect `tcpflags`.

## Verification

    tcpdump -nn -r /tmp/cap.pcap 'tcp[tcpflags] & (tcp-syn|tcp-rst|tcp-fin) != 0' | head
    # expect a SYN, a SYN-ACK reply, then ACK for a healthy connection

Pass means the capture shows the full three-way handshake and no unexpected RST. Report: "200-packet
capture on eth0 shows SYN with no SYN-ACK to 10.0.2.7:5432 — firewall drop, not app error."
