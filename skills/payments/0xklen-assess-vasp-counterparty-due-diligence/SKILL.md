---
name: assess-vasp-counterparty-due-diligence
description: Use when onboarding another virtual-asset service provider as a counterparty, correspondent or travel-rule peer, and you must check its licence, ownership and screening posture before sending value.
---

# Assess a VASP counterparty before onboarding

A peer VASP is a risk you inherit. The diligence is about three facts: is it licensed where it
says it operates, is it reachable for travel-rule data, and is anyone designated behind it.

## Procedure

1. Verify the licence at the source, not from the peer's website. Registries to check include the
   regulator's own public register — for example FinCEN's MSB registration, the FCA register, a
   state MTL lookup, or an EU competent-authority CASP register — and the entry must list the
   legal entity name, not just a brand.

```
       curl -s "https://register.fca.org.uk/services/V0.1/Firm/$FRN" \
         -H "X-Auth-Email: $FCA_EMAIL" -H "X-Auth-Key: $FCA_KEY" | jq -r '.Status, .Name'
```

2. Confirm the legal entity you are contracting with is the licensed entity. A licence held by a
   sister company in another country does not travel.

3. Check ownership against sanctions and the 50% rule, walking the chain up to natural persons or
   named listed parties.

4. Test travel-rule reachability before you rely on it: exchange a test payload and confirm you
   get an accepted response, not merely a 200.

       curl -sS -X POST "$PEER_ENDPOINT" -H "Content-Type: application/json" \
         -d @ivms101-test.json -o peer-reply.json; jq -r '.status' peer-reply.json

5. Note whether the peer allows nested or omnibus accounts, in which case the counterparty data
   you receive may describe the peer, not the underlying originator.

6. Record the review as a dated file with each fact and its source, a risk rating, and an expiry
   that forces periodic refresh:

       printf 'entity=%s licence=%s checked=%s next_review=%s\n' \
         "$PEER" "$FRN" "$(date -u +%F)" "$(date -u -v+12m +%F)" >> vasp-register.log

7. Set relationship limits in proportion to the rating and to how fast you can stop sending.

## Pitfalls

- Accepting a screenshot of a licence. Registers are queryable; a screenshot is not evidence.
- Onboarding a payment processor and assuming it is the licensed VASP; it may merely be a
  front-end for a different, unchecked entity.
- Skipping the travel-rule test and discovering mid-incident that the peer cannot receive
  required data.
- Reviewing once at onboarding and never again. Licences lapse and ownership changes.
- Missing branches. A licensed entity's unregulated affiliate is a different counterparty for
  sanctions and licensing purposes.

## Verification

    grep -c "^entity=" vasp-register.log
    jq -e '.status=="accepted"' peer-reply.json >/dev/null && echo travel-rule-ok

A pass records the peer with a licence reference and a review date and shows an accepted
travel-rule test; a peer that only returns an acknowledgement is not confirmed reachable.

Report the entity, licence and its registry source, ownership findings, travel-rule test result,
and next review date. Whether a relationship is permissible is a legal determination that a
qualified compliance officer and counsel must make.
