---
name: central-bank-communication
domain: investing/central-bank-communication
trigger: "Reading a central-bank statement for commitments rather than suggestions."
anti_trigger: "Not for predicting the next decision, and not for trading the announcement."
scope: "What a statement commits to, what the minutes add, and how to separate signal from ritual."
status: seedling
---

# Central bank communication

## Standard

A policy statement is a negotiated document with a small number of sentences that carry weight: the decision, the forward guidance, and any change in the description of conditions. The rest is ritual, repeated so that its absence would be news. Reading the statement means diffing it against the previous one and noting exactly which sentences changed.

The minutes and speeches add context but not commitments. A commitment is something the committee has said it will do conditional on stated conditions; a suggestion is anything else. Treating suggestions as commitments is the most common reading error, and it produces expectations that the committee never agreed to meet.

Primary sources: <https://www.federalreserve.gov/> and <https://fred.stlouisfed.org/>.

## Decision rules

- Diff the statement against the previous one and record the changed sentences verbatim.
- Separate the decision from the guidance from the description of conditions.
- Classify each forward-looking sentence as commitment, condition, or suggestion.
- Record the vote and any dissent; unanimity and a split carry different information.
- Treat minutes and speeches as context, never as new commitments.
- Record the market's reaction separately, and note where it exceeded what the text supports.

## Procedure

1. Obtain the current and previous statements.
2. Diff them and record the changed sentences.
3. Classify the forward-looking language.
4. Record the vote and dissents.
5. Note the market reaction against the text.
6. Write the reading with the classification explicit.

## Anti-patterns

- Reading the statement without the previous one.
- Treating guidance as a promise.
- Ignoring dissents.
- Inferring a change from the absence of a sentence without checking the convention.
- Reading the reaction as the text's meaning.

## Done checklist

- [ ] Statements diffed and changes recorded verbatim.
- [ ] Decision, guidance, and conditions separated.
- [ ] Forward-looking sentences classified.
- [ ] Vote and dissents recorded.
- [ ] Reaction separated from text.
- [ ] Reading written with classification.

## Sources

- Central-bank policy statements and minutes: <https://www.federalreserve.gov/>
- Rate and macro series: <https://fred.stlouisfed.org/>
- Investor education on monetary policy: <https://www.investor.gov/introduction-investing>

The diff discipline is what makes the reading cheap: most statements change two sentences, and the rest is convention. Reading the whole document each time is how an investor mistakes ritual for signal, because ritual is most of the text.

The vote is underrated as a signal. A unanimous decision with unchanged language says the committee is comfortable; a split decision with a change in the description of conditions says the next move is contested, and the two carry different implications for how long the current setting will last.
