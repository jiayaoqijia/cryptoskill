---
name: route-private-traffic-over-a-vpn
description: Use when services in different private networks must talk without exposing ports publicly, or a developer needs reach into a private subnet. Route private traffic over a VPN or bastion with the correct routes, split tunnel, and DNS instead of publishing the service to the internet.
---

# Route private traffic over a VPN

The safe way to reach a private service is to join the private network, not to expose the port. Get
the routes, split-tunnel policy, and internal DNS right or you will either leak traffic or see nothing.

## Procedure

1. Bring up the tunnel and confirm the peer is reachable:
   ```bash
   sudo wg show            # WireGuard handshake + transfer counters
   ip -br addr show tun0
   ping -c 3 10.20.0.1     # the private gateway
   ```
2. Verify the routes the client installed push your private subnets through the tunnel and nothing else:
   ```bash
   ip route show        # expect 10.20.0.0/16 dev tun0; default unchanged for split tunnel
   ```
   A default route through `tun0` means full tunnel — all traffic exits the VPN, which may be intended or not.
3. Confirm internal DNS resolves through the tunnel (see `resolve-split-horizon-dns`):
   ```bash
   dig @10.20.0.53 db.internal A +short
   ```
   Split tunnel often needs an explicit resolver for the private domain so it is not sent to the public resolver.
4. Test the actual service, staying inside the private range:
   ```bash
   curl -sS --max-time 5 http://10.20.1.30:5432/health 2>&1 | head -1
   ```
5. For a bastion instead of a mesh VPN, tunnel the port and connect to localhost:
   ```bash
   ssh -N -L 5432:10.20.1.30:5432 ec2-user@bastion.internal
   psql -h 127.0.0.1 -p 5432 -U app mydb
   ```
6. Lock the bastion down: key-only auth, an allowlisted source CIDR, and a short session timeout:
   ```bash
   ssh -o PasswordAuthentication=no -o ConnectTimeout=5 ec2-user@bastion.internal
   ```
7. Record which subnets are routed so a future service on a new subnet is not silently unreachable.

## Pitfalls

- A full-tunnel default route sends all traffic (including public sites) through the VPN, surprising users and overloading the gateway.
- A VPN that routes packets but provides no internal DNS still fails on hostnames — you debug the wrong layer.
- Overlapping CIDRs (both sides use `10.0.0.0/16`) mean the client cannot tell which `10.x` to route where.
- Publishing the DB port publicly "just for now" is the exposure the VPN is meant to prevent; a bastion and a temporary rule are not the same thing.
- Leaving the SSH tunnel open in a screen session exposes the DB to anything on localhost.
- `ssh -L` binds localhost by default; adding `-g` binds all interfaces and exposes the port on the LAN.
- WireGuard's `AllowedIPs` both routes traffic *and* filters it; a wrong mask silently drops return packets.

## Verification

    ip route get 10.20.1.30     # must show dev tun0 (or the tunnel)
    dig @10.20.0.53 db.internal A +short
    curl -sS --max-time 5 http://10.20.1.30:8080/health

Pass means the private IP routes through the tunnel, internal DNS resolves, and the service responds
without any public exposure. Report: "10.20.0.0/16 via tun0, split tunnel (public default intact),
internal DNS resolving; service reachable only over VPN."
