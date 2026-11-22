from datetime import date
from uuid import uuid4

from ...user.services.users_service import userService
from ..domain.guardian_domain import Guardian
from ..domain.guardian_errors import GuardianConflictError
from ..repositories.guardian_repositories import guardianRepository
from .guardian_account_service import create_account, validate_new_account
from .guardian_link_child_service import attach_child, find_child_self_service, pending_summary


async def register(
    dni: str,
    full_name: str,
    phone: str | None,
    email: str | None,
    password: str,
    child_identifier: str,
    child_birth_date: date,
    relationship: str,
    ip: str | None = None,
) -> dict:
    guardian = await guardianRepository.get_by_dni(dni)

    if guardian is not None and guardian.user_id is not None:
        raise GuardianConflictError("Ya existe una cuenta para este DNI, inicia sesion con tu DNI y contrasena")

    if guardian is not None and not guardian.active:
        raise GuardianConflictError("Tu registro de padre esta inactivo, acercate a tu establecimiento de salud")

    if await userService.get_by_username(dni) is not None:
        raise GuardianConflictError("Ya existe un usuario con este DNI, inicia sesion")

    await validate_new_account(guardian, dni, dni, password)
    child = await find_child_self_service(child_identifier, child_birth_date, ip, None)

    is_new = guardian is None
    if is_new:
        guardian = await guardianRepository.create(
            Guardian(id=uuid4(), full_name=full_name, dni=dni, phone=phone, email=email)
        )

    try:
        try:
            await attach_child(guardian, child, relationship, verified=False)
        except GuardianConflictError:
            pass
        guardian = await create_account(guardian, dni, password)
    except Exception:
        if is_new:
            await guardianRepository.discard_new(guardian.id)
        raise

    return {"guardian": guardian.to_dict(), "username": dni, "child": pending_summary(child_identifier, relationship)}
