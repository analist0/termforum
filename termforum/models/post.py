"""Post model"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    """Represents a forum post (reply)"""

    id: int
    thread_id: int
    user_id: int
    content: str
    parent_post_id: Optional[int] = None
    created_at: datetime = None
    updated_at: datetime = None
    upvotes: int = 0
    downvotes: int = 0
    is_deleted: bool = False
    is_edited: bool = False
    edit_reason: Optional[str] = None

    # Additional fields (populated by joins)
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    user_reputation: Optional[int] = None

    def __post_init__(self):
        """Set timestamps"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    @property
    def score(self) -> int:
        """Net vote score"""
        return self.upvotes - self.downvotes

    @property
    def is_reply(self) -> bool:
        """Check if this is a reply to another post"""
        return self.parent_post_id is not None

    @property
    def display_content(self) -> str:
        """Content with deleted indicator"""
        if self.is_deleted:
            return "*[This post has been deleted]*"
        return self.content

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "user_id": self.user_id,
            "content": self.content,
            "parent_post_id": self.parent_post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "is_deleted": self.is_deleted,
            "is_edited": self.is_edited,
            "edit_reason": self.edit_reason,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Post":
        """Create from dictionary"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)

    def __str__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Post(id={self.id}, score={self.score}, content='{preview}')"

    def __repr__(self) -> str:
        return self.__str__()
