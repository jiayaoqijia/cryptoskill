"""Quick test — fetch live odds from The Odds API and print consensus probabilities."""

import os
import requests

api_key = os.environ["THE_ODDS_API_KEY"]
sports = [
    "basketball_nba",
    "icehockey_nhl",
    "americanfootball_nfl",
    "baseball_mlb",
    "mma_mixed_martial_arts",
]

for sport in sports:
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"
    resp = requests.get(
        url,
        params={"apiKey": api_key, "regions": "us", "markets": "h2h", "oddsFormat": "decimal"},
        timeout=15,
    )
    if resp.status_code == 422:
        print(f"{sport}: not in season")
        continue
    if resp.status_code != 200:
        print(f"{sport}: error {resp.status_code}")
        continue
    games = resp.json()
    print(f"\n{sport}: {len(games)} games")
    for g in games[:3]:
        home = g["home_team"]
        away = g["away_team"]
        start = g.get("commence_time", "?")
        probs = []
        for bk in g.get("bookmakers", []):
            for mkt in bk.get("markets", []):
                if mkt["key"] != "h2h":
                    continue
                for out in mkt["outcomes"]:
                    if out["name"] == home:
                        probs.append(1.0 / out["price"])
        avg = sum(probs) / len(probs) if probs else 0
        print(f"  {away} @ {home} | {start} | {home} consensus: {avg:.1%} ({len(probs)} books)")

remaining = resp.headers.get("x-requests-remaining", "?")
used = resp.headers.get("x-requests-used", "?")
print(f"\nAPI credits: {used} used, {remaining} remaining")
