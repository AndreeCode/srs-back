from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.child_guardian_domain import ChildGuardian
from ..services.child_guardians_service import childGuardianService


class ChildGuardianUpdateRequest(BaseModel):
    relationship: str = Field(min_length=1, max_length=50)


async def update_child_guardian_handler(child_id: str, guardian_id: str, body: ChildGuardianUpdateRequest):
    try:
        child_uuid = parse_uuid(child_id, "child_id")
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")

        child_guardian = ChildGuardian(
            child_id=child_uuid,
            guardian_id=guardian_uuid,
            relationship=body.relationship,
        )

        updated = await childGuardianService.update(child_guardian)

        if updated is None:
            return error(404, "Vinculo no encontrado", ValueError(f"child_id={child_id} guardian_id={guardian_id}"))

        return success(200, "Vinculo actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al actualizar el vinculo", err)
