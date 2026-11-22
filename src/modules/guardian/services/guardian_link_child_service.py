from datetime import date

from ...child.domain.child_domain import Child
from ...child.repositories.child_repositories import childRepository
from ...child_guardian.domain.child_guardian_domain import ChildGuardian
from ...child_guardian.repositories.child_guardian_repositories import childGuardianRepository
from ...guardian_his_child.domain.guardian_his_child_domain import GuardianHisChild
from ...guardian_his_child.repositories.guardian_his_child_repositories import guardianHisChildRepository
from ...his.domain.his_domain import HisChild
from ...his.services.his_service import hisService
from ..domain.guardian_domain import Guardian
from ..domain.guardian_errors import GuardianChildNotFoundError, GuardianConflictError


async def find_child(identifier: str, birth_date: date) -> Child | HisChild:
    identifier = identifier.strip()
    child = await childRepository.find_by_identifier(identifier, birth_date)

    if child is not None:
        return child

    his_child = await hisService.find_child(identifier, birth_date) if identifier.isdigit() and len(identifier) == 8 else None

    if his_child is None:
        raise GuardianChildNotFoundError(
            "No encontramos a ningun nino con ese DNI o codigo de padron y esa fecha de nacimiento"
        )

    return his_child


def summary(child: Child | HisChild, relationship: str) -> dict:
    if isinstance(child, HisChild):
        return {
            "source": "his",
            "id": child.portal_id,
            "padron_code": child.document_number,
            "full_name": f"{child.document_type} {child.document_number}",
            "birth_date": child.birth_date.isoformat(),
            "relationship": relationship,
        }

    return {
        "source": "sicna",
        "id": str(child.id),
        "padron_code": child.padron_code,
        "full_name": f"{child.first_names} {child.last_names}",
        "birth_date": child.birth_date.isoformat(),
        "relationship": relationship,
    }


async def attach_child(guardian: Guardian, child: Child | HisChild, relationship: str) -> dict:
    if isinstance(child, HisChild):
        created = await guardianHisChildRepository.create(
            GuardianHisChild(
                guardian_id=guardian.id,
                document_number=child.document_number,
                birth_date=child.birth_date,
                relationship=relationship,
                linked_by=guardian.user_id,
            )
        )
        if created is None:
            raise GuardianConflictError("Ese nino ya esta vinculado a tu cuenta")
        return summary(child, relationship)

    if await childGuardianRepository.get_by_id(child.id, guardian.id) is not None:
        raise GuardianConflictError("Ese nino ya esta vinculado a tu cuenta")

    await childGuardianRepository.create(ChildGuardian(child_id=child.id, guardian_id=guardian.id, relationship=relationship))
    return summary(child, relationship)


async def link_child(guardian: Guardian, identifier: str, birth_date: date, relationship: str) -> dict:
    child = await find_child(identifier, birth_date)
    return await attach_child(guardian, child, relationship)
