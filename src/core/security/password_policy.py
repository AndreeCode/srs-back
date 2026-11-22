from .common_passwords import COMMON_PASSWORDS

MIN_LENGTH = 8
MAX_LENGTH = 128


class PasswordPolicyError(ValueError):
    pass


def password_problems(password: str | None, username: str | None = None, dni: str | None = None) -> list[str]:
    value = password or ""
    if len(value) < MIN_LENGTH:
        return [f"La contrasena debe tener al menos {MIN_LENGTH} caracteres"]
    problems = []
    if len(value) > MAX_LENGTH:
        problems.append(f"La contrasena no debe superar {MAX_LENGTH} caracteres")
    if not (any(c.isdigit() for c in value) and any(c.isalpha() for c in value)):
        problems.append("La contrasena debe combinar letras y numeros")
    lowered = value.lower()
    if lowered in COMMON_PASSWORDS or lowered.rstrip("!.*#$@") in COMMON_PASSWORDS:
        problems.append("Esa contrasena es demasiado comun, elige otra")
    for personal in (username, dni):
        if personal and len(personal) >= 4 and personal.lower() in lowered:
            problems.append("La contrasena no puede contener tu usuario ni tu DNI")
            break
    return problems


def ensure_strong_password(password: str | None, username: str | None = None, dni: str | None = None) -> None:
    problems = password_problems(password, username, dni)
    if problems:
        raise PasswordPolicyError("; ".join(problems))
