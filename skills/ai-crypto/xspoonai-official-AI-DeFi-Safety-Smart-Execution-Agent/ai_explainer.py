"""
AI Explainability Layer Module

Converts technical risk signals into plain-English explanations.
Uses an LLM (OpenRouter-compatible) when available, with deterministic
fallback for offline/keyless operation.
"""

import os
import json
from typing import Optional
import urllib.request
import urllib.error

from .safety_analyzer import TokenRiskResult
from .swap_simulator import SwapSimulationResult
from .risk_engine import SafetyVerdict


class AIExplainer:
    """
    Generates human-readable explanations of DeFi safety analysis.
    
    Features:
    - LLM-powered explanations via OpenRouter API (when key available)
    - Deterministic fallback for offline operation
    - Concise, neutral, non-financial-advice tone
    """
    
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
    
    SYSTEM_PROMPT = """You are a DeFi safety analyst assistant. Your role is to explain
technical risk assessments in clear, accessible language.

Guidelines:
- Be concise (2-4 sentences max)
- Be neutral and factual
- Never give financial advice
- Highlight the most important risk factors
- Use simple language avoiding jargon
- If the action is risky, clearly state why
- If the action is safe, acknowledge it briefly"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the explainer.
        
        Args:
            api_key: OpenRouter API key. If None, checks OPENROUTER_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    
    def explain(
        self,
        action_input,
        from_token_risk: TokenRiskResult,
        to_token_risk: TokenRiskResult,
        swap_result: SwapSimulationResult,
        safety_result: SafetyVerdict
    ) -> str:
        """
        Generate a plain-English explanation of the analysis.
        
        Args:
            action_input: Original action input
            from_token_risk: Source token risk analysis
            to_token_risk: Destination token risk analysis
            swap_result: Swap simulation results
            safety_result: Final safety verdict
        
        Returns:
            Human-readable explanation string
        """
        # Build context for explanation
        context = self._build_context(
            action_input,
            from_token_risk,
            to_token_risk,
            swap_result,
            safety_result
        )
        
        # Try LLM explanation if API key is available
        if self.api_key:
            llm_explanation = self._get_llm_explanation(context)
            if llm_explanation:
                return llm_explanation
        
        # Fallback to deterministic explanation
        return self._generate_fallback_explanation(
            action_input,
            from_token_risk,
            to_token_risk,
            swap_result,
            safety_result
        )
    
    def _build_context(
        self,
        action_input,
        from_token_risk: TokenRiskResult,
        to_token_risk: TokenRiskResult,
        swap_result: SwapSimulationResult,
        safety_result: SafetyVerdict
    ) -> str:
        """Build context string for LLM prompt."""
        context = f"""
Action: Swap {action_input.amount} {action_input.from_token} to {action_input.to_token} on {action_input.chain}

Safety Score: {safety_result.score}/100
Verdict: {safety_result.verdict}

Source Token ({action_input.from_token}):
- Risk Level: {from_token_risk.risk_level}
- Liquidity: ${from_token_risk.liquidity_usd:,.0f}
- Verified: {from_token_risk.is_verified}
- Audited: {from_token_risk.has_audit}
- Risk Flags: {len(from_token_risk.risk_flags)}

Destination Token ({action_input.to_token}):
- Risk Level: {to_token_risk.risk_level}
- Liquidity: ${to_token_risk.liquidity_usd:,.0f}
- Verified: {to_token_risk.is_verified}
- Audited: {to_token_risk.has_audit}
- Risk Flags: {len(to_token_risk.risk_flags)}

Swap Simulation:
- Expected Output: {swap_result.expected_output:.6f} {action_input.to_token}
- Price Impact: {swap_result.price_impact_percent:.2f}%
- Slippage: {swap_result.slippage_percent:.2f}%
- Gas Cost: ${swap_result.gas_estimate_usd:.2f}
- MEV Risk: {swap_result.mev_risk}
- Warnings: {len(swap_result.warnings)}
"""
        return context
    
    def _get_llm_explanation(self, context: str) -> Optional[str]:
        """Get explanation from LLM via OpenRouter API."""
        try:
            user_prompt = f"""Based on this DeFi safety analysis, provide a brief 
explanation for the user. Focus on the key risks or safety factors.

{context}

Provide a 2-4 sentence explanation:"""

            payload = {
                "model": self.DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://spoonos.dev",
                "X-Title": "DeFi Safety Agent"
            }
            
            req = urllib.request.Request(
                self.OPENROUTER_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"].strip()
                
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, Exception) as e:
            # Silent fallback - LLM unavailable
            return None
    
    def _generate_fallback_explanation(
        self,
        action_input,
        from_token_risk: TokenRiskResult,
        to_token_risk: TokenRiskResult,
        swap_result: SwapSimulationResult,
        safety_result: SafetyVerdict
    ) -> str:
        """
        Generate deterministic explanation without LLM.
        
        Uses rule-based logic to construct human-readable explanation.
        """
        explanations = []
        
        # Overall verdict statement
        if safety_result.verdict == "SAFE":
            explanations.append(
                f"This swap of {action_input.amount} {action_input.from_token} to "
                f"{action_input.to_token} on {action_input.chain} appears safe with "
                f"a safety score of {safety_result.score}/100."
            )
        elif safety_result.verdict == "CAUTION":
            explanations.append(
                f"This swap has moderate risks with a safety score of {safety_result.score}/100. "
                "Proceed with careful consideration."
            )
        else:  # DANGEROUS
            explanations.append(
                f"This swap carries significant risks with a safety score of only "
                f"{safety_result.score}/100. Caution is strongly advised."
            )
        
        # Key risk factors
        key_risks = []
        
        # Token risks
        if from_token_risk.risk_level in ["high", "critical"]:
            key_risks.append(f"{action_input.from_token} has elevated risk indicators")
        if to_token_risk.risk_level in ["high", "critical"]:
            key_risks.append(f"{action_input.to_token} has elevated risk indicators")
        
        # Liquidity concerns
        min_liquidity = min(from_token_risk.liquidity_usd, to_token_risk.liquidity_usd)
        if min_liquidity < 1_000_000:
            key_risks.append("low liquidity may impact execution")
        
        # Slippage concerns
        total_loss = swap_result.price_impact_percent + swap_result.slippage_percent
        if total_loss > 2:
            key_risks.append(f"expected slippage of {total_loss:.1f}% may reduce output")
        
        # MEV risks
        if swap_result.mev_risk == "high":
            key_risks.append("high MEV exposure could result in unfavorable execution")
        
        # Verification concerns
        if not from_token_risk.is_verified or not to_token_risk.is_verified:
            key_risks.append("unverified contract code increases uncertainty")
        
        # Add key risks to explanation
        if key_risks:
            if len(key_risks) == 1:
                explanations.append(f"The primary concern is {key_risks[0]}.")
            else:
                risk_list = ", ".join(key_risks[:-1]) + f", and {key_risks[-1]}"
                explanations.append(f"Key factors include {risk_list}.")
        else:
            explanations.append(
                "Both tokens are well-established with adequate liquidity and low slippage expected."
            )
        
        return " ".join(explanations)
