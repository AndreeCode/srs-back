from .child_control_create_repository import create_child_control
from .child_control_delete_repository import delete_child_control
from .child_control_get_all_repository import get_all_child_controls
from .child_control_get_by_id_repository import get_child_control_by_id
from .child_control_update_repository import update_child_control


class ChildControlRepository:
    create = staticmethod(create_child_control)
    get_all = staticmethod(get_all_child_controls)
    get_by_id = staticmethod(get_child_control_by_id)
    update = staticmethod(update_child_control)
    delete = staticmethod(delete_child_control)


childControlRepository = ChildControlRepository()
