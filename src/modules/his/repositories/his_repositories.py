from .his_attentions_get_repository import get_his_attentions
from .his_children_find_repository import find_his_children
from .his_rules_get_all_repository import get_all_his_rules


class HisRepository:
    find_children = staticmethod(find_his_children)
    get_attentions = staticmethod(get_his_attentions)
    get_rules = staticmethod(get_all_his_rules)


hisRepository = HisRepository()
