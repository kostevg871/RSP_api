from src.api.substances_calc.requests.verification_data.verification import check_count_substance_id, in_mode_on_substance
from src.core.init import InitRSP
from schemas import Property


def properties_list(substaneces_objects_globals: InitRSP,
                    substanceId: int, modeId: str) -> Property:

    count_substance = len(
        substaneces_objects_globals.data_get_substances_list)

    check_count_substance_id(substanceId=substanceId,
                             count_substance=count_substance)

    mode = modeId.upper()

    in_mode_on_substance(substaneces_objects_globals, substanceId, mode)

    return {"data": substaneces_objects_globals.properties[substanceId][mode]}
