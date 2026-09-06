"""
web3-ux-feedback / main_tool.py
--------------------------------
Prepares a web3 landing page for AI-powered UX and messaging analysis.

Fetches page metadata, extracts visible text content, and structures
the output for the SKILL.md agent's evaluation pass.

Usage:
    python scripts/main_tool.py --url https://yourproject.xyz
    python scripts/main_tool.py --url https://yourproject.xyz --output json
"""

import argparse
import json
import sys
from helper import score_messaging_gaps, format_action_plan

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


def fetch_page_content(url: str) -> dict:
    """
    Fetches a web3 landing page and extracts key content for analysis.

    Returns a structured dict with:
    - meta: title, description, og tags
    - hero: above-the-fold visible text
    - ctas: all button/link text found
    - features: any feature/benefit section text
    - social_proof: numbers, audit mentions, user counts
    - nav: navigation items
    """
    if not HAS_DEPS:
        return {
            "error": "Missing dependencies. Run: pip install requests beautifulsoup4",
            "url": url,
            "fallback": "Pass the page description directly to the SKILL.md agent."
        }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; web3-ux-feedback-skill/1.0)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e), "url": url}

    soup = BeautifulSoup(response.text, "html.parser")

    # Meta extraction
    meta = {
        "title": soup.title.string.strip() if soup.title else None,
        "description": None,
        "og_title": None,
        "og_description": None,
    }
    for tag in soup.find_all("meta"):
        name = tag.get("name", "").lower()
        prop = tag.get("property", "").lower()
        content = tag.get("content", "")
        if name == "description":
            meta["description"] = content
        elif prop == "og:title":
            meta["og_title"] = content
        elif prop == "og:description":
            meta["og_description"] = content

    # Headings
    headings = {
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(strip=True) for h in soup.find_all("h2")][:8],
        "h3": [h.get_text(strip=True) for h in soup.find_all("h3")][:8],
    }

    # CTAs — buttons and prominent links
    ctas = list(set([
        btn.get_text(strip=True)
        for btn in soup.find_all(["button", "a"])
        if btn.get_text(strip=True) and len(btn.get_text(strip=True)) < 60
    ]))[:20]

    # Navigation items
    nav_items = []
    for nav in soup.find_all("nav"):
        nav_items += [a.get_text(strip=True) for a in nav.find_all("a")]

    # Trust signals — look for audit, TVL, user count mentions
    body_text = soup.get_text(separator=" ", strip=True)
    trust_keywords = [
        "audited", "audit", "certik", "openZeppelin", "trail of bits", "halborn",
        "tvl", "total value locked", "users", "transactions", "secured",
        "non-custodial", "open source", "verified"
    ]
    trust_mentions = [kw for kw in trust_keywords if kw.lower() in body_text.lower()]

    result = {
        "url": url,
        "meta": meta,
        "headings": headings,
        "ctas": ctas,
        "nav_items": nav_items[:10],
        "trust_signals_found": trust_mentions,
        "body_text_preview": body_text[:1500],
        "ready_for_analysis": True,
        "next_step": (
            "Pass this output to the SKILL.md agent with: "
            "'Analyze this web3 landing page for UX and messaging using the "
            "web3-ux-feedback skill.' The agent will apply the 5-part messaging "
            "framework and generate redesign concepts."
        )
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a web3 landing page for UX and messaging analysis."
    )
    parser.add_argument("--url", required=True, help="URL of the web3 landing page")
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    print(f"\n🔍 Fetching: {args.url}\n")
    result = fetch_page_content(args.url)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        if "fallback" in result:
            print(f"💡 {result['fallback']}")
        sys.exit(1)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print("WEB3 UX FEEDBACK — PAGE ANALYSIS")
        print("=" * 60)
        print(f"\n📄 Title: {result['meta']['title']}")
        print(f"📝 Description: {result['meta']['description']}")
        print(f"\n🔤 H1 Headlines:")
        for h in result['headings']['h1']:
            print(f"   → {h}")
        print(f"\n🔤 H2 Subheadlines:")
        for h in result['headings']['h2'][:4]:
            print(f"   → {h}")
        print(f"\n🎯 CTAs Found:")
        for cta in result['ctas'][:10]:
            print(f"   → {cta}")
        print(f"\n🛡️  Trust Signals Detected: {', '.join(result['trust_signals_found']) or 'None found'}")
        print(f"\n✅ {result['next_step']}")
        print("=" * 60)


if __name__ == "__main__":
    main()