"""
Tela de Tracking de Humor
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, TextArea, Checkbox
from textual.containers import Container, Vertical, Horizontal
from mood_model import MoodModel
from mood_utils import MOOD_EMOJIS, MOOD_LABELS
from database import get_today_checklist, upsert_checklist


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
        margin-bottom: 2;
        border: solid $surface-lighten-1;
    }

    #wellness-title {
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }

    #ate-today-check {
        margin-bottom: 1;
    }

    #took-meds-check {
        margin-bottom: 1;
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
        with Container(id="tracking-container"):
            yield Static("💭  Como você está agora?", id="tracking-title")
            yield Static("Selecione o emoji que melhor representa seu humor:", id="tracking-subtitle")

            with Vertical(id="emoji-grid"):
                with Horizontal(classes="emoji-row"):
                    for level in range(1, 4):
                        yield Button(
                            f"{MOOD_EMOJIS[level]}  {MOOD_LABELS[level]}",
                            id=f"mood-{level}",
                            classes="emoji-btn",
                        )
                with Horizontal(classes="emoji-row"):
                    for level in range(4, 7):
                        yield Button(
                            f"{MOOD_EMOJIS[level]}  {MOOD_LABELS[level]}",
                            id=f"mood-{level}",
                            classes="emoji-btn",
                        )

            yield Static("Selecione um emoji acima ↑", id="selected-label")
            yield Static("📝  Como você está se sentindo? (opcional):", id="description-label")
            yield TextArea(id="description-area")

            # Placeholder onde os checkboxes serão injetados em on_mount
            yield Static("", id="wellness-anchor")

            yield Static("", id="msg")
            yield Button("💾  Salvar Registro", id="btn-save")
            yield Button("← Voltar ao Menu", id="btn-back")
            yield Static("[dim]ESC: Voltar[/]", id="footer-hint")

    def on_mount(self) -> None:
        user = getattr(self.app, "current_user", None) or {}
        user_id = user.get("id")
        needs_food = user.get("needs_food_reminder", False)
        needs_meds = user.get("needs_medication_reminder", False)

        if not (needs_food or needs_meds):
            return

        anchor = self.query_one("#wellness-anchor")
        checklist = get_today_checklist(user_id) if user_id else {}

        # Monta título
        anchor.update("✅  Checklist do dia:")
        anchor.styles.color = "rgb(150,120,255)"
        anchor.styles.text_style = "bold"
        anchor.styles.margin = (0, 0, 1, 0)

        container = self.query_one("#tracking-container")
        msg_widget = self.query_one("#msg")

        if needs_food:
            cb = Checkbox(
                "🍽️  Já me alimentei hoje",
                id="ate-today-check",
                value=checklist.get("ate_today", False),
            )
            container.mount(cb, before=msg_widget)

        if needs_meds:
            cb = Checkbox(
                "💊  Já tomei meus medicamentos hoje",
                id="took-meds-check",
                value=checklist.get("took_meds", False),
            )
            container.mount(cb, before=msg_widget)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        if btn_id and btn_id.startswith("mood-"):
            self._select_mood(int(btn_id.split("-")[1]))
        elif btn_id == "btn-save":
            self._save_entry()
        elif btn_id == "btn-back":
            self.action_go_back()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Persiste o checklist imediatamente ao marcar/desmarcar."""
        user = getattr(self.app, "current_user", None)
        if not user:
            return
        if event.checkbox.id == "ate-today-check":
            upsert_checklist(user["id"], ate_today=event.value)
        elif event.checkbox.id == "took-meds-check":
            upsert_checklist(user["id"], took_meds=event.value)

    def _select_mood(self, level: int) -> None:
        self._selected_mood = level
        for i in range(1, 7):
            btn = self.query_one(f"#mood-{i}", Button)
            btn.add_class("selected") if i == level else btn.remove_class("selected")
        self.query_one("#selected-label", Static).update(
            f"Selecionado: {MOOD_EMOJIS[level]}  {MOOD_LABELS[level]}"
        )
        self.query_one("#msg", Static).update("")

    def _save_entry(self) -> None:
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
            needs_food = user.get("needs_food_reminder", False)
            needs_meds = user.get("needs_medication_reminder", False)
            if needs_food or needs_meds:
                ate_val, meds_val = None, None
                try:
                    if needs_food:
                        ate_val = self.query_one("#ate-today-check", Checkbox).value
                except Exception:
                    pass
                try:
                    if needs_meds:
                        meds_val = self.query_one("#took-meds-check", Checkbox).value
                except Exception:
                    pass
                upsert_checklist(user["id"], ate_today=ate_val, took_meds=meds_val)

            self.query_one("#msg", Static).update(f"[green]✓ {message}[/]")
            self._selected_mood = None
            for i in range(1, 7):
                self.query_one(f"#mood-{i}", Button).remove_class("selected")
            self.query_one("#selected-label", Static).update("Selecione um emoji acima ↑")
            self.query_one("#description-area", TextArea).clear()
        else:
            self.query_one("#msg", Static).update(f"[red]⚠ {message}[/]")

    def action_go_back(self) -> None:
        self.app.pop_screen()
