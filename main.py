
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.handlers.users.main import user_router


from init import InitRSP
from schemas import *

import rsp


# api
app = FastAPI(
    title="RSP api"
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://real-substance-properties.netlify.app",
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS",
                                  "DELETE", "PATCH", "PUT"],
                   allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                                  "Authorization"],)

app.substaneces_objects_globals = InitRSP()

substance_router = APIRouter()


@substance_router.get("/getAvailableSubstances", response_model=AvailableSubstance, description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    return {"data": app.substaneces_objects_globals.data_get_substances_list}


@substance_router.get("/getCalcModesInfo", response_model=ParameterMode, description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: str) -> ParameterMode:
    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}


@substance_router.get("/getPropertiesLists", response_model=Property,  description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId: str, modeId: str) -> Property:
    return {"data": app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]}


@substance_router.post("/getPropertiesTableRow", response_model=PropertyRowTableResponse, description="Запрос для получения строки таблицы по параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyRowTableResponse:
    val = rsp.callProperty(
        app.substaneces_objects_globals.substances_objects[int(
            request.substanceId)],
        request.params.propertyId,
        request.modeId,
        request.params.value)

    return {
        "data":
        {
            "dimensionId": "SI",
            "property": str(app.substaneces_objects_globals.properties[int(request.substanceId)][str(request.modeId)][request.params.propertyId]),
            "value": val
        }
    }


@substance_router.post("/getPropertiesTable", response_model=PropertyTableResponse, description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(substanceId: str, modeId: str, parameters: list[float]) -> PropertyTableResponse:
    results = dict(zip(
        app.substaneces_objects_globals.properties[int(
            substanceId)][str(modeId)],
        [None] * len(app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)])))
    for prop in app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]:
        results[str(prop)] = rsp.callProperty(
            app.substaneces_objects_globals.substances_objects[int(
                substanceId)],
            prop,
            modeId,
            parameters
        )

    print(results)

    return {"data": results}


main_api_router = APIRouter()
main_api_router.include_router(user_router, tags=["user"])
main_api_router.include_router(
    substance_router, tags=["substance"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
