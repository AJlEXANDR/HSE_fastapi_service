from fastapi import FastAPI, Depends
from src.auth.users import auth_backend, current_active_user, fastapi_users
from src.auth.schemas import UserCreate, UserRead
from src.auth.db import User
from src.links.router import router as links_router
from src.auth.router import router as auth_router
from src.config import settings
from src.links.public_router import public_router

import uvicorn


app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(auth_router)
app.include_router(links_router)
app.include_router(public_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", log_level="info")