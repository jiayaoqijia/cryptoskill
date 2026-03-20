#!/usr/bin/env python3
"""
Polymarket Sports Edge — trade odds divergence between sportsbook consensus
and Polymarket sports markets via the Simmer SDK.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta

from simmer_sdk import SimmerClient

# ── Identity ─────────────────────────────────────────────────────────
SKILL_SLUG = "polymarket-sports-edge"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

# ── Configuration (all overridable via env) ──────────────────────────
MIN_DIVERGENCE = float(os.environ.get("MIN_DIVERGENCE", "0.08"))
TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT", "10.0"))
DRY_RUN = os.environ.get("LIVE", "").lower() != "true"

DEFAULT_SPORTS = [
    "basketball_nba",
    "americanfootball_nfl",
    "icehockey_nhl",
    "baseball_mlb",
    "mma_mixed_martial_arts",
    "soccer_epl",
    "soccer_usa_mls",
]
SPORTS = os.environ.get("SPORTS", "").split(",") if os.environ.get("SPORTS") else DEFAULT_SPORTS

# Search terms to find sports markets on Simmer
SPORT_QUERIES = {
    "basketball_nba": "NBA",
    "americanfootball_nfl": "NFL",
    "icehockey_nhl": "NHL",
    "baseball_mlb": "MLB",
    "mma_mixed_martial_arts": "UFC",
    "soccer_epl": "Premier League",
    "soccer_usa_mls": "MLS",
}

# ── Simmer client (lazy singleton) ──────────────────────────────────
_client = None

def get_client():
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue="polymarket",
        )
    return _client


# ── Odds API helpers ────────────────────────────────────────────────
def fetch_odds(sport_key):
    """Fetch upcoming/live odds from The Odds API for a given sport."""
    api_key = os.environ["THE_ODDS_API_KEY"]
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        "apiKey": api_key,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }
    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code == 422:
        # Sport not currently in season
        return []
    resp.raise_for_status()
    return resp.json()


def consensus_prob(game, team_name):
    """Average implied probability across all bookmakers for a team in a h2h market."""
    probs = []
    for bookmaker in game.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market["key"] != "h2h":
                continue
            for outcome in market["outcomes"]:
                if outcome["name"].lower() == team_name.lower():
                    decimal_odds = outcome["price"]
                    if decimal_odds > 0:
                        probs.append(1.0 / decimal_odds)
    return sum(probs) / len(probs) if probs else None


# ── Matching ────────────────────────────────────────────────────────
def normalize(name):
    """Lowercase and strip punctuation for fuzzy matching."""
    return name.lower().replace(".", "").replace("'", "").strip()


def team_tokens(name):
    """Split a team name into matchable tokens."""
    return set(normalize(name).split())


FUTURES_KEYWORDS = {"finish", "winner", "champion", "win the", "mvp", "relegat", "promot", "place in"}


def is_futures_market(question):
    """Detect season-long futures markets that shouldn't match individual games."""
    q = question.lower()
    return any(kw in q for kw in FUTURES_KEYWORDS)


def match_market_to_game(market_question, games):
    """
    Find the best-matching game for a Simmer market question.
    Skips futures/season markets. Returns (game, home_team, away_team) or (None, None, None).
    """
    if is_futures_market(market_question):
        return None, None, None

    q = normalize(market_question)
    best_game = None
    best_home = None
    best_away = None
    best_score = 0

    for game in games:
        home = game.get("home_team", "")
        away = game.get("away_team", "")
        home_toks = team_tokens(home)
        away_toks = team_tokens(away)

        # Count how many team-name tokens appear in the question
        home_hits = sum(1 for t in home_toks if t in q and len(t) > 2)
        away_hits = sum(1 for t in away_toks if t in q and len(t) > 2)

        # Require at least one meaningful token from each team
        if home_hits >= 1 and away_hits >= 1:
            score = home_hits + away_hits
            if score > best_score:
                best_score = score
                best_game = game
                best_home = home
                best_away = away

    return best_game, best_home, best_away


# ── Core logic ──────────────────────────────────────────────────────
def scan_sport(sport_key):
    """Scan one sport for divergence opportunities. Returns list of trades made."""
    client = get_client()
    label = SPORT_QUERIES.get(sport_key, sport_key)
    log(f"{label}: Fetching odds...")

    # 1. Get sportsbook odds
    try:
        games = fetch_odds(sport_key)
    except Exception as e:
        log(f"{label}: Odds API error — {e}")
        return []

    if not games:
        log(f"{label}: No games with odds right now.")
        return []

    log(f"{label}: Found {len(games)} games with odds")

    # 2. Get Simmer markets for this sport via REST (SDK doesn't support text search)
    try:
        api_key = os.environ["SIMMER_API_KEY"]
        resp = requests.get(
            "https://api.simmer.markets/api/sdk/markets",
            headers={"Authorization": f"Bearer {api_key}"},
            params={"q": label, "status": "active", "limit": 50},
            timeout=15,
        )
        resp.raise_for_status()
        markets = resp.json()
        if isinstance(markets, dict):
            markets = markets.get("markets", markets.get("data", []))
    except Exception as e:
        log(f"{label}: Simmer API error — {e}")
        return []

    if not markets:
        log(f"{label}: No active markets on Simmer.")
        return []

    # 3. Match and compare
    trades = []
    for market in markets:
        question = market.get("question", "")
        market_id = market.get("id", "")
        market_price = market.get("current_probability") or market.get("external_price_yes")

        if market_price is None:
            continue

        game, home, away = match_market_to_game(question, games)
        if game is None:
            continue

        # Determine which team the market is about (the YES side)
        # Typically "Will X win?" → YES = X wins
        q_lower = normalize(question)
        home_lower = normalize(home)
        away_lower = normalize(away)

        # Figure out which team YES refers to
        yes_team = None
        no_team = None

        # Heuristic: the first team mentioned in "Will X beat Y" is the YES side
        home_pos = q_lower.find(normalize(home.split()[-1]))
        away_pos = q_lower.find(normalize(away.split()[-1]))

        if home_pos >= 0 and away_pos >= 0:
            if home_pos < away_pos:
                yes_team, no_team = home, away
            else:
                yes_team, no_team = away, home
        elif home_pos >= 0:
            yes_team, no_team = home, away
        elif away_pos >= 0:
            yes_team, no_team = away, home
        else:
            continue

        # Get consensus probability for the YES team
        book_prob = consensus_prob(game, yes_team)
        if book_prob is None:
            continue

        divergence = book_prob - market_price

        log(
            f"  Matched: \"{question[:60]}\" → {yes_team} vs {no_team}\n"
            f"    Polymarket YES: {market_price:.2f} | Books: {book_prob:.2f} | "
            f"Divergence: {divergence:+.2f}"
        )

        # Check both sides for edge
        if divergence >= MIN_DIVERGENCE:
            # YES is underpriced on Polymarket
            trades.append(
                execute_trade(market_id, "yes", market_price, book_prob, divergence, question, yes_team)
            )
        elif divergence <= -MIN_DIVERGENCE:
            # NO is underpriced (YES is overpriced)
            no_price = 1.0 - market_price
            no_book = 1.0 - book_prob
            trades.append(
                execute_trade(market_id, "no", no_price, no_book, -divergence, question, no_team)
            )

    return trades


def execute_trade(market_id, side, market_price, book_prob, edge, question, team):
    """Place a trade (or dry-run log it)."""
    client = get_client()
    reasoning = (
        f"Sportsbook consensus {book_prob:.0%} vs Polymarket {market_price:.0%} for {team}. "
        f"Edge: {edge:.0%}. Buying {side.upper()}."
    )

    if DRY_RUN:
        log(f"  DRY RUN: Would buy {side.upper()} at {market_price:.2f} (edge {edge:.0%}) — {TRADE_AMOUNT}")
        return {"market_id": market_id, "side": side, "edge": edge, "dry_run": True}

    try:
        result = client.trade(
            market_id=market_id,
            side=side,
            amount=TRADE_AMOUNT,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
        )
        if result.success if hasattr(result, "success") else result.get("success"):
            log(f"  TRADE: Bought {side.upper()} at {market_price:.2f} (edge {edge:.0%}) — {TRADE_AMOUNT}")
        else:
            error = result.error if hasattr(result, "error") else result.get("error", "unknown")
            log(f"  TRADE FAILED: {error}")
        return result
    except Exception as e:
        log(f"  TRADE ERROR: {e}")
        return {"error": str(e)}


# ── Utilities ───────────────────────────────────────────────────────
def log(msg):
    print(f"[Sports Edge] {msg}")


def main():
    log(f"Scanning {len(SPORTS)} sports... (dry_run={DRY_RUN}, min_divergence={MIN_DIVERGENCE:.0%})")

    all_trades = []
    for sport_key in SPORTS:
        trades = scan_sport(sport_key)
        all_trades.extend(trades)

    executed = [t for t in all_trades if not (isinstance(t, dict) and t.get("dry_run"))]
    dry = [t for t in all_trades if isinstance(t, dict) and t.get("dry_run")]

    if DRY_RUN:
        log(f"Done. {len(dry)} opportunities found (dry run).")
    else:
        log(f"Done. {len(executed)} trades executed.")

    if not all_trades:
        log("No divergence above threshold this cycle.")


if __name__ == "__main__":
    main()
