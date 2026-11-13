---
name: proxy-contest-arithmetic
domain: investing/proxy-contest-arithmetic
trigger: "Working out whether a proxy contest can win the seats it seeks."
anti_trigger: "Not for predicting the vote, and not for the investment case."
scope: "Vote thresholds, turnout, and the seats a contest can win."
status: seedling
---

# Proxy contest arithmetic

## Standard

A proxy contest is decided by arithmetic, and the arithmetic starts with the voting standard. A plurality contest elects the nominees with the most votes, so a dissident needs to beat the company's nominees rather than to reach a majority. A majority standard requires more than half of the votes cast, which is a harder threshold and a different campaign.

The second input is ownership. Retail turnout is low, index funds vote with the board more often than not, and a dissident's path runs through the largest active holders. Estimating the vote means mapping the register: who holds, how they have voted before, and what a dissident needs from each. A campaign that cannot name the holders it must win has not done the arithmetic.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the voting standard for the seats contested: plurality or majority.
- Record the record date and the shares outstanding.
- Record the register by holder type: index, active, retail, insider.
- Record the votes required under each standard.
- Record the historical voting behaviour of the largest holders.
- Record the company's own stake and any affiliate holdings.

## Procedure

1. Record the standard and the seat count.
2. Record outstanding shares and the record date.
3. Map the register by holder type and size.
4. Compute the votes required for each outcome.
5. Record the holders whose votes decide it.
6. Write the arithmetic with the assumptions.

## Anti-patterns

- Assuming a majority is required for a plurality contest.
- Counting insider and affiliate holdings as available votes.
- Ignoring low retail turnout, which concentrates power in large holders.
- Treating past voting behaviour as a guarantee.
- Estimating a vote without mapping the register.

## Done checklist

- [ ] Standard and seats recorded.
- [ ] Shares outstanding and record date recorded.
- [ ] Register mapped.
- [ ] Votes required computed.
- [ ] Deciding holders identified.
- [ ] Arithmetic written with assumptions.

Turnout is the variable that most often decides an unexpected result: a contest the dissident appears to lead on the register can fail if its supporters do not vote, and a company with a large retail base can win on the votes of holders who never considered the question. Estimating turnout by holder type, rather than assuming all shares vote, is what turns a register map into a forecast.

## Sources

- Proxy contest disclosure: <https://www.sec.gov/investor>
- Governance standards: <https://www.cfainstitute.org/>
- Corporate governance research: <https://www.nber.org/>
