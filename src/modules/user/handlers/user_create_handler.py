from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel

from ....core.http.error import error
from ....core.http.succes import success
from ....core.security.access_error import AccessDeniedError
from ....core.security.password import hash_password
from ....core.security.password_policy import PasswordPolicyError, ensure_strong_password
from ..domain.user_domain import User
from ..domain.user_errors import UserValidationError
from ..services.users_service import userService


class UserCreateRequest(BaseModel):
    username: str
    password: str
    role_id: UUID
    full_name: str
    dni: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    terms_accepted: bool = False
    terms_version: Optional[str] = None
    terms_accepted_at: Optional[datetime] = None
    region_ids: list[UUID] = []


async def create_user_handler(caller_id: UUID, body: UserCreateRequest):
    try:
        ensure_strong_password(body.password, body.username, body.dni, body.full_name, body.email)
        user = User(
            id=uuid4(),
            username=body.username,
            password_hash=hash_password(body.password),
            role_id=body.role_id,
            full_name=body.full_name,
            dni=body.dni,
            phone=body.phone,
            email=body.email,
            terms_accepted=body.terms_accepted,
            terms_version=body.terms_version,
            terms_accepted_at=body.terms_accepted_at,
            region_ids=list(dict.fromkeys(body.region_ids)),
        )

        created = await userService.create(user, caller_id)
        return success(201, "Usuario creado correctamente", created.to_dict())

    except AccessDeniedError as err:
        return error(403, str(err), err)

    except PasswordPolicyError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "El nombre de usuario ya existe", err)

    except UserValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        if err.constraint_name == "user_region_region_id_fkey":
            return error(400, "Alguna de las region_ids indicadas no existe", err)
        return error(400, "El role_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al crear el usuario", err)
