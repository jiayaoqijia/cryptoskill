"""
Token Safety Analyzer Module

Analyzes token-level risks using heuristic logic including:
- Liquidity depth assessment
- Holder concentration analysis
- Honeypot / blacklist / pause detection (heuristic)
- Centralization risk indicators
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict
from enum import Enum


class RiskLevel(Enum):
    """Risk level classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskFlag:
    """Individual risk flag with severity and description."""
    category: str
    severity: str
    description: str
    weight: float = 1.0


@dataclass
class TokenRiskResult:
    """Complete token risk analysis result."""
    token: str
    chain: str
    risk_level: str
    risk_score: int  # 0-100, higher = riskier
    liquidity_usd: float
    holder_count: int
    top_holder_percentage: float
    risk_flags: List[Dict] = field(default_factory=list)
    is_verified: bool = True
    has_audit: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class SafetyAnalyzer:
    """
    Analyzes token safety using heuristic rules and mock data.
    
    In production, this would integrate with:
    - DEX liquidity APIs (Uniswap, SushiSwap, etc.)
    - Token holder distribution APIs (Etherscan, Arbiscan)
    - Security audit databases (CertiK, Trail of Bits)
    - Honeypot detection services
    """
    
    # Mock token database with realistic characteristics
    TOKEN_DATA = {
        # Major stablecoins - high safety
        "USDC": {
            "liquidity_usd": 500_000_000,
            "holder_count": 1_500_000,
            "top_holder_pct": 15.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": True,
            "has_pause": True,  # Circle can pause
            "has_blacklist": True,
        },
        "USDT": {
            "liquidity_usd": 600_000_000,
            "holder_count": 2_000_000,
            "top_holder_pct": 20.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": True,
            "has_pause": True,
            "has_blacklist": True,
        },
        "DAI": {
            "liquidity_usd": 200_000_000,
            "holder_count": 500_000,
            "top_holder_pct": 8.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": True,
            "has_pause": False,
            "has_blacklist": False,
        },
        # Major tokens - high safety
        "ETH": {
            "liquidity_usd": 1_000_000_000,
            "holder_count": 100_000_000,
            "top_holder_pct": 5.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        "WETH": {
            "liquidity_usd": 800_000_000,
            "holder_count": 2_000_000,
            "top_holder_pct": 10.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        "WBTC": {
            "liquidity_usd": 300_000_000,
            "holder_count": 100_000,
            "top_holder_pct": 25.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        "ARB": {
            "liquidity_usd": 150_000_000,
            "holder_count": 800_000,
            "top_holder_pct": 40.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        # Medium-risk tokens
        "LINK": {
            "liquidity_usd": 100_000_000,
            "holder_count": 600_000,
            "top_holder_pct": 35.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        "UNI": {
            "liquidity_usd": 80_000_000,
            "holder_count": 400_000,
            "top_holder_pct": 30.0,
            "is_verified": True,
            "has_audit": True,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        # Higher risk example tokens
        "PEPE": {
            "liquidity_usd": 20_000_000,
            "holder_count": 200_000,
            "top_holder_pct": 55.0,
            "is_verified": True,
            "has_audit": False,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
        "SHIB": {
            "liquidity_usd": 50_000_000,
            "holder_count": 1_000_000,
            "top_holder_pct": 60.0,
            "is_verified": True,
            "has_audit": False,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        },
    }
    
    # Thresholds for risk assessment
    LIQUIDITY_THRESHOLDS = {
        "critical": 100_000,      # < $100K = critical
        "high": 1_000_000,        # < $1M = high risk
        "medium": 10_000_000,     # < $10M = medium risk
        "low": 50_000_000,        # >= $50M = low risk
    }
    
    HOLDER_CONCENTRATION_THRESHOLDS = {
        "critical": 70.0,  # Top holder > 70%
        "high": 50.0,      # Top holder > 50%
        "medium": 30.0,    # Top holder > 30%
    }
    
    def analyze_token(self, token: str, chain: str) -> TokenRiskResult:
        """
        Analyze a token's safety profile.
        
        Args:
            token: Token symbol (e.g., "ETH", "USDC")
            chain: Blockchain name (e.g., "Arbitrum", "Ethereum")
        
        Returns:
            TokenRiskResult with complete risk analysis
        """
        token = token.upper()
        risk_flags = []
        
        # Get token data (mock or default for unknown tokens)
        token_info = self._get_token_data(token)
        
        # Analyze liquidity
        liquidity_flags = self._analyze_liquidity(token_info["liquidity_usd"])
        risk_flags.extend(liquidity_flags)
        
        # Analyze holder concentration
        concentration_flags = self._analyze_holder_concentration(
            token_info["top_holder_pct"],
            token_info["holder_count"]
        )
        risk_flags.extend(concentration_flags)
        
        # Check for honeypot / blacklist indicators
        security_flags = self._analyze_security_features(token_info, token)
        risk_flags.extend(security_flags)
        
        # Check verification and audit status
        verification_flags = self._analyze_verification(token_info)
        risk_flags.extend(verification_flags)
        
        # Calculate overall risk score
        risk_score = self._calculate_risk_score(risk_flags)
        risk_level = self._classify_risk_level(risk_score)
        
        return TokenRiskResult(
            token=token,
            chain=chain,
            risk_level=risk_level,
            risk_score=risk_score,
            liquidity_usd=token_info["liquidity_usd"],
            holder_count=token_info["holder_count"],
            top_holder_percentage=token_info["top_holder_pct"],
            risk_flags=[asdict(f) if isinstance(f, RiskFlag) else f for f in risk_flags],
            is_verified=token_info["is_verified"],
            has_audit=token_info["has_audit"]
        )
    
    def _get_token_data(self, token: str) -> dict:
        """Get token data from mock database or generate defaults for unknown tokens."""
        if token in self.TOKEN_DATA:
            return self.TOKEN_DATA[token]
        
        # Unknown token - assume higher risk
        return {
            "liquidity_usd": 500_000,  # Low liquidity
            "holder_count": 5_000,
            "top_holder_pct": 45.0,
            "is_verified": False,
            "has_audit": False,
            "is_stablecoin": False,
            "has_pause": False,
            "has_blacklist": False,
        }
    
    def _analyze_liquidity(self, liquidity_usd: float) -> List[RiskFlag]:
        """Analyze liquidity depth and generate risk flags."""
        flags = []
        
        if liquidity_usd < self.LIQUIDITY_THRESHOLDS["critical"]:
            flags.append(RiskFlag(
                category="liquidity",
                severity="critical",
                description=f"Extremely low liquidity (${liquidity_usd:,.0f}). High slippage and exit risk.",
                weight=3.0
            ))
        elif liquidity_usd < self.LIQUIDITY_THRESHOLDS["high"]:
            flags.append(RiskFlag(
                category="liquidity",
                severity="high",
                description=f"Low liquidity (${liquidity_usd:,.0f}). Significant slippage possible.",
                weight=2.0
            ))
        elif liquidity_usd < self.LIQUIDITY_THRESHOLDS["medium"]:
            flags.append(RiskFlag(
                category="liquidity",
                severity="medium",
                description=f"Moderate liquidity (${liquidity_usd:,.0f}). Some slippage expected for large trades.",
                weight=1.0
            ))
        
        return flags
    
    def _analyze_holder_concentration(self, top_holder_pct: float, holder_count: int) -> List[RiskFlag]:
        """Analyze holder concentration for centralization risks."""
        flags = []
        
        if top_holder_pct >= self.HOLDER_CONCENTRATION_THRESHOLDS["critical"]:
            flags.append(RiskFlag(
                category="concentration",
                severity="critical",
                description=f"Extreme concentration: top holder owns {top_holder_pct:.1f}%. Rug pull risk.",
                weight=3.0
            ))
        elif top_holder_pct >= self.HOLDER_CONCENTRATION_THRESHOLDS["high"]:
            flags.append(RiskFlag(
                category="concentration",
                severity="high",
                description=f"High concentration: top holder owns {top_holder_pct:.1f}%. Price manipulation possible.",
                weight=2.0
            ))
        elif top_holder_pct >= self.HOLDER_CONCENTRATION_THRESHOLDS["medium"]:
            flags.append(RiskFlag(
                category="concentration",
                severity="medium",
                description=f"Moderate concentration: top holder owns {top_holder_pct:.1f}%.",
                weight=1.0
            ))
        
        if holder_count < 1000:
            flags.append(RiskFlag(
                category="adoption",
                severity="medium",
                description=f"Low holder count ({holder_count:,}). Limited market adoption.",
                weight=1.0
            ))
        
        return flags
    
    def _analyze_security_features(self, token_info: dict, token: str) -> List[RiskFlag]:
        """Analyze potential honeypot/blacklist/pause indicators."""
        flags = []
        
        if token_info.get("has_pause"):
            flags.append(RiskFlag(
                category="centralization",
                severity="low",
                description="Token has pause functionality. Issuer can freeze transfers.",
                weight=0.5
            ))
        
        if token_info.get("has_blacklist"):
            flags.append(RiskFlag(
                category="centralization",
                severity="low",
                description="Token has blacklist functionality. Addresses can be blocked.",
                weight=0.5
            ))
        
        # Heuristic honeypot detection for unknown tokens
        if token not in self.TOKEN_DATA:
            flags.append(RiskFlag(
                category="security",
                severity="high",
                description="Unknown token. Potential honeypot risk - verify contract before trading.",
                weight=2.5
            ))
        
        return flags
    
    def _analyze_verification(self, token_info: dict) -> List[RiskFlag]:
        """Check smart contract verification and audit status."""
        flags = []
        
        if not token_info.get("is_verified"):
            flags.append(RiskFlag(
                category="verification",
                severity="high",
                description="Contract source code not verified. Cannot inspect for malicious code.",
                weight=2.0
            ))
        
        if not token_info.get("has_audit"):
            flags.append(RiskFlag(
                category="audit",
                severity="medium",
                description="No security audit found. Smart contract may contain vulnerabilities.",
                weight=1.5
            ))
        
        return flags
    
    def _calculate_risk_score(self, flags: List[RiskFlag]) -> int:
        """Calculate overall risk score (0-100) from risk flags."""
        if not flags:
            return 0
        
        # Weight mapping for severity
        severity_weights = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3
        }
        
        total_score = 0
        for flag in flags:
            base_score = severity_weights.get(flag.severity, 5)
            total_score += base_score * flag.weight
        
        # Cap at 100
        return min(100, int(total_score))
    
    def _classify_risk_level(self, score: int) -> str:
        """Classify risk level based on score."""
        if score >= 60:
            return RiskLevel.CRITICAL.value
        elif score >= 40:
            return RiskLevel.HIGH.value
        elif score >= 20:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value
