#!/usr/bin/env python3
"""
DevFun Poker — Tournament S7 Daemon. Continuous loop, no cron gaps.
Adaptive polling: 3s when at a table (20s clock), 8s when in queue.
PID file prevents duplicates. Sends reasoning field for tournament API.

Rebuy Logic:
  - When 402 Payment Required detected, checks wallet balance via Monad RPC
  - If insufficient: ONE notification to Jordan, pauses in waiting_funds loop
  - Polls balance every 30s; auto-rebuys when funds arrive
"""
import json, os, sys, time, urllib.request, urllib.error, signal, random

BASE_URL = "https://arena.dev.fun/api/arena"
COMPETITION_ID = "cmrkmbltp6juswa5d4re81nt2"  # Tournament S7
STATE_FILE = "/root/.arena-poker-state-tournament"
CRED_FILE = "/root/.arena-credentials"
PID_FILE = "/tmp/poker-tournament-s7.pid"

# ─── Monad RPC (for wallet balance checks) ───
MONAD_RPC = "https://monad-testnet.drpc.org"
AGENT_WALLET = "0xd3af4E0FD43253fc0E16Bd65d1b2a78f88e54dB4"

# ─── Adaptive polling ───
TABLE_POLL = 3
QUEUE_POLL = 8
WAIT_FUNDS_POLL = 30  # check wallet balance every 30s when waiting for deposit
DEADLINE_BUFFER = 4

BALANCE_CACHE = {}  # Cache to detect changes
NOTIFIED = {"rebuy_needed": False}  # One-time notification gate


def write_pid():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))


def check_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            try:
                old_pid = int(f.read().strip())
                os.kill(old_pid, 0)
                print(f"Daemon already running (PID {old_pid}). Exiting.", flush=True)
                sys.exit(0)
            except (OSError, ValueError):
                pass
    write_pid()


def cleanup():
    if os.path.exists(PID_FILE):
        os.unlink(PID_FILE)


signal.signal(signal.SIGTERM, lambda *a: (cleanup(), sys.exit(0)))
signal.signal(signal.SIGINT, lambda *a: (cleanup(), sys.exit(0)))


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def api(method, path, body=None):
    try:
        creds = load_json(CRED_FILE)
    except Exception as e:
        return {"error": f"cred file: {e}"}
    key = creds.get("apiKey", "")
    url = f"{BASE_URL}{path}"
    headers = {"x-arena-api-key": key, "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return {"status": resp.status, "body": json.loads(resp.read())}
        except urllib.error.HTTPError as e:
            body_text = e.read().decode()
            try:
                return {"status": e.code, "body": json.loads(body_text)}
            except:
                return {"status": e.code, "body": body_text}
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < 2:
                time.sleep(1)
                continue
            return {"error": f"timeout: {e}"}


def rpc_call(method, params=None):
    """JSON-RPC call to Monad node to check wallet balance."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(MONAD_RPC, data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("result")
    except Exception as e:
        return None


def get_mon_balance():
    """Returns MON balance as float, or None on error."""
    raw = rpc_call("eth_getBalance", [AGENT_WALLET, "latest"])
    if raw and raw.startswith("0x"):
        try:
            return int(raw, 16) / 1e18
        except:
            pass
    return None


def wait_for_rebuy_funds(required_mon, to_address, purpose="rebuy"):
    """
    Wait loop when wallet has insufficient MON for a rebuy.
    Prints ONE notification, then polls balance silently until funded.
    Returns True when balance is sufficient and rebuy succeeded.
    """
    global NOTIFIED

    if not NOTIFIED.get("rebuy_needed"):
        balance = get_mon_balance()
        if balance is None:
            balance = 0
        need = required_mon - balance

        if balance < required_mon:
            print(f"\n⚠️  REBUY NEEDED — Tournament S7", flush=True)
            print(f"   Wallet: {AGENT_WALLET}", flush=True)
            print(f"   Balance: {balance:.2f} MON", flush=True)
            print(f"   Required: {required_mon} MON", flush=True)
            print(f"   Shortfall: ~{need:.0f} MON", flush=True)
            print(f"   Send to: {to_address} (Monad chain)", flush=True)
            print(f"   Daemon pausing — will auto-rebuy once funds arrive.\n", flush=True)
            NOTIFIED["rebuy_needed"] = True

    # Wait loop — poll balance silently, check for increase
    prev_balance = get_mon_balance() or 0
    while True:
        current = get_mon_balance()
        if current is None:
            time.sleep(WAIT_FUNDS_POLL)
            continue

        if current >= required_mon:
            print(f"[S7] Funds detected! Balance: {current:.2f} MON. Rebuking...", flush=True)
            # Try rebuy
            result = api("POST", "/texas/rebuy", {"competitionId": COMPETITION_ID})
            if result.get("status") == 200:
                print("[S7] Rebuy successful! Joining next table.", flush=True)
                NOTIFIED["rebuy_needed"] = False
                # Try joining
                join_result = api("POST", "/texas/join", {"competitionId": COMPETITION_ID})
                return True
            else:
                err = result.get("body", {}).get("error", str(result))
                if "paymentRequirements" in str(result.get("body", {})):
                    # Still needs payment — wait more
                    time.sleep(5)
                    continue
                print(f"[S7] Rebuy failed: {err}. Will retry.", flush=True)
                time.sleep(WAIT_FUNDS_POLL)
                continue

        # Balance didn't change — keep waiting silently
        time.sleep(WAIT_FUNDS_POLL)


# ─── State ───
def load_state():
    try:
        return load_json(STATE_FILE)
    except:
        return {"hands_played": 0, "hands_won": 0, "current_stack": 1000,
                "bankroll": 1000, "chip_state": "available", "biggest_pot": 0,
                "table_id": None, "rank": None, "best_rank": None}


def save_state(s):
    s["last_tick_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_json(STATE_FILE, s)


# ─── Hand evaluator ───
RANKS = "23456789TJQKA"
SUITS = "hdcs"
RANK_IDX = {r: i for i, r in enumerate(RANKS)}


def parse_card(s):
    return (s[0], s[1]) if len(s) == 2 else (s[0], s[1])


def hand_score(hole, board):
    ranks = [RANK_IDX[parse_card(c)[0]] for c in hole + board]
    pairs = set(r for r in ranks if ranks.count(r) >= 2)
    trips = set(r for r in ranks if ranks.count(r) >= 3)
    quads = set(r for r in ranks if ranks.count(r) >= 4)
    suits = [parse_card(c)[1] for c in hole + board]
    is_flush = any(suits.count(s) >= 5 for s in SUITS)
    sorted_ranks = sorted(set(ranks))
    is_straight = False
    if len(sorted_ranks) >= 5:
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                is_straight = True
        if 0 in sorted_ranks and 12 in sorted_ranks:
            is_straight = True
    if quads or (trips and is_flush and is_straight) or (is_flush and is_straight):
        return 4
    if trips or (len(pairs) >= 2 and is_flush):
        return 3
    if len(pairs) >= 2:
        return 2
    if pairs:
        return 2 if list(pairs)[0] >= RANK_IDX.get('J', 9) else 1
    if is_flush or is_straight:
        return 1
    return 0


def preflop_decision(hole, position, pot, stack):
    """LAG strategy — wider ranges, more aggression, fewer folds."""
    if not hole or len(hole) < 2:
        return "fold", 0, ""
    r0 = RANK_IDX.get(parse_card(hole[0])[0])
    r1 = RANK_IDX.get(parse_card(hole[1])[0])
    if r0 is None or r1 is None:
        return "fold", 0, ""
    suited = parse_card(hole[0])[1] == parse_card(hole[1])[1]
    high = max(r0, r1)
    low = min(r0, r1)
    pair = r0 == r1

    if pair and high >= RANK_IDX['T']:
        return "raise", min(stack, max(pot * 4, 40)), f"Premium pair {hole[0]}{hole[1]}, applying pressure."
    if high == RANK_IDX['A'] and low == RANK_IDX['K']:
        return "raise", min(stack, max(pot * 4, 40)), "AK premium, raise to isolate."

    if position <= 2:
        if pair and high >= RANK_IDX['7']:
            return "raise", min(stack, max(pot * 3, 20)), f"Pair {hole[0]}{hole[1]} in EP, raising."
        if high >= RANK_IDX['A'] and low >= RANK_IDX['J']:
            return "raise", min(stack, max(pot * 3, 20)), "AJ+ in EP."
        if suited and high == RANK_IDX['K'] and low >= RANK_IDX['J']:
            return "raise", min(stack, max(pot * 3, 20)), "KJs+ in EP."
        if suited and high == RANK_IDX['Q'] and low == RANK_IDX['J']:
            return "raise", min(stack, max(pot * 3, 20)), "QJs in EP."
        if suited and high == RANK_IDX['J'] and low == RANK_IDX['T']:
            return "raise", min(stack, max(pot * 3, 20)), "JTs in EP."
        if pair:
            return "call", 0, f"Small pair {hole[0]}{hole[1]} in EP."
        if suited and high == RANK_IDX['A']:
            return "call", 0, "Suited ace in EP."
        if suited and high == RANK_IDX['K'] and low >= RANK_IDX['T']:
            return "call", 0, "KTs+ suited in EP."
        if suited and high == RANK_IDX['J'] and low >= RANK_IDX['9']:
            return "call", 0, "J9s+ suited in EP."
        if suited and (high - low) <= 2 and low >= RANK_IDX['5']:
            return "call", 0, f"Suited connector {hole[0]}{hole[1]} in EP."
        return "fold", 0, f"{hole[0]}{hole[1]} UTG — fold."

    if pair:
        return "raise", min(stack, max(pot * 3.5, 24)), f"Pair {hole[0]}{hole[1]} in LP, raising."
    if high == RANK_IDX['A']:
        if low >= RANK_IDX['8'] or suited:
            return "raise", min(stack, max(pot * 3, 20)), f"A{hole[1]} in LP, raising."
        return "call", 0, "A2-A7o in LP."
    if high >= RANK_IDX['K'] and low >= RANK_IDX['T']:
        return "raise", min(stack, max(pot * 3, 20)), f"KT+ in LP, raising."
    if high >= RANK_IDX['Q'] and low >= RANK_IDX['J']:
        return "raise", min(stack, max(pot * 3, 20)), "QJ+ in LP."
    if suited and high >= RANK_IDX['J'] and low >= RANK_IDX['9']:
        return "raise", min(stack, max(pot * 3, 20)), f"J9s+ in LP."
    if suited and low >= RANK_IDX['5'] and (high - low) <= 2:
        return "raise", min(stack, max(pot * 3, 20)), f"Suited connector {hole[0]}{hole[1]} in LP."
    if suited:
        return "call", 0, f"Suited {hole[0]}{hole[1]} in LP."
    if high >= RANK_IDX['Q']:
        return "call", 0, f"Qx in LP."
    if high >= RANK_IDX['J'] and low >= RANK_IDX['8']:
        return "call", 0, f"J8+ in LP."
    if high >= RANK_IDX['T'] and low >= RANK_IDX['7']:
        return "call", 0, f"T7+ in LP."

    if position >= 6:
        if high == RANK_IDX['A'] or pair or suited:
            return "call", 0, f"Blind defense {hole[0]}{hole[1]}."
        if high == RANK_IDX['K']:
            return "call", 0, "Kx blind defense."
        if high >= RANK_IDX['Q'] and low >= RANK_IDX['7']:
            return "call", 0, "Q7+ blind defense."
        if high >= RANK_IDX['J'] and low >= RANK_IDX['8']:
            return "call", 0, "J8+ blind defense."
        if high >= RANK_IDX['T'] and low >= RANK_IDX['9']:
            return "call", 0, "T9+ blind defense."
        if (high - low) <= 3 and low >= RANK_IDX['5']:
            return "call", 0, f"Connected {hole[0]}{hole[1]} in blind."
        return "fold", 0, f"{hole[0]}{hole[1]} too weak."
    return "fold", 0, f"{hole[0]}{hole[1]} not playable."


def postflop_decision(score, pot, stack, committed, board):
    if score >= 3:
        return "raise", min(stack, int(pot * 1.2)), "Trips+, potting for max value."
    if score >= 2:
        return "raise", min(stack, max(int(pot * 0.85), 20)), "Two pair+, pot-sized."
    if score >= 1:
        return "raise", min(stack, max(int(pot * 0.7), 12)), "Top pair, betting for value."
    if committed > 0:
        if len(board) <= 3:
            return "raise", min(stack, max(int(pot * 0.6), 12)), "C-bet flop 100%."
        if len(board) == 4:
            return "raise", min(stack, max(int(pot * 0.7), 14)), "Double barrel turn."
        if pot > 40 and random.random() < 0.4:
            return "raise", min(stack, max(int(pot * 0.5), 10)), "River bluff stab."
    return "check", 0, "Nothing on board, checking back."


def safe_action(allowed_actions):
    aa = allowed_actions.get("availableActions", [])
    if "check" in aa:
        return "check", 0, "Deadline tight, checking."
    elif "call" in aa:
        return "call", allowed_actions.get("callChips", 0), "Deadline tight, calling."
    else:
        return "fold", 0, "Deadline tight, folding."


def generate_message(action):
    msgs = {
        "fold": ["Not today.", "You win this one.", "Saving chips.", "This hand smells like a trap."],
        "check": ["Free card?", "Checking with intent.", "Setting the trap."],
        "call": ["Alright, let's dance.", "Priced in.", "Calling because I can."],
        "raise": ["Time to apply pressure.", "Let's find out who's serious.", "Raising for value."],
        "all-in": ["All in. Let's race.", "If you're bluffing, nice one.", "This pot is mine."],
    }
    return random.choice(msgs.get(action, ["Playing my hand."]))


def handle_table(table):
    table_id = table.get("tableId") or table.get("id")
    allowed_actions = table.get("allowedActions", {})
    self_seat = table.get("selfSeatNumber", 0)
    seats = table.get("seats", [])
    our_seat = next((s for s in seats if s.get("seatNumber") == self_seat), {})
    hole = our_seat.get("holeCards", [])
    stack = our_seat.get("stackChips", 0) or 0
    committed = our_seat.get("payoutChips", 0) or 0
    board = table.get("boardCards", [])
    pot = table.get("potChips", 0) or 0
    deadline = table.get("actionDeadlineAt", 0)
    position = min(self_seat - 1, 7) if self_seat else 0
    street = table.get("street", "Preflop").lower()

    now_ms = time.time() * 1000
    if deadline > 1e15:
        deadline_ok = deadline > now_ms + DEADLINE_BUFFER * 1000
    elif deadline > 1e9:
        deadline_ok = deadline > time.time() + DEADLINE_BUFFER
    else:
        deadline_ok = True

    if not deadline_ok:
        action, amount, reasoning = safe_action(allowed_actions)
    elif street == "preflop":
        action, amount, reasoning = preflop_decision(hole, position, pot, stack)
    else:
        score = hand_score(hole, board)
        action, amount, reasoning = postflop_decision(score, pot, stack, committed, board)

    available = allowed_actions.get("availableActions", [])
    if action not in available:
        action = available[0] if available else "fold"

    body = {
        "tableId": table_id,
        "competitionId": COMPETITION_ID,
        "action": action,
        "reasoning": reasoning,
        "message": generate_message(action),
    }
    if action == "raise":
        rr = allowed_actions.get("raiseRange", {})
        min_amt = rr.get("min", allowed_actions.get("minRaiseTo", 0))
        max_amt = rr.get("max", allowed_actions.get("maxCommit", stack))
        body["amount"] = max(min_amt, min(amount, max_amt))

    return api("POST", "/texas/action", body)


def main_loop():
    check_pid()
    state = load_state()
    print(f"[S7 Daemon] Started. PID {os.getpid()}. Wallet: {AGENT_WALLET}", flush=True)

    while True:
        try:
            result = api("GET", f"/texas/pending-actions?competitionId={COMPETITION_ID}")
            if "error" in result:
                time.sleep(QUEUE_POLL)
                continue

            body = result.get("body", {})
            tables = body.get("tables", [])
            participant = body.get("participant", {})

            if participant:
                state["hands_played"] = participant.get("totalHands", state.get("hands_played", 0))
                state["hands_won"] = participant.get("handsWon", state.get("hands_won", 0))
                state["current_stack"] = participant.get("tableChips", state.get("current_stack", 0))
                state["bankroll"] = participant.get("bankrollChips", state.get("bankroll", 0))
                state["chip_state"] = participant.get("chipState", state.get("chip_state", "available"))
                save_state(state)

            if tables:
                for t in tables:
                    if t.get("actingSeatNumber") == t.get("selfSeatNumber"):
                        handle_table(t)
                        time.sleep(1)
                time.sleep(TABLE_POLL)
                continue

            lobby = body.get("lobby")
            chip_state = state.get("chip_state", "available")

            if chip_state == "busted" or (lobby is None and state.get("current_stack", 0) == 0
                                          and state.get("bankroll", 0) < 10):
                # Busted or minimal chips — try rebuy
                if state.get("chip_state") != "busted":
                    state["chip_state"] = "busted"
                    save_state(state)

                rebuy_result = api("POST", "/texas/rebuy", {"competitionId": COMPETITION_ID})
                rbody = rebuy_result.get("body", {}) if isinstance(rebuy_result, dict) else {}

                if "paymentRequirements" in rbody:
                    req = rbody["paymentRequirements"]
                    to_addr = req.get("to", "0xa0af9ED64C8fe5d00ce879BADD40e94b47dB2542")
                    amount_mon = int(req.get("amount", "250"))
                    wait_for_rebuy_funds(amount_mon, to_addr)
                    # After wait_for_rebuy_funds returns, rebuy succeeded — continue loop
                    continue

                elif rebuy_result.get("status") == 200 or (isinstance(rbody, dict) and "participant" in rbody):
                    print("[S7] Rebuy successful! Back in action.", flush=True)
                    state["chip_state"] = "available"
                    NOTIFIED["rebuy_needed"] = False
                    save_state(state)
                    time.sleep(QUEUE_POLL)
                    continue

                # Rebuy failed for other reason — wait and retry
                time.sleep(QUEUE_POLL)
                continue

            elif lobby is None:
                # Not queued, not busted — try to join
                join_result = api("POST", "/texas/join", {"competitionId": COMPETITION_ID})
                jbody = join_result.get("body", {}) if isinstance(join_result, dict) else {}

                if "paymentRequirements" in jbody:
                    req = jbody["paymentRequirements"]
                    to_addr = req.get("to", "0xa0af9ED64C8fe5d00ce879BADD40e94b47dB2542")
                    amount_mon = int(req.get("amount", "250"))
                    wait_for_rebuy_funds(amount_mon, to_addr)
                    continue

                elif "participant" in jbody:
                    p = jbody["participant"]
                    state["chip_state"] = p.get("chipState", state["chip_state"])
                    state["current_stack"] = p.get("tableChips", 0)
                    state["bankroll"] = p.get("bankrollChips", 0)
                    save_state(state)

            # Queue polling
            time.sleep(QUEUE_POLL)

        except KeyboardInterrupt:
            print("[S7 Daemon] Shutting down.", flush=True)
            break
        except Exception as e:
            print(f"[S7 Daemon] Error: {e}", flush=True)
            time.sleep(QUEUE_POLL)

    cleanup()


if __name__ == "__main__":
    main_loop()
