"""
Tela inicial com opções de Login e Cadastro.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical


LOGO = """
╔═══════════════════════════════════╗
║                                   ║
║        S A F E S P A C E          ║
║                                   ║
║   Seu espaço seguro de bem-estar  ║
║                                   ║
╚═══════════════════════════════════╝
"""


class HomeScreen(Screen):
    """
    Tela inicial da aplicação. Apresenta o logo e os botões
    para navegar para Login ou Cadastro.
    """

    CSS = """
    HomeScreen {
        align: center middle;
        background: $background;
    }

    #home-container {
        width: 50;
        height: auto;
        align: center middle;
        padding: 2 4;
        border: double $primary;
        background: $surface;
    }

    #logo {
        text-align: center;
        color: $success;
        margin-bottom: 1;
    }

    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    .home-btn {
        width: 100%;
        margin-bottom: 1;
    }

    #btn-login {
        background: $primary;
        color: $text;
    }

    #btn-register {
        background: $success;
        color: $text;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Sair"),
        ("ctrl+c", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        """Compõe os widgets da tela inicial."""
        with Container(id="home-container"):
            yield Static(LOGO, id="logo")
            yield Static("Bem-vindo(a)! Como deseja continuar?", id="subtitle")
            with Vertical():
                yield Button("🔑  Fazer Login", id="btn-login", classes="home-btn")
                yield Button("📝  Criar Conta", id="btn-register", classes="home-btn")
            yield Static("[dim]Q: Sair[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Navega para Login ou Cadastro conforme o botão pressionado.
        """
        if event.button.id == "btn-login":
            self.app.push_screen("login")
        elif event.button.id == "btn-register":
            self.app.push_screen("register")

    def action_quit(self) -> None:
        """Encerra a aplicação."""
        self.app.exit()
