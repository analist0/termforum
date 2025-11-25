"""Main Textual application for TermForum"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from .storage import Database
from .models import User
from .ui.screens import HomeScreen
from .i18n import get_translator
from .config import get_config


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

    def __init__(self, database: Database, current_user: User):
        super().__init__()
        self.database = database
        self.current_user = current_user

        # Initialize i18n and config
        self.translator = get_translator()
        self.config = get_config()
        t = self.translator.t

        # Set language from config if specified
        config_lang = self.config.get_language()
        if config_lang:
            self.translator.set_language(config_lang)

        # Set title and subtitle with translations
        self.title = f"{t('app.name')} {t('app.version')} - {current_user.display_name}"
        self.sub_title = t('app.subtitle')

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
        t = self.translator.t
        self.notify(t('messages.help_text'))

    def action_goto_home(self) -> None:
        """Go to home screen"""
        self.push_screen(HomeScreen(self.database, self.current_user))

    def action_goto_categories(self) -> None:
        """Go to categories screen"""
        from .ui.screens.categories import CategoriesScreen
        self.push_screen(CategoriesScreen(self.database, self.current_user))

    def action_goto_search(self) -> None:
        """Go to search screen"""
        t = self.translator.t
        self.notify(t('messages.coming_soon', feature=t('navigation.search')))

    def action_goto_profile(self) -> None:
        """Go to profile screen"""
        t = self.translator.t
        self.notify(f"{t('user.profile')}: {self.current_user.username}")

    def action_goto_settings(self) -> None:
        """Go to settings screen"""
        from .ui.screens.settings import SettingsScreen
        self.push_screen(SettingsScreen(self.database, self.current_user))

    def action_new_thread(self) -> None:
        """Create new thread"""
        t = self.translator.t
        self.notify(t('messages.coming_soon', feature=t('navigation.new_thread')))
