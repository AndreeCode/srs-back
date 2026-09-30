from typing import Optional

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.permission_catalog import PERMISSION_CODE_PATTERN
from ..domain.permission_domain import Permission
from ..services.permissions_service import permissionService


class PermissionUpdateRequest(BaseModel):
    code: Optional[str] = Field(default=None, max_length=100, pattern=PERMISSION_CODE_PATTERN)
    description: Optional[str] = None


async def update_permission_handler(permission_id: str, body: PermissionUpdateRequest):
    try:
        permission_uuid = parse_uuid(permission_id, "permission_id")
        current = await permissionService.get_by_id(permission_uuid)

        if current is None:
            return error(404, "Permiso no encontrado", ValueError(f"permission_id={permission_id}"))

        permission = Permission(
            id=current.id,
            code=body.code if body.code is not None else current.code,
            description=body.description if body.description is not None else current.description,
        )

        updated = await permissionService.update(permission)

        if updated is None:
            return error(404, "Permiso no encontrado", ValueError(f"permission_id={permission_id}"))

        return success(200, "Permiso actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un permiso con ese codigo", err)

    except Exception as err:
        return error(500, "Error al actualizar el permiso", err)
