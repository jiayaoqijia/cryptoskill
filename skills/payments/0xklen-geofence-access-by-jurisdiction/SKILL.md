---
name: geofence-access-by-jurisdiction
description: Use when a service must not be reachable from certain countries, whether because of sanctions, an unlicensed activity or a product restriction, and the block has to hold up against VPNs.
---

# Geofence access by jurisdiction

A geofence is a control with a bypass, and the bypass is usually a $5 VPN. Design the block
knowing that, decide fail-open or fail-closed deliberately, and keep the evidence that the block
was live.

## Procedure

1. Write the blocked set as data with a reason per region, so legal can read it:

       cat > geoblock.yaml <<'YAML'
       deny:
         - { country: IR, reason: "sanctions", fail: closed }
         - { country: KP, reason: "sanctions", fail: closed }
         - { country: US-NY, reason: "no licence", fail: closed }
       YAML

2. Resolve country at the edge from the request, not only from what the client claims. Use the
   connecting IP, and treat `X-Forwarded-For` as advisory; a header set by the client is not a
   country.

3. Decide the failure mode per row. For sanctions regions, fail closed: if geo lookup is down, the
   request is denied. For a soft restriction, fail open with a flag is acceptable — but write
   which is which.

4. Handle the VPN problem honestly. Datacentre and hosting ASNs are the strongest signal; block or
   challenge them where the restriction matters. Put the ASN check next to the country check so
   one change covers both:

       grep -w "$ASN" asn-deny.txt && echo "deny: hosting ASN"

5. Cover the whole surface: web, API, mobile app store availability, and the marketing site. A
   blocked web app with an open public API is not geofenced.

6. Log the decision per request with the input it used — resolved country, ASN, action — so a
   later dispute can be checked against the config of that moment.

7. Re-review on regime change, not on a schedule. A new sanctions designation or a licence grant
   changes the deny list, and the config should be version-controlled so the change is visible.

## Pitfalls

- Trusting a client-supplied locale, SIM or device language as the location. It is a preference,
  not a location.
- Blocking the country of a company's registration rather than the customer's connection; the two
  are unrelated and the wrong one both over- and under-blocks.
- Leaving the mobile app available in a blocked region's app store while blocking web. The app is
  the product.
- Fail-open by accident: a geo resolver exception that returns `allowed` turns a control into a
  no-op during exactly the incident you care about.
- Blocking an entire country for a state-level restriction; sub-national restrictions (the NY
  example) need state resolution, which IP geolocation only sometimes provides.

## Verification

    python3 -c 'import yaml;d=yaml.safe_load(open("geoblock.yaml"));
    assert all("fail" in r for r in d["deny"]); print(len(d["deny"]), "rules, all with fail mode")'

A pass means every deny rule states its failure mode; a rule with no `fail` key is ambiguous and
fails the check.

Report the deny list with reasons and failure modes, the signals used (IP, ASN), and the log
field that records the decision. Which countries a product may serve is set by counsel and the
relevant regulator, not by the engineering team.
