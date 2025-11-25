"""SQLite database manager for TermForum"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from datetime import datetime
from ..models import User, Category, Thread, Post


class Database:
    """SQLite database manager"""

    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            db_path = str(Path.home() / ".termforum" / "forum.db")

        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.connect()
        self.init_schema()

    def connect(self) -> None:
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def init_schema(self) -> None:
        """Initialize database schema"""
        cursor = self.conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL CHECK(length(username) >= 3 AND length(username) <= 20),
                email TEXT UNIQUE,
                bio TEXT CHECK(length(bio) <= 500),
                avatar TEXT DEFAULT '👤',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                posts_count INTEGER DEFAULT 0,
                threads_count INTEGER DEFAULT 0,
                reputation INTEGER DEFAULT 0,
                is_admin BOOLEAN DEFAULT 0,
                is_banned BOOLEAN DEFAULT 0,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                description TEXT,
                icon TEXT DEFAULT '📁',
                color TEXT DEFAULT '#3B82F6',
                position INTEGER DEFAULT 0,
                threads_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Threads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(title) >= 3 AND length(title) <= 200),
                slug TEXT UNIQUE NOT NULL,
                category_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                view_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 1,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                is_pinned BOOLEAN DEFAULT 0,
                is_locked BOOLEAN DEFAULT 0,
                is_deleted BOOLEAN DEFAULT 0,
                last_post_user_id INTEGER,
                last_post_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (last_post_user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                parent_post_id INTEGER,
                content TEXT NOT NULL CHECK(length(content) <= 10000),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                is_deleted BOOLEAN DEFAULT 0,
                is_edited BOOLEAN DEFAULT 0,
                edit_reason TEXT,
                FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (parent_post_id) REFERENCES posts(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_threads_category ON threads(category_id, is_deleted, is_pinned DESC, updated_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_thread ON posts(thread_id, is_deleted, created_at ASC)")

        self.conn.commit()

        # Create default categories if empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            self._create_default_categories()

    def _create_default_categories(self) -> None:
        """Create default categories"""
        default_categories = [
            ("General", "general", "General discussions", "💬", "#3B82F6"),
            ("Announcements", "announcements", "Important announcements", "📢", "#EF4444"),
            ("Support", "support", "Get help and support", "🆘", "#10B981"),
            ("Off-Topic", "off-topic", "Anything goes", "🎲", "#8B5CF6"),
        ]

        for i, (name, slug, desc, icon, color) in enumerate(default_categories):
            self.create_category(name=name, slug=slug, description=desc, icon=icon, color=color, position=i)

    # ════════════════════════════════════════════
    # USER OPERATIONS
    # ════════════════════════════════════════════

    def create_user(self, username: str, **kwargs) -> User:
        """Create a new user"""
        cursor = self.conn.cursor()

        email = kwargs.get("email")
        bio = kwargs.get("bio")
        avatar = kwargs.get("avatar", "👤")
        is_admin = kwargs.get("is_admin", False)

        cursor.execute("""
            INSERT INTO users (username, email, bio, avatar, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, bio, avatar, is_admin))

        self.conn.commit()
        user_id = cursor.lastrowid
        return self.get_user(user_id)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if row:
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                bio=row["bio"],
                avatar=row["avatar"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                posts_count=row["posts_count"],
                threads_count=row["threads_count"],
                reputation=row["reputation"],
                is_admin=bool(row["is_admin"]),
                is_banned=bool(row["is_banned"]),
                last_seen=datetime.fromisoformat(row["last_seen"]),
            )
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row:
            return self.get_user(row["id"])
        return None

    # ════════════════════════════════════════════
    # CATEGORY OPERATIONS
    # ════════════════════════════════════════════

    def create_category(self, name: str, **kwargs) -> Category:
        """Create a new category"""
        cursor = self.conn.cursor()

        slug = kwargs.get("slug", name.lower().replace(" ", "-"))
        description = kwargs.get("description")
        icon = kwargs.get("icon", "📁")
        color = kwargs.get("color", "#3B82F6")
        position = kwargs.get("position", 0)

        cursor.execute("""
            INSERT INTO categories (name, slug, description, icon, color, position)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, slug, description, icon, color, position))

        self.conn.commit()
        category_id = cursor.lastrowid
        return self.get_category(category_id)

    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()

        if row:
            return Category(
                id=row["id"],
                name=row["name"],
                slug=row["slug"],
                description=row["description"],
                icon=row["icon"],
                color=row["color"],
                position=row["position"],
                threads_count=row["threads_count"],
                posts_count=row["posts_count"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
        return None

    def list_categories(self) -> List[Category]:
        """List all categories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY position ASC")

        categories = []
        for row in cursor.fetchall():
            categories.append(Category(
                id=row["id"],
                name=row["name"],
                slug=row["slug"],
                description=row["description"],
                icon=row["icon"],
                color=row["color"],
                position=row["position"],
                threads_count=row["threads_count"],
                posts_count=row["posts_count"],
                created_at=datetime.fromisoformat(row["created_at"]),
            ))

        return categories

    # ════════════════════════════════════════════
    # THREAD OPERATIONS
    # ════════════════════════════════════════════

    def create_thread(self, title: str, content: str, user_id: int, category_id: int, **kwargs) -> Thread:
        """Create a new thread"""
        from slugify import slugify

        cursor = self.conn.cursor()
        slug = kwargs.get("slug", slugify(title))

        cursor.execute("""
            INSERT INTO threads (title, slug, category_id, user_id, content, last_post_user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, slug, category_id, user_id, content, user_id))

        # Update user threads_count
        cursor.execute("UPDATE users SET threads_count = threads_count + 1 WHERE id = ?", (user_id,))

        # Update category threads_count
        cursor.execute("UPDATE categories SET threads_count = threads_count + 1 WHERE id = ?", (category_id,))

        self.conn.commit()
        thread_id = cursor.lastrowid
        return self.get_thread(thread_id, increment_views=False)

    def get_thread(self, thread_id: int, increment_views: bool = True) -> Optional[Thread]:
        """Get thread by ID"""
        cursor = self.conn.cursor()

        if increment_views:
            cursor.execute("UPDATE threads SET view_count = view_count + 1 WHERE id = ?", (thread_id,))
            self.conn.commit()

        cursor.execute("""
            SELECT t.*, c.name as category_name, c.icon as category_icon,
                   u.username as user_name, u.avatar as user_avatar
            FROM threads t
            JOIN categories c ON t.category_id = c.id
            JOIN users u ON t.user_id = u.id
            WHERE t.id = ?
        """, (thread_id,))

        row = cursor.fetchone()

        if row:
            return Thread(
                id=row["id"],
                title=row["title"],
                slug=row["slug"],
                category_id=row["category_id"],
                user_id=row["user_id"],
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                view_count=row["view_count"],
                posts_count=row["posts_count"],
                upvotes=row["upvotes"],
                downvotes=row["downvotes"],
                is_pinned=bool(row["is_pinned"]),
                is_locked=bool(row["is_locked"]),
                is_deleted=bool(row["is_deleted"]),
                last_post_user_id=row["last_post_user_id"],
                last_post_at=datetime.fromisoformat(row["last_post_at"]),
                category_name=row["category_name"],
                category_icon=row["category_icon"],
                user_name=row["user_name"],
                user_avatar=row["user_avatar"],
            )
        return None

    def list_threads(self, category_id: int = None, user_id: int = None,
                     limit: int = 50, offset: int = 0) -> List[Thread]:
        """List threads with optional filters"""
        cursor = self.conn.cursor()

        query = """
            SELECT t.*, c.name as category_name, c.icon as category_icon,
                   u.username as user_name, u.avatar as user_avatar
            FROM threads t
            JOIN categories c ON t.category_id = c.id
            JOIN users u ON t.user_id = u.id
            WHERE t.is_deleted = 0
        """
        params = []

        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)

        if user_id:
            query += " AND t.user_id = ?"
            params.append(user_id)

        query += " ORDER BY t.is_pinned DESC, t.updated_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)

        threads = []
        for row in cursor.fetchall():
            threads.append(Thread(
                id=row["id"],
                title=row["title"],
                slug=row["slug"],
                category_id=row["category_id"],
                user_id=row["user_id"],
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                view_count=row["view_count"],
                posts_count=row["posts_count"],
                upvotes=row["upvotes"],
                downvotes=row["downvotes"],
                is_pinned=bool(row["is_pinned"]),
                is_locked=bool(row["is_locked"]),
                is_deleted=bool(row["is_deleted"]),
                last_post_user_id=row["last_post_user_id"],
                last_post_at=datetime.fromisoformat(row["last_post_at"]),
                category_name=row["category_name"],
                category_icon=row["category_icon"],
                user_name=row["user_name"],
                user_avatar=row["user_avatar"],
            ))

        return threads

    # ════════════════════════════════════════════
    # POST OPERATIONS
    # ════════════════════════════════════════════

    def create_post(self, thread_id: int, user_id: int, content: str,
                    parent_post_id: int = None) -> Post:
        """Create a new post"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO posts (thread_id, user_id, content, parent_post_id)
            VALUES (?, ?, ?, ?)
        """, (thread_id, user_id, content, parent_post_id))

        # Update thread posts_count and last_post info
        cursor.execute("""
            UPDATE threads
            SET posts_count = posts_count + 1,
                last_post_user_id = ?,
                last_post_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id, thread_id))

        # Update user posts_count
        cursor.execute("UPDATE users SET posts_count = posts_count + 1 WHERE id = ?", (user_id,))

        self.conn.commit()
        post_id = cursor.lastrowid
        return self.get_post(post_id)

    def get_post(self, post_id: int) -> Optional[Post]:
        """Get post by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.*, u.username as user_name, u.avatar as user_avatar, u.reputation as user_reputation
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        """, (post_id,))

        row = cursor.fetchone()

        if row:
            return Post(
                id=row["id"],
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                content=row["content"],
                parent_post_id=row["parent_post_id"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                upvotes=row["upvotes"],
                downvotes=row["downvotes"],
                is_deleted=bool(row["is_deleted"]),
                is_edited=bool(row["is_edited"]),
                edit_reason=row["edit_reason"],
                user_name=row["user_name"],
                user_avatar=row["user_avatar"],
                user_reputation=row["user_reputation"],
            )
        return None

    def list_posts(self, thread_id: int, limit: int = 100, offset: int = 0) -> List[Post]:
        """List posts in a thread"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.*, u.username as user_name, u.avatar as user_avatar, u.reputation as user_reputation
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.thread_id = ? AND p.is_deleted = 0
            ORDER BY p.created_at ASC
            LIMIT ? OFFSET ?
        """, (thread_id, limit, offset))

        posts = []
        for row in cursor.fetchall():
            posts.append(Post(
                id=row["id"],
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                content=row["content"],
                parent_post_id=row["parent_post_id"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                upvotes=row["upvotes"],
                downvotes=row["downvotes"],
                is_deleted=bool(row["is_deleted"]),
                is_edited=bool(row["is_edited"]),
                edit_reason=row["edit_reason"],
                user_name=row["user_name"],
                user_avatar=row["user_avatar"],
                user_reputation=row["user_reputation"],
            ))

        return posts

    # ════════════════════════════════════════════
    # STATISTICS
    # ════════════════════════════════════════════

    def get_forum_stats(self) -> Dict:
        """Get forum statistics"""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM threads WHERE is_deleted = 0")
        threads_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM posts WHERE is_deleted = 0")
        posts_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM categories")
        categories_count = cursor.fetchone()["count"]

        return {
            "users": users_count,
            "threads": threads_count,
            "posts": posts_count,
            "categories": categories_count,
            "total_content": threads_count + posts_count,
        }
