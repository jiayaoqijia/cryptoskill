#!/usr/bin/env python3
"""
Translation Tool - Multi-language translation service
Created by ETHPanda for SpoonOS
"""

import os
import re
import sys
import json
from typing import Optional, List, Dict, Any
from enum import Enum

try:
    from googletrans import Translator as GoogleTranslator
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Warning: googletrans not installed. Install with: pip install googletrans==4.0.0-rc1", file=sys.stderr)


class TranslationProvider(Enum):
    """Available translation providers"""
    GOOGLE = "google"
    DEEPL = "deepl"


class TranslationTool:
    """Main translation tool class"""

    def __init__(self, provider: str = "google", api_key: Optional[str] = None):
        """
        Initialize the translation tool

        Args:
            provider: Translation provider to use ("google" or "deepl")
            api_key: API key for the provider (if required)
        """
        self.provider = provider
        self.api_key = api_key or os.getenv("TRANSLATION_API_KEY")
        self.translator = None

        if provider == "google" and GOOGLE_AVAILABLE:
            self.translator = GoogleTranslator()
        elif provider == "deepl":
            # DeepL implementation would go here
            raise NotImplementedError("DeepL provider not yet implemented")
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> str:
        """
        Translate text from one language to another

        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'es', 'fr', 'ja')
            source_lang: Source language code (auto-detected if None)

        Returns:
            Translated text
        """
        if not self.translator:
            return f"Error: Translator not initialized"

        try:
            if self.provider == "google":
                result = self.translator.translate(
                    text,
                    dest=target_lang,
                    src=source_lang or 'auto'
                )
                return result.text
            else:
                return f"Error: Provider {self.provider} not supported"
        except Exception as e:
            return f"Translation error: {str(e)}"

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text

        Args:
            text: Text to analyze

        Returns:
            Dictionary with language code and confidence
        """
        if not self.translator:
            return {"error": "Translator not initialized"}

        try:
            if self.provider == "google":
                result = self.translator.detect(text)
                return {
                    "language": result.lang,
                    "confidence": result.confidence
                }
            else:
                return {"error": f"Provider {self.provider} not supported"}
        except Exception as e:
            return {"error": str(e)}

    def translate_code_comments(
        self,
        code: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> str:
        """
        Translate comments in code while preserving code structure

        Args:
            code: Source code with comments
            target_lang: Target language code
            source_lang: Source language code (auto-detected if None)

        Returns:
            Code with translated comments
        """
        if not self.translator:
            return code

        # Pattern to match single-line comments
        single_line_pattern = r'([ \t]*)(#|//)(.*?)$'
        # Pattern to match multi-line comments (Python docstrings, C-style)
        multi_line_pattern = r'([ \t]*)("""|\'\'\'/\*)(.*?)("""|\'\'\'|\*/)'

        def translate_match(match):
            indent = match.group(1)
            comment_start = match.group(2)
            comment_text = match.group(3).strip()

            if not comment_text:
                return match.group(0)

            try:
                translated = self.translate_text(comment_text, target_lang, source_lang)
                return f"{indent}{comment_start} {translated}"
            except:
                return match.group(0)

        # Translate single-line comments
        result = re.sub(single_line_pattern, translate_match, code, flags=re.MULTILINE)

        return result

    def batch_translate(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> List[str]:
        """
        Translate multiple text blocks at once

        Args:
            texts: List of text strings to translate
            target_lang: Target language code
            source_lang: Source language code (auto-detected if None)

        Returns:
            List of translated strings
        """
        results = []
        for text in texts:
            translated = self.translate_text(text, target_lang, source_lang)
            results.append(translated)
        return results


def main():
    """CLI interface for the translation tool"""
    import argparse

    parser = argparse.ArgumentParser(description="Translation Tool by ETHPanda")
    parser.add_argument("command", choices=["translate", "detect", "translate-code", "batch"],
                       help="Command to execute")
    parser.add_argument("--text", help="Text to translate")
    parser.add_argument("--code", help="Code with comments to translate")
    parser.add_argument("--target", "-t", help="Target language code")
    parser.add_argument("--source", "-s", help="Source language code (optional)")
    parser.add_argument("--provider", "-p", default="google",
                       help="Translation provider (google, deepl)")
    parser.add_argument("--batch", nargs="+", help="Multiple texts to translate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Initialize translator
    tool = TranslationTool(provider=args.provider)

    # Execute command
    if args.command == "translate":
        if not args.text or not args.target:
            print("Error: --text and --target are required", file=sys.stderr)
            sys.exit(1)

        result = tool.translate_text(args.text, args.target, args.source)

        if args.json:
            print(json.dumps({"translation": result}))
        else:
            print(result)

    elif args.command == "detect":
        if not args.text:
            print("Error: --text is required", file=sys.stderr)
            sys.exit(1)

        result = tool.detect_language(args.text)

        if args.json:
            print(json.dumps(result))
        else:
            print(f"Language: {result.get('language', 'unknown')}")
            print(f"Confidence: {result.get('confidence', 0):.2%}")

    elif args.command == "translate-code":
        if not args.code or not args.target:
            print("Error: --code and --target are required", file=sys.stderr)
            sys.exit(1)

        result = tool.translate_code_comments(args.code, args.target, args.source)

        if args.json:
            print(json.dumps({"code": result}))
        else:
            print(result)

    elif args.command == "batch":
        if not args.batch or not args.target:
            print("Error: --batch and --target are required", file=sys.stderr)
            sys.exit(1)

        results = tool.batch_translate(args.batch, args.target, args.source)

        if args.json:
            print(json.dumps({"translations": results}))
        else:
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")


if __name__ == "__main__":
    main()
