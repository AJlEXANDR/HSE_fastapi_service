from pydantic import BaseModel, HttpUrl, Field, field_serializer, field_validator
from uuid import UUID
from typing import Optional
from datetime import datetime
from urllib.parse import urlparse


class ShortURLCreate(BaseModel):
    original_url: str
    custom_alias: Optional[str] = Field(default=None, min_length=3, max_length=30)
    expires_at: Optional[datetime] = None

    @field_validator("original_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        return v.rstrip("/")


class ShortURLUpdate(BaseModel):
    original_url: Optional[str] = None
    custom_alias: Optional[str] = Field(default=None, min_length=3, max_length=30)
    expires_at: Optional[datetime] = None

    @field_validator("original_url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        return v.rstrip("/")


class ShortURLResponse(BaseModel):
    id: UUID
    short_code: str
    original_url: str
    custom_alias: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    short_url: Optional[str] = None

    class Config:
        from_attributes = True

    @field_serializer("short_url", when_used="always")
    def build_short_url(self, v, info):
        base_url = info.context.get("base_url") if info.context else "http://localhost:8000"
        return f"{base_url.rstrip('/')}/{self.short_code}"


class ShortURLStats(BaseModel):
    original_url: str
    clicks: int
    created_at: datetime
    last_clicked: Optional[datetime]
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class ShortURLSearchResult(BaseModel):
    id: UUID
    short_code: str
    original_url: str
    custom_alias: Optional[str]
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True