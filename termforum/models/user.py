"""User model"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a forum user"""

    id: int
    username: str
    email: Optional[str] = None
    password_hash: Optional[str] = None  # PolyCrypt hash
    bio: Optional[str] = None
    avatar: str = "👤"
    created_at: datetime = None
    updated_at: datetime = None
    posts_count: int = 0
    threads_count: int = 0
    reputation: int = 0
    is_admin: bool = False
    is_banned: bool = False
    last_seen: datetime = None
    # Security fields
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None

    def __post_init__(self):
        """Set default timestamps"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.last_seen is None:
            self.last_seen = datetime.now()

    @property
    def display_name(self) -> str:
        """Get display name with avatar"""
        return f"{self.avatar} {self.username}"

    @property
    def total_activity(self) -> int:
        """Total posts + threads"""
        return self.posts_count + self.threads_count

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "bio": self.bio,
            "avatar": self.avatar,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "posts_count": self.posts_count,
            "threads_count": self.threads_count,
            "reputation": self.reputation,
            "is_admin": self.is_admin,
            "is_banned": self.is_banned,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "failed_login_attempts": self.failed_login_attempts,
            "account_locked_until": self.account_locked_until.isoformat() if self.account_locked_until else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create from dictionary"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if "last_seen" in data and isinstance(data["last_seen"], str):
            data["last_seen"] = datetime.fromisoformat(data["last_seen"])
        if "account_locked_until" in data and isinstance(data["account_locked_until"], str):
            data["account_locked_until"] = datetime.fromisoformat(data["account_locked_until"])
        return cls(**data)

    def __str__(self) -> str:
        return f"User({self.username}, posts={self.posts_count}, rep={self.reputation})"

    def __repr__(self) -> str:
        return self.__str__()
