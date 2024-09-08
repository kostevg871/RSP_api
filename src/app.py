from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import uvicorn

from src.api.users.router_users import router_users
from src.api.auth.router_auth import router_auth
from src.api.substances_calc.substances import router_substances
from src.api.substances_calc.response_model import model_error_422

http_bearer = HTTPBearer(auto_error=False)

app = FastAPI(
    title="RSP App",
    dependencies=[Depends(http_bearer)],
    responses={422: model_error_422}
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": {
                "status_code": 422,
                "description": exc.errors()[0]["msg"],
                # "error": exc.errors()[0]["ctx"]["error"],
                "msg": "Не правильно введены данные!",
            }
        })
    )

# CORS settings
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://real-substance-properties.netlify.app",
    "https://rsp-api.ru"
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS",
                                  "DELETE", "PATCH", "PUT"],
                   allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                                  "Authorization"],)

# Endpoints (routers)
app.include_router(router=router_substances)

# Добавление ручек users
app.include_router(router=router_auth)
app.include_router(router=router_users)
