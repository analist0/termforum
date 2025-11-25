"""Glow integration for beautiful markdown rendering"""

import subprocess
import shutil
from typing import Optional


def glow_available() -> bool:
    """Check if Glow is installed"""
    return shutil.which("glow") is not None


def render_markdown(content: str, width: int = 80, style: str = "dark") -> str:
    """
    Render markdown content using Glow

    Args:
        content: Markdown content to render
        width: Terminal width for wrapping
        style: Glow style (dark, light, notty)

    Returns:
        Rendered markdown or plain text if Glow unavailable
    """
    if not glow_available():
        # Fallback to plain text if Glow not available
        return content

    try:
        # Run Glow with stdin
        result = subprocess.run(
            ["glow", "-s", style, "-w", str(width)],
            input=content,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return result.stdout
        else:
            # Fallback to plain text on error
            return content

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fallback to plain text on any error
        return content


def render_markdown_to_file(content: str, output_path: str, style: str = "dark") -> bool:
    """
    Render markdown to HTML file using Glow

    Args:
        content: Markdown content
        output_path: Path to save HTML file
        style: Glow style

    Returns:
        True if successful, False otherwise
    """
    if not glow_available():
        return False

    try:
        with open(output_path, "w") as f:
            result = subprocess.run(
                ["glow", "-s", style],
                input=content,
                stdout=f,
                text=True,
                timeout=5
            )
        return result.returncode == 0

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        return False
