"""
Modelo de usuário responsável pelas operações de banco de dados
relacionadas a autenticação, cadastro e perfil do usuário.
"""

import hashlib
import os
from database import get_connection


def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Gera um hash para a senha 
    """
    if salt is None:
        salt = os.urandom(32).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt
 

def _verify_password(password: str, stored_hash: str) -> bool:

    try:
        salt, expected_hash = stored_hash.split(":", 1)
        actual_hash, _ = _hash_password(password, salt)
        return actual_hash == expected_hash
    except Exception:
        return False


class UserModel:

    def register(self, name: str, email: str, password: str, emergency_contact: str = "") -> tuple[bool, str]:

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
            if cursor.fetchone():
                return False, "Este email já está cadastrado."

            password_hash, salt = _hash_password(password)
            stored = f"{salt}:{password_hash}"
            contact = emergency_contact.strip() if emergency_contact else None

            cursor.execute(
                "INSERT INTO users (name, email, password_hash, emergency_contact) VALUES (?, ?, ?, ?)",
                (name, email.lower(), stored, contact),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Cadastro realizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao cadastrar: {e}"

    def login(self, email: str, password: str) -> tuple[bool, dict | str]:

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, email, password_hash, emergency_contact FROM users WHERE email = ?",
                (email.lower(),),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if not row:
                return False, "Email não encontrado."

            if not _verify_password(password, row["password_hash"]):
                return False, "Senha incorreta."

            return True, {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "emergency_contact": row["emergency_contact"],
            }
        except Exception as e:
            return False, f"Erro ao fazer login: {e}"

    def get_by_id(self, user_id: int) -> dict | None:

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email, emergency_contact FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return dict(row) if row else None
        except Exception:
            return None

    def update_user(self, user_id: int, name: str, email: str, emergency_contact: str = "") -> tuple[bool, str]:
        """
        Atualiza os dados do usuário (nome, email e contato de emergência)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET name = ?, email = ?, emergency_contact = ? WHERE id = ?",
                (name, email.lower(), emergency_contact, user_id),
            )

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Dados atualizados com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar: {e}"

    def delete_user(self, user_id: int) -> tuple[bool, str]:
        """
        DELETE: remove um usuário do banco de dados permanentemente.
        Usado quando o usuário deseja excluir sua conta.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

            cursor.close()
            conn.close()
            return True, "Usuário removido com sucesso."
        except Exception as e:
            return False, f"Erro ao deletar usuário: {e}"