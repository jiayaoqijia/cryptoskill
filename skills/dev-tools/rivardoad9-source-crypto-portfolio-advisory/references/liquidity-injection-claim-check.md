# Verifying "the Fed will inject $X tomorrow" claims

## Why this recurs
Social posts recycle routine desk operations as rescues. The number is usually real; the meaning is
replaced. The job is to identify the operation, then decide whether it is liquidity, and whether it
is a catalyst at all.

## Decision order

1. **What is actually on the calendar for that date?** NY Fed desk pages list operations with dates.
   Reverse repo **drains** cash (money funds lend to the Fed); repo **adds**. A reverse-repo entry is
   the opposite of an injection, and it runs almost every business day.
2. **If the number is a Treasury bill purchase**, it is reinvestment or a reserve management purchase
   (RMP): routine, pre-announced, sized in the monthly schedule (Oct 2026: ~$17.6B reinvestment plus
   ~$10B RMP). It does add reserves, but it is maintenance, not a rescue.
3. **Put the size against the balance sheet.** $8.6B against ~$6.5T is ~0.13% — smaller than one day
   of crypto volatility. Say the ratio out loud instead of letting the headline stand.
4. **Look for actual funding stress, which is absent if the claim is fake.** SOFR above the target
   range, repo rate spiking, RRP draining to zero, reserve balances falling. If none of those print,
   there is no injection story to tell — only a schedule.
5. **Check blackout.** FOMC dates come from the Fed calendar; the blackout starts the second Saturday
   before the meeting. During blackout no official can signal anything that week, so any "emergency"
   has to show up in the desk data first.
6. **Verdict shape:** what is scheduled → what it does → the stress evidence → therefore it is / is not
   a catalyst. If it is not, say to remove it from the trade thesis, because a phantom catalyst makes
   the user unable to explain a loss.

## Worked snapshot (18 Oct 2026)

SOFR 3.89%, flat all month (3.87–3.89). Fed overnight repo outstanding 0.000 (16 Oct) = no injection
happening. Reverse-repo operation listed for 19 Oct. FOMC 27–28 Oct, so blackout from 17 Oct. The
"$8,633,000,000 injection" circulating on Instagram/Facebook was a routine bill purchase inside the
monthly RMP/reinvestment schedule.

## Audit the claim list before computing any probability

When the user pastes a list of macro claims ("oil above 100, banks dumping, VIX 4-month high..."),
label every line **benar / salah / tidak terverifikasi** against live data *before* answering the
probability question. In the 18 Oct list, 3 held, 2 were factually wrong (XLF was up 2.3% on the week;
US10Y was down 3% on the week), 2 were unverifiable (inflation print, AI-fund rumour) and 1 was
exaggerated. Wrong inputs carry the bearish framing — correcting them changes the trade, and it is the
honest version of disagreeing with the user's gut.

## Endpoints that worked from this VPS

- `markets.newyorkfed.org/api/rates/secured/sofr/last/10.json` — SOFR prints (JSON, fast)
- `newyorkfed.org/markets/desk-operations/reverse-repo` and `/repo` — dated operation calendar (HTML)
- `federalreserve.gov/monetarypolicy/fomccalendars.htm` — FOMC dates and blackout window
- `markets.newyorkfed.org/api/operations/list.json?startDate=…` returns 400 with those params; scrape
  the desk pages instead
- FRED `fredgraph.csv` times out from this IP — do not burn a 180s call on it; use the NY Fed pages
  and the SOFR endpoint

## Failure modes

- Confusing reverse repo with repo, then reporting a drain as a rescue.
- Treating reinvestment or RMP as stimulus.
- Trusting a headline with a precise number but no date or operation type.
- Feeding a rumoured injection into a bullish thesis without a single funding-stress datapoint.
