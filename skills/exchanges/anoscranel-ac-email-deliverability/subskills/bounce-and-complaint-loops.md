---
name: bounce-and-complaint-loops
domain: software-engineering/bounce-and-complaint-loops
trigger: "Operating the feedback loops that protect the sending reputation."
anti_trigger: "Not for send-side marketing rules, and not for webhook plumbing generally."
scope: "Hard versus soft, the feedback loops, and the suppression list."
status: seedling
---

# Bounce and complaint loops

## Standard

A bounce is the receiver's machine verdict on an address; a complaint is a human's. They feed the same reputation either way, and the sender's defence is to process both instantly and stop sending. The classification matters because the right response differs: a hard bounce — the address does not exist — is permanent suppression, while a soft bounce — full mailbox, greylisting, temporary deferral — is retry grounds, not removal, unless a threshold is crossed over time.

The loops themselves must be wired before volume, not after the first block. Bounce webhooks arrive from the platform; spam complaints arrive through the feedback loops that major receivers operate, and the not-spam side has rules of its own — one-click unsubscribe headers matter precisely because a tired reader's alternative is the spam button. Processing both is not monitoring; it is a control loop whose delay directly converts to reputation.

Primary sources: <https://en.wikipedia.org/wiki/Bounce_message> and <https://datatracker.ietf.org/doc/html/rfc5965>.

## Decision rules

- Classify every bounce into hard and soft before acting: suppress hard immediately, schedule soft retries with thresholds.
- Wire the platform's bounce webhook and each major receiver's complaint feedback loop before any volume ramp.
- Every complaint suppresses the address immediately and records it; the complaint is a signal, not an argument.
- Set a soft-bounce ceiling in count or time, and suppress only when the ceiling is crossed.
- Honour unsubscribe mechanically — including the one-click header — because the spam button is the alternative.
- Track complaint rate as the key ratio with the denominator it deserves: per delivered, not per sent.

## Procedure

1. Enable bounce processing in the platform and read its webhook on every send batch.
2. Register for complaint feedback loops with each major receiver.
3. Implement the hard/soft table with suppression actions and retention policies.
4. Implement the one-click unsubscribe header and verify it against the receiver's checker.
5. Compute complaint ratio per delivery on a stated cadence with a stated threshold.
6. Record loop status and threshold actions in the deliverability record.

## Anti-patterns

- Re-trying a hard bounce list on the next campaign because it was easy to re-export.
- Processing complaints weekly in a batch and calling it a loop.
- Enough unsubscribe friction that the reader reaches for the spam button, which costs the domain, not the email.
- Treating complaint rate per sent instead of per delivered, hiding a failing stream.
- A suppression list that only exists in the current SMTP provider's dashboard and survives no migration.

## Done checklist

- [ ] Bounce webhook live with a hard/soft table.
- [ ] Soft thresholds defined and enforced.
- [ ] Complaint loops registered with each major receiver.
- [ ] Complaints suppressed immediately and recorded.
- [ ] One-click unsubscribe verified working.
- [ ] Complaint ratio computed per delivered with a threshold.

## Sources

- The bounce mechanism and its classifications: <https://en.wikipedia.org/wiki/Bounce_message>
- RFC 5965, the anti-spam feedback report format: <https://datatracker.ietf.org/doc/html/rfc5965>
- Sender guidelines from a major receiver: <https://support.google.com/a/answer/81126>
