from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from src.models import User
from src.auth.db import get_user_db
from src.config import settings

from uuid import UUID

from typing import Optional


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET_KEY, 
        lifetime_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret=settings.JWT_SECRET_KEY
    verification_token_secret=settings.JWT_SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Пользователь зарегистрирован: {user.email}")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Пользователь запросил сброс пароля: {user.email}, токен: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Пользователь запросил верификацию: {user.email}, токен: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
optional_user = fastapi_users.current_user(optional=True)