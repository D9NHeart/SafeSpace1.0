"""
O arquivo do banco é criado automaticamente na pasta do projeto.
"""

import sqlite3
import os

# Caminho do arquivo .db na mesma pasta do projeto
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_BASE_DIR, "safespace.db")


def get_connection() -> sqlite3.Connection:
    """
    Configura para retornar linhas como dicionários e habilita o suporte a chaves estrangeiras.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    """
    Inicializa o banco de dados criando as tabelas necessárias
    caso elas ainda não existam. Deve ser chamada na inicialização do app.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT,
            email             TEXT    NOT NULL UNIQUE,
            password_hash     TEXT    NOT NULL,
            emergency_contact TEXT,
            calm_timer        INTEGER DEFAULT 3,
            created_at        TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            mood_level  INTEGER NOT NULL,
            description TEXT,
            recorded_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_checklist (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            check_date    TEXT    NOT NULL,
            ate_today     INTEGER DEFAULT 0,
            took_meds     INTEGER DEFAULT 0,
            updated_at    TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(user_id, check_date),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Migrações seguras: adicionam colunas novas em bancos já existentes
    migrations = [
        "ALTER TABLE users ADD COLUMN name TEXT",
        "ALTER TABLE users ADD COLUMN calm_timer INTEGER DEFAULT 3",
        "ALTER TABLE users ADD COLUMN needs_food_reminder INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN needs_medication_reminder INTEGER DEFAULT 0",
    ]
    for migration in migrations:
        try:
            cursor.execute(migration)
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Coluna já existe, tudo certo

    conn.commit()
    cursor.close()
    conn.close()


# ---------------------------------------------------------------------------
# Helpers para o checklist diário
# ---------------------------------------------------------------------------

def get_today_checklist(user_id: int) -> dict:
    """
    Retorna o registro de checklist do dia atual para o usuário.
    Se não existir, retorna valores padrão (não marcado).
    """
    from datetime import date
    today = date.today().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ate_today, took_meds FROM daily_checklist WHERE user_id = ? AND check_date = ?",
        (user_id, today),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"ate_today": bool(row["ate_today"]), "took_meds": bool(row["took_meds"])}
    return {"ate_today": False, "took_meds": False}


def upsert_checklist(user_id: int, ate_today: bool = None, took_meds: bool = None) -> None:
    """
    Insere ou atualiza o checklist do dia.  Apenas os campos passados como
    não-None são alterados; o outro permanece com o valor existente.
    """
    from datetime import date
    today = date.today().isoformat()
    conn = get_connection()
    cursor = conn.cursor()

    # Garante que a linha existe
    cursor.execute(
        "INSERT OR IGNORE INTO daily_checklist (user_id, check_date) VALUES (?, ?)",
        (user_id, today),
    )

    if ate_today is not None:
        cursor.execute(
            "UPDATE daily_checklist SET ate_today = ?, updated_at = datetime('now','localtime') "
            "WHERE user_id = ? AND check_date = ?",
            (int(ate_today), user_id, today),
        )

    if took_meds is not None:
        cursor.execute(
            "UPDATE daily_checklist SET took_meds = ?, updated_at = datetime('now','localtime') "
            "WHERE user_id = ? AND check_date = ?",
            (int(took_meds), user_id, today),
        )

    conn.commit()
    cursor.close()
    conn.close()