#!/usr/bin/env python3
"""
Refactoring Suggestion Generator
Generates specific refactoring recommendations with code examples
"""

from typing import Dict, List, Any

class RefactoringSuggester:
    """Generate refactoring recommendations."""

    def __init__(self):
        self.patterns = {
            "god_function": {
                "rank": 1,
                "pattern": "Function is too large",
                "solutions": [
                    "Extract method pattern - break into smaller functions",
                    "Use strategy pattern for complex logic branches",
                    "Apply decorator pattern for cross-cutting concerns"
                ]
            },
            "long_parameter_list": {
                "rank": 2,
                "pattern": "Too many parameters",
                "solutions": [
                    "Use parameter object / dataclass",
                    "Apply builder pattern",
                    "Use dependency injection"
                ]
            },
            "deep_nesting": {
                "rank": 3,
                "pattern": "Deeply nested conditionals",
                "solutions": [
                    "Extract nested logic to separate functions",
                    "Use guard clauses / early returns",
                    "Apply strategy or state pattern"
                ]
            },
            "duplicate_code": {
                "rank": 4,
                "pattern": "Code duplication",
                "solutions": [
                    "Extract common method",
                    "Use composition over inheritance",
                    "Apply DRY principle"
                ]
            },
            "reentrancy_risk": {
                "rank": 5,
                "pattern": "Reentrancy vulnerability",
                "solutions": [
                    "Add reentrancy guard (OpenZeppelin)",
                    "Use checks-effects-interactions pattern",
                    "Transfer funds last"
                ]
            }
        }

    def suggest_refactoring(self, smell_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate refactoring suggestions."""
        suggestions = []
        
        for smell in smell_data.get("smells", []):
            smell_type = smell.get("type")
            pattern_info = self.patterns.get(smell_type, {})
            
            suggestion = {
                "smell_type": smell_type,
                "severity": smell.get("severity"),
                "confidence": smell.get("confidence"),
                "current_issue": smell.get("recommendation", "Code smell detected"),
                "solutions": pattern_info.get("solutions", []),
                "priority": pattern_info.get("rank", 5),
                "refactoring_effort": self._estimate_effort(smell_type),
                "benefits": self._get_benefits(smell_type),
                "code_example": self._get_example(smell_type)
            }
            suggestions.append(suggestion)
        
        # Sort by priority
        suggestions = sorted(suggestions, key=lambda x: x["priority"])

        return {
            "refactoring_opportunities": len(suggestions),
            "code_quality_improvement": self._estimate_improvement(suggestions),
            "estimated_total_effort": self._estimate_total_effort(suggestions),
            "suggestions": suggestions
        }

    def _estimate_effort(self, smell_type: str) -> str:
        """Estimate refactoring effort."""
        effort_map = {
            "magic_numbers": "TRIVIAL (5 min)",
            "insufficient_comments": "TRIVIAL (10 min)",
            "long_parameter_list": "SMALL (30 min)",
            "deep_nesting": "SMALL (1 hour)",
            "god_function": "MEDIUM (2-3 hours)",
            "duplicate_code": "MEDIUM (2-4 hours)",
            "reentrancy_risk": "LARGE (4+ hours)",
            "unchecked_arithmetic": "SMALL (1 hour)"
        }
        return effort_map.get(smell_type, "MEDIUM (2 hours)")

    def _get_benefits(self, smell_type: str) -> List[str]:
        """Get benefits of refactoring."""
        benefits_map = {
            "god_function": [
                "Improved testability",
                "Better code reuse",
                "Easier debugging",
                "Reduced cognitive load"
            ],
            "long_parameter_list": [
                "Clearer API",
                "Better maintainability",
                "Easier testing with fixtures",
                "Reduced parameter coupling"
            ],
            "deep_nesting": [
                "Improved readability",
                "Reduced cyclomatic complexity",
                "Easier testing",
                "Better maintainability"
            ],
            "reentrancy_risk": [
                "Enhanced security",
                "Protection against attacks",
                "Compliance with best practices",
                "Reduced vulnerability surface"
            ],
            "duplicate_code": [
                "Reduced maintenance burden",
                "Single source of truth",
                "Easier bug fixes",
                "Better code reuse"
            ]
        }
        return benefits_map.get(smell_type, ["Improved code quality"])

    def _get_example(self, smell_type: str) -> Dict[str, str]:
        """Get refactoring code example."""
        examples = {
            "god_function": {
                "before": """def process_order(user_id, items, address, payment, quantity):
    # 100 lines of logic
    validate_user()
    check_inventory()
    calculate_price()
    process_payment()
    update_shipment()""",
                "after": """class OrderProcessor:
    def process(self, order: Order):
        self.validate_user(order.user_id)
        self.check_inventory(order.items)
        price = self.calculate_price(order)
        self.process_payment(price)
        self.update_shipment(order)"""
            },
            "long_parameter_list": {
                "before": "def create_user(name, email, password, phone, address, country, zipcode):",
                "after": """@dataclass
class UserInput:
    name: str
    email: str
    password: str
    phone: str
    address: str
    country: str
    zipcode: str

def create_user(user_input: UserInput):"""
            },
            "reentrancy_risk": {
                "before": """function withdraw() external {
    uint balance = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
    balances[msg.sender] = 0;
}""",
                "after": """function withdraw() external nonReentrant {
    uint balance = balances[msg.sender];
    balances[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success);
}"""
            }
        }
        return examples.get(smell_type, {"before": "...", "after": "..."})

    def _estimate_improvement(self, suggestions: List[Dict]) -> int:
        """Estimate code quality improvement."""
        if not suggestions:
            return 0
        
        high_priority = sum(1 for s in suggestions if s["priority"] <= 2)
        return min(100, high_priority * 15)

    def _estimate_total_effort(self, suggestions: List[Dict]) -> str:
        """Estimate total refactoring effort."""
        effort_hours = 0
        for suggestion in suggestions[:5]:  # Top 5
            effort_text = suggestion["refactoring_effort"]
            if "5 min" in effort_text:
                effort_hours += 0.1
            elif "10 min" in effort_text:
                effort_hours += 0.17
            elif "30 min" in effort_text:
                effort_hours += 0.5
            elif "1 hour" in effort_text:
                effort_hours += 1
            elif "2-3 hours" in effort_text:
                effort_hours += 2.5
            elif "2-4 hours" in effort_text:
                effort_hours += 3
            elif "4+" in effort_text:
                effort_hours += 5
        
        return f"{effort_hours:.1f} hours"


if __name__ == "__main__":
    suggester = RefactoringSuggester()
    
    sample_smell = {
        "smells": [
            {
                "type": "god_function",
                "severity": "HIGH",
                "confidence": 95,
                "recommendation": "Split function into smaller pieces"
            },
            {
                "type": "long_parameter_list",
                "severity": "MEDIUM",
                "confidence": 90,
                "recommendation": "Use dataclass"
            }
        ]
    }
    
    result = suggester.suggest_refactoring(sample_smell)
    
    import json
    print(json.dumps(result, indent=2))
