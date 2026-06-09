"""
SafeSpace - Aplicação de Controle de Humor
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textual.app import App, ComposeResult
from textual.widgets import Static

from database import initialize_database
from home_screen import HomeScreen
from login_screen import LoginScreen, load_session
from register_screen import RegisterScreen
from menu_screen import MenuScreen
from tracking_screen import TrackingScreen
from reports_screen import ReportsScreen
from emergency_screen import EmergencyScreen
from meltdown_screen import CalmScreen
from settings_screen import SettingsScreen


class SafeSpaceApp(App):

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
        "calm": CalmScreen,
        "emergency": EmergencyScreen,
        "settings": SettingsScreen,
    }

    def __init__(self):
        super().__init__()
        self.current_user: dict | None = None

    def on_mount(self) -> None:
        from user_model import UserModel
        user_id = load_session()
        if user_id:
            user = UserModel().get_by_id(user_id)
            if user:
                self.current_user = user
                self.push_screen("menu")
                return
        self.push_screen("home")


def main():
    print("🌿 Iniciando SafeSpace...")
    try:
        initialize_database()
        print("✓ Banco de dados inicializado.")
    except Exception as e:
        print(f"\n❌ Erro ao inicializar a aplicação: {e}")
        sys.exit(1)

    app = SafeSpaceApp()
    app.run()


if __name__ == "__main__":
    main()
