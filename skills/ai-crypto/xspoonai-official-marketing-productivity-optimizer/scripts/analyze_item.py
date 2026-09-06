"""
analyze_item.py — Item Analysis & Marketing Insight Extraction

Analyzes item characteristics and generates structured marketing insights
including value propositions, target audience mapping, and copy angles.

Usage:
    echo '{"category": "electronics", "description": "Wireless noise-cancelling earbuds with 30h battery"}' | python analyze_item.py
    python analyze_item.py --input item.json
"""

import json
import sys
import argparse
from typing import Any


# Style/tone mapping based on item categories
CATEGORY_TONE_MAP = {
    "electronics": {"tone": "innovative", "angles": ["tech specs", "convenience", "premium quality"]},
    "fashion": {"tone": "aspirational", "angles": ["style", "confidence", "self-expression"]},
    "food": {"tone": "sensory", "angles": ["taste", "health", "convenience"]},
    "beauty": {"tone": "transformative", "angles": ["results", "self-care", "confidence"]},
    "fitness": {"tone": "motivational", "angles": ["performance", "transformation", "lifestyle"]},
    "home": {"tone": "comfortable", "angles": ["quality of life", "design", "practicality"]},
    "travel": {"tone": "adventurous", "angles": ["experience", "freedom", "discovery"]},
    "education": {"tone": "empowering", "angles": ["growth", "opportunity", "expertise"]},
    "software": {"tone": "efficient", "angles": ["productivity", "simplicity", "results"]},
    "health": {"tone": "trustworthy", "angles": ["wellness", "safety", "improvement"]},
}

# Default audience segments
AUDIENCE_SEGMENTS = {
    "gen_z": {"age": "18-24", "traits": ["digital native", "value-driven", "trend-conscious"]},
    "millennial": {"age": "25-40", "traits": ["experience-seeking", "brand-aware", "convenience-focused"]},
    "gen_x": {"age": "41-56", "traits": ["quality-oriented", "practical", "loyal"]},
    "professional": {"age": "25-45", "traits": ["career-focused", "time-constrained", "ROI-minded"]},
    "parent": {"age": "28-45", "traits": ["family-first", "safety-conscious", "budget-aware"]},
}

# Platform-specific constraints
PLATFORM_SPECS = {
    "instagram": {
        "primary_text_limit": 2200,
        "visible_text_limit": 125,
        "headline_limit": None,
        "hashtag_count": "5-10",
        "image_sizes": ["1080x1080", "1080x1920"],
    },
    "facebook": {
        "primary_text_limit": 125,
        "visible_text_limit": 125,
        "headline_limit": 27,
        "hashtag_count": "0-3",
        "image_sizes": ["1200x628", "1080x1080"],
    },
}


def analyze_item(item_data: dict[str, Any]) -> dict[str, Any]:
    """Analyze item and produce structured marketing insights."""
    category = item_data.get("category", "general").lower()
    description = item_data.get("description", "")
    target_audience = item_data.get("target_audience", None)
    platform = item_data.get("platform", "instagram").lower()

    # Get tone and angles
    tone_info = CATEGORY_TONE_MAP.get(category, {"tone": "engaging", "angles": ["value", "quality", "trust"]})

    # Build analysis result
    analysis = {
        "item": {
            "category": category,
            "description": description,
            "tone": tone_info["tone"],
            "recommended_angles": tone_info["angles"],
        },
        "audience": _resolve_audience(target_audience, category),
        "platform": {
            "name": platform,
            "specs": PLATFORM_SPECS.get(platform, PLATFORM_SPECS["instagram"]),
        },
        "copy_strategy": {
            "hooks": {
                "problem_solution": f"Lead with the pain point that {category} items typically solve",
                "benefit_first": f"Lead with the primary benefit using a {tone_info['tone']} tone",
                "social_proof": "Lead with credibility, stats, or scarcity",
            },
            "guidelines": {
                "language": "English",
                "tone": tone_info["tone"],
                "emoji_usage": "max 2-3, purposeful only",
                "cta_required": True,
            },
        },
        "visual_strategy": {
            "recommended_styles": _recommend_styles(category, tone_info["tone"]),
        },
    }

    return analysis


def _resolve_audience(target_audience: str | None, category: str) -> dict[str, Any]:
    """Resolve target audience from user input or infer from category."""
    if target_audience:
        return {
            "source": "user_defined",
            "description": target_audience,
            "suggestion": "Use the user-provided audience definition as primary targeting.",
        }

    # Infer audience from category
    category_audience_map = {
        "electronics": "millennial",
        "fashion": "gen_z",
        "food": "millennial",
        "beauty": "gen_z",
        "fitness": "millennial",
        "home": "gen_x",
        "travel": "millennial",
        "education": "professional",
        "software": "professional",
        "health": "parent",
    }

    segment_key = category_audience_map.get(category, "millennial")
    segment = AUDIENCE_SEGMENTS[segment_key]

    return {
        "source": "inferred",
        "segment": segment_key,
        "age_range": segment["age"],
        "traits": segment["traits"],
        "suggestion": f"Inferred '{segment_key}' audience based on '{category}' category. Adjust if needed.",
    }


def _recommend_styles(category: str, tone: str) -> list[dict[str, str]]:
    """Recommend 4 visual styles based on item category and tone."""
    style_pool = {
        "clean_minimal": {"name": "Clean Minimal", "description": "White/neutral background, product focus, elegant typography"},
        "lifestyle": {"name": "Lifestyle Context", "description": "Product in real-life usage scenario with people"},
        "bold_graphic": {"name": "Bold & Graphic", "description": "Strong colors, large typography, attention-grabbing"},
        "mood_aesthetic": {"name": "Mood & Aesthetic", "description": "Atmospheric, color-graded, editorial feel"},
        "flat_lay": {"name": "Flat Lay", "description": "Top-down arrangement with complementary props"},
        "before_after": {"name": "Before/After", "description": "Transformation comparison visual"},
        "infographic": {"name": "Infographic Style", "description": "Feature callouts, specs, comparison data"},
        "ugc_authentic": {"name": "UGC / Authentic", "description": "Casual, user-generated content aesthetic"},
    }

    # Category-to-style mapping (pick 4 per category)
    category_styles = {
        "electronics": ["clean_minimal", "infographic", "lifestyle", "bold_graphic"],
        "fashion": ["lifestyle", "mood_aesthetic", "bold_graphic", "ugc_authentic"],
        "food": ["flat_lay", "lifestyle", "mood_aesthetic", "ugc_authentic"],
        "beauty": ["before_after", "mood_aesthetic", "clean_minimal", "lifestyle"],
        "fitness": ["before_after", "lifestyle", "bold_graphic", "ugc_authentic"],
        "home": ["lifestyle", "flat_lay", "clean_minimal", "mood_aesthetic"],
        "travel": ["mood_aesthetic", "lifestyle", "ugc_authentic", "bold_graphic"],
        "education": ["infographic", "clean_minimal", "bold_graphic", "lifestyle"],
        "software": ["infographic", "clean_minimal", "bold_graphic", "lifestyle"],
        "health": ["clean_minimal", "lifestyle", "before_after", "infographic"],
    }

    selected_keys = category_styles.get(category, ["clean_minimal", "lifestyle", "bold_graphic", "mood_aesthetic"])
    return [style_pool[key] for key in selected_keys]


def main():
    parser = argparse.ArgumentParser(description="Analyze item for marketing insights")
    parser.add_argument("--input", "-i", type=str, help="Path to JSON input file")
    args = parser.parse_args()

    # Read input from file or stdin
    if args.input:
        with open(args.input, "r") as f:
            item_data = json.load(f)
    else:
        item_data = json.load(sys.stdin)

    # Run analysis
    result = analyze_item(item_data)

    # Output as formatted JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
