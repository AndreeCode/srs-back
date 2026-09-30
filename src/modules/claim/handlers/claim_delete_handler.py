from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.claims_service import claimService


async def delete_claim_handler(claim_id: str):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id")
        result = await claimService.delete(claim_uuid)

        if result == "not_found":
            return error(404, "Reclamo no encontrado", ValueError(f"claim_id={claim_id}"))

        return success(200, "Reclamo eliminado correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar el reclamo", err)
