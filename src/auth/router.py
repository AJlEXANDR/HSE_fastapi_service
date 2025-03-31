from fastapi import APIRouter
from src.auth.users import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate


router = APIRouter(prefix="/auth", tags=["auth"])


auth_router = fastapi_users.get_auth_router(auth_backend)
auth_router.routes = [
    route for route in auth_router.routes if route.path == "/login"
]
for route in auth_router.routes:
    route.operation_id = "auth_jwt_login"
router.include_router(auth_router, prefix="/jwt")


register_router = fastapi_users.get_register_router(UserRead, UserCreate)
register_router.routes = [
    route for route in register_router.routes if route.path == ""
]
for route in register_router.routes:
    route.operation_id = "auth_register"
router.include_router(register_router, prefix="/jwt")


users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if "/me" in route.path
]
for route in users_router.routes:
    if route.path.endswith("/me") and route.methods == {"GET"}:
        route.operation_id = "get_current_user"
    elif route.path.endswith("/me") and route.methods == {"PATCH"}:
        route.operation_id = "update_current_user"
router.include_router(users_router, prefix="/users")