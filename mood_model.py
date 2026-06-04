"""
Modelo de entradas de humor responsável pelas operações de banco de dados
relacionadas ao tracking e consulta do histórico de humor do usuário.
"""

from datetime import date, datetime
from database import get_connection


def _parse_recorded_at(value) -> datetime:
    """
    Converte o campo recorded_at para um objeto datetime do Python.
    """
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(value, fmt)
        except (ValueError, TypeError):
            continue
    # Fallback: retorna hoje à meia-noite se o parse falhar
    return datetime.now()


class MoodModel:
    """
    operações  relacionadas ao registro e consulta de humor do usuário.
    """

    def save_entry(self, user_id: int, mood_level: int, description: str = "") -> tuple[bool, str]:
        """
        Salva um novo registro de humor para o usuário.
        """
        try:
            if not 1 <= mood_level <= 6:
                return False, "Nível de humor deve ser entre 1 e 6."

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mood_entries (user_id, mood_level, description) VALUES (?, ?, ?)",
                (user_id, mood_level, description.strip() if description else None),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Humor registrado com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar registro: {e}"

    def get_entries_by_period(self, user_id: int, start: date, end: date) -> list[dict]:
        """
        Busca todas as entradas de humor do usuário em um período definido.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, mood_level, description, recorded_at
                FROM mood_entries
                WHERE user_id = ?
                  AND date(recorded_at) BETWEEN ? AND ?
                ORDER BY recorded_at ASC
                """,
                (user_id, start.isoformat(), end.isoformat()),
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            entries = []
            for row in rows:
                entries.append({
                    "id": row["id"],
                    "mood_level": row["mood_level"],
                    "description": row["description"],
                    "recorded_at": _parse_recorded_at(row["recorded_at"]),
                })
            return entries
        except Exception:
            return []

    def has_data_in_period(self, user_id: int, start: date, end: date) -> bool:
        """
        Verifica se o usuário possui algum registro de humor no período informado.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM mood_entries
                WHERE user_id = ?
                  AND date(recorded_at) BETWEEN ? AND ?
                """,
                (user_id, start.isoformat(), end.isoformat()),
            )
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count > 0
        except Exception:
            return False

    def get_earliest_entry_date(self, user_id: int) -> date | None:
        """
        Retorna a data do registro de humor mais antigo do usuário.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MIN(date(recorded_at)) FROM mood_entries WHERE user_id = ?",
                (user_id,),
            )
            result = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            if result is None:
                return None
            return date.fromisoformat(result)
        except Exception:
            return None
