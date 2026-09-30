from ...child.services.children_service import childService
from ...guardian.services.guardians_service import guardianService
from ..domain.child_guardian_domain import ChildGuardian
from ..domain.child_guardian_errors import ChildGuardianValidationError
from ..repositories.child_guardian_repositories import childGuardianRepository


async def create(child_guardian: ChildGuardian) -> ChildGuardian:
    child = await childService.get_by_id(child_guardian.child_id)

    if child is None:
        raise ChildGuardianValidationError("El child_id indicado no existe")

    if not child.active:
        raise ChildGuardianValidationError("El nino indicado esta inactivo")

    guardian = await guardianService.get_by_id(child_guardian.guardian_id)

    if guardian is None:
        raise ChildGuardianValidationError("El guardian_id indicado no existe")

    if not guardian.active:
        raise ChildGuardianValidationError("El apoderado indicado esta inactivo")

    return await childGuardianRepository.create(child_guardian)
