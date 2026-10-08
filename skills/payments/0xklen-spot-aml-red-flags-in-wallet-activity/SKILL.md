---
name: spot-aml-red-flags-in-wallet-activity
description: Use when reviewing account activity or a wallet history for money-laundering typologies before escalating, and you need on-chain evidence for each flag rather than a general impression.
---

# Spot AML red flags in on-chain activity

A red flag is a pattern plus its supporting transactions. The reviewer's job is to hand the
compliance owner a short list of patterns, each with the hashes that show it, not a narrative
about how the activity "looks suspicious".

## Procedure

1. Pull the activity window into a working file so patterns are reproducible:

       cat > addr.txt <<< "$ADDR"
       curl -s "https://api.etherscan.io/api?module=account&action=txlist&address=$ADDR\
       &startblock=0&endblock=latest&sort=asc&apikey=$ETHERSCAN_API_KEY" \
         | jq -r '.result[] | [.timeStamp,.from,.to,.value] | @csv' > txs.csv
       wc -l txs.csv

2. Check structuring: many transfers sized just under a reporting or travel-rule floor.

       python3 -c '
       import csv
       rows=[float(r[3])/1e18 for r in csv.reader(open("txs.csv")) if r]
       near=[v for v in rows if 0.9e3 <= v <= 3e3]
       print(f"{len(near)} sends in the 900-3000 band")'

3. Check pass-through: value in and out within a short window at a near-identical amount, which
   is layering, not custody. Compare inbound and outbound timestamps and amounts.

4. Check exposure to obfuscation services: deposits to or withdrawals from mixers, privacy pools
   or swap chains. Record the counterparty address, not just the service name.

5. Check burstiness: a dormant address that suddenly moves its whole balance, or an account whose
   volume jumps an order of magnitude against its own baseline.

6. Check counterparty concentration and geography: a retail-looking account whose only
   significant counterparty is a single high-risk cluster is a different case from a market
   maker's routine flow.

7. Write one line per flag as `pattern | tx hashes | why it matches the typology`, and route to
   the compliance owner within the internal window.

## Pitfalls

- Calling normal market-maker or treasury activity layering. High velocity is not a flag on its
  own; the flag is velocity with no economic purpose.
- Reporting a mixer interaction without the address, which is the only part a reviewer can act on.
- Judging by fiat value using today's price; a 2016 transfer's apparent size depends entirely on
  the price at the time, and the ledger entry does not carry it.
- Reading only inbound or only outbound history; the pattern is usually in the join.
- Inferring intent from a pattern. The procedure establishes facts; the inference belongs to the
  reviewer who can weigh the full customer file.

## Verification

    grep -c "," txs.csv && grep -E ",(0\.[0-9]*[0-9]|[0-9]+)," txs.csv | wc -l

Confirm the window you analysed covers the account's full life or state the coverage gap
explicitly at the top of the report.

Report each pattern with its hashes, the coverage window, and the chain(s) reviewed. Whether a
pattern warrants a report is a legal determination that only a qualified officer and counsel can
make.
