from pydantic import BaseModel

# Ошибка с описанием


class Schemas_exc_400_create_user(BaseModel):
    code: float
    type: str
    error_info: str
    msg_user_ru: str
    msg_user_en: str
    request_info: dict | None = None


model_exc_400 = {
    "model": Schemas_exc_400_create_user,
}
