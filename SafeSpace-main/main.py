"""
SafeSpace - Aplicação de Controle de Humor
==========================================
Ponto de entrada principal da aplicação 
construída com Textual e Sqlite.

Módulos:
    config/database.py   - Configuração e inicialização do banco de dados
    models/user_model.py  - Operações de usuário no banco
    models/mood_model.py  - Operações de humor no banco
    utils/validators.py  - Validação de email, senha e telefone
    utils/mood_utils.py  - Utilitários de humor (emojis, gráficos)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textual.app import App, ComposeResult
from textual.widgets import Static

from database import initialize_database
from home_screen import HomeScreen
from login_screen import LoginScreen
from register_screen import RegisterScreen
from menu_screen import MenuScreen
from tracking_screen import TrackingScreen
from reports_screen import ReportsScreen
from emergency_screen import EmergencyScreen


class SafeSpaceApp(App):
    """
    Classe principal da aplicação SafeSpace.
    Gerencia todas as telas, o usuário atual e o tema visual.
    """

    TITLE = "SafeSpace 🌿"
    SUB_TITLE = "Seu espaço seguro de bem-estar"

    CSS = """
    Button {
        border: none;
        padding: 0 2;
    }

    Button:hover {
        opacity: 0.85;
    }

    Input {
        border: tall $primary 60%;
    }

    Input:focus {
        border: tall $primary;
    }

    TextArea {
        border: tall $primary 60%;
    }

    TextArea:focus {
        border: tall $primary;
    }
    """

    SCREENS = {
        "home": HomeScreen,
        "login": LoginScreen,
        "register": RegisterScreen,
        "menu": MenuScreen,
        "tracking": TrackingScreen,
        "reports": ReportsScreen,
        "emergency": EmergencyScreen,
    }

    def __init__(self):
        super().__init__()
        self.current_user: dict | None = None

    def on_mount(self) -> None:
        self.push_screen("home")


def main():

    print("🌿 Iniciando SafeSpace...")

    try:
        initialize_database()
        print("✓ Banco de dados SQLite inicializado.")
    except Exception as e:
        print(f"\n❌ Erro ao inicializar o banco de dados: {e}")
        sys.exit(1)

    app = SafeSpaceApp()
    app.run()


if __name__ == "__main__":
    main()
