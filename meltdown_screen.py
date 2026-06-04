"""
Tela de Momento de Calma — técnica 5-4-3-2-1 com ruído branco.
"""

import random
import threading
import os
import winsound
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical

SOUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "white_noise.wav")

MESSAGES = [
    "respire fundo... devagar...",
    "solte o ar lentamente.",
    "veja 5 coisas ao seu redor.",
    "toque 4 superfícies perto de você.",
    "ouça 3 sons ao redor.",
    "sinta 2 cheiros no ambiente.",
    "imagine o sabor de algo que você gosta.",
    "sinta seus pés no chão.",
    "relaxe os ombros.",
    "você está seguro(a) agora.",
    "esse momento vai passar.",
    "respire.",
]

NOISE_CHARS = ["·", "∘", "○", "◦", "⋅", " ", " ", " "]


def _play_loop(stop_event: threading.Event) -> None:
    try:
        winsound.PlaySound(SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        while not stop_event.is_set():
            import time
            time.sleep(0.5)
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass


class CalmScreen(Screen):

    CSS = """
    CalmScreen {
        align: center middle;
        background: #0f0a1a;
    }

    #calm-container {
        width: 52;
        height: auto;
        padding: 3 4;
        border: round #3d2b5e;
        background: #160d2b;
    }

    #calm-title {
        text-align: center;
        color: #9b7fd4;
        text-style: bold;
        margin-bottom: 2;
    }

    #calm-message {
        text-align: center;
        color: #c9b8e8;
        text-style: italic;
        height: 3;
        margin-bottom: 1;
    }

    #noise-bar {
        text-align: center;
        color: #2a1f3d;
        height: 1;
        margin-bottom: 2;
    }

    #calm-question {
        text-align: center;
        color: #c9b8e8;
        text-style: bold;
        margin-bottom: 2;
        height: 2;
    }

    .calm-btn {
        width: 100%;
        margin-bottom: 1;
    }

    #btn-better {
        background: #3d5a3e;
        color: #b8e8ba;
    }

    #btn-more-time {
        background: #3d3a5e;
        color: #b8b5e8;
    }

    #btn-emergency {
        background: #5e2a2a;
        color: #e8b8b8;
    }
    """

    def __init__(self):
        super().__init__()
        self._timer = None
        self._noise_timer = None
        self._message_timer = None
        self._seconds_remaining = 0
        self._message_index = 0
        self._stop_sound = threading.Event()
        self._sound_thread = None

    def compose(self) -> ComposeResult:
        with Container(id="calm-container"):
            yield Static("🌙  momento de calma", id="calm-title")
            yield Static("", id="calm-message")
            yield Static("", id="noise-bar")
            yield Static("", id="calm-question")
            with Vertical():
                yield Button("✓  sim, estou melhor", id="btn-better", classes="calm-btn")
                yield Button("🔄  preciso de mais tempo", id="btn-more-time", classes="calm-btn")
                yield Button("🆘  ligar para emergência", id="btn-emergency", classes="calm-btn")

    def on_mount(self) -> None:
        user = getattr(self.app, "current_user", {})
        minutes = user.get("calm_timer", 3) if user else 3
        self._start_session(minutes)
        self._start_sound()

    def _start_sound(self) -> None:
        self._stop_sound.clear()
        self._sound_thread = threading.Thread(
            target=_play_loop,
            args=(self._stop_sound,),
            daemon=True
        )
        self._sound_thread.start()

    def _stop_sound_playback(self) -> None:
        self._stop_sound.set()

    def _start_session(self, minutes: int) -> None:
        self._stop_timers()
        self._seconds_remaining = minutes * 60
        self._message_index = 0
        self._set_buttons_visible(False)
        self.query_one("#calm-question", Static).update("")
        self._show_next_message()
        self._timer = self.set_interval(1.0, self._tick)
        self._noise_timer = self.set_interval(0.4, self._update_noise)
        self._message_timer = self.set_interval(8.0, self._show_next_message)

    def _stop_timers(self) -> None:
        for t in [self._timer, self._noise_timer, self._message_timer]:
            if t:
                t.stop()
        self._timer = None
        self._noise_timer = None
        self._message_timer = None

    def _tick(self) -> None:
        self._seconds_remaining -= 1
        if self._seconds_remaining <= 0:
            self._finish_session()

    def _update_noise(self) -> None:
        try:
            self.query_one("#noise-bar", Static).update(
                "".join(random.choice(NOISE_CHARS) for _ in range(48))
            )
        except Exception:
            pass

    def _show_next_message(self) -> None:
        try:
            msg = MESSAGES[self._message_index % len(MESSAGES)]
            self.query_one("#calm-message", Static).update(f'"{msg}"')
            self._message_index += 1
        except Exception:
            pass

    def _finish_session(self) -> None:
        self._stop_timers()
        try:
            self.query_one("#calm-question", Static).update(
                "você se sente melhor agora?"
            )
            self._set_buttons_visible(True)
        except Exception:
            pass

    def _set_buttons_visible(self, visible: bool) -> None:
        for btn_id in ["btn-better", "btn-more-time", "btn-emergency"]:
            try:
                self.query_one(f"#{btn_id}", Button).visible = visible
            except Exception:
                pass

    def _leave(self) -> None:
        self._stop_timers()
        self._stop_sound_playback()
        if len(self.app.screen_stack) > 1:
            self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-better":
            self._leave()
        elif btn == "btn-more-time":
            user = getattr(self.app, "current_user", {})
            minutes = user.get("calm_timer", 3) if user else 3
            self._start_session(minutes)
        elif btn == "btn-emergency":
            self._stop_timers()
            self._stop_sound_playback()
            self.app.push_screen("emergency")