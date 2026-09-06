#!/usr/bin/env python3
"""
Polymarket Sports Edge — trade odds divergence between sportsbook consensus
and Polymarket sports markets via the Simmer SDK.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta

from simmer_sdk import SimmerClient

# ── Identity ─────────────────────────────────────────────────────────
SKILL_SLUG = "polymarket-sports-edge"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

# ── Configuration (all overridable via env) ──────────────────────────
MIN_DIVERGENCE = float(os.environ.get("MIN_DIVERGENCE", "0.05"))
TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT", "10.0"))
DRY_RUN = os.environ.get("LIVE", "").lower() != "true"
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "30"))

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

# Futures / outrights sport keys (championship winners)
DEFAULT_FUTURES = [
    "basketball_nba_championship_winner",
    "americanfootball_nfl_super_bowl_winner",
    "icehockey_nhl_championship_winner",
    "baseball_mlb_world_series_winner",
]
FUTURES = os.environ.get("FUTURES", "").split(",") if os.environ.get("FUTURES") else DEFAULT_FUTURES

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

# Simmer search queries for futures markets (tuned to actual market question text)
FUTURES_QUERIES = {
    "basketball_nba_championship_winner": ["NBA Finals", "NBA championship"],
    "americanfootball_nfl_super_bowl_winner": ["NFL league championship", "Super Bowl"],
    "icehockey_nhl_championship_winner": ["Stanley Cup", "NHL Stanley Cup"],
    "baseball_mlb_world_series_winner": ["World Series", "MLB World Series"],
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


def simmer_search(query, retries=2):
    """Search Simmer markets with retry on transient errors (502, timeout)."""
    api_key = os.environ["SIMMER_API_KEY"]
    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                "https://api.simmer.markets/api/sdk/markets",
                headers={"Authorization": f"Bearer {api_key}"},
                params={"q": query, "status": "active", "limit": 50},
                timeout=API_TIMEOUT,
            )
            if resp.status_code == 502 and attempt < retries:
                log(f"  Simmer 502 on '{query}', retrying ({attempt + 1}/{retries})...")
                time.sleep(2)
                continue
            resp.raise_for_status()
            markets = resp.json()
            if isinstance(markets, dict):
                markets = markets.get("markets", markets.get("data", []))
            return markets
        except requests.exceptions.Timeout:
            if attempt < retries:
                log(f"  Simmer timeout on '{query}', retrying ({attempt + 1}/{retries})...")
                time.sleep(2)
                continue
            raise
    return []


# ── Odds API helpers ────────────────────────────────────────────────
def is_outright_sport(sport_key):
    """Check if a sport key is for outrights/futures (ends with _winner)."""
    return sport_key.endswith("_winner")


def fetch_odds(sport_key):
    """Fetch upcoming/live odds from The Odds API for a given sport."""
    api_key = os.environ["THE_ODDS_API_KEY"]
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    market_type = "outrights" if is_outright_sport(sport_key) else "h2h"
    params = {
        "apiKey": api_key,
        "regions": "us",
        "markets": market_type,
        "oddsFormat": "decimal",
    }
    resp = requests.get(url, params=params, timeout=API_TIMEOUT)
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


def consensus_prob_outright(events, team_name):
    """Average implied probability across all bookmakers for a team in outrights markets."""
    probs = []
    team_lower = team_name.lower()
    for event in events:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] != "outrights":
                    continue
                for outcome in market["outcomes"]:
                    if outcome["name"].lower() == team_lower:
                        decimal_odds = outcome["price"]
                        if decimal_odds > 0:
                            probs.append(1.0 / decimal_odds)
    return sum(probs) / len(probs) if probs else None


def get_outright_teams(events):
    """Extract all unique team/player names from outrights events."""
    teams = set()
    for event in events:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] != "outrights":
                    continue
                for outcome in market["outcomes"]:
                    teams.add(outcome["name"])
    return teams


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

    # 2. Get Simmer markets for this sport
    try:
        markets = simmer_search(label)
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

        divergence = round(book_prob - market_price, 4)

        log(
            f"  Matched: \"{question[:60]}\" → {yes_team} vs {no_team}\n"
            f"    Polymarket YES: {market_price:.3f} | Books: {book_prob:.3f} | "
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


def match_market_to_outright(market_question, outright_teams):
    """
    Match a Simmer futures market question to a team from outrights data.
    Returns the matched team name or None.
    """
    q = normalize(market_question)
    best_team = None
    best_score = 0

    for team in outright_teams:
        tokens = team_tokens(team)
        hits = sum(1 for t in tokens if t in q and len(t) > 2)
        if hits >= 1 and hits > best_score:
            best_score = hits
            best_team = team

    return best_team


def scan_futures(sport_key):
    """Scan futures/outrights markets for divergence. Returns list of trades."""
    queries = FUTURES_QUERIES.get(sport_key, [sport_key])
    label = queries[0]
    log(f"Futures {label}: Fetching outrights...")

    # 1. Get outrights from Odds API
    try:
        events = fetch_odds(sport_key)
    except Exception as e:
        log(f"Futures {label}: Odds API error — {e}")
        return []

    if not events:
        log(f"Futures {label}: No outrights available.")
        return []

    outright_teams = get_outright_teams(events)
    log(f"Futures {label}: Found {len(outright_teams)} teams in outrights")

    # 2. Search Simmer for futures markets using multiple queries
    seen_ids = set()
    all_markets = []
    for query in queries:
        try:
            markets = simmer_search(query)
            for m in markets:
                mid = m.get("id", "")
                if mid and mid not in seen_ids:
                    seen_ids.add(mid)
                    all_markets.append(m)
        except Exception as e:
            log(f"Futures {label}: Simmer search '{query}' error — {e}")

    if not all_markets:
        log(f"Futures {label}: No active markets on Simmer.")
        return []

    log(f"Futures {label}: Found {len(all_markets)} Simmer markets to check")

    # 3. Match and compare
    trades = []
    for market in all_markets:
        question = market.get("question", "")
        market_id = market.get("id", "")
        market_price = market.get("current_probability") or market.get("external_price_yes")

        if market_price is None:
            continue

        # For futures, we WANT markets with futures keywords
        team = match_market_to_outright(question, outright_teams)
        if team is None:
            continue

        book_prob = consensus_prob_outright(events, team)
        if book_prob is None:
            continue

        divergence = round(book_prob - market_price, 4)

        log(
            f"  Matched: \"{question[:60]}\" → {team}\n"
            f"    Polymarket YES: {market_price:.3f} | Books: {book_prob:.3f} | "
            f"Divergence: {divergence:+.2f}"
        )

        if divergence >= MIN_DIVERGENCE:
            trades.append(
                execute_trade(market_id, "yes", market_price, book_prob, divergence, question, team)
            )
        elif divergence <= -MIN_DIVERGENCE:
            no_price = 1.0 - market_price
            no_book = 1.0 - book_prob
            trades.append(
                execute_trade(market_id, "no", no_price, no_book, -divergence, question, team)
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
    log(f"Scanning {len(SPORTS)} sports + {len(FUTURES)} futures... (dry_run={DRY_RUN}, min_divergence={MIN_DIVERGENCE:.0%})")

    all_trades = []

    # Game-level h2h scanning
    for sport_key in SPORTS:
        trades = scan_sport(sport_key)
        all_trades.extend(trades)

    # Futures/outrights scanning
    for sport_key in FUTURES:
        trades = scan_futures(sport_key)
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
