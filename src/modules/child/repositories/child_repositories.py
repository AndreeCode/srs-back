from .child_create_repository import create_child
from .child_delete_repository import delete_child
from .child_get_all_repository import get_all_children
from .child_get_by_id_repository import get_child_by_id
from .child_update_repository import update_child


class ChildRepository:
    create = staticmethod(create_child)
    get_all = staticmethod(get_all_children)
    get_by_id = staticmethod(get_child_by_id)
    update = staticmethod(update_child)
    delete = staticmethod(delete_child)


childRepository = ChildRepository()
