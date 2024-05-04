from typing import Union

from fastapi import FastAPI

from calculations.router import router as router_calculation


app = FastAPI(
    title="RSP App"
)


@app.get("/")
def start():
    return {"info": "Сервер работает!"}


app.include_router(router_calculation)
