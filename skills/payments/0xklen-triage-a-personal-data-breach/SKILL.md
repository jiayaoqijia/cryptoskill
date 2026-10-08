---
name: triage-a-personal-data-breach
description: Use when personal data may have been exposed and you must scope risk and start the notification clock. Establish the facts before deciding who to notify.
---

# Triage a personal data breach

The first hours decide notification obligations. This skill establishes scope, risk, and the clock without jumping to conclusions.

## Procedure

1. Open an incident channel and build a timeline from the first observation, noting the source: monitoring, user report, or a third party.

2. Contain before investigating deeply: revoke the exposed credential, disable the endpoint, or pull the link. Preserve evidence by copying logs before any rotation.

3. Establish four facts: what data, how many subjects, was it encrypted, and who received it (accidental internal, public, or attacker).

4. Assess risk to individuals: identity theft, discrimination, financial loss, reputational harm. High risk drives individual notification.

5. Apply the clock in the relevant jurisdiction, commonly 72 hours from awareness to the regulator where required.

6. Build the subject list precisely from logs rather than guessing:
   `select distinct subject_id from access_log where served_at between $T0 and $T1;`
   Which rows were served, or which file was downloaded, is the scope. "Maybe everyone" is not a scope.

7. If the data was encrypted with keys that were not exposed, risk may be low; verify key separation before claiming that.

8. Draft the notification content: nature of the breach, categories and approximate numbers, likely consequences, measures taken, and contact.

9. Decide notification per audience (regulator, individuals, occasionally the public) and document the reasoning whichever way it lands.

## Pitfalls

- Destroying evidence (deleting the leaked file, wiping the disk) before scoping is common and blocks the assessment.
- Assuming low risk because it was internal is wrong; an employee inbox is still a disclosure.
- Under-counting subjects because logs had already expired; log retention itself becomes the gap.
- Notifying speculatively can itself cause harm; base the notice on the established scope.
- A processor's breach is your obligation to your users; ask the vendor for their scope, do not assume theirs is complete.

## Verification

    jq '{data_types, subject_count, encrypted, recipients, risk}' breach_scope.json   # all fields populated before any notice

Report the four facts, the risk assessment, the clock start time, and every notification triggered or excluded with reasons.
