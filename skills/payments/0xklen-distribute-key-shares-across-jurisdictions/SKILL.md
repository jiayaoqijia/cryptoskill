---
name: distribute-key-shares-across-jurisdictions
description: Use when one custody provider or one legal entity holds every key share. Splits shares across independent vendors, regions, and legal systems so no single seizure, outage, or bankruptcy reaches quorum.
---

# Distribute key shares across jurisdictions

If every share sits under one provider, one regulator, or one cloud region, the threshold is decorative. This skill places shares so that no single failure — technical, legal, or commercial — can assemble `t` of `n`.

## Procedure

1. Enumerate the failure domains the scheme must survive: one vendor outage, one cloud region, one country's freeze order, one company's insolvency, one malicious insider. A share placement is only useful if it breaks at least one class.
2. Place shares so at most `t-1` fall in any single domain. For 3-of-5 across two vendors, no vendor may hold three shares:
   - Vendor A, region us-east: 2 shares
   - Vendor B, region eu-central: 2 shares
   - Self-custodied hardware in a third country: 1 share
3. Keep at least one share you can operate without any third party — a hardware device in your own control. If the vendor is the only path to quorum, the vendor holds your funds.
4. Record, per share: vendor, legal entity, jurisdiction, region, and the recovery contact. Store the map separately from the shares.
5. Test that losing any one domain leaves quorum reachable: remove a vendor's shares from the map and confirm `n_remaining >= t`.
6. Re-review after any provider change of ownership, region, or terms; a migration you did not consent to can collapse two domains into one.

## Pitfalls

- Two vendors that both use the same underlying cloud and key-management service are one domain wearing two logos.
- A jurisdiction is not a domain if both copies are reachable by the same subpoena; legal independence must be real.
- Storing the whole recovery map next to a share hands an attacker the other locations; keep the map in a separate system with different access.
- Personal hardware in one home is one domain regardless of how many devices sit in the drawer.
- Never paste a seed phrase or a share into a chat or shell pipeline to "back it up"; each share is moved by its own channel and lands in a restricted file or offline medium.

## Verification

    # with the placement map loaded, confirm no domain reaches the threshold
    python3 -c "from collections import defaultdict; d=defaultdict(list);
    [d[j['domain']].append(j) for j in shares];
    assert max(len(v) for v in d.values()) < THRESHOLD; print('no single domain reaches quorum')"
    # expect the assertion to pass; a max >= threshold means a single domain can sign alone

Report the placement per domain, the count in the largest domain, and that it is below `t`, quoting the check.
