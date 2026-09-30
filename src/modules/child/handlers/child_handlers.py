from .child_create_handler import create_child_handler
from .child_delete_handler import delete_child_handler
from .child_get_all_handler import get_all_children_handler
from .child_get_by_id_handler import get_child_by_id_handler
from .child_update_handler import update_child_handler


class ChildHandler:
    create = staticmethod(create_child_handler)
    get_all = staticmethod(get_all_children_handler)
    get_by_id = staticmethod(get_child_by_id_handler)
    update = staticmethod(update_child_handler)
    delete = staticmethod(delete_child_handler)


childHandler = ChildHandler()
