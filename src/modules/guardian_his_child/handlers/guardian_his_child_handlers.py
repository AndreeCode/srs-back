from datetime import date
from typing import Literal, Optional

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.db.sqlserver import SqlServerUnavailableError
from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.guardian_his_child_domain import GuardianHisChild
from ..domain.guardian_his_child_errors import GuardianHisChildConflictError, GuardianHisChildValidationError
from ..services.guardian_his_children_service import guardianHisChildService

Relationship = Literal["Madre", "Padre", "Abuelo(a)", "Tío(a)", "Hermano(a)", "Apoderado"]
Document = Field(pattern=r"^\d{8}$")


class GuardianHisChildCreateRequest(BaseModel):
    guardian_id: str
    document_number: str = Document
    birth_date: date
    relationship: Relationship = "Madre"
    child_name: Optional[str] = Field(default=None, max_length=150)


class GuardianHisChildUpdateRequest(BaseModel):
    relationship: Optional[Relationship] = None
    child_name: Optional[str] = Field(default=None, max_length=150)


def clean_name(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(value.split()) or None


async def create_handler(request: Request, body: GuardianHisChildCreateRequest):
    try:
        link = await guardianHisChildService.create(
            GuardianHisChild(
                guardian_id=parse_uuid(body.guardian_id, "guardian_id"),
                document_number=body.document_number,
                birth_date=body.birth_date,
                relationship=body.relationship,
                child_name=clean_name(body.child_name),
                linked_by=parse_uuid(request.state.user["sub"], "sub"),
            )
        )
        return success(201, "Nino de HIS-MINSA vinculado al padre correctamente", link.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except GuardianHisChildValidationError as err:
        return error(400, str(err), err)

    except GuardianHisChildConflictError as err:
        return error(409, str(err), err)

    except SqlServerUnavailableError as err:
        return error(503, str(err), err)

    except Exception as err:
        return error(500, "Error al vincular el nino de HIS-MINSA", err)


async def get_all_handler(guardian_id: str | None, document_number: str | None):
    try:
        guardian_uuid = parse_uuid(guardian_id, "guardian_id") if guardian_id else None
        links = await guardianHisChildService.get_all(guardian_uuid, document_number)
        return list_response(200, "Vinculos con HIS-MINSA obtenidos correctamente", [link.to_dict() for link in links])

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los vinculos con HIS-MINSA", err)


async def update_handler(guardian_id: str, document_number: str, body: GuardianHisChildUpdateRequest):
    try:
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")
        current = next(iter(await guardianHisChildService.get_all(guardian_uuid, document_number)), None)

        if current is None:
            return error(404, "Vinculo no encontrado", ValueError(f"guardian_id={guardian_id} document={document_number}"))

        if "relationship" in body.model_fields_set and body.relationship:
            current.relationship = body.relationship
        if "child_name" in body.model_fields_set:
            current.child_name = clean_name(body.child_name)

        updated = await guardianHisChildService.update(current)
        return success(200, "Vinculo actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al actualizar el vinculo", err)


async def delete_handler(guardian_id: str, document_number: str):
    try:
        result = await guardianHisChildService.delete(parse_uuid(guardian_id, "guardian_id"), document_number)

        if result == "not_found":
            return error(404, "Vinculo no encontrado", ValueError(f"guardian_id={guardian_id} document={document_number}"))

        return success(200, "Nino de HIS-MINSA desvinculado del padre")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al desvincular el nino", err)


class GuardianHisChildHandler:
    create = staticmethod(create_handler)
    get_all = staticmethod(get_all_handler)
    update = staticmethod(update_handler)
    delete = staticmethod(delete_handler)


guardianHisChildHandler = GuardianHisChildHandler()
