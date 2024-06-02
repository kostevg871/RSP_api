from fastapi import HTTPException
from api.requests.exception.exception import in_mode_on_substance
from core.init import InitRSP
from schemas import Property


def properties_list(substaneces_objects_globals: InitRSP,
                    substanceId: int, modeId: str) -> Property:
    mode = modeId.upper()

    in_mode_on_substance(substaneces_objects_globals, substanceId, mode)

    return {"data": substaneces_objects_globals.properties[substanceId][mode]}
