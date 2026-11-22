from .guardian_his_child_create_service import create
from ..repositories.guardian_his_child_repositories import guardianHisChildRepository


class GuardianHisChildService:
    create = staticmethod(create)
    get_all = staticmethod(guardianHisChildRepository.get_all)
    update = staticmethod(guardianHisChildRepository.update)
    delete = staticmethod(guardianHisChildRepository.delete)


guardianHisChildService = GuardianHisChildService()
