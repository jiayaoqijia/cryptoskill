# Borrowing on Based Loans

## How a loan is sized

- The most you can borrow is the collateral's value times its max loan-to-value (50% on every current market), limited by the USDC lenders have made available for that token.
- `quote_borrow` takes a collateral amount and, optionally, a loan amount. Leave the loan amount out to borrow the most the collateral allows. If you name a smaller amount, only the collateral needed is taken; the rest stays in the wallet.
- The loan fee (2.49% today) is taken out of the loan amount. Example from a live quote: loan 71.55 USDC, fee 1.78, received 69.77.
- The buyback cost is the loan amount plus the term's cost, fixed at opening. The same loan on the short term costs 73.34 USDC to buy back (71.55 × 1.025).

## Short funding

Lenders are queued per token. The contract stops adding lenders once less than 50 USDC of the loan is still unfunded, so a loan can be funded a little short of what was asked. `quote_borrow` replays the queue and tells you exactly what would happen:

- `partialFill: true` plus a warning means the loan would be funded short. Offer the user `fullFillLoanAmountUsdc`, which is the largest amount that funds in full.
- `wouldFail` set means the loan cannot open (for example, the collateral supports less than the 50 USDC minimum). Explain the reason and don't build it.
- `build_borrow` refuses loans that would fail. It also refuses loans funded more than 25% short unless you pass a higher `max_shortfall_bps`.

## Opening

`build_borrow` returns up to two transactions: an approval for the collateral token (only if the allowance is too low), then the loan itself. The user signs them in order. The USDC arrives in the same transaction that opens the loan.

## During the loan

- Nothing happens if the price moves. There are no liquidations and no margin calls.
- `get_borrower_loans` shows status, buyback remaining and due date. `get_loan` shows one loan in detail.

## Buying back

- Full: `build_buyback` with only the loan ID. All collateral comes back.
- Partial: pass `payment_usdc` (at least 1 USDC, at most what is still owed). Collateral comes back in proportion to the payment, and the rest stays in the loan until it is bought back or the due date passes.
- Approval: buyback payments approve the lending ledger contract, not the core contract. `build_buyback` handles this.
- Deadline: buybacks must land before the due date. Suggest a buffer: due dates are exact to the second.

## Default

If the due date passes without a full buyback, the borrower keeps the USDC and the remaining collateral goes to the lenders who funded the loan. The borrower owes nothing more, and nothing affects any other loan.
