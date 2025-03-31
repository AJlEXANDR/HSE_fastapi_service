from pydantic import EmailStr, constr
from uuid import UUID
from datetime import datetime
from typing import Optional
from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRead(schemas.BaseUser):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserLogin(schemas.BaseUserCreate):
    pass


class Token(schemas.BaseModel):
    access_token: str
    token_type: str = "bearer"