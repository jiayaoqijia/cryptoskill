---
name: compromise-response
domain: crypto-trading/compromise-response
trigger: "Responding in the first hour after a suspected account compromise."
anti_trigger: "Not for legal advice, and not for recovering funds."
scope: "The first hour: revoke, freeze, change, preserve evidence, and notify."
status: seedling
---

# Compromise response

## Standard

The first hour decides how much is lost. The order is fixed by consequence: stop the outflow, then remove the attacker's access, then change what the attacker could use, and only then investigate. Investigators who begin by reading logs while withdrawals continue are watching the loss happen, which is why the sequence is written before it is needed.

Evidence survives only if it is captured early: session lists, login history, withdrawal records, and the messages that preceded the event. Those records are what the venue, the police, and any insurer will ask for, and they are also what distinguishes a compromise from an operational error. Capturing them is cheap; reconstructing them later is not.

Primary sources: <https://www.cisa.gov/> and <https://www.ftc.gov/>.

## Decision rules

- Withdrawals are frozen and keys revoked before any investigation begins.
- All credentials and second factors are changed, not only the one suspected.
- Evidence is captured and stored before systems are cleaned.
- The venue's security team is contacted through its published channel, never through a message.
- A written timeline records what happened, in what order, with times.
- The cause is recorded even if it is embarrassing; a response that hides the cause repeats it.

## Procedure

1. Freeze withdrawals and disable API keys.
2. Change passwords, factors, and recovery material.
3. Revoke active sessions and trusted devices.
4. Capture logs, messages, and transaction records.
5. Contact the venue and, where material, law enforcement.
6. Write the timeline and the cause, and record the controls to change.

## Anti-patterns

- Investigating before stopping the outflow.
- Changing one credential and leaving the rest.
- Cleaning up before capturing evidence.
- Contacting "support" through a link in the suspicious message.
- Writing a timeline that omits the mistake that enabled the event.

## Done checklist

- [ ] Withdrawals frozen and keys revoked.
- [ ] All credentials and factors changed.
- [ ] Sessions and devices revoked.
- [ ] Evidence captured and stored.
- [ ] Venue and authorities contacted where appropriate.
- [ ] Timeline and cause written with controls to change.

The procedure's value is that it removes the decision from the worst moment: someone who is panicking should be following a list, not deciding what to do first. The list is short for the same reason, and it is rehearsed by reading it before it is needed.

## Sources

- Incident response guidance: <https://www.cisa.gov/>
- Consumer fraud reporting: <https://www.ftc.gov/>
- Investor protection and reporting routes: <https://www.investor.gov/introduction-investing>
