import re

from .common_passwords import COMMON_PASSWORDS

APP_WORDS = ("sicna", "signa", "sisnat")

MIN_LENGTH = 8
MAX_LENGTH = 128


class PasswordPolicyError(ValueError):
    pass


def context_words(values: tuple[str | None, ...]) -> set[str]:
    words: set[str] = set(APP_WORDS)
    for value in values:
        if not value:
            continue
        value = value.strip().lower().split("@")[0]
        words.add(value)
        words.update(re.split(r"[\s._-]+", value))
    return {word for word in words if len(word) >= 4}


def password_problems(
    password: str | None, username: str | None = None, dni: str | None = None, *others: str | None
) -> list[str]:
    value = password or ""
    if len(value) < MIN_LENGTH:
        return [f"La contrasena debe tener al menos {MIN_LENGTH} caracteres"]
    problems = []
    if len(value) > MAX_LENGTH:
        problems.append(f"La contrasena no debe superar {MAX_LENGTH} caracteres")
    lowered = value.lower()
    if lowered in COMMON_PASSWORDS or lowered.rstrip("!.*#$@") in COMMON_PASSWORDS:
        problems.append("Esa contrasena es demasiado comun, elige otra")
    if any(word in lowered for word in context_words((username, dni, *others))):
        problems.append("La contrasena no puede contener tu usuario, DNI, nombre, correo ni el nombre del sistema")
    return problems


def ensure_strong_password(
    password: str | None, username: str | None = None, dni: str | None = None, *others: str | None
) -> None:
    problems = password_problems(password, username, dni, *others)
    if problems:
        raise PasswordPolicyError("; ".join(problems))
