import re
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.guardian_pending_link_service import approve_pending_link, get_pending_links, reject_pending_link


class PendingLinkRequest(BaseModel):
    source: Literal["sicna", "his"]
    guardian_id: UUID
    child_key: str = Field(min_length=1, max_length=50)


def validate_key(body: PendingLinkRequest) -> str:
    if body.source == "sicna":
        return str(parse_uuid(body.child_key, "child_key"))
    if not re.fullmatch(r"\d{8}", body.child_key):
        raise InvalidUUIDError("child_key debe ser el DNI de 8 digitos del nino de HIS")
    return body.child_key


def serialize(row: dict) -> dict:
    return {
        **row,
        "guardian_id": str(row["guardian_id"]),
        "child_birth_date": row["child_birth_date"].isoformat() if row["child_birth_date"] else None,
        "requested_at": row["requested_at"].isoformat() if row["requested_at"] else None,
    }


async def get_pending_links_handler():
    try:
        rows = await get_pending_links()
        return success(200, "Vinculos pendientes obtenidos correctamente", [serialize(row) for row in rows])

    except Exception as err:
        return error(500, "Error al obtener los vinculos pendientes", err)


async def approve_pending_link_handler(caller_id: UUID, body: PendingLinkRequest):
    try:
        if not await approve_pending_link(body.source, body.guardian_id, validate_key(body), caller_id):
            return error(404, "No hay un vinculo pendiente con esos datos", ValueError(body.model_dump_json()))
        return success(200, "Vinculo verificado: el padre ya puede ver la informacion del nino")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al verificar el vinculo", err)


async def reject_pending_link_handler(body: PendingLinkRequest):
    try:
        if not await reject_pending_link(body.source, body.guardian_id, validate_key(body)):
            return error(404, "No hay un vinculo pendiente con esos datos", ValueError(body.model_dump_json()))
        return success(200, "Solicitud de vinculo rechazada")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al rechazar el vinculo", err)
