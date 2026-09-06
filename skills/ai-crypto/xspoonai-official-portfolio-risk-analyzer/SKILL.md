---
name: portfolio-risk-analyzer
description: Advanced portfolio risk analysis and monitoring for Web3 assets with liquidation warnings, correlation analysis, and diversification recommendations
version: 1.0.0
author: Sambit Sargam
tags:
  - portfolio
  - risk
  - analysis
  - liquidation
  - correlation
  - diversification
  - defi
  - monitoring
  - alerts
triggers:
  - type: keyword
    keywords:
      - portfolio risk
      - liquidation risk
      - portfolio health
      - risk score
      - concentration risk
      - correlation
      - diversification
      - ltv
      - loan-to-value
      - portfolio exposure
      - risk management
      - position risk
    priority: 95
  - type: pattern
    patterns:
      - "(?i)(analyze|check|assess) .*portfolio .*(risk|health|exposure)"
      - "(?i)(calculate|show|get) .*risk .*(score|rating|level)"
      - "(?i)(what|check) .*liquidation .*(price|risk|danger)"
      - "(?i)(am|is) .*(my|this|the) .*(portfolio|position) .*(safe|at risk|healthy)"
      - "(?i)(how|much) .*(concentration|diversification) .*(risk|exposure)"
      - "(?i)(monitor|alert) .*(portfolio|position|account) .*(risk|health|danger)"
      - "(?i)(ltv|loan.to.value) .*(health|status|ratio)"
    priority: 90
  - type: intent
    intent_category: portfolio_risk_analysis
    priority: 98
parameters:
  - name: address
    type: string
    required: true
    description: Wallet address to analyze for risk
  - name: chain
    type: string
    required: false
    default: ethereum
    description: Blockchain network (ethereum, polygon, arbitrum, optimism, avalanche, base)
  - name: analysis_type
    type: string
    required: false
    default: comprehensive
    description: Type of analysis (comprehensive, concentration, correlation, liquidation, defi_exposure)
  - name: include_defi_positions
    type: boolean
    required: false
    default: true
    description: Include DeFi lending/borrowing positions in analysis
  - name: alert_threshold
    type: number
    required: false
    default: 75
    description: Risk threshold percentage for alerts (0-100)
  - name: include_recommendations
    type: boolean
    required: false
    default: true
    description: Include diversification and rebalancing recommendations
prerequisites:
  env_vars:
    - ETHERSCAN_API_KEY
    - ALCHEMY_API_KEY
    - DEFI_PROTOCOL_API_KEY (optional for lending protocol data)
  skills: []
composable: true
persist_state: true
cache_enabled: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: portfolio_fetcher
      description: Fetch all ERC20 and NFT holdings from wallet
      type: python
      file: portfolio_fetcher.py
      timeout: 45
      requires_auth: false

    - name: risk_calculator
      description: Calculate comprehensive risk metrics for portfolio
      type: python
      file: risk_calculator.py
      timeout: 60
      requires_auth: false

    - name: correlation_analyzer
      description: Analyze token correlation and concentration risk
      type: python
      file: correlation_analyzer.py
      timeout: 45
      requires_auth: false

    - name: defi_exposure_analyzer
      description: Analyze DeFi lending/borrowing positions and liquidation risk
      type: python
      file: defi_exposure_analyzer.py
      timeout: 45
      requires_auth: false

    - name: liquidation_monitor
      description: Calculate liquidation prices and LTV health
      type: python
      file: liquidation_monitor.py
      timeout: 30
      requires_auth: false

    - name: diversification_recommender
      description: Generate portfolio rebalancing and diversification recommendations
      type: python
      file: diversification_recommender.py
      timeout: 30
      requires_auth: false

capabilities:
  - real-time portfolio valuation
  - concentration risk scoring
  - token correlation analysis
  - liquidation price warnings
  - defi position monitoring
  - ltv health tracking
  - diversification recommendations
  - risk-adjusted allocation suggestions
  - portfolio rebalancing guidance
  - exposure analysis across chains

security_considerations:
  - Read-only operations (no transaction signing)
  - No private key exposure
  - Public blockchain data queries only
  - Rate-limited API calls
  - Optional data caching for performance
  - No wallet balance modification

use_cases:
  - Monitor DeFi position safety in real-time
  - Identify liquidation risks before they occur
  - Reduce concentration risk through data-driven recommendations
  - Optimize portfolio allocation across chains
  - Track correlation between holdings
  - Alert on portfolio health changes

example_queries:
  - "Analyze portfolio risk for address 0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543 on Ethereum"
  - "Calculate liquidation risk for my Aave position"
  - "Show portfolio concentration and diversification suggestions"
  - "What's my current LTV health and liquidation price on Compound?"
  - "Analyze correlation between my token holdings"
  - "Alert if my portfolio risk score exceeds 75%"
  - "Generate rebalancing recommendations for safer allocation"

integration_points:
  - Etherscan API (token holdings, transfers)
  - Alchemy API (portfolio data, NFT metadata)
  - Aave Subgraph (lending positions)
  - Compound Subgraph (borrowing positions)
  - Curve Finance API (LP positions)
  - Uniswap Subgraph (V2/V3 LP positions)
  - CoinGecko API (token prices, market data)

version_history:
  - version: 1.0.0
    date: 2026-02-07
    changes:
      - Initial release with core portfolio risk analysis
      - Support for 6 major EVM chains
      - DeFi position monitoring
      - Liquidation risk alerts
      - Diversification recommendations
