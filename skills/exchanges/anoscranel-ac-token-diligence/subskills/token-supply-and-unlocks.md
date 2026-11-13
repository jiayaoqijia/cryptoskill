---
name: token-supply-and-unlocks
domain: crypto-trading/token-supply-and-unlocks
trigger: "Reading a token's supply schedule and dating its unlock cliffs before exposure."
anti_trigger: "Not for price forecasting, and not for sizing a position."
scope: "Circulating versus total versus max supply, emission schedules, and unlock cliffs with their dates and float arithmetic."
status: seedling
---

# Token supply and unlocks

## Standard

Supply is three different numbers, and the gap between them is dilution. Circulating supply is what trades today. Total supply is what exists, including locked allocations. Max supply is what will ever exist if the schedule completes. A diligence question that starts with "what is the market cap" is asking about circulating supply times price; the honest question is what fraction of the eventual supply that represents.

The second number that matters is the calendar. Locked allocations do not vanish; they arrive. A token whose circulating float is a fifth of total supply has four-fifths of dilution still ahead, and the schedule that releases it is the single most predictable price-relevant fact about the asset. Predictable does not mean priced: markets routinely under-discount unlocks that are months away and react when they land.

Primary sources: <https://ethereum.org/en/developers/docs/standards/tokens/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record circulating, total, and max supply with the source and date of each. If any figure has no source, record it as unknown rather than estimating.
- Compute the float ratio: circulating divided by max supply. Below one third is a dilution-heavy structure and must be written down as such.
- Build the unlock calendar for the next twelve months: date, size as a percentage of circulating, and recipient class (team, investors, treasury, community).
- An unlock above roughly five percent of circulating in a single event is a material event; above ten percent it dominates every other fact in the record.
- Never treat an announced schedule as fixed. Governance can change it; the record notes who could and whether they have.
- If the schedule is undisclosed, that is a red flag, not an absence of information.

## Procedure

1. Pull the supply figures from the issuer's documentation and one independent tracker. Reconcile; where they disagree, record both.
2. Compute the float ratio and the fully diluted valuation at the current price, with the arithmetic shown.
3. Build the twelve-month unlock table: date, tokens, percent of circulating, recipient class.
4. Identify the largest single unlock and its date. Write one sentence on what it does to float.
5. Check whether the schedule has ever been amended, and by whom.
6. Record every figure with its source and date, and mark the ones you could not verify.

## Anti-patterns

- Quoting a market capitalisation without stating which supply it uses.
- Treating a vesting chart in a blog post as the schedule.
- Assuming a long unlock horizon means no dilution; it means dilution is deferred, not absent.
- Reading a low float as scarcity rather than as future supply.
- Ignoring insider allocations because they are labelled "ecosystem".

## Done checklist

- [ ] Circulating, total, and max supply each carry a source and a date.
- [ ] Float ratio computed and stated.
- [ ] Twelve-month unlock table built with recipient classes.
- [ ] Largest single unlock identified with date and float impact.
- [ ] Amendments to the schedule checked and recorded.
- [ ] Unknowns listed explicitly.

## Sources

- Ethereum token standards documentation: <https://ethereum.org/en/developers/docs/standards/tokens/>
- Investor education on disclosure and dilution: <https://www.investor.gov/introduction-investing>
- Market-microstructure measurement of liquidity and float: <https://doi.org/10.1093/jjfinec/nbt003>
