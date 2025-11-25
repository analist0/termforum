"""Session Management System for TermForum

Handles user sessions, remember-me tokens, and login persistence.
"""

import json
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass, asdict


@dataclass
class Session:
    """Represents a user session"""
    user_id: int
    username: str
    token: str
    created_at: str
    expires_at: str
    remember_me: bool = False

    def is_expired(self) -> bool:
        """Check if session has expired"""
        expires = datetime.fromisoformat(self.expires_at)
        return datetime.now() > expires

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Create from dictionary"""
        return cls(**data)


class SessionManager:
    """Manages user sessions and authentication tokens"""

    def __init__(self, session_file: Optional[Path] = None):
        """
        Initialize session manager

        Args:
            session_file: Path to session storage file (default: ~/.termforum/session.json)
        """
        if session_file is None:
            session_file = Path.home() / ".termforum" / "session.json"

        self.session_file = Path(session_file)
        self.session_file.parent.mkdir(parents=True, exist_ok=True)

    def create_session(
        self,
        user_id: int,
        username: str,
        remember_me: bool = False,
        duration_hours: int = 24
    ) -> Session:
        """
        Create a new session for user

        Args:
            user_id: User ID
            username: Username
            remember_me: If True, session lasts 30 days instead of 24 hours
            duration_hours: Session duration in hours (default: 24)

        Returns:
            New Session object
        """
        # Generate secure random token
        token = secrets.token_urlsafe(32)

        # Calculate expiration
        if remember_me:
            duration = timedelta(days=30)
        else:
            duration = timedelta(hours=duration_hours)

        now = datetime.now()
        expires_at = now + duration

        session = Session(
            user_id=user_id,
            username=username,
            token=token,
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            remember_me=remember_me
        )

        # Save session
        self._save_session(session)

        return session

    def get_session(self) -> Optional[Session]:
        """
        Get current session if it exists and is valid

        Returns:
            Session object if valid, None otherwise
        """
        if not self.session_file.exists():
            return None

        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)

            session = Session.from_dict(data)

            # Check if expired
            if session.is_expired():
                self.clear_session()
                return None

            return session

        except Exception:
            return None

    def clear_session(self) -> None:
        """Clear current session (logout)"""
        if self.session_file.exists():
            self.session_file.unlink()

    def _save_session(self, session: Session) -> None:
        """Save session to file"""
        with open(self.session_file, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)

    def get_all_sessions_info(self) -> Dict[str, any]:
        """
        Get information about all sessions (for debugging/admin)

        Returns:
            Dictionary with session info
        """
        session = self.get_session()

        if not session:
            return {
                "active": False,
                "session_file": str(self.session_file),
                "exists": self.session_file.exists()
            }

        return {
            "active": True,
            "username": session.username,
            "user_id": session.user_id,
            "created_at": session.created_at,
            "expires_at": session.expires_at,
            "remember_me": session.remember_me,
            "is_expired": session.is_expired()
        }
