"""
Tela de Cadastro 
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label
from textual.containers import Container, Vertical, ScrollableContainer
from user_model import UserModel
from validators import validate_email, validate_password, validate_phone, format_phone


class RegisterScreen(Screen):


    CSS = """
    RegisterScreen {
        align: center middle;
        background: $background;
    }

    #register-container {
        width: 56;
        height: auto;
        max-height: 90vh;
        padding: 2 4;
        border: double $success;
        background: $surface;
    }

    #register-title {
        text-align: center;
        color: $success;
        text-style: bold;
        margin-bottom: 1;
    }

    #register-subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    .field-label {
        color: $text-muted;
        margin-top: 1;
    }

    .field-hint {
        color: $text-disabled;
        margin-bottom: 1;
    }

    Input {
        margin-bottom: 0;
    }

    .field-error {
        color: $error;
        height: 1;
    }

    #global-error {
        color: $error;
        text-align: center;
        height: 1;
        margin-top: 1;
    }

    #global-success {
        color: $success;
        text-align: center;
        height: 1;
        margin-top: 1;
    }

    #btn-do-register {
        width: 100%;
        background: $success;
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

    #password-rules {
        color: $text-muted;
        background: $surface-darken-1;
        padding: 1;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Voltar"),
    ]

    def __init__(self):
        """Inicializa a tela de cadastro com o modelo de usuário."""
        super().__init__()
        self._user_model = UserModel()

    def compose(self) -> ComposeResult:
        """widgets da tela"""
        with ScrollableContainer(id="register-container"):
            yield Static("📝  Criar Conta", id="register-title")
            yield Static("Crie sua conta no SafeSpace", id="register-subtitle")

            yield Label("📧  Email:", classes="field-label")
            yield Input(placeholder="seu@email.com", id="email-input")
            yield Static("", id="email-error", classes="field-error")

            yield Label("🔒  Senha:", classes="field-label")
            yield Static(
                "Mín. 8 chars │ 1 maiúscula │ 2 números │ 1 especial",
                id="password-rules",
            )
            yield Input(placeholder="••••••••", password=True, id="password-input")
            yield Static("", id="password-error", classes="field-error")

            yield Label("🔒  Confirmar Senha:", classes="field-label")
            yield Input(placeholder="••••••••", password=True, id="confirm-input")
            yield Static("", id="confirm-error", classes="field-error")

            yield Label("📱  Contato de Emergência (opcional):", classes="field-label")
            yield Static("Ex: (81) 99999-9999", classes="field-hint")
            yield Input(placeholder="(XX) XXXXX-XXXX", id="phone-input")
            yield Static("", id="phone-error", classes="field-error")

            yield Static("", id="global-error")
            yield Static("", id="global-success")

            yield Button("Criar Conta ✓", id="btn-do-register")
            yield Button("← Voltar", id="btn-back")
            yield Static("[dim]ESC: Voltar[/]", id="footer-hint")

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "btn-back":
            self.action_go_back()
        elif event.button.id == "btn-do-register":
            self._attempt_register()

    def _clear_errors(self) -> None:

        for widget_id in ["email-error", "password-error", "confirm-error", "phone-error", "global-error", "global-success"]:
            self.query_one(f"#{widget_id}", Static).update("")

    def _attempt_register(self) -> None:
        """
        Coleta os dados do formulário e registra
        """
        self._clear_errors()
        has_error = False

        email = self.query_one("#email-input", Input).value.strip()
        password = self.query_one("#password-input", Input).value
        confirm = self.query_one("#confirm-input", Input).value
        phone = self.query_one("#phone-input", Input).value.strip()

        valid_email, email_msg = validate_email(email)
        if not valid_email:
            self.query_one("#email-error", Static).update(f"⚠ {email_msg}")
            has_error = True

        valid_pass, pass_msg = validate_password(password)
        if not valid_pass:
            self.query_one("#password-error", Static).update(f"⚠ {pass_msg}")
            has_error = True

        if password and confirm != password:
            self.query_one("#confirm-error", Static).update("⚠ As senhas não coincidem.")
            has_error = True

        if phone:
            valid_phone, phone_msg = validate_phone(phone)
            if not valid_phone:
                self.query_one("#phone-error", Static).update(f"⚠ {phone_msg}")
                has_error = True
            else:
                phone = format_phone(phone)

        if has_error:
            return

        success, message = self._user_model.register(email, password, phone)

        if not success:
            self.query_one("#global-error", Static).update(f"⚠ {message}")
        else:
            self.query_one("#global-success", Static).update(f"✓ {message}")
            self.app.push_screen("login")

    def action_go_back(self) -> None:
        """Volta para a tela inicial."""
        self.app.pop_screen()
