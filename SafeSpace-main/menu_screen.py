"""
Tela de Menu Principal.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical


class MenuScreen(Screen):
    """
    Menu principal da aplicação. Apresenta as opções de navegação
    """

    CSS = """
    MenuScreen {
        align: center middle;
        background: $background;
    }

    #menu-container {
        width: 52;
        height: auto;
        padding: 2 4;
        border: double $primary;
        background: $surface;
    }

    #menu-header {
        text-align: center;
        color: $success;
        text-style: bold;
        margin-bottom: 0;
    }

    #menu-user {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    .menu-btn {
        width: 100%;
        margin-bottom: 1;
    }

    #btn-tracking {
        background: $primary;
    }

    #btn-reports {
        background: $secondary;
    }

    #btn-emergency {
        background: $error;
    }

    #btn-home {
        background: $surface-darken-2;
    }

    #btn-quit {
        background: $surface-darken-3;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("q", "quit_app", "Sair"),
        ("escape", "go_home", "Tela Inicial"),
    ]

    def compose(self) -> ComposeResult:
        """widgets do menu principal."""
        user = getattr(self.app, "current_user", {})
        email = user.get("email", "Usuário") if user else "Usuário"

        with Container(id="menu-container"):
            yield Static("🌿  SafeSpace", id="menu-header")
            yield Static(f"Olá, {email}", id="menu-user")
            with Vertical():
                yield Button("💭  Tracking de Humor", id="btn-tracking", classes="menu-btn")
                yield Button("📊  Relatórios", id="btn-reports", classes="menu-btn")
                yield Button("🆘  Emergência", id="btn-emergency", classes="menu-btn")
                yield Button("🏠  Tela Inicial", id="btn-home", classes="menu-btn")
                yield Button("🚪  Sair", id="btn-quit", classes="menu-btn")
            yield Static("[dim]ESC: Início │ Q: Sair[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        navegação para a tela correspondente à opção escolhida.
        """
        btn = event.button.id
        if btn == "btn-tracking":
            self.app.push_screen("tracking")
        elif btn == "btn-reports":
            self.app.push_screen("reports")
        elif btn == "btn-emergency":
            self.app.push_screen("emergency")
        elif btn == "btn-home":
            self.action_go_home()
        elif btn == "btn-quit":
            self.action_quit_app()

    def action_go_home(self) -> None:
        """
        Volta para a tela inicial, deslogando o usuário atual
        """
        self.app.current_user = None
        while len(self.app.screen_stack) > 1:
            self.app.pop_screen()

    def action_quit_app(self) -> None:
        self.app.exit()
