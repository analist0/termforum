"""Configuration Manager for TermForum

Manages user preferences and application settings.
Settings are stored in ~/.termforum/config.json
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        "language": None,  # None = auto-detect
        "theme": "dark",
        "vim_mode": True,
        "auto_save_drafts": True,
        "notifications_enabled": True,
        "glow_style": "dark",
        "show_avatars": True,
        "show_icons": True,
        "compact_view": False,
        "markdown_preview": True,
        "ai_enabled": True,
        "ai_model": "qwen2.5-coder:7b",
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager

        Args:
            config_path: Path to config file. Defaults to ~/.termforum/config.json
        """
        if config_path is None:
            config_dir = Path.home() / ".termforum"
            config_dir.mkdir(exist_ok=True)
            self.config_path = config_dir / "config.json"
        else:
            self.config_path = config_path

        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file

        Returns:
            Configuration dict
        """
        if not self.config_path.exists():
            # Create default config
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # Merge with defaults (in case new settings were added)
            config = self.DEFAULT_CONFIG.copy()
            config.update(loaded_config)
            return config
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
            return self.DEFAULT_CONFIG.copy()

    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file

        Args:
            config: Configuration dict to save
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error: Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any, save: bool = True) -> None:
        """Set configuration value

        Args:
            key: Configuration key
            value: Value to set
            save: Whether to save to file immediately
        """
        self.config[key] = value
        if save:
            self._save_config(self.config)

    def update(self, updates: Dict[str, Any], save: bool = True) -> None:
        """Update multiple configuration values

        Args:
            updates: Dict of key-value pairs to update
            save: Whether to save to file immediately
        """
        self.config.update(updates)
        if save:
            self._save_config(self.config)

    def reset(self) -> None:
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)

    def get_language(self) -> Optional[str]:
        """Get configured language

        Returns:
            Language code (e.g., 'en', 'he') or None for auto-detect
        """
        return self.config.get("language")

    def set_language(self, language: str) -> None:
        """Set language preference

        Args:
            language: Language code (e.g., 'en', 'he')
        """
        self.set("language", language)

    def get_theme(self) -> str:
        """Get theme name

        Returns:
            Theme name (e.g., 'dark', 'light', 'kali')
        """
        return self.config.get("theme", "dark")

    def set_theme(self, theme: str) -> None:
        """Set theme preference

        Args:
            theme: Theme name
        """
        self.set("theme", theme)


# Global config instance
_config: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global configuration manager instance

    Returns:
        Global ConfigManager instance
    """
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config
