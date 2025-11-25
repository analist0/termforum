"""Categories Screen - Browse forum categories"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import Container
from textual.binding import Binding
from ...storage import Database
from ...models import User, Category
from ...i18n import get_translator


class CategoryItem(ListItem):
    """A single category item"""

    def __init__(self, category: Category):
        super().__init__()
        self.category = category

    def compose(self) -> ComposeResult:
        """Compose category item"""
        # Category display
        title = f"{self.category.icon} {self.category.name}"
        description = self.category.description or "No description"
        stats = f"📋 {self.category.threads_count} threads • 💬 {self.category.posts_count} posts"

        yield Label(title, classes="category-title")
        yield Label(description, classes="category-description")
        yield Label(stats, classes="category-stats")


class CategoriesScreen(Screen):
    """Screen for browsing categories"""

    CSS = """
    CategoriesScreen {
        layout: vertical;
    }

    #header {
        height: 3;
        background: $boost;
        padding: 1;
        border: solid $primary;
    }

    #categories-list {
        height: 1fr;
        border: solid $primary;
    }

    .category-title {
        text-style: bold;
        color: $text;
    }

    .category-description {
        color: $text-muted;
    }

    .category-stats {
        color: $text-disabled;
        margin: 0 0 1 0;
    }

    #footer {
        height: 1;
        background: $panel;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("enter", "select", "Open", show=True),
        Binding("escape", "go_back", "Back", show=True),
        Binding("q", "go_back", "Back", show=False),
    ]

    def __init__(self, database: Database, current_user: User):
        super().__init__()
        self.database = database
        self.current_user = current_user

    def compose(self) -> ComposeResult:
        """Compose the categories screen"""
        t = get_translator().t

        # Header
        yield Container(
            Label(f"📁 {t('categories.title')}", classes="header-title"),
            id="header"
        )

        # Categories list
        yield self._build_categories_list()

        # Footer
        footer_text = (
            f"[Enter] {t('thread.view_thread')}  "
            f"[J/K] {t('keyboard.navigate_down')}/{t('keyboard.navigate_up')}  "
            f"[Esc] {t('common.back')}"
        )
        yield Container(
            Label(footer_text),
            id="footer"
        )

    def _build_categories_list(self) -> ListView:
        """Build categories list"""
        categories_list = ListView(id="categories-list")

        # Get all categories
        categories = self.database.list_categories()

        for category in categories:
            categories_list.append(CategoryItem(category))

        return categories_list

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle category selection"""
        if isinstance(event.item, CategoryItem):
            t = get_translator().t
            category = event.item.category
            self.app.notify(f"{t('categories.browse')}: {category.name}")
            # TODO: Navigate to category threads view

    def action_move_down(self) -> None:
        """Move selection down"""
        list_view = self.query_one(ListView)
        list_view.action_cursor_down()

    def action_move_up(self) -> None:
        """Move selection up"""
        list_view = self.query_one(ListView)
        list_view.action_cursor_up()

    def action_select(self) -> None:
        """Select current item"""
        list_view = self.query_one(ListView)
        list_view.action_select_cursor()

    def action_go_back(self) -> None:
        """Go back to previous screen"""
        self.app.pop_screen()
