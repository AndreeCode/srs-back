from ..domain.child_control_domain import ChildControl
from ..repositories.child_control_repositories import childControlRepository
from .child_control_validate_service import validate_child_control


async def update(child_control: ChildControl, current: ChildControl) -> ChildControl | None:
    await validate_child_control(
        child_control,
        is_new=False,
        facility_changed=child_control.health_facility_id != current.health_facility_id,
    )
    return await childControlRepository.update(child_control)
