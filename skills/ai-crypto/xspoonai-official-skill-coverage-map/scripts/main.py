#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, List, Tuple


# Real category definitions and track mappings
TRACK_CATEGORIES = {
    "ai-productivity": {
        "categories": ["API", "Database", "Email", "Monitoring", "Messaging", "PDF Processing", "Scheduling", "Screenshots", "Storage", "Vector DB"],
        "description": "AI-powered productivity skills for automation and integration"
    },
    "enterprise-skills": {
        "categories": ["API Contracts", "CI/CD", "Code Review", "Documentation", "Incident Management", "Licensing", "Performance", "Refactoring", "Security", "Testing"],
        "description": "Enterprise-grade skills for code quality and DevOps"
    },
    "platform-challenge": {
        "categories": ["CI Integration", "Coverage Analysis", "Documentation", "Example Execution", "Metrics Collection", "PR Preparation", "Linting", "Routing", "Script Testing", "Template Generation"],
        "description": "Platform infrastructure and tooling skills"
    },
    "web3-core-operations": {
        "categories": ["Bridge Operations", "Contract Events", "DAO Governance", "DeFi Execution", "ERC20 Management", "ENS Lookup", "NFT Operations", "NFT Minting", "Solana Tools", "Wallet Operations"],
        "description": "Web3 core operational skills"
    },
    "web3-data-intelligence": {
        "categories": ["DEX Arbitrage", "Gas Monitoring", "Governance Tracking", "Mempool Analysis", "NFT Trading", "Risk Assessment", "Stablecoin Analysis", "Token Liquidity", "Transaction Analysis", "Whale Tracking"],
        "description": "Web3 data analysis and monitoring"
    }
}

# Skill-to-category mapping based on actual implementations
SKILL_MAPPING = {
    "ai-productivity": {
        "api-webhook-signer": ["API"],
        "db-sql-runner": ["Database"],
        "email-ses-sender": ["Email"],
        "logfile-alerts": ["Monitoring", "Email"],
        "messaging-slack-notify": ["Messaging"],
        "pdf-splitter-ocr": ["PDF Processing"],
        "scheduler-cron-json": ["Scheduling"],
        "screenshot-diff": ["Screenshots"],
        "storage-s3-uploader": ["Storage"],
        "vector-notes-indexer": ["Vector DB"]
    },
    "enterprise-skills": {
        "api-contract-diff": ["API Contracts"],
        "ci-pipeline-scaffold": ["CI/CD"],
        "code-review-basics": ["Code Review"],
        "doc-changelog-writer": ["Documentation"],
        "incident-template": ["Incident Management"],
        "license-audit": ["Licensing"],
        "perf-budget-checker": ["Performance"],
        "refactor-plan-writer": ["Refactoring"],
        "security-deps-audit": ["Security"],
        "test-suggestions": ["Testing"]
    },
    "platform-challenge": {
        "skill-ci-checklist": ["CI Integration"],
        "skill-coverage-map": ["Coverage Analysis"],
        "skill-doc-index": ["Documentation"],
        "skill-example-runner": ["Example Execution"],
        "skill-metrics-collector": ["Metrics Collection"],
        "skill-pr-prep": ["PR Preparation"],
        "skill-readme-linter": ["Linting"],
        "skill-router-demo": ["Routing"],
        "skill-scripts-tester": ["Script Testing"],
        "skill-template-generator": ["Template Generation"]
    },
    "web3-core-operations": {
        "bridge-status-checker": ["Bridge Operations"],
        "contract-event-tail": ["Contract Events"],
        "dao-proposal-starter": ["DAO Governance"],
        "defi-quote-exec-demo": ["DeFi Execution"],
        "erc20-allowance-manager": ["ERC20 Management"],
        "identity-ens-lookup": ["ENS Lookup"],
        "nft-metadata-pinner": ["NFT Operations"],
        "nft-minter-basic": ["NFT Minting"],
        "solana-key-tools": ["Solana Tools"],
        "wallet-multisend": ["Wallet Operations"]
    },
    "web3-data-intelligence": {
        "dex-arb-detector": ["DEX Arbitrage"],
        "gas-spike-monitor": ["Gas Monitoring"],
        "governance-vote-tracker": ["Governance Tracking"],
        "mempool-signal-scan": ["Mempool Analysis"],
        "nft-trader-watch": ["NFT Trading"],
        "rugrisk-heuristics": ["Risk Assessment"],
        "stablecoin-flow-map": ["Stablecoin Analysis"],
        "token-liquidity-scan": ["Token Liquidity"],
        "tx-cluster-analyzer": ["Transaction Analysis"],
        "whale-tracker": ["Whale Tracking"]
    }
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def calculate_coverage_metrics(track: str = None) -> Dict[str, Any]:
    """Calculate comprehensive coverage metrics across all tracks or a specific track."""
    
    if track and track not in TRACK_CATEGORIES:
        raise ValueError(f"Unknown track: {track}")
    
    tracks_to_analyze = {track: TRACK_CATEGORIES[track]} if track else TRACK_CATEGORIES
    
    coverage_by_track = {}
    total_coverage = 0
    total_categories = 0
    
    for track_name, track_info in tracks_to_analyze.items():
        categories = track_info["categories"]
        skills_for_track = SKILL_MAPPING.get(track_name, {})
        
        # Map categories to skills
        category_coverage = {}
        total_skills_in_track = 0
        no_skill_categories = []
        
        for category in categories:
            skills_with_category = [
                skill for skill, categories_list in skills_for_track.items()
                if category in categories_list
            ]
            category_coverage[category] = skills_with_category
            total_skills_in_track += len(skills_with_category)
            
            if len(skills_with_category) == 0:
                no_skill_categories.append(category)
        
        # Calculate percentage coverage (categories with at least one skill)
        categories_with_skills = len([c for c in categories if category_coverage[c]])
        track_coverage_pct = (categories_with_skills / len(categories) * 100) if categories else 0
        
        coverage_by_track[track_name] = {
            "description": track_info["description"],
            "total_categories": len(categories),
            "categories_covered": categories_with_skills,
            "coverage_percentage": round(track_coverage_pct, 1),
            "total_skills": len(skills_for_track),
            "skills_assigned": total_skills_in_track,
            "skills_unassigned": len(skills_for_track) - total_skills_in_track,
            "gaps": no_skill_categories,
            "detail": category_coverage
        }
        
        total_coverage += track_coverage_pct
        total_categories += 1
    
    # Calculate recommendations
    recommendations = []
    for track_name, coverage_info in coverage_by_track.items():
        if coverage_info["coverage_percentage"] < 100:
            gaps = coverage_info["gaps"]
            recommendations.append({
                "track": track_name,
                "issue": f"Incomplete coverage ({coverage_info['coverage_percentage']}%)",
                "missing_categories": gaps,
                "suggestion": f"Create skills for: {', '.join(gaps[:3])}{'...' if len(gaps) > 3 else ''}"
            })
        
        if coverage_info["skills_unassigned"] > 0:
            recommendations.append({
                "track": track_name,
                "issue": f"{coverage_info['skills_unassigned']} skill(s) not assigned to categories",
                "suggestion": "Review skill categorization for better organization"
            })
    
    overall_coverage = (total_coverage / total_categories) if total_categories > 0 else 0
    
    return {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "overall_coverage_percentage": round(overall_coverage, 1),
        "tracks_analyzed": len(coverage_by_track),
        "total_categories": sum(len(info["categories"]) for info in TRACK_CATEGORIES.values()) if not track else len(TRACK_CATEGORIES[track]["categories"]),
        "total_skills": sum(len(SKILL_MAPPING.get(t, {})) for t in (SKILL_MAPPING.keys() if not track else [track])),
        "coverage_by_track": coverage_by_track,
        "recommendations": recommendations,
        "status": "excellent" if overall_coverage >= 90 else "good" if overall_coverage >= 70 else "needs_improvement"
    }


def analyze_coverage(skills: List[Dict], categories: List[str]) -> Dict[str, Any]:
    """Analyze skill coverage for custom input."""
    coverage = {cat: [] for cat in categories}
    uncategorized = []
    
    for skill in skills:
        skill_cats = skill.get("categories", [])
        categorized = False
        
        for cat in skill_cats:
            if cat in coverage:
                coverage[cat].append(skill["name"])
                categorized = True
        
        if not categorized:
            uncategorized.append(skill["name"])
    
    gaps = [cat for cat, skills_list in coverage.items() if len(skills_list) == 0]
    
    return {
        "coverage": coverage,
        "gaps": gaps,
        "uncategorized": uncategorized,
        "total_skills": len(skills),
        "coverage_percentage": round((len(categories) - len(gaps)) / len(categories) * 100, 1) if categories else 0
    }


def main():
    parser = argparse.ArgumentParser(description='Map skill coverage across tracks and categories')
    parser.add_argument('--demo', action='store_true', help='Run demo mode (analyze all tracks)')
    parser.add_argument('--track', type=str, help='Analyze specific track coverage')
    parser.add_argument('--params', type=str, help='JSON parameters for custom analysis')
    
    args = parser.parse_args()
    
    try:
        if args.demo or args.track:
            result = calculate_coverage_metrics(track=args.track if args.track else None)
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            skills = params.get("skills", [])
            categories = params.get("categories", [])
            
            analysis = analyze_coverage(skills, categories)
            print(format_success(analysis))
        
        else:
            print(format_error("Either --demo, --track, or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(f"Value error: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
