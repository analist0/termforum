"""AI Bot for TermForum using Ollama"""

from typing import Optional, List
from ..storage import Database
from ..models import User, Thread, Post
from .ollama_client import OllamaClient
from .commands import AICommandParser, AICommand
from .prompts import (
    FORUM_ASSISTANT_PROMPT,
    SUMMARIZE_PROMPT,
    ASCII_ART_PROMPT,
    TRANSLATE_PROMPT,
    HELP_TEXT,
    AI_BOT_BIO,
    ERROR_OLLAMA_NOT_RUNNING,
    ERROR_NO_MODELS,
    ERROR_GENERATION_FAILED,
)


class AIBot:
    """AI-powered bot for TermForum"""

    def __init__(
        self,
        database: Database,
        ollama_url: str = "http://localhost:11434",
        model: str = "qwen2.5-coder:7b",
        auto_create_user: bool = True
    ):
        """
        Initialize AI Bot

        Args:
            database: Forum database
            ollama_url: Ollama API URL
            model: Model name to use
            auto_create_user: Create bot user if not exists
        """
        self.db = database
        self.client = OllamaClient(ollama_url)
        self.model = model
        self.bot_user = None

        if auto_create_user:
            self._ensure_bot_user()

    def _ensure_bot_user(self) -> None:
        """Ensure AI bot user exists"""
        bot = self.db.get_user_by_username("ai-bot")
        if not bot:
            bot = self.db.create_user(
                username="ai-bot",
                bio=AI_BOT_BIO,
                avatar="🤖"
            )
        self.bot_user = bot

    def is_available(self) -> bool:
        """Check if AI bot is available"""
        return self.client.is_available()

    def get_status(self) -> dict:
        """Get bot status"""
        available = self.is_available()
        models = self.client.list_models() if available else []

        return {
            "available": available,
            "models": models,
            "current_model": self.model,
            "bot_user_id": self.bot_user.id if self.bot_user else None,
        }

    def handle_command(
        self,
        command: AICommand,
        thread: Thread,
        context_posts: Optional[List[Post]] = None
    ) -> str:
        """
        Handle AI command and generate response

        Args:
            command: Parsed AI command
            thread: Thread where command was issued
            context_posts: Recent posts for context

        Returns:
            AI-generated response
        """
        if not self.is_available():
            return ERROR_OLLAMA_NOT_RUNNING

        models = self.client.list_models()
        if not models:
            return ERROR_NO_MODELS

        # Ensure model is available
        if self.model not in models:
            # Use first available model
            self.model = models[0]

        # Handle different command types
        if command.command_type == 'mention':
            return self._handle_mention(command.content, thread, context_posts)

        elif command.command_type == 'summarize':
            return self._handle_summarize(thread, context_posts)

        elif command.command_type == 'ascii':
            return self._handle_ascii(command.content)

        elif command.command_type == 'translate':
            return self._handle_translate(command.content)

        elif command.command_type == 'help':
            return HELP_TEXT

        return "Unknown command"

    def _handle_mention(
        self,
        question: str,
        thread: Thread,
        context_posts: Optional[List[Post]]
    ) -> str:
        """Handle @ai mention"""
        # Build context from thread
        context = f"Thread: {thread.title}\n\n"
        if context_posts:
            context += "Recent discussion:\n"
            for post in context_posts[-5:]:  # Last 5 posts
                context += f"- {post.content[:100]}...\n"
            context += "\n"

        context += f"User question: {question}"

        # Generate response
        response = self.client.generate(
            model=self.model,
            prompt=context,
            system=FORUM_ASSISTANT_PROMPT,
            temperature=0.7,
            max_tokens=500
        )

        if response.startswith("Error:"):
            return ERROR_GENERATION_FAILED

        return response

    def _handle_summarize(
        self,
        thread: Thread,
        context_posts: Optional[List[Post]]
    ) -> str:
        """Handle /summarize command"""
        if not context_posts:
            return "No posts to summarize."

        # Build discussion text
        discussion = f"Thread: {thread.title}\n\n"
        discussion += f"First post: {thread.content}\n\n"
        discussion += "Discussion:\n"
        for post in context_posts:
            discussion += f"- {post.content}\n"

        # Generate summary
        response = self.client.generate(
            model=self.model,
            prompt=discussion,
            system=SUMMARIZE_PROMPT,
            temperature=0.5,
            max_tokens=300
        )

        if response.startswith("Error:"):
            return ERROR_GENERATION_FAILED

        return f"## 📝 Thread Summary\n\n{response}"

    def _handle_ascii(self, description: str) -> str:
        """Handle /ascii command"""
        prompt = ASCII_ART_PROMPT.format(request=description)

        response = self.client.generate(
            model=self.model,
            prompt=description,
            system=prompt,
            temperature=0.8,
            max_tokens=300
        )

        if response.startswith("Error:"):
            return ERROR_GENERATION_FAILED

        return f"```\n{response}\n```"

    def _handle_translate(self, text: str) -> str:
        """Handle /translate command"""
        prompt = f"{TRANSLATE_PROMPT}\n\nText: {text}"

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            system="You are a translator. Translate accurately.",
            temperature=0.3,
            max_tokens=500
        )

        if response.startswith("Error:"):
            return ERROR_GENERATION_FAILED

        return response

    def auto_reply(
        self,
        post: Post,
        thread: Thread,
        context_posts: List[Post]
    ) -> Optional[Post]:
        """
        Auto-reply to post if it contains AI command

        Args:
            post: Post to check
            thread: Thread containing post
            context_posts: Context for AI

        Returns:
            Created reply post or None
        """
        command = AICommandParser.parse(post.content)
        if not command:
            return None

        # Generate response
        response = self.handle_command(command, thread, context_posts)

        # Create reply
        reply = self.db.create_post(
            thread_id=thread.id,
            user_id=self.bot_user.id,
            content=response,
            parent_post_id=post.id
        )

        return reply
