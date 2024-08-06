from src.core.init import InitRSP
from src.schemas import AvailableSubstance


def available_substances(substaneces_objects: InitRSP) -> AvailableSubstance:
    return {"data": substaneces_objects.data_get_substances_list}
