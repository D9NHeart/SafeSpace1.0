"""
Tela inicial com opções de Login e Cadastro.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical


LOGO = """
  S A F E S P A C E
  Seu espaço seguro de bem-estar
"""


class HomeScreen(Screen):

    CSS = """
    HomeScreen {
        align: center middle;
        background: #1a1025;
    }

    #home-container {
        width: 50;
        height: auto;
        align: center middle;
        padding: 2 4;
        border: double #9b7fd4;
        background: #221533;
    }

    #logo {
        text-align: center;
        color: #c9a0f5;
        text-style: bold;
        margin-bottom: 2;
    }

    #subtitle {
        text-align: center;
        color: #a08db5;
        margin-bottom: 2;
    }

    .home-btn {
        width: 100%;
        margin-bottom: 1;
    }

    #btn-login {
        background: #5b4a8a;
        color: #ede0ff;
    }

    #btn-register {
        background: #3a5a8a;
        color: #dceeff;
    }

    #footer-hint {
        text-align: center;
        color: #6b5a80;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Sair"),
        ("ctrl+c", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="home-container"):
            yield Static(LOGO, id="logo")
            yield Static("Bem-vindo(a)! Como deseja continuar?", id="subtitle")
            with Vertical():
                yield Button("🔑  Fazer Login", id="btn-login", classes="home-btn")
                yield Button("📝  Criar Conta", id="btn-register", classes="home-btn")
            yield Static("[dim]Q: Sair[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-login":
            self.app.push_screen("login")
        elif event.button.id == "btn-register":
            self.app.push_screen("register")

    def action_quit(self) -> None:
        self.app.exit()