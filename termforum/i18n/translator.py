"""Translation engine for TermForum

Supports multiple languages with JSON-based translation files.
Contributors can easily add new languages by creating language files.
"""

import json
import locale
import os
from pathlib import Path
from typing import Dict, Optional


class Translator:
    """Translation engine for TermForum"""

    def __init__(self, language: Optional[str] = None):
        """Initialize translator

        Args:
            language: Language code (e.g., 'en', 'he'). Auto-detects if None.
        """
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_language = language or self._detect_system_language()
        self.fallback_language = "en"
        self._load_translations()

    def _detect_system_language(self) -> str:
        """Detect system language from locale"""
        try:
            # Get system locale
            system_locale, _ = locale.getdefaultlocale()
            if system_locale:
                # Extract language code (e.g., 'en_US' -> 'en', 'he_IL' -> 'he')
                lang_code = system_locale.split('_')[0].lower()
                return lang_code if lang_code in ['en', 'he'] else 'en'
        except Exception:
            pass
        return 'en'  # Default to English

    def _load_translations(self) -> None:
        """Load translation files"""
        i18n_dir = Path(__file__).parent

        # Load all available language files
        for lang_file in i18n_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load {lang_file}: {e}")

    def t(self, key: str, **kwargs) -> str:
        """Translate a key to current language

        Args:
            key: Translation key (dot-separated path, e.g., 'home.welcome')
            **kwargs: Variables to format into the translation string

        Returns:
            Translated string

        Examples:
            >>> t('home.welcome')
            'Welcome to TermForum!'
            >>> t('post.count', count=5)
            '5 posts'
        """
        # Try current language
        value = self._get_translation(key, self.current_language)

        # Fallback to English if not found
        if value == key and self.current_language != self.fallback_language:
            value = self._get_translation(key, self.fallback_language)

        # Format with variables if provided
        if kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass

        return value

    def _get_translation(self, key: str, lang: str) -> str:
        """Get translation from a specific language

        Args:
            key: Translation key (dot-separated)
            lang: Language code

        Returns:
            Translated string or key if not found
        """
        if lang not in self.translations:
            return key

        # Navigate through nested dict using dot-separated key
        parts = key.split('.')
        value = self.translations[lang]

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return key  # Key not found

        return value if isinstance(value, str) else key

    def set_language(self, language: str) -> bool:
        """Set current language

        Args:
            language: Language code (e.g., 'en', 'he')

        Returns:
            True if language was set successfully, False if not available
        """
        if language in self.translations:
            self.current_language = language
            return True
        return False

    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages

        Returns:
            Dict of language codes to native names

        Example:
            {'en': 'English', 'he': 'עברית'}
        """
        languages = {}
        for lang_code in self.translations.keys():
            # Get language name from its own translation file
            lang_name = self.translations[lang_code].get('meta', {}).get('name', lang_code)
            languages[lang_code] = lang_name
        return languages

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language


# Global translator instance
_translator: Optional[Translator] = None


def get_translator() -> Translator:
    """Get global translator instance

    Returns:
        Global Translator instance
    """
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def set_language(language: str) -> bool:
    """Set global language

    Args:
        language: Language code (e.g., 'en', 'he')

    Returns:
        True if language was set successfully
    """
    translator = get_translator()
    return translator.set_language(language)


# Convenience function for translations
def t(key: str, **kwargs) -> str:
    """Translate a key using global translator

    Args:
        key: Translation key
        **kwargs: Format variables

    Returns:
        Translated string
    """
    translator = get_translator()
    return translator.t(key, **kwargs)
