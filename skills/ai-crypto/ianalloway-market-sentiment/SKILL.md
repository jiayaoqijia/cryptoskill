---
name: market-sentiment
description: "Analyze market sentiment for stocks and crypto using Reddit, news headlines, and fear/greed indicators. Get a quick read on crowd psychology before trading."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["python3", "curl"] },
        "credentials": [],
      },
  }
---

# Market Sentiment Analyzer

Read the crowd before you trade. Pulls sentiment signals from Reddit mentions, news headline tone, and the Fear & Greed Index to give you a directional bias for stocks and crypto.

## Fear & Greed Index (Crypto)

```bash
curl -s "https://api.alternative.me/fng/?limit=7" | python3 -c "
import json, sys
data = json.load(sys.stdin)['data']
print('=== Crypto Fear & Greed Index ===')
for d in data:
    value = int(d['value'])
    label = d['value_classification']
    date = d['timestamp']
    bar = '█' * (value // 5) + '░' * (20 - value // 5)
    print(f'{label:<18} [{bar}] {value:>3}/100')
print()
print(f'Current Reading: {data[0][\"value_classification\"]} ({data[0][\"value\"]})')
if int(data[0]['value']) < 25:
    print('Signal: EXTREME FEAR — historically good accumulation zone')
elif int(data[0]['value']) > 75:
    print('Signal: EXTREME GREED — consider reducing exposure')
else:
    print('Signal: Neutral — wait for extremes for high-conviction entries')
"
```

## Reddit Mention Counter (Crypto/Stocks)

Track how many times a ticker is mentioned across Reddit finance subs:

```bash
python3 -c "
import urllib.request, json, re, sys

def reddit_mentions(ticker, subreddits=['wallstreetbets', 'CryptoMoonShots', 'investing', 'stocks', 'CryptoCurrency']):
    ticker = ticker.upper()
    counts = {}
    headers = {'User-Agent': 'SentimentBot/1.0'}

    for sub in subreddits:
        url = f'https://www.reddit.com/r/{sub}/search.json?q={ticker}&sort=new&limit=25&t=day'
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read())
            posts = data['data']['children']
            count = sum(1 for p in posts if ticker in p['data'].get('title','').upper())
            counts[sub] = count
        except:
            counts[sub] = -1  # rate limited or error

    total = sum(v for v in counts.values() if v >= 0)
    print(f'=== Reddit Mentions: \${ticker} (Last 24h) ===')
    for sub, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        bar = '█' * min(cnt, 20)
        if cnt >= 0:
            print(f'r/{sub:<25} {bar} {cnt}')
        else:
            print(f'r/{sub:<25} (rate limited)')
    print(f'Total mentions: {total}')

    if total > 50:
        print('Buzz level: 🔥 HIGH - possible pump or breakout chatter')
    elif total > 15:
        print('Buzz level: ⚡ MODERATE - watch for momentum')
    else:
        print('Buzz level: 😴 LOW - under the radar')

# Change ticker here
reddit_mentions('BTC')
"
```

## Headline Sentiment Scorer

Score the sentiment of recent news headlines for any ticker using basic NLP:

```bash
python3 -c "
import urllib.request, json, re

BULLISH = ['surge', 'rally', 'soar', 'breakout', 'gain', 'beat', 'outperform', 'upgrade',
           'buy', 'bullish', 'record', 'growth', 'profit', 'upside', 'strong', 'win', 'rise']
BEARISH = ['crash', 'plunge', 'drop', 'fall', 'loss', 'miss', 'downgrade', 'sell',
           'bearish', 'risk', 'warn', 'weak', 'concern', 'debt', 'decline', 'probe', 'lawsuit']

def score_headline(text):
    text = text.lower()
    bull = sum(1 for w in BULLISH if w in text)
    bear = sum(1 for w in BEARISH if w in text)
    if bull > bear: return '🟢 BULLISH', bull - bear
    elif bear > bull: return '🔴 BEARISH', bear - bull
    else: return '⚪ NEUTRAL', 0

# Sample headlines — replace with live feed or paste your own
headlines = [
    'Bitcoin surges past 70k as institutional demand grows',
    'Fed signals rate cuts may come sooner than expected',
    'Apple beats earnings estimates, stock rises 3%',
    'Crypto exchange hacked, user funds at risk',
    'Tesla misses delivery targets for second quarter',
    'Gold hits record high amid inflation concerns',
    'NVIDIA upgrade: analysts raise price target to 1200',
    'Bank earnings decline as loan losses mount',
]

print('=== Headline Sentiment Analysis ===')
scores = []
for h in headlines:
    label, strength = score_headline(h)
    print(f'{label}  (strength: {strength})  {h[:60]}')
    scores.append(1 if '🟢' in label else -1 if '🔴' in label else 0)

avg = sum(scores) / len(scores)
print()
print(f'Overall Bias: {avg:+.2f}')
if avg > 0.3: print('Market Tone: Broadly bullish — momentum favors longs')
elif avg < -0.3: print('Market Tone: Broadly bearish — risk-off sentiment')
else: print('Market Tone: Mixed — wait for clarity')
"
```

## Volatility Spike Detector (Options-Implied)

Estimate market fear from VIX-equivalent moves:

```bash
python3 -c "
# Rough VIX interpretation for position sizing context
vix_levels = [
    (0,  15,  'Low Fear',     '✅', 'Trend-following works well. Momentum strategies outperform.'),
    (15, 20,  'Mild Unease',  '🟡', 'Normal market noise. Stick to your plan.'),
    (20, 30,  'Elevated Fear','⚠️',  'Widen stops. Reduce position size 20-30%.'),
    (30, 40,  'High Fear',    '🔴', 'Heightened risk. Defensive posture. Mean-reversion setups emerge.'),
    (40, 999, 'Panic',        '🚨', 'Capitulation zone. Best long-term buying opportunities historically.'),
]

# Replace with live VIX value
current_vix = 18.5

print(f'Current VIX: {current_vix}')
print()
for low, high, label, icon, advice in vix_levels:
    active = '← YOU ARE HERE' if low <= current_vix < high else ''
    print(f'{icon} VIX {low}-{high}: {label}  {active}')
    if active:
        print(f'   {advice}')
        print()

# Implied move calculation
import math
days = 1
annual_vol = current_vix / 100
daily_move = annual_vol / math.sqrt(252)
print(f'Implied 1-day move (±): {daily_move:.2%}')
print(f'Implied 1-week move (±): {daily_move * math.sqrt(5):.2%}')
"
```

## Composite Sentiment Score

Combine all signals into a single directional read:

```bash
python3 -c "
def composite_sentiment(fear_greed=50, reddit_buzz=0, headline_bias=0.0, vix=20):
    '''
    fear_greed: 0-100 (0=extreme fear, 100=extreme greed)
    reddit_buzz: -1 to 1 normalized mention trend
    headline_bias: -1 to 1 from headline scorer
    vix: current VIX level
    Returns: score -100 to +100
    '''
    # Contrarian Fear/Greed (buy fear, sell greed)
    fg_signal = (50 - fear_greed) / 50  # low FG = positive signal

    # Direct Reddit/Headline signals
    momentum_signal = (reddit_buzz + headline_bias) / 2

    # VIX risk adjustment
    if vix > 30: vix_multiplier = 1.3  # more weight to contrarian signals
    elif vix > 20: vix_multiplier = 1.0
    else: vix_multiplier = 0.8

    score = (fg_signal * 0.4 + momentum_signal * 0.6) * vix_multiplier * 100

    print('=== Composite Market Sentiment ===')
    print(f'Fear & Greed: {fear_greed}/100  → Signal: {fg_signal:+.2f}')
    print(f'Social Buzz:  {reddit_buzz:+.2f}  Headline: {headline_bias:+.2f}  → {momentum_signal:+.2f}')
    print(f'VIX: {vix}  Multiplier: {vix_multiplier}x')
    print()
    print(f'COMPOSITE SCORE: {score:+.1f} / 100')

    if score > 30:   print('Bias: 📈 BULLISH — lean long on pullbacks')
    elif score < -30: print('Bias: 📉 BEARISH — reduce exposure or hedge')
    else:            print('Bias: ↔️  NEUTRAL — wait for stronger signal')

# Example: extreme fear + bearish headlines + VIX spike
composite_sentiment(fear_greed=22, reddit_buzz=-0.3, headline_bias=-0.4, vix=32)
"
```

## Quick Cheat Sheet

| Signal | Bullish Reading | Bearish Reading |
|--------|----------------|-----------------|
| Fear & Greed | < 25 (extreme fear) | > 75 (extreme greed) |
| Reddit Buzz | Rising ticker mentions | Silence after a pump |
| Headlines | Upgrade, beat, surge | Probe, miss, debt |
| VIX | < 15 (complacent) | > 30 (fear spike) |

> "Be fearful when others are greedy and greedy when others are fearful." — Warren Buffett

## Author

Created by [Ian Alloway](https://github.com/ianalloway) — Data Scientist, sports analytics & fintech.

## License

MIT License
