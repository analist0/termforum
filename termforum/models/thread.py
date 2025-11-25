"""Thread model"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from slugify import slugify


@dataclass
class Thread:
    """Represents a forum thread"""

    id: int
    title: str
    slug: str = ""
    category_id: int = 0
    user_id: int = 0
    content: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    view_count: int = 0
    posts_count: int = 1
    upvotes: int = 0
    downvotes: int = 0
    is_pinned: bool = False
    is_locked: bool = False
    is_deleted: bool = False
    last_post_user_id: Optional[int] = None
    last_post_at: datetime = None

    # Additional fields (populated by joins)
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None

    def __post_init__(self):
        """Generate slug and set timestamps"""
        if not self.slug:
            self.slug = slugify(self.title)
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.last_post_at is None:
            self.last_post_at = self.created_at

    @property
    def score(self) -> int:
        """Net vote score"""
        return self.upvotes - self.downvotes

    @property
    def reply_count(self) -> int:
        """Number of replies (excluding first post)"""
        return max(0, self.posts_count - 1)

    @property
    def is_active(self) -> bool:
        """Check if thread is active (not locked/deleted)"""
        return not (self.is_locked or self.is_deleted)

    @property
    def display_title(self) -> str:
        """Title with status indicators"""
        prefix = ""
        if self.is_pinned:
            prefix += "📌 "
        if self.is_locked:
            prefix += "🔒 "
        return f"{prefix}{self.title}"

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "view_count": self.view_count,
            "posts_count": self.posts_count,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "is_pinned": self.is_pinned,
            "is_locked": self.is_locked,
            "is_deleted": self.is_deleted,
            "last_post_user_id": self.last_post_user_id,
            "last_post_at": self.last_post_at.isoformat() if self.last_post_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Thread":
        """Create from dictionary"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if "last_post_at" in data and isinstance(data["last_post_at"], str):
            data["last_post_at"] = datetime.fromisoformat(data["last_post_at"])
        return cls(**data)

    def __str__(self) -> str:
        return f"Thread({self.title}, posts={self.posts_count}, score={self.score})"

    def __repr__(self) -> str:
        return self.__str__()
