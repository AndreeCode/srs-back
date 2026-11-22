import re

from ....core.db.sqlserver import SqlServerUnavailableError
from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ...guardian_his_child.services.guardian_his_children_service import guardianHisChildService
from ..services.his_service import hisService


async def child_handler(document_number: str):
    try:
        if not re.fullmatch(r"\d{8}", document_number):
            return error(400, "El DNI o CNV debe tener 8 digitos", ValueError(document_number))

        data = await hisService.followup([{"document_number": document_number}], with_attentions=True)

        if not data["children"]:
            return error(404, f"No hay ningun nino con documento {document_number} en HIS-MINSA", ValueError(document_number))

        child = data["children"][0]
        links = await guardianHisChildService.get_all(None, document_number)
        return success(
            200,
            "Nino encontrado en HIS-MINSA",
            {
                "child": child,
                "controls": data["controls"],
                "attentions": data["attentions"].get(child["id"], []),
                "links": [link.to_dict() for link in links],
            },
        )

    except SqlServerUnavailableError as err:
        return error(503, str(err), err)

    except Exception as err:
        return error(500, "Error al consultar HIS-MINSA", err)


async def guardian_handler(guardian_id: str):
    try:
        links = await guardianHisChildService.get_all(parse_uuid(guardian_id, "guardian_id"), None)
        data = await hisService.followup([link.to_dict() for link in links])
        return success(200, "Hijos de HIS-MINSA obtenidos correctamente", {"children": data["children"], "controls": data["controls"]})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except SqlServerUnavailableError as err:
        return error(503, str(err), err)

    except Exception as err:
        return error(500, "Error al consultar HIS-MINSA", err)
