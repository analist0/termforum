"""Home screen for TermForum"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import Container, Vertical, Horizontal
from ...storage import Database
from ...models import User
from ...i18n import get_translator


class ThreadListItem(ListItem):
    """A single thread item in the list"""

    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    def compose(self) -> ComposeResult:
        """Compose the thread item"""
        # Thread title with status indicators
        title = f"{self.thread.display_title}"

        # Thread metadata
        meta = (
            f"{self.thread.category_icon} {self.thread.category_name} • "
            f"{self.thread.user_avatar} {self.thread.user_name} • "
            f"💬 {self.thread.reply_count} • "
            f"👀 {self.thread.view_count} • "
            f"⬆️ {self.thread.score}"
        )

        yield Label(title, classes="thread-title")
        yield Label(meta, classes="thread-meta")


class HomeScreen(Screen):
    """Home screen showing thread list"""

    CSS = """
    HomeScreen {
        layout: grid;
        grid-size: 2 3;
        grid-rows: auto 1fr auto;
    }

    #stats-container {
        column-span: 2;
        height: 3;
        background: $boost;
        padding: 1;
    }

    #main-container {
        column-span: 2;
        row-span: 1;
    }

    #thread-list {
        border: solid $primary;
        height: 1fr;
    }

    .thread-title {
        text-style: bold;
        color: $text;
    }

    .thread-meta {
        color: $text-muted;
    }

    #footer-info {
        column-span: 2;
        height: 1;
        background: $panel;
        padding: 0 1;
    }
    """

    def __init__(self, database: Database, current_user: User):
        super().__init__()
        self.database = database
        self.current_user = current_user

    def compose(self) -> ComposeResult:
        """Compose the home screen"""
        t = get_translator().t

        # Stats header
        stats = self.database.get_forum_stats()
        stats_text = (
            f"📊 {t('home.stats.users')}: {stats['users']} • "
            f"📋 {t('home.stats.threads')}: {stats['threads']} • "
            f"💬 {t('home.stats.posts')}: {stats['posts']} • "
            f"📁 {t('home.stats.categories')}: {stats['categories']}"
        )

        yield Container(
            Static(stats_text, id="stats-text"),
            id="stats-container"
        )

        # Main content area with empty ListView (will populate in on_mount)
        yield Container(
            ListView(id="thread-list"),
            id="main-container"
        )

        # Footer info
        footer_text = (
            f"j/k: {t('keyboard.navigate_down')}/{t('keyboard.navigate_up')} • "
            f"Enter: {t('common.select')} • "
            f"n: {t('navigation.new_thread')} • "
            f"q: {t('common.quit')} • "
            f"?: {t('common.help')}"
        )
        yield Container(
            Static(footer_text),
            id="footer-info"
        )

    def on_mount(self) -> None:
        """Called after screen is mounted - populate thread list"""
        self._populate_thread_list()

    def _populate_thread_list(self) -> None:
        """Populate the thread list with data"""
        t = get_translator().t
        thread_list = self.query_one("#thread-list", ListView)

        # Get threads from database
        threads = self.database.list_threads(limit=50)

        if not threads:
            # Show empty state
            thread_list.append(ListItem(Label(t('home.no_threads'))))
        else:
            for thread in threads:
                thread_list.append(ThreadListItem(thread))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle thread selection"""
        if isinstance(event.item, ThreadListItem):
            thread = event.item.thread
            # Navigate to thread view screen
            from .thread_view import ThreadViewScreen
            self.app.push_screen(ThreadViewScreen(self.database, self.current_user, thread))
