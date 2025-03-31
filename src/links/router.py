from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import AnyHttpUrl
from typing import Optional

from src.links.schemas import (
    ShortURLCreate,
    ShortURLResponse,
    ShortURLUpdate,
    ShortURLStats,
    ShortURLSearchResult,
)
from src.models import ShortURL
from src.database import get_async_session
from src.auth.users import current_active_user, optional_user
from src.models import User
from src.config import settings

import random
import string
from datetime import datetime, timezone
from uuid import UUID


router = APIRouter(
    prefix="/links",
    tags=["links"],
)

def generate_short_code(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@router.post("/shorten", response_model=ShortURLResponse)
async def create_short_url(
    data: ShortURLCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(optional_user)
):
    if data.custom_alias:
        result = await session.execute(select(ShortURL).where(ShortURL.custom_alias == data.custom_alias))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Alias already exists")
        short_code = data.custom_alias
    else:
        while True:
            short_code = generate_short_code()
            result = await session.execute(select(ShortURL).where(ShortURL.short_code == short_code))
            if not result.scalars().first():
                break

    short_url = ShortURL(
        original_url=data.original_url,
        short_code=short_code,
        custom_alias=data.custom_alias,
        expires_at=data.expires_at,
        created_at=datetime.now(timezone.utc),
        owner_id=user.id if user else None
    )

    session.add(short_url)
    await session.commit()
    await session.refresh(short_url)
    return ShortURLResponse.model_validate(
        short_url,
        context={"base_url": str(request.base_url)}
    )


@router.get("/search", response_model=list[ShortURLSearchResult])
async def search_by_original_url(
    original_url: Optional[str] = Query(None, description="Original URL to search for"),
    session: AsyncSession = Depends(get_async_session)
):
    normalized_url = original_url.rstrip("/")
    
    result = await session.execute(select(ShortURL).where(ShortURL.original_url == normalized_url))
    links = result.scalars().all()

    if not links:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return links


@router.get("/{short_code}")
async def redirect_to_original(
    short_code: str,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(ShortURL).where(ShortURL.short_code == short_code))
    link = result.scalars().first()

    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if link.expires_at and link.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Short URL expired")

    link.clicks += 1
    link.last_clicked = datetime.now(timezone.utc)
    await session.commit()

    return RedirectResponse(url=link.original_url)


@router.put("/{short_code}", response_model=ShortURLResponse)
async def update_short_url(
    short_code: str,
    data: ShortURLUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(ShortURL).where(ShortURL.short_code == short_code))
    link = result.scalars().first()

    if not link or link.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized or link not found")

    if data.original_url:
        link.original_url = data.original_url
    if data.custom_alias:
        link.custom_alias = data.custom_alias
        link.short_code = data.custom_alias
    if data.expires_at:
        link.expires_at = data.expires_at

    await session.commit()
    await session.refresh(link)

    return ShortURLResponse.model_validate(
        link,
        context={"base_url": settings.BASE_URL}
    )


@router.delete("/{short_code}")
async def delete_short_url(
    short_code: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(ShortURL).where(ShortURL.short_code == short_code))
    link = result.scalars().first()

    if not link or link.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized or link not found")

    await session.delete(link)
    await session.commit()

    return {"detail": "Short URL deleted"}


@router.get("/{short_code}/stats", response_model=ShortURLStats)
async def get_stats(
    short_code: str,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(ShortURL).where(ShortURL.short_code == short_code))
    link = result.scalars().first()

    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return link