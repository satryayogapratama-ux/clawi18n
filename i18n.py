#!/usr/bin/env python3
"""
ClawI18n - Internationalization Framework for OpenClaw
Provides translation, locale detection, and language switching capabilities.
"""

import json
import os
import re
from pathlib import Path
from string import Template
from typing import Dict, Optional, List

# Locales below this completion threshold are served as English fallback
# to avoid shipping half-translated UIs.
PARTIAL_LOCALE_THRESHOLD = 0.80  # 80%


class I18n:
    """Translation engine with locale detection and variable substitution."""
    
    # Language detection keywords for common locales
    LOCALE_KEYWORDS = {
        'id': [
            'yang', 'dengan', 'ini', 'adalah', 'untuk', 'dari', 'ke', 'di',
            'saya', 'anda', 'dia', 'kami', 'mereka', 'telah', 'sudah'
        ],
        'zh': [
            '的', '一', '是', '在', '不', '了', '有', '和', '人', '这',
            '中', '大', '为', '上', '个', '国', '我', '以', '要', '他'
        ],
        'th': [
            'ที่', 'ได้', 'จาก', 'ใหม่', 'ว่า', 'นี้', 'โดย', 'ใหญ่',
            'ความ', 'ของ', 'กับ', 'เพื่อ', 'ไป', 'มา', 'เป็น'
        ],
        'ms': [
            'yang', 'dengan', 'di', 'ke', 'dari', 'untuk', 'adalah',
            'saya', 'anda', 'dia', 'kami', 'mereka', 'telah', 'sudah'
        ],
        'vi': [
            'của', 'trong', 'và', 'là', 'cái', 'này', 'có', 'được',
            'từ', 'đến', 'tôi', 'bạn', 'nó', 'chúng', 'tôi'
        ]
    }
    
    def __init__(self, locales_dir: str = None, default_locale: str = 'en'):
        """
        Initialize the I18n engine.
        
        Args:
            locales_dir: Path to locales directory (defaults to current directory)
            default_locale: Default locale code (defaults to 'en')
        """
        if locales_dir is None:
            # Try to find locales relative to this script
            script_dir = Path(__file__).parent
            locales_dir = script_dir / 'locales'
        
        self.locales_dir = Path(locales_dir)
        self.default_locale = default_locale
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_all_locales()
    
    def _load_all_locales(self) -> None:
        """Load all available translation files."""
        if not self.locales_dir.exists():
            raise FileNotFoundError(f"Locales directory not found: {self.locales_dir}")
        
        for json_file in self.locales_dir.glob('*.json'):
            locale_code = json_file.stem
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self._translations[locale_code] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load locale {locale_code}: {e}")
    
    def load_locale(self, lang_code: str) -> bool:
        """
        Load a specific locale's translation file.
        
        Args:
            lang_code: Language code (e.g., 'id', 'zh', 'th')
        
        Returns:
            True if loaded successfully, False otherwise
        """
        locale_file = self.locales_dir / f'{lang_code}.json'
        
        if not locale_file.exists():
            return False
        
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                self._translations[lang_code] = json.load(f)
            return True
        except (json.JSONDecodeError, IOError):
            return False
    
    def t(self, key: str, locale: str = None, **kwargs) -> str:
        """
        Translate a key to the specified locale with variable substitution.
        
        Args:
            key: Translation key (e.g., 'memory.search')
            locale: Target locale (uses default if not specified)
            **kwargs: Variables for substitution (e.g., count=5)
        
        Returns:
            Translated string with substituted variables, or the key if not found
        """
        if locale is None:
            locale = self.default_locale

        # Fall back to default locale for partial/incomplete translations
        if locale != self.default_locale and self._is_partial_locale(locale):
            locale = self.default_locale

        # Get translation from specified locale, fallback to default, then key
        translations = self._translations.get(locale, {})
        translation = translations.get(key)
        
        if translation is None and locale != self.default_locale:
            translations = self._translations.get(self.default_locale, {})
            translation = translations.get(key, key)
        
        if translation is None:
            translation = key
        
        # Safe variable substitution — no KeyError, no format-string injection
        if kwargs:
            safe_kwargs = {k: str(v) for k, v in kwargs.items()}
            try:
                translation = Template(translation).safe_substitute(**safe_kwargs)
            except Exception:
                pass  # Return unsubstituted string rather than crash

        return translation
    
    def _is_partial_locale(self, locale: str) -> bool:
        """Return True if locale completion is below the threshold."""
        en_keys = set(self._translations.get(self.default_locale, {}).keys())
        if not en_keys:
            return False
        locale_keys = set(self._translations.get(locale, {}).keys())
        completion = len(locale_keys & en_keys) / len(en_keys)
        return completion < PARTIAL_LOCALE_THRESHOLD

    def detect_locale(self, text: str) -> Optional[str]:
        """
        Detect language from input text using keyword matching.
        
        Args:
            text: Input text to analyze
        
        Returns:
            Detected locale code, or None if detection fails
        """
        if not text or len(text) < 5:
            return None
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Score each locale based on keyword matches
        scores: Dict[str, int] = {}
        
        for locale, keywords in self.LOCALE_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[locale] = score
        
        # Return locale with highest score
        if scores:
            return max(scores, key=scores.get)
        
        return None
    
    def get_supported_locales(self) -> List[str]:
        """
        Get list of supported locale codes.
        
        Returns:
            List of available locale codes
        """
        return sorted(list(self._translations.keys()))
    
    def get_completion_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get translation completion statistics for each locale.
        
        Returns:
            Dictionary with locale stats including translated/total keys
        """
        if not self._translations:
            return {}
        
        # Use English as reference for total keys
        en_keys = set(self._translations.get('en', {}).keys())
        total_keys = len(en_keys)
        
        stats = {}
        for locale, translations in self._translations.items():
            translated_keys = len(set(translations.keys()) & en_keys)
            completion_pct = (translated_keys / total_keys * 100) if total_keys > 0 else 0
            
            stats[locale] = {
                'translated': translated_keys,
                'total': total_keys,
                'completion': round(completion_pct, 1)
            }
        
        return stats


# Module-level convenience functions
_default_i18n: Optional[I18n] = None


def init(locales_dir: str = None, default_locale: str = 'en') -> I18n:
    """Initialize the default I18n instance."""
    global _default_i18n
    _default_i18n = I18n(locales_dir, default_locale)
    return _default_i18n


def t(key: str, locale: str = None, **kwargs) -> str:
    """Translate using the default I18n instance."""
    if _default_i18n is None:
        init()
    return _default_i18n.t(key, locale, **kwargs)


def detect_locale(text: str) -> Optional[str]:
    """Detect locale using the default I18n instance."""
    if _default_i18n is None:
        init()
    return _default_i18n.detect_locale(text)


def get_supported_locales() -> List[str]:
    """Get supported locales from the default I18n instance."""
    if _default_i18n is None:
        init()
    return _default_i18n.get_supported_locales()


if __name__ == '__main__':
    # Example usage
    i18n = I18n()
    
    print("Supported locales:", i18n.get_supported_locales())
    print("\nCompletion stats:")
    for locale, stats in i18n.get_completion_stats().items():
        print(f"  {locale}: {stats['translated']}/{stats['total']} ({stats['completion']}%)")
    
    print("\nSample translations:")
    for locale in i18n.get_supported_locales():
        print(f"\n{locale}:")
        print(f"  'memory.search' = {i18n.t('memory.search', locale)}")
        print(f"  'error.generic' = {i18n.t('error.generic', locale)}")
    
    print("\nVariable substitution example:")
    for locale in ['en', 'id', 'zh']:
        print(f"  {locale}: {i18n.t('memory.found', locale, count=5)}")
    
    print("\nLocale detection example:")
    test_texts = [
        "Mencari memori dengan cepat",
        "正在加载中...",
        "Searching for something"
    ]
    for text in test_texts:
        detected = i18n.detect_locale(text)
        print(f"  '{text}' => {detected}")
