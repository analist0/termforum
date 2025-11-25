"""Login and Registration Screens for TermForum

Features:
- Animated ASCII art splash screen
- Password strength meter
- Remember me checkbox
- Session management
- Beautiful cyberpunk design
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Button, Checkbox, Label
from textual.containers import Container, Vertical, Horizontal, Center
from textual.validation import Function, ValidationResult, Validator
from textual import events
from ...storage import Database
from ...auth import hash_password, verify_password, check_password_strength, SessionManager
from ...i18n import get_translator


# ASCII Art Splash Screens
SPLASH_HACKER = """
╔════════════════════════════════════════════════════════════════╗
║  ████████╗███████╗██████╗ ███╗   ███╗███████╗ ██████╗ ██████╗ ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝██╔═══██╗██╔══██╗║
║     ██║   █████╗  ██████╔╝██╔████╔██║█████╗  ██║   ██║██████╔╝║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██╗║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝║
║                                                                  ║
║           🔐 Advanced Terminal Forum for Hackers 🔐             ║
║              PolyCrypt™ Authentication System                   ║
╚════════════════════════════════════════════════════════════════╝
"""

SPLASH_CYBER = """
    ▄▄▄█████▓▓█████  ██▀███   ███▄ ▄███▓  █████▒▒█████   ██▀███   █    ██  ███▄ ▄███▓
    ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▓██▒▀█▀ ██▒▓██   ▒▒██▒  ██▒▓██ ▒ ██▒ ██  ▓██▒▓██▒▀█▀ ██▒
    ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒▓██    ▓██░▒████ ░▒██░  ██▒▓██ ░▄█ ▒▓██  ▒██░▓██    ▓██░
    ░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  ▒██    ▒██ ░▓█▒  ░▒██   ██░▒██▀▀█▄  ▓▓█  ░██░▒██    ▒██
      ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒██▒   ░██▒░▒█░   ░ ████▓▒░░██▓ ▒██▒▒▒█████▓ ▒██▒   ░██▒
      ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ░  ░ ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░   ░  ░

                    🌐 Next-Gen Terminal Communication 🌐
"""


class PasswordStrengthValidator(Validator):
    """Validator that shows password strength in real-time"""

    def validate(self, value: str) -> ValidationResult:
        """Validate password and show strength"""
        if not value:
            return self.success()

        score, label = check_password_strength(value)

        if score < 30:
            return self.failure(f"Strength: {label}")
        elif score < 50:
            return self.success()  # Allow but show warning
        else:
            return self.success()


class LoginScreen(Screen):
    """Login screen with beautiful design and animations"""

    CSS = """
    LoginScreen {
        align: center middle;
        background: $surface;
    }

    #splash-container {
        width: 70;
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 1 2;
        margin: 1;
    }

    #splash-art {
        color: $accent;
        text-style: bold;
    }

    #login-container {
        width: 60;
        height: auto;
        background: $panel;
        border: heavy $success;
        padding: 2;
        margin: 1;
    }

    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 1;
    }

    .input-label {
        margin-top: 1;
        color: $text;
    }

    Input {
        width: 100%;
        margin-bottom: 1;
        border: solid $primary;
    }

    Input:focus {
        border: solid $accent;
    }

    #password-strength {
        height: 1;
        width: 100%;
        margin-bottom: 1;
        color: $warning;
    }

    #remember-me {
        margin: 1 0;
    }

    #button-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        margin-top: 1;
    }

    Button {
        width: 1fr;
        margin: 0 1;
    }

    Button.login-button {
        background: $success;
    }

    Button.register-button {
        background: $primary;
    }

    Button.login-button:hover {
        background: $success-darken-1;
    }

    Button.register-button:hover {
        background: $primary-darken-1;
    }

    #error-message {
        color: $error;
        text-style: bold;
        margin-top: 1;
        height: 1;
    }

    #info-message {
        color: $text-muted;
        text-align: center;
        margin-top: 1;
    }
    """

    def __init__(self, database: Database, session_manager: SessionManager):
        super().__init__()
        self.database = database
        self.session_manager = session_manager
        self.t = get_translator().t

    def compose(self) -> ComposeResult:
        """Compose the login screen"""
        # Splash screen
        yield Container(
            Static(SPLASH_CYBER, id="splash-art"),
            id="splash-container"
        )

        # Login form
        yield Container(
            Static(f"🔐 {self.t('auth.login')}", id="title"),
            Label(self.t('auth.username'), classes="input-label"),
            Input(placeholder=self.t('auth.username_placeholder'), id="username-input"),
            Label(self.t('auth.password'), classes="input-label"),
            Input(
                placeholder=self.t('auth.password_placeholder'),
                password=True,
                id="password-input"
            ),
            Static("", id="error-message"),
            Checkbox(self.t('auth.remember_me'), id="remember-me"),
            Horizontal(
                Button(self.t('auth.login'), variant="success", id="login-button", classes="login-button"),
                Button(self.t('auth.register'), variant="primary", id="register-button", classes="register-button"),
                id="button-container"
            ),
            Static(self.t('auth.no_account_hint'), id="info-message"),
            id="login-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "login-button":
            self._handle_login()
        elif event.button.id == "register-button":
            self._show_register_screen()

    def _handle_login(self) -> None:
        """Handle login attempt"""
        username_input = self.query_one("#username-input", Input)
        password_input = self.query_one("#password-input", Input)
        remember_checkbox = self.query_one("#remember-me", Checkbox)
        error_label = self.query_one("#error-message", Static)

        username = username_input.value.strip()
        password = password_input.value

        # Validate inputs
        if not username or not password:
            error_label.update(self.t('auth.error.empty_fields'))
            return

        # Get user from database
        user = self.database.get_user_by_username(username)

        if not user:
            error_label.update(self.t('auth.error.user_not_found'))
            return

        # Check if user has password (old users might not)
        if not hasattr(user, 'password_hash') or not user.password_hash:
            error_label.update(self.t('auth.error.no_password'))
            return

        # Verify password
        if not verify_password(password, user.password_hash):
            error_label.update(self.t('auth.error.wrong_password'))
            return

        # Create session
        remember_me = remember_checkbox.value
        self.session_manager.create_session(
            user_id=user.id,
            username=user.username,
            remember_me=remember_me
        )

        # Success! Return user to main app
        self.dismiss(user)

    def _show_register_screen(self) -> None:
        """Switch to register screen"""
        self.app.push_screen(RegisterScreen(self.database, self.session_manager))


class RegisterScreen(Screen):
    """Registration screen with password strength meter"""

    CSS = """
    RegisterScreen {
        align: center middle;
        background: $surface;
    }

    #register-container {
        width: 60;
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 2;
        margin: 1;
    }

    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 1;
    }

    .input-label {
        margin-top: 1;
        color: $text;
    }

    Input {
        width: 100%;
        margin-bottom: 1;
        border: solid $primary;
    }

    Input:focus {
        border: solid $accent;
    }

    #password-strength {
        height: 1;
        width: 100%;
        margin-bottom: 1;
        padding: 0 1;
    }

    .strength-bar {
        background: $panel;
        color: $text;
    }

    #button-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        margin-top: 1;
    }

    Button {
        width: 1fr;
        margin: 0 1;
    }

    Button.register-button {
        background: $success;
    }

    Button.back-button {
        background: $warning;
    }

    #error-message {
        color: $error;
        text-style: bold;
        margin-top: 1;
        height: 2;
    }

    #success-message {
        color: $success;
        text-style: bold;
        margin-top: 1;
        height: 2;
    }
    """

    def __init__(self, database: Database, session_manager: SessionManager):
        super().__init__()
        self.database = database
        self.session_manager = session_manager
        self.t = get_translator().t

    def compose(self) -> ComposeResult:
        """Compose the register screen"""
        yield Container(
            Static(f"📝 {self.t('auth.register')}", id="title"),
            Label(self.t('auth.username'), classes="input-label"),
            Input(
                placeholder=self.t('auth.username_placeholder'),
                id="username-input"
            ),
            Label(self.t('auth.email'), classes="input-label"),
            Input(
                placeholder=self.t('auth.email_placeholder'),
                id="email-input"
            ),
            Label(self.t('auth.password'), classes="input-label"),
            Input(
                placeholder=self.t('auth.password_placeholder'),
                password=True,
                id="password-input"
            ),
            Static("", id="password-strength", classes="strength-bar"),
            Label(self.t('auth.confirm_password'), classes="input-label"),
            Input(
                placeholder=self.t('auth.confirm_password_placeholder'),
                password=True,
                id="confirm-password-input"
            ),
            Static("", id="error-message"),
            Static("", id="success-message"),
            Horizontal(
                Button(self.t('auth.register'), variant="success", id="register-button", classes="register-button"),
                Button(self.t('common.back'), variant="warning", id="back-button", classes="back-button"),
                id="button-container"
            ),
            id="register-container"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Update password strength meter in real-time"""
        if event.input.id == "password-input":
            password = event.value
            strength_label = self.query_one("#password-strength", Static)

            if not password:
                strength_label.update("")
                return

            score, label = check_password_strength(password)

            # Create visual strength bar
            bar_length = int(score / 5)  # 0-20 characters
            bar = "█" * bar_length + "░" * (20 - bar_length)

            # Color based on strength
            if score < 30:
                color = "red"
            elif score < 50:
                color = "yellow"
            elif score < 70:
                color = "cyan"
            else:
                color = "green"

            strength_label.update(f"[{color}]{bar}[/] {label} ({score}/100)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "register-button":
            self._handle_register()
        elif event.button.id == "back-button":
            self.app.pop_screen()

    def _handle_register(self) -> None:
        """Handle registration attempt"""
        username_input = self.query_one("#username-input", Input)
        email_input = self.query_one("#email-input", Input)
        password_input = self.query_one("#password-input", Input)
        confirm_input = self.query_one("#confirm-password-input", Input)
        error_label = self.query_one("#error-message", Static)
        success_label = self.query_one("#success-message", Static)

        username = username_input.value.strip()
        email = email_input.value.strip()
        password = password_input.value
        confirm_password = confirm_input.value

        # Clear previous messages
        error_label.update("")
        success_label.update("")

        # Validate inputs
        if not username or not password:
            error_label.update(self.t('auth.error.empty_fields'))
            return

        if len(username) < 3:
            error_label.update(self.t('auth.error.username_too_short'))
            return

        if password != confirm_password:
            error_label.update(self.t('auth.error.password_mismatch'))
            return

        # Check password strength
        score, _ = check_password_strength(password)
        if score < 30:
            error_label.update(self.t('auth.error.password_too_weak'))
            return

        # Check if username exists
        existing_user = self.database.get_user_by_username(username)
        if existing_user:
            error_label.update(self.t('auth.error.username_exists'))
            return

        # Hash password
        password_hash = hash_password(password)

        # Create user
        try:
            user = self.database.create_user(
                username=username,
                email=email if email else None,
                password_hash=password_hash
            )

            # Show success message
            success_label.update(f"✅ {self.t('auth.success.registered')}")

            # Create session
            self.session_manager.create_session(
                user_id=user.id,
                username=user.username,
                remember_me=False
            )

            # Return to app after 2 seconds
            self.set_timer(2.0, lambda: self.dismiss(user))

        except Exception as e:
            error_label.update(f"{self.t('auth.error.registration_failed')}: {str(e)}")
