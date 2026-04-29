"""
Tela de Tracking de Humor
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, TextArea
from textual.containers import Container, Vertical, Horizontal
from mood_model import MoodModel
from mood_utils import MOOD_EMOJIS, MOOD_LABELS, mood_to_emoji


class TrackingScreen(Screen):

    CSS = """
    TrackingScreen {
        align: center middle;
        background: $background;
    }

    #tracking-container {
        width: 60;
        height: auto;
        padding: 2 4;
        border: double $primary;
        background: $surface;
    }

    #tracking-title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }

    #tracking-subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    #emoji-grid {
        height: auto;
        margin-bottom: 2;
    }

    .emoji-row {
        height: auto;
        align: center middle;
        margin-bottom: 1;
    }

    .emoji-btn {
        width: 14;
        height: 3;
        margin: 0 1;
        background: $surface-darken-1;
        border: solid $surface-lighten-1;
        text-align: center;
    }

    .emoji-btn.selected {
        background: $primary-darken-1;
        border: solid $primary;
        text-style: bold;
    }

    #selected-label {
        text-align: center;
        color: $success;
        text-style: bold;
        height: 1;
        margin-bottom: 2;
    }

    #description-label {
        color: $text-muted;
        margin-bottom: 1;
    }

    #description-area {
        height: 5;
        margin-bottom: 1;
        border: solid $surface-lighten-1;
    }

    #msg {
        text-align: center;
        height: 1;
        margin-bottom: 1;
    }

    #btn-save {
        width: 100%;
        background: $success;
        margin-bottom: 1;
    }

    #btn-back {
        width: 100%;
        background: $surface-darken-1;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Voltar"),
    ]

    def __init__(self):

        super().__init__()
        self._mood_model = MoodModel()
        self._selected_mood: int | None = None

    def compose(self) -> ComposeResult:
        """widgets tracking de humor."""
        with Container(id="tracking-container"):
            yield Static("💭  Como você está agora?", id="tracking-title")
            yield Static("Selecione o emoji que melhor representa seu humor:", id="tracking-subtitle")

            with Vertical(id="emoji-grid"):
                with Horizontal(classes="emoji-row"):
                    for level in range(1, 4):
                        emoji = MOOD_EMOJIS[level]
                        label = MOOD_LABELS[level]
                        yield Button(
                            f"{emoji}  {label}",
                            id=f"mood-{level}",
                            classes="emoji-btn",
                        )
                with Horizontal(classes="emoji-row"):
                    for level in range(4, 7):
                        emoji = MOOD_EMOJIS[level]
                        label = MOOD_LABELS[level]
                        yield Button(
                            f"{emoji}  {label}",
                            id=f"mood-{level}",
                            classes="emoji-btn",
                        )

            yield Static("Selecione um emoji acima ↑", id="selected-label")

            yield Static("📝  Como você está se sentindo? (opcional):", id="description-label")
            yield TextArea(id="description-area")

            yield Static("", id="msg")
            yield Button("💾  Salvar Registro", id="btn-save")
            yield Button("← Voltar ao Menu", id="btn-back")
            yield Static("[dim]ESC: Voltar[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:

        btn_id = event.button.id

        if btn_id and btn_id.startswith("mood-"):
            level = int(btn_id.split("-")[1])
            self._select_mood(level)

        elif btn_id == "btn-save":
            self._save_entry()

        elif btn_id == "btn-back":
            self.action_go_back()

    def _select_mood(self, level: int) -> None:
        """
        Atualiza a seleção de humor atual"""
        self._selected_mood = level

        for i in range(1, 7):
            btn = self.query_one(f"#mood-{i}", Button)
            if i == level:
                btn.add_class("selected")
            else:
                btn.remove_class("selected")

        emoji = MOOD_EMOJIS[level]
        label = MOOD_LABELS[level]
        self.query_one("#selected-label", Static).update(
            f"Selecionado: {emoji}  {label}"
        )
        self.query_one("#msg", Static).update("")

    def _save_entry(self) -> None:
        """
        Salva o registro de humor 
        """
        if self._selected_mood is None:
            self.query_one("#msg", Static).update("[red]⚠ Selecione um emoji primeiro![/]")
            return

        user = getattr(self.app, "current_user", None)
        if not user:
            self.query_one("#msg", Static).update("[red]⚠ Usuário não autenticado.[/]")
            return

        description = self.query_one("#description-area", TextArea).text.strip()

        success, message = self._mood_model.save_entry(
            user_id=user["id"],
            mood_level=self._selected_mood,
            description=description,
        )

        if success:
            self.query_one("#msg", Static).update(f"[green]✓ {message}[/]")
            self._selected_mood = None
            for i in range(1, 7):
                self.query_one(f"#mood-{i}", Button).remove_class("selected")
            self.query_one("#selected-label", Static).update("Selecione um emoji acima ↑")
            self.query_one("#description-area", TextArea).clear()
        else:
            self.query_one("#msg", Static).update(f"[red]⚠ {message}[/]")

    def action_go_back(self) -> None:
        """Volta para o menu principal."""
        self.app.pop_screen()