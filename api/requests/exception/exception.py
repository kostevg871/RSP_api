from fastapi import HTTPException

from core.init import InitRSP
from helpers.constants import PROPERTY_AVAILABE_DIM

# check mode calculation


def in_mode_on_substance(substaneces_objects_globals: InitRSP, substanceId: int, mode: str) -> None:
    if mode not in substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=441,
                            detail={"error_message": "mode={mode} not in substance".format(mode=mode),
                                    "available_modes": substaneces_objects_globals.substances_calc_modes_id[substanceId],
                                    "status_code": 441})

# check count substance_id


def check_count_substance_id(substanceId: int, count_substance: int) -> None:
    if substanceId < 0 or substanceId > count_substance-1:
        raise HTTPException(status_code=400, detail="substanceId = {substanceId} be in the range from 0 to {count_substance}".format(
            substanceId=substanceId, count_substance=count_substance-1))

# check property


def check_property(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, property: list[str]) -> None:
    if not property in substaneces_objects_globals.properties[substanceId][mode]:
        raise HTTPException(status_code=443,
                            detail={"error_message": "property= {property} not in substance".format(property=property),
                                    "available_property_dimensions": list(substaneces_objects_globals.properties[substanceId][mode]),
                                    "status_code": 443})
