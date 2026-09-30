from ..domain.child_control_domain import ChildControl
from ..repositories.child_control_repositories import childControlRepository
from .child_control_validate_service import validate_child_control


async def create(child_control: ChildControl) -> ChildControl:
    await validate_child_control(child_control, is_new=True, facility_changed=True)
    return await childControlRepository.create(child_control)
