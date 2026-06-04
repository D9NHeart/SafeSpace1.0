"""
Tela de Relatórios
"""

from datetime import date
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from mood_model import MoodModel
from mood_utils import (
    compute_daily_averages,
    compute_period_average,
    generate_period_chart,
    get_week_dates,
    get_month_dates,
    mood_to_emoji,
    mood_to_label,
    MOOD_EMOJIS,
)


class ReportsScreen(Screen):

    CSS = """
    ReportsScreen {
        align: center middle;
        background: $background;
    }

    #reports-container {
        width: 70;
        height: 90vh;
        padding: 1 3;
        border: double $secondary;
        background: $surface;
    }

    #reports-title {
        text-align: center;
        color: $secondary;
        text-style: bold;
        margin-bottom: 1;
    }

    #period-selector {
        height: auto;
        align: center middle;
        margin-bottom: 1;
    }

    .period-btn {
        width: 14;
        margin: 0 1;
    }

    .period-btn.active {
        background: $secondary;
        text-style: bold;
    }

    #nav-row {
        height: auto;
        align: center middle;
        margin-bottom: 1;
    }

    #period-label {
        text-align: center;
        color: $text;
        text-style: bold;
        width: 30;
    }

    .nav-btn {
        width: 12;
    }

    #chart-scroll {
        height: 1fr;
        border: solid $surface-lighten-1;
        padding: 1;
        margin-bottom: 1;
    }

    #chart-content {
        color: $text;
    }

    #legend-row {
        height: auto;
        margin-bottom: 1;
    }

    #legend {
        color: $text-muted;
        text-align: center;
    }

    #avg-label {
        text-align: center;
        color: $success;
        text-style: bold;
        height: 1;
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

    #no-data {
        text-align: center;
        color: $text-muted;
        padding: 3;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Voltar"),
        ("left", "nav_prev", "Anterior"),
        ("right", "nav_next", "Próximo"),
    ]

    def __init__(self):

        super().__init__()
        self._mood_model = MoodModel()
        self._mode: str = "week"
        self._offset: int = 0
        self._today = date.today()

    def compose(self) -> ComposeResult:
        """widgets da tela """
        with Container(id="reports-container"):
            yield Static("📊  Relatórios de Humor", id="reports-title")

            with Horizontal(id="period-selector"):
                yield Button("📅  Semana", id="btn-week", classes="period-btn active")
                yield Button("🗓  Mês", id="btn-month", classes="period-btn")

            with Horizontal(id="nav-row"):
                yield Button("◀ Anterior", id="btn-prev", classes="nav-btn")
                yield Static("", id="period-label")
                yield Button("Próximo ▶", id="btn-next", classes="nav-btn")

            with ScrollableContainer(id="chart-scroll"):
                yield Static("", id="chart-content")

            yield Static("", id="avg-label")

            with Horizontal(id="legend-row"):
                yield Static(
                    "  ".join(f"{MOOD_EMOJIS[i]}={i}" for i in range(1, 7)),
                    id="legend",
                )

            yield Button("← Voltar ao Menu", id="btn-back")
            yield Static("[dim]ESC: Voltar │ ←/→: Navegar períodos[/]", id="footer-hint")

    def on_mount(self) -> None:
       
        self._render_report()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Trata todos os cliques de botões
        """
        btn_id = event.button.id

        if btn_id == "btn-week":
            self._mode = "week"
            self._offset = 0
            self._update_period_buttons()
            self._render_report()

        elif btn_id == "btn-month":
            self._mode = "month"
            self._offset = 0
            self._update_period_buttons()
            self._render_report()

        elif btn_id == "btn-prev":
            self.action_nav_prev()

        elif btn_id == "btn-next":
            self.action_nav_next()

        elif btn_id == "btn-back":
            self.action_go_back()

    def _update_period_buttons(self) -> None:
        """
        Atualiza o estilo visual dos botões de modo (semana/mês)
        """
        week_btn = self.query_one("#btn-week", Button)
        month_btn = self.query_one("#btn-month", Button)
        if self._mode == "week":
            week_btn.add_class("active")
            month_btn.remove_class("active")
        else:
            month_btn.add_class("active")
            week_btn.remove_class("active")

    def _get_period_dates(self) -> list[date]:

        if self._mode == "week":
            return get_week_dates(self._today, self._offset)
        else:
            return get_month_dates(self._today, self._offset)

    def _get_period_label(self, dates: list[date]) -> str:
        """
        Gera o rótulo textual do período exibido no cabeçalho do relatório.
        """
        MONTHS_PT = [
            "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
        ]
        if not dates:
            return ""
        if self._mode == "week":
            return f"{dates[0].strftime('%d/%m')} – {dates[-1].strftime('%d/%m/%Y')}"
        else:
            return f"{MONTHS_PT[dates[0].month]}/{dates[0].year}"

    def _render_report(self) -> None:
    
        user = getattr(self.app, "current_user", None)
        if not user:
            return

        period_dates = self._get_period_dates()
        label = self._get_period_label(period_dates)
        self.query_one("#period-label", Static).update(label)

        entries = self._mood_model.get_entries_by_period(
            user["id"], period_dates[0], period_dates[-1]
        )

        daily_avgs = compute_daily_averages(entries)

        btn_next = self.query_one("#btn-next", Button)
        btn_next.disabled = self._offset >= 0

        if not entries:
            chart_text = "\n\n  📭  Nenhum registro neste período.\n\n  Use o Tracking de Humor para registrar seus dados!"
            self.query_one("#chart-content", Static).update(chart_text)
            self.query_one("#avg-label", Static).update("")
            return

        chart = generate_period_chart(daily_avgs, period_dates)
        self.query_one("#chart-content", Static).update(chart)

        period_avg = compute_period_average(daily_avgs)
        if period_avg is not None:
            emoji = mood_to_emoji(period_avg)
            label_text = mood_to_label(round(period_avg))
            self.query_one("#avg-label", Static).update(
                f"Média do período: {emoji} {period_avg:.2f} – {label_text}"
            )

    def action_nav_prev(self) -> None:
        """
        Navega para o período anterior (semana ou mês).

        """
        user = getattr(self.app, "current_user", None)
        if not user:
            return

        earliest = self._mood_model.get_earliest_entry_date(user["id"])
        if earliest is None:
            return

        new_offset = self._offset - 1

        if self._mode == "week":
            test_dates = get_week_dates(self._today, new_offset)
        else:
            test_dates = get_month_dates(self._today, new_offset)

        
        if test_dates[-1] >= earliest:
            self._offset = new_offset
            self._render_report()

    def action_nav_next(self) -> None:
        """
        Navega para o próximo período
        """
        if self._offset < 0:
            self._offset += 1
            self._render_report()

    def action_go_back(self) -> None:
        """Volta para o menu principal."""
        self.app.pop_screen()
