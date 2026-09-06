"""
Translation Tool Package
Created by ETHPanda for SpoonOS AI-Enhanced Productivity Challenge
"""

__version__ = "1.0.0"
__author__ = "ETHPanda"
__description__ = "Multi-language translation tool for SpoonOS"

from .translate import TranslationTool, TranslationProvider

__all__ = ["TranslationTool", "TranslationProvider"]
