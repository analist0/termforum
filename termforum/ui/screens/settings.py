"""Settings Screen - Application preferences and configuration"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label, Button
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from ...storage import Database
from ...models import User
from ...i18n import get_translator
from ...config import get_config


class SettingItem(ListItem):
    """A single setting item"""

    def __init__(self, label: str, value: str, setting_key: str):
        super().__init__()
        self.label = label
        self.value = value
        self.setting_key = setting_key

    def compose(self) -> ComposeResult:
        """Compose setting item"""
        yield Label(f"{self.label}: {self.value}", classes="setting-label")


class SettingsScreen(Screen):
    """Screen for application settings"""

    CSS = """
    SettingsScreen {
        layout: vertical;
    }

    #header {
        height: 3;
        background: $boost;
        padding: 1;
        border: solid $primary;
    }

    .header-title {
        text-style: bold;
        color: $text;
    }

    #settings-container {
        height: 1fr;
        padding: 1;
    }

    #settings-list {
        border: solid $primary;
        height: 1fr;
    }

    .setting-label {
        color: $text;
        padding: 0 1;
    }

    .setting-description {
        color: $text-muted;
        padding: 0 1;
        margin: 0 0 1 0;
    }

    #footer {
        height: 3;
        background: $panel;
        padding: 1;
    }

    #buttons-container {
        layout: horizontal;
        height: auto;
        margin: 1 0;
    }

    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("enter", "select", "Edit", show=True),
        Binding("escape", "go_back", "Back", show=True),
        Binding("q", "go_back", "Back", show=False),
    ]

    def __init__(self, database: Database, current_user: User):
        super().__init__()
        self.database = database
        self.current_user = current_user
        self.config = get_config()
        self.translator = get_translator()

    def compose(self) -> ComposeResult:
        """Compose the settings screen"""
        t = self.translator.t

        # Header
        yield Container(
            Label(f"⚙️ {t('settings.title')}", classes="header-title"),
            id="header"
        )

        # Settings container
        yield Container(
            ListView(id="settings-list"),
            id="settings-container"
        )

        # Footer with instructions
        footer_text = (
            f"[Enter] {t('settings.edit')}  "
            f"[J/K] {t('keyboard.navigate_down')}/{t('keyboard.navigate_up')}  "
            f"[Esc] {t('common.back')}"
        )
        yield Container(
            Label(footer_text),
            id="footer"
        )

    def on_mount(self) -> None:
        """Called after screen is mounted - populate settings"""
        self._populate_settings_list()

    def _populate_settings_list(self) -> None:
        """Populate the settings list"""
        t = self.translator.t
        settings_list = self.query_one("#settings-list", ListView)

        # Language setting
        current_lang = self.config.get_language()
        if current_lang is None:
            lang_display = t('settings.language_auto')
        elif current_lang == "en":
            lang_display = "English"
        elif current_lang == "he":
            lang_display = "עברית"
        else:
            lang_display = current_lang

        settings_list.append(
            SettingItem(
                t('settings.language'),
                lang_display,
                "language"
            )
        )

        # Theme setting
        theme = self.config.get_theme()
        settings_list.append(
            SettingItem(
                t('settings.theme'),
                theme,
                "theme"
            )
        )

        # Vim mode setting
        vim_mode = self.config.get("vim_mode", True)
        vim_display = t('common.yes') if vim_mode else t('common.no')
        settings_list.append(
            SettingItem(
                t('settings.vim_mode'),
                vim_display,
                "vim_mode"
            )
        )

        # Show avatars setting
        show_avatars = self.config.get("show_avatars", True)
        avatars_display = t('common.yes') if show_avatars else t('common.no')
        settings_list.append(
            SettingItem(
                t('settings.show_avatars'),
                avatars_display,
                "show_avatars"
            )
        )

        # AI enabled setting
        ai_enabled = self.config.get("ai_enabled", True)
        ai_display = t('common.yes') if ai_enabled else t('common.no')
        settings_list.append(
            SettingItem(
                t('settings.ai_enabled'),
                ai_display,
                "ai_enabled"
            )
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle setting selection"""
        if isinstance(event.item, SettingItem):
            setting_key = event.item.setting_key

            if setting_key == "language":
                self._change_language()
            elif setting_key == "theme":
                self._change_theme()
            elif setting_key == "vim_mode":
                self._toggle_vim_mode()
            elif setting_key == "show_avatars":
                self._toggle_avatars()
            elif setting_key == "ai_enabled":
                self._toggle_ai()

    def _change_language(self) -> None:
        """Cycle through available languages"""
        t = self.translator.t
        current_lang = self.config.get_language()

        # Cycle: Auto -> English -> Hebrew -> Auto
        if current_lang is None:
            new_lang = "en"
            self.config.set_language("en")
            self.translator.set_language("en")
            self.app.notify(t('settings.language_changed', language="English"))
        elif current_lang == "en":
            new_lang = "he"
            self.config.set_language("he")
            self.translator.set_language("he")
            self.app.notify(t('settings.language_changed', language="עברית"))
        else:
            new_lang = None
            self.config.set_language(None)
            self.translator.detect_language()
            self.app.notify(t('settings.language_changed', language=t('settings.language_auto')))

        # Refresh the settings list
        self._refresh_settings()

    def _change_theme(self) -> None:
        """Cycle through available themes"""
        t = self.translator.t
        current_theme = self.config.get_theme()

        # Cycle: dark -> light -> kali -> dark
        themes = ["dark", "light", "kali"]
        current_index = themes.index(current_theme) if current_theme in themes else 0
        new_theme = themes[(current_index + 1) % len(themes)]

        self.config.set_theme(new_theme)
        self.app.notify(t('settings.theme_changed', theme=new_theme))

        # Refresh the settings list
        self._refresh_settings()

    def _toggle_vim_mode(self) -> None:
        """Toggle vim mode"""
        t = self.translator.t
        current = self.config.get("vim_mode", True)
        new_value = not current
        self.config.set("vim_mode", new_value)

        status = t('common.enabled') if new_value else t('common.disabled')
        self.app.notify(f"{t('settings.vim_mode')}: {status}")

        self._refresh_settings()

    def _toggle_avatars(self) -> None:
        """Toggle avatar display"""
        t = self.translator.t
        current = self.config.get("show_avatars", True)
        new_value = not current
        self.config.set("show_avatars", new_value)

        status = t('common.enabled') if new_value else t('common.disabled')
        self.app.notify(f"{t('settings.show_avatars')}: {status}")

        self._refresh_settings()

    def _toggle_ai(self) -> None:
        """Toggle AI features"""
        t = self.translator.t
        current = self.config.get("ai_enabled", True)
        new_value = not current
        self.config.set("ai_enabled", new_value)

        status = t('common.enabled') if new_value else t('common.disabled')
        self.app.notify(f"{t('settings.ai_enabled')}: {status}")

        self._refresh_settings()

    def _refresh_settings(self) -> None:
        """Refresh the settings display"""
        settings_list = self.query_one("#settings-list", ListView)
        settings_list.clear()
        self._populate_settings_list()

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
