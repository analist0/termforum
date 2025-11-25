"""Category model"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from slugify import slugify


@dataclass
class Category:
    """Represents a forum category"""

    id: int
    name: str
    slug: str = ""
    description: Optional[str] = None
    icon: str = "📁"
    color: str = "#3B82F6"
    position: int = 0
    threads_count: int = 0
    posts_count: int = 0
    created_at: datetime = None

    def __post_init__(self):
        """Generate slug and set timestamp"""
        if not self.slug:
            self.slug = slugify(self.name)
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def display_name(self) -> str:
        """Get display name with icon"""
        return f"{self.icon} {self.name}"

    @property
    def total_activity(self) -> int:
        """Total threads + posts"""
        return self.threads_count + self.posts_count

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "position": self.position,
            "threads_count": self.threads_count,
            "posts_count": self.posts_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Create from dictionary"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

    def __str__(self) -> str:
        return f"Category({self.name}, threads={self.threads_count})"

    def __repr__(self) -> str:
        return self.__str__()
