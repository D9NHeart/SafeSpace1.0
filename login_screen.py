"""
Tela de Login do SafeSpace.
"""

import json
import os
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label, Checkbox
from textual.containers import Container, Vertical
from user_model import UserModel

SESSION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session.json")


def save_session(user_id: int) -> None:
    with open(SESSION_PATH, "w") as f:
        json.dump({"user_id": user_id}, f)


def clear_session() -> None:
    if os.path.exists(SESSION_PATH):
        os.remove(SESSION_PATH)


def load_session() -> int | None:
    try:
        with open(SESSION_PATH, "r") as f:
            data = json.load(f)
            return data.get("user_id")
    except Exception:
        return None


class LoginScreen(Screen):

    CSS = """
    LoginScreen {
        align: center middle;
        background: $background;
    }

    #login-container {
        width: 52;
        height: auto;
        padding: 2 4;
        border: double $primary;
        background: $surface;
    }

    #login-title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 2;
    }

    .field-label {
        color: $text-muted;
        margin-top: 1;
    }

    Input {
        margin-bottom: 1;
    }

    #remember-me {
        margin-top: 1;
        margin-bottom: 1;
    }

    #error-msg {
        color: $error;
        text-align: center;
        height: 1;
        margin-bottom: 1;
    }

    #btn-do-login {
        width: 100%;
        background: $primary;
        margin-top: 1;
    }

    #btn-back {
        width: 100%;
        background: $surface-darken-1;
        margin-top: 1;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Voltar"),
        ("q", "go_back", "Voltar"),
    ]

    def __init__(self):
        super().__init__()
        self._user_model = UserModel()

    def compose(self) -> ComposeResult:
        with Container(id="login-container"):
            yield Static("🔑  Login", id="login-title")
            yield Label("Email:", classes="field-label")
            yield Input(placeholder="seu@email.com", id="email-input")
            yield Label("Senha:", classes="field-label")
            yield Input(placeholder="••••••••", password=True, id="password-input")
            yield Checkbox("Lembrar de mim", id="remember-me")
            yield Static("", id="error-msg")
            yield Button("Entrar →", id="btn-do-login")
            yield Button("← Voltar", id="btn-back")
            yield Static("[dim]ESC: Voltar[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.action_go_back()
        elif event.button.id == "btn-do-login":
            self._attempt_login()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._attempt_login()

    def _attempt_login(self) -> None:
        email = self.query_one("#email-input", Input).value.strip()
        password = self.query_one("#password-input", Input).value

        if not email or not password:
            self._show_error("Preencha email e senha.")
            return

        success, result = self._user_model.login(email, password)

        if not success:
            self._show_error(result)
        else:
            self.app.current_user = result
            remember = self.query_one("#remember-me", Checkbox).value
            if remember:
                save_session(result["id"])
            else:
                clear_session()
            self.app.push_screen("menu")

    def _show_error(self, message: str) -> None:
        self.query_one("#error-msg", Static).update(f"⚠ {message}")

    def action_go_back(self) -> None:
        self.app.pop_screen()
