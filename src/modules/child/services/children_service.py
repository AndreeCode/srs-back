from .child_create_service import create
from .child_delete_service import delete
from .child_get_all_service import get_all
from .child_get_by_id_service import get_by_id
from .child_update_service import update


class ChildService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


childService = ChildService()
