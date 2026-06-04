def format_note(note):
    """
    Formata a nota para exibição no listbox
    Ex: (1, "texto") → "ID 1: texto"
    """
    return f"ID {note[0]}: {note[1]}"


def validate_note(text):
    """
    Valida se a nota não está vazia ou inválida.
    Retorna (True, "") se válido
    Retorna (False, mensagem_erro) se inválido
    """
    if not text or text.strip() == "":
        return False, "❌ Erro: A anotação não pode estar vazia."

    if len(text.strip()) < 3:
        return False, "❌ Erro: A anotação deve ter pelo menos 3 caracteres."

    return True, ""


def truncate_text(text, limit=30):
    """
    Limita o tamanho do texto para exibição
    """
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def search_notes(notes, keyword):
    """
    Filtra notas que contenham a palavra-chave
    """
    if not keyword or keyword.strip() == "":
        return notes  # retorna tudo se busca vazia

    return [note for note in notes if keyword.lower() in note[1].lower()]


def count_notes(notes):
    """
    Retorna quantidade de notas
    """
    return len(notes)


def get_note_by_id(notes, note_id):
    """
    Retorna uma nota específica pelo ID
    """
    for note in notes:
        if note[0] == note_id:
            return note
    return None


def format_error(message):
    """
    Padroniza mensagens de erro
    """
    return f"⚠️ {message}"


def format_success(message):
    """
    Padroniza mensagens de sucesso
    """
    return f"✅ {message}"