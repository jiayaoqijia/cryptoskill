---
name: account-security-record
domain: crypto-trading/account-security-record
trigger: "Writing and reviewing the account-security record."
anti_trigger: "Not for storing secret values, and not for venue selection."
scope: "The written record: accounts, key inventory, controls in place, and review triggers."
status: seedling
---

# Account security record

## Standard

The security record is a one-page inventory of the doors into the capital: which accounts exist, which keys exist, which controls are enabled, and who can reach them. It exists so that a review can be a checklist rather than a memory exercise, and so that a compromise response can start from a known list instead of an improvised search.

Its second purpose is continuity. The person who configured the controls is not always the person who must respond, and an executor, a colleague, or a future self needs to know where the keys are held, which factors are registered, and where the recovery material lives. That is why the record names locations and never values.

Primary sources: <https://www.nist.gov/> and <https://osf.io/prereg/>.

## Decision rules

- Every account appears once, with venue, purpose, and balance tier.
- Every key appears once, with scope, allowlist status, and rotation date.
- Every control appears with its state: enabled, disabled, or unavailable.
- The location of recovery material is recorded; the material itself is not.
- Review triggers are dated: new account, new key, factor change, address change, quarterly review.
- The record is stored where a responder can reach it without the account it describes.

## Procedure

1. List accounts with venue, purpose, and tier.
2. List keys with scope, allowlist, and last rotation.
3. Record each control and its state.
4. Record where recovery material is held.
5. Set review triggers.
6. Store the record separately from the credentials it maps.

## Anti-patterns

- A record that contains values.
- Listing accounts without their controls.
- Storing the record inside the account manager that holds the passwords for those accounts, with no separate copy.
- No rotation dates, so stale keys are invisible.
- A review that never happens because no trigger exists.

## Done checklist

- [ ] Accounts listed with purpose and tier.
- [ ] Keys listed with scope and rotation date.
- [ ] Controls recorded with state.
- [ ] Recovery material located, not reproduced.
- [ ] Review triggers dated.
- [ ] Record stored separately from credentials.

The quarterly review is where the record earns its keep: keys created for a one-off task, factors registered on a device that has since been replaced, and whitelists never updated after a wallet change are all invisible until someone reads the list against reality. Reading it is the control.

## Sources

- Identity and access management guidance: <https://www.nist.gov/>
- Pre-registration practice for review conditions: <https://osf.io/prereg/>
- Cybersecurity guidance on access control: <https://www.cisa.gov/>
