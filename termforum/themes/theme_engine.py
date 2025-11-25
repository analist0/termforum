"""CyberPunk Theme Engine™ for TermForum

Dynamic theme system with 4 beautiful themes:
- Dark Hacker (Matrix style)
- Kali Red (Penetration testing)
- Neon Cyber (Cyberpunk 2077)
- Light Pro (Professional)

Features:
- Hot-swap themes without restart
- Gradient borders
- Glow effects
- Custom ASCII art per theme
"""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ThemeName(str, Enum):
    """Available theme names"""
    DARK_HACKER = "dark_hacker"
    KALI_RED = "kali_red"
    NEON_CYBER = "neon_cyber"
    LIGHT_PRO = "light_pro"


@dataclass
class Theme:
    """Theme configuration"""
    name: str
    display_name: str
    description: str
    icon: str

    # Core colors
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str

    # Text colors
    text: str
    text_muted: str
    text_disabled: str

    # Semantic colors
    success: str
    warning: str
    error: str
    info: str

    # UI elements
    border: str
    panel: str
    boost: str

    # Special effects
    glow: bool = False
    gradient: bool = False

    def to_css(self) -> str:
        """Convert theme to Textual CSS variables"""
        css = f"""
/* {self.display_name} Theme - {self.description} */

* {{
    /* Core colors */
    $primary: {self.primary};
    $secondary: {self.secondary};
    $accent: {self.accent};
    $background: {self.background};
    $surface: {self.surface};

    /* Text colors */
    $text: {self.text};
    $text-muted: {self.text_muted};
    $text-disabled: {self.text_disabled};

    /* Semantic colors */
    $success: {self.success};
    $success-darken-1: {self._darken(self.success)};
    $warning: {self.warning};
    $warning-darken-1: {self._darken(self.warning)};
    $error: {self.error};
    $error-darken-1: {self._darken(self.error)};
    $info: {self.info};

    /* UI elements */
    $border: {self.border};
    $panel: {self.panel};
    $boost: {self.boost};
}}
"""
        return css

    @staticmethod
    def _darken(color: str) -> str:
        """Darken a color (simplified for terminal colors)"""
        # Terminal color darkening mapping
        darken_map = {
            "green": "darkgreen",
            "red": "darkred",
            "blue": "darkblue",
            "cyan": "darkcyan",
            "magenta": "darkmagenta",
            "yellow": "darkyellow",
        }
        return darken_map.get(color, color)


# ═══════════════════════════════════════════════════════════════════
# Theme Definitions
# ═══════════════════════════════════════════════════════════════════

DARK_HACKER = Theme(
    name=ThemeName.DARK_HACKER,
    display_name="🌑 Dark Hacker",
    description="Matrix style - Black & Green terminal hacker aesthetic",
    icon="🌑",

    # Core colors - Matrix green on black
    primary="green",
    secondary="darkgreen",
    accent="lime",
    background="black",
    surface="#0a0f0a",

    # Text - Green terminal text
    text="lime",
    text_muted="green",
    text_disabled="darkgreen",

    # Semantic
    success="lime",
    warning="yellow",
    error="red",
    info="cyan",

    # UI
    border="green",
    panel="#0f1f0f",
    boost="#1a3f1a",

    glow=True,
    gradient=False
)

KALI_RED = Theme(
    name=ThemeName.KALI_RED,
    display_name="🎯 Kali Red",
    description="Penetration testing - Black & Red (Kali Linux inspired)",
    icon="🎯",

    # Core colors - Kali red on black
    primary="red",
    secondary="darkred",
    accent="#ff0040",
    background="black",
    surface="#0f0505",

    # Text - Red/White terminal
    text="white",
    text_muted="#ff6666",
    text_disabled="darkred",

    # Semantic
    success="lime",
    warning="yellow",
    error="red",
    info="cyan",

    # UI
    border="red",
    panel="#1f0505",
    boost="#3f0a0a",

    glow=True,
    gradient=False
)

NEON_CYBER = Theme(
    name=ThemeName.NEON_CYBER,
    display_name="🌈 Neon Cyber",
    description="Cyberpunk 2077 - Purple, Cyan & Pink neon glow",
    icon="🌈",

    # Core colors - Cyberpunk neon
    primary="magenta",
    secondary="purple",
    accent="cyan",
    background="#0a0014",
    surface="#14001e",

    # Text - Neon colors
    text="cyan",
    text_muted="magenta",
    text_disabled="purple",

    # Semantic
    success="lime",
    warning="#ffaa00",
    error="#ff0066",
    info="cyan",

    # UI
    border="magenta",
    panel="#1e0028",
    boost="#280a3c",

    glow=True,
    gradient=True
)

LIGHT_PRO = Theme(
    name=ThemeName.LIGHT_PRO,
    display_name="☀️ Light Pro",
    description="Professional - Clean white/blue for readability",
    icon="☀️",

    # Core colors - Professional light
    primary="blue",
    secondary="darkblue",
    accent="cyan",
    background="white",
    surface="#f5f5f5",

    # Text - Dark on light
    text="black",
    text_muted="#666666",
    text_disabled="#999999",

    # Semantic
    success="green",
    warning="#ff9900",
    error="red",
    info="blue",

    # UI
    border="blue",
    panel="#e0e0e0",
    boost="#d0d0ff",

    glow=False,
    gradient=False
)


# Theme registry
THEMES: Dict[str, Theme] = {
    ThemeName.DARK_HACKER: DARK_HACKER,
    ThemeName.KALI_RED: KALI_RED,
    ThemeName.NEON_CYBER: NEON_CYBER,
    ThemeName.LIGHT_PRO: LIGHT_PRO,
}


class ThemeEngine:
    """
    Theme management system

    Handles theme switching, persistence, and CSS generation
    """

    def __init__(self, default_theme: str = ThemeName.DARK_HACKER):
        """
        Initialize theme engine

        Args:
            default_theme: Default theme name
        """
        self.current_theme_name = default_theme
        self.current_theme = THEMES.get(default_theme, DARK_HACKER)

    def set_theme(self, theme_name: str) -> Theme:
        """
        Set current theme

        Args:
            theme_name: Theme name from ThemeName enum

        Returns:
            The activated theme
        """
        if theme_name not in THEMES:
            raise ValueError(f"Unknown theme: {theme_name}")

        self.current_theme_name = theme_name
        self.current_theme = THEMES[theme_name]
        return self.current_theme

    def get_theme(self, theme_name: str = None) -> Theme:
        """Get theme by name, or current theme if name is None"""
        if theme_name is None:
            return self.current_theme
        return THEMES.get(theme_name, self.current_theme)

    def list_themes(self) -> list[Theme]:
        """Get list of all available themes"""
        return list(THEMES.values())

    def get_css(self, theme_name: str = None) -> str:
        """Get CSS for a theme"""
        theme = self.get_theme(theme_name)
        return theme.to_css()

    def cycle_theme(self) -> Theme:
        """Cycle to next theme in list"""
        theme_names = list(THEMES.keys())
        current_index = theme_names.index(self.current_theme_name)
        next_index = (current_index + 1) % len(theme_names)
        next_theme_name = theme_names[next_index]
        return self.set_theme(next_theme_name)

    def get_theme_splash(self, theme_name: str = None) -> str:
        """Get ASCII art splash screen for theme"""
        theme = self.get_theme(theme_name)

        if theme.name == ThemeName.DARK_HACKER:
            return """
╔═══════════════════════════════════════════════════════════════╗
║ > SYSTEM ACCESS GRANTED                                       ║
║ > LOADING DARK HACKER MATRIX PROTOCOL...                      ║
║                                                                ║
║   ▓▓▓▓▓▓▓▓  MATRIX  MODE  ACTIVATED  ▓▓▓▓▓▓▓▓               ║
║                                                                ║
║   🌑 "In the matrix, anything is possible"                    ║
╚═══════════════════════════════════════════════════════════════╝
"""
        elif theme.name == ThemeName.KALI_RED:
            return """
╔═══════════════════════════════════════════════════════════════╗
║ ⚠️  KALI RED PENETRATION MODE ACTIVATED  ⚠️                   ║
║                                                                ║
║   ▓▓▓▓▓▓▓▓  SECURITY  RESEARCH  MODE  ▓▓▓▓▓▓▓▓              ║
║                                                                ║
║   🎯 "The quieter you become, the more you can hear"          ║
╚═══════════════════════════════════════════════════════════════╝
"""
        elif theme.name == ThemeName.NEON_CYBER:
            return """
╔═══════════════════════════════════════════════════════════════╗
║ ⚡ NEON CYBERPUNK INTERFACE ONLINE ⚡                          ║
║                                                                ║
║   ▓▓▓▓▓▓▓▓  CYBER  NEURAL  LINK  ▓▓▓▓▓▓▓▓                   ║
║                                                                ║
║   🌈 "In 2077, what makes someone a criminal?"                ║
╚═══════════════════════════════════════════════════════════════╝
"""
        else:  # LIGHT_PRO
            return """
╔═══════════════════════════════════════════════════════════════╗
║ ☀️  PROFESSIONAL MODE - MAXIMUM READABILITY                   ║
║                                                                ║
║   ▓▓▓▓▓▓▓▓  CLEAN  INTERFACE  MODE  ▓▓▓▓▓▓▓▓                ║
║                                                                ║
║   📋 "Simplicity is the ultimate sophistication"              ║
╚═══════════════════════════════════════════════════════════════╝
"""
