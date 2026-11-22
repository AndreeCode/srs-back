from .guardian_his_child_create_repository import create_guardian_his_child
from .guardian_his_child_delete_repository import delete_guardian_his_child
from .guardian_his_child_get_all_repository import get_all_guardian_his_children
from .guardian_his_child_update_repository import update_guardian_his_child


class GuardianHisChildRepository:
    create = staticmethod(create_guardian_his_child)
    get_all = staticmethod(get_all_guardian_his_children)
    update = staticmethod(update_guardian_his_child)
    delete = staticmethod(delete_guardian_his_child)


guardianHisChildRepository = GuardianHisChildRepository()
