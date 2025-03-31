from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone

from src.models import ShortURL
from src.database import get_async_session

public_router = APIRouter()

@public_router.get("/{short_code}", include_in_schema=False)
async def public_redirect(
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
