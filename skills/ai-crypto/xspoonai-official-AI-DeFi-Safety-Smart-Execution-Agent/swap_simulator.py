"""
Swap Simulation Module

Simulates DEX swaps with realistic output estimates including:
- Expected output calculation
- Slippage impact estimation
- Gas cost estimation
- MEV / instability heuristics

This is a READ-ONLY simulation - no actual transactions are executed.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Tuple
from enum import Enum
import math


class MEVRisk(Enum):
    """MEV (Maximal Extractable Value) risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SwapSimulationResult:
    """Complete swap simulation result."""
    from_token: str
    to_token: str
    input_amount: float
    expected_output: float
    minimum_output: float  # After slippage
    price_impact_percent: float
    slippage_percent: float
    gas_estimate_usd: float
    mev_risk: str
    route: str
    warnings: list

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class SwapSimulator:
    """
    Simulates DEX swaps with realistic estimates.
    
    In production, this would integrate with:
    - DEX aggregator APIs (1inch, Paraswap, 0x)
    - On-chain price feeds (Chainlink, Uniswap TWAP)
    - Gas price oracles
    - MEV protection services (Flashbots, MEV Blocker)
    """
    
    # Mock price data (USD values)
    TOKEN_PRICES = {
        "ETH": 3200.00,
        "WETH": 3200.00,
        "BTC": 95000.00,
        "WBTC": 94800.00,
        "USDC": 1.00,
        "USDT": 1.00,
        "DAI": 1.00,
        "ARB": 1.85,
        "LINK": 18.50,
        "UNI": 12.30,
        "PEPE": 0.000015,
        "SHIB": 0.000025,
    }
    
    # Mock liquidity depths (used for slippage calculation)
    LIQUIDITY_DEPTHS = {
        "ETH": 500_000_000,
        "WETH": 400_000_000,
        "USDC": 800_000_000,
        "USDT": 700_000_000,
        "DAI": 200_000_000,
        "WBTC": 150_000_000,
        "ARB": 100_000_000,
        "LINK": 80_000_000,
        "UNI": 60_000_000,
        "PEPE": 15_000_000,
        "SHIB": 30_000_000,
    }
    
    # Gas costs by chain (in USD for a typical swap)
    CHAIN_GAS_COSTS = {
        "ethereum": 15.00,
        "arbitrum": 0.30,
        "optimism": 0.25,
        "polygon": 0.05,
        "base": 0.20,
        "bsc": 0.15,
        "avalanche": 0.50,
    }
    
    # DEX routing preferences by chain
    CHAIN_DEXS = {
        "ethereum": ["Uniswap V3", "Curve", "Sushiswap"],
        "arbitrum": ["Uniswap V3", "Camelot", "GMX"],
        "optimism": ["Velodrome", "Uniswap V3"],
        "polygon": ["Quickswap", "Uniswap V3", "Balancer"],
        "base": ["Aerodrome", "Uniswap V3"],
        "bsc": ["PancakeSwap", "Biswap"],
        "avalanche": ["Trader Joe", "Pangolin"],
    }
    
    def simulate_swap(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str,
        max_slippage: float = 1.0
    ) -> SwapSimulationResult:
        """
        Simulate a token swap and estimate outcomes.
        
        Args:
            from_token: Source token symbol
            to_token: Destination token symbol
            amount: Amount of from_token to swap
            chain: Blockchain to execute on
            max_slippage: Maximum acceptable slippage percentage
        
        Returns:
            SwapSimulationResult with complete simulation data
        """
        from_token = from_token.upper()
        to_token = to_token.upper()
        chain = chain.lower()
        warnings = []
        
        # Get token prices
        from_price = self._get_token_price(from_token)
        to_price = self._get_token_price(to_token)
        
        if from_price == 0 or to_price == 0:
            warnings.append("Price data unavailable for one or more tokens")
        
        # Calculate base swap values
        input_value_usd = amount * from_price
        base_output = input_value_usd / to_price if to_price > 0 else 0
        
        # Calculate price impact based on liquidity
        price_impact = self._calculate_price_impact(
            from_token, to_token, input_value_usd
        )
        
        # Estimate actual slippage
        estimated_slippage = self._estimate_slippage(
            from_token, to_token, input_value_usd, chain
        )
        
        # Check if slippage exceeds max
        if estimated_slippage > max_slippage:
            warnings.append(
                f"Estimated slippage ({estimated_slippage:.2f}%) exceeds max ({max_slippage:.2f}%)"
            )
        
        # Calculate expected and minimum outputs
        total_loss_pct = price_impact + estimated_slippage
        expected_output = base_output * (1 - price_impact / 100)
        minimum_output = base_output * (1 - total_loss_pct / 100)
        
        # Get gas estimate
        gas_estimate = self._estimate_gas(chain, from_token, to_token)
        
        # Warn if gas is significant portion of swap
        gas_percentage = (gas_estimate / input_value_usd * 100) if input_value_usd > 0 else 0
        if gas_percentage > 5:
            warnings.append(
                f"Gas cost ({gas_estimate:.2f} USD) is {gas_percentage:.1f}% of swap value"
            )
        
        # Assess MEV risk
        mev_risk = self._assess_mev_risk(input_value_usd, chain, from_token, to_token)
        if mev_risk == MEVRisk.HIGH:
            warnings.append("High MEV risk: Consider using private transaction pool")
        
        # Determine routing
        route = self._determine_route(chain, from_token, to_token)
        
        return SwapSimulationResult(
            from_token=from_token,
            to_token=to_token,
            input_amount=amount,
            expected_output=round(expected_output, 8),
            minimum_output=round(minimum_output, 8),
            price_impact_percent=round(price_impact, 4),
            slippage_percent=round(estimated_slippage, 4),
            gas_estimate_usd=round(gas_estimate, 2),
            mev_risk=mev_risk.value,
            route=route,
            warnings=warnings
        )
    
    def _get_token_price(self, token: str) -> float:
        """Get token price in USD."""
        return self.TOKEN_PRICES.get(token, 0.0)
    
    def _calculate_price_impact(
        self,
        from_token: str,
        to_token: str,
        value_usd: float
    ) -> float:
        """
        Calculate price impact based on trade size vs liquidity.
        
        Uses simplified constant product AMM formula approximation.
        """
        # Get liquidity for both tokens
        from_liquidity = self.LIQUIDITY_DEPTHS.get(from_token, 1_000_000)
        to_liquidity = self.LIQUIDITY_DEPTHS.get(to_token, 1_000_000)
        
        # Use the smaller liquidity pool as the constraint
        effective_liquidity = min(from_liquidity, to_liquidity)
        
        # Calculate impact: larger trades relative to liquidity = higher impact
        # Simplified formula: impact = (trade_size / liquidity) * 100 * multiplier
        impact = (value_usd / effective_liquidity) * 100 * 2
        
        # Cap at reasonable maximum
        return min(impact, 50.0)
    
    def _estimate_slippage(
        self,
        from_token: str,
        to_token: str,
        value_usd: float,
        chain: str
    ) -> float:
        """
        Estimate execution slippage based on various factors.
        """
        base_slippage = 0.1  # 0.1% base for DEX fees
        
        # Add volatility component for non-stablecoins
        stablecoins = {"USDC", "USDT", "DAI", "FRAX", "LUSD"}
        
        if from_token not in stablecoins:
            base_slippage += 0.15
        if to_token not in stablecoins:
            base_slippage += 0.15
        
        # Add size-based slippage
        if value_usd > 100_000:
            base_slippage += 0.3
        elif value_usd > 10_000:
            base_slippage += 0.1
        
        # L2s typically have slightly better execution
        l2_chains = {"arbitrum", "optimism", "base", "polygon"}
        if chain in l2_chains:
            base_slippage *= 0.8
        
        return base_slippage
    
    def _estimate_gas(self, chain: str, from_token: str, to_token: str) -> float:
        """Estimate gas cost in USD for the swap."""
        base_gas = self.CHAIN_GAS_COSTS.get(chain, 1.0)
        
        # Multi-hop routes cost more
        # Simplified: non-ETH pairs might need extra hops
        if from_token not in {"ETH", "WETH"} and to_token not in {"ETH", "WETH"}:
            base_gas *= 1.5
        
        return base_gas
    
    def _assess_mev_risk(
        self,
        value_usd: float,
        chain: str,
        from_token: str,
        to_token: str
    ) -> MEVRisk:
        """
        Assess MEV (sandwich attack, frontrunning) risk.
        """
        # Large trades on mainnet have highest MEV risk
        if chain == "ethereum":
            if value_usd > 50_000:
                return MEVRisk.HIGH
            elif value_usd > 10_000:
                return MEVRisk.MEDIUM
        
        # L2s have lower MEV due to sequencer ordering
        l2_chains = {"arbitrum", "optimism", "base"}
        if chain in l2_chains:
            if value_usd > 100_000:
                return MEVRisk.MEDIUM
            return MEVRisk.LOW
        
        # Default assessment
        if value_usd > 25_000:
            return MEVRisk.MEDIUM
        
        return MEVRisk.LOW
    
    def _determine_route(self, chain: str, from_token: str, to_token: str) -> str:
        """Determine optimal routing for the swap."""
        available_dexs = self.CHAIN_DEXS.get(chain, ["Generic DEX"])
        primary_dex = available_dexs[0] if available_dexs else "Unknown DEX"
        
        # Check if direct pair or needs routing through ETH/stablecoin
        major_tokens = {"ETH", "WETH", "USDC", "USDT"}
        
        if from_token in major_tokens or to_token in major_tokens:
            return f"Direct swap via {primary_dex}"
        else:
            return f"Multi-hop via {primary_dex}: {from_token} → WETH → {to_token}"
