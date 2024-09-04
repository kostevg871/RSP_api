from fastapi_users.authentication import AuthenticationBackend
from src.core.authentication.transpors import bearer_transport
from src.core.authentication.strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
