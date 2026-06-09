"""
Tela de Configurações do SafeSpace.
Segue o mesmo padrão estrutural de register_screen.py:
ScrollableContainer como raiz, sem Container com altura fixa envolvendo.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label, Checkbox
from textual.containers import ScrollableContainer, Vertical
from user_model import UserModel
from validators import validate_phone, format_phone


# ---------------------------------------------------------------------------
# Helpers de banco
# ---------------------------------------------------------------------------

def _update_calm_timer(user_id: int, minutes: int) -> tuple[bool, str]:
    from database import get_connection
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET calm_timer = ? WHERE id = ?", (minutes, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Timer atualizado."
    except Exception as e:
        return False, f"Erro ao atualizar timer: {e}"


def _update_wellness_reminders(user_id: int, needs_food: bool, needs_meds: bool) -> tuple[bool, str]:
    from database import get_connection
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET needs_food_reminder = ?, needs_medication_reminder = ? WHERE id = ?",
            (int(needs_food), int(needs_meds), user_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Lembretes atualizados."
    except Exception as e:
        return False, f"Erro ao atualizar lembretes: {e}"


def _update_name_and_phone(user_id: int, name: str, phone: str) -> tuple[bool, str]:
    from database import get_connection
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, emergency_contact = ? WHERE id = ?",
            (name, phone or None, user_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Dados atualizados."
    except Exception as e:
        return False, f"Erro ao atualizar: {e}"


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

TIMER_OPTIONS = [3, 5, 10]


# ---------------------------------------------------------------------------
# Tela
# ---------------------------------------------------------------------------

class SettingsScreen(Screen):

    CSS = """
    SettingsScreen {
        align: center middle;
        background: $background;
    }

    /* raiz — igual ao register_screen */
    #settings-container {
        width: 56;
        height: auto;
        max-height: 90vh;
        padding: 2 4;
        border: double $primary;
        background: $surface;
    }

    /* título */
    #settings-title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 0;
    }

    #settings-subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    /* separadores de seção */
    .section-title {
        color: $primary;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    /* campos */
    .field-label {
        color: $text-muted;
        margin-top: 1;
    }

    .field-hint {
        color: $text-disabled;
        margin-bottom: 0;
    }

    .field-error {
        color: $error;
        height: 1;
    }

    Input {
        margin-bottom: 0;
    }

    /* checkboxes */
    .timer-check {
        margin-bottom: 1;
    }

    .wellness-check {
        margin-bottom: 1;
    }

    /* hint abaixo dos títulos de seção */
    .section-hint {
        color: $text-muted;
        margin-bottom: 1;
    }

    /* divisor visual entre seções */
    .divider {
        height: 1;
        color: $surface-lighten-1;
        margin-top: 1;
        margin-bottom: 1;
    }

    /* mensagem global */
    #msg-global {
        text-align: center;
        height: 1;
        margin-top: 1;
        margin-bottom: 1;
    }

    /* botões */
    #btn-save {
        width: 100%;
        background: $success;
        margin-top: 1;
        margin-bottom: 1;
    }

    #btn-back {
        width: 100%;
        background: $surface-darken-1;
        margin-bottom: 1;
    }

    #footer-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }

    /* zona de perigo */
    .danger-title {
        color: $error;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    #btn-delete {
        width: 100%;
        background: $error;
        margin-bottom: 1;
    }

    #delete-warning {
        color: $warning;
        text-align: center;
        margin-bottom: 1;
    }

    #btn-confirm-delete {
        width: 100%;
        background: $error;
        margin-bottom: 1;
    }

    #btn-cancel-delete {
        width: 100%;
        background: $surface-darken-1;
        margin-bottom: 1;
    }
    """

    BINDINGS = [("escape", "go_back", "Voltar")]

    def __init__(self):
        super().__init__()
        self._user_model = UserModel()
        self._delete_confirm_visible = False
        self._selected_timer: int = 3

    # ------------------------------------------------------------------
    # Composição — mesmo padrão de register_screen.py
    # ------------------------------------------------------------------

    def compose(self) -> ComposeResult:
        user = getattr(self.app, "current_user", {}) or {}
        self._selected_timer = user.get("calm_timer", 3)
        needs_food = user.get("needs_food_reminder", False)
        needs_meds = user.get("needs_medication_reminder", False)

        with ScrollableContainer(id="settings-container"):

            yield Static("⚙️   Configurações", id="settings-title")
            yield Static("Personalize sua experiência no SafeSpace", id="settings-subtitle")

            # ── Seção 1: Perfil ──────────────────────────────────────
            yield Static("👤  Perfil", classes="section-title")

            yield Label("Nome:", classes="field-label")
            yield Input(
                value=user.get("name") or "",
                placeholder="Como posso te chamar?",
                id="name-input",
            )
            yield Static("", id="name-error", classes="field-error")

            yield Label("📱  Telefone de emergência:", classes="field-label")
            yield Static(
                "Deixe em branco para remover  •  Ex: (81) 99999-9999",
                classes="field-hint",
            )
            yield Input(
                value=user.get("emergency_contact") or "",
                placeholder="(XX) XXXXX-XXXX",
                id="phone-input",
            )
            yield Static("", id="phone-error", classes="field-error")

            # ── Seção 2: Sessão de Calma ─────────────────────────────
            yield Static("─" * 48, classes="divider")
            yield Static("🌙  Sessão de Calma", classes="section-title")
            yield Static(
                "Duração da sessão na tela de Momento de Calma:",
                classes="section-hint",
            )

            for mins in TIMER_OPTIONS:
                label = f"{mins} minutos" + ("  (padrão)" if mins == 3 else "")
                yield Checkbox(
                    label,
                    id=f"timer-{mins}",
                    value=(mins == self._selected_timer),
                    classes="timer-check",
                )

            # ── Seção 3: Lembretes de Bem-Estar ──────────────────────
            yield Static("─" * 48, classes="divider")
            yield Static("🌱  Lembretes de Bem-Estar", classes="section-title")
            yield Static(
                "Exibe avisos no menu quando você ainda não completou o item hoje:",
                classes="section-hint",
            )

            yield Checkbox(
                "🍽️  Lembrar de me alimentar todos os dias",
                id="food-check",
                value=needs_food,
                classes="wellness-check",
            )
            yield Checkbox(
                "💊  Lembrar de tomar meus medicamentos",
                id="meds-check",
                value=needs_meds,
                classes="wellness-check",
            )

            # ── Zona de Perigo ────────────────────────────────────────
            yield Static("─" * 48, classes="divider")
            yield Static("⚠️   Zona de Perigo", classes="danger-title")
            yield Button("🗑️  Excluir minha conta", id="btn-delete")
            yield Static(
                "Todos os dados serão apagados permanentemente.\nEssa ação não pode ser desfeita.",
                id="delete-warning",
            )
            yield Button("✓  Sim, excluir tudo", id="btn-confirm-delete")
            yield Button("✕  Cancelar exclusão", id="btn-cancel-delete")

            # ── Rodapé ────────────────────────────────────────────────
            yield Static("─" * 48, classes="divider")
            yield Static("", id="msg-global")
            yield Button("💾  Salvar Alterações", id="btn-save")
            yield Button("← Voltar ao Menu", id="btn-back")
            yield Static("[dim]ESC: Voltar[/]", id="footer-hint")

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------

    def on_mount(self) -> None:
        self.query_one("#delete-warning").display = False
        self.query_one("#btn-confirm-delete").display = False
        self.query_one("#btn-cancel-delete").display = False

    # ------------------------------------------------------------------
    # Checkboxes de timer — exclusão mútua
    # ------------------------------------------------------------------

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        cb_id = event.checkbox.id
        timer_ids = [f"timer-{m}" for m in TIMER_OPTIONS]

        if cb_id not in timer_ids:
            return

        # Impede desmarcar sem selecionar outro
        if not event.value:
            parsed = int(cb_id.split("-")[1])
            if parsed == self._selected_timer:
                event.checkbox.value = True
            return

        # Desmarca os outros e atualiza seleção
        new_mins = int(cb_id.split("-")[1])
        self._selected_timer = new_mins
        for mins in TIMER_OPTIONS:
            if mins != new_mins:
                try:
                    self.query_one(f"#timer-{mins}", Checkbox).value = False
                except Exception:
                    pass

    # ------------------------------------------------------------------
    # Botões
    # ------------------------------------------------------------------

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-save":
            self._save_settings()
        elif btn_id == "btn-back":
            self.action_go_back()
        elif btn_id == "btn-delete":
            self._toggle_delete_confirm()
        elif btn_id == "btn-confirm-delete":
            self._delete_account()
        elif btn_id == "btn-cancel-delete":
            self._hide_delete_confirm()

    # ------------------------------------------------------------------
    # Salvar
    # ------------------------------------------------------------------

    def _clear_errors(self) -> None:
        for wid in ["name-error", "phone-error"]:
            self.query_one(f"#{wid}", Static).update("")
        self.query_one("#msg-global", Static).update("")

    def _save_settings(self) -> None:
        self._clear_errors()

        user = getattr(self.app, "current_user", None)
        if not user:
            self.query_one("#msg-global", Static).update("[red]⚠ Usuário não autenticado.[/]")
            return

        name = self.query_one("#name-input", Input).value.strip()
        phone = self.query_one("#phone-input", Input).value.strip()
        has_error = False

        if not name:
            self.query_one("#name-error", Static).update("⚠ Nome é obrigatório.")
            has_error = True

        formatted_phone = ""
        if phone:
            valid_phone, phone_msg = validate_phone(phone)
            if not valid_phone:
                self.query_one("#phone-error", Static).update(f"⚠ {phone_msg}")
                has_error = True
            else:
                formatted_phone = format_phone(phone)

        if has_error:
            return

        needs_food = self.query_one("#food-check", Checkbox).value
        needs_meds = self.query_one("#meds-check", Checkbox).value

        ok, msg = _update_name_and_phone(user["id"], name, formatted_phone or "")
        if not ok:
            self.query_one("#msg-global", Static).update(f"[red]⚠ {msg}[/]")
            return

        _update_calm_timer(user["id"], self._selected_timer)
        _update_wellness_reminders(user["id"], needs_food, needs_meds)

        updated = self._user_model.get_by_id(user["id"])
        if updated:
            updated["calm_timer"] = self._selected_timer
            self.app.current_user = updated

        self.query_one("#msg-global", Static).update("[green]✓ Configurações salvas com sucesso![/]")

    # ------------------------------------------------------------------
    # Exclusão de conta
    # ------------------------------------------------------------------

    def _toggle_delete_confirm(self) -> None:
        if self._delete_confirm_visible:
            self._hide_delete_confirm()
        else:
            self._show_delete_confirm()

    def _show_delete_confirm(self) -> None:
        self._delete_confirm_visible = True
        self.query_one("#delete-warning").display = True
        self.query_one("#btn-confirm-delete").display = True
        self.query_one("#btn-cancel-delete").display = True
        self.query_one("#btn-delete", Button).label = "↑ Cancelar exclusão"

    def _hide_delete_confirm(self) -> None:
        self._delete_confirm_visible = False
        self.query_one("#delete-warning").display = False
        self.query_one("#btn-confirm-delete").display = False
        self.query_one("#btn-cancel-delete").display = False
        self.query_one("#btn-delete", Button).label = "🗑️  Excluir minha conta"

    def _delete_account(self) -> None:
        user = getattr(self.app, "current_user", None)
        if not user:
            return
        ok, msg = self._user_model.delete_user(user["id"])
        if not ok:
            self.query_one("#msg-global", Static).update(f"[red]⚠ {msg}[/]")
            return
        from login_screen import clear_session
        clear_session()
        self.app.current_user = None
        while len(self.app.screen_stack) > 1:
            self.app.pop_screen()

    # ------------------------------------------------------------------
    # Navegação
    # ------------------------------------------------------------------

    def action_go_back(self) -> None:
        self.app.pop_screen()
