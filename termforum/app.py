"""Main Textual application for TermForum"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from .storage import Database
from .models import User
from .ui.screens import HomeScreen


class TermForumApp(App):
    """TermForum TUI Application"""

    CSS = """
    Screen {
        background: $surface;
    }

    Header {
        background: $primary;
        color: $text;
    }

    Footer {
        background: $panel;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "help", "Help"),
        Binding("1", "goto_home", "Home"),
        Binding("2", "goto_categories", "Categories"),
        Binding("3", "goto_search", "Search"),
        Binding("4", "goto_profile", "Profile"),
        Binding("5", "goto_settings", "Settings"),
        Binding("n", "new_thread", "New Thread"),
    ]

    def __init__(self, database: Database, current_user: User):
        super().__init__()
        self.database = database
        self.current_user = current_user
        self.title = f"TermForum v0.1.0 - {current_user.display_name}"
        self.sub_title = "Terminal Forum Application"

    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted"""
        # Show home screen
        self.push_screen(HomeScreen(self.database, self.current_user))

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()

    def action_help(self) -> None:
        """Show help"""
        self.notify("Help: j/k=navigate, Enter=select, n=new thread, q=quit")

    def action_goto_home(self) -> None:
        """Go to home screen"""
        self.push_screen(HomeScreen(self.database, self.current_user))

    def action_goto_categories(self) -> None:
        """Go to categories screen"""
        from .ui.screens.categories import CategoriesScreen
        self.push_screen(CategoriesScreen(self.database, self.current_user))

    def action_goto_search(self) -> None:
        """Go to search screen"""
        self.notify("Search screen - Coming soon!")

    def action_goto_profile(self) -> None:
        """Go to profile screen"""
        self.notify(f"Profile: {self.current_user.username}")

    def action_goto_settings(self) -> None:
        """Go to settings screen"""
        self.notify("Settings screen - Coming soon!")

    def action_new_thread(self) -> None:
        """Create new thread"""
        self.notify("New thread editor - Coming soon!")
