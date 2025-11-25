"""Thread View Screen - Full thread with nested replies"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label, Button, Markdown
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.binding import Binding
from ...storage import Database
from ...models import User, Thread, Post


class PostItem(ListItem):
    """A single post item with nested replies"""

    def __init__(self, post: Post, depth: int = 0):
        super().__init__()
        self.post = post
        self.depth = depth

    def compose(self) -> ComposeResult:
        """Compose post item"""
        # Indentation for nested replies
        indent = "  " * self.depth

        # Author info
        author_info = f"{indent}{self.post.user_avatar} {self.post.user_name}"
        time_info = "now"  # TODO: Format time ago

        # Score
        score = self.post.score
        score_color = "green" if score > 0 else "red" if score < 0 else "white"

        # Meta line
        meta = f"{author_info} • {time_info} • ⬆️ {score}"

        yield Label(meta, classes="post-meta")

        # Content (markdown)
        content = self.post.display_content
        yield Markdown(content, classes="post-content")

        # Actions
        actions = f"{indent}[R] Reply  [U] Upvote  [D] Downvote"
        if self.post.is_edited:
            actions += "  [Edited]"
        yield Label(actions, classes="post-actions")


class ThreadViewScreen(Screen):
    """Screen for viewing a single thread with all posts"""

    CSS = """
    ThreadViewScreen {
        layout: vertical;
    }

    #thread-header {
        height: auto;
        background: $boost;
        padding: 1;
        border: solid $primary;
    }

    .thread-title {
        text-style: bold;
        color: $text;
    }

    .thread-meta {
        color: $text-muted;
    }

    #thread-content {
        height: auto;
        background: $surface;
        padding: 1;
        margin: 1 0;
        border: solid $accent;
    }

    #posts-container {
        height: 1fr;
        overflow-y: auto;
    }

    .post-meta {
        color: $text-muted;
        margin: 1 0;
    }

    .post-content {
        margin: 0 0 1 0;
    }

    .post-actions {
        color: $text-disabled;
        text-style: italic;
        margin: 0 0 2 0;
    }

    #footer-actions {
        height: 3;
        background: $panel;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False),
        Binding("k", "scroll_up", "Up", show=False),
        Binding("r", "reply_thread", "Reply", show=True),
        Binding("u", "upvote", "Upvote", show=True),
        Binding("d", "downvote", "Downvote", show=True),
        Binding("escape", "go_back", "Back", show=True),
        Binding("q", "go_back", "Back", show=False),
    ]

    def __init__(self, database: Database, current_user: User, thread: Thread):
        super().__init__()
        self.database = database
        self.current_user = current_user
        self.thread = thread
        self.posts = []

    def compose(self) -> ComposeResult:
        """Compose the thread view"""

        # Thread header
        yield Container(
            Label(f"📋 {self.thread.display_title}", classes="thread-title"),
            Label(
                f"{self.thread.category_icon} {self.thread.category_name} • "
                f"{self.thread.user_avatar} {self.thread.user_name} • "
                f"💬 {self.thread.posts_count} posts • "
                f"👀 {self.thread.view_count} views • "
                f"⬆️ {self.thread.score}",
                classes="thread-meta"
            ),
            id="thread-header"
        )

        # Thread content (first post)
        yield Container(
            Markdown(self.thread.content),
            id="thread-content"
        )

        # Posts list
        yield Container(
            self._build_posts_list(),
            id="posts-container"
        )

        # Footer actions
        footer_text = "[R] Reply  [U] Upvote  [D] Downvote  [J/K] Scroll  [Esc] Back"
        yield Container(
            Label(footer_text),
            id="footer-actions"
        )

    def _build_posts_list(self) -> ListView:
        """Build the posts list with nested replies"""
        posts_list = ListView()

        # Get all posts
        self.posts = self.database.list_posts(self.thread.id, limit=1000)

        if not self.posts:
            posts_list.append(ListItem(Label("No replies yet. Be the first to reply!")))
        else:
            # Build tree structure
            posts_by_parent = {}
            for post in self.posts:
                parent_id = post.parent_post_id
                if parent_id not in posts_by_parent:
                    posts_by_parent[parent_id] = []
                posts_by_parent[parent_id].append(post)

            # Render posts recursively
            def render_post_tree(parent_id, depth=0):
                if parent_id in posts_by_parent:
                    for post in posts_by_parent[parent_id]:
                        posts_list.append(PostItem(post, depth))
                        # Render children
                        render_post_tree(post.id, depth + 1)

            # Start with root posts (parent_post_id is None)
            render_post_tree(None, 0)

        return posts_list

    def action_scroll_down(self) -> None:
        """Scroll down"""
        posts_container = self.query_one("#posts-container")
        posts_container.scroll_down()

    def action_scroll_up(self) -> None:
        """Scroll up"""
        posts_container = self.query_one("#posts-container")
        posts_container.scroll_up()

    def action_reply_thread(self) -> None:
        """Reply to thread"""
        self.app.notify("Reply editor - Coming soon!")
        # TODO: Open reply editor

    def action_upvote(self) -> None:
        """Upvote thread"""
        self.app.notify(f"Upvoted: {self.thread.title}")
        # TODO: Implement voting

    def action_downvote(self) -> None:
        """Downvote thread"""
        self.app.notify(f"Downvoted: {self.thread.title}")
        # TODO: Implement voting

    def action_go_back(self) -> None:
        """Go back to previous screen"""
        self.app.pop_screen()
