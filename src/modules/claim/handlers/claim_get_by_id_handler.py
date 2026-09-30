from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.claims_service import claimService


async def get_claim_by_id_handler(claim_id: str):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id")
        claim = await claimService.get_by_id(claim_uuid)

        if claim is None:
            return error(404, "Reclamo no encontrado", ValueError(f"claim_id={claim_id}"))

        return success(200, "Reclamo obtenido correctamente", claim.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el reclamo", err)
