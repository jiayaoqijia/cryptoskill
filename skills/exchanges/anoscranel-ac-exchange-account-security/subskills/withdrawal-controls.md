---
name: withdrawal-controls
domain: crypto-trading/withdrawal-controls
trigger: "Configuring and reviewing the controls that govern fund movement."
anti_trigger: "Not for choosing a venue, and not for handling key values."
scope: "Whitelists, delays, sub-accounts, and the difference between reading and moving funds."
status: seedling
---

# Withdrawal controls

## Standard

Withdrawal is the step where an account compromise becomes a loss, so the controls that govern it deserve more attention than the login screen. The three that matter are the address whitelist, the withdrawal delay, and the separation of funds across sub-accounts: a whitelist means a stolen session can only send to addresses the owner already approved; a delay gives the owner a window to react; and separation limits how much any single account can lose.

Each control has an operational cost that must be paid deliberately. A whitelist slows a legitimate new destination; a delay slows a legitimate transfer; separation complicates collateral management. Writing the cost beside the control is what stops the control from being quietly disabled in a busy week.

Primary sources: <https://www.cisa.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Every account with a balance has a whitelist, and the process for adding an address is recorded.
- Withdrawal delays are enabled where offered, and the delay length is recorded.
- Funds are separated so that no single account holds more than the operational need.
- The whitelist is verified after any address change, with a test transfer.
- Controls that were disabled are recorded with the reason and the date.
- Where the venue does not offer a control, that gap is recorded.

## Procedure

1. Record the controls available at each venue used.
2. Enable the whitelist and record the approved addresses.
3. Set the withdrawal delay and record its length.
4. Split balances across sub-accounts by purpose.
5. Test the whitelist with a small transfer.
6. Record the controls, their costs, and any disabled.

## Anti-patterns

- Leaving withdrawals open because a whitelist is inconvenient.
- Adding an address and transferring the full balance immediately.
- Holding all trading capital in one account.
- Disabling a delay during a busy period and not restoring it.
- Assuming a control exists without verifying it in the venue's settings.

## Done checklist

- [ ] Controls recorded per venue.
- [ ] Whitelist enabled and addresses recorded.
- [ ] Withdrawal delay set and recorded.
- [ ] Balances separated by purpose.
- [ ] Whitelist tested with a small transfer.
- [ ] Gaps and disabled controls recorded.

The controls also protect against the account holder: a delay catches a transfer made in haste, a whitelist catches an address copied from the wrong place, and separated balances limit the damage of a single mistaken or malicious action. Their value is not only adversarial.

## Sources

- Account and credential protection guidance: <https://www.cisa.gov/>
- Market-participant and custody guidance: <https://www.sec.gov/investor>
- Investor protection information: <https://www.investor.gov/introduction-investing>
