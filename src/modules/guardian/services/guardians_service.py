from .guardian_account_service import check_account, create_account
from .guardian_create_service import create
from .guardian_delete_service import delete
from .guardian_get_all_service import get_all
from .guardian_get_by_id_service import get_by_id
from .guardian_link_child_service import attach_child, find_child, link_child
from .guardian_register_service import register
from .guardian_update_service import update


class GuardianService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)
    check_account = staticmethod(check_account)
    create_account = staticmethod(create_account)
    find_child = staticmethod(find_child)
    attach_child = staticmethod(attach_child)
    link_child = staticmethod(link_child)
    register = staticmethod(register)


guardianService = GuardianService()
