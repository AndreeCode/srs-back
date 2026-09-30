from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.role_domain import Role, RoleName
from ..services.roles_service import roleService


class RoleUpdateRequest(BaseModel):
    name: Optional[RoleName] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[list[UUID]] = None


async def update_role_handler(role_id: str, body: RoleUpdateRequest):
    try:
        role_uuid = parse_uuid(role_id, "role_id")
        current = await roleService.get_by_id(role_uuid)

        if current is None:
            return error(404, "Rol no encontrado", ValueError(f"role_id={role_id}"))

        role = Role(
            id=current.id,
            name=body.name if body.name is not None else current.name,
            is_active=body.is_active if body.is_active is not None else current.is_active,
            permission_ids=(
                list(dict.fromkeys(body.permission_ids))
                if body.permission_ids is not None
                else current.permission_ids
            ),
        )

        updated = await roleService.update(role)

        if updated is None:
            return error(404, "Rol no encontrado", ValueError(f"role_id={role_id}"))

        return success(200, "Rol actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un rol con ese nombre", err)

    except ForeignKeyViolationError as err:
        return error(400, "Alguno de los permission_ids indicados no existe", err)

    except Exception as err:
        return error(500, "Error al actualizar el rol", err)
