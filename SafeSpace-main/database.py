"""
O arquivo do banco é criado automaticamente na pasta do projeto.
"""

import sqlite3
import os

# Caminho do arquivo .db relativo à raiz do projeto
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
            email             TEXT    NOT NULL UNIQUE,
            password_hash     TEXT    NOT NULL,
            emergency_contact TEXT,
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

    conn.commit()
    cursor.close()
    conn.close()
