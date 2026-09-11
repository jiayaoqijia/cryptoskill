---
name: streak-tracker
description: "Track hot and cold streaks for sports teams and players. Identify momentum patterns, ATS performance trends, and regression-to-mean signals."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["python3"] },
        "credentials": [],
      },
  }
---

# Streak Tracker

Momentum matters in sports betting. This skill helps you identify hot/cold streaks, ATS trends, and over/under patterns to find teams due for regression — or continuation.

## Basic Streak Analyzer

Input a team's recent results and get a full streak breakdown:

```bash
python3 -c "
def analyze_streak(team, results):
    '''
    results: list of dicts with keys: opponent, margin, ats_result, total_result
    ats_result: 'W'=covered, 'L'=didn't cover, 'P'=push
    total_result: 'O'=over, 'U'=under, 'P'=push
    margin: point differential (positive = win, negative = loss)
    '''
    wins   = [r for r in results if r['margin'] > 0]
    losses = [r for r in results if r['margin'] < 0]
    ats_w  = [r for r in results if r.get('ats_result') == 'W']
    ats_l  = [r for r in results if r.get('ats_result') == 'L']
    overs  = [r for r in results if r.get('total_result') == 'O']
    unders = [r for r in results if r.get('total_result') == 'U']

    # Current straight-up streak
    su_streak = 0
    su_dir = 'W' if results[0]['margin'] > 0 else 'L'
    for r in results:
        if (r['margin'] > 0 and su_dir == 'W') or (r['margin'] < 0 and su_dir == 'L'):
            su_streak += 1
        else:
            break

    # Current ATS streak
    ats_streak = 0
    ats_dir = results[0].get('ats_result', 'P')
    for r in results:
        if r.get('ats_result') == ats_dir and ats_dir != 'P':
            ats_streak += 1
        else:
            break

    avg_margin = sum(r['margin'] for r in results) / len(results)

    print(f'=== Streak Report: {team} (Last {len(results)} games) ===')
    print()
    print(f'SU Record:    {len(wins)}-{len(losses)}  (current streak: {su_streak}{su_dir})')
    print(f'ATS Record:   {len(ats_w)}-{len(ats_l)}  (current streak: {ats_streak}{ats_dir})')
    print(f'O/U Split:    {len(overs)}O / {len(unders)}U')
    print(f'Avg Margin:   {avg_margin:+.1f} pts')
    print()

    # Momentum signal
    if su_streak >= 5:
        print(f'🔥 HOT STREAK: {su_streak} straight {su_dir}s')
        print('   Beware of regression — market may be overvaluing')
    elif su_streak <= -4 or (su_dir == 'L' and su_streak >= 4):
        print(f'🥶 COLD STREAK: {su_streak} consecutive losses')
        print('   Look for value — market may be undervaluing')

    if len(ats_w) >= 7:
        print(f'📈 ATS HOT: {len(ats_w)}-{len(ats_l)} ATS — public fading becomes attractive')
    elif len(ats_l) >= 7:
        print(f'📉 ATS COLD: {len(ats_w)}-{len(ats_l)} ATS — sharp money may target them as fade')

    if len(overs) >= 7:
        print(f'🔓 OVER TREND: {len(overs)} overs in last {len(results)} — total may be inflated')
    elif len(unders) >= 7:
        print(f'🔒 UNDER TREND: {len(unders)} unders in last {len(results)} — look for unders')

# Example: Lakers last 10 games
lakers = [
    {'opponent': 'OKC',  'margin': +8,  'ats_result': 'W', 'total_result': 'O'},
    {'opponent': 'PHX',  'margin': +3,  'ats_result': 'L', 'total_result': 'U'},
    {'opponent': 'GSW',  'margin': +15, 'ats_result': 'W', 'total_result': 'O'},
    {'opponent': 'DEN',  'margin': +6,  'ats_result': 'W', 'total_result': 'O'},
    {'opponent': 'MIA',  'margin': -2,  'ats_result': 'L', 'total_result': 'U'},
    {'opponent': 'BKN',  'margin': +11, 'ats_result': 'W', 'total_result': 'O'},
    {'opponent': 'NYK',  'margin': +4,  'ats_result': 'W', 'total_result': 'U'},
    {'opponent': 'TOR',  'margin': +9,  'ats_result': 'W', 'total_result': 'O'},
    {'opponent': 'CHI',  'margin': -5,  'ats_result': 'L', 'total_result': 'U'},
    {'opponent': 'ATL',  'margin': +7,  'ats_result': 'W', 'total_result': 'O'},
]
analyze_streak('Los Angeles Lakers', lakers)
"
```

## Regression-to-Mean Detector

Find teams statistically due for a reversal:

```bash
python3 -c "
def regression_signal(team, win_pct, ats_win_pct, avg_point_diff, games=10):
    '''
    Identify if a team's recent results look sustainable or due for regression.
    '''
    print(f'=== Regression Analysis: {team} ===')
    print(f'Win %: {win_pct:.1%}  |  ATS Win %: {ats_win_pct:.1%}  |  Avg Margin: {avg_point_diff:+.1f}')
    print()

    signals = []

    # Win % check
    if win_pct > 0.80:
        signals.append(('🔴 SELL', f'Win% ({win_pct:.0%}) is unsustainably high — regression likely'))
    elif win_pct < 0.20:
        signals.append(('🟢 BUY', f'Win% ({win_pct:.0%}) is depressed — bounce candidate'))

    # ATS sustainability
    if ats_win_pct > 0.75:
        signals.append(('🔴 FADE ATS', f'ATS% ({ats_win_pct:.0%}) over 10 games never holds — market adjusts'))
    elif ats_win_pct < 0.25:
        signals.append(('🟢 BACK ATS', f'ATS% ({ats_win_pct:.0%}) — oddsmakers likely over-adjusted'))

    # Margin sustainability
    if avg_point_diff > 18:
        signals.append(('⚠️  WARN', f'Avg margin +{avg_point_diff} pts is extraordinary — injury risk or schedule soft spot'))
    elif avg_point_diff < -15:
        signals.append(('⚠️  WARN', f'Avg margin {avg_point_diff} pts — could be tanking or missing key players'))

    # Pythagorean expectation proxy
    if avg_point_diff > 0 and win_pct < 0.40:
        signals.append(('🟢 VALUE', 'Outgaining opponents but losing — likely due for positive variance'))
    elif avg_point_diff < 0 and win_pct > 0.60:
        signals.append(('🔴 OVERRATED', 'Win% driven by luck — negative margins say fade'))

    if not signals:
        signals.append(('⚪ NEUTRAL', 'Results appear sustainable — no strong regression signal'))

    for label, msg in signals:
        print(f'{label}: {msg}')

# Example
regression_signal('Boston Celtics', win_pct=0.90, ats_win_pct=0.80, avg_point_diff=+14.5, games=10)
print()
regression_signal('Washington Wizards', win_pct=0.20, ats_win_pct=0.30, avg_point_diff=-8.2, games=10)
"
```

## Home/Away Split Tracker

Some teams are completely different animals at home vs. away:

```bash
python3 -c "
def home_away_split(team, home_results, away_results):
    def stats(results):
        wins = sum(1 for r in results if r['margin'] > 0)
        ats  = sum(1 for r in results if r.get('ats_result') == 'W')
        avg  = sum(r['margin'] for r in results) / len(results) if results else 0
        return wins, len(results) - wins, ats, len(results) - ats, avg

    hw, hl, hats_w, hats_l, havg = stats(home_results)
    aw, al, aats_w, aats_l, aavg = stats(away_results)

    print(f'=== Home/Away Split: {team} ===')
    print(f'{'':20} {'HOME':>12} {'AWAY':>12} {'DIFF':>10}')
    print(f'{'SU Record':20} {hw}-{hl:>10} {aw}-{al:>10}')
    print(f'{'ATS Record':20} {hats_w}-{hats_l:>10} {aats_w}-{aats_l:>10}')
    print(f'{'Avg Margin':20} {havg:>+11.1f} {aavg:>+10.1f} {havg-aavg:>+9.1f}')
    print()

    diff = havg - aavg
    if diff > 10:
        print(f'⚠️  MAJOR HOME/AWAY SPLIT: +{diff:.1f} pts at home vs away')
        print('   Adjust line significantly when they travel')
    elif diff > 5:
        print(f'Notable split: +{diff:.1f} pts home advantage above league avg')

home = [
    {'margin': +12, 'ats_result': 'W'}, {'margin': +8, 'ats_result': 'W'},
    {'margin': +3, 'ats_result': 'L'}, {'margin': +20, 'ats_result': 'W'},
    {'margin': +7, 'ats_result': 'W'},
]
away = [
    {'margin': -3, 'ats_result': 'L'}, {'margin': +2, 'ats_result': 'W'},
    {'margin': -8, 'ats_result': 'L'}, {'margin': -1, 'ats_result': 'L'},
    {'margin': +5, 'ats_result': 'W'},
]
home_away_split('Denver Nuggets', home, away)
"
```

## Back-to-Back Fatigue Filter

NBA/NHL games on zero rest produce massive ATS edges:

```bash
python3 -c "
def b2b_analysis(b2b_results, rested_results):
    def pct(results, key, val):
        hits = sum(1 for r in results if r.get(key) == val)
        return hits / len(results) if results else 0

    b2b_ats = pct(b2b_results, 'ats_result', 'W')
    rest_ats = pct(rested_results, 'ats_result', 'W')
    b2b_margin = sum(r['margin'] for r in b2b_results) / len(b2b_results) if b2b_results else 0
    rest_margin = sum(r['margin'] for r in rested_results) / len(rested_results) if rested_results else 0

    print('=== Back-to-Back Fatigue Analysis ===')
    print(f'On B2B:  ATS {b2b_ats:.0%}  Avg Margin {b2b_margin:+.1f}')
    print(f'Rested:  ATS {rest_ats:.0%}  Avg Margin {rest_margin:+.1f}')
    print(f'Fatigue penalty: {b2b_margin - rest_margin:+.1f} pts per game')
    print()

    if b2b_ats < 0.35:
        print('🔴 SIGNIFICANT B2B FADE SPOT — this team struggles mightily with no rest')
        print('   Lean toward fading them on second night of back-to-back')
    elif b2b_ats < 0.45:
        print('⚠️  Slight B2B disadvantage — worth noting as tiebreaker')
    else:
        print('✅ Team handles back-to-backs reasonably — no strong fade signal')

# Example
b2b = [
    {'margin': -6, 'ats_result': 'L'}, {'margin': -11, 'ats_result': 'L'},
    {'margin': +2, 'ats_result': 'L'}, {'margin': -4, 'ats_result': 'L'},
    {'margin': -9, 'ats_result': 'L'},
]
rested = [
    {'margin': +10, 'ats_result': 'W'}, {'margin': +5, 'ats_result': 'W'},
    {'margin': -2, 'ats_result': 'L'}, {'margin': +8, 'ats_result': 'W'},
    {'margin': +12, 'ats_result': 'W'},
]
b2b_analysis(b2b, rested)
"
```

## Quick Reference

| Pattern | Betting Implication |
|---------|-------------------|
| 5+ SU win streak | Fade — market overvalues, line inflated |
| 0-5 ATS on the road | Automatic home-team ATS lean |
| 7+ overs in a row | Look for sharp under plays |
| B2B on road | One of strongest consistent ATS edges |
| Win% > margin | Regression coming — fade |
| Margin > Win% | Positive variance pending — back |

## Author

Created by [Ian Alloway](https://github.com/ianalloway) — Data Scientist specializing in sports analytics and ML.

## License

MIT License
