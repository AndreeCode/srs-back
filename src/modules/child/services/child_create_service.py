from ..domain.child_domain import Child
from ..repositories.child_repositories import childRepository
from .child_validate_service import validate_child, validate_health_facility


async def create(child: Child) -> Child:
    validate_child(child)
    await validate_health_facility(child.health_facility_id)
    return await childRepository.create(child)
