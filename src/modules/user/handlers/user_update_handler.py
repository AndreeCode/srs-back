from datetime import datetime
from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ....core.security.access_error import AccessDeniedError
from ....core.security.password import hash_password
from ..domain.user_domain import User
from ..domain.user_errors import UserValidationError
from ..services.users_service import userService


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[UUID] = None
    full_name: Optional[str] = None
    dni: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    terms_accepted: Optional[bool] = None
    terms_version: Optional[str] = None
    terms_accepted_at: Optional[datetime] = None
    active: Optional[bool] = None
    blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None
    region_ids: Optional[list[UUID]] = None


async def update_user_handler(caller_id: UUID, user_id: str, body: UserUpdateRequest):
    try:
        user_uuid = parse_uuid(user_id, "user_id")
        current = await userService.get_by_id(user_uuid)

        if current is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={user_id}"))

        user = User(
            id=current.id,
            username=body.username if body.username is not None else current.username,
            password_hash=hash_password(body.password) if body.password else current.password_hash,
            role_id=body.role_id if body.role_id is not None else current.role_id,
            full_name=body.full_name if body.full_name is not None else current.full_name,
            dni=body.dni if body.dni is not None else current.dni,
            phone=body.phone if body.phone is not None else current.phone,
            email=body.email if body.email is not None else current.email,
            terms_accepted=body.terms_accepted if body.terms_accepted is not None else current.terms_accepted,
            terms_version=body.terms_version if body.terms_version is not None else current.terms_version,
            terms_accepted_at=body.terms_accepted_at if body.terms_accepted_at is not None else current.terms_accepted_at,
            active=body.active if body.active is not None else current.active,
            blocked=body.blocked if body.blocked is not None else current.blocked,
            blocked_reason=body.blocked_reason if body.blocked_reason is not None else current.blocked_reason,
            region_ids=list(dict.fromkeys(body.region_ids)) if body.region_ids is not None else current.region_ids,
        )

        updated = await userService.update(caller_id, user, current)

        if updated is None:
            return error(404, "Usuario no encontrado", ValueError(f"user_id={user_id}"))

        return success(200, "Usuario actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except AccessDeniedError as err:
        return error(403, str(err), err)

    except UniqueViolationError as err:
        return error(409, "El nombre de usuario ya existe", err)

    except UserValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        if err.constraint_name == "user_region_region_id_fkey":
            return error(400, "Alguna de las region_ids indicadas no existe", err)
        return error(400, "El role_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al actualizar el usuario", err)
