from .child_control_create_service import create
from .child_control_delete_service import delete
from .child_control_get_all_service import get_all
from .child_control_get_by_id_service import get_by_id
from .child_control_update_service import update


class ChildControlService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


childControlService = ChildControlService()
