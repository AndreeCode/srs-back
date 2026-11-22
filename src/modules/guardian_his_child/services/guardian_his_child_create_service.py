from ...guardian.services.guardians_service import guardianService
from ...his.services.his_service import hisService
from ..domain.guardian_his_child_domain import GuardianHisChild
from ..domain.guardian_his_child_errors import GuardianHisChildConflictError, GuardianHisChildValidationError
from ..repositories.guardian_his_child_repositories import guardianHisChildRepository


async def create(link: GuardianHisChild) -> GuardianHisChild:
    guardian = await guardianService.get_by_id(link.guardian_id)

    if guardian is None:
        raise GuardianHisChildValidationError("El guardian_id indicado no existe")

    if not guardian.active:
        raise GuardianHisChildValidationError("El apoderado indicado esta inactivo")

    child = await hisService.find_child(link.document_number)

    if child is None:
        raise GuardianHisChildValidationError(f"No hay ningun nino con documento {link.document_number} en HIS-MINSA")

    if child.birth_date != link.birth_date:
        raise GuardianHisChildValidationError("La fecha de nacimiento no coincide con la registrada en HIS-MINSA")

    created = await guardianHisChildRepository.create(link)

    if created is None:
        raise GuardianHisChildConflictError("Ese nino ya esta vinculado a este padre")

    return created
