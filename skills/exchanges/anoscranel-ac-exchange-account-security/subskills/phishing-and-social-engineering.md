---
name: phishing-and-social-engineering
domain: crypto-trading/phishing-and-social-engineering
trigger: "Checking whether a message, site, or call is genuinely from the venue."
anti_trigger: "Not for incident response after a compromise, and not for venue selection."
scope: "Lookalike domains, fake support, migration messages, and the verification habit."
status: seedling
---

# Phishing and social engineering

## Standard

The message is the attack surface. A lookalike domain differs by one character, a support account replies to a complaint before the venue could have, and a "migration" notice creates urgency around a task the venue has never asked for. Each works because it arrives in a channel the recipient already trusts, and each is defeated by the same habit: verify through a route the message did not supply.

Verification means navigating to the venue by a bookmarked address or a known application, then checking whether the message's claim appears there. It is slow, and slowness is the point: urgency is the attacker's main instrument, and any message that demands action before verification is a message to treat as hostile.

Primary sources: <https://www.cisa.gov/> and <https://www.ftc.gov/>.

## Decision rules

- No credential, code, or key is entered after following a link in a message.
- Every claim is verified by navigating independently to the venue.
- Urgency, secrecy, and unusual payment instructions are treated as hostile indicators.
- Support contact details come from the venue's own site, never from a message.
- Any message requesting a transfer, a key, or a code is recorded and reported.
- The verification habit is applied to colleagues and to automated messages equally.

## Procedure

1. Pause on any message that asks for an action.
2. Open the venue by bookmark or application, not by the message's link.
3. Check whether the claim exists in the account or the venue's announcements.
4. If it does not, record the message and report it to the venue.
5. Never send a code, a key, or a document on request.
6. Record the attempt and the channel it arrived in.

## Anti-patterns

- Clicking a link because the sender's name looks right.
- Reading a domain quickly rather than character by character.
- Trusting a support conversation that started with the attacker's message.
- Acting within minutes because the message said the account would be frozen.
- Reporting after acting rather than before.

## Done checklist

- [ ] Action requests verified independently.
- [ ] No credentials entered via message links.
- [ ] Urgency and payment indicators recognised.
- [ ] Support details taken from the venue's own site.
- [ ] Suspicious messages recorded and reported.
- [ ] Attempt recorded with its channel.

## Sources

- Phishing and social-engineering guidance: <https://www.cisa.gov/>
- Consumer fraud guidance and reporting: <https://www.ftc.gov/>
- Investor guidance on fraud: <https://www.investor.gov/introduction-investing>
