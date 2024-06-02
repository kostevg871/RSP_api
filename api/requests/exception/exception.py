from fastapi import HTTPException

from core.init import InitRSP

# check mode calculation


def in_mode_on_substance(substaneces_objects_globals: InitRSP, substanceId: int, mode: str) -> HTTPException | None:
    if mode not in substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=441,
                            detail={"error_message": "mode={mode} not in substance".format(mode=mode),
                                    "available_modes": substaneces_objects_globals.substances_calc_modes_id[substanceId],
                                    "status_code": 441})
