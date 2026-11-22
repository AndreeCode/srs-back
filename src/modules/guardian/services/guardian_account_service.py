from dataclasses import replace
from uuid import uuid4

from ....core.security.password import hash_password
from ....core.security.password_policy import PasswordPolicyError, ensure_strong_password
from ...role.services.roles_service import roleService
from ...user.domain.user_domain import User
from ...user.repositories.user_repositories import userRepository
from ...user.services.users_service import userService
from ..domain.guardian_domain import Guardian
from ..domain.guardian_errors import GuardianValidationError
from ..repositories.guardian_repositories import guardianRepository


async def check_account(guardian: Guardian | None, username: str) -> None:
    if guardian is not None and guardian.user_id is not None:
        raise GuardianValidationError("El padre ya tiene una cuenta del portal")

    if await userService.get_by_username(username) is not None:
        raise GuardianValidationError(f"El usuario {username} ya existe, elige otro")


async def validate_new_account(guardian: Guardian | None, dni: str | None, username: str, password: str) -> None:
    await check_account(guardian, username)

    try:
        ensure_strong_password(password, username, dni)
    except PasswordPolicyError as err:
        raise GuardianValidationError(str(err)) from err


async def create_account(guardian: Guardian, username: str, password: str, temporary: bool = False) -> Guardian:
    await validate_new_account(guardian, guardian.dni, username, password)

    role = next((r for r in await roleService.get_all() if r.name == "guardian" and r.is_active), None)

    if role is None:
        raise GuardianValidationError("No existe el rol guardian activo")

    user = await userService.create(
        User(
            id=uuid4(),
            username=username,
            password_hash=hash_password(password),
            role_id=role.id,
            full_name=guardian.full_name,
            dni=guardian.dni,
            phone=guardian.phone,
            email=guardian.email,
        )
    )

    if temporary:
        await userRepository.mark_temporary(user.id)

    return await guardianRepository.update(replace(guardian, user_id=user.id))
