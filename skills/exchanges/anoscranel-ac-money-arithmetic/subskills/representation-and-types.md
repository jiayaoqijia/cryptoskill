---
name: representation-and-types
domain: software-engineering/representation-and-types
trigger: "Choosing how to store and compute a monetary amount."
anti_trigger: "Not for database schema design, and not for pricing decisions."
scope: "Minor units, decimal types, and why binary floating point fails."
status: seedling
---

# Representation and types

## Standard

Binary floating point cannot represent most decimal fractions exactly, so a value like one-tenth is stored as the nearest binary approximation. Adding such values repeatedly accumulates error, and comparing them for equality fails in ways that appear random. For money, that means a cent can appear or vanish depending on the sequence of operations.

Two representations avoid the problem. Integer minor units store the amount as a whole number of the smallest unit, so addition and subtraction are exact and division requires an explicit rounding decision. A decimal type stores a base-ten significand and an exponent, so decimal fractions are exact and the rounding rule must still be stated. Both require a policy; neither makes the policy unnecessary.

Primary sources: <https://www.iso.org/> and <https://ieeexplore.ieee.org/>.

## Decision rules

- Record the storage representation and the currency's minor unit exponent.
- Record whether the type is exact for the operations performed, and where division enters.
- Record the precision required and the maximum magnitude the type must hold.
- Record the parsing and formatting path, which must not route through binary floating point.
- Record the database column type, which often differs from the application's.
- Record the serialisation format and whether it preserves exactness.

## Procedure

1. Choose integer minor units or a decimal type and record the reason.
2. Record the minor unit exponent per currency, since not all have two.
3. Audit the code path for operations that divide.
4. Verify parsing and formatting are exact end to end.
5. Reconcile the database type with the application's.
6. Record the serialisation format and its exactness.

## Anti-patterns

- Storing money in a binary floating type.
- Assuming every currency has two decimal places.
- Parsing a decimal string through a floating conversion.
- A database column with insufficient precision.
- Serialising as a float in JSON and calling it exact.

## Done checklist

- [ ] Representation recorded with reason.
- [ ] Minor unit exponent recorded per currency.
- [ ] Division points audited.
- [ ] Parse and format path verified exact.
- [ ] Database type reconciled.
- [ ] Serialisation format recorded.

The serialisation point is worth checking at every boundary: a JSON encoder that emits a decimal as a floating number has undone the representation the code chose, and the loss happens silently at the edge rather than in the arithmetic where the policy was made.


## Sources

- Currency code and minor unit standards: <https://www.iso.org/>
- Floating point arithmetic standard: <https://ieeexplore.ieee.org/>
- Payment messaging standards: <https://www.iso20022.org/>
