from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.role_domain import Role, RoleName
from ..services.roles_service import roleService


class RoleCreateRequest(BaseModel):
    name: RoleName
    permission_ids: list[UUID] = []


async def create_role_handler(body: RoleCreateRequest):
    try:
        role = Role(id=uuid4(), name=body.name, permission_ids=list(dict.fromkeys(body.permission_ids)))
        created = await roleService.create(role)
        return success(201, "Rol creado correctamente", created.to_dict())

    except UniqueViolationError as err:
        return error(409, "Ya existe un rol con ese nombre", err)

    except ForeignKeyViolationError as err:
        return error(400, "Alguno de los permission_ids indicados no existe", err)

    except Exception as err:
        return error(500, "Error al crear el rol", err)
