#!/usr/bin/env python3
import json
import argparse
import sys
import os
import re
from typing import Dict, Any, List, Tuple


# Real skill documentation metadata
SKILL_DOCUMENTATION = {
    "ai-productivity": {
        "api-webhook-signer": {
            "title": "API Webhook Signer",
            "description": "Generate and validate HMAC signatures for webhook requests",
            "keywords": ["webhook", "signature", "HMAC", "security", "API", "authentication"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Verify webhook authenticity", "Sign outgoing requests", "Secure integrations"]
        },
        "db-sql-runner": {
            "title": "Database SQL Runner",
            "description": "Execute SQL queries against database connections",
            "keywords": ["database", "SQL", "query", "execution", "DB", "relational"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Run queries", "Execute migrations", "Database automation"]
        },
        "email-ses-sender": {
            "title": "Email SES Sender",
            "description": "Send emails using AWS SES",
            "keywords": ["email", "SES", "AWS", "messaging", "notification"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Send notifications", "Email campaigns", "Transactional emails"]
        },
        "logfile-alerts": {
            "title": "Logfile Alerts",
            "description": "Monitor log files and trigger alerts on patterns",
            "keywords": ["logging", "monitoring", "alerts", "patterns", "automation"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Error detection", "Log monitoring", "Automated alerting"]
        },
        "messaging-slack-notify": {
            "title": "Messaging Slack Notifier",
            "description": "Send notifications to Slack channels",
            "keywords": ["Slack", "messaging", "notifications", "integration", "channels"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Team notifications", "Alert routing", "Event notifications"]
        },
        "pdf-splitter-ocr": {
            "title": "PDF Splitter OCR",
            "description": "Split PDF documents and extract text with OCR",
            "keywords": ["PDF", "OCR", "document processing", "text extraction"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Document processing", "Text extraction", "PDF manipulation"]
        },
        "scheduler-cron-json": {
            "title": "Scheduler Cron JSON",
            "description": "Schedule tasks using cron expressions in JSON",
            "keywords": ["scheduling", "cron", "automation", "tasks", "timing"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Task scheduling", "Automation", "Recurring jobs"]
        },
        "screenshot-diff": {
            "title": "Screenshot Diff Checker",
            "description": "Compare screenshots and detect visual differences",
            "keywords": ["screenshot", "comparison", "visual testing", "diff"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Visual regression testing", "UI comparison", "Quality assurance"]
        },
        "storage-s3-uploader": {
            "title": "Storage S3 Uploader",
            "description": "Upload files to AWS S3 storage",
            "keywords": ["S3", "storage", "AWS", "file upload", "cloud"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["File storage", "Cloud backup", "Content delivery"]
        },
        "vector-notes-indexer": {
            "title": "Vector Notes Indexer",
            "description": "Index notes and documents as vectors for semantic search",
            "keywords": ["vector", "indexing", "search", "embeddings", "semantic"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Full-text search", "Semantic search", "Knowledge management"]
        }
    },
    "enterprise-skills": {
        "api-contract-diff": {
            "title": "API Contract Diff",
            "description": "Detect breaking changes in API contracts and specifications",
            "keywords": ["API", "contract", "diff", "OpenAPI", "breaking changes"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["API validation", "Contract testing", "Change detection"]
        },
        "ci-pipeline-scaffold": {
            "title": "CI Pipeline Scaffold",
            "description": "Generate CI/CD pipeline configurations",
            "keywords": ["CI", "pipeline", "automation", "deployment", "DevOps"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Pipeline setup", "CI configuration", "DevOps automation"]
        },
        "code-review-basics": {
            "title": "Code Review Basics",
            "description": "Provide code review guidelines and checks",
            "keywords": ["code review", "quality", "standards", "guidelines"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Code review", "Quality standards", "Team guidelines"]
        },
        "doc-changelog-writer": {
            "title": "Documentation Changelog Writer",
            "description": "Generate changelog documentation from commits",
            "keywords": ["documentation", "changelog", "git", "commits", "releases"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Release notes", "Change history", "Documentation"]
        },
        "incident-template": {
            "title": "Incident Template",
            "description": "Create structured incident reports with timeline tracking",
            "keywords": ["incident", "template", "SLA", "timeline", "management"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Incident management", "Post-mortems", "Documentation"]
        },
        "license-audit": {
            "title": "License Audit",
            "description": "Audit dependencies for license compliance",
            "keywords": ["license", "compliance", "audit", "dependencies"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["License compliance", "Dependency audit", "Risk assessment"]
        },
        "perf-budget-checker": {
            "title": "Performance Budget Checker",
            "description": "Monitor application performance against budget thresholds",
            "keywords": ["performance", "budget", "metrics", "monitoring"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Performance monitoring", "Budget enforcement", "Metrics tracking"]
        },
        "refactor-plan-writer": {
            "title": "Refactor Plan Writer",
            "description": "Analyze code and generate refactoring plans",
            "keywords": ["refactoring", "code quality", "debt", "analysis"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Code analysis", "Refactoring planning", "Quality improvement"]
        },
        "security-deps-audit": {
            "title": "Security Dependencies Audit",
            "description": "Audit dependencies for known security vulnerabilities",
            "keywords": ["security", "vulnerability", "CVE", "dependencies", "audit"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Security scanning", "Vulnerability detection", "Compliance"]
        },
        "test-suggestions": {
            "title": "Test Suggestions",
            "description": "Generate test cases and suggestions from code analysis",
            "keywords": ["testing", "test generation", "coverage", "quality"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Test planning", "Coverage improvement", "Test generation"]
        }
    },
    "platform-challenge": {
        "skill-ci-checklist": {
            "title": "Skill CI Checklist",
            "description": "Validate skills against quality gates for CI/CD readiness",
            "keywords": ["CI", "quality", "validation", "checklist", "standards"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Quality assurance", "CI validation", "Pre-merge checks"]
        },
        "skill-coverage-map": {
            "title": "Skill Coverage Map",
            "description": "Map skill coverage across categories and identify gaps",
            "keywords": ["coverage", "mapping", "gaps", "categories", "analysis"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Portfolio planning", "Gap analysis", "Coverage reporting"]
        },
        "skill-doc-index": {
            "title": "Skill Documentation Index",
            "description": "Build searchable index of skill documentation with full-text search",
            "keywords": ["documentation", "index", "search", "semantic", "discovery"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Skill discovery", "Documentation search", "Knowledge base"]
        },
        "skill-example-runner": {
            "title": "Skill Example Runner",
            "description": "Execute and validate skill examples with output capture",
            "keywords": ["examples", "execution", "validation", "testing"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Example testing", "Skill validation", "Documentation verification"]
        },
        "skill-metrics-collector": {
            "title": "Skill Metrics Collector",
            "description": "Collect and aggregate metrics from skill executions",
            "keywords": ["metrics", "collection", "aggregation", "reporting"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Metrics tracking", "Performance reporting", "Usage analytics"]
        },
        "skill-pr-prep": {
            "title": "Skill PR Preparation",
            "description": "Prepare skills for pull requests with validation and checks",
            "keywords": ["PR", "preparation", "validation", "checklist"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Pre-submission checks", "PR preparation", "Quality validation"]
        },
        "skill-readme-linter": {
            "title": "Skill README Linter",
            "description": "Lint and validate README documentation structure",
            "keywords": ["linting", "README", "documentation", "validation"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Documentation quality", "Consistency checks", "Standards enforcement"]
        },
        "skill-router-demo": {
            "title": "Skill Router Demo",
            "description": "Route and execute skill demonstrations with orchestration",
            "keywords": ["routing", "orchestration", "execution", "demo"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Skill execution", "Routing", "Orchestration"]
        },
        "skill-scripts-tester": {
            "title": "Skill Scripts Tester",
            "description": "Test skill scripts for correctness and functionality",
            "keywords": ["testing", "scripts", "validation", "execution"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Script testing", "Validation", "Quality assurance"]
        },
        "skill-template-generator": {
            "title": "Skill Template Generator",
            "description": "Generate boilerplate templates for new skills",
            "keywords": ["templates", "generation", "boilerplate", "scaffolding"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Skill generation", "Bootstrapping", "Template management"]
        }
    },
    "web3-core-operations": {
        "bridge-status-checker": {
            "title": "Bridge Status Checker",
            "description": "Check status and liquidity of cross-chain bridges",
            "keywords": ["bridge", "cross-chain", "liquidity", "status", "web3"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Bridge monitoring", "Liquidity tracking", "Cross-chain operations"]
        },
        "contract-event-tail": {
            "title": "Contract Event Tail",
            "description": "Monitor and tail blockchain contract events in real-time",
            "keywords": ["events", "blockchain", "contracts", "monitoring", "real-time"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Event monitoring", "Real-time tracking", "Contract interaction"]
        },
        "dao-proposal-starter": {
            "title": "DAO Proposal Starter",
            "description": "Create and launch DAO governance proposals",
            "keywords": ["DAO", "governance", "proposals", "voting", "web3"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["DAO governance", "Proposal creation", "Community voting"]
        },
        "defi-quote-exec-demo": {
            "title": "DeFi Quote Executor Demo",
            "description": "Get DeFi quotes and execute swaps",
            "keywords": ["DeFi", "swap", "quote", "execution", "liquidity"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Swap execution", "Price quotes", "DeFi operations"]
        },
        "erc20-allowance-manager": {
            "title": "ERC20 Allowance Manager",
            "description": "Manage ERC20 token approvals and allowances",
            "keywords": ["ERC20", "allowance", "approval", "tokens"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Token management", "Approvals", "Permission handling"]
        },
        "identity-ens-lookup": {
            "title": "Identity ENS Lookup",
            "description": "Look up Ethereum Name Service identities and addresses",
            "keywords": ["ENS", "identity", "address", "lookup", "Ethereum"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Address resolution", "ENS lookups", "Identity management"]
        },
        "nft-metadata-pinner": {
            "title": "NFT Metadata Pinner",
            "description": "Pin NFT metadata to IPFS for persistence",
            "keywords": ["NFT", "metadata", "IPFS", "pinning", "persistence"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Metadata management", "IPFS pinning", "NFT operations"]
        },
        "nft-minter-basic": {
            "title": "NFT Minter Basic",
            "description": "Mint NFTs on supported blockchains",
            "keywords": ["NFT", "minting", "ERC721", "blockchain"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["NFT creation", "Minting", "Token generation"]
        },
        "solana-key-tools": {
            "title": "Solana Key Tools",
            "description": "Manage Solana keypairs and wallet operations",
            "keywords": ["Solana", "keys", "wallet", "keypair", "management"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Key management", "Wallet operations", "Solana accounts"]
        },
        "wallet-multisend": {
            "title": "Wallet Multisend",
            "description": "Send transactions to multiple addresses in batch",
            "keywords": ["wallet", "multisend", "batch", "transactions"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Batch transfers", "Distribution", "Multi-recipient payments"]
        }
    },
    "web3-data-intelligence": {
        "dex-arb-detector": {
            "title": "DEX Arbitrage Detector",
            "description": "Detect arbitrage opportunities across DEX protocols",
            "keywords": ["arbitrage", "DEX", "opportunity", "detection"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Arbitrage detection", "Opportunity finding", "Trading analysis"]
        },
        "gas-spike-monitor": {
            "title": "Gas Spike Monitor",
            "description": "Monitor gas prices and detect spikes in real-time",
            "keywords": ["gas", "monitoring", "spikes", "Ethereum", "pricing"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Gas monitoring", "Price tracking", "Transaction optimization"]
        },
        "governance-vote-tracker": {
            "title": "Governance Vote Tracker",
            "description": "Track governance votes and proposal outcomes",
            "keywords": ["governance", "voting", "tracking", "proposals"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Vote tracking", "Governance monitoring", "Administration"]
        },
        "mempool-signal-scan": {
            "title": "Mempool Signal Scanner",
            "description": "Scan mempool for signals and pending transactions",
            "keywords": ["mempool", "signals", "transactions", "scanning"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Front-running detection", "Opportunity scanning", "Transaction analysis"]
        },
        "nft-trader-watch": {
            "title": "NFT Trader Watch",
            "description": "Monitor NFT trading activity and market movements",
            "keywords": ["NFT", "trading", "monitoring", "markets"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Market monitoring", "Trading alerts", "Portfolio tracking"]
        },
        "rugrisk-heuristics": {
            "title": "Rug Risk Heuristics",
            "description": "Analyze tokens for rug pull risk indicators",
            "keywords": ["risk", "rug pull", "analysis", "heuristics"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Risk assessment", "Token analysis", "Safety evaluation"]
        },
        "stablecoin-flow-map": {
            "title": "Stablecoin Flow Map",
            "description": "Map stablecoin flows across protocols and chains",
            "keywords": ["stablecoin", "flow", "mapping", "liquidity"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Flow analysis", "Liquidity tracking", "Cross-chain monitoring"]
        },
        "token-liquidity-scan": {
            "title": "Token Liquidity Scanner",
            "description": "Scan and analyze token liquidity pools",
            "keywords": ["liquidity", "tokens", "pools", "analysis"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Liquidity analysis", "Pool discovery", "Trading opportunities"]
        },
        "tx-cluster-analyzer": {
            "title": "Transaction Cluster Analyzer",
            "description": "Analyze transaction clusters and patterns",
            "keywords": ["transactions", "clustering", "patterns", "analysis"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Transaction analysis", "Pattern detection", "Network analysis"]
        },
        "whale-tracker": {
            "title": "Whale Tracker",
            "description": "Track large wallet movements and transactions",
            "keywords": ["whale", "tracking", "wallets", "large transactions"],
            "sections": ["Overview", "Usage", "Parameter", "Example", "Features"],
            "use_cases": ["Whale monitoring", "Large transaction tracking", "Market analysis"]
        }
    }
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def build_documentation_index() -> Dict[str, Any]:
    """Build comprehensive documentation index from all skills."""
    index = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "total_skills": 0,
        "by_track": {},
        "by_keyword": {},
        "search_index": [],
        "keyword_frequency": {},
        "track_stats": {}
    }
    
    for track, skills in SKILL_DOCUMENTATION.items():
        track_skills = []
        
        for skill_name, skill_doc in skills.items():
            index["total_skills"] += 1
            
            # Index by track
            if track not in index["by_track"]:
                index["by_track"][track] = []
            track_skills.append(skill_name)
            
            # Index keywords
            for keyword in skill_doc.get("keywords", []):
                if keyword not in index["by_keyword"]:
                    index["by_keyword"][keyword] = []
                index["by_keyword"][keyword].append(skill_name)
                
                # Track frequency
                index["keyword_frequency"][keyword] = index["keyword_frequency"].get(keyword, 0) + 1
            
            # Add to search index
            index["search_index"].append({
                "name": skill_name,
                "title": skill_doc.get("title", ""),
                "track": track,
                "description": skill_doc.get("description", ""),
                "keywords": skill_doc.get("keywords", []),
                "sections": skill_doc.get("sections", []),
                "use_cases": skill_doc.get("use_cases", [])
            })
        
        index["by_track"][track] = track_skills
        index["track_stats"][track] = {
            "total_skills": len(track_skills),
            "skills": track_skills
        }
    
    # Sort by frequency for recommendations
    index["top_keywords"] = sorted(
        index["keyword_frequency"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    return index


def search_documentation(index: Dict, query: str, limit: int = 10) -> Dict[str, Any]:
    """Perform full-text search on documentation index."""
    query_lower = query.lower()
    query_words = query_lower.split()
    
    results = []
    
    for entry in index.get("search_index", []):
        score = 0
        matches = []
        
        # Exact name match (highest priority)
        if query_lower == entry["name"].lower():
            score += 100
            matches.append("name_exact")
        elif query_lower in entry["name"].lower():
            score += 50
            matches.append("name_partial")
        
        # Title match
        if query_lower in entry["title"].lower():
            score += 30
            matches.append("title")
        
        # Description match (each word)
        description = entry["description"].lower()
        for word in query_words:
            if word in description:
                score += 10
                matches.append(f"description:{word}")
        
        # Keyword match (highest value)
        for keyword in entry["keywords"]:
            if query_lower in keyword.lower():
                score += 20
                matches.append(f"keyword:{keyword}")
        
        # Use case match
        for use_case in entry.get("use_cases", []):
            if query_lower in use_case.lower():
                score += 5
                matches.append(f"use_case:{use_case}")
        
        if score > 0:
            results.append({
                **entry,
                "relevance_score": score,
                "match_types": matches[:3]  # Top 3 match types
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "query": query,
        "total_results": len(results),
        "results": results[:limit],
        "search_time_ms": 0
    }


def main():
    parser = argparse.ArgumentParser(description='Build searchable documentation index for skills')
    parser.add_argument('--demo', action='store_true', help='Run demo mode with sample searches')
    parser.add_argument('--search', type=str, help='Search the documentation index')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo or args.search:
            index = build_documentation_index()
            
            if args.demo:
                # Run sample searches
                sample_searches = ["security", "NFT", "monitoring", "web3", "automation"]
                search_results = {}
                
                for sample_query in sample_searches:
                    search_results[sample_query] = search_documentation(index, sample_query, limit=3)
                
                result = {
                    "index_stats": {
                        "total_skills": index["total_skills"],
                        "tracks": len(index["track_stats"]),
                        "unique_keywords": len(index["keyword_frequency"])
                    },
                    "track_distribution": index["track_stats"],
                    "top_keywords": [kw for kw, _ in index["top_keywords"]],
                    "sample_searches": search_results
                }
                print(format_success(result))
            
            elif args.search:
                results = search_documentation(index, args.search)
                print(format_success(results))
        
        elif args.params:
            params = json.loads(args.params)
            index = build_documentation_index()
            
            action = params.get("action", "search")
            if action == "search":
                query = params.get("query", "")
                limit = params.get("limit", 10)
                results = search_documentation(index, query, limit=limit)
                print(format_success(results))
            
            elif action == "index":
                print(format_success({
                    "total_skills": index["total_skills"],
                    "tracks": len(index["track_stats"]),
                    "keywords": len(index["keyword_frequency"])
                }))
            
            else:
                raise ValueError(f"Unknown action: {action}")
        
        else:
            print(format_error("Either --demo, --search, or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
