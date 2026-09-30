from .child_control_create_handler import create_child_control_handler
from .child_control_delete_handler import delete_child_control_handler
from .child_control_get_all_handler import get_all_child_controls_handler
from .child_control_get_by_id_handler import get_child_control_by_id_handler
from .child_control_update_handler import update_child_control_handler


class ChildControlHandler:
    create = staticmethod(create_child_control_handler)
    get_all = staticmethod(get_all_child_controls_handler)
    get_by_id = staticmethod(get_child_control_by_id_handler)
    update = staticmethod(update_child_control_handler)
    delete = staticmethod(delete_child_control_handler)


childControlHandler = ChildControlHandler()
