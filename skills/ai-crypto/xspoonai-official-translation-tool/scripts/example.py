#!/usr/bin/env python3
"""
Example usage of the Translation Tool
Created by ETHPanda for SpoonOS
"""

from translate import TranslationTool


def example_basic_translation():
    """Example 1: Basic text translation"""
    print("=== Example 1: Basic Text Translation ===")
    tool = TranslationTool(provider="google")

    text = "Hello, world! How are you today?"
    target_lang = "es"

    result = tool.translate_text(text, target_lang)
    print(f"Original (EN): {text}")
    print(f"Translated (ES): {result}")
    print()


def example_language_detection():
    """Example 2: Language detection"""
    print("=== Example 2: Language Detection ===")
    tool = TranslationTool(provider="google")

    texts = [
        "Hello, world!",
        "Bonjour le monde!",
        "こんにちは世界",
        "Hola mundo",
        "Привет мир"
    ]

    for text in texts:
        result = tool.detect_language(text)
        print(f"Text: {text}")
        print(f"Language: {result.get('language')} (confidence: {result.get('confidence', 0):.2%})")
        print()


def example_code_translation():
    """Example 3: Code comment translation"""
    print("=== Example 3: Code Comment Translation ===")
    tool = TranslationTool(provider="google")

    code = """
# Calculate the total price
def calculate_total(items):
    # Initialize total to zero
    total = 0
    # Loop through all items
    for item in items:
        # Add item price to total
        total += item.price
    # Return the final total
    return total
"""

    print("Original code (English comments):")
    print(code)

    # Translate to Spanish
    translated = tool.translate_code_comments(code, "es")
    print("\nTranslated code (Spanish comments):")
    print(translated)


def example_batch_translation():
    """Example 4: Batch translation"""
    print("=== Example 4: Batch Translation ===")
    tool = TranslationTool(provider="google")

    texts = [
        "Welcome to our application",
        "Please enter your username",
        "Password is required",
        "Login successful",
        "Thank you for using our service"
    ]

    target_lang = "fr"

    print(f"Translating UI strings to French:")
    results = tool.batch_translate(texts, target_lang)

    for original, translated in zip(texts, results):
        print(f"EN: {original}")
        print(f"FR: {translated}")
        print()


def example_multi_language():
    """Example 5: Translate to multiple languages"""
    print("=== Example 5: Multi-Language Translation ===")
    tool = TranslationTool(provider="google")

    text = "Welcome to SpoonOS Translation Tool by ETHPanda"
    languages = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh-cn": "Chinese (Simplified)",
        "ko": "Korean"
    }

    print(f"Original: {text}\n")

    for lang_code, lang_name in languages.items():
        translated = tool.translate_text(text, lang_code)
        print(f"{lang_name} ({lang_code}): {translated}")


if __name__ == "__main__":
    print("=" * 60)
    print("Translation Tool Examples by ETHPanda")
    print("=" * 60)
    print()

    try:
        example_basic_translation()
        example_language_detection()
        example_code_translation()
        example_batch_translation()
        example_multi_language()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure to install dependencies:")
        print("pip install -r requirements.txt")
