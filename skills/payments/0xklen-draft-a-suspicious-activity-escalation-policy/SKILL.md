---
name: draft-a-suspicious-activity-escalation-policy
description: Use when writing or operating the internal route from a red flag to a decision maker, including clocks, evidence handling and the no-tipping-off rule, without the agent itself deciding to file.
---

# Draft a suspicious-activity escalation route

The escalation route is the control that turns an observation into a measured decision. Its job
is to get the right facts to a named human within a deadline and to leave a record — never to
have a tool auto-file a report.

## Procedure

1. Fix the intake. Anything from the screening queue, a customer-service note, or an analyst
   finding enters one queue with a required field set:

       cat > intake.schema.json <<'JSON'
       {"required":["subject","observed_at","typology","evidence_refs","analyst"],
        "evidence_refs":"list of tx hashes, list digests or alert ids"}
       JSON

2. Name the decision maker and a deputy. An escalation with no owner is an escalation that
   stalls; put the role, not a person's initials, on the ticket.

3. Set clocks in writing: internal review begins within 24 hours of intake, a decision is
   recorded within the internal window that sits inside the regulatory filing window for the
   jurisdiction. Track ageing on the queue, not in email.

       awk -F, 'NR>1 && $4!="closed" {print $1, (systime()-$3)/3600 "h open"}' queue.csv

4. Write the no-tipping-off rule into the runbook: no one who touches the case contacts the
   subject, and the customer-facing team is not told why an account is restricted. Restrict the
   system prompt so a support agent cannot narrate a case status.

5. Route evidence correctly: reference transaction hashes and list digests; do not paste
   customer PII or documents into the ticket body.

6. Record the outcome as `file`, `no file`, or `further review`, with the deciding role and the
   reasons. A `no file` needs reasons as much as a `file` does.

7. Re-open on new facts. A closed case that later gets a new counterparty alert should reopen,
   not be resurrected by editing the original — version it.

## Pitfalls

- Letting a tool decide to file. Filing is a legal act with named accountability; an agent may
  prepare a draft package, never transmit it.
- Tipping off the subject through a support reply that explains exactly why the account is
  limited. Disclosure of a report is itself an offence in many regimes.
- Missing the clock because the queue was worked from email threads. Ageing must be queryable.
- Escalating an impression with no evidence references, which forces the reviewer to redo the
  analysis and delays the decision past the window.
- Treating `no file` as "nothing happened". It is a recorded decision with a rationale, and it is
  the record that shows the programme worked.

## Verification

    python3 -c 'import json;json.load(open("intake.schema.json"));print("schema ok")'
    awk -F, 'NR>1 && $4!="closed" && (systime()-$3)>86400 {c++} END {print c+0, "breaching 24h"}' queue.csv

A pass means the schema parses and no open case exceeds the internal clock; any breaching count
above zero is a finding to report, not to hide.

Report queue depth, oldest open age, decisions by type with the deciding role. Whether the facts
require a filing is a determination for a qualified compliance officer and counsel — this
procedure only guarantees the facts arrive and the decision is recorded.
