---
name: dfs-optimizer
description: "Build optimal Daily Fantasy Sports lineups for DraftKings and FanDuel. Maximize projected points under salary cap constraints for NBA, NFL, and MLB slates."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🏆",
        "requires": { "bins": ["python3"] },
        "credentials": [],
      },
  }
---

# DFS Lineup Optimizer

Build mathematically optimal Daily Fantasy Sports lineups. Uses a greedy salary-cap optimizer to maximize projected fantasy points under DraftKings/FanDuel roster constraints. No paid API needed — paste your own projections or use the built-in samples.

## NBA DraftKings Optimizer

```bash
python3 -c "
import itertools, json

# =====================================================
# PASTE YOUR SLATE HERE
# Format: (name, position, salary, projected_points)
# Positions: PG, SG, SF, PF, C, G (PG/SG), F (SF/PF), UTIL (any)
# DraftKings NBA: 2 PG, 2 SG, 2 SF, 1 PF, 1 C = 8 players, \$50,000 cap
# =====================================================
players = [
    ('LeBron James',     'SF', 9800, 52.4),
    ('Stephen Curry',    'PG', 9600, 51.8),
    ('Nikola Jokic',     'C',  9900, 58.1),
    ('Luka Doncic',      'PG', 10200, 59.2),
    ('Jayson Tatum',     'SF', 9200, 49.3),
    ('Anthony Davis',    'PF', 9400, 53.7),
    ('Ja Morant',        'PG', 8600, 46.2),
    ('Kevin Durant',     'SF', 8800, 47.5),
    ('Joel Embiid',      'C',  9500, 55.0),
    ('Trae Young',       'PG', 8200, 44.1),
    ('Devin Booker',     'SG', 8400, 45.3),
    ('Bam Adebayo',      'C',  7800, 41.2),
    ('DeMar DeRozan',    'SF', 7200, 38.5),
    ('Miles Bridges',    'SF', 6800, 36.1),
    ('Tyrese Haliburton','PG', 8000, 43.7),
    ('Jordan Poole',     'SG', 6200, 32.8),
    ('Franz Wagner',     'SF', 7000, 37.9),
    ('Alperen Sengun',   'C',  7400, 39.8),
    ('Brandon Ingram',   'SF', 7600, 40.5),
    ('Cole Anthony',     'PG', 5600, 28.4),
]

SALARY_CAP = 50000
ROSTER = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 1, 'C': 1}

def greedy_lineup(players, cap, roster_req):
    # Value = pts per \$1000 salary
    valued = [(name, pos, sal, pts, pts / sal * 1000) for name, pos, sal, pts in players]
    valued.sort(key=lambda x: -x[4])  # sort by value desc

    lineup = []
    remaining_slots = dict(roster_req)
    total_salary = 0
    total_pts = 0

    for name, pos, sal, pts, val in valued:
        if remaining_slots.get(pos, 0) > 0 and total_salary + sal <= cap:
            lineup.append((name, pos, sal, pts, val))
            remaining_slots[pos] -= 1
            total_salary += sal
            total_pts += pts
            if all(v == 0 for v in remaining_slots.values()):
                break

    return lineup, total_salary, total_pts

lineup, total_sal, total_pts = greedy_lineup(players, SALARY_CAP, ROSTER)

print('=== DraftKings NBA Optimal Lineup ===')
print(f'{\"Name\":<22} {\"POS\":<5} {\"SALARY\":>8} {\"PROJ\":>7} {\"VALUE\":>8}')
print('-' * 58)
for name, pos, sal, pts, val in sorted(lineup, key=lambda x: list(ROSTER.keys()).index(x[1]) if x[1] in ROSTER else 99):
    print(f'{name:<22} {pos:<5} \${sal:>7,} {pts:>7.1f} {val:>7.2f}x')
print('-' * 58)
print(f'{\"TOTAL\":<22} {\"\":<5} \${total_sal:>7,} {total_pts:>7.1f}')
print(f'Salary remaining: \${SALARY_CAP - total_sal:,}')
"
```

## NFL DraftKings Optimizer

```bash
python3 -c "
# DraftKings NFL: 1 QB, 2 RB, 3 WR, 1 TE, 1 FLEX (RB/WR/TE), 1 DST
# Cap: \$50,000

players = [
    # (name, position, salary, projected_pts)
    ('Patrick Mahomes', 'QB',  8400, 32.1),
    ('Josh Allen',      'QB',  8800, 33.8),
    ('Christian McCaffrey', 'RB', 9200, 38.4),
    ('Austin Ekeler',   'RB',  6800, 26.2),
    ('Breece Hall',     'RB',  7400, 28.9),
    ('Isiah Pacheco',   'RB',  6200, 24.5),
    ('Tyreek Hill',     'WR',  9000, 35.2),
    ('Stefon Diggs',    'WR',  7600, 29.8),
    ('Davante Adams',   'WR',  8200, 32.6),
    ('Jaylen Waddle',   'WR',  7000, 27.4),
    ('Travis Kelce',    'TE',  8600, 34.5),
    ('Mark Andrews',    'TE',  7200, 28.1),
    ('San Francisco 49ers', 'DST', 4200, 12.4),
    ('Kansas City Chiefs', 'DST', 3800, 11.2),
    ('Dallas Cowboys',  'DST', 3600, 10.8),
    ('Ja\'Marr Chase',   'WR',  8600, 34.1),
    ('Alvin Kamara',    'RB',  7000, 27.6),
    ('Sam LaPorta',     'TE',  5800, 22.3),
]

SALARY_CAP = 50000
SLOTS = [('QB', 1), ('RB', 2), ('WR', 3), ('TE', 1), ('DST', 1)]
FLEX_POSITIONS = {'RB', 'WR', 'TE'}

def optimize_nfl(players, cap, slots, flex_count=1):
    from collections import defaultdict
    by_pos = defaultdict(list)
    for p in players:
        name, pos, sal, pts = p
        by_pos[pos].append((name, pos, sal, pts, pts / sal * 1000))
    for pos in by_pos:
        by_pos[pos].sort(key=lambda x: -x[4])

    lineup = []
    total_sal = 0
    total_pts = 0

    for pos, count in slots:
        added = 0
        for player in by_pos[pos]:
            if added >= count: break
            if total_sal + player[2] > cap: continue
            lineup.append(player)
            total_sal += player[2]
            total_pts += player[3]
            added += 1

    # Flex slot
    flex_candidates = []
    in_lineup = {p[0] for p in lineup}
    for pos in FLEX_POSITIONS:
        for p in by_pos[pos]:
            if p[0] not in in_lineup:
                flex_candidates.append(p)
    flex_candidates.sort(key=lambda x: -x[4])
    for p in flex_candidates:
        if total_sal + p[2] <= cap:
            lineup.append(p)
            total_sal += p[2]
            total_pts += p[3]
            break

    return lineup, total_sal, total_pts

lineup, total_sal, total_pts = optimize_nfl(players, SALARY_CAP, SLOTS)

print('=== DraftKings NFL Optimal Lineup ===')
print(f'{\"Name\":<26} {\"POS\":<5} {\"SALARY\":>8} {\"PROJ\":>7}')
print('-' * 52)
for name, pos, sal, pts, val in lineup:
    print(f'{name:<26} {pos:<5} \${sal:>7,} {pts:>7.1f}')
print('-' * 52)
print(f'{\"TOTAL\":<26} {\"\":<5} \${total_sal:>7,} {total_pts:>7.1f}')
"
```

## Stacking Calculator

NFL DFS rewards correlated lineups — QB + receiver from same game:

```bash
python3 -c "
# Stack value: extra points from correlated plays in the same game
def stack_value(qb_proj, wr_proj, correlation=0.35):
    '''
    Correlation bonus — when QB plays well, his WR often does too.
    Expected additional points from stacking vs. independent picks.
    '''
    import math
    stack_bonus = correlation * math.sqrt(qb_proj * wr_proj) * 0.15
    return stack_bonus

stacks = [
    ('Josh Allen',    'Stefon Diggs',   33.8, 29.8),
    ('Patrick Mahomes', 'Travis Kelce', 32.1, 34.5),
    ('Ja\'Marr Chase', 'Joe Burrow',    34.1, 30.2),
]

print('=== Stack Analysis ===')
print(f'{\"QB\":<18} {\"WR/TE\":<18} {\"Combined\":>10} {\"Stack Bonus\":>12} {\"Total\":>8}')
print('-' * 72)
for qb, wr, qb_pts, wr_pts in stacks:
    bonus = stack_value(qb_pts, wr_pts)
    total = qb_pts + wr_pts + bonus
    print(f'{qb:<18} {wr:<18} {qb_pts+wr_pts:>10.1f} {bonus:>+11.2f} {total:>8.1f}')

print()
print('Rule: Stack a QB with his top receiver + the opposing team\'s best WR (game stack).')
"
```

## Ownership & Leverage

Low-ownership plays win big tournaments. Find the right level of contrarian exposure:

```bash
python3 -c "
players = [
    # (name, pos, proj_pts, ownership_pct)
    ('Luka Doncic',     'PG', 59.2, 38.5),
    ('Nikola Jokic',    'C',  58.1, 35.2),
    ('Patrick Mahomes', 'QB', 32.1, 42.0),
    ('Travis Kelce',    'TE', 34.5, 28.4),
    ('Jordan Poole',    'SG', 32.8,  6.2),  # sneaky low ownership
    ('Cole Anthony',    'PG', 28.4,  4.1),  # punt play
]

def leverage_score(proj, ownership):
    '''Points above expected divided by ownership — higher = more leverage in tournaments'''
    expected_points_at_ownership = ownership / 10  # crude baseline
    return (proj - expected_points_at_ownership * 2) / (ownership + 1) * 10

print('=== Ownership & Leverage Analysis ===')
print(f'{\"Player\":<22} {\"PROJ\":>6} {\"OWN%\":>6} {\"LEVERAGE\":>10} {\"PLAY TYPE\":>12}')
print('-' * 65)
for name, pos, proj, own in sorted(players, key=lambda x: -leverage_score(x[2], x[3])):
    lev = leverage_score(proj, own)
    if own < 10: play_type = '🎯 CONTRARIAN'
    elif own < 20: play_type = '⚡ LEVERAGE'
    elif own > 35: play_type = '⚠️  CHALK'
    else: play_type = '✅ BALANCED'
    print(f'{name:<22} {proj:>6.1f} {own:>5.1f}% {lev:>+9.2f}  {play_type}')

print()
print('Cash games: Use chalk (high ownership) — optimize for consistency')
print('Tournaments: Target 1-2 contrarian plays with strong projections')
"
```

## Quick Reference

| Format | Salary Cap | Roster |
|--------|-----------|--------|
| DK NBA | \$50,000 | 2PG/2SG/2SF/1PF/1C |
| DK NFL | \$50,000 | 1QB/2RB/3WR/1TE/1FLEX/1DST |
| DK MLB | \$50,000 | 2P/1C/1B/2B/3B/SS/3OF |
| FD NBA | \$60,000 | 2PG/2SG/2SF/1PF/1C |
| FD NFL | \$60,000 | 1QB/2RB/3WR/1TE/1FLEX/1K |

## Tips

1. **Always stack in tournaments** — correlated lineups have higher variance (good)
2. **Go contrarian on big slates** — 12+ game slates reward unique lineups
3. **Injury news is alpha** — late scratch creates value in replacement players
4. **Vegas totals matter** — high over/under games produce more fantasy points
5. **Never maximize ownership** — the crowd is already pricing in the obvious plays

## Author

Created by [Ian Alloway](https://github.com/ianalloway) — Data Scientist specializing in sports analytics and ML.

## License

MIT License
