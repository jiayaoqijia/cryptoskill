"""
web3-ux-feedback / helper.py
------------------------------
Scoring utilities and output formatters for the web3-ux-feedback skill.

Functions:
    score_messaging_gaps()   — evaluates 5-part framework coverage
    format_action_plan()     — generates a prioritized action plan table
    detect_antipatterns()    — flags common web3 messaging mistakes
"""

from typing import Optional


# ─── Messaging Gap Scoring ────────────────────────────────────────────────────

FRAMEWORK_PARTS = [
    "market_context",
    "icp",
    "competitive_alternatives",
    "product_capabilities",
    "value_proposition",
]

STATUS_SCORES = {
    "missing": 0,
    "weak": 1,
    "present": 2,
    "strong": 3,
}


def score_messaging_gaps(evaluation: dict) -> dict:
    """
    Takes a dict of framework part statuses and returns a scored summary.

    Args:
        evaluation: {
            "market_context": "missing" | "weak" | "present" | "strong",
            "icp": "...",
            "competitive_alternatives": "...",
            "product_capabilities": "...",
            "value_proposition": "...",
        }

    Returns:
        {
            "total_score": int (0–15),
            "percentage": float,
            "grade": str,
            "weakest_parts": list[str],
            "summary": str,
        }
    """
    scores = {}
    for part in FRAMEWORK_PARTS:
        status = evaluation.get(part, "missing").lower()
        scores[part] = STATUS_SCORES.get(status, 0)

    total = sum(scores.values())
    max_score = len(FRAMEWORK_PARTS) * 3
    percentage = round((total / max_score) * 100, 1)

    if percentage >= 80:
        grade = "Strong"
    elif percentage >= 60:
        grade = "Solid — some gaps to close"
    elif percentage >= 40:
        grade = "Weak — significant messaging gaps"
    else:
        grade = "Critical — messaging needs rebuilding"

    weakest = sorted(
        [p for p in FRAMEWORK_PARTS if scores[p] <= 1],
        key=lambda p: scores[p]
    )

    return {
        "total_score": total,
        "max_score": max_score,
        "percentage": percentage,
        "grade": grade,
        "part_scores": scores,
        "weakest_parts": weakest,
        "summary": f"Messaging score: {total}/{max_score} ({percentage}%) — {grade}",
    }


# ─── Action Plan Formatter ────────────────────────────────────────────────────

def format_action_plan(actions: list[dict]) -> str:
    """
    Formats a list of action dicts into a markdown priority table.

    Args:
        actions: list of {
            "action": str,
            "impact": "High" | "Medium" | "Low",
            "effort": "High" | "Medium" | "Low",
            "when": str  (e.g., "This week", "Next sprint")
        }

    Returns:
        Markdown table string
    """
    # Sort: High impact first, then Low effort first
    impact_order = {"High": 0, "Medium": 1, "Low": 2}
    effort_order = {"Low": 0, "Medium": 1, "High": 2}

    sorted_actions = sorted(
        actions,
        key=lambda a: (impact_order.get(a["impact"], 2), effort_order.get(a["effort"], 2))
    )

    lines = [
        "| Priority | Action | Impact | Effort | When |",
        "|----------|--------|--------|--------|------|",
    ]
    for i, action in enumerate(sorted_actions, 1):
        lines.append(
            f"| {i} | {action['action']} | {action['impact']} | {action['effort']} | {action['when']} |"
        )

    return "\n".join(lines)


# ─── Anti-pattern Detector ────────────────────────────────────────────────────

ANTIPATTERNS = {
    "future_of_x": {
        "triggers": ["future of", "next generation of", "revolutionizing"],
        "message": "Generic 'future of X' claim — replace with a specific outcome",
        "priority": "High",
    },
    "connect_wallet_only_cta": {
        "triggers": ["connect wallet"],
        "message": "Only CTA is 'Connect Wallet' — add value-oriented primary CTAs",
        "priority": "High",
    },
    "jargon_wall": {
        "triggers": ["amm", "lp token", "liquidity pool", "yield farming", "tvl"],
        "message": "Unexplained DeFi jargon — add tooltips or plain-language versions",
        "priority": "Medium",
    },
    "vague_security": {
        "triggers": ["secure protocol", "security first", "safe and secure"],
        "message": "Vague security claim without proof — add audit badge + link",
        "priority": "High",
    },
    "broad_icp": {
        "triggers": ["for everyone", "for all users", "for anyone", "for crypto users"],
        "message": "No specific ICP in headline — target one user type explicitly",
        "priority": "High",
    },
    "no_quantification": {
        "triggers": ["low fees", "fast transactions", "high performance"],
        "message": "Unquantified benefit claim — add a specific number",
        "priority": "Medium",
    },
}


def detect_antipatterns(text: str) -> list[dict]:
    """
    Scans landing page text for common web3 messaging anti-patterns.

    Args:
        text: raw text content from the landing page

    Returns:
        list of detected anti-pattern dicts with message and priority
    """
    text_lower = text.lower()
    detected = []

    for pattern_id, pattern in ANTIPATTERNS.items():
        for trigger in pattern["triggers"]:
            if trigger.lower() in text_lower:
                detected.append({
                    "pattern": pattern_id,
                    "trigger_found": trigger,
                    "message": pattern["message"],
                    "priority": pattern["priority"],
                })
                break  # Only flag once per pattern

    return detected


# ─── Quick Usage Example ──────────────────────────────────────────────────────

if __name__ == "__main__":
    # Example: score a messaging evaluation
    sample_evaluation = {
        "market_context": "missing",
        "icp": "weak",
        "competitive_alternatives": "missing",
        "product_capabilities": "weak",
        "value_proposition": "present",
    }
    result = score_messaging_gaps(sample_evaluation)
    print(result["summary"])
    print(f"Weakest parts to fix first: {result['weakest_parts']}")

    # Example: format an action plan
    sample_actions = [
        {"action": "Add audit badge to hero section", "impact": "High", "effort": "Low", "when": "This week"},
        {"action": "Replace generic headline", "impact": "High", "effort": "Low", "when": "This week"},
        {"action": "Add secondary CTA", "impact": "High", "effort": "Low", "when": "This week"},
        {"action": "Rewrite features with benefits ladder", "impact": "High", "effort": "Medium", "when": "Next sprint"},
        {"action": "Add demo video to hero", "impact": "Medium", "effort": "High", "when": "Next month"},
    ]
    print("\n" + format_action_plan(sample_actions))