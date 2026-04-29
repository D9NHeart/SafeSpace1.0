"""
Módulo de utilitários para validação 
"""

import re


VALID_EMAIL_DOMAINS = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com",
    "icloud.com", "live.com", "ufrpe.br", "usp.br", "unicamp.br",
    "ufrj.br", "ufmg.br", "ufc.br", "ufba.br", "protonmail.com",
    "ufpe.br", "ufpb.br", "ufam.br", "unb.br", "edu.br",
]


def validate_email(email: str) -> tuple[bool, str]:

    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return False, "Formato de email inválido."

    domain = email.split("@")[1]
    if not any(email.endswith(d) for d in VALID_EMAIL_DOMAINS):
        return False, f"Domínio '@{domain}' não é aceito. Use Gmail, Hotmail, Outlook, etc."

    return True, "Email válido."


def validate_password(password: str) -> tuple[bool, str]:

    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."

    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos 1 letra maiúscula."

    if len(re.findall(r"\d", password)) < 2:
        return False, "A senha deve conter pelo menos 2 números."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_=+\[\]\\;'/`~]", password):
        return False, "A senha deve conter pelo menos 1 caractere especial."

    return True, "Senha válida."


def validate_phone(phone: str) -> tuple[bool, str]:

    if not phone or phone.strip() == "":
        return True, "Contato opcional não informado."

    digits = re.sub(r"\D", "", phone)

    if len(digits) < 10 or len(digits) > 11:
        return False, "Telefone inválido. Use formato: (XX) XXXXX-XXXX"

    return True, "Telefone válido."


def format_phone(phone: str) -> str:
    
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return phone
