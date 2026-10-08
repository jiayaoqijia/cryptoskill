---
name: diagnose-mtu-blackhole
description: Use when a connection works for small requests but hangs on large ones, or TLS completes and then stalls. Test the path MTU with ping -M do and clamp MSS so oversized packets stop being silently dropped.
---

# Diagnose an MTU blackhole

A blackhole is the nastiest network bug: the handshake works, small responses work, and only large
packets vanish with no error. It happens when PMTUD is blocked and a link cannot carry a full-size
frame.

## Procedure

1. Reproduce the split: small requests succeed, large ones hang.
   ```bash
   curl -sS -o /dev/null -w '%{time_total}\n' https://api.example.com/small   # fast
   curl -sS -o /dev/null -w '%{time_total}\n' --max-time 20 https://api.example.com/big  # hangs
   ```
2. Find the largest packet that survives, with the DF (don't-fragment) bit set:
   ```bash
   ping -c 1 -M do -s 1472 10.0.2.7   # 1472 + 28 = 1500
   ping -c 1 -M do -s 1400 10.0.2.7   # try smaller until it replies
   ```
   A reply at 1400 but silence (or "message too long") at 1472 means the path MTU is below 1500.
3. Bisect to the exact MTU by testing a few sizes; `+28` for IP+ICMP headers gives the link MTU.
4. Confirm the blackhole signature on the wire — the large packet goes out and nothing comes back,
   while small ones are ACKed (see `capture-network-traffic-with-tcpdump`):
   ```bash
   sudo tcpdump -nn -i any 'host 10.0.2.7 and greater 1400'
   ```
5. Apply the fix — clamp MSS on the tunnel/VPN interface so both ends negotiate a size that fits:
   ```bash
   sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
     -j TCPMSS --clamp-mss-to-pmtu
   ```
6. Lower the interface MTU directly when the link itself is the limit (VPNs typically need 1400 or less):
   ```bash
   sudo ip link set dev tun0 mtu 1400
   ```
7. Re-run the large request; it should now complete.

## Pitfalls

- PMTUD depends on ICMP "fragmentation needed" getting back; a firewall that drops all ICMP silently creates the blackhole.
- "Ping works" proves nothing — the default ping size is 56 bytes, far below any MTU issue.
- VPN and tunnel interfaces (WireGuard, IPsec, GRE) shrink the usable MTU; the overlay's default 1500 is wrong.
- HTTPS is often where it shows because the TLS Certificate message is the first large packet — handshakes succeed, data stalls.
- Clamping MSS on one side only can still break if the reverse direction carries the large packet.
- A too-low MTU costs throughput and fragmentation; measure the real limit, do not guess 1200.

## Verification

    ping -c 1 -M do -s 1472 <peer>   # expect "message too long" or timeout
    ping -c 1 -M do -s 1400 <peer>   # expect a reply
    curl -sS -o /dev/null -w '%{time_total}\n' --max-time 20 https://api.example.com/big

Pass means small-MTU pings reply, oversized ones fail, and the large request now returns under the
timeout. Report: "path MTU 1400; MSS clamped; 5 MB download that hung now completes in 2.4 s."
