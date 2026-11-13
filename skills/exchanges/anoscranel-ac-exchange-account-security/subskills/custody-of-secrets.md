---
name: custody-of-secrets
domain: crypto-trading/custody-of-secrets
trigger: "Deciding where credentials, keys, and recovery material live."
anti_trigger: "Not for storing secret values in the record, and not for venue selection."
scope: "Where keys and recovery codes live, backups, and sharing access without exposing values."
status: seedling
---

# Custody of secrets

## Standard

Secrets have three states that need different handling: at rest, in use, and in backup. At rest they belong in a manager designed for them, not in a note, a document, or a spreadsheet. In use they should be injected by a tool rather than pasted, so that the value never enters a shell history or a conversation. In backup they need an offline copy that survives the loss of the primary device, because a second factor that cannot be restored is a lockout rather than a control.

The rule that keeps all three honest is that the record describes the secret without containing it. An inventory that says which key exists, what it can do, and where it is stored is operationally sufficient and cannot itself be leaked usefully.

Primary sources: <https://www.nist.gov/> and <https://www.cisa.gov/>.

## Decision rules

- Secrets are stored in a manager or a hardware device, never in documents or code.
- Each secret is inventoried by identifier, purpose, scope, and storage location.
- Backups exist offline, and their restoration is tested.
- Secrets are injected into processes rather than pasted into shells or messages.
- Access shared with another person or system is granted per-secret and recorded.
- Any secret that has appeared in a message or a log is treated as exposed and rotated.

## Procedure

1. Inventory each secret with identifier, purpose, and location.
2. Move any stored in plain text into the manager.
3. Create offline backups and test a restore.
4. Replace pasted entry with injection where the tooling allows.
5. Record shared access per secret.
6. Rotate anything with a suspected exposure and record the rotation.

## Anti-patterns

- Keeping a key in a chat message "just for now".
- Backing up the manager to the same device it runs on.
- Sharing a manager account instead of a secret.
- Recording a secret value in the inventory to "avoid confusion".
- Testing a restore for the first time during an incident.

## Done checklist

- [ ] Secrets inventoried without values.
- [ ] Plain-text copies removed.
- [ ] Offline backups created and a restore tested.
- [ ] Injection used where available.
- [ ] Shared access recorded per secret.
- [ ] Exposed secrets rotated and logged.

## Sources

- Digital identity and secret management guidance: <https://www.nist.gov/>
- Cybersecurity practice guidance: <https://www.cisa.gov/>
- Market-participant security guidance: <https://www.sec.gov/investor>
