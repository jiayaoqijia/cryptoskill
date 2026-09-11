---
name: bet-journal
description: "Track your sports bets in a local CSV journal. Calculate ROI, CLV, win rate by sport/bet-type, and identify where you're actually making money."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📒",
        "requires": { "bins": ["python3"] },
        "credentials": [],
      },
  }
---

# Bet Journal

The most important edge in sports betting isn't picking winners — it's *tracking* your bets to learn where your edge is real vs. imagined. This skill creates and analyzes a local CSV bet journal.

## Initialize the Journal

```bash
python3 -c "
import csv, os

JOURNAL_FILE = os.path.expanduser('~/.openclaw/bet-journal.csv')
os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)

HEADERS = ['date', 'sport', 'game', 'bet_type', 'pick', 'odds_american',
           'stake', 'result', 'pnl', 'closing_odds', 'notes']

if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, 'w', newline='') as f:
        csv.DictWriter(f, fieldnames=HEADERS).writeheader()
    print(f'Journal created: {JOURNAL_FILE}')
else:
    print(f'Journal already exists: {JOURNAL_FILE}')

print()
print('Fields:')
for h in HEADERS:
    print(f'  {h}')
print()
print('result values: W (win), L (loss), P (push), V (void)')
print('bet_type values: ML (moneyline), SPREAD, TOTAL, PARLAY, PROP, FUTURES')
"
```

## Add a Bet

```bash
python3 -c "
import csv, os
from datetime import date

JOURNAL_FILE = os.path.expanduser('~/.openclaw/bet-journal.csv')

def add_bet(sport, game, bet_type, pick, odds_american, stake, result, closing_odds=None, notes=''):
    if result == 'W':
        if odds_american > 0:
            pnl = stake * odds_american / 100
        else:
            pnl = stake * 100 / abs(odds_american)
    elif result in ('L',):
        pnl = -stake
    else:
        pnl = 0  # push or void

    row = {
        'date': date.today().isoformat(),
        'sport': sport,
        'game': game,
        'bet_type': bet_type,
        'pick': pick,
        'odds_american': odds_american,
        'stake': stake,
        'result': result,
        'pnl': round(pnl, 2),
        'closing_odds': closing_odds or '',
        'notes': notes,
    }

    with open(JOURNAL_FILE, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=row.keys()).writerow(row)

    print(f'Added: {sport} | {game} | {pick} ({odds_american:+d}) | Result: {result} | P&L: {pnl:+.2f}')

# --- EDIT THESE TO LOG YOUR BET ---
add_bet(
    sport='NBA',
    game='Lakers vs Warriors',
    bet_type='SPREAD',
    pick='Warriors -3.5',
    odds_american=-110,
    stake=100,
    result='W',          # W / L / P / V
    closing_odds=-115,    # Line at close (for CLV tracking)
    notes='Sharp action on Warriors, public on Lakers',
)
"
```

## View Your Dashboard

```bash
python3 -c "
import csv, os
from collections import defaultdict

JOURNAL_FILE = os.path.expanduser('~/.openclaw/bet-journal.csv')

if not os.path.exists(JOURNAL_FILE):
    print('No journal found. Run the init script first.')
    exit()

bets = []
with open(JOURNAL_FILE) as f:
    for row in csv.DictReader(f):
        row['stake'] = float(row['stake'])
        row['pnl'] = float(row['pnl'])
        row['odds_american'] = int(row['odds_american'])
        bets.append(row)

if not bets:
    print('No bets logged yet.')
    exit()

wins   = [b for b in bets if b['result'] == 'W']
losses = [b for b in bets if b['result'] == 'L']
pushes = [b for b in bets if b['result'] in ('P', 'V')]

total_bets = len(wins) + len(losses)
win_rate = len(wins) / total_bets if total_bets else 0
total_wagered = sum(b['stake'] for b in bets)
total_pnl = sum(b['pnl'] for b in bets)
roi = total_pnl / total_wagered if total_wagered else 0

print('=== Bet Journal Dashboard ===')
print(f'Record:       {len(wins)}-{len(losses)}-{len(pushes)}')
print(f'Win Rate:     {win_rate:.1%}')
print(f'Total Wagered: \${total_wagered:,.2f}')
print(f'Net P&L:      {total_pnl:+,.2f}')
print(f'ROI:          {roi:+.1%}')
print()

# By sport
by_sport = defaultdict(list)
for b in bets:
    by_sport[b['sport']].append(b)

print('=== P&L by Sport ===')
for sport, sbets in sorted(by_sport.items()):
    sw = sum(1 for b in sbets if b['result'] == 'W')
    sl = sum(1 for b in sbets if b['result'] == 'L')
    spnl = sum(b['pnl'] for b in sbets)
    swag = sum(b['stake'] for b in sbets)
    sroi = spnl / swag if swag else 0
    print(f'  {sport:<8} {sw}-{sl}  P&L: {spnl:+.2f}  ROI: {sroi:+.1%}')

# By bet type
print()
print('=== P&L by Bet Type ===')
by_type = defaultdict(list)
for b in bets:
    by_type[b['bet_type']].append(b)

for bt, tbets in sorted(by_type.items()):
    tw = sum(1 for b in tbets if b['result'] == 'W')
    tl = sum(1 for b in tbets if b['result'] == 'L')
    tpnl = sum(b['pnl'] for b in tbets)
    twag = sum(b['stake'] for b in tbets)
    troi = tpnl / twag if twag else 0
    print(f'  {bt:<10} {tw}-{tl}  P&L: {tpnl:+.2f}  ROI: {troi:+.1%}')
"
```

## Closing Line Value (CLV) Calculator

CLV is the #1 predictor of long-term betting success. If you consistently beat the closing line, you have a real edge:

```bash
python3 -c "
import csv, os

JOURNAL_FILE = os.path.expanduser('~/.openclaw/bet-journal.csv')

def american_to_prob(american):
    if american > 0:
        return 100 / (american + 100)
    else:
        return abs(american) / (abs(american) + 100)

bets_with_clv = []
with open(JOURNAL_FILE) as f:
    for row in csv.DictReader(f):
        if row['closing_odds']:
            open_prob = american_to_prob(int(row['odds_american']))
            close_prob = american_to_prob(int(row['closing_odds']))
            clv = close_prob - open_prob  # positive = you got better than closing line
            bets_with_clv.append({**row, 'clv': clv, 'open_prob': open_prob, 'close_prob': close_prob})

if not bets_with_clv:
    print('No CLV data yet — add closing_odds when logging bets')
    exit()

avg_clv = sum(b['clv'] for b in bets_with_clv) / len(bets_with_clv)
positive_clv = sum(1 for b in bets_with_clv if b['clv'] > 0)

print('=== Closing Line Value Report ===')
print(f'Bets with CLV data: {len(bets_with_clv)}')
print(f'Avg CLV:            {avg_clv:+.2%}')
print(f'Beat closing line:  {positive_clv}/{len(bets_with_clv)} ({positive_clv/len(bets_with_clv):.0%})')
print()

if avg_clv > 0.01:
    print('VERDICT: ✅ Positive CLV — you are buying at better than market prices')
    print('         Your edge is REAL. Keep doing what you are doing.')
elif avg_clv > -0.01:
    print('VERDICT: ⚪ Neutral CLV — roughly breaking even vs. market')
    print('         Improve line shopping and timing to push positive.')
else:
    print('VERDICT: 🔴 Negative CLV — you are consistently getting bad lines')
    print('         Shop more books, bet earlier when sharp action moves lines')
print()
print('Recent CLV (last 5 bets):')
for b in bets_with_clv[-5:]:
    clv_str = f\"{b['clv']:+.2%}\"
    print(f\"  {b['game']:<30} {b['pick']:<20} CLV: {clv_str}\")
"
```

## Monthly P&L Chart

```bash
python3 -c "
import csv, os
from collections import defaultdict

JOURNAL_FILE = os.path.expanduser('~/.openclaw/bet-journal.csv')

monthly = defaultdict(float)
with open(JOURNAL_FILE) as f:
    for row in csv.DictReader(f):
        month = row['date'][:7]  # YYYY-MM
        monthly[month] += float(row['pnl'])

print('=== Monthly P&L ===')
running = 0
for month in sorted(monthly):
    pnl = monthly[month]
    running += pnl
    bar_len = int(abs(pnl) / 10)
    bar = ('█' * min(bar_len, 30)) if pnl >= 0 else ('▓' * min(bar_len, 30))
    sign = '+' if pnl >= 0 else ''
    color_prefix = '🟢' if pnl >= 0 else '🔴'
    print(f'{color_prefix} {month}  {sign}{pnl:>8.2f}  {bar}  (running: {running:+.2f})')
"
```

## Import from Bet Tracker Apps

Convert Action Network or Betstamp exports to journal format:

```bash
python3 -c "
import csv, os

# Converts a basic Action Network CSV export
def import_action_network(input_file, output_file):
    rows_added = 0
    with open(input_file) as fin, open(output_file, 'a', newline='') as fout:
        reader = csv.DictReader(fin)
        writer = None
        for row in reader:
            mapped = {
                'date': row.get('Date', ''),
                'sport': row.get('Sport', ''),
                'game': row.get('Event', ''),
                'bet_type': row.get('Type', 'ML'),
                'pick': row.get('Pick', ''),
                'odds_american': row.get('Odds', '0'),
                'stake': row.get('Risk', '0').replace('\$', '').replace(',', ''),
                'result': 'W' if row.get('Result') == 'Won' else 'L' if row.get('Result') == 'Lost' else 'P',
                'pnl': row.get('Profit', '0').replace('\$', '').replace(',', ''),
                'closing_odds': '',
                'notes': 'imported from Action Network',
            }
            if writer is None:
                writer = csv.DictWriter(fout, fieldnames=mapped.keys())
            writer.writerow(mapped)
            rows_added += 1
    print(f'Imported {rows_added} bets from {input_file}')

print('Usage: import_action_network(\"action_export.csv\", \"~/.openclaw/bet-journal.csv\")')
print('Modify the field mapping above to match your export format.')
"
```

## The Numbers That Matter

| Metric | Break-even | Good | Elite |
|--------|-----------|------|-------|
| Win Rate (at -110) | 52.4% | 54%+ | 57%+ |
| ROI | 0% | +3%+ | +8%+ |
| Average CLV | 0% | +1%+ | +2.5%+ |
| CLV Beat Rate | 50% | 55%+ | 60%+ |

> Track everything. Your gut thinks you're winning everywhere. Your spreadsheet knows the truth.

## Author

Created by [Ian Alloway](https://github.com/ianalloway) — Data Scientist specializing in sports analytics and ML.

## License

MIT License
