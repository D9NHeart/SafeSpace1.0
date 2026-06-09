"""
Tela de Menu Principal.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical
from login_screen import clear_session
from database import get_today_checklist


class MenuScreen(Screen):

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

    #btn-calm {
        background: #3d2b5e;
        color: #c9b8e8;
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

    #btn-settings {
        background: #2a3a4a;
        color: #a8c8e8;
    }

    #btn-quit {
        background: $surface-darken-3;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }

    #wellness-banner {
        text-align: center;
        background: #3a2800;
        color: #ffd080;
        padding: 0 1;
        margin-bottom: 1;
        border: solid #7a5800 60%;
    }
    """

    BINDINGS = [
        ("q", "quit_app", "Sair"),
        ("escape", "go_home", "Tela Inicial"),
    ]

    def compose(self) -> ComposeResult:
        user = getattr(self.app, "current_user", {})
        name = user.get("name") or user.get("email", "Usuário") if user else "Usuário"

        with Container(id="menu-container"):
            yield Static("🌿  SafeSpace", id="menu-header")
            yield Static(f"Olá, {name} 👋", id="menu-user")
            # Banner de lembretes — preenchido em on_mount após verificar o checklist
            yield Static("", id="wellness-banner")
            with Vertical():
                yield Button("💭  Tracking de Humor", id="btn-tracking", classes="menu-btn")
                yield Button("🌙  Momento de Calma", id="btn-calm", classes="menu-btn")
                yield Button("📊  Relatórios", id="btn-reports", classes="menu-btn")
                yield Button("🆘  Emergência", id="btn-emergency", classes="menu-btn")
                yield Button("⚙️   Configurações", id="btn-settings", classes="menu-btn")
                yield Button("🏠  Tela Inicial", id="btn-home", classes="menu-btn")
                yield Button("🚪  Sair", id="btn-quit", classes="menu-btn")
            yield Static("[dim]ESC: Início │ Q: Sair[/]", id="footer-hint")

    def on_mount(self) -> None:
        """Verifica o checklist do dia e exibe o banner de lembretes se necessário."""
        self._refresh_wellness_banner()

    def on_screen_resume(self) -> None:
        """Atualiza o banner sempre que o menu voltar ao topo da pilha (ex: após tracking)."""
        self._refresh_wellness_banner()

    def _refresh_wellness_banner(self) -> None:
        user = getattr(self.app, "current_user", {}) or {}
        user_id = user.get("id")
        needs_food = user.get("needs_food_reminder", False)
        needs_meds = user.get("needs_medication_reminder", False)

        banner = self.query_one("#wellness-banner", Static)

        if not user_id or not (needs_food or needs_meds):
            banner.display = False
            return

        checklist = get_today_checklist(user_id)
        pending = []

        if needs_food and not checklist["ate_today"]:
            pending.append("🍽️ alimentar")
        if needs_meds and not checklist["took_meds"]:
            pending.append("💊 tomar remédios")

        if pending:
            items = " e ".join(pending)
            banner.update(f"⚠  Lembrete: você ainda precisa {items} hoje!")
            banner.display = True
        else:
            banner.display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-tracking":
            self.app.push_screen("tracking")
        elif btn == "btn-calm":
            self.app.push_screen("calm")
        elif btn == "btn-reports":
            self.app.push_screen("reports")
        elif btn == "btn-emergency":
            self.app.push_screen("emergency")
        elif btn == "btn-settings":
            self.app.push_screen("settings")
        elif btn == "btn-home":
            self.action_go_home()
        elif btn == "btn-quit":
            self.action_quit_app()

    def action_go_home(self) -> None:
        clear_session()
        self.app.current_user = None
        while len(self.app.screen_stack) > 1:
            self.app.pop_screen()

    def action_quit_app(self) -> None:
        self.app.exit()