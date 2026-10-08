---
name: tighten-firewall-rules-to-least-privilege
description: Use when reviewing or changing security groups, firewalls, or network ACLs — especially before removing a temporary 0.0.0.0/0 rule. Scope each rule to the minimum source, port, and protocol it needs, and prove the rule is required before deleting it.
---

# Tighten firewall rules to least privilege

A rule open to `0.0.0.0/0` is a standing invitation. Least privilege means every allow names a
specific source, port, and direction — and every rule you keep has a proven consumer.

## Procedure

1. Dump the current rules with their sources and ports:
   ```bash
   aws ec2 describe-security-groups --group-ids "$SG" \
     --query 'SecurityGroups[].IpPermissions[].[IpProtocol,FromPort,ToPort,IpRanges[].CidrIp]' --output json
   ```
   For Linux hosts: `sudo iptables -S` or `sudo nft list ruleset`.
2. Flag every overly broad rule — ingress from `0.0.0.0/0`, `-A INPUT ... -j ACCEPT` with no match:
   ```bash
   aws ec2 describe-security-groups --group-ids "$SG" \
     --query 'SecurityGroups[].IpPermissions[?contains(IpRanges[].CidrIp, `0.0.0.0/0`)]'
   ```
3. For each broad rule, identify the real consumer before changing it:
   ```bash
   # AWS VPC flow logs: which sources actually hit this port
   aws logs filter-log-events --log-group-name /aws/vpc/flowlogs \
     --filter-pattern '{ $.dstport = 5432 }' --query 'events[].message' | head
   ```
   No observed traffic over a representative window is evidence a rule may be removable — not proof.
4. Narrow public ingress to the actual CIDR of the client (office range, CDN egress range, partner IP):
   ```bash
   aws ec2 revoke-security-group-ingress --group-id "$SG" --protocol tcp --port 5432 --cidr 0.0.0.0/0
   aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 5432 --cidr 203.0.113.0/24
   ```
5. Reference another security group as the source instead of a CIDR when the caller is known:
   ```bash
   aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 5432 \
     --source-group sg-0app123
   ```
6. Keep explicit deny at the end (NACL) or default-deny (security groups are allow-only) and document
   each remaining rule with a tag or comment naming the owner.
7. Re-test the flows the rule serves before removing a temporary exception.

## Pitfalls

- Removing a "temporary" `0.0.0.0/0` rule during business hours cuts users who never got migrated.
- Security groups are allow-only and stateful; a network ACL is stateless, so narrowing one direction breaks return traffic.
- A CIDR of `10.0.0.0/8` is not least privilege — it is every private host in every peered VPC.
- VPC flow logs sample and can lag; absence of traffic in a log is weak evidence, not certainty.
- Hardcoding a dynamic IP (home office) into a rule guarantees a future outage when the IP changes.
- Opening a wide port range (`0-65535`) "to be safe" is worse than a single wrong port.
- Rule changes are not transactional; a revoke-then-authorize gap drops in-flight connections.

## Verification

    aws ec2 describe-security-groups --group-ids "$SG" \
      --query 'SecurityGroups[].IpPermissions[].IpRanges[].CidrIp' | grep '0.0.0.0/0'
    # expect no output for the tightened port

Pass means the previously public port no longer lists `0.0.0.0/0` and the real consumer still
connects. Report: "port 5432 narrowed 0.0.0.0/0 → 203.0.113.0/24; app connectivity verified."
