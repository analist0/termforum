"""AI command parser for TermForum"""

import re
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class AICommand:
    """Represents a parsed AI command"""
    command_type: str  # 'mention', 'summarize', 'ascii', 'translate', 'help'
    content: str
    original_text: str


class AICommandParser:
    """Parse AI commands from forum posts"""

    # Command patterns
    MENTION_PATTERN = r'@ai\s+(.+)'
    SUMMARIZE_PATTERN = r'/summarize'
    ASCII_PATTERN = r'/ascii\s+(.+)'
    TRANSLATE_PATTERN = r'/translate\s+(.+)'
    HELP_PATTERN = r'/help'

    @staticmethod
    def parse(text: str) -> Optional[AICommand]:
        """
        Parse text for AI commands

        Args:
            text: Post content

        Returns:
            AICommand if found, None otherwise
        """
        text = text.strip()

        # Check for @ai mention
        match = re.search(AICommandParser.MENTION_PATTERN, text, re.IGNORECASE)
        if match:
            return AICommand(
                command_type='mention',
                content=match.group(1).strip(),
                original_text=text
            )

        # Check for /summarize
        if re.search(AICommandParser.SUMMARIZE_PATTERN, text, re.IGNORECASE):
            return AICommand(
                command_type='summarize',
                content='',
                original_text=text
            )

        # Check for /ascii
        match = re.search(AICommandParser.ASCII_PATTERN, text, re.IGNORECASE)
        if match:
            return AICommand(
                command_type='ascii',
                content=match.group(1).strip(),
                original_text=text
            )

        # Check for /translate
        match = re.search(AICommandParser.TRANSLATE_PATTERN, text, re.IGNORECASE)
        if match:
            return AICommand(
                command_type='translate',
                content=match.group(1).strip(),
                original_text=text
            )

        # Check for /help
        if re.search(AICommandParser.HELP_PATTERN, text, re.IGNORECASE):
            return AICommand(
                command_type='help',
                content='',
                original_text=text
            )

        return None

    @staticmethod
    def contains_ai_command(text: str) -> bool:
        """Check if text contains any AI command"""
        return AICommandParser.parse(text) is not None

    @staticmethod
    def extract_all_commands(text: str) -> list[AICommand]:
        """Extract all AI commands from text (supports multiple)"""
        commands = []

        # Split by lines and check each
        lines = text.split('\n')
        for line in lines:
            cmd = AICommandParser.parse(line)
            if cmd:
                commands.append(cmd)

        return commands
