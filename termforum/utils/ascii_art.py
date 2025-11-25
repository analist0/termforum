"""ASCII Art utilities for TermForum"""

import pyfiglet
from art import text2art, art
from typing import Optional, List
from PIL import Image
import io


def create_banner(text: str, font: str = "slant") -> str:
    """
    Create ASCII banner from text

    Args:
        text: Text to convert
        font: Font name (slant, banner, big, block, etc.)

    Returns:
        ASCII banner string
    """
    try:
        return pyfiglet.figlet_format(text, font=font)
    except Exception:
        # Fallback to default font
        return pyfiglet.figlet_format(text)


def create_art(text: str, art_type: str = "random") -> str:
    """
    Create decorative ASCII art from text

    Args:
        text: Text to convert
        art_type: Art style (random, block, graffiti, etc.)

    Returns:
        ASCII art string
    """
    try:
        return text2art(text, font=art_type)
    except Exception:
        return text2art(text)


def get_random_art(category: str = "random") -> str:
    """
    Get random ASCII art from library

    Args:
        category: Category (animals, faces, objects, etc.)

    Returns:
        ASCII art string
    """
    try:
        return art(category)
    except Exception:
        return art("random")


def list_banner_fonts() -> List[str]:
    """List available pyfiglet fonts"""
    return pyfiglet.FigletFont.getFonts()


def list_art_fonts() -> List[str]:
    """List available art fonts"""
    from art import FONT_NAMES
    return FONT_NAMES


def image_to_ascii(image_path: str, width: int = 80, height: int = None) -> str:
    """
    Convert image to ASCII art

    Args:
        image_path: Path to image file
        width: Target width in characters
        height: Target height in characters (auto if None)

    Returns:
        ASCII art representation of image
    """
    try:
        # Open image
        img = Image.open(image_path)

        # Calculate height maintaining aspect ratio
        if height is None:
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio * 0.55)  # 0.55 to account for character aspect ratio

        # Resize image
        img = img.resize((width, height))

        # Convert to grayscale
        img = img.convert('L')

        # ASCII gradient (dark to light)
        ascii_chars = '@%#*+=-:. '

        # Convert pixels to ASCII
        ascii_art = []
        pixels = img.getdata()

        for i in range(0, len(pixels), width):
            row = pixels[i:i+width]
            ascii_row = ''.join([ascii_chars[min(pixel // 25, len(ascii_chars)-1)] for pixel in row])
            ascii_art.append(ascii_row)

        return '\n'.join(ascii_art)

    except Exception as e:
        return f"Error converting image: {e}"


# Predefined ASCII art templates
ASCII_TEMPLATES = {
    "welcome": """
╔══════════════════════════════════════════════════════════════╗
║                     🗣️  TERMFORUM                           ║
║              Terminal Discussion Board                       ║
╚══════════════════════════════════════════════════════════════╝
    """,

    "divider": "─" * 80,

    "new_thread": """
┌─────────────────────────────────────────┐
│  📝  CREATE NEW THREAD                  │
└─────────────────────────────────────────┘
    """,

    "loading": """
    ⠋ Loading...
    ⠙ Loading...
    ⠹ Loading...
    ⠸ Loading...
    ⠼ Loading...
    ⠴ Loading...
    ⠦ Loading...
    ⠧ Loading...
    ⠇ Loading...
    ⠏ Loading...
    """,

    "success": """
    ✓ Success!
    """,

    "error": """
    ✗ Error!
    """,
}


def get_template(name: str) -> str:
    """Get predefined ASCII art template"""
    return ASCII_TEMPLATES.get(name, "")


# Common ASCII art elements
ICONS = {
    "thread": "📋",
    "post": "💬",
    "user": "👤",
    "category": "📁",
    "upvote": "⬆️",
    "downvote": "⬇️",
    "views": "👀",
    "pinned": "📌",
    "locked": "🔒",
    "fire": "🔥",
    "star": "⭐",
    "check": "✓",
    "cross": "✗",
    "arrow_right": "→",
    "arrow_left": "←",
    "bullet": "•",
}


def get_icon(name: str) -> str:
    """Get icon by name"""
    return ICONS.get(name, "•")
