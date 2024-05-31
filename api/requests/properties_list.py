from fastapi import HTTPException
from core.init import InitRSP
from schemas import Property


def properties_list(substaneces_objects_globals: InitRSP,
                    substanceId: int, modeId: str) -> Property:
    mode = modeId.upper()

    if mode not in substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=400,
                            detail="mode=" +
                            mode + " not in substance")

    return {"data": substaneces_objects_globals.properties[substanceId][mode]}
