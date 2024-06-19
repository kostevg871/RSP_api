from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn


from src.api.substances_calc.substances import router_substances
from src.api.substances_calc.response_model import model_error_422

app = FastAPI(
    title="RSP App",
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
                "msg": "Не правильно введены данные!",
            }
        })
    )

# CORS settings
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

# Endpoints (routers)
app.include_router(router=router_substances)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
